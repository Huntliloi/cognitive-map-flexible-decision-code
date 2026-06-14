import rsatoolbox as rb
from brainiak.searchlight.searchlight import Ball, Searchlight
import nibabel
import numpy as np
import pandas as pd
# from pymer4.models import Lmer
from nilearn import image
import scipy.stats as stats
# 标准化
from scipy.stats import zscore
# 多元线性回归
from sklearn.linear_model import LinearRegression
# 计算肯德尔系数 准备画图的命令——rb.rdm.compare_kendall_tau()

# 在 每个searchlight 内部计算 rdm 的函数
def rdm_calc(data):
    obs = {
        "cond":
            ['Face_10', 'Face_11', 'Face_12', 'Face_13', 'Face_14', 'Face_15',
             'Face_2', 'Face_3', 'Face_4', 'Face_5', 'Face_6', 'Face_7', 'Face_8', 'Face_9']
    }
    rb_data = rb.data.Dataset(data, obs_descriptors=obs)
    rb_rdm = rb.rdm.calc_rdm(rb_data, descriptor="cond", method="euclidean")
    # rb_rdm.dissimilarities = np.where(rb_rdm.dissimilarities > 1, -1 - (1 - rb_rdm.dissimilarities),
    #                                   rb_rdm.dissimilarities)
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
    # 按照一个searchlight执行一个这样的操作，22个被试*1001次比较

    for i, data in enumerate(dat):
        r = []
        for i, data in enumerate(dat):
            sl_data = data[msk, :].T  # 提取出这个 searchlight 的数据
            rdm = rdm_calc(sl_data)   # 计算这个searchlight的rdm
        r.append(rb.rdm.compare_kendall_tau(bcast_var, rdm))
        print(f"Step3.4.1:  subNum:{i} compare kendall done!")
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
# 生成RDM格式的矩阵
def makeRDM(matrix2D):
    """
    该函数用于生成RDMs格式的矩阵,便于进行kendall系数的计算
    :param mattix2D: 输入一个2D的RDM矩阵
    :return: 返回一个RDMs
    """
    matrix = matrix2D[np.newaxis, :]
    matrix = rb.rdm.rdms.RDMs(matrix,
                              pattern_descriptors={"cond":
                                                       ['Face_10', 'Face_11', 'Face_12', 'Face_13', 'Face_14',
                                                        'Face_15', 'Face_2', 'Face_3', 'Face_4', 'Face_5',
                                                        'Face_6', 'Face_7', 'Face_8', 'Face_9']})
    return matrix


if __name__ == "__main__":
    subj_list = ["001", "002", "003", "004", "006", "007", "009", "010", "011", "015", "017", "018",
                 "019", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031"]

    mask = np.array(nibabel.load(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/brainMaskwCue.nii').get_fdata(),
                    dtype=bool)
    # 导入modelRDM
    # broadcast = makeRDM(np.loadtxt(open(f'/home/medicaldata/LJData/SR_ana/analysis_res/sr3RSAmodel/E.csv', "rb"),
    #                                delimiter=","))

    # 分别读入七个模型并按照RDMs的格式累加
    modelRDMs = np.loadtxt(open(f'/home/medicaldata3/LJData/rsa/wCue/modelRDM_wCue.csv', "rb"),
                                   delimiter=",")
    # broadcast_raw = np.empty(modelRDMs.shape)
    # for i in range(7):
    #     broadcast[:,i] = zscore(modelRDMs[:, i], nan_policy='omit')
    # grid
    # broadcast = makeRDM(modelRDMs[:, 0])
    # diag
    broadcast = makeRDM(modelRDMs[:, 1])


    print('Step1: setting rawdata and modelRDMs done!')

    for subj in subj_list:
        data = [nibabel.load(f'/home/medicaldata3/LJData/rsa/wCue/stats.{subj}_REML.nii').get_fdata().squeeze()[..., 4:45:3]]

    # 执行searchlight操作并计算kendall系数 broadcast第一行为模型RDM，从第二个数据后为Nperm的结果
        searchlight_result = do_searchlight(data, mask, broadcast)
        print('Step3: regress calculate Done!')

        Result = np.squeeze(np.array(list(searchlight_result[mask])))
        xyz = np.column_stack(np.where(mask))
        modelmask = image.load_img(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/brainMaskwCue.nii')
        niftiNew = makeNifti(modelmask, Result)
        niftiNew.to_filename(f'/home/medicaldata3/LJData/rsa/wCue/tau_grid/tau.diag.{subj}.nii')
        print(f'Step4: beta.{subj} saved done')