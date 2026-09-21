#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 2 A-C logistic mixed-effects reanalysis.

Input:
    SR4seq(1).xlsx

What this script does
---------------------
1) Reconstructs the original trial-wise predictors from the workbook.
2) Replaces the original Gaussian LMM with a binomial-logit random-intercept GLMM.
3) Fits:
   A: single-dimensional task
   B: mixed-dimensional task
   C: four congruency × difficulty subsets
4) Writes:
   - Fig2_GLMM_figure_coefficients.csv
   - Fig2_GLMM_all_fixed_effects.csv
   - Fig2_GLMM_model_info.csv

Important implementation note
-----------------------------
The GLMM is fitted by maximum likelihood with Gauss-Hermite quadrature for one
participant-specific random intercept. Fixed-effect standard errors are obtained from
the numerical Hessian of the marginal log-likelihood.

Panel-B variables are reconstructed from the white-cue rows of the SR4 information
sheet because the stored subSR4wCue sheet does not include the original derived
columns "diag" and "chooseF1big".

For panel B, the run variable is centered/z-scored before the original full interaction
is fitted. This does not change the fitted model space; it makes the plotted main effects
refer to the mean run rather than the nonexistent block 0.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import math

import numpy as np
import pandas as pd
import patsy
from numpy.polynomial.hermite import hermgauss
from scipy.optimize import minimize
from scipy.special import logsumexp
from scipy.stats import norm
from statsmodels.tools.numdiff import approx_hess3


def zscale(x):
    x = np.asarray(x, dtype=float)
    return (x - x.mean()) / x.std(ddof=1)


def fit_random_intercept_logit(
    df: pd.DataFrame,
    formula: str,
    group_col: str = "sub",
    n_quad: int = 30,
):
    """Frequentist binomial-logit GLMM with one random intercept.

    Marginal likelihood is evaluated with Gauss-Hermite quadrature:
        y ~ Bernoulli(logit^-1(X beta + b_s))
        b_s ~ N(0, sigma_b^2)
    """
    y_mat, X_df = patsy.dmatrices(formula, df, return_type="dataframe")
    y = np.asarray(y_mat, dtype=float).ravel()
    X = np.asarray(X_df, dtype=float)
    names = list(X_df.design_info.column_names)

    groups = np.asarray(df[group_col])
    unique_groups = np.unique(groups)
    group_indices = [np.where(groups == g)[0] for g in unique_groups]

    # Starting values from a standard logistic GLM when possible.
    try:
        import statsmodels.api as sm
        start_fit = sm.GLM(y, X, family=sm.families.Binomial()).fit()
        beta0 = np.asarray(start_fit.params, dtype=float)
    except Exception:
        beta0 = np.zeros(X.shape[1], dtype=float)

    gh_x, gh_w = hermgauss(n_quad)
    log_gh_w = np.log(gh_w)
    log_sqrt_pi = 0.5 * np.log(np.pi)

    p = X.shape[1]
    theta0 = np.r_[beta0, np.log(0.5)]

    def nll(theta):
        beta = theta[:p]
        sigma = np.exp(theta[p])
        b_nodes = np.sqrt(2.0) * sigma * gh_x

        total = 0.0
        for ind in group_indices:
            eta0 = X[ind] @ beta
            yi = y[ind]

            eta = eta0[None, :] + b_nodes[:, None]
            logp1 = -np.logaddexp(0.0, -eta)
            logp0 = -np.logaddexp(0.0, eta)
            ll_nodes = (yi[None, :] * logp1 + (1.0 - yi[None, :]) * logp0).sum(axis=1)

            total += logsumexp(log_gh_w + ll_nodes) - log_sqrt_pi

        return -total

    opt = minimize(
        nll,
        theta0,
        method="BFGS",
        options={"maxiter": 1000, "gtol": 1e-7},
    )

    if not opt.success:
        alt = minimize(
            nll,
            opt.x,
            method="L-BFGS-B",
            bounds=[(None, None)] * p + [(-8.0, 4.0)],
            options={"maxiter": 2000, "ftol": 1e-12},
        )
        if alt.success or alt.fun < opt.fun:
            opt = alt

    theta = np.asarray(opt.x, dtype=float)

    # Wald covariance from the marginal-likelihood Hessian.
    hess = approx_hess3(theta, nll)
    cov = np.linalg.pinv(hess)
    se_all = np.sqrt(np.clip(np.diag(cov), 0.0, np.inf))

    beta = theta[:p]
    se = se_all[:p]
    z = beta / se
    pval = 2.0 * norm.sf(np.abs(z))
    ci_low = beta - 1.96 * se
    ci_high = beta + 1.96 * se

    fixed = pd.DataFrame(
        {
            "term": names,
            "beta": beta,
            "SE": se,
            "z": z,
            "p": pval,
            "CI_low": ci_low,
            "CI_high": ci_high,
        }
    )

    info = {
        "formula": formula,
        "N_trials": int(len(y)),
        "N_participants": int(len(unique_groups)),
        "random_intercept_SD": float(np.exp(theta[p])),
        "converged": bool(opt.success),
        "optimizer_message": str(opt.message),
        "neg_log_likelihood": float(opt.fun),
        "n_quad": int(n_quad),
    }
    return fixed, info


