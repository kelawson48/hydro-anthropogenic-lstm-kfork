import os
import unittest

import torch

import definitions
from data import GagesConfig
from data.data_input import save_datamodel, _basin_norm, GagesModel
from data.gages_input_dataset import GagesModels
from hydroDL.master.master import master_train, master_test, master_train_1by1, master_test_1by1
from utils import serialize_numpy
from visual.plot_model import plot_we_need
import numpy as np

from visual.plot_stat import plot_loss_early_stop


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """before all of these, natural flow model need to be generated by config.ini of gages dataset, and it need
        to be moved to right dir manually """
        config_dir = definitions.CONFIG_DIR
        self.config_file = os.path.join(config_dir, "gages1by1/config_exp8.ini")
        self.subdir = r"gages1by1/exp8"
        self.config_data = GagesConfig.set_subdir(self.config_file, self.subdir)

    def test_gages_data_model(self):
        gages_model = GagesModels(self.config_data)
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

    def test_train_gages_iter(self):
        data_model = GagesModel.load_datamodel(self.config_data.data_path["Temp"],
                                               data_source_file_name='data_source.txt',
                                               stat_file_name='Statistics.json', flow_file_name='flow.npy',
                                               forcing_file_name='forcing.npy', attr_file_name='attr.npy',
                                               f_dict_file_name='dictFactorize.json',
                                               var_dict_file_name='dictAttribute.json',
                                               t_s_dict_file_name='dictTimeSpace.json')
        valid_size = 0.2
        with torch.cuda.device(1):
            for i in range(679, data_model.data_flow.shape[0]):
                print("\n", "Training model", str(i + 1), ":\n")
                data_models_i = GagesModel.which_data_model(data_model, i)
                model, train_loss, valid_loss = master_train_1by1(data_models_i, valid_size=valid_size)
                fig = plot_loss_early_stop(train_loss, valid_loss)
                out_dir = data_models_i.data_source.data_config.data_path["Out"]
                fig.savefig(os.path.join(out_dir, 'loss_plot.png'), bbox_inches='tight')

    def test_test_gages_iter(self):
        data_model = GagesModel.load_datamodel(self.config_data.data_path["Temp"],
                                               data_source_file_name='test_data_source.txt',
                                               stat_file_name='test_Statistics.json', flow_file_name='test_flow.npy',
                                               forcing_file_name='test_forcing.npy', attr_file_name='test_attr.npy',
                                               f_dict_file_name='test_dictFactorize.json',
                                               var_dict_file_name='test_dictAttribute.json',
                                               t_s_dict_file_name='test_dictTimeSpace.json')
        with torch.cuda.device(1):
            obs_lst = []
            pred_lst = []
            for i in range(0, data_model.data_flow.shape[0]):
                print("\n", "Testing model", str(i + 1), ":\n")
                data_models_i = GagesModel.which_data_model(data_model, i)
                pred, obs = master_test_1by1(data_models_i)
                basin_area = data_models_i.data_source.read_attr(data_models_i.t_s_dict["sites_id"], ['DRAIN_SQKM'],
                                                                 is_return_dict=False)
                mean_prep = data_models_i.data_source.read_attr(data_models_i.t_s_dict["sites_id"],
                                                                ['PPTAVG_BASIN'],
                                                                is_return_dict=False)
                mean_prep = mean_prep / 365 * 10
                pred = _basin_norm(pred, basin_area, mean_prep, to_norm=False)
                obs = _basin_norm(obs, basin_area, mean_prep, to_norm=False)
                obs_lst.append(obs.flatten())
                pred_lst.append(pred.flatten())
            preds = np.array(pred_lst)
            obss = np.array(obs_lst)
            flow_pred_file = os.path.join(data_model.data_source.data_config.data_path['Temp'],
                                          'flow_pred')
            flow_obs_file = os.path.join(data_model.data_source.data_config.data_path['Temp'],
                                         'flow_obs')
            serialize_numpy(preds, flow_pred_file)
            serialize_numpy(obss, flow_obs_file)


if __name__ == '__main__':
    unittest.main()
