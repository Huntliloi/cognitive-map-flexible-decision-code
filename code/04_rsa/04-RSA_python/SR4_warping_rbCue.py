### SR4正式实验分析 data analysis ###

from nibabel import load
import rsatoolbox
import pandas as pd
import numpy as np
import itertools
from collections import defaultdict



# 被试列表
subj_list = ["001", "002", "003", "004", "006", "007", "009", "010", "011", "015", "017", "018",
             "019", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031"]
# subj_list = ["001"]

GRID_MAP = pd.DataFrame({
    'number': range(1, 17),
    'x': np.tile(range(1, 5), 4),
    'y': np.repeat(range(1, 5), 4)

})
GRID_MAP['number'] = (4 * GRID_MAP['y']) + 1 - GRID_MAP['x']
GRID_MAP = GRID_MAP[['number', 'x', 'y']].sort_values(by='number').reset_index(drop=True)


GRID_MAP_LOOKUP = {(row.x, row.y): row.number for index, row in GRID_MAP.iterrows()}
def get_face_num_by_coords(x, y):
    return GRID_MAP_LOOKUP.get((x, y))

all_results = []
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
        roi_list = ["Amyl", "Amyr", "ECl", "ECr", "HCl", "HCr", "mPFC"]
        # roi_list = ["mPFC"]
        # roi_list = ["Amyl", "Amyr", "ECl", "ECr", "HCl", "HCr", "mPFC",
        #             "precuneus", "precuneusl", "precuneusr",
        #             "Insulal", "Insular", "IPLl", "IPLr", "MFGl", "MFGr"]
        roi_masks = [
            np.array(load(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/parkROI/{roi}.nii').get_fdata(),
                     dtype=bool)
            for roi in roi_list]

        # roi_masks = [
        #     np.array(load(f'/home/medicaldata/LJData/SR_ana/analysis_res/rois/BN_atlas/{roi}.nii.gz').get_fdata(),
        #              dtype=bool)
        #     for roi in roi_list]
        # 循环控制在4个ROI上进行RSA
        for i in range(len(roi_list)):
            # 记录ROI名，用于数据保存
            roi_name = roi_list[i]
            print(roi_name)
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
            rdm = rsatoolbox.rdm.calc_rdm(dataset=rsadata, method="euclidean", descriptor="cond")
            neural_rdm = pd.DataFrame(rdm.get_matrices()[0], index=rdm.pattern_descriptors['cond'], columns=rdm.pattern_descriptors['cond'])

            # --- b. 计算 ω_attention (主轴扭曲) ---
            distances_by_d = {
                1: {'relevant': [], 'irrelevant': []},
                2: {'relevant': [], 'irrelevant': []},
                3: {'relevant': [], 'irrelevant': []}
            }

            for d in range(1, 4):
                # 遍历所有可能的起始点
                for y_start in range(1, 5):
                    for x_start in range(1, 5):  # 确保终点x_start+d不超过4
                        start_rel = get_face_num_by_coords(x_start, y_start)
                        end_rel = get_face_num_by_coords(x_start + d, y_start)
                        start_irrel = get_face_num_by_coords(x_start, y_start)
                        end_irrel = get_face_num_by_coords(x_start, y_start + d)
                        # if start_rel is not None and end_rel is not None:
                        #     print(f" rel RedFace_{start_rel}", f"RedFace_{end_rel}")
                        # if start_irrel is not None and end_irrel is not None:
                        #     print(f" irrel RedFace_{start_irrel}", f"RedFace_{end_irrel}")

                        # Red Face: 横向是“相关轴”
                        if start_rel is not None and end_rel is not None:
                            dist_red_horiz = neural_rdm.loc[f"BlueFace_{start_rel}", f"BlueFace_{end_rel}"]
                            distances_by_d[d]['relevant'].append(dist_red_horiz)

                        # Red Face: 纵向是“无关轴”
                        if start_irrel is not None and end_irrel is not None:
                            dist_red_vert = neural_rdm.loc[f"BlueFace_{start_irrel}", f"BlueFace_{end_irrel}"]
                            distances_by_d[d]['irrelevant'].append(dist_red_vert)

            # --- 1.2b: 遍历并收集所有“纵向”向量的距离 ---
            for d in range(1, 4):
                for x_start in range(1, 5):
                    for y_start in range(1, 5):  # 确保终点y_start+d不超过4
                        start_rel = get_face_num_by_coords(x_start, y_start)
                        end_rel = get_face_num_by_coords(x_start, y_start + d)
                        start_irrel = get_face_num_by_coords(x_start, y_start)
                        end_irrel = get_face_num_by_coords(x_start + d, y_start)
                        # print(f" rel BlueFace_{start_rel}", f"BlueFace_{end_rel}")
                        # print(f" irrel BlueFace_{start_irrel}", f"BlueFace_{end_irrel}")

                        # Blue Face: 纵向是“相关轴”
                        if start_rel is not None and end_rel is not None:
                            dist_blue_vert = neural_rdm.loc[f"RedFace_{start_rel}", f"RedFace_{end_rel}"]
                            distances_by_d[d]['relevant'].append(dist_blue_vert)
                        # Blue Face: 纵向是“无关轴”
                        if start_irrel is not None and end_irrel is not None:
                            dist_blue_horiz = neural_rdm.loc[f"RedFace_{start_irrel}", f"RedFace_{end_irrel}"]
                            distances_by_d[d]['irrelevant'].append(dist_blue_horiz)

            omega_attention_by_d = []  # 用于存储最终的3个omega值
            for d, dists in distances_by_d.items():
                mean_relevant_dist = np.mean(dists['relevant'])
                mean_irrelevant_dist = np.mean(dists['irrelevant'])
                ratio = mean_irrelevant_dist / mean_relevant_dist
                omega_attention_by_d.append(ratio)
                # print(
                #     f"  步长 d={d}: mean(irrel)/mean(rel) = {mean_irrelevant_dist:.3f} / {mean_relevant_dist:.3f} = {ratio:.4f}")
            omega_attention = np.mean(omega_attention_by_d)-1
            print(f"\n ω_attention = {omega_attention:.4f}")


            # --- c. 计算 ω_congurent (对角线) ---
            vector_distances = defaultdict(lambda: {'red': [], 'blue': []})
            # 遍历所有可能的点对，生成向量实例
            for p1_num in range(1, 17):
                for p2_num in range(p1_num + 1, 17):
                    x1, y1 = GRID_MAP.loc[GRID_MAP['number'] == p1_num, ['x', 'y']].iloc[0]
                    x2, y2 = GRID_MAP.loc[GRID_MAP['number'] == p2_num, ['x', 'y']].iloc[0]
                    dx, dy = x2 - x1, y2 - y1
                    vector_type = (dx, dy)
                    dist_red = neural_rdm.loc[f"RedFace_{p1_num}", f"RedFace_{p2_num}"]
                    dist_blue = neural_rdm.loc[f"BlueFace_{p1_num}", f"BlueFace_{p2_num}"]
                    vector_distances[vector_type]['red'].append(dist_red)
                    vector_distances[vector_type]['blue'].append(dist_blue)
            # --- 2. (数据聚合) 计算每种向量类型的平均神经距离 ---
            avg_dissim_map = {}
            for vector_type, color_dists in vector_distances.items():
                # 将red和blue的距离列表合并，然后求平均
                all_dists = color_dists['red'] + color_dists['blue']
                avg_dissim_map[vector_type] = np.mean(all_dists)
            # --- 3. (遍历与计算) 遍历9种对称配对，计算比率 ---
            symmetric_pair_types = [
                {'cong': (1, 1), 'incong': (-1, 1)}, {'cong': (2, 1), 'incong': (-2, 1)},
                {'cong': (1, 2), 'incong': (-1, 2)}, {'cong': (2, 2), 'incong': (-2, 2)},
                {'cong': (3, 1), 'incong': (-3, 1)}, {'cong': (1, 3), 'incong': (-1, 3)},
                {'cong': (3, 2), 'incong': (-3, 2)}, {'cong': (2, 3), 'incong': (-2, 3)},
                {'cong': (3, 3), 'incong': (-3, 3)}
            ]
            final_ratios = []
            # 遍历这9种配对
            for pair in symmetric_pair_types:
                vc_type, vl_type = pair['cong'], pair['incong']
                # --- 为一致性向量类型提取平均距离 ---
                vc_pos_dist = avg_dissim_map.get(vc_type)
                avg_dist_cong = np.nanmean(vc_pos_dist)
                # --- 为不一致性向量类型提取平均距离 ---
                vl_pos_dist = avg_dissim_map.get(vl_type)
                avg_dist_incong = np.nanmean(vl_pos_dist)
                # --- 计算比率 ---
                if not np.isnan(avg_dist_cong) and not np.isnan(avg_dist_incong) and avg_dist_cong > 0:
                    ratio =  avg_dist_incong / avg_dist_cong
                    final_ratios.append(ratio)
            # --- 4. 计算最终的 ω_neural 指标 ---
            omega_congruent = np.mean(final_ratios)-1
            print(f"\n ω_congruent = {omega_congruent:.4f}")


            result_attn = {
                'subject': subj_name,
                'roi': roi_name,
                'condition': 'attention',
                'omega': omega_attention
            }
            all_results.append(result_attn)
            result_cong = {
                'subject': subj_name,
                'roi': roi_name,
                'condition': 'congruent',
                'omega': omega_congruent
            }
            all_results.append(result_cong)

results_df = pd.DataFrame(all_results)

# 保存RDM矩阵
pd.DataFrame(all_results).to_csv(f"/home/medicaldata/LJData/SR_ana/analysis_res/rsa/rbCue/warping/warping_eucli_park.csv", sep=',',
    header=True, index=False, float_format='%.4f')


print("ALL PROCESS IS DONE!")

