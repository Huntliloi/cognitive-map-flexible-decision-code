import rsatoolbox as rb
from brainiak.searchlight.searchlight import Ball, Searchlight
import nibabel
import numpy as np
import pandas as pd
# from pymer4.models import Lmer
from nilearn import image
import scipy.stats as stats
# 计算肯德尔系数 准备画图的命令——rb.rdm.compare_kendall_tau()

# 在 searchlight 内部计算 rdm 的函数
def rdm_calc(data):
    obs = {
        "cond":
            ['RedFace_1', 'RedFace_10', 'RedFace_11', 'RedFace_12', 'RedFace_13',
             'RedFace_14', 'RedFace_15', 'RedFace_16', 'RedFace_2', 'RedFace_3',
             'RedFace_4', 'RedFace_5', 'RedFace_6', 'RedFace_7', 'RedFace_8', 'RedFace_9']
    }
    rb_data = rb.data.Dataset(data, obs_descriptors=obs)
    rb_rdm = rb.rdm.calc_rdm(rb_data, descriptor="cond", method="mahalanobis")

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
    q = []
    for i, data in enumerate(dat):
        sl_data = data[msk, :].T  # 提取出这个 searchlight 的数据
        rdm = rdm_calc(sl_data)
        r = []
        for n in range(len(bcast_var)):
            r.append(rb.rdm.compare_kendall_tau(bcast_var[n], rdm))
        q.append(r)
        print(f"Step3.4.1:  subNum:{i}   kendall{n} compare kendall done!")
    T0 = [np.array(item[0]) - np.mean(item[1:], axis=0) for item in q]
    # p_value = stats.wilcoxon(T0, alternative='greater')
    # test_p = p_value.pvalue
    # T0_mean = np.mean(T0, axis=0)
    # T0_SEM = np.std(T0, axis=0) / len(T0)
    # wilxconResult = np.array((T0_mean[0, 0], T0_SEM[0, 0], test_p[0, 0]))
    return T0
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
                                                       ['RedFace_1', 'RedFace_10', 'RedFace_11', 'RedFace_12', 'RedFace_13',
                                                        'RedFace_14', 'RedFace_15', 'RedFace_16', 'RedFace_2','RedFace_3',
                                                        'RedFace_4', 'RedFace_5', 'RedFace_6', 'RedFace_7', 'RedFace_8',
                                                        'RedFace_9']})
    # matrix.reorder([7, 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15])
    return matrix
# 创建随机矩阵
def EucRDM_factorize(faceRng,Nperm):
    # 生成随机矩阵
    Xperm = np.random.randint(1, 5, (len(faceRng), Nperm))
    Yperm = np.random.randint(1, 5, (len(faceRng), Nperm))
    E_rdm_perm = []
    D1_rdm_perm = []  # D1为品德维度
    D2_rdm_perm = []  # D2为才能维度
    for n in range(Nperm):
        X0 = Xperm[:, n]
        Y0 = Yperm[:, n]
        I = np.arange(1, len(faceRng) + 1)
        i, j = np.meshgrid(I, I)
        E_rdm_perm_n = np.sqrt((X0[i - 1] - X0[j - 1]) ** 2 + (Y0[i - 1] - Y0[j - 1]) ** 2)
        # E_rdm_perm_n = np.abs(X0[i - 1] - X0[j - 1]) + np.abs(Y0[i - 1] - Y0[j - 1])  # 计算曼哈顿距离
        D1_rdm_perm_n = np.abs(X0[i - 1] - X0[j - 1])
        D2_rdm_perm_n = np.abs(Y0[i - 1] - Y0[j - 1])
        E_rdm_perm.append(E_rdm_perm_n)
        D1_rdm_perm.append(D1_rdm_perm_n)
        D2_rdm_perm.append(D2_rdm_perm_n)

    return E_rdm_perm, D1_rdm_perm, D2_rdm_perm
# 将随机矩阵修改为RDMs格式，并与模型RDM累加
def do_randomRDM(broadcast, nPerm):
    [E, D1, D2] = EucRDM_factorize([1, 10, 11, 12, 13, 14, 15, 16, 2, 3, 4, 5, 6, 7, 8, 9], nPerm)
    for n in range(nPerm):
        E[n] = makeRDM(E[n])
        D1[n] = makeRDM(D1[n])
        D2[n] = makeRDM(D2[n])
    # 合并所有model项目
    broad_E = [broadcast] + E
    broad_red = [broadcast] + D1
    broad_blue = [broadcast] + D2
    return broad_E, broad_red, broad_blue

