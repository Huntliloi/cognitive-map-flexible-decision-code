#!/bin/bash

ana_path="/home/medicaldata/LJData/SR_ana/analysis_res"
result_path="/home/medicaldata/LJData/SR_ana/analysis_res/xmat_rbCue/"

for subj in `cat NotNull.txt`
#for subj in 001

do
    
    mkdir -p ${result_path}
    cd ${result_path}
    echo wCue.glm1$subj is running!
    mkdir A E I D 

#    1d_tool.py -infile ${ana_path}/glm_raw/wCue.glm1.result/${subj}/motion_${subj}_censor.1D -write ./motion_${subj}.txt

    1d_tool.py -infile ${ana_path}/rbCue.glm1.D.result/${subj}/X.xmat.1D -write ./D/xmat.${subj}.D.txt
    1d_tool.py -infile ${ana_path}/rbCue.glm2.I.result/${subj}/X.xmat.1D -write ./I/xmat.${subj}.I.txt
    1d_tool.py -infile ${ana_path}/rbCue.glm3.E.result/${subj}/X.xmat.1D -write ./E/xmat.${subj}.E.txt
    1d_tool.py -infile ${ana_path}/rbCue.glm4.A.result/${subj}/X.xmat.1D -write ./A/xmat.${subj}.A.txt
    
done
echo 'ALL processes is done!'
