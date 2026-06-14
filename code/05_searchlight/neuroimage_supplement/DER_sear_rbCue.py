import rsatoolbox as rb
from brainiak.searchlight.searchlight import Ball, Searchlight
import nibabel
import numpy as np
import pandas as pd
# from pymer4.models import Lmer
from nilearn import image

# 在 searchlight 内部计算 rdm 的函数
def rdm_calc(data):
    # obs = {
    #     "cond":
    #         ['18.43', '26.57', '33.69', '45', '56.31', '63.43', '108.43', '116.57', '123.69',
    #          '135', '146.31', '153.43', '161.57', '198.43', '206.57', '213.69', '225',
    #          '236.31', '243.43', '251.57', '288.43', '296.57', '303.69', '315', '326.31',
    #          '333.43', '341.57']
    # }
    obs = {
        "cond":
            ['0.3217505', '0.4636476', '0.5880026', '0.7853981', '0.9827937', '1.1071487', '1.8925468',
             '2.0344439', '2.1587989', '2.3561944', '2.5535900', '2.6779450', '2.8198420', '3.4633432',
             '3.6052402', '3.7295952', '3.9269908', '4.1243863', '4.2487413', '4.3906384', '5.0341395',
             '5.1760365', '5.3003915', '5.4977871', '5.6951827', '5.8195376', '5.9614347'

             ]
    }
    rb_data = rb.data.Dataset(data, obs_descriptors=obs)
    rb_rdm = rb.rdm.calc_rdm(rb_data, descriptor="cond", method="correlation")

    return rb_rdm
# 在每个 searchlight 上要运行的函数
def sl_func(dat, msk, myrad, bcast_var):
    """
    searchlight function : 在每个 searchlight 上要运行的函数

    params:
        dat       : 即 "sl.distribute([data], mask)" 中的 [data]
        msk       : 这个 searchlight 上要运行的函数
        myrad     : 没用到
        bcast_var : 需要在每个 searchlight 中共享的信息，即 "sl.broadcast(broadcast)" 中的 broadcast，
                    比如 rsa 或者 mvpa 中数据的标签，
                    注：这个不是必须的，如果没有需要共享的信息，连 "sl.broadcast(broadcast)" 都可以不调用
    """

    # bcast_var  # 提取共享信息,
    # 无论做什么操作，这部分基本必有
    ###############################################
    r=[]
    for data in dat:
        sl_data = data[msk, :].T  # 提取出这个 searchlight 的数据
        rdm = rdm_calc(sl_data)
        # 判断sl_data数据是否为空
        if np.all(np.isnan(rdm.dissimilarities)):
            r.append(0)
            # print(r)
        else:
            # r.append(rb.inference.eval_fixed(models=bcast_var, data=rdm, method="tau-a").evaluations[0, 0, 0])
            r.append(rb.inference.evaluate.compare(bcast_var, rdm, method="corr"))
    return r

# Do Searchlight
def do_searchlight(data, mask, broadcast):
    """
    do searchlight

    params:
        data: single subject data ,shape = (x, y, z, n_cond)
        mask: searchlight search region
        broadcast: all process shared message

    return:
        sl_result: np.array, shape = (x, y, z)
    """
    print("### Step3.1 construct searchlight ###")
    sl = Searchlight(sl_rad=3, shape=Ball)
    print("### Step3.2 distribute data to searchlight ###")
    sl.distribute(data, mask)
    print("### Step3.3 distribute shared data to searchlight ###")
    sl.broadcast(broadcast)
    print("### Step3.4 run searchlight analysis ###")
    sl_result = sl.run_searchlight(sl_func, pool_size=40)
    print("Step3.5 searchlight compute finished!")
    return sl_result
# 模型列向量转为RDM
def model(matrix_utri):
    moel_rdm = rb.rdm.RDMs(matrix_utri)
    model = rb.model.ModelFixed('utriRDM', moel_rdm)
    return model

# 投射p值至MNI
def makeNifti(modelMask, para):
    """
    该函数用于为mask赋值
    :param maskOld: 提供原始放射矩阵和头文件的nifti文件，即最后需要将参数展示在什么nifti文件上
    :param para: 需要overlay的参数列表
    :return: 一个包含参数的新nifti文件
    """
    # 加载一个用于填充数据的空坐标模板，用其仿射矩阵与头文件
    X_scaled = para
    maskdata = modelMask.get_fdata()
    NiftiNew = np.zeros(maskdata.shape)
    NiftiNew[maskdata == 1] = X_scaled
    # 生成新的nifti文件
    new_img = image.new_img_like(modelMask, NiftiNew)
    return new_img

if __name__ == "__main__":
    subj_list = ["001", "002", "003", "004", "006", "007", "009", "010", "011", "015", "017", "018",
                 "019", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031"]
    # subj_list = ["001"]
    mask = np.array(nibabel.load(f'/home/medicaldata3/LJData/rsa/dire.ttest/MNI_mask.nii').get_fdata(),
                    dtype=bool)
    broadcast = model(
        np.loadtxt(open(f'/home/medicaldata/LJData/SR_ana/analysis_res/DerModel/Uptri_du_rbCueModel-6fold.csv', "rb"),
                   delimiter=","))
    models = [broadcast]
    theta = [None] * len(models)
    for k, model in enumerate(models):
        rdm_pred = model.predict_rdm(theta=theta[k])

    for subj in subj_list:
        data = [nibabel.load(
            f'/home/medicaldata3/LJData/rsa/rbCue.rsa_direction/stats.{subj}_REML.nii').get_fdata().squeeze()[...,
                1:81:3]]

        # 执行searchlight操作并计算kendall系数 broadcast第一行为模型RDM，从第二个数据后为Nperm的结果
        searchlight_result = do_searchlight(data, mask, rdm_pred)
        print(f'Step3: subNum: {subj} regress calculate Done!')
        searchlight_result_transformed = [np.array([item]) if np.shape(item) == () else item for item in
                                          searchlight_result[mask]]
        # Result = np.squeeze(np.array(list(searchlight_result_transformed)))
        Result = [arr.item() if isinstance(arr, np.ndarray) else arr for sublist in searchlight_result_transformed for arr in
                          sublist]
        xyz = np.column_stack(np.where(mask))
        modelmask = image.load_img(f'/home/medicaldata3/LJData/rsa/dire.ttest/MNI_mask.nii')
        niftiNew = makeNifti(modelmask, Result)
        niftiNew.to_filename(f'/home/medicaldata3/LJData/rsa/rbCue.rsa_direction/du/corr/corr.fold6.{subj}.nii')
        print(f'Step4: beta.{subj} saved done')