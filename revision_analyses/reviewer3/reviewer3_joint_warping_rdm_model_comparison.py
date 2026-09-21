#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reviewer 3: held-out-identity comparison of four representational accounts
============================================================================

This script is deliberately aligned with the manuscript's 32-condition
single-dimensional-task RDM (16 identities x 2 task contexts):

    Red  = morality context
    Blue = competence context
    x    = morality rank
    y    = competence rank

It does NOT load the mixed-dimensional-task data.

The same 32-condition patterns are used for all models.  Within each
searchlight and cross-validation fold, models are fitted only to within-context
neural dissimilarities among TRAINING identities and evaluated only on pairs
formed entirely by HELD-OUT identities.

Four prespecified models are compared:

1. fixed_2d
   One context-invariant Euclidean 2-D distance predictor.

2. theory_joint_warping
   A joint theory-constrained model containing BOTH manuscript warps:

       base       = dx^2 + dy^2
       task axis  = s_context * (dx^2 - dy^2)
       congruency = 2 * dx * dy

   where s_Red=+1 and s_Blue=-1.  A positive task component therefore
   stretches morality in Red and competence in Blue.  A positive congruency
   component stretches the congruent diagonal relative to the incongruent
   diagonal.  The normalized task and congruency strengths are non-negative
   and jointly constrained so the two context metrics remain positive definite.

3. context_dimension_weighting
   Separate non-negative morality/competence weights in Red and Blue.  This is
   the reviewer's context-dependent weighting alternative.  It can express
   original-axis weighting but contains no dx*dy cross-term.

4. context_specific_quadratic_predictor
   Separate context-specific quadratic predictors of the fixed 2-D
   coordinates, including a free cross-term in each context.  This is an
   intentionally flexible predictive benchmark, not a literal downstream
   biological readout.  The companion direct-pattern analysis contains the
   explicit context-specific linear-readout comparison.

All models include separate Red and Blue nuisance intercepts to absorb a
context-specific dissimilarity noise floor.  The theory model is parameterized
as a positive-definite 2-D metric, with task and congruency strengths restricted
to a prespecified quarter disk.  This guarantees that its predictions describe
a valid geometric deformation.  Non-negative coefficients in the other
structured models are fitted by exact active-set enumeration; cross-terms in
the broad quadratic benchmark are unconstrained.

Primary score:
    held-out CV-MSE across all within-context pairs formed entirely by test
    identities.

Secondary scores:
    - task-pair MSE: axial pairs (exactly one of dx,dy is zero), corresponding
      to the face-pair subset underlying task-relevant-axis warping;
    - congruency-pair MSE: non-axial pairs (both dx and dy are non-zero),
      spanning the nine (|dx|,|dy|) direction families whose congruent and
      incongruent members are geometrically matched in the 4x4 grid.

The two secondary subsets may overlap across the manuscript's original index
construction at the identity level; no independence between them is assumed.
They are descriptive.  Formal group inference is based on the single primary
held-out prediction score and three prespecified theory-vs-comparator contrasts.

Contrast definition:
    delta_CV_MSE = MSE_comparator - MSE_theory

Positive values favor the theory model.  Formal inference uses one two-sided
global max-|t| sign-flip null controlling FWER jointly over whole-brain space
and all three model contrasts.  Training MSE maps are saved only as descriptive
optimization QC and are never used for formal group inference.

SEARCHLIGHT RADIUS IS 3 VOXELS (nominally 6 mm on the 2-mm grid).
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

import nibabel as nib
import numba
import numpy as np
import pandas as pd
import scipy
from numba import njit


# ============================================================================
# 1. CONFIGURATION
# ============================================================================

ALL_SUBJECTS = [
    "001", "002", "003", "004", "006", "007",
    "009", "010", "011", "015", "017", "018",
    "019", "021", "022", "023", "024", "025",
    "026", "027", "028", "029", "030", "031",
]

# Run TEST001 first.  After checking its outputs, change this to FORMAL.
RUN_MODE = "TEST001"
if RUN_MODE not in {"TEST001", "FORMAL"}:
    raise ValueError("RUN_MODE must be TEST001 or FORMAL")
IS_TEST = RUN_MODE == "TEST001"
SUBJECTS = ["001"] if IS_TEST else ALL_SUBJECTS

RBCUE_TEMPLATE = "/home/medicaldata3/LJData/rsa/rbCue/stats.{subj}_REML.nii"
MASK_PATH = (
    "/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/"
    "brainMeanMaskrb.nii"
)

OUTPUT_BASE = Path(
    "/home/image030/analysis_code/new_gmj/results/"
    "reviewer3_joint_warping_rdm_model_comparison"
)
OUTPUT_DIR = OUTPUT_BASE / RUN_MODE

SEARCHLIGHT_RADIUS_VOX = 3
MIN_SPHERE_VOXELS = 20
VOXEL_SD_MIN = 1e-8
CONTEXT_RMS_MIN = 1e-8
RIDGE_EPS = 1e-8

# Positive-definite theory metric:
#   G_Red  = [[1+t, g], [g, 1-t]]
#   G_Blue = [[1-t, g], [g, 1+t]]
# with t>=0, g>=0, and t^2+g^2 <= THEORY_RADIUS_MAX^2 < 1.
THEORY_RADIUS_MAX = 0.95
THEORY_GRID_POINTS = 7
THEORY_REFINEMENT_LEVELS = 4

# 4 folds: 12 training identities and 4 identities completely held out.
N_FOLDS = 4
CV_SEED = 20260918

N_JOBS = 8
CENTER_CHUNK = 200

RUN_GROUP_INFERENCE = RUN_MODE == "FORMAL"
N_SIGNFLIP = 20000
SIGNFLIP_BATCH = 16
SIGNFLIP_SEED = 20260926


# ============================================================================
# 2. SOCIAL COORDINATES, CONTEXTS, AND CV PAIRS
# ============================================================================

IDENTITIES = np.arange(1, 17, dtype=np.int64)


