#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reviewer #4 validation of the rbCue neural warping indices (v6, rbCue-only).

Scope
-----
This script validates the directional warping estimators used for the six rbCue
runs, where the same 4x4 social map is evaluated under two alternative
single-dimensional task contexts (x / y; corresponding to the two rbCue task
contexts). The three wCue runs are intentionally excluded because they do not
instantiate the same context-switching contrast and were not used for the
warping analysis.

Estimator matched to the original rbCue implementation
-------------------------------------------------------
1) Neural dissimilarity is mean squared Euclidean pattern dissimilarity.
2) Task-axis warping uses three matched rank steps d=1,2,3:
       omega_task = 1 - mean_d(mean(irrelevant_d) / mean(relevant_d))
   where the relevant axis switches with task context.
3) Congruency-axis warping uses nine matched diagonal vector classes:
       omega_cong = 1 - mean_k(mean(incongruent_k) / mean(congruent_k))
   Red-Red and Blue-Blue (x-context and y-context) distances are pooled within
   each vector class; cross-context distances are never computed. The nine
   vector-class ratios are equally weighted.
4) Positive omega means stronger expansion along the theory-predicted axis.

Validation components
---------------------
A. Exact 4x4-grid combinatorial and sign audit.
B. Independent fixed-geometry calibration of a joint two-index threshold.
C. Five formal structured nulls corresponding to the reviewer alternatives.
D. Ground-truth geometric-warp recovery and cross-talk tests.

Important interpretation
------------------------
- "Task difficulty" here means processing demand structured WITHIN rbCue
  conditions (for example, by relevant rank distance). It does not mean the
  between-task fact that wCue may be globally harder than rbCue.
- A context-wide nonspecific shift/gain is tested separately as a main null.
- Pure downstream decision weighting leaves neural means fixed and is a
  negative control. Conditions that directly change neural pattern geometry
  are not treated as fixed-geometry nulls in the formal analysis.
- This is estimator-level simulation. It does not replace the empirical
  whole-brain confound-controlled reanalysis and does not reproduce the
  original whole-brain spatial/FWE selection pipeline.

Examples
--------
Smoke test:
    python reviewer4_rbCue_warping_validation_v6.py \
        --mode SMOKE \
        --strict-rsatoolbox-parity \
        --output results/r4_v6_smoke

Formal run:
    python reviewer4_rbCue_warping_validation_v6.py \
        --mode FORMAL \
        --strict-rsatoolbox-parity \
        --output results/r4_v6_FORMAL_main_only_20260913
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import beta as beta_dist


# =============================================================================
# 1. CONFIG
# =============================================================================

@dataclass(frozen=True)
class Config:
    BASE_SEED: int = 20260912
    N_SUBJECTS: int = 24
    N_VOXELS: int = 80
    BASE_NOISE_SD: float = 1.0

    CAL_STUDIES_SMOKE: int = 30
    CAL_STUDIES_QUICK: int = 500
    CAL_STUDIES_FORMAL: int = 2000

    NULL_STUDIES_SMOKE: int = 12
    NULL_STUDIES_QUICK: int = 300
    NULL_STUDIES_FORMAL: int = 2000

    RECOVERY_STUDIES_SMOKE: int = 12
    RECOVERY_STUDIES_QUICK: int = 150
    RECOVERY_STUDIES_FORMAL: int = 500

    RHO_VALUES: Tuple[float, ...] = (1.00, 0.90, 0.80, 0.70, 0.60, 0.50)
    NOISE_LEVELS: Tuple[float, ...] = (0.50, 1.00, 1.50)
    NUISANCE_MULTIPLIERS: Tuple[float, ...] = (0.50, 1.00, 2.00)
    RELIABILITY_RATIOS: Tuple[float, ...] = (1.00, 1.50, 2.00)

    DEFAULT_DIFFICULTY_AMPLITUDE: float = 0.50
    DEFAULT_CONGRUENCY_AMPLITUDE: float = 0.50
    DEFAULT_DECISION_AMPLITUDE: float = 0.50
    GLOBAL_CONTEXT_GAIN_DELTA: float = 0.25

    DECISION_WEIGHT_RELEVANT: float = 2.5
    DECISION_WEIGHT_IRRELEVANT: float = 0.35

    ALPHA: float = 0.05


PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument("--mode", choices=("SMOKE", "QUICK", "FORMAL"), default="SMOKE")
PARSER.add_argument("--output", default="reviewer4_rbCue_v6_results")
PARSER.add_argument("--n-voxels", type=int, default=80)
PARSER.add_argument("--n-subjects", type=int, default=24)
PARSER.add_argument(
    "--strict-rsatoolbox-parity",
    action="store_true",
    help=(
        "If rsatoolbox is installed, require the direct mean-squared-Euclidean "
        "implementation to match rsatoolbox's no-noise mahalanobis scale up to "
        "a common multiplicative factor."
    ),
)
ARGS = PARSER.parse_args()
CFG = Config(N_SUBJECTS=ARGS.n_subjects, N_VOXELS=ARGS.n_voxels)
OUT = Path(ARGS.output)

if CFG.N_SUBJECTS < 3:
    raise SystemExit("--n-subjects must be >= 3")
if CFG.N_VOXELS < 2:
    raise SystemExit("--n-voxels must be >= 2")

if ARGS.mode == "SMOKE":
    N_CAL = CFG.CAL_STUDIES_SMOKE
    N_NULL = CFG.NULL_STUDIES_SMOKE
    N_RECOVERY = CFG.RECOVERY_STUDIES_SMOKE
    RHO_VALUES = (1.00, 0.70, 0.50)
    NOISE_LEVELS = (1.00,)
    NUISANCE_MULTIPLIERS = (1.00,)
    RELIABILITY_RATIOS = (1.50,)
elif ARGS.mode == "QUICK":
    N_CAL = CFG.CAL_STUDIES_QUICK
    N_NULL = CFG.NULL_STUDIES_QUICK
    N_RECOVERY = CFG.RECOVERY_STUDIES_QUICK
    RHO_VALUES = CFG.RHO_VALUES
    NOISE_LEVELS = CFG.NOISE_LEVELS
    NUISANCE_MULTIPLIERS = CFG.NUISANCE_MULTIPLIERS
    RELIABILITY_RATIOS = CFG.RELIABILITY_RATIOS
