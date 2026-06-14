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
set output_dir = /home/medicaldata3/LJData/rsa/rbCue.rsa_direction.result/$subj
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
cp /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.0.3217505.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.0.4636476.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.0.5880026.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.0.7853981.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.0.9827937.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.1.1071487.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.1.8925468.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.2.0344439.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.2.1587989.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.2.3561944.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.2.5535900.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.2.6779450.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.2.8198420.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.3.4633432.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.3.6052402.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.3.7295952.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.3.9269908.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.4.1243863.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.4.2487413.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.4.3906384.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.5.0341395.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.5.1760365.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.5.3003915.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.5.4977871.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.5.6951827.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.5.8195376.txt \
   /home/image030/analysis_code/stimulus_rsa/rbcue.rsa.direction/rbcue.dire.times.5.9614347.txt \
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
    -stim_times 1 stimuli/rbcue.dire.times.0.3217505.txt 'BLOCK(2,1)'             \
    -stim_label 1 0.3217505                                                  \
    -stim_times 2 stimuli/rbcue.dire.times.0.4636476.txt 'BLOCK(2,1)'            \
    -stim_label 2 0.4636476                                                 \
    -stim_times 3 stimuli/rbcue.dire.times.0.5880026.txt 'BLOCK(2,1)'            \
    -stim_label 3 0.5880026                                                 \
    -stim_times 4 stimuli/rbcue.dire.times.0.7853981.txt 'BLOCK(2,1)'            \
    -stim_label 4 0.7853981                                                 \
    -stim_times 5 stimuli/rbcue.dire.times.0.9827937.txt 'BLOCK(2,1)'            \
    -stim_label 5 0.9827937                                                 \
    -stim_times 6 stimuli/rbcue.dire.times.1.1071487.txt 'BLOCK(2,1)'            \
    -stim_label 6 1.1071487                                                 \
    -stim_times 7 stimuli/rbcue.dire.times.1.8925468.txt 'BLOCK(2,1)'            \
    -stim_label 7 1.8925468                                                 \
    -stim_times 8 stimuli/rbcue.dire.times.2.0344439.txt 'BLOCK(2,1)'            \
    -stim_label 8 2.0344439                                                 \
    -stim_times 9 stimuli/rbcue.dire.times.2.1587989.txt 'BLOCK(2,1)'            \
    -stim_label 9 2.1587989                                                 \
    -stim_times 10 stimuli/rbcue.dire.times.2.3561944.txt 'BLOCK(2,1)'          \
    -stim_label 10 2.3561944                                               \
    -stim_times 11 stimuli/rbcue.dire.times.2.5535900.txt 'BLOCK(2,1)'          \
    -stim_label 11 2.5535900                                               \
    -stim_times 12 stimuli/rbcue.dire.times.2.6779450.txt 'BLOCK(2,1)'            \
    -stim_label 12 2.6779450                                                 \
    -stim_times 13 stimuli/rbcue.dire.times.2.8198420.txt 'BLOCK(2,1)'          \
    -stim_label 13 2.8198420                                               \
    -stim_times 14 stimuli/rbcue.dire.times.3.4633432.txt 'BLOCK(2,1)'          \
    -stim_label 14 3.4633432                                               \
    -stim_times 15 stimuli/rbcue.dire.times.3.6052402.txt 'BLOCK(2,1)'          \
    -stim_label 15 3.6052402                                               \
    -stim_times 16 stimuli/rbcue.dire.times.3.7295952.txt 'BLOCK(2,1)'          \
    -stim_label 16 3.7295952                                               \
    -stim_times 17 stimuli/rbcue.dire.times.3.9269908.txt 'BLOCK(2,1)'          \
    -stim_label 17 3.9269908                                               \
    -stim_times 18 stimuli/rbcue.dire.times.4.1243863.txt 'BLOCK(2,1)'           \
    -stim_label 18 4.1243863                                                \
    -stim_times 19 stimuli/rbcue.dire.times.4.2487413.txt 'BLOCK(2,1)'           \
    -stim_label 19 4.2487413                                                \
    -stim_times 20 stimuli/rbcue.dire.times.4.3906384.txt 'BLOCK(2,1)'           \
    -stim_label 20 4.3906384                                                \
    -stim_times 21 stimuli/rbcue.dire.times.5.0341395.txt 'BLOCK(2,1)'           \
    -stim_label 21 5.0341395                                                \
    -stim_times 22 stimuli/rbcue.dire.times.5.1760365.txt 'BLOCK(2,1)'           \
    -stim_label 22 5.1760365                                                \
    -stim_times 23 stimuli/rbcue.dire.times.5.3003915.txt 'BLOCK(2,1)'            \
    -stim_label 23 5.3003915                                                 \
    -stim_times 24 stimuli/rbcue.dire.times.5.4977871.txt 'BLOCK(2,1)'           \
    -stim_label 24 5.4977871                                                \
    -stim_times 25 stimuli/rbcue.dire.times.5.6951827.txt 'BLOCK(2,1)'           \
    -stim_label 25 5.6951827                                                \
    -stim_times 26 stimuli/rbcue.dire.times.5.8195376.txt 'BLOCK(2,1)'           \
    -stim_label 26 5.8195376                                                \
    -stim_times 27 stimuli/rbcue.dire.times.5.9614347.txt 'BLOCK(2,1)'            \
    -stim_label 27 5.9614347                                                 \
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
