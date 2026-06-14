#!/bin/tcsh -xef

# the user may specify a single subject to run with
if ( $#argv > 0 ) then
    set subj = $argv[1]
else
    set subj = sub_001
endif

# set glm1_rpath = /home/image030/analysis_res/rbCue.glm1.result/${subj}
set glm1_rpath = /home/medicaldata/LJData/SR_ana/analysis_res/glm_raw/rbCue.glm1.result/${subj}
if ( ! -d $glm1_rpath ) then
    echo "This subject ${subj}'s glm1 result is not exsit, please do glm1 process first!"
    exit
endif

# assign output directory name
# set output_dir = /home/image030/analysis_res/rbCue.glm2.result/$subj
set output_dir = /home/medicaldata3/LJData/rsa/PPI_ana/rbCue.ppi.result/$subj
# verify that the results directory does not yet exist
if ( -d $output_dir ) then
    echo output dir "$subj.results" already exists
    exit
endif

# create results and stimuli directories
mkdir -p $output_dir
mkdir -p $output_dir/stimuli

cd $output_dir

# copy stim files into stimulus directory
cp  /home/image030/analysis_code/stimulus_glm/rbCue.ppi/rbCue.ppi.times.F1.txt   \
    /home/image030/analysis_code/stimulus_glm/rbCue.ppi/rbCue.ppi.times.F2.txt \
    $output_dir/stimuli
    
# ------------------------------
# run the regression analysis
3dDeconvolve -input $glm1_rpath/pb04.$subj.r*.scale+tlrc.HEAD                            \
    -censor $glm1_rpath/motion_${subj}_censor.1D                                         \
    -ortvec $glm1_rpath/mot_demean.r01.1D mot_demean_r01                                 \
    -ortvec $glm1_rpath/mot_demean.r02.1D mot_demean_r02                                 \
    -ortvec $glm1_rpath/mot_demean.r03.1D mot_demean_r03                                 \
    -ortvec $glm1_rpath/mot_demean.r04.1D mot_demean_r04                                 \
    -ortvec $glm1_rpath/mot_demean.r05.1D mot_demean_r05                                 \
    -ortvec $glm1_rpath/mot_demean.r06.1D mot_demean_r06                                 \
    -polort 3 -float                                                         \
    -num_stimts 2                                                            \
    -stim_times 1 stimuli/rbCue.ppi.times.F1.txt 'BLOCK(2,1)'                \
    -stim_label 1 F1                                               \
    -stim_times 2 stimuli/rbCue.ppi.times.F2.txt 'BLOCK(2,1)'                \
    -stim_label 2 F2                                                   \
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