import unittest

import torch

import definitions
from data import GagesConfig, GagesSource
from data.data_input import GagesModel, _basin_norm, save_datamodel, save_result, load_result
from data.gages_input_dataset import GagesDamDataModel, choose_which_purpose, load_dataconfig_case_exp
from data.nid_input import NidModel
from explore.gages_stat import split_results_to_regions
from explore.stat import statError, ecdf
from hydroDL.master.master import master_train, master_test
import numpy as np
import os
import pandas as pd

from utils import unserialize_json
from utils.dataset_format import subset_of_dict
from visual import plot_ts_obs_pred
from visual.plot_model import plot_we_need, plot_map
from visual.plot_stat import plot_ecdf, plot_diff_boxes, plot_ecdfs


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        config_dir = definitions.CONFIG_DIR
        self.config_file = os.path.join(config_dir, "dam/config_exp27.ini")
        self.subdir = r"dam/exp27"
        self.config_data = GagesConfig.set_subdir(self.config_file, self.subdir)
        # self.nid_file = 'PA_U.xlsx'
        # self.nid_file = 'OH_U.xlsx'
        self.nid_file = 'NID2018_U.xlsx'
        self.test_epoch = 300

    def test_gages_data_model(self):
        config_data = self.config_data
        dam_num = [1, 2000]  # max dam num is 1740
        source_data = GagesSource.choose_some_basins(config_data, config_data.model_dict["data"]["tRangeTrain"],
                                                     screen_basin_area_huc4=False, dam_num=dam_num)
        sites_id = source_data.all_configs['flow_screen_gage_id']
        quick_data_dir = os.path.join(self.config_data.data_path["DB"], "quickdata")
        data_dir = os.path.join(quick_data_dir, "conus-all_90-10_nan-0.0_00-1.0")
        data_model_train = GagesModel.load_datamodel(data_dir,
                                                     data_source_file_name='data_source.txt',
                                                     stat_file_name='Statistics.json', flow_file_name='flow.npy',
                                                     forcing_file_name='forcing.npy', attr_file_name='attr.npy',
                                                     f_dict_file_name='dictFactorize.json',
                                                     var_dict_file_name='dictAttribute.json',
                                                     t_s_dict_file_name='dictTimeSpace.json')
        data_model_test = GagesModel.load_datamodel(data_dir,
                                                    data_source_file_name='test_data_source.txt',
                                                    stat_file_name='test_Statistics.json',
                                                    flow_file_name='test_flow.npy',
                                                    forcing_file_name='test_forcing.npy',
                                                    attr_file_name='test_attr.npy',
                                                    f_dict_file_name='test_dictFactorize.json',
                                                    var_dict_file_name='test_dictAttribute.json',
                                                    t_s_dict_file_name='test_dictTimeSpace.json')
        gages_model_train = GagesModel.update_data_model(self.config_data, data_model_train, sites_id_update=sites_id,
                                                         screen_basin_area_huc4=False)
        gages_model_test = GagesModel.update_data_model(self.config_data, data_model_test, sites_id_update=sites_id,
                                                        train_stat_dict=gages_model_train.stat_dict,
                                                        screen_basin_area_huc4=False)
        save_datamodel(gages_model_train, data_source_file_name='data_source.txt',
                       stat_file_name='Statistics.json', flow_file_name='flow', forcing_file_name='forcing',
                       attr_file_name='attr', f_dict_file_name='dictFactorize.json',
                       var_dict_file_name='dictAttribute.json', t_s_dict_file_name='dictTimeSpace.json')
        save_datamodel(gages_model_test, data_source_file_name='test_data_source.txt',
                       stat_file_name='test_Statistics.json', flow_file_name='test_flow',
                       forcing_file_name='test_forcing', attr_file_name='test_attr',
                       f_dict_file_name='test_dictFactorize.json', var_dict_file_name='test_dictAttribute.json',
                       t_s_dict_file_name='test_dictTimeSpace.json')
        print("read and save data model")

    def test_dam_train(self):
        with torch.cuda.device(0):
            gages_model_train = GagesModel.load_datamodel(self.config_data.data_path["Temp"],
                                                          data_source_file_name='data_source.txt',
                                                          stat_file_name='Statistics.json', flow_file_name='flow.npy',
                                                          forcing_file_name='forcing.npy', attr_file_name='attr.npy',
                                                          f_dict_file_name='dictFactorize.json',
                                                          var_dict_file_name='dictAttribute.json',
                                                          t_s_dict_file_name='dictTimeSpace.json')
            master_train(gages_model_train)
            # pre_trained_model_epoch = 100
            # master_train(gages_model_train, pre_trained_model_epoch=pre_trained_model_epoch)

    def test_dam_test(self):
        with torch.cuda.device(1):
            data_model_test = GagesModel.load_datamodel(self.config_data.data_path["Temp"],
                                                        data_source_file_name='test_data_source.txt',
                                                        stat_file_name='test_Statistics.json',
                                                        flow_file_name='test_flow.npy',
                                                        forcing_file_name='test_forcing.npy',
                                                        attr_file_name='test_attr.npy',
                                                        f_dict_file_name='test_dictFactorize.json',
                                                        var_dict_file_name='test_dictAttribute.json',
                                                        t_s_dict_file_name='test_dictTimeSpace.json')
            gages_input = GagesModel.update_data_model(self.config_data, data_model_test)
            pred, obs = master_test(gages_input, epoch=self.test_epoch)
            basin_area = gages_input.data_source.read_attr(gages_input.t_s_dict["sites_id"], ['DRAIN_SQKM'],
                                                           is_return_dict=False)
            mean_prep = gages_input.data_source.read_attr(gages_input.t_s_dict["sites_id"], ['PPTAVG_BASIN'],
                                                          is_return_dict=False)
            mean_prep = mean_prep / 365 * 10
            pred = _basin_norm(pred, basin_area, mean_prep, to_norm=False)
            obs = _basin_norm(obs, basin_area, mean_prep, to_norm=False)
            save_result(gages_input.data_source.data_config.data_path['Temp'], self.test_epoch, pred, obs)
            plot_we_need(gages_input, obs, pred, id_col="STAID", lon_col="LNG_GAGE", lat_col="LAT_GAGE")


if __name__ == '__main__':
    unittest.main()
