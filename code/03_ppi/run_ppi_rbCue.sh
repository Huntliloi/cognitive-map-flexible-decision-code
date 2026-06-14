#!/bin/bash

########################## post ##############################
 i=0
for subj in `cat NotNull.txt`
 #for subj in 007 009 010 011 015 017 018 019 021 022 023 024 025 026 027 028 029 030 031
 do
     echo $subj is running!
     tcsh ./PPI_scripts/sr4/s1.PPI_rbCue_cue.sh $subj &
#      tcsh ./PPI_scripts/sr4/s1.PPI_rbCue.sh $subj &
#     tcsh ./PPI_scripts/sr4/s1.PPI_wCue.sh $subj &
     # 控制并行数目，最多同时运行2个
     i=`expr $i + 1`
     if [ `expr $i % 2` == 0 ];then
         wait
     fi
 done
 echo 'PPI Done!'

