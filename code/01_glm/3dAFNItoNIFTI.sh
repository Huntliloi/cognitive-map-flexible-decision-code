#!/bin/bash

ana_path="/home/medicaldata/LJData/SR_ana/analysis_res/glm_raw/wCue.glm1.result"
result_path="/home/medicaldata/LJData/SR_ana/analysis_res/glm_raw/rbCue.pb04"
mkdir -p ${result_path}


i=0
for subj in `cat NotNull.txt`
do
    echo $subj is running!
    # 将所有被试的beta转为nfiti格式，并保存在同一个目录中
    
    cd ${ana_path}
    3dAFNItoNIFTI $ana_path/$subj/pb04.$subj.r01.scale+tlrc*
    3dAFNItoNIFTI $ana_path/$subj/pb04.$subj.r02.scale+tlrc*
    3dAFNItoNIFTI $ana_path/$subj/pb04.$subj.r03.scale+tlrc*
#    3dAFNItoNIFTI $ana_path/$subj/pb04.$subj.r04.scale+tlrc*
#    3dAFNItoNIFTI $ana_path/$subj/pb04.$subj.r05.scale+tlrc*
#    3dAFNItoNIFTI $ana_path/$subj/pb04.$subj.r06.scale+tlrc*
    
      mv pb04.$subj.r01.scale.nii ${result_path}/pb04.$subj.r07.scale.nii
      mv pb04.$subj.r02.scale.nii ${result_path}/pb04.$subj.r08.scale.nii
      mv pb04.$subj.r03.scale.nii ${result_path}/pb04.$subj.r09.scale.nii
        
    # 控制并行数目，最多同时运行2个
    i=`expr $i + 1`
    if [ `expr $i % 2` == 0 ];then
        wait
    fi
   
done
echo 'ALL processes is done!'
