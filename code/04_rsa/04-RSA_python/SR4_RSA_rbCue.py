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
    for run in ["rbCue"]:
        # for run in ["rbCue", "wCue"]:
        # 加载subj的beta数据
        data = load(f'/home/medicaldata3/LJData/rsa/{run}/stats.{subj_name}_REML.nii').get_fdata()
        data = np.nan_to_num(data)
        # 筛选有用的 sub-brick RedFace1-16 + BlueFace1-16
        data = data[..., 1:103:3].squeeze()  # x,y,z,34
        data = np.concatenate((data[..., 0:26], data[..., 28:]), axis=3)  # x,y,z,32

        # 加载ROI
        # mapROI
        # roi_list = ["EC_L", "EC_R", "Hippocampus_L","Hippocampus_R", "vmPFC", "OFC_L", "OFC_R"]
        # parkROI
        # roi_list = ["ECl", "ECr", "HCl", "HCr", "mPFC", "M1l", "M1r"]
        # roi_list = ["ECl", "ECr", "HCl", "HCr", "mPFC", "M1l", "M1r"]
        # roi_list = ["chirrel_MFG_r", "chirrel_precuences", "chrel_Putamen_l", "unrel_MFG_l",
        #             "D_IFG_l", "D_insula_r", "D_IPL_l", "D_precentral_l", "D_Precuneus_l",
        #             "F1rel_IPL_l", "F2rel_precnetral_l", "I_precentral_l", "unrel_IFG_l", "unrel_IPL_l"]
        roi_list = ["Amyl", "Amyr", "ECl", "ECr", "HCl", "HCr", "mPFC"]
        roi_masks = [
            np.array(load(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/{roi}.nii').get_fdata(),
                     dtype=bool)
            for roi in roi_list]
        # 循环控制在4个ROI上进行RSA
        for i in range(len(roi_list)):
            # 记录ROI名，用于数据保存
            roi_name = roi_list[i]
            # 取出ROI的数据
            roi_data = data[roi_masks[i], :].T  # (n_roi_voxels,32 )转置后为（32,n_roi_voxels）
            # add condition label
            obs = {
                "cond":
                    ['RedFace_1', 'RedFace_10', 'RedFace_11', 'RedFace_12', 'RedFace_13',
                     'RedFace_14', 'RedFace_15', 'RedFace_16', 'BlueFace_1', 'BlueFace_10',
                     'BlueFace_11', 'RedFace_2', 'BlueFace_12', 'BlueFace_13', 'BlueFace_14',
                     'BlueFace_15', 'BlueFace_16', 'BlueFace_2', 'BlueFace_3', 'BlueFace_4',
                     'BlueFace_5', 'BlueFace_6', 'RedFace_3', 'BlueFace_7', 'BlueFace_8', 'BlueFace_9',
                     'RedFace_4', 'RedFace_5', 'RedFace_6', 'RedFace_7', 'RedFace_8', 'RedFace_9']
            }

            # 转化为rsatoolbox专用运算对象
            rsadata = rsatoolbox.data.Dataset(measurements=roi_data, obs_descriptors=obs)
            # calculate the neuro-rdm计算RDM（当前是计算Pearson相关性）
            rdm = rsatoolbox.rdm.calc_rdm(dataset=rsadata, method="correlation", descriptor="cond")

            # 保存RDM矩阵
            pd.DataFrame(data=rdm.get_matrices().squeeze(), columns=obs["cond"]).to_csv(
                f"/home/medicaldata3/LJData/rsa/{run}/Rdm_{subj_name}_{roi_name}.csv", sep=',',
                header=True, index=False, float_format='%.4f')

            # 保存RDM矩阵上三角
            # pd.DataFrame(rdm.get_matrices().squeeze()[np.triu_indices(rdm.n_cond, 1)]).to_csv(
            #     f"/home/medicaldata/LJData/SR_ana/analysis_res/rsa/{run}/RdmUptri_{subj_name}_{roi_name}.csv", sep=',',
            #     header=False, index=False,
            #     float_format='%.4f')

print("ALL PROCESS IS DONE!")

# 定义用于比较的设计矩阵
# 1-D rank difference  (16红+16蓝)*(16红+16蓝)
# diffRank1d = pd.read_excel(f'/home/medicaldata/LJData/SR_ana/analysis_res/rsa/designMatrix.xlsx',sheet_name = 'diffRank1d',header=None)
# print(diffRank1d.shape)
# Eucli2d = pd.read_excel(f'/home/medicaldata/LJData/SR_ana/analysis_res/rsa/designMatrix.xlsx', sheet_name = 'Eucli2d')
# relContext = pd.read_excel(f'/home/medicaldata/LJData/SR_ana/analysis_res/rsa/designMatrix.xlsx', sheet_name = 'relContext')


# # 加权模型，计算回归系数
# beta = rsatoolbox.model.fitter.fit_optimize(model1, rdm, method="tau-a")
# 保存回归结果
# pd.DataFrame(beta).to_csv(f"./results/beta_{roi_name}_{subj_name}.tsv", sep='\t', header=True, index=True,
#                           float_format='%.4f')

# 计算MDS
# select random seed
# seed = np.random.RandomState(seed=1)
# set the MDS parameter
# embedding = MDS(n_components=2, random_state=seed,
#                dissimilarity='precomputed')
# load rdm_matrix
# rdm_matrix = pd.read_csv("VmPFC_rdm_matrix.csv")

# compute the MDS
# points_coords = embedding.fit_transform(rdm_matrix)

# transform to pands dataframe and save it
# pd.DataFrame(data=points_coords,
#             columns=["x", "y"]).to_csv("Vm_PFC_MDS_points.csv",
#                                        header=True, index=False)


# rsatoolbox.vis.show_MDS()
