#!/bin/bash

i=0
for subj in `cat NotNull.txt`
do
    echo $subj is running!
    
    # 调用 proc.sub_001.rbCue.glm1.sh 对每个 subj 进行处理
    tcsh ./old_proc/proc.sub_001.face.glm.sh $subj &
    
    # 控制并行数目，最多同时运行2个
    i=`expr $i + 1`
    if [ `expr $i % 2` == 0 ];then
        wait
    fi
   
done
echo 'ALL processes is done!'
