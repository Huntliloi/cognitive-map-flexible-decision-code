#!/bin/bash

##################### GLM analysis timing_file generate #####################
# 前6个run，rbcue.***
ipath=/home/image030/analysis_code/stimulus_orig/rbCue.glm
opath=/home/image030/analysis_code/stimulus_glm
if [ -f $opath/rbcue.times.redCue.txt ]
then
echo rbCue glm timing_file is exist!
else
    timing_tool.py -multi_timing_3col_tsv $ipath/blueCue_run_*.tsv -write_multi_timing $opath/rbcue.
    
    timing_tool.py -multi_timing_3col_tsv $ipath/redCue_run_*.tsv -write_multi_timing $opath/rbcue.
    
    timing_tool.py -multi_timing_3col_tsv $ipath/F1_run_[1-6].tsv \
                   -tsv_labels onset duration trial_type relevant_rank  irrelevant_rank \
                   -write_multi_timing $opath/rbcue.
                   
    timing_tool.py -multi_timing_3col_tsv $ipath/F2_GLM1_run_[1-6].tsv \
                   -tsv_labels onset duration trial_type relevant_rank  irrelevant_rank D I \
                   -write_multi_timing $opath/rbcue.GLM1.
                   
    timing_tool.py -multi_timing_3col_tsv $ipath/F2_GLM2_run_[1-6].tsv \
                   -tsv_labels onset duration trial_type relevant_rank  irrelevant_rank E \
                   -write_multi_timing $opath/rbcue.GLM2.
fi
               
# 后3个run，wcue.***
ipath=/home/image030/analysis_code/stimulus_orig/wCue.glm
opath=/home/image030/analysis_code/stimulus_glm
if [ -f $opath/wcue.times.whiteCue.txt ]
then
echo wCue glm timing_file is exist!
else
    timing_tool.py -multi_timing_3col_tsv $ipath/whiteCue_run_*.tsv \
                   -write_multi_timing $opath/wcue. 
    
    timing_tool.py -multi_timing_3col_tsv $ipath/F1_run_[7-9].tsv -tsv_labels onset duration trial_type relevant_rank  irrelevant_rank \
                   -write_multi_timing $opath/wcue.
                   
    timing_tool.py -multi_timing_3col_tsv $ipath/F2_GLM1_run_[7-9].tsv -tsv_labels onset duration trial_type relevant_rank  irrelevant_rank D I \
                   -write_multi_timing $opath/wcue.GLM1.
                   
    timing_tool.py -multi_timing_3col_tsv $ipath/F2_GLM2_run_[7-9].tsv -tsv_labels onset duration trial_type relevant_rank  irrelevant_rank E \
                   -write_multi_timing $opath/wcue.GLM2.
fi           
#############################################################################


#####################     RSA  timing_file generate     #####################

# 前6个run，rbcue.***
ipath=/home/image030/analysis_code/stimulus_orig/rbCue.rsa
opath=/home/image030/analysis_code/stimulus_rsa
if [ -f $opath/rbcue.times.Cue_red.txt ]
then
echo rbCue rsa timing_file is exist!
else
    
    timing_tool.py -multi_timing_3col_tsv $ipath/rsa_run_*.tsv \
                   -write_multi_timing $opath/rbcue. 
fi      
       
# 后3个run，wcue.***
ipath=/home/image030/analysis_code/stimulus_orig/wCue.rsa
opath=/home/image030/analysis_code/stimulus_rsa      

if [ -f $opath/wcue.times.Cue_blank.txt ]
then
echo wCue rsa timing_file is exist!
else
timing_tool.py -multi_timing_3col_tsv $ipath/rsa_run_*.tsv \
               -write_multi_timing $opath/wcue. 
fi
#############################################################################




############################### SR3 #########################################
############################### SR3 #########################################
############################### SR3 #########################################
##################### GLM analysis timing_file generate #####################

