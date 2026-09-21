# Flexible Decision Code and Data

This repository contains the analysis code and summary data needed to reproduce the main computational, behavioral, and fMRI analyses, together with the additional analyses completed during manuscript revision.

The package was assembled from two local project sources:

- Primary source: `01-related-code`
- Supplementary source: `neuroimage-related-code/04-related-code`

Reviewer-response scripts and results are collected in `revision_analyses/`.

Files related to the separate SR3 project were excluded.

## Directory Overview

```text
cognitive-map-flexible-decision-code/
|-- code/
|   |-- 01_glm/                 # AFNI first-level GLM scripts and timing files
|   |-- 02_bms/                 # Bayesian model selection GLM scripts and timing files
|   |-- 03_ppi/                 # PPI scripts for SR4 rbCue/wCue analyses
|   |-- 04_rsa/                 # RSA timing, AFNI scripts, and Python RSA utilities
|   |-- 05_searchlight/         # Searchlight RSA scripts
|   `-- 06_rnn_warping/         # RNN/warping simulation code, images, and notebooks
|-- data/
|   |-- behavior/               # Behavioral summary tables
|   |-- bms/                    # BMS raw and summarized tables
|   |-- timecourse/             # ROI time-course summary tables
|   `-- rsa_fig/                # RSA/RDM data and MATLAB/Python plotting scripts
|-- figures_and_statistics/     # R Markdown scripts for statistical analyses and plotting
|-- revision_analyses/          # Reviewer-response and revised statistical analyses
|-- docs/                       # Notes copied from the original server analysis folder
|-- LICENSE
`-- README.md
```

## Main Analysis Components

### Behavioral and Statistical Figures

Use:

- `figures_and_statistics/04-staticsPlot.Rmd`
- `figures_and_statistics/staticsPlot_revise.Rmd`

Relevant data:

- `data/behavior/subSR4rbCue.csv`
- `data/behavior/subSR4wCue.csv`
- `data/behavior/learn_block_ACC.csv`
- `data/behavior/learn_block_RT.csv`
- `data/behavior/learn_face_speed.csv`
- `data/behavior/learn_face_RT.csv`
- `data/behavior/face_placement.csv`
- `data/behavior/SR4seq.xlsx`

These files support the behavioral analyses, learning-stage analyses, and related manuscript figures.

### GLM Analyses

Use:

- `code/01_glm/`

This folder contains original and derived timing files plus single-subject AFNI scripts for the rbCue and wCue GLM analyses. The `neuroimage_supplement/` subfolder contains additional GLM timing and script files from the curated NeuroImage-related code folder.

### Bayesian Model Selection

Use:

- `code/02_bms/`
- `data/bms/`

The `code/02_bms/` folder contains scripts and timing files used to estimate model-specific residuals. The `data/bms/RAW/` folder contains the model-wise residual/variance tables used by the R Markdown scripts for BMS statistics and plots.

### PPI Analyses

Use:

- `code/03_ppi/`
- `code/01_glm/neuroimage_supplement/02-stimulus_glm/rbCue.ppi/`
- `code/01_glm/neuroimage_supplement/02-stimulus_glm/wCue.ppi/`

The PPI folder contains the SR4 rbCue/wCue scripts. Generic PPI tutorial/reference folders and SR3 scripts were intentionally excluded.

### RSA and Fig. 4/5 Analyses

Use:

- `code/04_rsa/`
- `data/rsa_fig/`

Important scripts include:

- `code/04_rsa/04-RSA_python/SR4_RSA_rbCue.py`
- `code/04_rsa/04-RSA_python/SR4_RSA_wCue.py`
- `code/04_rsa/04-RSA_python/SR4_RSA_wCue_biggest.py`
- `code/04_rsa/04-RSA_python/SR4_warping_rbCue.py`
- `data/rsa_fig/rbCue_getRDM.py`
- `data/rsa_fig/wCue_getRDM.py`
- `data/rsa_fig/rbCue_RSA.m`
- `data/rsa_fig/wCue_RSA.m`
- `data/rsa_fig/grid_RSA.m`

The `data/rsa_fig/` folder also includes `.mat` RDM/result files used for the RSA figure panels.

### Searchlight RSA

Use:

- `code/05_searchlight/SR4_rbCue_searchlight.py`
- `code/05_searchlight/SR4_wCue_searchlight.py`

Additional historical or exploratory searchlight scripts are under `code/05_searchlight/neuroimage_supplement/`.

### RNN / Warping Simulations

Use:

- `code/06_rnn_warping/`

The main entry point is:

```bash
./run_all_experiments.sh
```

See `code/06_rnn_warping/README.md` and `code/06_rnn_warping/requirements.txt` for model-specific setup instructions.

### Revision Analyses

Use:

- `revision_analyses/logstic_test/`
- `revision_analyses/reviewer3/`
- `revision_analyses/reviewer4/`
- `revision_analyses/reviewer5/`
- `revision_analyses/section3_6_two_family_correction_backup/`

This directory contains the core scripts and compact result tables added during manuscript revision. Generated figures, duplicate workbooks, run metadata, superseded notebooks, and large row-level permutation null distributions are excluded.

| Directory | Analysis | Retained results |
| --- | --- | --- |
| `logstic_test/` | Binomial-logit mixed-effects reanalysis of the Fig. 2 choice data. | Figure coefficients, all fixed effects, and model diagnostics. |
| `reviewer3/` | Searchlight comparison of fixed 2-D, joint-warping, context-weighting, and quadratic representational models. | Global maximum-statistic group summary. |
| `reviewer4/` | AFNI single-trial rbCue model and simulation validation of neural-warping estimators. | Fixed-null thresholds, structured-null results, and recovery summaries. |
| `reviewer5/rnn_model/` | Seed-preserving RNN reanalysis. | Checkpoint statistics, corrected onsets, training changes, and regression results. |
| `reviewer5/brain_behavior_warping_fig5/` | Participant-label permutation analysis of representational-warping brain-behavior correlations. | Subject-level behavioral indices, corrected results, and reproduction checks. |
| `reviewer5/brain_behavior_correlations_fig7/` | Joint correction of representational-warping and time-resolved ROI-coding correlations. | Complete and Fig. 7 results, candidate mappings, and behavioral coefficients. |
| `section3_6_two_family_correction_backup/` | Two-family synchronized sign-flip maximum-statistic correction for Section 3.6. | Family tables, key results, and the data-integrity check. |

The revision analyses use Python 3.10 or later with `numpy`, `pandas`, `scipy`, `matplotlib`, `patsy`, `statsmodels`, `openpyxl`, `nibabel`, and `numba`. `rsatoolbox` is optional for the Reviewer 4 parity check. The AFNI script requires AFNI and `tcsh` on a Unix-like system.

Examples, run from the repository root:

```bash
# Fig. 2 choice GLMM
python revision_analyses/logstic_test/Fig2_choice_GLMM_analysis.py \
  --input data/behavior/SR4seq.xlsx \
  --outdir revision_analyses/logstic_test

