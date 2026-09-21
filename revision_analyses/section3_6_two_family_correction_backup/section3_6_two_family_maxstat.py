#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Section 3.6 two-family multiple-comparison correction
=====================================================

Purpose
-------
Recompute the time-resolved ROI coding statistics used in manuscript Section 3.6
and correct them in two prespecified families using a participant-wise synchronized
sign-flip maximum-statistic procedure.

Pointwise test:
    Two-sided Wilcoxon signed-rank test (N=24).

Family-wise statistic:
    For each test, use the absolute signed-rank score

        T = | sum_i sign(beta_i) * rank(|beta_i|) |

    In each permutation, one Rademacher sign (+1/-1) is drawn per participant and
    applied synchronously to every trajectory/time point in the family. The maximum
    T across the whole family is saved. Corrected P_FWER is the proportion of the
    max-statistic null distribution at least as extreme as the observed T, with the
    +1 correction.

Families
--------
Family 1 (single-dimensional task; 100 tests):
    10 trajectories x 10 TENT points
      1) IPL F1 task-relevant rank
      2) IPL F1 task-irrelevant rank
      3) IPL F2 task-relevant rank difference
      4) Right insula F1 task-relevant rank
      5) Right insula F1 task-irrelevant rank
      6) Right insula F2 task-relevant rank difference
      7) Precuneus F2 task-relevant rank difference
      8) Precuneus F2 task-irrelevant rank difference
      9) Precuneus easy-trial task-irrelevant effect
     10) Precuneus hard-trial task-irrelevant effect

Family 2 (mixed-dimensional task; 40 tests):
    4 trajectories x 10 TENT points
      1) Right insula F1 diagonal rank
      2) Left hippocampus F1 diagonal rank
      3) Right insula F2 diagonal rank difference
      4) Left hippocampus F2 diagonal rank difference

Important data-integrity note
-----------------------------
In the supplied wCue.diagF1F2.tent.csv, the extracted right-insula and left-
hippocampus trajectories used in Family 2 are numerically identical. The script
therefore writes an explicit integrity-check file. Family-2 results should be
interpreted only after confirming the original TENT export.

Input files expected in --input-dir
-----------------------------------
rbCue.F1F2relirrel.tent.csv
rbCue.easyhard.tent.csv
wCue.diagF1F2.tent.csv

Usage
-----
python section3_6_two_family_maxstat.py
python section3_6_two_family_maxstat.py --input-dir /path/to/csvs --output-dir results
python section3_6_two_family_maxstat.py --n-perm 100000 --seed 20260919

