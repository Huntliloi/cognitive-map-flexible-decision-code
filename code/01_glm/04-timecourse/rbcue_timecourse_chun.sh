#!/bin/bash



raw_path="/home/medicaldata3/LJData/rbCue.choose.tent.result"

for subj in `cat NotNull.txt`
#for subj in 001
do
    echo $subj is running!
    cd ${raw_path}/${subj}
        # F1
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_F1rel_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_F2rel_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_D_pecentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_D_insular.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_D_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_D_IFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_D_precuneusl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_I_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_chrel_putamenl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_chirrel_precuences.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_chirrel_MFGr.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_unrel_IFGl.txt        
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_MFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_unrel_MFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#${num}_Coef]
    done >>choose_unrel_IPLl.txt
    
   # unchoose
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_F1rel_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_F2rel_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_D_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_D_insular.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_D_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_D_IFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_D_precuneusl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_I_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_chrel_putamenl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_chirrel_precuences.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_chirrel_MFGr.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_unrel_IFGl.txt        
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_MFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_unrel_MFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#${num}_Coef]
    done >>unchoose_unrel_IPLl.txt
     
done
echo 'ALL processes is done!'

