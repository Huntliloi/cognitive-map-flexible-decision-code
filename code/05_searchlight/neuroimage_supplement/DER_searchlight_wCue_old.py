import rsatoolbox as rb
from brainiak.searchlight.searchlight import Ball, Searchlight
import nibabel
import numpy as np
import pandas as pd
from pymer4.models import Lmer
from nilearn import image

# 在 searchlight 内部计算 rdm 的函数
def rdm_calc(data):
    obs = {
        "cond":
            ['18.4349', '26.5651', '33.6901', '45', '56.3099', '63.4349', '71.5651',
             '198.4349', '206.5651', '213.6901', '225', '243.4349', '251.5651']
    }
    rb_data = rb.data.Dataset(data, obs_descriptors=obs)
    rb_rdm = rb.rdm.calc_rdm(rb_data, descriptor="cond", method="correlation")
    rb_rdm.dissimilarities = np.where(rb_rdm.dissimilarities > 1, -1 - (1 - rb_rdm.dissimilarities),rb_rdm.dissimilarities)
    return rb_rdm

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
    trirdm = np.empty((0, 2))
    for data in dat:
        sl_data = data[msk, :].T  # 提取出这个 searchlight 的数据
        rdm = rdm_calc(sl_data)
        modified_matrix = np.column_stack((rdm.dissimilarities.squeeze().T, bcast_var.rdm.reshape(-1, 1)))
        trirdm = np.vstack((trirdm, modified_matrix))
        # r.append(rb.inference.eval_fixed(models=bcast_var, data=rdm, method="corr").evaluations[0, 0, 0])
    id = np.repeat(np.arange(1, 25), rdm.dissimilarities.squeeze().T.shape[0])
    trirdm = np.column_stack((id, trirdm))
    df = pd.DataFrame(trirdm)
    df.columns = ['id', 'correlation', 'models']
    dffit = Lmer(formula="correlation ~ models + (1| id)", data=df)
    dffit.fit()
    res = dffit.coefs.iloc[1]
    return res

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
    print("### construct searchlight ###")
    sl = Searchlight(sl_rad=3, shape=Ball)
    print("### distribute data to searchlight ###")
    sl.distribute(data, mask)
    print("### distribute shared data to searchlight ###")
    sl.broadcast(broadcast)
    print("### run searchlight analysis ###")
    sl_result = sl.run_searchlight(sl_func, pool_size=40)
    print("searchlight compute finished!")
    return sl_result

def model(matrix_utri):
    moel_rdm = rb.rdm.RDMs(matrix_utri)
    model = rb.model.ModelFixed('utriRDM',moel_rdm)
    return model

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

    data = [nibabel.load(
        f'/home/medicaldata3/LJData/wCue.rsa.derection/stats.{subj}_REML.nii').get_fdata().squeeze()[..., 1:39:3]
            for subj in subj_list]

    mask = np.array(nibabel.load(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/brainMaskwCue.nii').get_fdata(),
                    dtype=bool)

    broadcast = model(
        np.loadtxt(open(f'/home/medicaldata/LJData/SR_ana/analysis_res/DerModel/DERwCueModel-6fold.csv', "rb"),
                   delimiter=","))

    result = do_searchlight(data, mask, broadcast)

    corData = np.array(list(result[mask]))
    xyz = np.column_stack(np.where(mask))
    corData = np.column_stack((xyz, corData))
    print('corData done')

    # 将p值写入到每个体素上
    modelmask = image.load_img(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/brainMaskwCue.nii')
    par = corData[:, 9]
    niftiNew = makeNifti(modelmask, par)
    niftiNew.to_filename(f'/home/medicaldata3/LJData/wCue.rsa.derection/wCue.6fold.brain.nii')
    print('newNifit saved done')

    ## 保存 p <0.05 的值
    corDataPval = np.where(corData[:, 9] > 0.05, 0, corData[:, 9])
    niftiNew = makeNifti(modelmask, corDataPval)
    niftiNew.to_filename(f'/home/medicaldata3/LJData/wCue.rsa.derection/wCue.6fold.brainP.nii')

    ## 保存数据
    # pd.DataFrame(data=corData,
    #              columns=["x", "y", "z", "estimate", "2.5_CI", "97.5_CI", "std.error", "DF", "t-value", "p-value",
    #                       "Sig"]).to_csv(f"/home/medicaldata3/LJData/wCue.rsa.derection/wCue.6fold.brain.csv",
    #                                      sep=',',
    #                                      header=True, index=False, float_format='%.4f')
    print('csv done')

