#!/bin/bash


result_path="/home/medicaldata/LJData/SR_ana/analysis_res"
raw_path="/home/medicaldata/LJData/SR_ana/analysis_res/glm_raw/rbCue.glm1.result"

for subj in `cat NotNull.txt`
do
    for run in 01 02 03
    do
      cd ${raw_path}/${subj}
      rm pb04.${subj}.r${run}.scale_roi*
      3dcalc -a pb04.${subj}.r${run}.scale+tlrc -b ../../../rois/Amyl.nii -expr 'a*b' -prefix pb04.${subj}.r${run}.scale_Amyl
    done
done
echo 'ALL processes is done!'




# for subj in `cat NotNull.txt`
# do
#    echo $subj is running!
#    mkdir -p ${result_path}/epi_mask
#    cd ${result_path}/epi_mask
    
#    cp ${raw_path}/${subj}/mask_epi_anat.* ./

# done
#    3dmask_tool -input mask_epi_anat.*+tlrc.HEAD -prefix mask_inter \
#                  -frac 1.0