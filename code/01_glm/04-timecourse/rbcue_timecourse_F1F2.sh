#!/bin/bash



raw_path="/home/medicaldata/LJData/SR_ana/analysis_res/rbCue.F1F2relirrel.tent.result"

for subj in `cat NotNull.txt`
#for subj in 001
do
    echo $subj is running!
    cd ${raw_path}/${subj}
        # F1
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_F1rel_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_F2rel_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_D_pecentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_D_insular.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_D_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_D_IFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_D_precuneusl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_I_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_chrel_putamenl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_chirrel_precuences.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_chirrel_MFGr.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_unrel_IFGl.txt        
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_MFG_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_unrel_MFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}.nii[times.F1#${num}_Coef]
    done >>F1_unrel_IPLl.txt
    
   # F2
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_F1rel_IPLl.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_F2rel_precentrall.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_D_precentrall.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_D_insular.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_D_IPLl.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_D_IFGl.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_D_precuneusl.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_I_precentrall.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_chrel_putamenl.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_chirrel_precuences.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_chirrel_MFGr.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_unrel_IFGl.txt        
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_MFG_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_unrel_MFGl.txt
    
    for num in {0..49}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}.nii[GLM2.times.F2#${num}_Coef]
    done >>F2_unrel_IPLl.txt
     
done
echo 'ALL processes is done!'

