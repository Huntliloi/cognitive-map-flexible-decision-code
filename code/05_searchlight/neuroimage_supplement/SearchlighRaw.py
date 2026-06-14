import rsatoolbox as rb
from brainiak.searchlight.searchlight import Ball, Searchlight
import nibabel
import numpy as np
from scipy import stats
import pandas as pd

# 在 searchlight 内部计算 rdm 的函数
def rdm_calc(data):
    obs = {
        "cond":
            ['108.4349', '116.5651', '123.6901', '135', '146.3099', '153.4349',
             '161.5651', '18.4349', '198.434', '206.5651', '213.6901', '225',
             '236.3099', '243.4349', '251.5651', '26.5651', '288.4349', '296.5651',
             '303.6901', '315', '326.3099', '333.4349', '33.6901', '341.5651',
             '45', '56.3099', '63.4349']
    }
    rb_data = rb.data.Dataset(data, obs_descriptors=obs)
    rb_rdm = rb.rdm.calc_rdm(rb_data, descriptor="cond", method="mahalanobis")

    return rb_rdm

def sl_func(dat, msk, bcast_var):
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
        r.append(rb.inference.eval_fixed(models=bcast_var, data=rdm, method="corr").evaluations[0,0,0])
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

if __name__ == "__main__":
    subj_list = ["001", "002", "003", "004", "006", "007", "009", "010", "011", "015", "017", "018",
                 "019", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031"]

    data = [nibabel.load(
        f'/home/medicaldata3/LJData/rbCue.rsa.derection/stats.{subj}_REML.nii').get_fdata().squeeze()[..., 1:81:3]
            for subj in subj_list]

    mask = np.array(nibabel.load(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/HCl.nii').get_data(),
                    dtype=bool)

    broadcast = model(
        np.loadtxt(open(f'/home/medicaldata/LJData/SR_ana/analysis_res/DerModel/DERrbCueModel-4fold.csv', "rb"),
                   delimiter=","))

    result = do_searchlight(data, mask, broadcast)

    corMask = []
    Mean = []
    for i in range(0, result[mask].size, 1):
        corMask.append(stats.ttest_ind(a=result[mask][i], b=np.zeros(24), equal_var=False))
        Mean.append(np.mean(result[mask][i]))


    corData=[]
    for i in range(0, result[mask].size, 1):
        corData.append([i, Mean[i], corMask[i].statistic, corMask[i].pvalue])

        pd.DataFrame(data=corData, columns=["No", "corr", "t-value", "p-value"]).to_csv(
            f"/home/medicaldata3/LJData/rbCue.rsa.derection/rbCue.4fold.HCl.csv", sep=',',
            header=True, index=False, float_format='%.4f')

    # for i in range(0, result[mask].size, 1):
    #     if np.array(corMask[i].pvalue < 0.05) == True:
    #         print('体素序号：',i)
    #         print('该体素在所有被试中的平均相关值：',Mean[i])
    #         print('该体素在所有被试中的t值：', corMask[i].statistic)
    #         print('该体素在所有被试中的p值：', corMask[i].pvalue)
