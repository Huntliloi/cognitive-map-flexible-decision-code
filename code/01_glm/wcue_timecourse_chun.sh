#!/bin/bash



raw_path="/home/medicaldata/LJData/SR_ana/analysis_res/wCue.diag.choose.tent.result"

for subj in `cat NotNull.txt`
#for subj in 001
do
    echo $subj is running!
    cd ${raw_path}/${subj}
    
    # choose    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiag_PCG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_chdiag_PCG_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiagdiff_HC_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_chdiagdiff_HC_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/F2diagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_F2diagdiff_insula_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_undiagdiff_IFG_l.txt        

    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_undiagdiff_insula_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_undiagdiff_insula_r.txt    
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_undiagdiff_IPL_l.txt     
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_precuneus.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_undiagdiff_precuneus.txt        

    # unchoose

    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiag_PCG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_chdiag_PCG_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiagdiff_HC_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_chdiagdiff_HC_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/F2diagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_F2diagdiff_insula_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_undiagdiff_IFG_l.txt        

    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_undiagdiff_insula_l.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_undiagdiff_insula_r.txt    
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_undiagdiff_IPL_l.txt     
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_precuneus.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_undiagdiff_precuneus.txt   
done
echo 'ALL processes is done!'

