#!/bin/bash

i=0
for subj in `cat NotNull.txt`
#for subj in 030 031
do
    echo $subj is running!
    
    # 调用 proc.sub_001.wCue.glm1.sh 对每个 subj 进行处理
#    tcsh proc.sub_001.wCue.glm1.sh $subj &
#    tcsh proc.sub_001.wCue.glm2.sh $subj &
#    tcsh proc.sub_001.wCue.glm3.sh $subj &
#    tcsh proc.sub_001.wCue.glm4.sh $subj &
#    tcsh proc.sub_001.wCue.glm5.sh $subj &
#    tcsh proc.sub_001.wCue.diagF1F2.sh $subj &
#    tcsh proc.sub_001.wCue.choose.sh $subj &
#    tcsh proc.sub_001.wCue.diagF1F2.tent.sh $subj &
#    tcsh proc.sub_001.wCue.choose.tent.sh $subj &
#      tcsh ./bms_code/proc.sub_001.wCue.glm7.sh $subj &
    tcsh proc.sub_001.wCue.ppi.sh $subj &
    
    # 控制并行数目，最多同时运行2个
    i=`expr $i + 1`
    if [ `expr $i % 2` == 0 ];then
    wait
    fi
   
done
echo 'ALL processes is done!'