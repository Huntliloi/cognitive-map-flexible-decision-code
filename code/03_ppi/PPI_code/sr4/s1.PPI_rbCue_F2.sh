#!/bin/tcsh

# note location of scripts and data
set basedir = /home/medicaldata/LJData/SR_ana/analysis_res/glm_raw/rbCue.glm1.result
set scriptdir = /home/image030/analysis_code/PPI_scripts/sr4

# the user may specify a single subject to run with
if ( $#argv > 0 ) then
    set subj = $argv[1]
else
    set subj = sub_001
endif


set subjdir   = $basedir/"$subj"
set maskdir = /home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI
set glm1_rpath = /home/medicaldata/LJData/SR_ana/analysis_res/glm_raw/rbCue.glm1.result

# ----------------------------------------
# do all of the work in the $subj.results directory...
cd $subjdir


# ----------------------------------------
# generate seed time series, ppi.seed.1D
# start with primary visual cortex V1
set seed = HCl

# echo -28 -96 -6 | 3dUndump -xyz -srad 5 -master stats."$subj"_REML+tlrc -prefix mask.$seed.nii.gz -
# generate ppi.seed.1D (note that mask dset is unneeded, but visually useful)
# 得到种子区的时间序列  REML
3dmaskave -quiet -mask $maskdir/$seed.nii errts."$subj"_REML+tlrc > ppi.seed.$seed.1D


# ===========================================================================
# generate PPI regressors from seed and timing files
# (script uses 'set seed = ppi.seed.1D')

tcsh $scriptdir/cmd.ppi.2.make.regs.rbCue_F2 $subj $seed

# and copy the results into the stimuli directory
cp work.$seed/p6.* ppi.seed.$seed.1D stimuli

# and just to see consider:
#    1dplot -one ppi.seed.1D work.v1/p7.v1.sum.PPI.1D
#    1dplot ppi.seed.1D work.v1/p6.*


# ===========================================================================
# create and run a 3dDeconvolve command for the PPI
# (still run from $subjdir)

# create the 3dDeconvolve command, proc.3dd.ppi.post.full
#tcsh $scriptdir/cmd.ppi.3.ap.post

# and run it
tcsh $scriptdir/proc.3dd.ppi.post.full.rbCue_F2 $subj $seed $glm1_rpath



# ===========================================================================
# comments...

# - this data is not designed to capture a PPI effect
# - the results are in PPI.full.stats.FT+tlrc