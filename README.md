# Flexible Decision Code and Data

This repository contains the analysis code and summary data needed to reproduce the main computational, behavioral, and fMRI analyses for the flexible decision-making manuscript.

The package was assembled from two local project sources:

- Primary source: `01-related-code`
- Supplementary source: `neuroimage-related-code/04-related-code`

Files related to the separate SR3 project were excluded.

## Directory Overview

```text
open_source_flexible_decision_code/
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
`-- docs/                       # Notes copied from the original server analysis folder
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

## Notes Before Running

Many scripts were originally written for local/server paths such as `/home/medicaldata...`, `/home/image030...`, or `E:/...`. Before running the analyses, update these paths to match your local data layout.

This repository includes analysis scripts and derived/summary tables. It does not include raw fMRI images or original raw behavioral `.mat` files.

## Excluded Content

Files and folders related to the separate SR3 project were excluded from this open-source package. Generated R session files such as `.Rhistory` and `.RData`, generic PPI tutorial/reference folders, and most pre-rendered figure outputs were also excluded.

## Suggested Citation

If you use this code, please cite the associated flexible decision-making manuscript.