# Reviewer 4 estimator validation
python revision_analyses/reviewer4/reviewer4_rbCue_warping_validation_v6.py \
  --mode FORMAL --strict-rsatoolbox-parity \
  --output reviewer4_validation_results

# Reviewer 3 searchlight model comparison (after editing its configuration block)
python revision_analyses/reviewer3/reviewer3_joint_warping_rdm_model_comparison.py

# Section 3.6 two-family correction
python revision_analyses/section3_6_two_family_correction_backup/section3_6_two_family_maxstat.py \
  --input-dir data/timecourse \
  --output-dir section3_6_correction_results \
  --n-perm 100000 --seed 20260919
```

The Reviewer 3 script requires subject-level rbCue beta-series images and an analysis mask; configure its NIfTI template, mask, output directory, and `RUN_MODE` before use. Start with `TEST001` and use `FORMAL` only after validating the test output.

The Reviewer 5 brain-behavior scripts require a subject-level neural-warping table in addition to the public behavioral and time-course tables. Large null distributions are regenerated from the documented seeds and iteration counts rather than stored in the repository.

```bash
# Fig. 5 representational-warping correlations
python revision_analyses/reviewer5/brain_behavior_warping_fig5/reviewer5_warping_brain_behavior_maxstat_v1.py \
  --neural /path/to/warping_mas_BN.csv \
  --rbcue /path/to/liu_rbCue.csv \
  --wcue /path/to/liu_wCue.csv \
  --output-dir reviewer5_warping_results \
  --behavior-resamples 1000 --permutations 100000

# Joint Fig. 5/Fig. 7 correlation family
python revision_analyses/reviewer5/brain_behavior_correlations_fig7/reviewer5_complete_brain_behavior_maxstat_v1.py \
  --warping-neural /path/to/warping_mas_BN.csv \
  --warping-behavior revision_analyses/reviewer5/brain_behavior_warping_fig5/behavioral_warping_subjects.csv \
  --rbcue-neural data/timecourse/rbCue.subBeta.csv \
  --wcue-neural data/timecourse/wCue.subBeta.csv \
  --rbcue-trials data/behavior/subSR4rbCue.csv \
  --wcue-trials data/behavior/subSR4wCue.csv \
  --output-dir reviewer5_complete_results --permutations 100000
```

Result tables use `p_permutation`, `p_fwe_max`, `p_fwe_global`, or `P_FWER` for permutation-based probabilities. The Section 3.6 integrity table records duplicated trajectories in the supplied mixed-dimensional export; interpret that family only after checking the source export.

## Notes Before Running

Many scripts were originally written for local/server paths such as `/home/medicaldata...`, `/home/image030...`, or `E:/...`. Before running the analyses, update these paths to match your local data layout. This applies particularly to the Reviewer 3 searchlight script and Reviewer 4 AFNI preprocessing script.

This repository includes analysis scripts and derived/summary tables. It does not include raw fMRI images or original raw behavioral `.mat` files.

## Excluded Content

Files and folders related to the separate SR3 project were excluded from this open-source package. Generated R session files such as `.Rhistory` and `.RData`, generic PPI tutorial/reference folders, most pre-rendered figure outputs, duplicate revision workbooks, and large intermediate null-distribution tables were also excluded.

## Suggested Citation

If you use this code, please cite the associated flexible decision-making manuscript.
