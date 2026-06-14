#!/bin/tcsh -xef

# the user may specify a single subject to run with
if ( $#argv > 0 ) then
    set subj = $argv[1]
else
    set subj = sub_001
endif

# set glm1_rpath = /home/image030/analysis_res/rbCue.glm1.result/${subj}
set glm1_rpath = /home/medicaldata3/LJData/rsa/rbCue.rsa.result/${subj}
if ( ! -d $glm1_rpath ) then
    echo "This subject ${subj}'s glm1 result is not exsit, please do glm1 process first!"
    exit
endif

# assign output directory name
# set output_dir = /home/image030/analysis_res/rbCue.rsa.result/$subj
set output_dir = /home/medicaldata3/LJData/rsa/rbCue.rsa_direction.du.result/$subj
# verify that the results directory does not yet exist
if ( -d $output_dir ) then
    echo output dir "$subj.results" already exists
    exit
endif

# set list of runs#
# set runs = (`count -digits 2 1 6`)

# create results and stimuli directories
mkdir -p $output_dir
mkdir -p $output_dir/stimuli

cd $output_dir

# copy stim files into stimulus directory
cp /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.18.43.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.26.57.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.33.69.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.45.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.56.31.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.63.43.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.108.43.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.116.57.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.123.69.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.135.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.146.31.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.153.43.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.161.57.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.198.43.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.206.57.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.213.69.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.225.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.236.31.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.243.43.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.251.57.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.288.43.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.296.57.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.303.69.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.315.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.326.31.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.333.43.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction.du/rbcue.dire.times.341.57.txt \
   $output_dir/stimuli

# ------------------------------
# run the regression analysis
3dDeconvolve -input $glm1_rpath/pb03.$subj.r*.scale+tlrc.HEAD                            \
    -censor $glm1_rpath/motion_${subj}_censor.1D                                         \
    -ortvec $glm1_rpath/mot_demean.r01.1D mot_demean_r01                                 \
    -ortvec $glm1_rpath/mot_demean.r02.1D mot_demean_r02                                 \
    -ortvec $glm1_rpath/mot_demean.r03.1D mot_demean_r03                                 \
    -ortvec $glm1_rpath/mot_demean.r04.1D mot_demean_r04                                 \
    -ortvec $glm1_rpath/mot_demean.r05.1D mot_demean_r05                                 \
    -ortvec $glm1_rpath/mot_demean.r06.1D mot_demean_r06                                 \
    -polort 3 -float                                                         \
    -num_stimts 27                                                           \
    -stim_times 1 stimuli/rbcue.dire.times.18.43.txt 'BLOCK(2,1)'             \
    -stim_label 1 18.43                                                  \
    -stim_times 2 stimuli/rbcue.dire.times.26.57.txt 'BLOCK(2,1)'            \
    -stim_label 2 26.57                                                 \
    -stim_times 3 stimuli/rbcue.dire.times.33.69.txt 'BLOCK(2,1)'            \
    -stim_label 3 33.69                                                 \
    -stim_times 4 stimuli/rbcue.dire.times.45.txt 'BLOCK(2,1)'            \
    -stim_label 4 45                                                 \
    -stim_times 5 stimuli/rbcue.dire.times.56.31.txt 'BLOCK(2,1)'            \
    -stim_label 5 56.31                                                 \
    -stim_times 6 stimuli/rbcue.dire.times.63.43.txt 'BLOCK(2,1)'            \
    -stim_label 6 63.43                                                 \
    -stim_times 7 stimuli/rbcue.dire.times.108.43.txt 'BLOCK(2,1)'            \
    -stim_label 7 108.43                                                 \
    -stim_times 8 stimuli/rbcue.dire.times.116.57.txt 'BLOCK(2,1)'            \
    -stim_label 8 116.57                                                 \
    -stim_times 9 stimuli/rbcue.dire.times.123.69.txt 'BLOCK(2,1)'            \
    -stim_label 9 123.69                                                 \
    -stim_times 10 stimuli/rbcue.dire.times.135.txt 'BLOCK(2,1)'          \
    -stim_label 10 135                                               \
    -stim_times 11 stimuli/rbcue.dire.times.146.31.txt 'BLOCK(2,1)'          \
    -stim_label 11 146.31                                               \
    -stim_times 12 stimuli/rbcue.dire.times.153.43.txt 'BLOCK(2,1)'            \
    -stim_label 12 153.43                                                 \
    -stim_times 13 stimuli/rbcue.dire.times.161.57.txt 'BLOCK(2,1)'          \
    -stim_label 13 161.57                                               \
    -stim_times 14 stimuli/rbcue.dire.times.198.43.txt 'BLOCK(2,1)'          \
    -stim_label 14 198.43                                               \
    -stim_times 15 stimuli/rbcue.dire.times.206.57.txt 'BLOCK(2,1)'          \
    -stim_label 15 206.57                                               \
    -stim_times 16 stimuli/rbcue.dire.times.213.69.txt 'BLOCK(2,1)'          \
    -stim_label 16 213.69                                               \
    -stim_times 17 stimuli/rbcue.dire.times.225.txt 'BLOCK(2,1)'          \
    -stim_label 17 225                                               \
    -stim_times 18 stimuli/rbcue.dire.times.236.31.txt 'BLOCK(2,1)'           \
    -stim_label 18 236.31                                                \
    -stim_times 19 stimuli/rbcue.dire.times.243.43.txt 'BLOCK(2,1)'           \
    -stim_label 19 243.43                                                \
    -stim_times 20 stimuli/rbcue.dire.times.251.57.txt 'BLOCK(2,1)'           \
    -stim_label 20 251.57                                                \
    -stim_times 21 stimuli/rbcue.dire.times.288.43.txt 'BLOCK(2,1)'           \
    -stim_label 21 288.43                                                \
    -stim_times 22 stimuli/rbcue.dire.times.296.57.txt 'BLOCK(2,1)'           \
    -stim_label 22 296.57                                                \
    -stim_times 23 stimuli/rbcue.dire.times.303.69.txt 'BLOCK(2,1)'            \
    -stim_label 23 303.69                                                 \
    -stim_times 24 stimuli/rbcue.dire.times.315.txt 'BLOCK(2,1)'           \
    -stim_label 24 315                                                \
    -stim_times 25 stimuli/rbcue.dire.times.326.31.txt 'BLOCK(2,1)'           \
    -stim_label 25 326.31                                                \
    -stim_times 26 stimuli/rbcue.dire.times.333.43.txt 'BLOCK(2,1)'           \
    -stim_label 26 333.43                                                \
    -stim_times 27 stimuli/rbcue.dire.times.341.57.txt 'BLOCK(2,1)'            \
    -stim_label 27 341.57                                                 \
    -jobs 8                                                                  \
    -fout -tout -x1D X.xmat.1D -xjpeg X.jpg                                  \
    -x1D_uncensored X.nocensor.xmat.1D                                       \
    -errts errts.${subj}                                                     \
    -bucket stats.$subj
    # -fitts fitts.$subj                                                       \

# display any large pairwise correlations from the X-matrix
1d_tool.py -show_cormat_warnings -infile X.xmat.1D |& tee out.cormat_warn.txt



# display degrees of freedom info from X-matrix
1d_tool.py -show_df_info -infile X.xmat.1D |& tee out.df_info.txt


# -- execute the 3dREMLfit script, written by 3dDeconvolve --
tcsh -x stats.REML_cmd 



# ==========================================================================
# script generated by the command:
#
# afni_proc.py -subj_id sub_001 -script proc.sub_001 -scr_overwrite -blocks   \
#     tshift align tlrc volreg mask scale regress -copy_anat                  \
#     /home/image030/fMRI_data/$subj/anat/T1W_3D_MPRAGE_1mm_SENSE.nii.gz -dsets \
#     /home/image030/fMRI_data/$subj/func_2/SR4_run1_SENSE.nii.gz               \
#     /home/image030/fMRI_data/$subj/func_2/SR4_run2_SENSE.nii.gz               \
#     /home/image030/fMRI_data/$subj/func_2/SR4_run3_SENSE.nii.gz               \
#     /home/image030/fMRI_data/$subj/func_2/SR4_run4_SENSE.nii.gz               \
#     /home/image030/fMRI_data/$subj/func_2/SR4_run5_SENSE.nii.gz               \
#     /home/image030/fMRI_data/$subj/func_2/SR4_run6_SENSE.nii.gz               \
#     -tcat_remove_first_trs 0 -align_opts_aea -giant_move -tlrc_base         \
#     MNI_avg152T1+tlrc -volreg_align_to MIN_OUTLIER -volreg_align_e2a        \
#     -volreg_tlrc_warp -regress_stim_times                                   \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_1.txt     \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_10.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_11.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_12.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_13.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_14.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_15.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_16.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_1.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_10.txt   \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_11.txt   \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_2.txt     \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_12.txt   \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_13.txt   \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_14.txt   \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_15.txt   \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_16.txt   \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_2.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_3.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_4.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_5.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_6.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_3.txt     \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_7.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_8.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.BlueFace_9.txt    \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.Cue_blue.txt      \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.Cue_red.txt       \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_4.txt     \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_5.txt     \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_6.txt     \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_7.txt     \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_8.txt     \
#     /home/image030/analysis_code/stimulus_rsa/rbcue.times.RedFace_9.txt     \
#     -regress_stim_labels RedFace_1 RedFace_10 RedFace_11 RedFace_12         \
#     RedFace_13 RedFace_14 RedFace_15 RedFace_16 BlueFace_1 BlueFace_10      \
#     BlueFace_11 RedFace_2 BlueFace_12 BlueFace_13 BlueFace_14 BlueFace_15   \
#     BlueFace_16 BlueFace_2 BlueFace_3 BlueFace_4 BlueFace_5 BlueFace_6      \
#     RedFace_3 BlueFace_7 BlueFace_8 BlueFace_9 Cue_blue Cue_red RedFace_4   \
#     RedFace_5 RedFace_6 RedFace_7 RedFace_8 RedFace_9 -regress_basis_multi  \
#     'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)'        \
#     'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)'        \
#     'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)'        \
#     'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)'        \
#     'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)'        \
#     'BLOCK(2,1)' GAM GAM 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)'             \
#     'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' -regress_censor_motion 2.0       \
#     -regress_motion_per_run -regress_opts_3dD -jobs 8                       \
#     -regress_make_ideal_sum sum_ideal.1D -regress_est_blur_epits            \
#     -regress_est_blur_errts
