import os
import unittest

import torch

from data import *
from data.data_input import save_datamodel, GagesModel, _basin_norm, save_result
from data.gages_input_dataset import GagesModels
from hydroDL.master import *
import definitions
from visual.plot_model import plot_we_need


class MyTestCaseGages(unittest.TestCase):
    def setUp(self) -> None:
        """before all of these, natural flow model need to be generated by config.ini of gages dataset, and it need
        to be moved to right dir manually """
        config_dir = definitions.CONFIG_DIR
        # self.config_file = os.path.join(config_dir, "basic/config_exp13.ini")
        # self.subdir = r"basic/exp13"
        # self.config_file = os.path.join(config_dir, "basic/config_exp25.ini")
        # self.subdir = r"basic/exp25"

        # all nonref regions
        # self.config_file = os.path.join(config_dir, "basic/config_exp18.ini")
        # self.subdir = r"basic/exp18"

        # camels regions
        self.config_file = os.path.join(config_dir, "basic/config_exp10.ini")
        self.subdir = r"basic/exp10"

        # different regions seperately
        # self.config_file = os.path.join(config_dir, "basic/config_exp3.ini")
        # self.subdir = r"basic/exp3"

        # self.config_file = os.path.join(config_dir, "basic/config_exp9.ini")
        # self.subdir = r"basic/exp9"
        self.config_data = GagesConfig.set_subdir(self.config_file, self.subdir)
        test_epoch_lst = [100, 150, 200, 220, 250, 280, 290, 300, 310, 320, 350]
        # self.test_epoch = test_epoch_lst[0]
        # self.test_epoch = test_epoch_lst[1]
        # self.test_epoch = test_epoch_lst[2]
        # self.test_epoch = test_epoch_lst[3]
        # self.test_epoch = test_epoch_lst[4]
        # self.test_epoch = test_epoch_lst[5]
        # self.test_epoch = test_epoch_lst[6]
        self.test_epoch = test_epoch_lst[7]
        # self.test_epoch = test_epoch_lst[8]
        # self.test_epoch = test_epoch_lst[9]
        # self.test_epoch = test_epoch_lst[10]

    def test_gages_data_model(self):
        gages_model = GagesModels(self.config_data, screen_basin_area_huc4=False)
        save_datamodel(gages_model.data_model_train, data_source_file_name='data_source.txt',
                       stat_file_name='Statistics.json', flow_file_name='flow', forcing_file_name='forcing',
                       attr_file_name='attr', f_dict_file_name='dictFactorize.json',
                       var_dict_file_name='dictAttribute.json', t_s_dict_file_name='dictTimeSpace.json')
        save_datamodel(gages_model.data_model_test, data_source_file_name='test_data_source.txt',
                       stat_file_name='test_Statistics.json', flow_file_name='test_flow',
                       forcing_file_name='test_forcing', attr_file_name='test_attr',
                       f_dict_file_name='test_dictFactorize.json', var_dict_file_name='test_dictAttribute.json',
                       t_s_dict_file_name='test_dictTimeSpace.json')
        print("read and save data model")

    def test_gages_data_model_readquickdata(self):
        quick_data_dir = os.path.join(self.config_data.data_path["DB"], "quickdata")
        # data_dir = os.path.join(quick_data_dir, "conus-all_85-05_nan-0.1_00-1.0")
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

        gages_model_train = GagesModel.update_data_model(self.config_data, data_model_train, data_attr_update=True,
                                                         screen_basin_area_huc4=False)
        gages_model_test = GagesModel.update_data_model(self.config_data, data_model_test, data_attr_update=True,
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

    def test_train_gages(self):
        data_model = GagesModel.load_datamodel(self.config_data.data_path["Temp"],
                                               data_source_file_name='data_source.txt',
                                               stat_file_name='Statistics.json', flow_file_name='flow.npy',
                                               forcing_file_name='forcing.npy', attr_file_name='attr.npy',
                                               f_dict_file_name='dictFactorize.json',
                                               var_dict_file_name='dictAttribute.json',
                                               t_s_dict_file_name='dictTimeSpace.json')
        with torch.cuda.device(0):
            # pre_trained_model_epoch = 320
            master_train(data_model)
            # master_train(data_model, pre_trained_model_epoch=pre_trained_model_epoch)

    def test_test_gages(self):
        data_model = GagesModel.load_datamodel(self.config_data.data_path["Temp"],
                                               data_source_file_name='test_data_source.txt',
                                               stat_file_name='test_Statistics.json', flow_file_name='test_flow.npy',
                                               forcing_file_name='test_forcing.npy', attr_file_name='test_attr.npy',
                                               f_dict_file_name='test_dictFactorize.json',
                                               var_dict_file_name='test_dictAttribute.json',
                                               t_s_dict_file_name='test_dictTimeSpace.json')
        with torch.cuda.device(0):
            pred, obs = master_test(data_model, epoch=self.test_epoch)
            basin_area = data_model.data_source.read_attr(data_model.t_s_dict["sites_id"], ['DRAIN_SQKM'],
                                                          is_return_dict=False)
            mean_prep = data_model.data_source.read_attr(data_model.t_s_dict["sites_id"], ['PPTAVG_BASIN'],
                                                         is_return_dict=False)
            mean_prep = mean_prep / 365 * 10
            pred = _basin_norm(pred, basin_area, mean_prep, to_norm=False)
            obs = _basin_norm(obs, basin_area, mean_prep, to_norm=False)
            save_result(data_model.data_source.data_config.data_path['Temp'], self.test_epoch, pred, obs)
            plot_we_need(data_model, obs, pred, id_col="STAID", lon_col="LNG_GAGE", lat_col="LAT_GAGE")


if __name__ == '__main__':
    unittest.main()
