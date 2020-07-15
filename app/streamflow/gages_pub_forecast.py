import sys

import matplotlib.pyplot as plt
import torch
from functools import reduce

from matplotlib import gridspec

from data import GagesSource
from data.data_input import GagesModel, _basin_norm, save_result, load_result
from data.gages_input_dataset import load_ensemble_result, load_dataconfig_case_exp, load_pub_test_result
from explore.stat import statError

sys.path.append("../..")
import os
import definitions
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

exp_lst = [["ecoregion_exp1", "ecoregion_exp6"], ["ecoregion_exp2", "ecoregion_exp5"],
           ["ecoregion_exp3", "ecoregion_exp7"]]
# train_data_name_lst = [["LSTM-z", "LSTM-zs"], ["LSTM-z", "LSTM-zl"], ["LSTM-s", "LSTM-sl"]]
train_data_name_lst = [["Train-z", "Train-zs"], ["Train-z", "Train-zl"], ["Train-s", "Train-sl"]]
test_data_name_lst = [["PUB-z", "PUB-s"], ["PUB-z", "PUB-l"], ["PUB-s", "PUB-l"]]
config_dir = definitions.CONFIG_DIR
test_epoch = 300
split_num = 3

# test


train_set = "training"
test_set = "testing"
show_ind_key = "NSE"
fig = plt.figure(figsize=(15, 5))
gs = gridspec.GridSpec(1, 3)
colors = ["Greens", "Blues", "Reds"]
for k in range(len(exp_lst)):
    ax_k = plt.subplot(gs[k])
    frames = []
    for j in range(len(exp_lst[k])):
        config_data = load_dataconfig_case_exp(exp_lst[k][j])
        preds = []
        obss = []
        preds2 = []
        obss2 = []
        for i in range(split_num):
            data_model = GagesModel.load_datamodel(config_data.data_path["Temp"], str(i),
                                                   data_source_file_name='test_data_source.txt',
                                                   stat_file_name='test_Statistics.json',
                                                   flow_file_name='test_flow.npy',
                                                   forcing_file_name='test_forcing.npy', attr_file_name='test_attr.npy',
                                                   f_dict_file_name='test_dictFactorize.json',
                                                   var_dict_file_name='test_dictAttribute.json',
                                                   t_s_dict_file_name='test_dictTimeSpace.json')
            data_model_2 = GagesModel.load_datamodel(config_data.data_path["Temp"], str(i),
                                                     data_source_file_name='test_data_source_2.txt',
                                                     stat_file_name='test_Statistics_2.json',
                                                     flow_file_name='test_flow_2.npy',
                                                     forcing_file_name='test_forcing_2.npy',
                                                     attr_file_name='test_attr_2.npy',
                                                     f_dict_file_name='test_dictFactorize_2.json',
                                                     var_dict_file_name='test_dictAttribute_2.json',
                                                     t_s_dict_file_name='test_dictTimeSpace_2.json')
            pred_i, obs_i = load_result(data_model.data_source.data_config.data_path['Temp'], test_epoch)
            pred_i = pred_i.reshape(pred_i.shape[0], pred_i.shape[1])
            obs_i = obs_i.reshape(obs_i.shape[0], obs_i.shape[1])

            preds.append(pred_i)
            obss.append(obs_i)

            pred_2, obs_2 = load_result(data_model_2.data_source.data_config.data_path['Temp'],
                                        test_epoch, pred_name='flow_pred_2',
                                        obs_name='flow_obs_2')
            pred_2 = pred_2.reshape(pred_2.shape[0], pred_2.shape[1])
            obs_2 = obs_2.reshape(obs_2.shape[0], obs_2.shape[1])

            preds2.append(pred_2)
            obss2.append(obs_2)

        preds_np = reduce(lambda a, b: np.vstack((a, b)), preds)
        obss_np = reduce(lambda a, b: np.vstack((a, b)), obss)
        inds = statError(obss_np, preds_np)
        inds_df_a = pd.DataFrame(inds)

        preds2_np = reduce(lambda a, b: np.vstack((a, b)), preds2)
        obss2_np = reduce(lambda a, b: np.vstack((a, b)), obss2)
        inds2 = statError(obss2_np, preds2_np)
        inds_df_a2 = pd.DataFrame(inds2)

        df_a = pd.DataFrame({train_set: np.full([inds_df_a.shape[0]], train_data_name_lst[k][j]),
                             test_set: np.full([inds_df_a.shape[0]], test_data_name_lst[k][0]),
                             # train_data_name_lst[k][j] + "-" + test_data_name_lst[k][0])
                             show_ind_key: inds_df_a[show_ind_key]})
        df_a2 = pd.DataFrame({train_set: np.full([inds_df_a2.shape[0]], train_data_name_lst[k][j]),
                              test_set: np.full([inds_df_a2.shape[0]], test_data_name_lst[k][1]),
                              # train_data_name_lst[k][j] + "-" + test_data_name_lst[k][1]),
                              show_ind_key: inds_df_a2[show_ind_key]})
        frames.append(df_a)
        frames.append(df_a2)
        # keys_nse = "NSE"
        # xs = []
        # ys = []
        # cases_exps_legends_together = ["PUB_test_in_basins_1", "PUB_test_in_basins_2"]
        #
        # x1, y1 = ecdf(inds_df_a[keys_nse])
        # xs.append(x1)
        # ys.append(y1)
        #
        # x2, y2 = ecdf(inds_df_a2[keys_nse])
        # xs.append(x2)
        # ys.append(y2)
        #
        # plot_ecdfs(xs, ys, cases_exps_legends_together)

    result = pd.concat(frames)
    sns_box = sns.boxplot(ax=ax_k, x=train_set, y=show_ind_key, hue=test_set, data=result, showfliers=False,
                          palette=colors[k], width=0.8)
    plt.subplots_adjust(hspace=0.8)
    ax_k.set_ylim([-1.5, 1])
    medians = result.groupby([train_set, test_set], sort=False)[show_ind_key].median().values
    print(medians)
    # median_labels = [str(np.round(s, 3)) for s in medians]
    # pos = range(len(medians))
    # for tick, label in zip(pos, ax_k.get_xticklabels()):
    #     ax_k.text(pos[tick], medians[tick] + 0.02, median_labels[tick],
    #               horizontalalignment='center', size='x-small', weight='semibold')
    sns.despine()

plt.tight_layout()
show_config_data = load_dataconfig_case_exp(exp_lst[0][0])
plt.savefig(os.path.join(show_config_data.data_path["Out"], '3exps_pub.png'), dpi=500, bbox_inches="tight")