if __name__ == "__main__":
    subj_list = ["001", "002", "003", "004", "006", "007", "009", "010", "011", "015", "017", "018",
                 "019", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031"]
    data0 = [nibabel.load(
        f'/home/medicaldata3/LJData/rsa/rbCue/stats.{subj}_REML.nii').get_fdata().squeeze()[..., 1:103:3]
             for subj in subj_list]
    dataRed = []
    dataBlue = []
    for arr in data0:
        datared = np.concatenate((arr[..., 0:8], arr[..., 11, np.newaxis], arr[..., 22, np.newaxis], arr[..., 28:]),
                                 axis=3)  # x,y,z,16  # 取rCue
        datablue = np.concatenate((arr[..., 8:11], arr[..., 12:22], arr[..., 23:26]),
                                  axis=3)  # x,y,z,16  # 取bCue
        dataRed.append(datared)
        dataBlue.append(datablue)
    #   data[0][...,0].min()

    mask = np.array(nibabel.load(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/brainMeanMaskrb.nii').get_fdata(),
                    dtype=bool)
    # 导入modelRDM
    broadcast = makeRDM(np.loadtxt(open(f'/home/medicaldata/LJData/SR_ana/analysis_res/sr4RSAmodel/E.csv', "rb"),
                                   delimiter=","))
    data = dataRed
    print('Step1: setting done!')


    # 完成searchlight并保存wilcoxon检验的结果
    broadcastE, broadcastred, broadcastblue = do_randomRDM(broadcast, 1000)
    print('Step2:compute the random RDM Done!')

    # 执行searchlight操作并计算kendall系数 broadcast第一行为模型RDM，从第二个数据后为Nperm的结果
    searchlight_result = do_searchlight(data, mask, broadcastE)
    print('Step3: Kendall calculate Done!')

    Result = np.squeeze(np.array(list(searchlight_result[mask])), axis=(2, 3))
    # xyz = np.column_stack(np.where(mask))
    modelmask = image.load_img(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/brainMeanMaskrb.nii')
    # 将结果保存到每个fMRI数据中
    for i in range(len(subj_list)):
        Tau = Result[:, i]
        niftiNew = makeNifti(modelmask, Tau)
        niftiNew.to_filename(f'/home/medicaldata3/LJData/rsa/rbCue/tau/tau.rCue.{subj_list[i]}.E.nii')
        print(f'Step5: tau.{subj_list[i]} saved done')


    # 提取相关值，第一列为平均值，第二列为SEM，第三列为p值
    # wilxconResult = np.array(list(searchlight_result[mask]))
    # xyz = np.column_stack(np.where(mask))
    # wilxconResult = np.column_stack((xyz, wilxconResult))
    # wilxconSelect = wilxconResult[wilxconResult[:, 5] < 0.05]
    # print('Step4: wilxconSelect Done!')
    #
    # # 将p值写入到每个体素上
    # modelmask = image.load_img(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/brainMeanMaskrb.nii')
    # wilcoxon = wilxconResult[:, 5]
    # niftiNew = makeNifti(modelmask, wilcoxon)
    # niftiNew.to_filename(f'/home/medicaldata3/LJData/rsa/rbCue/rCue.brain.D.nii')
    # print('Step5: brain saved done')
    #
    # # 保存 p <0.05 的值
    # wilcoxonPval = np.where(wilxconResult[:, 5] > 0.05, 0, wilxconResult[:, 5])
    # niftiNew = makeNifti(modelmask, wilcoxonPval)
    # niftiNew.to_filename(f'/home/medicaldata3/LJData/rsa/rbCue/rCue.brainP.D.nii')
    # print('Step6: brainP saved done')
    #
    # # 保存数据
    # pd.DataFrame(data=wilxconResult,
    #              columns=["x", "y", "z", "mean", "SEM", "p-value"]).to_csv(
    #     f"/home/medicaldata3/LJData/rsa/rbCue/rCue.brain.D.csv", sep=',',
    #     header=True, index=False, float_format='%.4f')
    #
    # pd.DataFrame(data=wilxconSelect,
    #              columns=["x", "y", "z", "mean", "SEM", "p-value"]).to_csv(
    #     f"/home/medicaldata3/LJData/rsa/rbCue/rCue.brainSelectP.D.csv", sep=',',
    #     header=True, index=False, float_format='%.4f')
    # print('Step7: csv saved done')
