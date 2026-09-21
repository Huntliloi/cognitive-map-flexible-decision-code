#!/usr/bin/env python3
"""Complete brain--behavior correlation family for Reviewer 5.

This analysis combines:

1. representational-warping correlations (Fig. 5 family), and
2. time-resolved ROI-coding/choice-effect correlations (Fig. 7 family).

The same participant-label permutation is applied jointly to the entire
behavioral matrix in each iteration.  The largest absolute Pearson correlation
across every test in both families defines the global maximum-statistic null.

The Fig. 7 behavioral coefficients reproduce the supplied Rmd exactly: R's
``glm`` was called without ``family=binomial``, so it is a Gaussian identity-link
model (ordinary least squares).  Missing-response trials are removed and
responses are coded 1 for response 1 and 0 for response 2.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t as student_t


SUBJECTS = [1, 2, 3, 4, 6, 7, 9, 10, 11, 15, 17, 18, 19, 21,
            22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
CONDITIONS = ("congruent", "attention")
BILATERAL_PAIRS = {
    "Amy_bilateral": ("Amyl", "Amyr"),
    "EC_bilateral": ("ECl", "ECr"),
    "HC_bilateral": ("HCl", "HCr"),
    "IPL_bilateral": ("IPLl", "IPLr"),
    "Insula_bilateral": ("Insulal", "Insular"),
    "MFG_bilateral": ("MFGl", "MFGr"),
    "precuneus_bilateral": ("precuneusl", "precuneusr"),
}


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Global participant-label permutation max-|r| analysis.",
    )
    p.add_argument("--warping-neural", type=Path,
                   default=here / "warping_mas_BN.csv")
    p.add_argument("--warping-behavior", type=Path,
                   default=here / "behavioral_warping_subjects.csv")
    p.add_argument("--rbcue-neural", type=Path,
                   default=here / "rbCue.subBeta.csv")
    p.add_argument("--wcue-neural", type=Path,
                   default=here / "wCue.subBeta.csv")
    p.add_argument("--rbcue-trials", type=Path,
                   default=here / "subSR4rbCue.csv")
    p.add_argument("--wcue-trials", type=Path,
                   default=here / "subSR4wCue.csv")
    p.add_argument("--output-dir", type=Path,
                   default=here / "reviewer5_complete_brain_behavior_results")
    p.add_argument("--permutations", type=int, default=100000)
    p.add_argument("--seed", type=int, default=20260914)
    p.add_argument("--chunk-size", type=int, default=5000)
    return p.parse_args()


def require_file(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)


def normalize_subject(s: pd.Series, label: str) -> pd.Series:
    found = s.astype(str).str.extract(r"(\d+)", expand=False)
    if found.isna().any():
        raise ValueError(f"{label}: unparseable participant labels")
    return found.astype(int)


def validate_subjects(found: pd.Series, label: str) -> None:
    got = sorted(pd.unique(found).tolist())
    if got != SUBJECTS:
        raise ValueError(f"{label}: participant set differs; got {got}")


def fit_choice_effects(rb_path: Path, w_path: Path) -> pd.DataFrame:
    """Reproduce the participant-wise default-Gaussian R glm coefficients."""
    require_file(rb_path)
    require_file(w_path)
    rb = pd.read_csv(rb_path)
    w = pd.read_csv(w_path)
    for d, task, cols in [
        (rb, "rbCue", {"sub", "resp", "rel", "irrel", "blockrb"}),
        (w, "wCue", {"sub", "resp", "diag", "blockw"}),
    ]:
        missing = sorted(cols.difference(d.columns))
        if missing:
            raise ValueError(f"{task} trials: missing columns {missing}")
        d["subject"] = normalize_subject(d["sub"], task)
        validate_subjects(d.subject, task)

    rows: list[dict[str, float | int | str]] = []
    for subject in SUBJECTS:
        g = rb.loc[rb.subject == subject].dropna(
            subset=["resp", "rel", "irrel", "blockrb"]
        ).copy()
        y = (pd.to_numeric(g.resp, errors="raise").to_numpy() == 1).astype(float)
        rel = pd.to_numeric(g.rel, errors="raise").to_numpy(float)
        irrel = pd.to_numeric(g.irrel, errors="raise").to_numpy(float)
        block = pd.to_numeric(g.blockrb, errors="raise").to_numpy(float)
        x = np.column_stack([
            np.ones(len(g)), rel, irrel, block, rel * irrel,
            rel * block, irrel * block, rel * irrel * block,
        ])
        if np.linalg.matrix_rank(x) != x.shape[1]:
            raise ValueError(f"rbCue {subject}: rank-deficient behavioral model")
        beta = np.linalg.lstsq(x, y, rcond=None)[0]
        rows.extend([
            {"subject": subject, "task": "rbCue", "behavior_effect": "rel",
             "estimate": beta[1], "n_trials": len(g)},
            {"subject": subject, "task": "rbCue", "behavior_effect": "irrel",
             "estimate": beta[2], "n_trials": len(g)},
        ])

        g = w.loc[w.subject == subject].dropna(
            subset=["resp", "diag", "blockw"]
        ).copy()
        y = (pd.to_numeric(g.resp, errors="raise").to_numpy() == 1).astype(float)
        diag = pd.to_numeric(g.diag, errors="raise").to_numpy(float)
        block = pd.to_numeric(g.blockw, errors="raise").to_numpy(float)
        x = np.column_stack([np.ones(len(g)), diag, block, diag * block])
        if np.linalg.matrix_rank(x) != x.shape[1]:
            raise ValueError(f"wCue {subject}: rank-deficient behavioral model")
        beta = np.linalg.lstsq(x, y, rcond=None)[0]
        rows.append({
            "subject": subject, "task": "wCue", "behavior_effect": "diag",
            "estimate": beta[1], "n_trials": len(g),
        })

    out = pd.DataFrame(rows)
    if not np.isfinite(out.estimate).all():
        raise ValueError("Non-finite choice-effect estimates")
    return out


def load_choice_neural(rb_path: Path, w_path: Path) -> pd.DataFrame:
    frames = []
    for path, task in [(rb_path, "rbCue"), (w_path, "wCue")]:
        require_file(path)
        d = pd.read_csv(path)
        required = {"id", "roi", "face", "type", "beta"}
        missing = sorted(required.difference(d.columns))
        if missing:
            raise ValueError(f"{task} neural: missing columns {missing}")
        d = d.copy()
        d["subject"] = normalize_subject(d.id, task)
        d["beta"] = pd.to_numeric(d.beta, errors="raise")
        d["task"] = task
        validate_subjects(d.subject, task)
        key = ["subject", "roi", "face", "type"]
        if not (d.groupby(key).size() == 1).all():
            raise ValueError(f"{task} neural: duplicated cells")
        if not (d.groupby(["roi", "face", "type"]).subject.nunique()
                == len(SUBJECTS)).all():
            raise ValueError(f"{task} neural: incomplete cells")
        frames.append(d[["subject", "task", "roi", "face", "type", "beta"]])
    out = pd.concat(frames, ignore_index=True)
    if not np.isfinite(out.beta).all():
        raise ValueError("Non-finite neural choice coefficients")
    return out


def load_warping_neural(path: Path) -> pd.DataFrame:
    require_file(path)
    d = pd.read_csv(path)
    required = {"sub", "roi", "condition", "omega"}
    missing = sorted(required.difference(d.columns))
    if missing:
        raise ValueError(f"warping neural: missing columns {missing}")
    d = d.copy()
    d["subject"] = normalize_subject(d["sub"], "warping neural")
    d["omega"] = pd.to_numeric(d.omega, errors="raise")
    validate_subjects(d.subject, "warping neural")
    if set(d.condition.unique()) != set(CONDITIONS):
        raise ValueError("warping neural: unexpected conditions")
    if not (d.groupby(["subject", "roi", "condition"]).size() == 1).all():
        raise ValueError("warping neural: duplicated cells")
    base = d[["subject", "roi", "condition", "omega"]].rename(
        columns={"roi": "region"}
    )
    extra = []
    available = set(base.region.unique())
    for name, pair in BILATERAL_PAIRS.items():
        if not set(pair).issubset(available):
            raise ValueError(f"Cannot construct {name}; missing {pair}")
        z = (base.loc[base.region.isin(pair)]
             .groupby(["subject", "condition"], as_index=False).omega.mean())
        z["region"] = name
        extra.append(z[["subject", "region", "condition", "omega"]])
    out = pd.concat([base, *extra], ignore_index=True)
    if out.region.nunique() != 23:
        raise ValueError("Expected 23 warping region definitions")
    return out


def load_warping_behavior(path: Path) -> pd.DataFrame:
    require_file(path)
    d = pd.read_csv(path)
    if "subject" not in d.columns:
        raise ValueError("warping behavior: missing subject")
    d = d.copy()
    d["subject"] = normalize_subject(d.subject, "warping behavior")
    validate_subjects(d.subject, "warping behavior")
    required = [
        f"{task}_{definition}_{condition}"
        for task in ("rbCue", "wCue")
        for definition in ("raw", "adjusted")
        for condition in CONDITIONS
    ]
    missing = sorted(set(required).difference(d.columns))
    if missing:
        raise ValueError(f"warping behavior: missing columns {missing}")
    for col in required:
        d[col] = pd.to_numeric(d[col], errors="raise")
    if not np.isfinite(d[required].to_numpy(float)).all():
        raise ValueError("Non-finite warping behavior")
    return d[["subject", *required]]


def standardize(a: np.ndarray) -> np.ndarray:
    z = np.asarray(a, dtype=float)
    z = z - z.mean(axis=0, keepdims=True)
    norm = np.sqrt((z * z).sum(axis=0, keepdims=True))
    if (norm <= 0).any():
        raise ValueError("Zero-variance correlation variable")
    return z / norm


def construct_family(choice_neural: pd.DataFrame,
                     choice_behavior: pd.DataFrame,
                     warping_neural: pd.DataFrame,
                     warping_behavior: pd.DataFrame
                     ) -> tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """Build standardized matrices and the complete test specification."""
    neural_arrays: list[np.ndarray] = []
    neural_names: list[str] = []
    behavior_arrays: list[np.ndarray] = []
    behavior_names: list[str] = []
    tests: list[dict[str, object]] = []

    # Choice-effect behavioral variables: two rbCue effects and one wCue effect.
    cb = choice_behavior.pivot(index="subject", columns=["task", "behavior_effect"],
                               values="estimate").reindex(SUBJECTS)
    for task, effect in [("rbCue", "rel"), ("rbCue", "irrel"), ("wCue", "diag")]:
        behavior_names.append(f"choice::{task}::{effect}")
        behavior_arrays.append(cb[(task, effect)].to_numpy(float))
    behavior_lookup = {name: i for i, name in enumerate(behavior_names)}

    # All 108 supplied neural coefficient cells, crossed with all choice effects
    # from the same task: 84*2 + 24*1 = 192 tests.
    choice_cells = (choice_neural[["task", "roi", "face", "type"]]
                    .drop_duplicates().sort_values(["task", "roi", "face", "type"],
                                                   kind="stable"))
    for task, roi, face, code_type in choice_cells.itertuples(index=False, name=None):
        g = (choice_neural.loc[
            (choice_neural.task == task) & (choice_neural.roi == roi)
            & (choice_neural.face == face) & (choice_neural.type == code_type),
            ["subject", "beta"]
        ].set_index("subject").reindex(SUBJECTS))
        if g.beta.isna().any():
            raise ValueError(f"Incomplete choice neural cell {task}/{roi}/{face}/{code_type}")
        x_name = f"choice::{task}::{roi}::{face}::{code_type}"
        x_index = len(neural_names)
        neural_names.append(x_name)
        neural_arrays.append(g.beta.to_numpy(float))
        effects = ("rel", "irrel") if task == "rbCue" else ("diag",)
        for effect in effects:
            y_name = f"choice::{task}::{effect}"
            tests.append({
                "family": "time_resolved_roi_coding",
                "task": task,
                "region": roi,
                "neural_condition": f"{face}_{code_type}",
                "behavior_variable": effect,
                "behavior_definition": "choice_effect_legacy_gaussian_glm",
                "x_index": x_index,
                "y_index": behavior_lookup[y_name],
            })

    # Eight warping behavioral variables appended to the same behavior matrix.
    wb = warping_behavior.set_index("subject").reindex(SUBJECTS)
    for task in ("rbCue", "wCue"):
        for definition in ("raw", "adjusted"):
            for condition in CONDITIONS:
                col = f"{task}_{definition}_{condition}"
                behavior_lookup[f"warping::{col}"] = len(behavior_names)
                behavior_names.append(f"warping::{col}")
                behavior_arrays.append(wb[col].to_numpy(float))

    regions = sorted(warping_neural.region.unique())
    for condition in CONDITIONS:
        for region in regions:
            g = (warping_neural.loc[
                (warping_neural.region == region)
                & (warping_neural.condition == condition), ["subject", "omega"]
            ].set_index("subject").reindex(SUBJECTS))
            if g.omega.isna().any():
                raise ValueError(f"Incomplete warping cell {region}/{condition}")
            x_index = len(neural_names)
            neural_names.append(f"warping::{region}::{condition}")
            neural_arrays.append(g.omega.to_numpy(float))
            for task in ("rbCue", "wCue"):
                for definition in ("raw", "adjusted"):
                    bcol = f"{task}_{definition}_{condition}"
                    tests.append({
                        "family": "representational_warping",
                        "task": task,
                        "region": region,
                        "neural_condition": condition,
                        "behavior_variable": bcol,
                        "behavior_definition": definition,
                        "x_index": x_index,
                        "y_index": behavior_lookup[f"warping::{bcol}"],
                    })

    x = standardize(np.column_stack(neural_arrays))
    y = standardize(np.column_stack(behavior_arrays))
    spec = pd.DataFrame(tests)
    if len(spec) != 376:
        raise AssertionError(f"Expected 376 tests, got {len(spec)}")
    return x, y, spec


def permute_family(x: np.ndarray, y: np.ndarray, spec: pd.DataFrame,
                   permutations: int, seed: int, chunk_size: int
                   ) -> tuple[pd.DataFrame, np.ndarray]:
    xi = spec.x_index.to_numpy(int)
    yi = spec.y_index.to_numpy(int)
    observed = (x[:, xi] * y[:, yi]).sum(axis=0)
    point_exceed = np.zeros(len(spec), dtype=np.int64)
    max_exceed = np.zeros(len(spec), dtype=np.int64)
    max_null = np.empty(permutations, dtype=float)
    rng = np.random.default_rng(np.random.SeedSequence([seed, 505]))
    done = 0
    while done < permutations:
        size = min(chunk_size, permutations - done)
        perms = np.vstack([rng.permutation(len(SUBJECTS)) for _ in range(size)])
        corr = np.empty((size, len(spec)), dtype=float)
        for bidx in np.unique(yi):
            test_idx = np.flatnonzero(yi == bidx)
            corr[:, test_idx] = y[perms, bidx] @ x[:, xi[test_idx]]
        absolute = np.abs(corr)
        current_max = absolute.max(axis=1)
        max_null[done:done + size] = current_max
        point_exceed += (absolute >= np.abs(observed)[None, :]).sum(axis=0)
        max_exceed += (current_max[:, None] >= np.abs(observed)[None, :]).sum(axis=0)
        done += size
        print(f"participant-label permutations: {done}/{permutations}", flush=True)

    out = spec.drop(columns=["x_index", "y_index"]).copy()
    out["n"] = len(SUBJECTS)
    out["r"] = observed
    dfree = len(SUBJECTS) - 2
    tvalue = observed * np.sqrt(dfree / np.maximum(1e-15, 1.0 - observed ** 2))
    out["p_parametric"] = 2.0 * student_t.sf(np.abs(tvalue), dfree)
    out["p_permutation"] = (1.0 + point_exceed) / (permutations + 1.0)
    out["p_fwe_global"] = (1.0 + max_exceed) / (permutations + 1.0)
    out["survives_global_fwe_05"] = out.p_fwe_global < .05
    if (out.p_fwe_global + 1e-15 < out.p_permutation).any():
        raise AssertionError("Global FWE p smaller than pointwise permutation p")
    return out.sort_values(
        ["p_fwe_global", "p_permutation", "p_parametric", "family", "region"],
        kind="stable",
    ).reset_index(drop=True), max_null


def selected_fig7_rows(results: pd.DataFrame) -> pd.DataFrame:
    """Candidate mapping from the supplied Rmd, figure text, and ROI names."""
    wanted = [
        ("7B", "rbCue", "F1rel_IPL_l", "F1_rel", "rel", "inferred"),
        ("7B", "rbCue", "D_IPL_l", "F2_D", "rel", "inferred"),
        ("7D", "rbCue", "D_insular", "F1_rel", "rel", "inferred"),
        ("7D", "rbCue", "D_insular", "F2_D", "rel", "inferred"),
        ("7F", "rbCue", "chirrel_precuences", "F2_D", "rel", "explicit_Rmd"),
        ("7F", "rbCue", "chirrel_precuences", "F2_I", "irrel", "explicit_Rmd"),
        ("7H", "wCue", "undiagdiff_insula_r", "F2_diagdiff", "diag", "inferred"),
        ("7H", "wCue", "chdiagdiff_HC_l", "F2_diagdiff", "diag", "inferred"),
    ]
    rows = []
    zall = results.loc[results.family == "time_resolved_roi_coding"]
    for panel, task, roi, condition, behavior, basis in wanted:
        z = zall.loc[
            (zall.task == task) & (zall.region == roi)
            & (zall.neural_condition == condition)
            & (zall.behavior_variable == behavior)
        ]
        if len(z) != 1:
            raise ValueError(f"Missing candidate panel row {panel}/{roi}/{condition}/{behavior}")
        row = z.iloc[0].copy()
        row["panel"] = panel
        row["mapping_basis"] = basis
        rows.append(row)
    cols = ["panel", "mapping_basis", *results.columns]
    return pd.DataFrame(rows)[cols]


def main() -> None:
    args = parse_args()
    if args.permutations < 1000:
        raise ValueError("Use at least 1,000 participant-label permutations")
    if args.chunk_size < 1:
        raise ValueError("chunk-size must be positive")

    choice_behavior = fit_choice_effects(args.rbcue_trials, args.wcue_trials)
    choice_neural = load_choice_neural(args.rbcue_neural, args.wcue_neural)
    warping_neural = load_warping_neural(args.warping_neural)
    warping_behavior = load_warping_behavior(args.warping_behavior)
    x, y, spec = construct_family(
        choice_neural, choice_behavior, warping_neural, warping_behavior
    )
    print(
        f"preflight: {len(SUBJECTS)} participants; "
        f"{(spec.family == 'representational_warping').sum()} warping tests; "
        f"{(spec.family == 'time_resolved_roi_coding').sum()} coding tests; "
        f"{len(spec)} total tests",
        flush=True,
    )
    results, max_null = permute_family(
        x, y, spec, args.permutations, args.seed, args.chunk_size
    )
    selected = selected_fig7_rows(results)

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    results.to_csv(out / "complete_brain_behavior_maxstat.csv", index=False,
                   float_format="%.10g")
    results.loc[results.family == "representational_warping"].to_csv(
        out / "fig5_warping_correlations_global_corrected.csv", index=False,
        float_format="%.10g"
    )
    results.loc[results.family == "time_resolved_roi_coding"].to_csv(
        out / "fig7_roi_coding_correlations_global_corrected.csv", index=False,
        float_format="%.10g"
    )
    selected.to_csv(out / "fig7BDHF_candidate_mapping.csv", index=False,
                    float_format="%.10g")
    choice_behavior.to_csv(out / "choice_behavior_effects_legacy_glm.csv", index=False,
                           float_format="%.10g")
    pd.DataFrame({"max_abs_r": max_null}).to_csv(
        out / "complete_brain_behavior_maxnull.csv", index=False,
        float_format="%.10g"
    )
    metadata = {
        "analysis": "joint participant-label permutation with global max absolute Pearson r",
        "n_subjects": len(SUBJECTS),
        "subjects": SUBJECTS,
        "n_warping_tests": int((spec.family == "representational_warping").sum()),
        "n_roi_coding_tests": int((spec.family == "time_resolved_roi_coding").sum()),
        "n_total_tests": len(spec),
        "choice_family_definition": "all 84 rbCue neural cells crossed with rel and irrel behavior effects, plus all 24 wCue neural cells crossed with the diag behavior effect",
        "choice_behavior_model": {
            "rbCue": "Gaussian identity-link GLM: response01 ~ rel * irrel * blockrb; reported coefficients rel and irrel",
            "wCue": "Gaussian identity-link GLM: response01 ~ diag * blockw; reported coefficient diag",
            "reason": "Exact reproduction of supplied Rmd, whose glm calls omit family=binomial",
        },
        "participant_label_permutations": args.permutations,
        "seed": args.seed,
        "max_null_95th_percentile": float(np.quantile(max_null, .95)),
        "max_null_99th_percentile": float(np.quantile(max_null, .99)),
        "n_global_fwe_significant_05": int(results.survives_global_fwe_05.sum()),
        "n_fig5_global_fwe_significant_05": int(results.loc[
            results.family == "representational_warping", "survives_global_fwe_05"
        ].sum()),
        "n_fig7_global_fwe_significant_05": int(results.loc[
            results.family == "time_resolved_roi_coding", "survives_global_fwe_05"
        ].sum()),
        "mapping_note": "Fig. 7F rows are explicit in the supplied Rmd; Fig. 7B/D/H rows are inferred from figure text and ROI names and require confirmation against the original scatterplot code or figure source.",
    }
    (out / "analysis_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    print("\nCandidate Fig. 7B/D/F/H rows", flush=True)
    print(selected[["panel", "mapping_basis", "region", "neural_condition",
                    "behavior_variable", "r", "p_parametric", "p_permutation",
                    "p_fwe_global", "survives_global_fwe_05"]].to_string(index=False),
          flush=True)
    print("\nGlobal results", flush=True)
    print(results.groupby("family").agg(
        tests=("r", "size"), nominal_permutation_p05=("p_permutation", lambda z: int((z < .05).sum())),
        global_fwe_p05=("survives_global_fwe_05", "sum")
    ).to_string(), flush=True)
    print(f"Saved outputs to {out}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