Outputs
-------
family1_all_tests.csv
family2_all_tests.csv
key_results.csv
family2_data_integrity_check.csv
analysis_metadata.json
"""

from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
from scipy.stats import rankdata, wilcoxon


def add_position(df):
    """Index each value within participant x class x ROI in original row order."""
    out = df.copy()
    out["position"] = out.groupby(["id", "class", "roi"]).cumcount()
    return out


def extract_tent_block(df, roi, task_class, start_position, label):
    """
    Extract one 10-point TENT trajectory.

    The supplied long-format CSV stores consecutive 10-point TENT blocks.
    start_position is the zero-based first row position of the desired block
    within participant x class x ROI.
    """
    use = df[
        (df["roi"] == roi)
        & (df["class"] == task_class)
        & (df["position"].between(start_position, start_position + 9))
    ].copy()

    pivot = (
        use.pivot(index="id", columns="position", values="beta")
        .sort_index()
    )
    if pivot.shape != (24, 10):
        raise ValueError(
            f"{label}: expected 24 participants x 10 TENT points, got {pivot.shape}"
        )
    pivot.columns = np.arange(10, dtype=int)
    return label, pivot


def wilcoxon_summary(x):
    """
    Return positive-rank sum W, standard two-sided Wilcoxon P,
    and the absolute signed-rank score used for max-stat correction.
    """
    x = np.asarray(x, dtype=float)
    nonzero = x != 0
    ranks = np.zeros_like(x, dtype=float)
    ranks[nonzero] = rankdata(np.abs(x[nonzero]), method="average")

    w_positive = float(ranks[x > 0].sum())
    signed_rank_score = float(abs(np.sum(np.sign(x) * ranks)))

    p = float(
        wilcoxon(
            x,
            alternative="two-sided",
            zero_method="wilcox",
            method="auto",
        ).pvalue
    )
    return w_positive, p, signed_rank_score, ranks


def maxstat_family(trajectories, n_perm, seed, family_name):
    """
    Participant-wise synchronized sign-flip max-statistic correction.

    One random +/- sign is assigned to each participant per permutation and is
    shared across every test in the family.
    """
    rows = []
    test_vectors = []
    rank_vectors = []
    meta = []

    for effect, pivot in trajectories:
        for tent_index in range(10):
            x = pivot[tent_index].to_numpy(dtype=float)
            w_pos, p_unc, t_obs, ranks = wilcoxon_summary(x)

            test_vectors.append(x)
            rank_vectors.append(ranks)
            meta.append((effect, tent_index, w_pos, p_unc, t_obs))

    X = np.asarray(test_vectors)
    R = np.asarray(rank_vectors)
    n_tests, n_subjects = X.shape

    if n_subjects != 24:
        raise ValueError(f"{family_name}: expected N=24, got {n_subjects}")

    observed = np.asarray([m[4] for m in meta], dtype=float)

    rng = np.random.default_rng(seed)
    max_null = np.empty(n_perm, dtype=float)

    # Batch permutations to keep memory use small.
    batch_size = 5000
    for start in range(0, n_perm, batch_size):
        k = min(batch_size, n_perm - start)
        signs = rng.choice(
            np.array([-1.0, 1.0]),
            size=(k, n_subjects),
            replace=True,
        )

        # Under sign flipping, absolute ranks stay fixed.
        perm_stats = np.abs(signs @ R.T)  # permutations x tests
        max_null[start:start + k] = perm_stats.max(axis=1)

    # +1 correction gives a valid Monte-Carlo permutation P value.
    p_fwer = np.asarray([
        (1.0 + np.sum(max_null >= obs)) / (n_perm + 1.0)
        for obs in observed
    ])

    for i, (effect, tent_index, w_pos, p_unc, t_obs) in enumerate(meta):
        rows.append({
            "family": family_name,
            "effect": effect,
            "tent_index": tent_index,
            "N": n_subjects,
            "W_positive": w_pos,
            "P_uncorrected": p_unc,
            "abs_signed_rank_score": t_obs,
            "P_FWER": p_fwer[i],
            "significant_FWER_0.05": bool(p_fwer[i] < 0.05),
        })

    return pd.DataFrame(rows), max_null


def pick_row(df, effect, tent_index):
    row = df[(df["effect"] == effect) & (df["tent_index"] == tent_index)]
    if len(row) != 1:
        raise ValueError(f"Could not uniquely identify {effect}, TENT {tent_index}")
    return row.iloc[0].to_dict()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=Path("section3_6_correction_results"))
    parser.add_argument("--n-perm", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=20260919)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    rb = add_position(pd.read_csv(args.input_dir / "rbCue.F1F2relirrel.tent.csv"))
    eh = add_position(pd.read_csv(args.input_dir / "rbCue.easyhard.tent.csv"))
    wc = add_position(pd.read_csv(args.input_dir / "wCue.diagF1F2.tent.csv"))

    # ---- Family 1: single-dimensional task ----
    # F1 file layout used here:
    #   positions 10-19 = task-relevant rank trajectory
    #   positions 20-29 = task-irrelevant rank trajectory
    #
    # F2 file layout used here:
    #   positions 30-39 = task-relevant rank-difference trajectory
    #   positions 40-49 = task-irrelevant rank-difference trajectory
    #
    # Easy/hard file:
    #   positions 30-39 = trajectory matching the easy/hard precuneus result
    #                    reported in the original analysis.
    family1 = [
        extract_tent_block(rb, "F1rel_IPLl", "F1", 10, "IPL_F1_relevant"),
        extract_tent_block(rb, "F1rel_IPLl", "F1", 20, "IPL_F1_irrelevant"),
        extract_tent_block(rb, "D_IPLl", "F2", 30, "IPL_F2_relevant_difference"),

        extract_tent_block(rb, "D_insular", "F1", 10, "Insula_F1_relevant"),
        extract_tent_block(rb, "D_insular", "F1", 20, "Insula_F1_irrelevant"),
        extract_tent_block(rb, "D_insular", "F2", 30, "Insula_F2_relevant_difference"),

        extract_tent_block(
            rb, "chirrel_precuences", "F2", 30,
            "Precuneus_F2_relevant_difference"
        ),
        extract_tent_block(
            rb, "chirrel_precuences", "F2", 40,
            "Precuneus_F2_irrelevant_difference"
        ),

        extract_tent_block(
            eh, "chirrel_precuences", "F2.easy", 30,
            "Precuneus_easy_irrelevant"
        ),
        extract_tent_block(
            eh, "chirrel_precuences", "F2.hard", 30,
            "Precuneus_hard_irrelevant"
        ),
    ]

    # ---- Family 2: mixed-dimensional task ----
    # F1 positions 10-19 = diagonal-rank trajectory
    # F2 positions 20-29 = diagonal-rank-difference trajectory
    family2 = [
        extract_tent_block(
            wc, "F2diagdiff_insula_l", "F1", 10,
            "Insula_F1_diagonal_rank"
        ),
        extract_tent_block(
            wc, "chdiagdiff_HC_l", "F1", 10,
            "HC_F1_diagonal_rank"
        ),
        extract_tent_block(
            wc, "F2diagdiff_insula_l", "F2", 20,
            "Insula_F2_diagonal_difference"
        ),
        extract_tent_block(
            wc, "chdiagdiff_HC_l", "F2", 20,
            "HC_F2_diagonal_difference"
        ),
    ]

    res1, maxnull1 = maxstat_family(
        family1, args.n_perm, args.seed, "Family1_single_dimensional"
    )
    # Use a different deterministic stream for Family 2.
    res2, maxnull2 = maxstat_family(
        family2, args.n_perm, args.seed + 1, "Family2_mixed_dimensional"
    )

    res1.to_csv(args.output_dir / "family1_all_tests.csv", index=False)
    res2.to_csv(args.output_dir / "family2_all_tests.csv", index=False)

    # Key rows corresponding to the principal Section 3.6 statements.
    key_specs = [
        ("Family1_single_dimensional", res1, "IPL_F1_relevant", 4),
        ("Family1_single_dimensional", res1, "IPL_F1_irrelevant", 4),
        ("Family1_single_dimensional", res1, "IPL_F2_relevant_difference", 4),
        ("Family1_single_dimensional", res1, "Insula_F1_relevant", 4),
        ("Family1_single_dimensional", res1, "Insula_F1_irrelevant", 0),
        ("Family1_single_dimensional", res1, "Insula_F2_relevant_difference", 4),
        ("Family1_single_dimensional", res1, "Precuneus_F2_relevant_difference", 4),
        ("Family1_single_dimensional", res1, "Precuneus_F2_irrelevant_difference", 5),
        ("Family1_single_dimensional", res1, "Precuneus_easy_irrelevant", 0),
        ("Family1_single_dimensional", res1, "Precuneus_hard_irrelevant", 6),

        # For Family 2, include all corrected-significant time points rather than
        # forcing the dissertation's W=4/W=5 values, which are not reproduced by
        # the supplied CSV.
    ]

    key_rows = [pick_row(df, effect, tent) for _, df, effect, tent in key_specs]

    family2_sig = res2[res2["P_FWER"] < 0.05].copy()
    key_df = pd.concat(
        [pd.DataFrame(key_rows), family2_sig],
        ignore_index=True,
        sort=False,
    )
    key_df.to_csv(args.output_dir / "key_results.csv", index=False)

    # Data integrity check for the duplicated Family-2 trajectories.
    f2_map = {label: pivot for label, pivot in family2}
    checks = [
        {
            "comparison":
                "Insula_F1_diagonal_rank vs HC_F1_diagonal_rank",
            "identical_all_values":
                bool(np.array_equal(
                    f2_map["Insula_F1_diagonal_rank"].to_numpy(),
                    f2_map["HC_F1_diagonal_rank"].to_numpy()
                )),
            "max_abs_difference":
                float(np.max(np.abs(
                    f2_map["Insula_F1_diagonal_rank"].to_numpy()
                    - f2_map["HC_F1_diagonal_rank"].to_numpy()
                ))),
        },
        {
            "comparison":
                "Insula_F2_diagonal_difference vs HC_F2_diagonal_difference",
            "identical_all_values":
                bool(np.array_equal(
                    f2_map["Insula_F2_diagonal_difference"].to_numpy(),
                    f2_map["HC_F2_diagonal_difference"].to_numpy()
                )),
            "max_abs_difference":
                float(np.max(np.abs(
                    f2_map["Insula_F2_diagonal_difference"].to_numpy()
                    - f2_map["HC_F2_diagonal_difference"].to_numpy()
                ))),
        },
    ]
    pd.DataFrame(checks).to_csv(
        args.output_dir / "family2_data_integrity_check.csv",
        index=False,
    )

    metadata = {
        "analysis": "Section 3.6 two-family participant-wise sign-flip max-stat correction",
        "pointwise_test": "two-sided Wilcoxon signed-rank",
        "max_statistic": "maximum absolute signed-rank score",
        "N_subjects": 24,
        "n_permutations": args.n_perm,
        "seed_family1": args.seed,
        "seed_family2": args.seed + 1,
        "family1_n_tests": int(len(res1)),
        "family2_n_tests": int(len(res2)),
        "p_value_formula": "(1 + count(max_null >= observed)) / (n_perm + 1)",
        "family2_warning":
            "The supplied wCue.diagF1F2.tent.csv contains identical extracted "
            "insula and hippocampus trajectories for the Family-2 effects; "
            "verify the original TENT export before interpretation."
    }
    with open(args.output_dir / "analysis_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("\nFamily 1: corrected-significant tests")
    print(
        res1[res1["P_FWER"] < 0.05]
        .sort_values(["P_FWER", "effect", "tent_index"])
        .to_string(index=False)
    )

    print("\nFamily 2: corrected-significant tests")
    print(
        res2[res2["P_FWER"] < 0.05]
        .sort_values(["P_FWER", "effect", "tent_index"])
        .to_string(index=False)
    )

    print("\nFiles written to:", args.output_dir.resolve())


if __name__ == "__main__":
    main()
