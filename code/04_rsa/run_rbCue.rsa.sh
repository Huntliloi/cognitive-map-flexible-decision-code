#!/bin/bash

i=0
for subj in `cat NotNull.txt`
#for subj in 007
do
    echo $subj is running!
    
    # 调用 proc.sub_001.rbCue.glm1.sh 对每个 subj 进行处理
#    tcsh ./bms_code/proc.sub_001.rbCue.rsa.A.sh $subj &
#    tcsh ./bms_code/proc.sub_001.wCue.rsa.A.sh $subj &
    tcsh proc.sub_001.rbCue.rsa.dire.sh $subj &
#    tcsh proc.sub_001.rbCue.rsa.dire.du.sh $subj &
    # 控制并行数目，最多同时运行2个
    i=`expr $i + 1`
    if [ `expr $i % 2` == 0 ];then
        wait
    fi
   
done
echo 'ALL processes is done!'
