#!/bin/bash

########################## post ##############################
 i=0
 for subj in `cat NotNull.txt`
# for subj in 030 031 
 do
     echo $subj is running!
#     tcsh ./PPI_scripts/sr4/s1.PPI_rbCue.sh $subj &
     tcsh ./PPI_scripts/sr4/s1.PPI_wCue.sh $subj &
#      tcsh ./PPI_scripts/sr4/s1.PPI_rbCue_cue_HCr.sh $subj &
     # 控制并行数目，最多同时运行2个
     i=`expr $i + 1`
     if [ `expr $i % 2` == 0 ];then
         wait
     fi
 done
 echo 'PPI Done!'

