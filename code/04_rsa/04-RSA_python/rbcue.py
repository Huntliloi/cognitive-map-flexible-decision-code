# %% load toolbox
from typing import List, Any, Union
import rsatoolbox
import nibabel
import numpy as np
import matplotlib.pyplot as plt

# %% load and filter data
# 对于每个被试的操作，并某个特定ROI的神经RDM
    data = nibabel.load(
        "/home/medicaldata/LJData/SR_ana/analysis_res/rsa/rbCue/stats."+subj+"_REML.nii").get_fdata()  # x,y,z,102
    # 筛选有用的 sub-brick RedFace1-16 + BlueFace1-16
    data = data[..., 1:103:3].squeeze()  # x,y,z,34
    data = np.concatenate((data[..., 0:26], data[..., 28:]), axis=3)  # x,y,z,32
    print(f"data shape is {data.shape}")

# filter data within ROI
# load ROI
mask = np.array(nibabel.load("/home/medicaldata/LJData/SR_ana/analysis_res/rsa/Left_EC.nii.gz").get_fdata(),
                dtype=bool)  # x,y,z
print(f"mask shape is {mask.shape}")

# 在全脑的数据中筛选出ROI部分的beta
rsadata = data[mask, :].T  # (n_roi_voxels,32 )转置后为（32,n_roi_voxels）
print(f"rsadata shape is {rsadata.shape}")

# add condition label
obs = {
    "cond":
        ['RedFace_1', 'RedFace_10', 'RedFace_11', 'RedFace_12', 'RedFace_13',
         'RedFace_14', 'RedFace_15', 'RedFace_16',
         'BlueFace_1', 'BlueFace_10', 'BlueFace_11', 'RedFace_2', 'BlueFace_12',
         'BlueFace_13', 'BlueFace_14', 'BlueFace_15',
         'BlueFace_16', 'BlueFace_2', 'BlueFace_3', 'BlueFace_4', 'BlueFace_5',
         'BlueFace_6', 'RedFace_3', 'BlueFace_7',
         'BlueFace_8', 'BlueFace_9', 'RedFace_4', 'RedFace_5',
         'RedFace_6', 'RedFace_7', 'RedFace_8', 'RedFace_9']
}

EC_l_data = rsatoolbox.data.Dataset(measurements=rsadata, obs_descriptors=obs)

# calculate the neuro-rdm
EC_l_rdm_subj = rsatoolbox.rdm.calc_rdm(dataset=EC_l_data,
                                        descriptor="cond",
                                        method="correlation")
