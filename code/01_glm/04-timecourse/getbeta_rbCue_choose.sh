#!/bin/bash



raw_path="/home/medicaldata3/LJData/rbCue.choose.result/"

for subj in `cat NotNull.txt`
#for subj in 001
do
    echo $subj is running!
    cd ${raw_path}/${subj}
    
    # F1rel_IPL_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_F1rel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_F1rel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_F1rel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F1rel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_F1rel_IPL_l.txt

    # F2rel_precnetral_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_F2rel_precnetral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_F2rel_precnetral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_F2rel_precnetral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/F2rel_precnetral_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_F2rel_precnetral_l.txt


    # D_precentral_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_D_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_D_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_D_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_D_precentral_l.txt



    # D_insula_r.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_D_insular.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_D_insular.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_D_insular.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_D_insular.txt

    # D_IPL_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_D_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_D_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_D_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_D_IPL_l.txt


    # D_IFG_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_D_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_D_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_D_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_D_IFG_l.txt

  
    # D_Precuneus_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_D_precuneus_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_D_precuneus_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_D_precuneus_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/D_Precuneus_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_D_precuneus_l.txt
 

    # I_precentral_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_I_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_I_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_I_precentral_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/I_precentral_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_I_precentral_l.txt


    
    #  chrel_Putamen_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_chrel_putamen_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_chrel_putamen_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_chrel_putamen_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chrel_Putamen_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_chrel_putamen_l.txt

    
    #  chirrel_precuences.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_chirrel_precuences.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_chirrel_precuences.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_chirrel_precuences.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_precuences.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_chirrel_precuences.txt
  

    #  chirrel_MFG_r.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_chirrel_MFG_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_chirrel_MFG_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_chirrel_MFG_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/chirrel_MFG_r.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_chirrel_MFG_r.txt


    #  unrel_IFG_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_unrel_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_unrel_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_unrel_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_unrel_IFG_l.txt


    #  unrel_MFG_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_unrel_MFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_unrel_MFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_unrel_MFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_unrel_MFG_l.txt
 
    
    #  unrel_IPL_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#1_Coef]>>choose_rel_unrel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.choose#2_Coef]>>choose_irrel_unrel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#1_Coef]>>unchoose_rel_unrel_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_rbcue_ROI/unrel_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.unchoose#2_Coef]>>unchoose_irrel_unrel_IPL_l.txt

done
echo 'ALL processes is done!'

