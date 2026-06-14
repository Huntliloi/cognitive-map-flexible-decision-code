#!/bin/bash



raw_path="/home/medicaldata3/LJData/rbCue.easyhard.tent.result"

for subj in `cat NotNull.txt`
#for subj in 001
do
    echo $subj is running!
    cd ${raw_path}/${subj}
        # F1.EASY
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_F1rel_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_F2rel_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_D_pecentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_D_insular.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_D_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_D_IFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_D_precuneusl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_I_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_chrel_putamenl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_chirrel_precuences.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_chirrel_MFGr.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_unrel_IFGl.txt        
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_MFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_unrel_MFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.easy#${num}_Coef]
    done >>F1.easy_unrel_IPLl.txt
    
    # F1.HARD
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_F1rel_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_F2rel_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_D_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_D_insular.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_D_IPLl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_D_IFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_D_precuneusl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_I_precentrall.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_chrel_putamenl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_chirrel_precuences.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_chirrel_MFGr.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_unrel_IFGl.txt        
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_MFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_unrel_MFGl.txt
    
    for num in {0..29}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F1.hard#${num}_Coef]
    done >>F1.hard_unrel_IPLl.txt


    # F2.easy
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_F1rel_IPLl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_F2rel_precentrall.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_D_pecentrall.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_D_insular.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_D_IPLl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_D_IFGl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_D_precuneusl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_I_precentrall.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_chrel_putamenl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_chirrel_precuences.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_chirrel_MFGr.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_unrel_IFGl.txt        
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_MFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_unrel_MFGl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.easy#${num}_Coef]
    done >>F2.easy_unrel_IPLl.txt
    
   # F2.hard
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_F1rel_IPLl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_F2rel_precentrall.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_D_precentrall.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_D_insular.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_D_IPLl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_D_IFGl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_D_precuneusl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_I_precentrall.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_chrel_putamenl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_chirrel_precuences.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_chirrel_MFGr.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_unrel_IFGl.txt        
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_MFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_unrel_MFGl.txt
    
    for num in {0..39}; do
      3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F2.hard#${num}_Coef]
    done >>F2.hard_unrel_IPLl.txt


     
done
echo 'ALL processes is done!'