ipath=/home/image030/analysis_code/stimulus_orig/sr3.glm/rest
opath=/home/image030/analysis_code/stimulus_glm
if [ -f $opath/sr3.GLM.rest.times.red.txt ]
then
echo glm timing_file is exist!
else
        timing_tool.py -multi_timing_3col_tsv $ipath/SR3_Run*.tsv \
               -tsv_labels onset duration trial_type rank \
               -write_multi_timing $opath/sr3.GLM.rest.

fi
                      

ipath=/home/image030/analysis_code/stimulus_orig/sr3.glm/s001-2pre
opath=/home/image030/analysis_code/stimulus_glm
if [ -f $opath/sr3.GLM.s12pre.times.red.txt ]
then
echo glm timing_file is exist!
else

    
    
    timing_tool.py -multi_timing_3col_tsv $ipath/SR3_Run*.tsv \
               -tsv_labels onset duration trial_type rank \
               -write_multi_timing $opath/sr3.GLM.s12pre.

fi


ipath=/home/image030/analysis_code/stimulus_orig/sr3.glm/s001-2post
opath=/home/image030/analysis_code/stimulus_glm
if [ -f $opath/sr3.GLM.s12post.times.red.txt ]
then
echo glm timing_file is exist!
else

    
    
    timing_tool.py -multi_timing_3col_tsv $ipath/SR3_Run*.tsv \
               -tsv_labels onset duration trial_type rank \
               -write_multi_timing $opath/sr3.GLM.s12post.

fi


ipath=/home/image030/analysis_code/stimulus_orig/sr3.glm/s003-4pre
opath=/home/image030/analysis_code/stimulus_glm
if [ -f $opath/sr3.GLM.s34pre.times.red.txt ]
then
echo glm timing_file is exist!
else

    
    
    timing_tool.py -multi_timing_3col_tsv $ipath/SR3_Run*.tsv \
               -tsv_labels onset duration trial_type rank \
               -write_multi_timing $opath/sr3.GLM.s34pre.

fi

#############################################################################


#####################     RSA  timing_file generate     #####################

ipath=/home/image030/analysis_code/stimulus_orig/sr3.rsa/rest
opath=/home/image030/analysis_code/stimulus_rsa
if [ -f $opath/sr3.rsa.rest.times.red_1.txt ]
then
echo rsa timing_file is exist!
else
    
    timing_tool.py -multi_timing_3col_tsv $ipath/rsa_SR3_Run*.tsv -write_multi_timing $opath/sr3.rsa.rest.

fi 

ipath=/home/image030/analysis_code/stimulus_orig/sr3.rsa/s001-2pre
opath=/home/image030/analysis_code/stimulus_rsa
if [ -f $opath/sr3.rsa.s12pre.times.red_1.txt ]
then
echo rsa timing_file is exist!
else
    
    timing_tool.py -multi_timing_3col_tsv $ipath/rsa_SR3_Run*.tsv -write_multi_timing $opath/sr3.rsa.s12pre.

fi 


ipath=/home/image030/analysis_code/stimulus_orig/sr3.rsa/s001-2post
opath=/home/image030/analysis_code/stimulus_rsa
if [ -f $opath/sr3.rsa.s12post.times.red_1.txt ]
then
echo rsa timing_file is exist!
else

    timing_tool.py -multi_timing_3col_tsv $ipath/rsa_SR3_Run*.tsv -write_multi_timing $opath/sr3.rsa.s12post.

fi 

ipath=/home/image030/analysis_code/stimulus_orig/sr3.rsa/s003-4pre
opath=/home/image030/analysis_code/stimulus_rsa
if [ -f $opath/sr3.rsa.s34pre.times.red_1.txt ]
then
echo rsa timing_file is exist!
else

    timing_tool.py -multi_timing_3col_tsv $ipath/rsa_SR3_Run*.tsv -write_multi_timing $opath/sr3.rsa.s34pre.
    
fi 


#############################################################################


