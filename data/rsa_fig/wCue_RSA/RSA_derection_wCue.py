### SR4正式实验分析 data analysis ###

from nibabel import load
import rsatoolbox
import numpy as np
# from SR4_rsaModel import model1, model2
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import MDS

# 被试列表
subj_list = ["001", "002", "003", "004", "006", "007", "009", "010", "011", "015", "017", "018",
             "019", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031"]

# 循环计算每个被试的结果
for subj_name in subj_list:
    for run in ["wCue.rsa_direction"]:
        # for run in ["rbCue.rsa.derection", "wCue.rsa.derection"]:
        # 加载subj的beta数据
        data = load(f'/home/medicaldata3/LJData/rsa/{run}/stats.{subj_name}_REML.nii').get_fdata()
        data = np.nan_to_num(data)
        # 筛选有用的 sub-brick 弧度值
        data = data[..., 1:39:3].squeeze()  # x,y,z,13

        # 加载ROI
        # mapROI
        # roi_list = ["EC_L", "EC_R", "Hippocampus_L","Hippocampus_R", "vmPFC", "OFC_L", "OFC_R"]
        # parkROI
        # roi_list = ["ECl", "ECr", "HCl", "HCr", "mPFC", "Amyl", "Amyr"]
        roi_list = ["Clust_ECl", "Clust_ECr", "Clust_HCr","Clust_IPLl","Clust_mPFCr"]
        # /home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/{roi}.nii
        roi_masks = [
            np.array(load(f'/home/medicaldata3/LJData/rsa/dire.ttest/sr4.dire/{roi}.nii').get_fdata(),
                     dtype=bool)
            for roi in roi_list]
        # 循环控制在4个ROI上进行RSA
        for i in range(len(roi_list)):
            # 记录ROI名，用于数据保存
            roi_name = roi_list[i]
            # 取出ROI的数据
            roi_data = data[roi_masks[i], :].T  # (n_roi_voxels,32 )转置后为（32,n_roi_voxels）
            # add condition label  in du
            # obs = {
            #     "cond":
            #         ['18.43', '26.57', '33.69', '45', '63.43', '71.57', '198.43',
            #          '206.57', '213.69', '225', '236.31', '243.43', '251.57']
            # }

            # add condition label  in hudu
            obs = {
                "cond":
                    ['0.3217505', '0.4636476', '0.5880026', '0.7853981', '1.1071487', '1.2490457', '3.4633432',
                     '3.6052402', '3.7295952', '3.9269908', '4.1243863', '4.2487413', '4.3906384']
            }

            # 转化为rsatoolbox专用运算对象
            rsadata = rsatoolbox.data.Dataset(measurements=roi_data, obs_descriptors=obs)
            # calculate the neuro-rdm计算RDM（当前是计算Pearson相关性）
            rdm = rsatoolbox.rdm.calc_rdm(dataset=rsadata, method="euclidean", descriptor="cond")
            # rdm.dissimilarities = np.where(rdm.dissimilarities > 1, 2 - rdm.dissimilarities,
            #                                   rdm.dissimilarities)

            # 保存RDM矩阵
            pd.DataFrame(data=rdm.get_matrices().squeeze(), columns=obs["cond"]).to_csv(
                f"/home/medicaldata3/LJData/rsa/{run}/Rdm_{subj_name}_{roi_name}.csv", sep=',',
                header=True, index=False, float_format='%.4f')
            #
            # # 保存RDM矩阵上三角
            # pd.DataFrame(rdm.get_matrices().squeeze()[np.triu_indices(rdm.n_cond, 1)]).to_csv(
            #     f"/home/medicaldata3/LJData/rsa/{run}/RdmUptri_{subj_name}_{roi_name}.csv", sep=',',
            #     header=False, index=False,
            #     float_format='%.4f')

print("ALL PROCESS IS DONE!")