else:
    N_CAL = CFG.CAL_STUDIES_FORMAL
    N_NULL = CFG.NULL_STUDIES_FORMAL
    N_RECOVERY = CFG.RECOVERY_STUDIES_FORMAL
    RHO_VALUES = CFG.RHO_VALUES
    NOISE_LEVELS = CFG.NOISE_LEVELS
    NUISANCE_MULTIPLIERS = CFG.NUISANCE_MULTIPLIERS
    RELIABILITY_RATIOS = CFG.RELIABILITY_RATIOS


# =============================================================================
# 2. EXACT 4x4 GRID
# =============================================================================

# Original numbering rule:
# row 1: 4  3  2  1
# row 2: 8  7  6  5
# row 3: 12 11 10 9
# row 4: 16 15 14 13
# x increases from left to right in the script coordinates below.
def face_xy(identity: int) -> Tuple[float, float]:
    i = int(identity)
    if i < 1 or i > 16:
        raise ValueError("identity must be 1..16")
    row = (i - 1) // 4
    col_from_right = (i - 1) % 4
    x = 4 - col_from_right
    y = 1 + row
    return float(x), float(y)


IDENTITIES = np.arange(1, 17, dtype=int)
COORDS = np.array([face_xy(i) for i in IDENTITIES], dtype=float)
COORDS_CENTERED = COORDS - COORDS.mean(axis=0, keepdims=True)
COORD_TO_INDEX = {(int(x), int(y)): idx for idx, (x, y) in enumerate(COORDS)}

TASK_PAIRS: Dict[int, Dict[str, np.ndarray]] = {}
for d in (1, 2, 3):
    horizontal: List[Tuple[int, int]] = []
    vertical: List[Tuple[int, int]] = []
    for y in range(1, 5):
        for x in range(1, 5):
            a = COORD_TO_INDEX.get((x, y))
            b = COORD_TO_INDEX.get((x + d, y))
            c = COORD_TO_INDEX.get((x, y + d))
            if a is not None and b is not None:
                horizontal.append((a, b))
            if a is not None and c is not None:
                vertical.append((a, c))
    TASK_PAIRS[d] = {
        "horizontal": np.asarray(horizontal, dtype=int),
        "vertical": np.asarray(vertical, dtype=int),
    }

CONG_VECTOR_PAIRS: Dict[Tuple[int, int], np.ndarray] = {}
_tmp: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
for i in range(16):
    for j in range(i + 1, 16):
        dx = int(COORDS[j, 0] - COORDS[i, 0])
        dy = int(COORDS[j, 1] - COORDS[i, 1])
        _tmp.setdefault((dx, dy), []).append((i, j))
for key, value in _tmp.items():
    CONG_VECTOR_PAIRS[key] = np.asarray(value, dtype=int)

# Nine equally weighted vector classes in the original rbCue congruency index.
SYMMETRIC_CLASSES = [
    ((1, 1), (-1, 1)),
    ((2, 1), (-2, 1)),
    ((1, 2), (-1, 2)),
    ((2, 2), (-2, 2)),
    ((3, 1), (-3, 1)),
    ((1, 3), (-1, 3)),
    ((3, 2), (-3, 2)),
    ((2, 3), (-2, 3)),
    ((3, 3), (-3, 3)),
]


# =============================================================================
# 3. EXACT DISTANCE + WARPING INDICES
# =============================================================================

def squared_euclidean_pairs(Y: np.ndarray, pairs: np.ndarray) -> np.ndarray:
    """Mean squared Euclidean dissimilarity across voxels."""
    Y = np.asarray(Y, dtype=float)
    P = np.asarray(pairs, dtype=int)
    if P.ndim != 2 or P.shape[1] != 2:
        raise ValueError("pairs must be (n_pairs, 2)")
    diff = Y[P[:, 0]] - Y[P[:, 1]]
    return np.mean(diff * diff, axis=1)


def task_axis_warping_index(Y_x: np.ndarray, Y_y: np.ndarray) -> float:
    """Original three-step rbCue task-axis warping index."""
    ratios = []
    for d in (1, 2, 3):
        hp = TASK_PAIRS[d]["horizontal"]
        vp = TASK_PAIRS[d]["vertical"]

        # x context: horizontal relevant; y context: vertical relevant.
        relevant = np.concatenate([
            squared_euclidean_pairs(Y_x, hp),
            squared_euclidean_pairs(Y_y, vp),
        ])
        irrelevant = np.concatenate([
            squared_euclidean_pairs(Y_x, vp),
            squared_euclidean_pairs(Y_y, hp),
        ])

        mr = float(np.mean(relevant))
        mi = float(np.mean(irrelevant))
        if not np.isfinite(mr) or not np.isfinite(mi) or mr <= 0:
            return np.nan
        ratios.append(mi / mr)
    return float(1.0 - np.mean(ratios))


def congruency_axis_warping_index(Y_x: np.ndarray, Y_y: np.ndarray) -> float:
    """Original nine-class rbCue congruency-axis warping index.

    Within each vector class, distances are pooled across x and y contexts.
    Cross-context distances are never used. The nine class ratios are equally
    weighted, irrespective of how many face pairs a class contains.
    """
    ratios = []
    for congruent_key, incongruent_key in SYMMETRIC_CLASSES:
        cp = CONG_VECTOR_PAIRS[congruent_key]
        ip = CONG_VECTOR_PAIRS[incongruent_key]

        dc = np.concatenate([
            squared_euclidean_pairs(Y_x, cp),
            squared_euclidean_pairs(Y_y, cp),
        ])
        di = np.concatenate([
            squared_euclidean_pairs(Y_x, ip),
            squared_euclidean_pairs(Y_y, ip),
        ])

        mc = float(np.mean(dc))
        mi = float(np.mean(di))
        if not np.isfinite(mc) or not np.isfinite(mi) or mc <= 0:
            return np.nan
        ratios.append(mi / mc)
    return float(1.0 - np.mean(ratios))


