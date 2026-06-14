#!/bin/bash

i=0
for subj in `cat NotNull.txt`
#for subj in 030 031
do
    echo $subj is running!
    
    # 调用 proc.sub_001.rbCue.glm1.sh 对每个 subj 进行处理
#     tcsh proc.sub_001.rbCue.rel.irrel.sh $subj &
#     tcsh proc.sub_001.rbCue.choose.tent.sh $subj &
#     tcsh proc.sub_001.rbCue.easyhard.sh $subj &
      tcsh proc.sub_001.rbCue.con.sh $subj &

#tcsh ./bms_code/proc.sub_001.rbcue.glm7.sh $subj &
# tcsh ./bms_code/proc.sub_001.wCue.glm7.sh $subj &
     
#    tcsh proc.sub_001.rbcue.glm1.sh $subj &
#    tcsh proc.sub_001.rbcue.glm2.sh $subj &
#    tcsh proc.sub_001.rbcue.glm3.sh $subj &
#    tcsh proc.sub_001.rbcue.glm4.sh $subj &
#    tcsh proc.sub_001.rbcue.glm5.sh $subj &
#    tcsh ./bms_code/proc.sub_001.rbcue.glm1.sh $subj &
#    tcsh ./bms_code/proc.sub_001.rbcue.glm2.sh $subj &
#    tcsh ./bms_code/proc.sub_001.rbcue.glm3.sh $subj &
#    tcsh ./bms_code/proc.sub_001.rbcue.glm6.sh $subj &
#    tcsh ./bms_code/proc.sub_001.wCue.glm1.sh $subj &
#    tcsh ./bms_code/proc.sub_001.wCue.glm2.sh $subj &
#    tcsh ./bms_code/proc.sub_001.wCue.glm3.sh $subj &
#    tcsh ./bms_code/proc.sub_001.wCue.glm6.sh $subj &


    
    # 控制并行数目，最多同时运行2个
    i=`expr $i + 1`
    if [ `expr $i % 2` == 0 ];then
        wait
    fi
   
done
echo 'ALL processes is done!'