def reconstruct_data(input_xlsx: Path):
    # The workbook retains its original worksheet name; Unicode escapes keep
    # the public source file ASCII-only without changing the input contract.
    meta = pd.read_excel(input_xlsx, sheet_name="SR4\u4fe1\u606f\u6574\u7406")
    rb = pd.read_excel(input_xlsx, sheet_name="subSR4rbCue").copy()
    wc = pd.read_excel(input_xlsx, sheet_name="subSR4wCue").copy()

    # ---------- Single-dimensional task ----------
    rb_meta = meta[meta["Cuecolor"].isin(["red", "blue"])].reset_index(drop=True)
    rb["trial_in_sub"] = rb.groupby("sub").cumcount() + 1

    if len(rb_meta) != 120:
        raise ValueError(f"Expected 120 red/blue metadata trials, found {len(rb_meta)}.")

    mapped = rb_meta.iloc[rb["trial_in_sub"].to_numpy() - 1].reset_index(drop=True)
    for col in ["Cuecolor", "F1_red", "F1_blue", "F2_red", "F2_blue"]:
        rb[col] = mapped[col].to_numpy()

    # Positive signed difference favors choosing F1.
    red_diff = rb["F2_red"] - rb["F1_red"]
    blue_diff = rb["F2_blue"] - rb["F1_blue"]

    rb["rel"] = np.where(rb["Cuecolor"] == "red", red_diff, blue_diff).astype(float)
    rb["irrel"] = np.where(rb["Cuecolor"] == "red", blue_diff, red_diff).astype(float)
    rb["resp01"] = (rb["resp"] == 1).astype(int)

    # Six single-dimensional runs, 20 trials per run.
    rb["blockrb"] = ((rb["trial_in_sub"] - 1) // 20) + 1
    rb["zsblock"] = zscale(rb["blockrb"])

    rb["congruent"] = np.sign(rb["rel"]) == np.sign(rb["irrel"])
    rb["easy"] = rb["D"] > 1

    # ---------- Mixed-dimensional task ----------
    wc_meta = meta[meta["Cuecolor"] == "white"].reset_index(drop=True)
    wc["trial_in_sub"] = wc.groupby("sub").cumcount() + 1

    if len(wc_meta) != 60:
        raise ValueError(f"Expected 60 white-cue metadata trials, found {len(wc_meta)}.")

    mapped = wc_meta.iloc[wc["trial_in_sub"].to_numpy() - 1].reset_index(drop=True)
    for col in [
        "F1_red", "F1_blue", "F2_red", "F2_blue",
        "diag1", "diag2",
    ]:
        wc[col] = mapped[col].to_numpy()

    # Signed diagonal rank difference. Positive favors F1.
    wc["diag"] = (wc["diag2"] - wc["diag1"]).astype(float)

    red_diff = wc["F2_red"] - wc["F1_red"]
    blue_diff = wc["F2_blue"] - wc["F1_blue"]

    # Reconstruct original "chooseF1big":
    # use the dimension on which F1 has the better (numerically smaller) rank.
    # The else branch also handles F1_red == F1_blue, matching the original
    # coefficient pattern.
    wc["chooseF1big"] = np.where(
        wc["F1_red"] < wc["F1_blue"],
        red_diff,
        blue_diff,
    ).astype(float)

    wc["resp01"] = (wc["resp"] == 1).astype(int)

    # Three mixed-dimensional runs, 20 trials per run.
    wc["blockw"] = ((wc["trial_in_sub"] - 1) // 20) + 1
    wc["zsblockw"] = zscale(wc["blockw"])

    return rb, wc


def prepare_panel_c_subset(df):
    """Match the original condition-wise orthogonalization."""
    d = df.copy()
    a0 = d["rel"].to_numpy(dtype=float) - d["rel"].mean()
    projection = (
        np.sum(d["irrel"].to_numpy(dtype=float) * a0) / np.sum(a0 ** 2)
    ) * a0

    d["relorth"] = zscale(d["rel"])
    d["irrelorth"] = zscale(d["irrel"].to_numpy(dtype=float) - projection)
    d["zscblockrb"] = zscale(d["blockrb"])
    return d


def significance(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "n.s."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("SR4seq(1).xlsx"),
        help="Path to SR4seq(1).xlsx",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("."),
        help="Output directory",
    )
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    rb, wc = reconstruct_data(args.input)

    models = {}

    # A: exact fixed-effect structure from original plotting code,
    # now with binomial-logit GLMM.
    models["A_single_dim"] = fit_random_intercept_logit(
        rb,
        "resp01 ~ rel*irrel*zsblock",
    )

    # B: same full interaction structure as original plotting code.
    # Use centered/z-scored run so the plotted main effects are at mean run.
    models["B_mixed_dim"] = fit_random_intercept_logit(
        wc,
        "resp01 ~ diag*chooseF1big*zsblockw",
    )

    # Literal raw-block translation retained as a sensitivity check.
    models["B_raw_block_sensitivity"] = fit_random_intercept_logit(
        wc,
        "resp01 ~ diag*chooseF1big*blockw",
    )

    # C: exact original condition-wise fixed-effect structure.
    conditions = {
        "C_Congruent_Easy": rb[rb["congruent"] & rb["easy"]],
        "C_Incongruent_Easy": rb[(~rb["congruent"]) & rb["easy"]],
        "C_Congruent_Difficult": rb[rb["congruent"] & (~rb["easy"])],
        "C_Incongruent_Difficult": rb[(~rb["congruent"]) & (~rb["easy"])],
    }

    for name, dat in conditions.items():
        dat = prepare_panel_c_subset(dat)
        models[name] = fit_random_intercept_logit(
            dat,
            "resp01 ~ relorth*irrelorth*zscblockrb",
        )

    # ---------- all fixed effects ----------
    all_rows = []
    model_info = []

    for model_name, (fixed, info) in models.items():
        temp = fixed.copy()
        temp.insert(0, "model", model_name)
        temp["N_trials"] = info["N_trials"]
        temp["N_participants"] = info["N_participants"]
        temp["random_intercept_SD"] = info["random_intercept_SD"]
        temp["formula"] = info["formula"]
        all_rows.append(temp)

        model_info.append({"model": model_name, **info})

    all_fixed = pd.concat(all_rows, ignore_index=True)
    model_info = pd.DataFrame(model_info)

    # ---------- coefficients plotted in Fig. 2A-C ----------
    key_specs = [
        ("A_single_dim", "A", "All single-dimensional", "rel", "rel"),
        ("A_single_dim", "A", "All single-dimensional", "irrel", "irrel"),
        ("A_single_dim", "A", "All single-dimensional", "rel × irrel", "rel:irrel"),

        ("B_mixed_dim", "B", "All mixed-dimensional", "diag", "diag"),
        ("B_mixed_dim", "B", "All mixed-dimensional", "unitary", "chooseF1big"),
        ("B_mixed_dim", "B", "All mixed-dimensional", "diag × unitary", "diag:chooseF1big"),

        ("C_Congruent_Easy", "C", "Congruent-Easy", "rel", "relorth"),
        ("C_Congruent_Easy", "C", "Congruent-Easy", "irrel", "irrelorth"),
        ("C_Incongruent_Easy", "C", "Incongruent-Easy", "rel", "relorth"),
        ("C_Incongruent_Easy", "C", "Incongruent-Easy", "irrel", "irrelorth"),
        ("C_Congruent_Difficult", "C", "Congruent-Difficult", "rel", "relorth"),
        ("C_Congruent_Difficult", "C", "Congruent-Difficult", "irrel", "irrelorth"),
        ("C_Incongruent_Difficult", "C", "Incongruent-Difficult", "rel", "relorth"),
        ("C_Incongruent_Difficult", "C", "Incongruent-Difficult", "irrel", "irrelorth"),
    ]

    fig_rows = []
    model_lookup = {k: v for k, v in models.items()}

    for model_name, panel, condition, predictor, term in key_specs:
        fixed, info = model_lookup[model_name]
        row = fixed.loc[fixed["term"] == term].iloc[0]
        fig_rows.append(
            {
                "panel": panel,
                "condition": condition,
                "predictor": predictor,
                "term": term,
                "beta": row["beta"],
                "SE": row["SE"],
                "z": row["z"],
                "p": row["p"],
                "CI_low": row["CI_low"],
                "CI_high": row["CI_high"],
                "significance": significance(row["p"]),
                "N_trials": info["N_trials"],
                "N_participants": info["N_participants"],
            }
        )

    fig_coeff = pd.DataFrame(fig_rows)

    fig_coeff.to_csv(
        args.outdir / "Fig2_GLMM_figure_coefficients.csv",
        index=False,
        encoding="utf-8-sig",
    )
    all_fixed.to_csv(
        args.outdir / "Fig2_GLMM_all_fixed_effects.csv",
        index=False,
        encoding="utf-8-sig",
    )
    model_info.to_csv(
        args.outdir / "Fig2_GLMM_model_info.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("\nFig. 2 A-C coefficients")
    print(fig_coeff.to_string(index=False))
    print("\nSaved to:", args.outdir.resolve())


if __name__ == "__main__":
    main()