def face_xy(identity: int):
    """Manuscript coordinate convention: x=morality, y=competence."""
    z = int(identity) - 1
    return float(3 - (z % 4)), float(z // 4)


COORDS = np.asarray([face_xy(i) for i in IDENTITIES], dtype=np.float64)
CONTEXT_NAMES = ("Red_morality", "Blue_competence")
CONTEXT_SIGNS = np.asarray([+1.0, -1.0], dtype=np.float64)


def build_cv():
    if len(IDENTITIES) % N_FOLDS:
        raise RuntimeError("The 16 identities must split evenly across folds")
    rng = np.random.default_rng(CV_SEED)
    folds = np.split(rng.permutation(IDENTITIES), N_FOLDS)
    out = []
    for fold_i, test_ids in enumerate(folds):
        test_set = set(int(x) for x in test_ids)
        train_ids = np.asarray(
            [int(x) for x in IDENTITIES if int(x) not in test_set],
            dtype=np.int64,
        )
        test_ids = np.asarray(test_ids, dtype=np.int64)
        if len(train_ids) != 12 or len(test_ids) != 4:
            raise RuntimeError("Expected 12 train and 4 test identities")
        if set(train_ids.tolist()) & set(test_ids.tolist()):
            raise RuntimeError("Identity leakage in CV split")
        out.append((fold_i, train_ids, test_ids))
    return out


CV_SPLITS = build_cv()
EXPECTED_VALID_FOLDS = len(CV_SPLITS)


def identity_rows(ids):
    return np.asarray([int(i) - 1 for i in ids], dtype=np.int64)


def pair_spec(ids):
    """Within-context identity pairs, repeated once for Red and once for Blue."""
    rows = identity_rows(ids)
    rec = []
    for context in (0, 1):
        for a in range(len(rows)):
            for b in range(a + 1, len(rows)):
                i = int(rows[a])
                j = int(rows[b])
                dx = float(COORDS[i, 0] - COORDS[j, 0])
                dy = float(COORDS[i, 1] - COORDS[j, 1])
                rec.append((context, i, j, dx, dy))
    return np.asarray(rec, dtype=np.float64)


PAIR_FOLDS = []
for fold_i, train_ids, test_ids in CV_SPLITS:
    PAIR_FOLDS.append(
        {
            "fold": int(fold_i),
            "train_ids": train_ids,
            "test_ids": test_ids,
            "train_rows": identity_rows(train_ids),
            "test_rows": identity_rows(test_ids),
            "train_pairs": pair_spec(train_ids),
            "test_pairs": pair_spec(test_ids),
        }
    )


def serialize_splits():
    return [
        {
            "fold": int(x["fold"]),
            "train_ids": [int(v) for v in x["train_ids"]],
            "test_ids": [int(v) for v in x["test_ids"]],
            "n_train_pairs_both_contexts": int(len(x["train_pairs"])),
            "n_test_pairs_both_contexts": int(len(x["test_pairs"])),
        }
        for x in PAIR_FOLDS
    ]


# ============================================================================
# 3. MODEL DESIGN MATRICES
# ============================================================================

MODEL_NAMES = [
    "fixed_2d",
    "theory_joint_warping",
    "context_dimension_weighting",
    "context_specific_quadratic_predictor",
]

CONTRAST_NAMES = [
    "fixed_minus_theory",
    "weighting_minus_theory",
    "quadratic_minus_theory",
]

PRIMARY_MAP_NAMES = [
    "fixed_mse",
    "theory_mse",
    "weighting_mse",
    "quadratic_mse",
    *CONTRAST_NAMES,
]

SECONDARY_MAP_NAMES = [
    f"{m}_{subset}_mse"
    for subset in ("task_pairs", "congruency_pairs")
    for m in ("fixed", "theory", "weighting", "quadratic")
]

PARAMETER_MAP_NAMES = [
    "theory_base_coefficient",
    "theory_task_axis_coefficient",
    "theory_congruency_axis_coefficient",
    "theory_task_strength",
    "theory_congruency_strength",
]

TRAIN_QC_MAP_NAMES = [
    "fixed_train_mse",
    "theory_train_mse",
    "weighting_train_mse",
    "quadratic_train_mse",
]

MAP_NAMES = (
    PRIMARY_MAP_NAMES + SECONDARY_MAP_NAMES + PARAMETER_MAP_NAMES
    + TRAIN_QC_MAP_NAMES
)


@njit(cache=True)
def pair_components(spec):
    context = spec[:, 0].astype(np.int64)
    dx = spec[:, 3]
    dy = spec[:, 4]
    x2 = dx * dx
    y2 = dy * dy
    xy2 = 2.0 * dx * dy
    base = x2 + y2
    sign = CONTEXT_SIGNS[context]
    task = sign * (x2 - y2)
    red = (context == 0).astype(np.float64)
    blue = (context == 1).astype(np.float64)
    return context, red, blue, x2, y2, xy2, base, task


def model_designs(spec):
    """
    Return design matrices with FREE coefficients first and NON-NEGATIVE
    coefficients last.  This ordering is required by the active-set fitter.
    """
    context, red, blue, x2, y2, xy2, base, task = pair_components(spec)

    # fixed: free Red/Blue intercepts; non-negative common Euclidean slope.
    fixed = np.column_stack([red, blue, base])

    # Placeholder component matrix for theory. The formal theory fit below
    # uses the positive-definite quarter-disk parameterization rather than
    # unconstrained independent base/task/congruency coefficients.
    theory = np.column_stack([red, blue, base, task, xy2])

    # weighting: free intercepts; four non-negative original-axis weights.
    weighting = np.column_stack([
        red,
        blue,
        red * x2,
        red * y2,
        blue * x2,
        blue * y2,
    ])

    # broad quadratic benchmark: free intercepts and context-specific
    # cross-terms first;
    # four original-axis diagonal weights are constrained non-negative.
    quadratic = np.column_stack([
        red,
        blue,
        red * xy2,
        blue * xy2,
        red * x2,
        red * y2,
        blue * x2,
        blue * y2,
    ])

    return (
        np.ascontiguousarray(fixed, dtype=np.float64),
        np.ascontiguousarray(theory, dtype=np.float64),
        np.ascontiguousarray(weighting, dtype=np.float64),
        np.ascontiguousarray(quadratic, dtype=np.float64),
    )


for fold in PAIR_FOLDS:
    fold["train_designs"] = model_designs(fold["train_pairs"])
    fold["test_designs"] = model_designs(fold["test_pairs"])
    _, _, _, x2, y2, _, _, _ = pair_components(fold["test_pairs"])
    axial = ((x2 == 0.0) & (y2 > 0.0)) | ((y2 == 0.0) & (x2 > 0.0))
    diagonal = (x2 > 0.0) & (y2 > 0.0)
    fold["test_task_mask"] = axial
    fold["test_congruency_mask"] = diagonal


# ============================================================================
# 4. FAST CONSTRAINED REGRESSION
# ============================================================================

@njit(cache=True)
def fit_active_set_nonnegative(Xtr, ytr, Xte, n_free, n_nonnegative):
    """
    Exact enumeration over active sets for a small partially non-negative
    least-squares problem.  The first n_free coefficients are unconstrained;
    the remaining n_nonnegative coefficients are constrained >= 0.
    """
    p = Xtr.shape[1]
    best_sse = 1e300
    best_beta = np.zeros(p, dtype=np.float64)
    found = False

    for mask in range(1 << n_nonnegative):
        n_active = 0
        for k in range(n_nonnegative):
            if mask & (1 << k):
                n_active += 1

        q = n_free + n_active
        active = np.empty(q, dtype=np.int64)
        for k in range(n_free):
            active[k] = k
        pos = n_free
        for k in range(n_nonnegative):
            if mask & (1 << k):
                active[pos] = n_free + k
                pos += 1

        A = np.zeros((q, q), dtype=np.float64)
        b = np.zeros(q, dtype=np.float64)
        for r in range(Xtr.shape[0]):
            yr = ytr[r]
            for a in range(q):
                xa = Xtr[r, active[a]]
                b[a] += xa * yr
                for c in range(q):
                    A[a, c] += xa * Xtr[r, active[c]]
        for a in range(q):
            A[a, a] += RIDGE_EPS

        # RIDGE_EPS makes every active-set normal equation nonsingular in
        # practice and avoids exception handling inside Numba nopython code.
        coef = np.linalg.solve(A, b)

        feasible = True
        for a in range(n_free, q):
            if coef[a] < -1e-10 or not np.isfinite(coef[a]):
                feasible = False
                break
        if not feasible:
            continue

        beta = np.zeros(p, dtype=np.float64)
        for a in range(q):
            value = coef[a]
            if a >= n_free and value < 0.0:
                value = 0.0
            beta[active[a]] = value

        sse = 0.0
        for r in range(Xtr.shape[0]):
            pred = 0.0
            for c in range(p):
                pred += Xtr[r, c] * beta[c]
            err = ytr[r] - pred
            sse += err * err

        if np.isfinite(sse) and sse < best_sse:
            best_sse = sse
            best_beta = beta
            found = True

    if not found:
        return np.full(Xte.shape[0], np.nan), np.full(p, np.nan), np.nan

    pred = Xte @ best_beta
    return pred, best_beta, best_sse / max(1, Xtr.shape[0])


@njit(cache=True)
def _profile_theory(
    context_tr, base_tr, task_tr, congr_tr, ytr,
    context_te, base_te, task_te, congr_te,
    task_strength, congruency_strength,
):
    """Fit context intercepts and a common non-negative scale for one SPD metric."""
    ntr = ytr.shape[0]
    qtr = (
        base_tr
        + task_strength * task_tr
        + congruency_strength * congr_tr
    )

    mean_q = np.zeros(2, dtype=np.float64)
    mean_y = np.zeros(2, dtype=np.float64)
    counts = np.zeros(2, dtype=np.int64)
    for i in range(ntr):
        c = context_tr[i]
        mean_q[c] += qtr[i]
        mean_y[c] += ytr[i]
        counts[c] += 1
    for c in range(2):
        if counts[c] == 0:
            return (
                np.full(context_te.shape[0], np.nan),
                np.full(5, np.nan),
                np.nan,
            )
        mean_q[c] /= counts[c]
        mean_y[c] /= counts[c]

    numerator = 0.0
    denominator = RIDGE_EPS
    for i in range(ntr):
        c = context_tr[i]
        qc = qtr[i] - mean_q[c]
        yc = ytr[i] - mean_y[c]
        numerator += qc * yc
        denominator += qc * qc
    scale = max(0.0, numerator / denominator)
    intercept = np.empty(2, dtype=np.float64)
    for c in range(2):
        intercept[c] = mean_y[c] - scale * mean_q[c]

    sse = 0.0
    for i in range(ntr):
        c = context_tr[i]
        pred_i = intercept[c] + scale * qtr[i]
        err = ytr[i] - pred_i
        sse += err * err

    pred = np.empty(context_te.shape[0], dtype=np.float64)
    for i in range(context_te.shape[0]):
        q = (
            base_te[i]
            + task_strength * task_te[i]
            + congruency_strength * congr_te[i]
        )
        pred[i] = intercept[context_te[i]] + scale * q

    # Red intercept, Blue intercept, overall scale, normalized task strength,
    # normalized congruency strength.
    pars = np.asarray([
        intercept[0], intercept[1], scale,
        task_strength, congruency_strength,
    ])
    return pred, pars, sse / max(1, ntr)


@njit(cache=True)
def _theory_sufficient_statistics(context, base, task, congr, y):
    """Context-centered cross-products for O(1) theory grid evaluation."""
    means = np.zeros((2, 4), dtype=np.float64)
    counts = np.zeros(2, dtype=np.int64)
    for i in range(y.shape[0]):
        c = context[i]
        means[c, 0] += base[i]
        means[c, 1] += task[i]
        means[c, 2] += congr[i]
        means[c, 3] += y[i]
        counts[c] += 1
    for c in range(2):
        for k in range(4):
            means[c, k] /= counts[c]

    # BB, TT, GG, BT, BG, TG, yB, yT, yG, yy
    s = np.zeros(10, dtype=np.float64)
    for i in range(y.shape[0]):
        c = context[i]
        b = base[i] - means[c, 0]
        t = task[i] - means[c, 1]
        g = congr[i] - means[c, 2]
        yy = y[i] - means[c, 3]
        s[0] += b * b
        s[1] += t * t
        s[2] += g * g
        s[3] += b * t
        s[4] += b * g
        s[5] += t * g
        s[6] += yy * b
        s[7] += yy * t
        s[8] += yy * g
        s[9] += yy * yy
    return s


@njit(cache=True)
def _theory_mse_from_sufficient(s, n, t, g):
    denominator = (
        s[0] + t * t * s[1] + g * g * s[2]
        + 2.0 * t * s[3] + 2.0 * g * s[4] + 2.0 * t * g * s[5]
        + RIDGE_EPS
    )
    numerator = s[6] + t * s[7] + g * s[8]
    scale = max(0.0, numerator / denominator)
    sse = s[9] - 2.0 * scale * numerator + scale * scale * denominator
    if sse < 0.0 and abs(sse) < 1e-8:
        sse = 0.0
    return sse / max(1, n)


@njit(cache=True)
def fit_theory_positive_definite(train_spec, test_spec, ytr):
    ctr, _, _, _, _, congr_tr, base_tr, task_tr = pair_components(train_spec)
    cte, _, _, _, _, congr_te, base_te, task_te = pair_components(test_spec)

    t_lo, t_hi = 0.0, THEORY_RADIUS_MAX
    g_lo, g_hi = 0.0, THEORY_RADIUS_MAX
    best_t = 0.0
    best_g = 0.0
    best_mse = 1e300
    sufficient = _theory_sufficient_statistics(
        ctr, base_tr, task_tr, congr_tr, ytr
    )

    for _ in range(THEORY_REFINEMENT_LEVELS):
        t_step = (t_hi - t_lo) / (THEORY_GRID_POINTS - 1)
        g_step = (g_hi - g_lo) / (THEORY_GRID_POINTS - 1)
        local_best = 1e300
        local_i = 0
        local_j = 0
        for i in range(THEORY_GRID_POINTS):
            t = t_lo + i * t_step
            for j in range(THEORY_GRID_POINTS):
                g = g_lo + j * g_step
                if t * t + g * g > THEORY_RADIUS_MAX * THEORY_RADIUS_MAX:
                    continue
                mse = _theory_mse_from_sufficient(
                    sufficient, ytr.shape[0], t, g
                )
                if mse < local_best:
                    local_best = mse
                    local_i = i
                    local_j = j
                if mse < best_mse:
                    best_mse = mse
                    best_t = t
                    best_g = g

        new_t_lo = t_lo + max(0, local_i - 1) * t_step
        new_t_hi = t_lo + min(THEORY_GRID_POINTS - 1, local_i + 1) * t_step
        new_g_lo = g_lo + max(0, local_j - 1) * g_step
        new_g_hi = g_lo + min(THEORY_GRID_POINTS - 1, local_j + 1) * g_step
        t_lo, t_hi = new_t_lo, new_t_hi
        g_lo, g_hi = new_g_lo, new_g_hi

    return _profile_theory(
        ctr, base_tr, task_tr, congr_tr, ytr,
        cte, base_te, task_te, congr_te,
        best_t, best_g,
    )


def fit_four_models(train_spec, test_spec, train_designs, test_designs, y_train):
    fixed_tr, _theory_tr, weighting_tr, quadratic_tr = train_designs
    fixed_te, _theory_te, weighting_te, quadratic_te = test_designs

    fixed = fit_active_set_nonnegative(fixed_tr, y_train, fixed_te, 2, 1)
    theory = fit_theory_positive_definite(
        train_spec, test_spec, y_train
    )
    weighting = fit_active_set_nonnegative(
        weighting_tr, y_train, weighting_te, 2, 4
    )
    quadratic = fit_active_set_nonnegative(
        quadratic_tr, y_train, quadratic_te, 4, 4
    )

    fits = (fixed, theory, weighting, quadratic)
    predictions = [np.asarray(x[0], dtype=np.float64) for x in fits]
    betas = [np.asarray(x[1], dtype=np.float64) for x in fits]
    train_mse = [float(x[2]) for x in fits]
    return predictions, betas, train_mse


# ============================================================================
# 5. AFNI INPUT
# ============================================================================

RB_RE = re.compile(r"^(RedFace|BlueFace)_?([1-9]|1[0-6])#0_Coef$")


def command_output(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return ((p.stdout or "") + (p.stderr or "")).strip()
    except Exception as exc:
        return f"UNAVAILABLE: {exc}"


def afni_labels(path):
    if shutil.which("3dinfo") is None:
        raise RuntimeError("AFNI 3dinfo is not available")
    p = subprocess.run(
        ["3dinfo", "-label", str(path)], capture_output=True, text=True
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    labels = [x.strip() for x in p.stdout.strip().split("|") if x.strip()]
    if not labels:
        raise RuntimeError(f"No AFNI sub-brick labels found: {path}")
    return labels


def parse_rb(labels):
    red, blue = {}, {}
    for idx, label in enumerate(labels):
        match = RB_RE.fullmatch(label)
        if match is None:
            continue
        target = red if match.group(1) == "RedFace" else blue
        identity = int(match.group(2))
        if identity in target:
            raise RuntimeError(f"Duplicate condition label: {label}")
        target[identity] = idx
    missing = [
        int(i) for i in IDENTITIES
        if int(i) not in red or int(i) not in blue
    ]
    if missing:
        raise RuntimeError(f"Missing Red/Blue identities: {missing}")
    return red, blue


def volume3d(img, index):
    return np.asarray(img.dataobj[..., int(index)], dtype=np.float32).squeeze()


def input_fingerprint(path):
    path = Path(path).resolve()
    st = path.stat()
    return {
        "path": str(path),
        "size_bytes": int(st.st_size),
        "mtime_ns": int(st.st_mtime_ns),
    }


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while True:
            block = f.read(8 * 1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def preflight_subject(subject, shape, affine):
    path = Path(RBCUE_TEMPLATE.format(subj=subject)).resolve()
    if not path.exists():
        raise FileNotFoundError(path)
    img = nib.load(str(path))
    if img.shape[:3] != tuple(shape):
        raise RuntimeError(f"{subject}: rbCue shape mismatch")
    if not np.allclose(img.affine, affine, atol=1e-5):
        raise RuntimeError(f"{subject}: rbCue affine mismatch")
    labels = afni_labels(path)
    if len(labels) != img.shape[-1]:
        raise RuntimeError(f"{subject}: label/sub-brick count mismatch")
    red, blue = parse_rb(labels)
    return {
        "subject": subject,
        "file": input_fingerprint(path),
        "shape": [int(x) for x in img.shape],
        "red_subbricks": {str(i): int(red[i]) for i in red},
        "blue_subbricks": {str(i): int(blue[i]) for i in blue},
    }


def load_subject(subject, mask_bool):
    path = Path(RBCUE_TEMPLATE.format(subj=subject)).resolve()
    img = nib.load(str(path))
    labels = afni_labels(path)
    red_idx, blue_idx = parse_rb(labels)
    red = np.stack([
        volume3d(img, red_idx[int(i)])[mask_bool] for i in IDENTITIES
    ]).astype(np.float32)
    blue = np.stack([
        volume3d(img, blue_idx[int(i)])[mask_bool] for i in IDENTITIES
    ]).astype(np.float32)
    return np.stack([red, blue], axis=0), img.shape[:3], img.affine


# ============================================================================
# 6. SEARCHLIGHT GEOMETRY
# ============================================================================

def sphere_offsets(radius):
    out = []
    radius = int(radius)
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if dx * dx + dy * dy + dz * dz <= radius * radius:
                    out.append((dx, dy, dz))
    return np.asarray(out, dtype=np.int64)


def build_spheres(mask_bool):
    coords = np.argwhere(mask_bool)
    flat = -np.ones(mask_bool.shape, dtype=np.int32)
    flat[mask_bool] = np.arange(mask_bool.sum(), dtype=np.int32)
    offsets = sphere_offsets(SEARCHLIGHT_RADIUS_VOX)
    shape = np.asarray(mask_bool.shape, dtype=np.int64)
    centers, spheres, sizes = [], [], []
    for center in coords:
        points = center[None, :] + offsets
        good = np.all((points >= 0) & (points < shape[None, :]), axis=1)
        points = points[good]
        points = points[mask_bool[points[:, 0], points[:, 1], points[:, 2]]]
        inds = flat[points[:, 0], points[:, 1], points[:, 2]]
        inds = inds[inds >= 0]
        if len(inds) >= MIN_SPHERE_VOXELS:
            centers.append(center.copy())
            spheres.append(inds.astype(np.int32))
            sizes.append(len(inds))
    return (
        np.asarray(centers, dtype=np.int32),
        spheres,
        np.asarray(sizes, dtype=np.int16),
    )


# ============================================================================
# 7. ONE SEARCHLIGHT
# ============================================================================

def preprocess_fold(patterns, vox, train_rows, test_rows):
    """All voxel selection and scaling are determined from training identities."""
    local = np.asarray(patterns[:, :, vox], dtype=np.float64)
    train_stack = np.vstack([
        local[0, train_rows, :],
        local[1, train_rows, :],
    ])
    finite = np.all(np.isfinite(train_stack), axis=0)
    if finite.sum() < MIN_SPHERE_VOXELS:
        return None
    sd0 = np.std(train_stack[:, finite], axis=0, ddof=1)
    keep_local = np.isfinite(sd0) & (sd0 > VOXEL_SD_MIN)
    keep = np.zeros(local.shape[-1], dtype=bool)
    keep[np.where(finite)[0][keep_local]] = True
    if keep.sum() < MIN_SPHERE_VOXELS:
        return None
    if not np.all(np.isfinite(local[:, test_rows, :][:, :, keep])):
        return None

    mu = np.mean(train_stack[:, keep], axis=0)
    sd = np.std(train_stack[:, keep], axis=0, ddof=1)
    z = (local[:, :, keep] - mu[None, None, :]) / sd[None, None, :]

    # Context-specific TRAIN-only RMS normalization removes a nuisance global
    # amplitude difference without using held-out identities.
    for context in (0, 1):
        context_mu = np.mean(z[context, train_rows, :], axis=0)
        z[context] -= context_mu[None, :]
        rms = float(np.sqrt(np.mean(z[context, train_rows, :] ** 2)))
        if not np.isfinite(rms) or rms <= CONTEXT_RMS_MIN:
            return None
        z[context] /= rms
    return z


def neural_pair_distances(z, spec):
    context = spec[:, 0].astype(np.int64)
    i = spec[:, 1].astype(np.int64)
    j = spec[:, 2].astype(np.int64)
    diff = z[context, i, :] - z[context, j, :]
    # Mean squared Euclidean dissimilarity; division by voxel count makes MSE
    # comparable across edge spheres with slightly different retained nvox.
    return np.mean(diff * diff, axis=1)


def squared_error_sum(y, pred, mask=None):
    if mask is None:
        err = y - pred
    else:
        if int(np.sum(mask)) == 0:
            return 0.0, 0
        err = y[mask] - pred[mask]
    return float(np.sum(err * err)), int(err.size)


def evaluate_sphere(patterns, vox):
    overall_sse = np.zeros(4, dtype=np.float64)
    task_sse = np.zeros(4, dtype=np.float64)
    congr_sse = np.zeros(4, dtype=np.float64)
    overall_n = task_n = congr_n = 0
    theory_parameter_sum = np.zeros(5, dtype=np.float64)
    train_mse_sum = np.zeros(4, dtype=np.float64)
    nvalid = 0

    for fold in PAIR_FOLDS:
        z = preprocess_fold(
            patterns, vox, fold["train_rows"], fold["test_rows"]
        )
        if z is None:
            continue
        y_train = neural_pair_distances(z, fold["train_pairs"])
        y_test = neural_pair_distances(z, fold["test_pairs"])
        if not np.all(np.isfinite(y_train)) or not np.all(np.isfinite(y_test)):
            continue

        predictions, betas, train_mse = fit_four_models(
            fold["train_pairs"], fold["test_pairs"],
            fold["train_designs"], fold["test_designs"], y_train
        )
        if not all(np.all(np.isfinite(p)) for p in predictions):
            continue

        fold_overall_n = len(y_test)
        fold_task_n = int(np.sum(fold["test_task_mask"]))
        fold_congr_n = int(np.sum(fold["test_congruency_mask"]))
        for model_i, pred in enumerate(predictions):
            sse, _ = squared_error_sum(y_test, pred)
            overall_sse[model_i] += sse
            sse, _ = squared_error_sum(y_test, pred, fold["test_task_mask"])
            task_sse[model_i] += sse
            sse, _ = squared_error_sum(
                y_test, pred, fold["test_congruency_mask"]
            )
            congr_sse[model_i] += sse

        # Theory order: Red intercept, Blue intercept, scale, normalized task
        # strength, normalized congruency strength.
        theory_parameter_sum += betas[1]
        train_mse_sum += np.asarray(train_mse, dtype=np.float64)
        overall_n += fold_overall_n
        task_n += fold_task_n
        congr_n += fold_congr_n
        nvalid += 1

    if nvalid != EXPECTED_VALID_FOLDS:
        return None, nvalid
    if overall_n == 0 or task_n == 0 or congr_n == 0:
        return None, nvalid

    overall = overall_sse / overall_n
    task = task_sse / task_n
    congr = congr_sse / congr_n
    pars = theory_parameter_sum / nvalid
    scale, task_strength, congruency_strength = pars[2], pars[3], pars[4]
    coef = np.asarray([
        scale,
        scale * task_strength,
        scale * congruency_strength,
        task_strength,
        congruency_strength,
    ])
    train_qc = train_mse_sum / nvalid
    theory = overall[1]

    values = np.concatenate([
        overall,
        np.asarray([
            overall[0] - theory,
            overall[2] - theory,
            overall[3] - theory,
        ]),
        task,
        congr,
        coef,
        train_qc,
    ]).astype(np.float32)
    if len(values) != len(MAP_NAMES):
        raise RuntimeError("Internal map ordering error")
    return values, nvalid


# ============================================================================
# 8. PARALLEL SUBJECT ANALYSIS AND OUTPUT
# ============================================================================

_WORK_PATTERNS = None
_WORK_SPHERES = None


def worker_init(patterns, spheres):
    global _WORK_PATTERNS, _WORK_SPHERES
    _WORK_PATTERNS = patterns
    _WORK_SPHERES = spheres


def worker_chunk(bounds):
    start, stop = bounds
    out = []
    for center_i in range(start, stop):
        values, nvalid = evaluate_sphere(
            _WORK_PATTERNS, _WORK_SPHERES[center_i]
        )
        out.append((center_i, values, nvalid))
    return out


def save_nifti(path, data, affine, dtype=np.float32):
    path = Path(path)
    if path.exists():
        raise FileExistsError(path)
    nib.save(
        nib.Nifti1Image(np.asarray(data, dtype=dtype), affine),
        str(path),
    )


def save_subject_maps(workdir, results, valid_folds, centers, sizes, shape, affine):
    workdir.mkdir(parents=True, exist_ok=False)
    for map_i, name in enumerate(MAP_NAMES):
        volume = np.full(shape, np.nan, dtype=np.float32)
        volume[centers[:, 0], centers[:, 1], centers[:, 2]] = results[:, map_i]
        save_nifti(workdir / f"{name}.nii.gz", volume, affine)

    fold_volume = np.zeros(shape, dtype=np.int16)
    fold_volume[centers[:, 0], centers[:, 1], centers[:, 2]] = valid_folds
    save_nifti(workdir / "valid_fold_count.nii.gz", fold_volume, affine, np.int16)

    size_volume = np.zeros(shape, dtype=np.int16)
    size_volume[centers[:, 0], centers[:, 1], centers[:, 2]] = sizes
    save_nifti(workdir / "sphere_nvoxels.nii.gz", size_volume, affine, np.int16)

    valid = valid_folds == EXPECTED_VALID_FOLDS
    qc = {
        "expected_valid_folds": EXPECTED_VALID_FOLDS,
        "total_searchlight_centers": int(len(centers)),
        "complete_centers": int(valid.sum()),
        "incomplete_centers": int((~valid).sum()),
        "maps": MAP_NAMES,
    }
    (workdir / "subject_qc.json").write_text(
        json.dumps(qc, indent=2), encoding="utf-8"
    )


def subject_complete(subject, signature):
    marker = OUTPUT_DIR / "subjects" / subject / "SUBJECT_COMPLETE.json"
    if not marker.exists():
        return False
    info = json.loads(marker.read_text(encoding="utf-8"))
    return info.get("analysis_signature") == signature


def run_subject(subject, mask_bool, centers, spheres, sizes, shape, affine, signature):
    final_dir = OUTPUT_DIR / "subjects" / subject
    if subject_complete(subject, signature):
        print(f"{subject}: verified completion marker found; skipping", flush=True)
        return
    if final_dir.exists():
        raise RuntimeError(
            f"Existing incomplete/mismatched subject directory: {final_dir}. "
            "Move it aside before rerunning."
        )

    tmp_dir = OUTPUT_DIR / "subjects" / f".{subject}.working"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)

    patterns, subject_shape, subject_affine = load_subject(subject, mask_bool)
    if subject_shape != tuple(shape) or not np.allclose(subject_affine, affine, atol=1e-5):
        raise RuntimeError(f"{subject}: input grid changed after preflight")

    results = np.full((len(centers), len(MAP_NAMES)), np.nan, dtype=np.float32)
    valid_folds = np.zeros(len(centers), dtype=np.int16)
    chunks = [
        (start, min(start + CENTER_CHUNK, len(centers)))
        for start in range(0, len(centers), CENTER_CHUNK)
    ]

    with ProcessPoolExecutor(
        max_workers=N_JOBS,
        initializer=worker_init,
        initargs=(patterns, spheres),
    ) as executor:
        futures = [executor.submit(worker_chunk, chunk) for chunk in chunks]
        for done, future in enumerate(as_completed(futures), start=1):
            for center_i, values, nvalid in future.result():
                valid_folds[center_i] = nvalid
                if values is not None:
                    results[center_i] = values
            if done == 1 or done % 25 == 0 or done == len(futures):
                print(
                    f"{subject}: chunks {done}/{len(futures)} complete",
                    flush=True,
                )

    save_subject_maps(
        tmp_dir, results, valid_folds, centers, sizes, shape, affine
    )
    marker = {
        "subject": subject,
        "analysis_signature": signature,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
    }
    (tmp_dir / "SUBJECT_COMPLETE.json").write_text(
        json.dumps(marker, indent=2), encoding="utf-8"
    )
    tmp_dir.rename(final_dir)
    print(f"{subject}: completed", flush=True)


# ============================================================================
# 9. GROUP GLOBAL MAX-|T| INFERENCE ACROSS THREE CONTRASTS
# ============================================================================

def one_sample_t(X):
    n = X.shape[0]
    mean = np.mean(X, axis=0)
    sd = np.std(X, axis=0, ddof=1)
    out = np.zeros_like(mean)
    good = np.isfinite(sd) & (sd > 0)
    out[good] = mean[good] / (sd[good] / np.sqrt(n))
    out[~good & (mean > 0)] = np.inf
    out[~good & (mean < 0)] = -np.inf
    return mean, out


def load_contrast(subject, name):
    path = OUTPUT_DIR / "subjects" / subject / f"{name}.nii.gz"
    if not path.exists():
        raise FileNotFoundError(path)
    return np.asarray(nib.load(str(path)).dataobj, dtype=np.float32)


def group_inference(mask_bool, shape, affine):
    final_dir = OUTPUT_DIR / "group"
    if final_dir.exists():
        raise RuntimeError(f"Group directory already exists: {final_dir}")
    workdir = OUTPUT_DIR / ".group.working"
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)

    items = []
    for contrast in CONTRAST_NAMES:
        volumes = np.stack([
            load_contrast(subject, contrast) for subject in ALL_SUBJECTS
        ])
        valid = mask_bool.copy()
        valid &= np.all(np.isfinite(volumes), axis=0)
        if int(valid.sum()) == 0:
            raise RuntimeError(f"No group-valid voxels for {contrast}")
        X = np.asarray(volumes[:, valid], dtype=np.float64)
        mean, t_obs = one_sample_t(X)
        items.append({
            "contrast": contrast,
            "valid": valid,
            "X": X,
            "mean": mean,
            "t": t_obs,
        })

    rng = np.random.default_rng(SIGNFLIP_SEED)
    null_max = np.empty(N_SIGNFLIP, dtype=np.float64)
    cursor = 0
    while cursor < N_SIGNFLIP:
        batch_n = min(SIGNFLIP_BATCH, N_SIGNFLIP - cursor)
        signs = rng.choice(
            np.asarray([-1.0, 1.0]),
            size=(batch_n, len(ALL_SUBJECTS)),
            replace=True,
        )
        batch_max = np.zeros(batch_n, dtype=np.float64)
        for item in items:
            X = item["X"]
            n = X.shape[0]
            means = (signs @ X) / n
            sumsq = np.sum(X * X, axis=0)[None, :]
            var = (sumsq - n * means * means) / (n - 1)
            denom = np.sqrt(np.maximum(var, 0.0) / n)
            t = np.divide(
                means,
                denom,
                out=np.zeros_like(means),
                where=denom > 0,
            )
            batch_max = np.maximum(batch_max, np.max(np.abs(t), axis=1))
        null_max[cursor:cursor + batch_n] = batch_max
        cursor += batch_n
        if cursor % 1000 == 0 or cursor == N_SIGNFLIP:
            print(f"Group sign flips: {cursor}/{N_SIGNFLIP}", flush=True)

    rows = []
    for item in items:
        abs_t = np.abs(item["t"])
        # Exact maximum-statistic p values without allocating an enormous
        # N_SIGNFLIP x N_VOXELS boolean array.
        sorted_null = np.sort(null_max)
        exceed = N_SIGNFLIP - np.searchsorted(
            sorted_null, abs_t, side="left"
        )
        p = (1.0 + exceed) / (N_SIGNFLIP + 1.0)

        mean_vol = np.full(shape, np.nan, dtype=np.float32)
        t_vol = np.full(shape, np.nan, dtype=np.float32)
        p_vol = np.full(shape, np.nan, dtype=np.float32)
        mean_vol[item["valid"]] = item["mean"].astype(np.float32)
        t_vol[item["valid"]] = item["t"].astype(np.float32)
        p_vol[item["valid"]] = p.astype(np.float32)
        save_nifti(
            workdir / f"{item['contrast']}_group_mean_delta.nii.gz",
            mean_vol,
            affine,
        )
        save_nifti(
            workdir / f"{item['contrast']}_group_t.nii.gz",
            t_vol,
            affine,
        )
        save_nifti(
            workdir / f"{item['contrast']}_global_maxAbsT_FWER_p.nii.gz",
            p_vol,
            affine,
        )

        sig = p < 0.05
        positive = sig & (item["t"] > 0)
        negative = sig & (item["t"] < 0)
        rows.append({
            "contrast": item["contrast"],
            "valid_voxels": int(item["valid"].sum()),
            "max_t": float(np.nanmax(item["t"])),
            "min_t": float(np.nanmin(item["t"])),
            "max_abs_t": float(np.nanmax(np.abs(item["t"]))),
            "min_global_FWER_p": float(np.nanmin(p)),
            "sig_FWER05_total": int(sig.sum()),
            "sig_FWER05_positive_theory_better": int(positive.sum()),
            "sig_FWER05_negative_competitor_better": int(negative.sum()),
        })

    pd.DataFrame(rows).to_csv(
        workdir / "global_maxAbsT_group_summary.csv", index=False
    )
    np.save(workdir / "global_maxAbsT_null.npy", null_max)
    (workdir / "GROUP_COMPLETE.json").write_text(
        json.dumps(
            {
                "completed_utc": datetime.now(timezone.utc).isoformat(),
                "n_signflip": N_SIGNFLIP,
                "seed": SIGNFLIP_SEED,
                "contrasts": CONTRAST_NAMES,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    workdir.rename(final_dir)


# ============================================================================
# 10. MAIN
# ============================================================================

def canonical_hash(obj):
    payload = json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def software_versions():
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "pandas": pd.__version__,
        "nibabel": nib.__version__,
        "numba": numba.__version__,
        "afni": command_output(["3dinfo", "-ver"]),
    }


def warmup_numba():
    X = np.asarray([[1.0, 0.0, 1.0], [0.0, 1.0, 2.0], [1.0, 0.0, 3.0]])
    y = np.asarray([1.0, 2.0, 3.0])
    fit_active_set_nonnegative(X, y, X, 2, 1)
    spec = np.asarray([
        [0.0, 0.0, 1.0, 1.0, 0.0],
        [0.0, 0.0, 2.0, 0.0, 1.0],
        [1.0, 0.0, 1.0, 1.0, 1.0],
        [1.0, 0.0, 2.0, -1.0, 1.0],
    ])
    fit_theory_positive_definite(spec, spec, np.asarray([1.0, 2.0, 1.5, 2.5]))


def audit_theory_geometry():
    for t, g in ((0.0, 0.0), (0.4, 0.0), (0.3, 0.3), (0.7, 0.5)):
        if t * t + g * g > THEORY_RADIUS_MAX ** 2:
            continue
        for sign in (+1.0, -1.0):
            G = np.asarray([
                [1.0 + sign * t, g],
                [g, 1.0 - sign * t],
            ])
            if np.min(np.linalg.eigvalsh(G)) <= 0.0:
                raise RuntimeError("Theory metric positive-definiteness audit failed")


def main():
    audit_theory_geometry()
    script_path = Path(__file__).resolve()
    mask_path = Path(MASK_PATH).resolve()
    if not mask_path.exists():
        raise FileNotFoundError(mask_path)
    mask_img = nib.load(str(mask_path))
    mask_data = np.squeeze(np.asarray(mask_img.dataobj))
    mask_bool = np.isfinite(mask_data) & (mask_data > 0.5)
    shape = mask_bool.shape
    affine = mask_img.affine

    print("PRE-FLIGHT: validating single-dimensional-task inputs", flush=True)
    preflight = {}
    for i, subject in enumerate(SUBJECTS, start=1):
        preflight[subject] = preflight_subject(subject, shape, affine)
        print(f"  {subject}: OK ({i}/{len(SUBJECTS)})", flush=True)

    centers, spheres, sizes = build_spheres(mask_bool)
    print(f"Mask voxels: {int(mask_bool.sum())}", flush=True)
    print(f"Valid searchlight centers: {len(centers)}", flush=True)
    print(f"Radius: {SEARCHLIGHT_RADIUS_VOX} voxels (not mm)", flush=True)
    print("Red=morality; Blue=competence", flush=True)
    print("Only the single-dimensional-task 32 conditions are loaded", flush=True)

    signature_payload = {
        "run_mode": RUN_MODE,
        "subjects": SUBJECTS,
        "script_sha256": sha256_file(script_path),
        "mask": input_fingerprint(mask_path),
        "inputs": {s: preflight[s]["file"] for s in SUBJECTS},
        "radius_vox": SEARCHLIGHT_RADIUS_VOX,
        "minimum_sphere_voxels": MIN_SPHERE_VOXELS,
        "cv_splits": serialize_splits(),
        "models": MODEL_NAMES,
        "contrasts": CONTRAST_NAMES,
        "theory_positive_definite": {
            "radius_max": THEORY_RADIUS_MAX,
            "grid_points": THEORY_GRID_POINTS,
            "refinement_levels": THEORY_REFINEMENT_LEVELS,
        },
        "distance": "mean squared Euclidean dissimilarity after train-only scaling",
        "group_n_signflip": N_SIGNFLIP,
        "group_seed": SIGNFLIP_SEED,
    }
    signature = canonical_hash(signature_payload)

    metadata = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "argv": sys.argv,
        "cwd": os.getcwd(),
        "run_mode": RUN_MODE,
        "subjects": SUBJECTS,
        "analysis_signature": signature,
        "analysis_signature_payload": signature_payload,
        "coordinate_mapping": {
            "x": "morality",
            "y": "competence",
            "Red": "morality context",
            "Blue": "competence context",
        },
        "data_scope": "32 single-dimensional-task conditions only; no mixed-task data",
        "held_out_unit": "identity",
        "test_pairs": "pairs formed entirely by held-out identities",
        "primary_score": "held-out pairwise CV-MSE across all within-context pairs",
        "secondary_subsets": {
            "task_pairs": "exactly one of dx,dy is zero",
            "congruency_pairs": (
                "both dx and dy are non-zero; spans the nine matched "
                "(|dx|,|dy|) direction families"
            ),
        },
        "models": MODEL_NAMES,
        "contrasts": CONTRAST_NAMES,
        "theory_metric": {
            "Red": "[[1+t,g],[g,1-t]]",
            "Blue": "[[1-t,g],[g,1+t]]",
            "constraints": (
                "t>=0; g>=0; t^2+g^2<=radius_max^2; radius_max<1"
            ),
            "radius_max": THEORY_RADIUS_MAX,
            "guarantee": "both context metrics are positive definite",
        },
        "training_maps": (
            "descriptive optimization QC only; excluded from group inference"
        ),
        "contrast_sign": "comparator MSE minus theory MSE; positive favors theory",
        "group_inference": {
            "two_sided": True,
            "statistic": "global max absolute one-sample t",
            "multiplicity": "whole-brain space plus all three prespecified contrasts",
            "n_signflip": N_SIGNFLIP,
            "seed": SIGNFLIP_SEED,
        },
        "software": software_versions(),
    }

    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    if OUTPUT_DIR.exists():
        meta_path = OUTPUT_DIR / "run_metadata.json"
        if not meta_path.exists():
            raise RuntimeError(f"Unsafe existing output directory: {OUTPUT_DIR}")
        old = json.loads(meta_path.read_text(encoding="utf-8"))
        if old.get("analysis_signature") != signature:
            raise RuntimeError(
                "Existing output has a different analysis signature. "
                "Move it aside or use a new output path."
            )
        print(f"Resuming matching run: {OUTPUT_DIR}", flush=True)
    else:
        OUTPUT_DIR.mkdir()
        (OUTPUT_DIR / "subjects").mkdir()
        (OUTPUT_DIR / "run_metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        save_nifti(
            OUTPUT_DIR / "analysis_mask.nii.gz",
            mask_bool.astype(np.uint8),
            affine,
            np.uint8,
        )

    warmup_numba()
    for i, subject in enumerate(SUBJECTS, start=1):
        print(f"===== {subject} ({i}/{len(SUBJECTS)}) =====", flush=True)
        run_subject(
            subject, mask_bool, centers, spheres, sizes, shape, affine, signature
        )

    if RUN_GROUP_INFERENCE:
        for subject in ALL_SUBJECTS:
            if not subject_complete(subject, signature):
                raise RuntimeError(f"Cannot start group inference: {subject} incomplete")
        group_inference(mask_bool, shape, affine)

    print("DONE", flush=True)
    print(f"Output: {OUTPUT_DIR}", flush=True)
    print(
        "Positive contrast = theory has lower held-out CV-MSE; "
        "negative contrast = comparator has lower held-out CV-MSE.",
        flush=True,
    )


if __name__ == "__main__":
    main()