# =============================================================================
# 4. OPTIONAL RSATOOLBOX PARITY CHECK
# =============================================================================

def rsatoolbox_parity_check() -> Dict[str, object]:
    result: Dict[str, object] = {
        "available": False,
        "checked": False,
        "passed_up_to_common_scale": None,
        "scale": None,
        "max_abs_residual_after_scale": None,
        "error": None,
    }
    try:
        import rsatoolbox as rb  # type: ignore

        result["available"] = True
        rng = np.random.default_rng(12345)
        Y = rng.normal(size=(16, 11))
        obs = {"cond": [f"Face_{i:02d}" for i in range(1, 17)]}
        ds = rb.data.Dataset(measurements=Y, obs_descriptors=obs)
        rdm = rb.rdm.calc_rdm(ds, descriptor="cond", method="mahalanobis")
        M = np.asarray(rdm.get_matrices()[0], dtype=float)
        D = np.mean((Y[:, None, :] - Y[None, :, :]) ** 2, axis=-1)
        tri = np.triu_indices(16, 1)
        x = D[tri]
        y = M[tri]
        scale = float(np.dot(x, y) / np.dot(x, x))
        resid = y - scale * x
        passed = bool(np.allclose(y, scale * x, rtol=1e-7, atol=1e-9))
        result.update({
            "checked": True,
            "passed_up_to_common_scale": passed,
            "scale": scale,
            "max_abs_residual_after_scale": float(np.max(np.abs(resid))),
        })
    except Exception as exc:  # environment dependent
        result["error"] = repr(exc)
    return result


# =============================================================================
# 5. RANDOMNESS
# =============================================================================

BLOCK_CALIBRATION = 201
BLOCK_STRUCTURED_NULL = 301
BLOCK_RECOVERY = 401


def make_rng(block: int, *keys: int) -> np.random.Generator:
    ss = np.random.SeedSequence([CFG.BASE_SEED, int(block), *[int(k) for k in keys]])
    return np.random.default_rng(ss)


# =============================================================================
# 6. GEOMETRIC GENERATORS
# =============================================================================

SQRT2 = math.sqrt(2.0)
Q_CONG = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=float) / SQRT2


def random_basis(rng: np.random.Generator, n_voxels: int) -> np.ndarray:
    """2 x V orthogonal basis with RMS=1 per row."""
    M = rng.normal(size=(n_voxels, 2))
    Q, _ = np.linalg.qr(M)
    return Q[:, :2].T * math.sqrt(n_voxels)


def ratio_diag(rho: float, emphasize_first: bool = True) -> np.ndarray:
    rho = float(np.clip(rho, 1e-6, 1.0))
    # Constant Frobenius energy across rho.
    a = math.sqrt(2.0 / (1.0 + rho * rho))
    if emphasize_first:
        return np.array([[a, 0.0], [0.0, a * rho]], dtype=float)
    return np.array([[a * rho, 0.0], [0.0, a]], dtype=float)


def L_task_x(rho: float) -> np.ndarray:
    return ratio_diag(rho, True)


def L_task_y(rho: float) -> np.ndarray:
    return ratio_diag(rho, False)


def L_congruency(rho: float) -> np.ndarray:
    # First diagonal basis vector is (+1,+1), the theory-congruent diagonal.
    D = ratio_diag(rho, True)
    return Q_CONG @ D @ Q_CONG.T


