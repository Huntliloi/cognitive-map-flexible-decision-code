#!/usr/bin/env python3
"""Reviewer 5: participant-label permutation and max-|r| correction.

This script analyses the complete representational-warping brain--behavior
correlation family.  It reconstructs subject-level behavioral warping from the
single-dimensional (rbCue) and mixed-dimensional (wCue) trial tables, combines
the 16 supplied neural ROIs with symmetric bilateral averages, and corrects all
ROI x neural-axis x behavioral-task x behavioral-definition correlations with
one participant-label permutation maximum-statistic null.

The same participant permutation is applied to the entire behavioral matrix in
every iteration.  This preserves dependence among behavioral variables while
breaking their mapping to all neural measures.  Tests are two-sided and use the
maximum absolute Pearson correlation across the complete family.

Default primary behavioral handling
-----------------------------------
rbCue contained 48 congruent and 72 incongruent trials per participant.  The
legacy notebook used one unrecorded random sample of 48 incongruent trials.  To
retain equal trial counts without allowing one draw to determine the result,
the default here averages the behavioral indices across 1,000 independently
balanced resamples.  In every resample all 48 congruent trials and 48 sampled
incongruent trials are selected before applying the original RT < 2 s filter.

Both the raw behavioral distance ratio and the permutation-baseline-adjusted
effect (mean null ratio - observed ratio) are included in the corrected family.

Example
-------
python -u reviewer5_warping_brain_behavior_maxstat_v1.py \
    --neural warping_mas_BN.csv \
    --rbcue liu_rbCue.csv \
    --wcue liu_wCue.csv \
    --output-dir reviewer5_warping_maxstat_results \
    --behavior-resamples 1000 \
    --permutations 100000
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t as student_t


SUBJECTS = [1, 2, 3, 4, 6, 7, 9, 10, 11, 15, 17, 18, 19,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
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


@dataclass(frozen=True)
class CueArrays:
    rt: np.ndarray
    distance: np.ndarray
    euclidean: np.ndarray
    moral_diff: np.ndarray
    talent_diff: np.ndarray
    cue: str


def parse_args() -> argparse.Namespace:
    here = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Participant-label permutation with a global max-|r| null.",
    )
    p.add_argument("--neural", type=Path, default=here / "warping_mas_BN.csv")
    p.add_argument("--rbcue", type=Path, default=here / "liu_rbCue.csv")
    p.add_argument("--wcue", type=Path, default=here / "liu_wCue.csv")
    p.add_argument("--output-dir", type=Path,
                   default=here / "reviewer5_warping_maxstat_results")
    p.add_argument("--behavior-resamples", type=int, default=1000,
                   help="Balanced-trial and within-subject RT-null iterations.")
    p.add_argument("--permutations", type=int, default=100000,
                   help="Participant-label permutations for correlation inference.")
    p.add_argument("--seed", type=int, default=20260914)
    p.add_argument("--chunk-size", type=int, default=5000)
    p.add_argument(
        "--rb-strategy", choices=("repeated-balanced", "all-valid"),
        default="repeated-balanced",
        help="Primary rbCue trial handling; all-valid is a sensitivity option.",
    )
    p.add_argument("--no-bilateral", action="store_true",
                   help="Exclude bilateral averages (not recommended for the full family).")
    return p.parse_args()


def require_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"{label}: missing columns {missing}")


def normalize_subject(values: pd.Series, label: str) -> pd.Series:
    found = values.astype(str).str.extract(r"(\d+)", expand=False)
    if found.isna().any():
        bad = values[found.isna()].astype(str).unique().tolist()
        raise ValueError(f"{label}: unparseable subject labels {bad}")
    return found.astype(int)


def load_trials(path: Path, task: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    required = {"sub", "Cue", "RT", "D", "E", "rel", "irrel",
                "moral_diff", "talent_diff"}
    require_columns(df, required, task)
    df = df.copy()
    df["subject"] = normalize_subject(df["sub"], task)
    numeric = ["RT", "D", "E", "rel", "irrel", "moral_diff", "talent_diff"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="raise")
    if not np.isfinite(df[numeric].to_numpy(float)).all():
        raise ValueError(f"{task}: non-finite required values")
    if (df["E"] <= 0).any():
        raise ValueError(f"{task}: E must be positive")
    got = sorted(df["subject"].unique().tolist())
    if got != SUBJECTS:
        raise ValueError(f"{task}: subject set differs; got {got}")
    expected_rows = 120 if task == "rbCue" else 60
    counts = df.groupby("subject").size()
    if not (counts == expected_rows).all():
        raise ValueError(f"{task}: expected {expected_rows} rows per subject; "
                         f"got {counts.to_dict()}")
    expected_cues = {"moral", "talent"} if task == "rbCue" else {"hybrid"}
    got_cues = set(df["Cue"].astype(str).unique())
    if got_cues != expected_cues:
        raise ValueError(f"{task}: expected cues {expected_cues}; got {got_cues}")
    df["trial_congruent"] = np.where(
        np.sign(df["rel"].to_numpy()) == np.sign(df["irrel"].to_numpy()), 1, -1
    )
    return df


def cue_arrays(df: pd.DataFrame) -> list[CueArrays]:
    out: list[CueArrays] = []
    for cue, g in df.groupby("Cue", sort=True):
        out.append(CueArrays(
            rt=g["RT"].to_numpy(float),
            distance=g["D"].to_numpy(float),
            euclidean=g["E"].to_numpy(float),
            moral_diff=g["moral_diff"].to_numpy(float),
            talent_diff=g["talent_diff"].to_numpy(float),
            cue=str(cue),
        ))
    return out


def cue_omega(a: CueArrays, rt: np.ndarray) -> tuple[float, float]:
    """Return congruency and task-axis ratios for one participant/cue."""
    rt = np.asarray(rt, dtype=float)
    d = a.distance
    dc = d - d.mean()
    denom = float(dc @ dc)
    if denom <= 0:
        raise ValueError("Within-cue D has zero variance")
    slope = float(dc @ rt) / denom
    residual = rt - rt.mean() - slope * dc
    subjective_distance = np.exp(-residual / a.euclidean)
    theta = np.arctan2(a.talent_diff, a.moral_diff)
    x = subjective_distance * np.cos(theta)
    y = subjective_distance * np.sin(theta)
    covariance = np.cov(np.vstack((x, y)), ddof=1)
    if covariance.shape != (2, 2) or not np.isfinite(covariance).all():
        raise ValueError("Invalid behavioral covariance matrix")

    points = {
        "c1": covariance @ np.array([1.0, 1.0]),
        "c2": covariance @ np.array([4.0, 4.0]),
        "i1": covariance @ np.array([1.0, 4.0]),
        "i2": covariance @ np.array([4.0, 1.0]),
    }
    distance = lambda u, v: float(np.linalg.norm(points[u] - points[v]))
    v_congruent = distance("c1", "c2")
    v_incongruent = distance("i1", "i2")
    vertical = distance("c1", "i1")
    horizontal = distance("c1", "i2")
    if min(v_congruent, vertical, horizontal) <= 0:
        raise ValueError("Degenerate transformed behavioral geometry")
    congruent = v_incongruent / v_congruent
    # Moral uses horizontal as relevant; talent reverses the same axes.
    if a.cue in {"moral", "hybrid"}:
        attention = vertical / horizontal
    elif a.cue == "talent":
        attention = horizontal / vertical
    else:
        raise ValueError(f"Unexpected cue {a.cue}")
    return congruent, attention


def subject_omega(df: pd.DataFrame, rng: np.random.Generator | None,
                  shuffle_rt: bool) -> np.ndarray:
    vals = []
    for a in cue_arrays(df):
        rt = rng.permutation(a.rt) if shuffle_rt else a.rt
        vals.append(cue_omega(a, rt))
    return np.mean(np.asarray(vals, dtype=float), axis=0)


def behavior_for_subject_rb(g: pd.DataFrame, iterations: int, seed: int,
                            strategy: str) -> dict[str, float]:
    rng = np.random.default_rng(np.random.SeedSequence([seed, 11, int(g.subject.iloc[0])]))
    observed = []
    null = []
    if strategy == "all-valid":
        selected = g.loc[g.RT < 2].copy()
        obs = subject_omega(selected, None, False)
        observed = np.repeat(obs[None, :], iterations, axis=0)
        for _ in range(iterations):
            null.append(subject_omega(selected, rng, True))
    else:
        congruent = g.loc[g.trial_congruent == 1]
        incongruent = g.loc[g.trial_congruent == -1]
        if len(congruent) != 48 or len(incongruent) != 72:
            raise ValueError(
                f"rbCue subject {int(g.subject.iloc[0])}: expected 48/72 "
                f"congruent/incongruent trials, got {len(congruent)}/{len(incongruent)}"
            )
        for _ in range(iterations):
            take = rng.choice(len(incongruent), size=48, replace=False)
            selected = pd.concat((congruent, incongruent.iloc[take]), ignore_index=True)
            selected = selected.loc[selected.RT < 2].copy()
            observed.append(subject_omega(selected, None, False))
            null.append(subject_omega(selected, rng, True))
    observed = np.asarray(observed, dtype=float)
    null = np.asarray(null, dtype=float)
    obs_mean = observed.mean(axis=0)
    null_mean = null.mean(axis=0)
    return {
        "rbCue_raw_congruent": obs_mean[0],
        "rbCue_raw_attention": obs_mean[1],
        "rbCue_adjusted_congruent": null_mean[0] - obs_mean[0],
        "rbCue_adjusted_attention": null_mean[1] - obs_mean[1],
        "rbCue_raw_congruent_resample_sd": observed[:, 0].std(ddof=1),
        "rbCue_raw_attention_resample_sd": observed[:, 1].std(ddof=1),
    }


def behavior_for_subject_w(g: pd.DataFrame, iterations: int, seed: int) -> dict[str, float]:
    rng = np.random.default_rng(np.random.SeedSequence([seed, 22, int(g.subject.iloc[0])]))
    selected = g.loc[g.RT < 2].copy()
    obs = subject_omega(selected, None, False)
    null = np.asarray(
        [subject_omega(selected, rng, True) for _ in range(iterations)], dtype=float
    )
    null_mean = null.mean(axis=0)
    return {
        "wCue_raw_congruent": obs[0],
        "wCue_raw_attention": obs[1],
        "wCue_adjusted_congruent": null_mean[0] - obs[0],
        "wCue_adjusted_attention": null_mean[1] - obs[1],
    }


def build_behavior(rb: pd.DataFrame, w: pd.DataFrame, iterations: int,
                   seed: int, strategy: str) -> pd.DataFrame:
    rows = []
    for subject in SUBJECTS:
        row = {"subject": subject}
        row.update(behavior_for_subject_rb(
            rb.loc[rb.subject == subject], iterations, seed, strategy
        ))
        row.update(behavior_for_subject_w(
            w.loc[w.subject == subject], iterations, seed
        ))
        rows.append(row)
        print(f"behavior {subject:03d}: complete", flush=True)
    out = pd.DataFrame(rows)
    if not np.isfinite(out.drop(columns="subject").to_numpy(float)).all():
        raise ValueError("Non-finite subject-level behavioral values")
    return out


def load_neural(path: Path, include_bilateral: bool) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    require_columns(df, {"roi", "condition", "omega"}, "neural")
    id_col = "sub" if "sub" in df.columns else "subject"
    if id_col not in df.columns:
        raise ValueError("neural: expected a sub or subject column")
    df = df.copy()
    df["subject"] = normalize_subject(df[id_col], "neural")
    df["omega"] = pd.to_numeric(df["omega"], errors="raise")
    if not np.isfinite(df["omega"]).all():
        raise ValueError("neural: non-finite omega")
    if sorted(df.subject.unique().tolist()) != SUBJECTS:
        raise ValueError("neural: unexpected subject set")
    if set(df.condition.unique()) != set(CONDITIONS):
        raise ValueError(f"neural: unexpected conditions {sorted(df.condition.unique())}")
    multiplicity = df.groupby(["subject", "roi", "condition"]).size()
    if not (multiplicity == 1).all():
        raise ValueError("neural: duplicate or incomplete subject/ROI/condition cells")
    counts = df.groupby(["roi", "condition"]).size()
    if not (counts == len(SUBJECTS)).all():
        raise ValueError("neural: each ROI/condition must contain all participants")
    base = df[["subject", "roi", "condition", "omega"]].rename(columns={"roi": "region"})
    if not include_bilateral:
        return base
    extra = []
    available = set(base.region.unique())
    for name, pair in BILATERAL_PAIRS.items():
        if not set(pair).issubset(available):
            raise ValueError(f"Cannot create {name}; missing one of {pair}")
        z = (base.loc[base.region.isin(pair)]
             .groupby(["subject", "condition"], as_index=False)["omega"].mean())
        z["region"] = name
        extra.append(z[["subject", "region", "condition", "omega"]])
    return pd.concat([base, *extra], ignore_index=True)


def standardized(a: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=float)
    a = a - a.mean(axis=0, keepdims=True)
    norm = np.sqrt((a * a).sum(axis=0, keepdims=True))
    if (norm <= 0).any():
        raise ValueError("A correlation variable has zero variance")
    return a / norm


def correlation_family(neural: pd.DataFrame, behavior: pd.DataFrame,
                       permutations: int, seed: int,
                       chunk_size: int) -> tuple[pd.DataFrame, np.ndarray]:
    regions = sorted(neural.region.unique().tolist())
    wide = neural.pivot(index="subject", columns=["region", "condition"], values="omega")
    wide = wide.reindex(SUBJECTS)
    behavior = behavior.set_index("subject").reindex(SUBJECTS)

    neural_cols = [(region, condition) for condition in CONDITIONS for region in regions]
    x = standardized(wide[neural_cols].to_numpy(float))

    definitions = ("raw", "adjusted")
    behavior_cols = [
        f"{task}_{definition}_{condition}"
        for task in ("rbCue", "wCue")
        for definition in definitions
        for condition in CONDITIONS
    ]
    y = standardized(behavior[behavior_cols].to_numpy(float))

    x_lookup = {col: i for i, col in enumerate(neural_cols)}
    y_lookup = {col: i for i, col in enumerate(behavior_cols)}
    tests = []
    for task in ("rbCue", "wCue"):
        for definition in definitions:
            for condition in CONDITIONS:
                bcol = f"{task}_{definition}_{condition}"
                for region in regions:
                    tests.append({
                        "region": region,
                        "neural_condition": condition,
                        "behavior_task": task,
                        "behavior_definition": definition,
                        "behavior_variable": bcol,
                        "x_index": x_lookup[(region, condition)],
                        "y_index": y_lookup[bcol],
                    })

    xi = np.asarray([z["x_index"] for z in tests], dtype=int)
    yi = np.asarray([z["y_index"] for z in tests], dtype=int)
    observed = (x[:, xi] * y[:, yi]).sum(axis=0)
    uncorrected_exceed = np.zeros(len(tests), dtype=np.int64)
    corrected_exceed = np.zeros(len(tests), dtype=np.int64)
    max_null = np.empty(permutations, dtype=np.float64)

    rng = np.random.default_rng(np.random.SeedSequence([seed, 99]))
    done = 0
    while done < permutations:
        size = min(chunk_size, permutations - done)
        perms = np.vstack([rng.permutation(len(SUBJECTS)) for _ in range(size)])
        corr = np.empty((size, len(tests)), dtype=np.float64)
        for bidx in np.unique(yi):
            test_idx = np.flatnonzero(yi == bidx)
            corr[:, test_idx] = y[perms, bidx] @ x[:, xi[test_idx]]
        abs_corr = np.abs(corr)
        current_max = abs_corr.max(axis=1)
        max_null[done:done + size] = current_max
        uncorrected_exceed += (abs_corr >= np.abs(observed)[None, :]).sum(axis=0)
        corrected_exceed += (current_max[:, None] >= np.abs(observed)[None, :]).sum(axis=0)
        done += size
        print(f"participant-label permutations: {done}/{permutations}", flush=True)

    records = []
    dfree = len(SUBJECTS) - 2
    for j, test in enumerate(tests):
        r = float(observed[j])
        tval = r * math.sqrt(dfree / max(1e-15, 1.0 - r * r))
        p_param = float(2.0 * student_t.sf(abs(tval), dfree))
        records.append({
            "family": "representational_warping",
            "region": test["region"],
            "neural_condition": test["neural_condition"],
            "behavior_task": test["behavior_task"],
            "behavior_definition": test["behavior_definition"],
            "behavior_variable": test["behavior_variable"],
            "n": len(SUBJECTS),
            "r": r,
            "p_parametric": p_param,
            "p_permutation": (1.0 + uncorrected_exceed[j]) / (permutations + 1.0),
            "p_fwe_max": (1.0 + corrected_exceed[j]) / (permutations + 1.0),
        })
    results = pd.DataFrame(records)
    results["survives_fwe_05"] = results.p_fwe_max < 0.05
    results = results.sort_values(
        ["p_fwe_max", "p_permutation", "p_parametric", "region"],
        kind="stable",
    ).reset_index(drop=True)
    if (results.p_fwe_max + 1e-15 < results.p_permutation).any():
        raise AssertionError("Max-stat adjusted p smaller than pointwise permutation p")
    return results, max_null


def reproduction_rows(results: pd.DataFrame) -> pd.DataFrame:
    wanted = [
        ("HC_bilateral", "congruent", "wCue", "raw"),
        ("IPLl", "attention", "rbCue", "raw"),
        ("IPLr", "attention", "rbCue", "raw"),
        ("IPL_bilateral", "attention", "rbCue", "raw"),
    ]
    rows = []
    for region, condition, task, definition in wanted:
        z = results.loc[
            (results.region == region)
            & (results.neural_condition == condition)
            & (results.behavior_task == task)
            & (results.behavior_definition == definition)
        ]
        if len(z) == 1:
            rows.append(z.iloc[0])
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    if args.behavior_resamples < 100:
        raise ValueError("Use at least 100 behavioral resamples")
    if args.permutations < 1000:
        raise ValueError("Use at least 1,000 participant-label permutations")
    if args.chunk_size < 1:
        raise ValueError("chunk-size must be positive")

    rb = load_trials(args.rbcue, "rbCue")
    w = load_trials(args.wcue, "wCue")
    neural = load_neural(args.neural, include_bilateral=not args.no_bilateral)
    print(
        f"preflight: {len(SUBJECTS)} subjects; "
        f"{neural.region.nunique()} region definitions; 2 neural conditions",
        flush=True,
    )
    behavior = build_behavior(
        rb, w, args.behavior_resamples, args.seed, args.rb_strategy
    )
    results, max_null = correlation_family(
        neural, behavior, args.permutations, args.seed, args.chunk_size
    )

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    behavior_path = out / "behavioral_warping_subjects.csv"
    results_path = out / "brain_behavior_warping_maxstat.csv"
    null_path = out / "brain_behavior_warping_maxnull.csv"
    reproduction_path = out / "original_result_reproduction.csv"
    metadata_path = out / "analysis_metadata.json"
    behavior.to_csv(behavior_path, index=False, float_format="%.10g")
    results.to_csv(results_path, index=False, float_format="%.10g")
    pd.DataFrame({"max_abs_r": max_null}).to_csv(
        null_path, index=False, float_format="%.10g"
    )
    reproduction_rows(results).to_csv(
        reproduction_path, index=False, float_format="%.10g"
    )
    metadata = {
        "analysis": "participant-label permutation with global max-|r| null",
        "neural_input": str(args.neural.resolve()),
        "rbcue_input": str(args.rbcue.resolve()),
        "wcue_input": str(args.wcue.resolve()),
        "subjects": SUBJECTS,
        "n_subjects": len(SUBJECTS),
        "n_original_rois": 16,
        "bilateral_definitions": {} if args.no_bilateral else BILATERAL_PAIRS,
        "n_region_definitions": int(neural.region.nunique()),
        "n_tests": int(len(results)),
        "behavior_definitions": ["raw ratio", "mean null ratio - observed ratio"],
        "rb_strategy": args.rb_strategy,
        "behavior_resamples": args.behavior_resamples,
        "participant_label_permutations": args.permutations,
        "seed": args.seed,
        "max_null_95th_percentile": float(np.quantile(max_null, 0.95)),
        "max_null_99th_percentile": float(np.quantile(max_null, 0.99)),
        "n_fwe_significant_05": int(results.survives_fwe_05.sum()),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print("\nTop corrected results", flush=True)
    print(results.head(12).to_string(index=False), flush=True)
    print("\nOriginal-result checks", flush=True)
    print(reproduction_rows(results).to_string(index=False), flush=True)
    print(f"\nSaved outputs to {out}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
