#!/bin/bash



raw_path="/home/medicaldata/LJData/SR_ana/analysis_res/glm/rbCue.NoREL.glm12.DI/"

for subj in `cat NotNull.txt`
#for subj in 001
do
    echo $subj is running!
    cd ${raw_path}/${subj}
    
    # F1rel_IPL_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_F1rel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_F1rel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_F1rel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_F1rel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_F1rel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_F1rel_IPL_l.txt

    # F2rel_precnetral_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_F2rel_precnetral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_F2rel_precnetral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_F2rel_precnetral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_F2rel_precnetral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_F2rel_precnetral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_F2rel_precnetral_l.txt


    # D_precentral_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_D_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_D_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_D_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_D_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_D_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_D_precentral_l.txt


    # D_insula_r.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_D_insular.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_D_insular.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_D_insular.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_D_insular.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_D_insular.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_D_insular.txt

    # D_IPL_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_D_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_D_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_D_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_D_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_D_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_D_IPL_l.txt


    # D_IFG_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_D_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_D_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_D_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_D_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_D_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_D_IFG_l.txt
  
  
    # D_Precuneus_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_D_precuneus_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_D_precuneus_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_D_precuneus_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_D_precuneus_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_D_precuneus_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_D_precuneus_l.txt
    

    # I_precentral_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_I_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_I_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_I_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_I_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_I_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_I_precentral_l.txt
  

    
    #  chrel_Putamen_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_chrel_putamen_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_chrel_putamen_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_chrel_putamen_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_chrel_putamen_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_chrel_putamen_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_chrel_putamen_l.txt
    
    
    #  chirrel_precuences.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_chirrel_precuences.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_chirrel_precuences.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_chirrel_precuences.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_chirrel_precuences.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_chirrel_precuences.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_chirrel_precuences.txt
    

    #  chirrel_MFG_r.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_chirrel_MFG_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_chirrel_MFG_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_chirrel_MFG_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_chirrel_MFG_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_chirrel_MFG_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_chirrel_MFG_r.txt
  

    #  unrel_IFG_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_unrel_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_unrel_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_unrel_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_unrel_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_unrel_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_unrel_IFG_l.txt
    

    #  unrel_MFG_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_unrel_MFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_unrel_MFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_unrel_MFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_unrel_MFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_unrel_MFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_unrel_MFG_l.txt
    
    
    #  unrel_IPL_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}.nii[times.F1#1_Coef]>>F1_rel_unrel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}.nii[times.F1#2_Coef]>>F1_irrel_unrel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#1_Coef]>>F2_rel_unrel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#2_Coef]>>F2_irrel_unrel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#3_Coef]>>F2_D_unrel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}.nii[GLM1.times.F2#4_Coef]>>F2_I_unrel_IPL_l.txt

done
echo 'ALL processes is done!'

