#!/bin/bash
# Copyright (c) 2023 Institute of Health and Medical Technology, Hefei Institutes of Physical Science, CAS, All Rights Reserved.
# @Time     : 2024/9.5
# @Author   : J.L
# @Email    : jennieliu@mail.ustc.edu.cn
# @Reference: None
# @FileName : s2.3danova2.sh
# @Software : Shell; VS Code; Ubuntu 18.04.5 LTS (GNU/Linux 5.4.0-59-generic x86_64)
# @Hardware : Intel Xeon 6258R 2.7G 28C*2
# @Version  : V1.0.0 - J.L: 2024.9.5
# @Brief    : PPI组分析：ANOVA


subj_dirs=/home/medicaldata3/LJData/rsa/PPI_ana/rbCue.ppi.cue.result
output_dir=/home/medicaldata3/LJData/rsa/PPI_ana/rbCue.ppi.cue.group
# find $output_dir -type f -name "group.PPI.*.nii.gz" -exec rm {} \;
seed=HCl

echo '----------------------------' ANOVA: "$seed" '----------------------------'
# one factor: task type (5 levels)
3dANOVA -levels 2                                                                            \
    -dset 1 "$subj_dirs/019/PPI.$seed.stats.019+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/019/PPI.$seed.stats.019+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/028/PPI.$seed.stats.028+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/028/PPI.$seed.stats.028+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/002/PPI.$seed.stats.002+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/002/PPI.$seed.stats.002+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/003/PPI.$seed.stats.003+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/003/PPI.$seed.stats.003+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/031/PPI.$seed.stats.031+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/031/PPI.$seed.stats.031+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/006/PPI.$seed.stats.006+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/006/PPI.$seed.stats.006+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/015/PPI.$seed.stats.015+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/015/PPI.$seed.stats.015+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/026/PPI.$seed.stats.026+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/026/PPI.$seed.stats.026+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/004/PPI.$seed.stats.004+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/004/PPI.$seed.stats.004+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/011/PPI.$seed.stats.011+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/011/PPI.$seed.stats.011+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/021/PPI.$seed.stats.021+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/021/PPI.$seed.stats.021+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/018/PPI.$seed.stats.018+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/018/PPI.$seed.stats.018+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/024/PPI.$seed.stats.024+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/024/PPI.$seed.stats.024+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/025/PPI.$seed.stats.025+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/025/PPI.$seed.stats.025+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/009/PPI.$seed.stats.009+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/009/PPI.$seed.stats.009+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/022/PPI.$seed.stats.022+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/022/PPI.$seed.stats.022+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/029/PPI.$seed.stats.029+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/029/PPI.$seed.stats.029+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/007/PPI.$seed.stats.007+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/007/PPI.$seed.stats.007+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/027/PPI.$seed.stats.027+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/027/PPI.$seed.stats.027+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/010/PPI.$seed.stats.010+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/010/PPI.$seed.stats.010+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/023/PPI.$seed.stats.023+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/023/PPI.$seed.stats.023+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/030/PPI.$seed.stats.030+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/030/PPI.$seed.stats.030+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/017/PPI.$seed.stats.017+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/017/PPI.$seed.stats.017+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -dset 1 "$subj_dirs/001/PPI.$seed.stats.001+tlrc.HEAD[PPI.red#0_Coef]"   \
    -dset 2 "$subj_dirs/001/PPI.$seed.stats.001+tlrc.HEAD[PPI.blue#0_Coef]"   \
    -ftr Tasks -mean 1 PPI_mean:red -mean 2 PPI_mean:blue                 \
    -diff 2 1 PPI_diff:redvsblue                     \
    -bucket $output_dir/group.PPI.$seed.nii.gz

    # for roimask in roi_mask/roi_mask*.nii.gz; do
    #     {
    #         roi=$(echo $roimask | cut -d'.' -f2)
    #         if [[ $sd != $roi ]]; then
    #            3dcalc -a $output_dir/group.PPI.$seed.nii.gz -b $roimask \
    #                   -expr "a*step(b)" -prefix $output_dir/group.PPI.$seed.bm.$roi.nii.gz -overwrite
    #         fi
    #     }
    #    done