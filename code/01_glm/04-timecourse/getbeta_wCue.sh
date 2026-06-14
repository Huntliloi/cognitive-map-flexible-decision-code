#!/bin/bash



raw_path="/home/medicaldata/LJData/SR_ana/analysis_res/wCue.diagF1F2.result/"

for subj in `cat NotNull.txt`
#for subj in 001
do
    echo $subj is running!
    cd ${raw_path}/${subj}
    
    # chdiag_PCG_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiag_PCG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#1_Coef]>>F1_diag_chdiag_PCG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiag_PCG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#1_Coef]>>F2_diag_chdiag_PCG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiag_PCG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#2_Coef]>>F2_diagdiff_chdiag_PCG_l.txt

    # chdiagdiff_HC_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiagdiff_HC_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#1_Coef]>>F1_diag_chdiagdiff_HC_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiagdiff_HC_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#1_Coef]>>F2_diag_chdiagdiff_HC_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/chdiagdiff_HC_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#2_Coef]>>F2_diagdiff_chdiagdiff_HC_l.txt


    # F2diagdiff_insula_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/F2diagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#1_Coef]>>F1_diag_F2diagdiff_insula_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/F2diagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#1_Coef]>>F2_diag_F2diagdiff_insula_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/F2diagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#2_Coef]>>F2_diagdiff_F2diagdiff_insula_l.txt


    # undiagdiff_IFG_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#1_Coef]>>F1_diag_undiagdiff_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#1_Coef]>>F2_diag_undiagdiff_IFG_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IFG_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#2_Coef]>>F2_diagdiff_undiagdiff_IFG_l.txt

    # undiagdiff_insula_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#1_Coef]>>F1_diag_undiagdiff_insula_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#1_Coef]>>F2_diag_undiagdiff_insula_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#2_Coef]>>F2_diagdiff_undiagdiff_insula_l.txt


    # undiagdiff_insula_r.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.F1#1_Coef]>>F1_diag_undiagdiff_insula_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.F2#1_Coef]>>F2_diag_undiagdiff_insula_r.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_insula_r.nii -q stats.${subj}+tlrc.BRIK[times.F2#2_Coef]>>F2_diagdiff_undiagdiff_insula_r.txt
  
  
    # undiagdiff_IPL_l.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F1#1_Coef]>>F1_diag_undiagdiff_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#1_Coef]>>F2_diag_undiagdiff_IPL_l.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_IPL_l.nii -q stats.${subj}+tlrc.BRIK[times.F2#2_Coef]>>F2_diagdiff_undiagdiff_IPL_l.txt
    

    # undiagdiff_precuneus.nii
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_precuneus.nii -q stats.${subj}+tlrc.BRIK[times.F1#1_Coef]>>F1_diag_undiagdiff_precuneus.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_precuneus.nii -q stats.${subj}+tlrc.BRIK[times.F2#1_Coef]>>F2_diag_undiagdiff_precuneus.txt
    3dmaskave -mask /home/medicaldata/LJData/SR_ana/analysis_res/rois/SR4_wCue_diag_ROI/undiagdiff_precuneus.nii -q stats.${subj}+tlrc.BRIK[times.F2#2_Coef]>>F2_diagdiff_undiagdiff_precuneus.txt
  
done
echo 'ALL processes is done!'