def unit(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    n = float(np.linalg.norm(v))
    if n < 1e-12:
        raise ValueError("zero vector")
    return v / n


def add_noise(mu: np.ndarray, rng: np.random.Generator, sd: np.ndarray | float) -> np.ndarray:
    mu = np.asarray(mu, dtype=float)
    if np.isscalar(sd):
        scale = np.full(mu.shape[0], float(sd), dtype=float)
    else:
        scale = np.asarray(sd, dtype=float)
        if scale.shape != (mu.shape[0],):
            raise ValueError("row-wise noise SD must have shape (16,)")
    return mu + rng.normal(size=mu.shape) * scale[:, None]


def zscore(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    sd = float(np.std(v, ddof=1))
    if sd < 1e-12:
        return np.zeros_like(v)
    return (v - np.mean(v)) / sd


# =============================================================================
# 7. SYNTHETIC WITHIN-rbCue NUISANCE PROFILES
# =============================================================================

def idealized_profiles() -> Dict[str, Dict[str, np.ndarray]]:
    """Condition-wise exposure profiles for the complete 4x4 rbCue grid.

    difficulty:
        fraction of all face-pair comparisons containing that identity for
        which the task-relevant rank difference equals one step. This is a
        synthetic within-context processing-demand profile, not a between-task
        rbCue-vs-wCue comparison.

    congruency_exposure:
        fraction of comparisons containing that identity whose signed vector
        lies on the incongruent diagonal side (dx*dy < 0).
    """
    out: Dict[str, Dict[str, np.ndarray]] = {}
    for context in ("x", "y"):
        diff_lists: List[List[float]] = [[] for _ in range(16)]
        cong_lists: List[List[float]] = [[] for _ in range(16)]
        for i in range(16):
            for j in range(i + 1, 16):
                dx = float(COORDS[j, 0] - COORDS[i, 0])
                dy = float(COORDS[j, 1] - COORDS[i, 1])
                relevant_distance = abs(dx) if context == "x" else abs(dy)
                hard = float(relevant_distance == 1)
                incongruent = float(dx * dy < 0)
                for k in (i, j):
                    diff_lists[k].append(hard)
                    cong_lists[k].append(incongruent)
        out[context] = {
            "difficulty": np.array([np.mean(v) for v in diff_lists], dtype=float),
            "congruency_exposure": np.array([np.mean(v) for v in cong_lists], dtype=float),
        }
    return out


PROFILES = idealized_profiles()


def decision_axis_values(context: str) -> np.ndarray:
    x = COORDS_CENTERED[:, 0]
    y = COORDS_CENTERED[:, 1]
    wr = CFG.DECISION_WEIGHT_RELEVANT
    wi = CFG.DECISION_WEIGHT_IRRELEVANT
    if context == "x":
        v = wr * x + wi * y
    elif context == "y":
        v = wi * x + wr * y
    else:
        raise ValueError(context)
    return zscore(v)


def reliability_stress_sd(context: str, ratio: float) -> np.ndarray:
    """Identity-dependent noise heterogeneity with unchanged condition means."""
    r = float(ratio)
    edge = np.sqrt(np.sum(COORDS_CENTERED ** 2, axis=1))
    edge = (edge - edge.min()) / (np.ptp(edge) + 1e-12)
    if context == "x":
        mult = 1.0 + (r - 1.0) * edge
    elif context == "y":
        mult = r - (r - 1.0) * edge
    else:
        raise ValueError(context)
    return CFG.BASE_NOISE_SD * mult


# =============================================================================
# 8. SCENARIOS
# =============================================================================

STRUCTURED_SCENARIOS = [
    # Formal structured nulls only. Adversarial geometry-changing stress
    # scenarios are internal sensitivity checks, not nulls and not reported.
    "fixed_grid_null",
    "global_context_difficulty_null",
    "congruency_exposure_null",
    "unequal_reliability_null",
    "downstream_decision_weighting_null",
]

STRUCTURED_SCENARIO_FAMILY = {
    "fixed_grid_null": "main_null",
    "global_context_difficulty_null": "main_null",
    "congruency_exposure_null": "main_null",
    "unequal_reliability_null": "main_null",
    "downstream_decision_weighting_null": "main_null",
}

RECOVERY_SCENARIOS = [
    "fixed_geometry",
    "true_task_warp",
    "true_congruency_warp",
    "true_both_warps",
    "non_target_xy_anisotropy_control",
]

RECOVERY_SCENARIO_FAMILY = {
    "fixed_geometry": "negative_control",
    "true_task_warp": "positive_control",
    "true_congruency_warp": "positive_control",
    "true_both_warps": "positive_control",
    "non_target_xy_anisotropy_control": "geometric_specificity_control",
}


def simulate_subject(
    scenario: str,
    rng: np.random.Generator,
    *,
    rho: float = 1.0,
    noise_level: float = 1.0,
    nuisance_multiplier: float = 1.0,
    reliability_ratio: float = 1.5,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, object]]:
    """Generate 16 x V patterns for the two rbCue contexts."""
    B = random_basis(rng, CFG.N_VOXELS)
    X = COORDS_CENTERED
    base = X @ B
    mu_x = base.copy()
    mu_y = base.copy()

    # Random nuisance readout directions.
    g_diff = unit(rng.normal(size=CFG.N_VOXELS)) * math.sqrt(CFG.N_VOXELS)
    g_cong_random = unit(rng.normal(size=CFG.N_VOXELS)) * math.sqrt(CFG.N_VOXELS)
    g_context = unit(rng.normal(size=CFG.N_VOXELS)) * math.sqrt(CFG.N_VOXELS)

    # Directions aligned with theoretical map axes.
    g_x = unit(B[0]) * math.sqrt(CFG.N_VOXELS)
    g_y = unit(B[1]) * math.sqrt(CFG.N_VOXELS)
    g_diag = unit(B[0] + B[1]) * math.sqrt(CFG.N_VOXELS)

    meta: Dict[str, object] = {
        "directional_social_geometry_fixed": True,
        "true_task_warp": False,
        "true_congruency_warp": False,
        "downstream_weight_ratio": (
            CFG.DECISION_WEIGHT_RELEVANT / CFG.DECISION_WEIGHT_IRRELEVANT
        ),
    }

    if scenario in {"fixed_grid_null", "fixed_geometry"}:
        pass

    elif scenario == "global_context_difficulty_null":
        # Nonspecific context-wide processing demand.
        # A common offset cancels exactly in within-context pairwise distances.
        # An isotropic gain changes overall scale/SNR but not axis directionality.
        amp = CFG.DEFAULT_DIFFICULTY_AMPLITUDE * nuisance_multiplier
        gain = 1.0 + CFG.GLOBAL_CONTEXT_GAIN_DELTA * nuisance_multiplier
        mu_x = gain * mu_x + amp * g_context[None, :]
        meta["global_context_gain"] = gain
        meta["global_context_offset_amplitude"] = amp

    elif scenario == "congruency_exposure_null":
        # Fixed latent map + a random neural component associated with the
        # condition-wise frequency of incongruent comparisons.
        amp = CFG.DEFAULT_CONGRUENCY_AMPLITUDE * nuisance_multiplier
        for context, mu in (("x", mu_x), ("y", mu_y)):
            mu += (
                amp
                * zscore(PROFILES[context]["congruency_exposure"])[:, None]
                * g_cong_random[None, :]
            )

    elif scenario == "distance_structured_difficulty_stress":
        # Fixed latent map + within-context difficulty signal structured by
        # task-relevant rank distance. This is an identifiability stress test.
        amp = CFG.DEFAULT_DIFFICULTY_AMPLITUDE * nuisance_multiplier
        for context, mu in (("x", mu_x), ("y", mu_y)):
            mu += (
                amp
                * zscore(PROFILES[context]["difficulty"])[:, None]
                * g_diff[None, :]
            )

    elif scenario == "axis_aligned_difficulty_stress":
        # Worst-case difficulty signal aligned with the currently relevant map axis.
        amp = CFG.DEFAULT_DIFFICULTY_AMPLITUDE * nuisance_multiplier
        mu_x += amp * zscore(PROFILES["x"]["difficulty"])[:, None] * g_x[None, :]
        mu_y += amp * zscore(PROFILES["y"]["difficulty"])[:, None] * g_y[None, :]

    elif scenario == "axis_aligned_congruency_stress":
        amp = CFG.DEFAULT_CONGRUENCY_AMPLITUDE * nuisance_multiplier
        mu_x += (
            amp
            * zscore(PROFILES["x"]["congruency_exposure"])[:, None]
            * g_diag[None, :]
        )
        mu_y += (
            amp
            * zscore(PROFILES["y"]["congruency_exposure"])[:, None]
            * g_diag[None, :]
        )

    elif scenario == "downstream_decision_weighting_null":
        # Pure downstream weighting: neural condition means remain unchanged.
        pass

    elif scenario == "decision_signal_contamination_stress":
        # Decision-variable signal enters neural patterns while latent map remains fixed.
        amp = CFG.DEFAULT_DECISION_AMPLITUDE * nuisance_multiplier
        mu_x += amp * decision_axis_values("x")[:, None] * g_x[None, :]
        mu_y += amp * decision_axis_values("y")[:, None] * g_y[None, :]

    elif scenario == "combined_nuisance_stress":
        ad = CFG.DEFAULT_DIFFICULTY_AMPLITUDE * nuisance_multiplier
        ac = CFG.DEFAULT_CONGRUENCY_AMPLITUDE * nuisance_multiplier
        av = CFG.DEFAULT_DECISION_AMPLITUDE * nuisance_multiplier
        mu_x += ad * zscore(PROFILES["x"]["difficulty"])[:, None] * g_diff[None, :]
        mu_y += ad * zscore(PROFILES["y"]["difficulty"])[:, None] * g_diff[None, :]
        mu_x += ac * zscore(PROFILES["x"]["congruency_exposure"])[:, None] * g_cong_random[None, :]
        mu_y += ac * zscore(PROFILES["y"]["congruency_exposure"])[:, None] * g_cong_random[None, :]
        mu_x += av * decision_axis_values("x")[:, None] * g_x[None, :]
        mu_y += av * decision_axis_values("y")[:, None] * g_y[None, :]

    elif scenario == "unequal_reliability_null":
        pass  # condition means fixed; row-wise SD handled below

    elif scenario == "true_task_warp":
        mu_x = X @ L_task_x(rho) @ B
        mu_y = X @ L_task_y(rho) @ B
        meta["directional_social_geometry_fixed"] = False
        meta["true_task_warp"] = True

    elif scenario == "true_congruency_warp":
        C = L_congruency(rho)
        mu_x = X @ C @ B
        mu_y = X @ C @ B
        meta["directional_social_geometry_fixed"] = False
        meta["true_congruency_warp"] = True

    elif scenario == "true_both_warps":
        C = L_congruency(rho)
        mu_x = X @ L_task_x(rho) @ C @ B
        mu_y = X @ L_task_y(rho) @ C @ B
        meta["directional_social_geometry_fixed"] = False
        meta["true_task_warp"] = True
        meta["true_congruency_warp"] = True

    elif scenario == "non_target_xy_anisotropy_control":
        # Genuine geometric anisotropy, but not one of the two target mechanisms.
        # The SAME x/y anisotropy is applied in both task contexts. Therefore it
        # does not switch with task context and is sign-symmetric for the two
        # diagonal vector families.
        L = ratio_diag(rho, emphasize_first=True)
        mu_x = X @ L @ B
        mu_y = X @ L @ B
        meta["directional_social_geometry_fixed"] = False
        meta["non_target_geometric_anisotropy"] = True

    else:
        raise ValueError(f"Unknown scenario: {scenario}")

    if scenario == "unequal_reliability_null":
        sd_x = reliability_stress_sd("x", reliability_ratio) * noise_level
        sd_y = reliability_stress_sd("y", reliability_ratio) * noise_level
    else:
        sd_x = sd_y = CFG.BASE_NOISE_SD * noise_level

    Y_x = add_noise(mu_x, rng, sd_x)
    Y_y = add_noise(mu_y, rng, sd_y)
    return Y_x, Y_y, meta


# =============================================================================
# 9. GROUP STATISTICS
# =============================================================================

def one_sample_t_positive(x: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 3:
        return np.nan
    m = float(np.mean(x))
    s = float(np.std(x, ddof=1))
    if s < 1e-15:
        if m > 0:
            return np.inf
        if m < 0:
            return -np.inf
        return 0.0
    return m / (s / math.sqrt(len(x)))


def binom_ci(k: int, n: int, alpha: float = 0.05) -> Tuple[float, float]:
    if n <= 0:
        return np.nan, np.nan
    lo = 0.0 if k == 0 else float(beta_dist.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta_dist.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi


def classify(t_task: float, t_cong: float, joint_threshold: float) -> str:
    task = bool(np.isfinite(t_task) and t_task > joint_threshold)
    cong = bool(np.isfinite(t_cong) and t_cong > joint_threshold)
    if task and cong:
        return "both"
    if task:
        return "task_only"
    if cong:
        return "congruency_only"
    return "neither"


def simulate_study(
    scenario: str,
    *,
    block: int,
    study: int,
    cell: int,
    rho: float = 1.0,
    noise_level: float = 1.0,
    nuisance_multiplier: float = 1.0,
    reliability_ratio: float = 1.5,
) -> Dict[str, float]:
    task_vals = []
    cong_vals = []
    for s in range(CFG.N_SUBJECTS):
        rng = make_rng(block, cell, study, s)
        Yx, Yy, _ = simulate_subject(
            scenario,
            rng,
            rho=rho,
            noise_level=noise_level,
            nuisance_multiplier=nuisance_multiplier,
            reliability_ratio=reliability_ratio,
        )
        task_vals.append(task_axis_warping_index(Yx, Yy))
        cong_vals.append(congruency_axis_warping_index(Yx, Yy))

    task_arr = np.asarray(task_vals, dtype=float)
    cong_arr = np.asarray(cong_vals, dtype=float)
    return {
        "task_mean": float(np.nanmean(task_arr)),
        "congruency_mean": float(np.nanmean(cong_arr)),
        "task_t": one_sample_t_positive(task_arr),
        "congruency_t": one_sample_t_positive(cong_arr),
    }


# =============================================================================
# 10. EXACT GRID / SIGN AUDIT
# =============================================================================

def exact_grid_audit() -> pd.DataFrame:
    rows = []

    # Pair-count balance for task-axis classes.
    for d in (1, 2, 3):
        nh = len(TASK_PAIRS[d]["horizontal"])
        nv = len(TASK_PAIRS[d]["vertical"])
        rows.append({
            "audit": "task_pair_count",
            "class": f"d={d}",
            "count_a": nh,
            "count_b": nv,
            "difference": nh - nv,
            "passed": int(nh == nv),
        })

    # Pair-count balance for the nine congruency vector classes.
    for congruent, incongruent in SYMMETRIC_CLASSES:
        nc = len(CONG_VECTOR_PAIRS[congruent])
        ni = len(CONG_VECTOR_PAIRS[incongruent])
        rows.append({
            "audit": "congruency_pair_count",
            "class": f"{congruent} vs {incongruent}",
            "count_a": nc,
            "count_b": ni,
            "difference": nc - ni,
            "passed": int(nc == ni),
        })

    # Explicit pair-direction sanity checks from the original numbering rule.
    examples = [
        (4, 7, (1, 1)),
        (3, 8, (-1, 1)),
        (4, 13, (3, 3)),
        (1, 16, (-3, 3)),
    ]
    for face_a, face_b, expected_delta in examples:
        observed = tuple(int(v) for v in (COORDS[face_b - 1] - COORDS[face_a - 1]))
        passed = observed == expected_delta
        rows.append({
            "audit": "example_pair_direction",
            "class": f"Face{face_a}->Face{face_b}: observed={observed}, expected={expected_delta}",
            "count_a": np.nan,
            "count_b": np.nan,
            "difference": 0.0 if passed else 1.0,
            "passed": int(passed),
        })

    # Isotropic noiseless geometry must give exact zeros.
    Y = COORDS_CENTERED @ np.eye(2, dtype=float)
    task0 = task_axis_warping_index(Y, Y)
    cong0 = congruency_axis_warping_index(Y, Y)
    rows.extend([
        {
            "audit": "noiseless_fixed_geometry",
            "class": "task_index",
            "count_a": np.nan,
            "count_b": np.nan,
            "difference": task0,
            "passed": int(abs(task0) < 1e-12),
        },
        {
            "audit": "noiseless_fixed_geometry",
            "class": "congruency_index",
            "count_a": np.nan,
            "count_b": np.nan,
            "difference": cong0,
            "passed": int(abs(cong0) < 1e-12),
        },
    ])

    # A genuine but non-target x/y anisotropy should also give zero target indices.
    L = ratio_diag(0.5, True)
    Ynt = COORDS_CENTERED @ L
    task_nt = task_axis_warping_index(Ynt, Ynt)
    cong_nt = congruency_axis_warping_index(Ynt, Ynt)
    rows.extend([
        {
            "audit": "noiseless_non_target_xy_anisotropy",
            "class": "task_index",
            "count_a": np.nan,
            "count_b": np.nan,
            "difference": task_nt,
            "passed": int(abs(task_nt) < 1e-12),
        },
        {
            "audit": "noiseless_non_target_xy_anisotropy",
            "class": "congruency_index",
            "count_a": np.nan,
            "count_b": np.nan,
            "difference": cong_nt,
            "passed": int(abs(cong_nt) < 1e-12),
        },
    ])

    audit = pd.DataFrame(rows)
    if not bool(audit["passed"].all()):
        raise RuntimeError("Exact grid/sign audit failed.")
    return audit


# =============================================================================
# 11. FIXED-NULL JOINT THRESHOLD
# =============================================================================

def calibrate_joint_thresholds() -> pd.DataFrame:
    rows = []
    for noise_i, noise in enumerate(NOISE_LEVELS):
        max_stats = []
        task_stats = []
        cong_stats = []
        for study in range(N_CAL):
            r = simulate_study(
                "fixed_geometry",
                block=BLOCK_CALIBRATION,
                study=study,
                cell=noise_i,
                rho=1.0,
                noise_level=noise,
            )
            task_stats.append(r["task_t"])
            cong_stats.append(r["congruency_t"])
            max_stats.append(max(r["task_t"], r["congruency_t"]))
        thr = float(np.quantile(np.asarray(max_stats, dtype=float), 1.0 - CFG.ALPHA))
        rows.append({
            "noise_level": noise,
            "n_calibration_studies": N_CAL,
            "joint_threshold": thr,
            "task_t_mean": float(np.mean(task_stats)),
            "congruency_t_mean": float(np.mean(cong_stats)),
            "max_t_95": thr,
        })
    return pd.DataFrame(rows)


# =============================================================================
# 12. FORMAL STRUCTURED NULLS
# =============================================================================

def structured_cells() -> List[Tuple[str, float, float]]:
    cells: List[Tuple[str, float, float]] = []
    multiplier_scenarios = {
        "global_context_difficulty_null",
        "congruency_exposure_null",
    }
    for scenario in STRUCTURED_SCENARIOS:
        if scenario == "unequal_reliability_null":
            for rr in RELIABILITY_RATIOS:
                cells.append((scenario, 1.0, float(rr)))
        elif scenario in multiplier_scenarios:
            for mult in NUISANCE_MULTIPLIERS:
                cells.append((scenario, float(mult), 1.0))
        else:
            cells.append((scenario, 1.0, 1.0))
    return cells


def run_structured_nulls(thresholds: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if 1.0 not in set(float(v) for v in thresholds.noise_level):
        raise RuntimeError("Need calibrated threshold at noise_level=1.0")
    thr = float(
        thresholds.loc[np.isclose(thresholds.noise_level, 1.0), "joint_threshold"].iloc[0]
    )

    raw_rows = []
    for cell, (scenario, mult, rr) in enumerate(structured_cells()):
        family = STRUCTURED_SCENARIO_FAMILY[scenario]
        for study in range(N_NULL):
            r = simulate_study(
                scenario,
                block=BLOCK_STRUCTURED_NULL,
                study=study,
                cell=cell,
                rho=1.0,
                noise_level=1.0,
                nuisance_multiplier=mult,
                reliability_ratio=rr,
            )
            label = classify(r["task_t"], r["congruency_t"], thr)
            raw_rows.append({
                "scenario": scenario,
                "scenario_family": family,
                "nuisance_multiplier": mult,
                "reliability_ratio": rr,
                "study": study,
                **r,
                "joint_threshold": thr,
                "detected": label,
                "task_detected": int(label in {"task_only", "both"}),
                "congruency_detected": int(label in {"congruency_only", "both"}),
                "any_detected": int(label != "neither"),
            })
        print(
            f"structured done: {scenario}, family={family}, mult={mult}, rr={rr}",
            flush=True,
        )

    raw = pd.DataFrame(raw_rows)
    summary_rows = []
    group_cols = ["scenario", "scenario_family", "nuisance_multiplier", "reliability_ratio"]
    for keys, g in raw.groupby(group_cols, dropna=False):
        scenario, family, mult, rr = keys
        n = len(g)
        for outcome in ("task_detected", "congruency_detected", "any_detected"):
            k = int(g[outcome].sum())
            lo, hi = binom_ci(k, n)
            summary_rows.append({
                "scenario": scenario,
                "scenario_family": family,
                "nuisance_multiplier": mult,
                "reliability_ratio": rr,
                "outcome": outcome,
                "n_studies": n,
                "n_detected": k,
                "rate": k / n,
                "ci95_low": lo,
                "ci95_high": hi,
                "mean_task_index": float(g.task_mean.mean()),
                "mean_congruency_index": float(g.congruency_mean.mean()),
                "mean_task_t": float(g.task_t.mean()),
                "mean_congruency_t": float(g.congruency_t.mean()),
            })
    return raw, pd.DataFrame(summary_rows)


# =============================================================================
# 13. GEOMETRIC RECOVERY / CROSS-TALK
# =============================================================================

def expected_label(scenario: str, rho: float) -> str:
    if rho >= 0.999999:
        return "neither"
    return {
        "fixed_geometry": "neither",
        "true_task_warp": "task_only",
        "true_congruency_warp": "congruency_only",
        "true_both_warps": "both",
        "non_target_xy_anisotropy_control": "neither",
    }[scenario]


def run_recovery(
    thresholds: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    thr_map = {
        float(r.noise_level): float(r.joint_threshold)
        for _, r in thresholds.iterrows()
    }
    rows = []
    cell = 0
    for noise in NOISE_LEVELS:
        thr = thr_map[float(noise)]
        for rho in RHO_VALUES:
            for scenario in RECOVERY_SCENARIOS:
                family = RECOVERY_SCENARIO_FAMILY[scenario]
                for study in range(N_RECOVERY):
                    r = simulate_study(
                        scenario,
                        block=BLOCK_RECOVERY,
                        study=study,
                        cell=cell,
                        rho=float(rho),
                        noise_level=float(noise),
                    )
                    label = classify(r["task_t"], r["congruency_t"], thr)
                    truth = expected_label(scenario, float(rho))
                    rows.append({
                        "scenario": scenario,
                        "scenario_family": family,
                        "rho": rho,
                        "noise_level": noise,
                        "study": study,
                        **r,
                        "joint_threshold": thr,
                        "expected": truth,
                        "recovered": label,
                        "correct": int(label == truth),
                        "task_detected": int(label in {"task_only", "both"}),
                        "congruency_detected": int(label in {"congruency_only", "both"}),
                    })
                cell += 1
                print(
                    f"recovery done: noise={noise}, rho={rho}, scenario={scenario}",
                    flush=True,
                )

    raw = pd.DataFrame(rows)
    summary_rows = []
    for keys, g in raw.groupby(["scenario", "scenario_family", "rho", "noise_level"]):
        scenario, family, rho, noise = keys
        n = len(g)
        k = int(g.correct.sum())
        lo, hi = binom_ci(k, n)
        summary_rows.append({
            "scenario": scenario,
            "scenario_family": family,
            "rho": rho,
            "noise_level": noise,
            "expected": g.expected.iloc[0],
            "n_studies": n,
            "n_correct": k,
            "recovery_accuracy": k / n,
            "ci95_low": lo,
            "ci95_high": hi,
            "task_detection_rate": float(g.task_detected.mean()),
            "congruency_detection_rate": float(g.congruency_detected.mean()),
            "mean_task_index": float(g.task_mean.mean()),
            "mean_congruency_index": float(g.congruency_mean.mean()),
        })
    summary = pd.DataFrame(summary_rows)

    confusion = (
        raw.groupby([
            "scenario",
            "scenario_family",
            "rho",
            "noise_level",
            "expected",
            "recovered",
        ])
        .size()
        .rename("n")
        .reset_index()
    )
    confusion["proportion"] = confusion.groupby(
        ["scenario", "rho", "noise_level"]
    )["n"].transform(lambda x: x / x.sum())

    return raw, summary, confusion


# =============================================================================
# 14. PLOTS
# =============================================================================

def plot_structured_family(summary: pd.DataFrame, family: str, filename: str) -> None:
    d = summary[
        summary.scenario_family.eq(family) & summary.outcome.eq("any_detected")
    ].copy()
    if d.empty:
        return

    labels, rates, lows, highs = [], [], [], []
    for _, r in d.iterrows():
        if r.scenario == "unequal_reliability_null":
            label = f"reliability x{r.reliability_ratio:g}"
        elif r.nuisance_multiplier != 1.0:
            label = f"{r.scenario}\n×{r.nuisance_multiplier:g}"
        else:
            label = str(r.scenario)
        labels.append(label)
        rates.append(float(r.rate))
        lows.append(float(r.rate - r.ci95_low))
        highs.append(float(r.ci95_high - r.rate))

    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(max(10, len(labels) * 0.85), 6))
    ax.bar(x, rates)
    ax.errorbar(x, rates, yerr=np.vstack([lows, highs]), fmt="none", capsize=3)
    ax.axhline(CFG.ALPHA, linestyle="--", linewidth=1)
    ax.set_ylabel("Any-index detection rate")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=40, ha="right")
    ax.set_ylim(0, min(1.0, max(0.15, max(rates) * 1.2)))
    ax.set_title(f"{family}: joint two-index detection")
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=220)
    plt.close(fig)


def plot_recovery(summary: pd.DataFrame) -> None:
    for noise in sorted(summary.noise_level.unique()):
        d = summary[np.isclose(summary.noise_level, noise)]
        fig, ax = plt.subplots(figsize=(9, 6))
        for scenario in RECOVERY_SCENARIOS:
            z = d[d.scenario.eq(scenario)].sort_values("rho")
            ax.plot(z.rho, z.recovery_accuracy, marker="o", label=scenario)
        ax.set_xlabel("rho (1 = no anisotropy; smaller = stronger transform)")
        ax.set_ylabel("Correct recovery proportion")
        ax.set_ylim(0, 1.02)
        ax.set_title(f"Mechanism/index recovery — noise level {noise:g}")
        ax.legend(frameon=False, fontsize=8)
        fig.tight_layout()
        fig.savefig(OUT / f"recovery_accuracy_noise_{noise:g}.png", dpi=220)
        plt.close(fig)


def plot_index_strength(summary: pd.DataFrame) -> None:
    for scenario, ycol, ylabel in (
        ("true_task_warp", "mean_task_index", "Mean task-axis warping index"),
        ("true_congruency_warp", "mean_congruency_index", "Mean congruency-axis warping index"),
    ):
        d = summary[summary.scenario.eq(scenario)]
        fig, ax = plt.subplots(figsize=(8, 6))
        for noise in sorted(d.noise_level.unique()):
            z = d[np.isclose(d.noise_level, noise)].sort_values("rho")
            ax.plot(z.rho, z[ycol], marker="o", label=f"noise={noise:g}")
        ax.axhline(0.0, linewidth=1)
        ax.set_xlabel("rho")
        ax.set_ylabel(ylabel)
        ax.set_title(f"Warp-strength sensitivity — {scenario}")
        ax.legend(frameon=False)
        fig.tight_layout()
        fig.savefig(OUT / f"warp_strength_{scenario}.png", dpi=220)
        plt.close(fig)


# =============================================================================
# 15. MAIN
# =============================================================================

def main() -> None:
    if OUT.exists() and any(OUT.iterdir()):
        raise SystemExit(f"Output directory is non-empty; choose a new --output: {OUT}")
    OUT.mkdir(parents=True, exist_ok=True)

    print("=" * 84)
    print("Reviewer #4 rbCue warping-index validation v6")
    print(f"MODE={ARGS.mode}")
    print(f"N_SUBJECTS={CFG.N_SUBJECTS}, N_VOXELS={CFG.N_VOXELS}")
    print(f"N_CAL={N_CAL}, N_NULL={N_NULL}, N_RECOVERY={N_RECOVERY}")
    print("DATA SCOPE: rbCue only; two single-dimensional task contexts; wCue excluded")
    print("Estimator: mean squared Euclidean; positive omega = theory-predicted expansion")
    print("Congruency: 9 equally weighted vector classes; within-context x/x + y/y only")
    print("Scope: estimator simulation, not whole-brain spatial/FWE simulation")
    print("=" * 84, flush=True)

    audit = exact_grid_audit()
    audit.to_csv(OUT / "grid_combinatorics_audit.csv", index=False)

    parity = rsatoolbox_parity_check()
    with (OUT / "rsatoolbox_parity.json").open("w", encoding="utf-8") as f:
        json.dump(parity, f, indent=2)
    if ARGS.strict_rsatoolbox_parity:
        if not parity.get("checked") or not parity.get("passed_up_to_common_scale"):
            raise SystemExit(f"Strict rsatoolbox parity check failed/skipped: {parity}")

    thresholds = calibrate_joint_thresholds()
    thresholds.to_csv(OUT / "fixed_null_joint_thresholds.csv", index=False)

    structured_raw, structured_summary = run_structured_nulls(thresholds)
    structured_raw.to_csv(OUT / "structured_null_studies.csv", index=False)
    structured_summary.to_csv(OUT / "structured_null_summary.csv", index=False)
    structured_summary.to_csv(OUT / "structured_null_main.csv", index=False)

    rec_raw, rec_summary, rec_conf = run_recovery(thresholds)
    rec_raw.to_csv(OUT / "recovery_studies.csv", index=False)
    rec_summary.to_csv(OUT / "recovery_summary.csv", index=False)
    rec_summary.to_csv(OUT / "recovery_primary.csv", index=False)
    rec_conf.to_csv(OUT / "mechanism_recovery_confusion.csv", index=False)

    plot_structured_family(
        structured_summary,
        "main_null",
        "structured_main_null_detection.png",
    )
    plot_recovery(rec_summary)
    plot_index_strength(rec_summary)

    metadata = {
        **asdict(CFG),
        "mode": ARGS.mode,
        "n_calibration_studies": N_CAL,
        "n_structured_studies_per_cell": N_NULL,
        "n_recovery_studies_per_cell": N_RECOVERY,
        "rho_values": list(RHO_VALUES),
        "noise_levels": list(NOISE_LEVELS),
        "nuisance_multipliers": list(NUISANCE_MULTIPLIERS),
        "reliability_ratios": list(RELIABILITY_RATIOS),
        "analysis_scope": "rbCue_only_six_runs_two_single_dimension_contexts",
        "wCue_included": False,
        "distance": "mean_squared_euclidean",
        "task_index": "1 - mean_d(mean_irrelevant_d / mean_relevant_d), d=1..3",
        "congruency_index": "1 - mean_9(mean_incongruent_k / mean_congruent_k)",
        "congruency_pooling": (
            "within each vector class, pool x-context and y-context distances; "
            "never compute cross-context distances; nine class ratios equally weighted"
        ),
        "difficulty_definition": (
            "synthetic within-rbCue processing-demand exposure based on one-step "
            "task-relevant rank difference; not a rbCue-vs-wCue difficulty contrast"
        ),
        "structured_scenario_families": STRUCTURED_SCENARIO_FAMILY,
        "formal_structured_nulls_only": True,
        "recovery_scenario_families": RECOVERY_SCENARIO_FAMILY,
        "scope_warning": (
            "Estimator-level sensitivity/specificity simulation only; does not reproduce "
            "whole-brain spatial/FWE selection and does not by itself exclude empirical confounds."
        ),
        "rsatoolbox_parity": parity,
    }
    with (OUT / "analysis_metadata.json").open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("\nDone.")
    print(f"Results written to: {OUT.resolve()}")
    print("Key outputs:")
    for name in (
        "grid_combinatorics_audit.csv",
        "rsatoolbox_parity.json",
        "fixed_null_joint_thresholds.csv",
        "structured_null_main.csv",
        "recovery_primary.csv",
        "mechanism_recovery_confusion.csv",
        "analysis_metadata.json",
    ):
        print(f"  {name}")


if __name__ == "__main__":
    main()
