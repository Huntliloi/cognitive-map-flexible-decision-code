#!/bin/bash



raw_path="/home/medicaldata/LJData/SR_ana/analysis_res/wCue.diagF1F2.tent.result"

for subj in `cat NotNull.txt`
#for subj in 001
do
    echo $subj is running!
    cd ${raw_path}/${subj}
    
    # choose    
    for num in {0..19}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiag_PCG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#${num}_Coef]
    done >>F1_chdiag_PCG_l.txt
    
    for num in {0..19}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiagdiff_HC_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#${num}_Coef]
    done >>F1_chdiagdiff_HC_l.txt
    
    for num in {0..19}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/F2diagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#${num}_Coef]
    done >>F1_F2diagdiff_insula_l.txt
    
    for num in {0..19}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#${num}_Coef]
    done >>F1_undiagdiff_IFG_l.txt        

    for num in {0..19}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#${num}_Coef]
    done >>F1_undiagdiff_insula_l.txt
    
    for num in {0..19}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.F1#${num}_Coef]
    done >>F1_undiagdiff_insula_r.txt    
    
    for num in {0..19}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#${num}_Coef]
    done >>F1_undiagdiff_IPL_l.txt     
    
    for num in {0..19}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_precuneus.nii -q stats.${subj}+tlrc.BRIK[times.F1#${num}_Coef]
    done >>F1_undiagdiff_precuneus.txt        

    # F2

    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiag_PCG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#${num}_Coef]
    done >>F2_chdiag_PCG_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiagdiff_HC_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#${num}_Coef]
    done >>F2_chdiagdiff_HC_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/F2diagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#${num}_Coef]
    done >>F2_F2diagdiff_insula_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#${num}_Coef]
    done >>F2_undiagdiff_IFG_l.txt        

    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#${num}_Coef]
    done >>F2_undiagdiff_insula_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.F2#${num}_Coef]
    done >>F2_undiagdiff_insula_r.txt    
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#${num}_Coef]
    done >>F2_undiagdiff_IPL_l.txt     
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_precuneus.nii -q stats.${subj}+tlrc.BRIK[times.F2#${num}_Coef]
    done >>F2_undiagdiff_precuneus.txt   
done
echo 'ALL processes is done!'

