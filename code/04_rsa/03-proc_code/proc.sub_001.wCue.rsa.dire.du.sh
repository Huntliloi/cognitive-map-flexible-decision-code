#!/bin/tcsh -xef

# the user may specify a single subject to run with
if ( $#argv > 0 ) then
    set subj = $argv[1]
else
    set subj = sub_001
endif

# set glm1_rpath = /home/image030/analysis_res/wCue.glm1.result/${subj}
set glm1_rpath = /home/medicaldata3/LJData/rsa/wCue.rsa.result/${subj}
if ( ! -d $glm1_rpath ) then
    echo "This subject ${subj}'s glm1 result is not exsit, please do glm1 process first!"
    exit
endif


# assign output directory name
# set output_dir = /home/image030/analysis_res/wCue.rsa.result/$subj
set output_dir = /home/medicaldata3/LJData/rsa/wCue.rsa_direction.du.result/$subj
# verify that the results directory does not yet exist
if ( -d $output_dir ) then
    echo output dir "$subj.results" already exists
    exit
endif

# # set list of runs
# set runs = (`count -digits 2 1 3`)

# create results and stimuli directories
mkdir -p $output_dir
mkdir -p $output_dir/stimuli

cd $output_dir

# copy stim files into stimulus directory
cp /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.18.43.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.26.57.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.33.69.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.45.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.63.43.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.71.57.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.198.43.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.206.57.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.213.69.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.225.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.236.31.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.243.43.txt  \
   /home/image030/analysis_code/stimulus_rsa/wcue.rsa.direction.du/wcue.dire.times.251.57.txt  \
   $output_dir/stimuli


# ------------------------------
# run the regression analysis
3dDeconvolve -input $glm1_rpath/pb03.$subj.r*.scale+tlrc.HEAD                        \
    -censor $glm1_rpath/motion_${subj}_censor.1D                                     \
    -ortvec $glm1_rpath/mot_demean.r01.1D mot_demean_r01                             \
    -ortvec $glm1_rpath/mot_demean.r02.1D mot_demean_r02                             \
    -ortvec $glm1_rpath/mot_demean.r03.1D mot_demean_r03                             \
    -polort 3 -float                                                     \
    -num_stimts 13                                                       \
    -stim_times 1 stimuli/wcue.dire.times.18.43.txt 'BLOCK(2,1)'                 \
    -stim_label 1 18.43                                              \
    -stim_times 2 stimuli/wcue.dire.times.26.57.txt 'BLOCK(2,1)'            \
    -stim_label 2 26.57                                                \
    -stim_times 3 stimuli/wcue.dire.times.33.69.txt 'BLOCK(2,1)'            \
    -stim_label 3 33.69                                                \
    -stim_times 4 stimuli/wcue.dire.times.45.txt 'BLOCK(2,1)'            \
    -stim_label 4 45                                                \
    -stim_times 5 stimuli/wcue.dire.times.63.43.txt 'BLOCK(2,1)'            \
    -stim_label 5 63.43                                                \
    -stim_times 6 stimuli/wcue.dire.times.71.57.txt 'BLOCK(2,1)'            \
    -stim_label 6 71.57                                                \
    -stim_times 7 stimuli/wcue.dire.times.198.43.txt 'BLOCK(2,1)'            \
    -stim_label 7 198.43                                                \
    -stim_times 8 stimuli/wcue.dire.times.206.57.txt 'BLOCK(2,1)'             \
    -stim_label 8 206.57                                                 \
    -stim_times 9 stimuli/wcue.dire.times.213.69.txt 'BLOCK(2,1)'             \
    -stim_label 9 213.69                                                 \
    -stim_times 10 stimuli/wcue.dire.times.225.txt 'BLOCK(2,1)'            \
    -stim_label 10 225                                                \
    -stim_times 11 stimuli/wcue.dire.times.236.31.txt 'BLOCK(2,1)'            \
    -stim_label 11 236.31                                                \
    -stim_times 12 stimuli/wcue.dire.times.243.43.txt 'BLOCK(2,1)'            \
    -stim_label 12 243.43                                                \
    -stim_times 13 stimuli/wcue.dire.times.251.57.txt 'BLOCK(2,1)'            \
    -stim_label 13 251.57                                                \
    -jobs 8                                                              \
    -fout -tout -x1D X.xmat.1D -xjpeg X.jpg                              \
    -x1D_uncensored X.nocensor.xmat.1D                                   \
    -errts errts.${subj}                                                 \
    -bucket stats.$subj
    # -fitts fitts.$subj                                                   \



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
#     /home/image030/fMRI_data/$subj/func_2/SR4_run7_SENSE.nii.gz               \
#     /home/image030/fMRI_data/$subj/func_2/SR4_run8_SENSE.nii.gz               \
#     /home/image030/fMRI_data/$subj/func_2/SR4_run9_SENSE.nii.gz               \
#     -tcat_remove_first_trs 0 -align_opts_aea -giant_move -tlrc_base         \
#     MNI_avg152T1+tlrc -volreg_align_to MIN_OUTLIER -volreg_align_e2a        \
#     -volreg_tlrc_warp -regress_stim_times                                   \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Cue_blank.txt      \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_10.txt        \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_11.txt        \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_12.txt        \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_13.txt        \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_14.txt        \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_15.txt        \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_2.txt         \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_3.txt         \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_4.txt         \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_5.txt         \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_6.txt         \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_7.txt         \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_8.txt         \
#     /home/image030/analysis_code/stimulus_rsa/wcue.times.Face_9.txt         \
#     -regress_stim_labels Cue_blank Face_10 Face_11 Face_12 Face_13 Face_14  \
#     Face_15 Face_2 Face_3 Face_4 Face_5 Face_6 Face_7 Face_8 Face_9         \
#     -regress_basis_multi GAM 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)'         \
#     'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)'        \
#     'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)' 'BLOCK(2,1)'        \
#     'BLOCK(2,1)' -regress_censor_motion 2.0 -regress_motion_per_run         \
#     -regress_opts_3dD -jobs 8 -regress_make_ideal_sum sum_ideal.1D          \
#     -regress_est_blur_epits -regress_est_blur_errts
