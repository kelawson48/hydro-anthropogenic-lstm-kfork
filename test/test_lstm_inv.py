import unittest

import definitions
from data import GagesConfig, GagesSource, DataModel
from data.gages_input_dataset import GagesInvDataset
from hydroDL.master.master import train_lstm_inv

import os


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """before all of these, natural flow model need to be generated by config.ini of gages dataset, and it need
        to be moved to right dir manually """
        config_dir = definitions.CONFIG_DIR
        self.config_file_1 = os.path.join(config_dir, "inv/config_inv_1_ex1.ini")
        self.config_file_2 = os.path.join(config_dir, "inv/config_inv_2_ex1.ini")
        self.subdir = r"inv/exp1"

    def test_inv(self):
        # data1 is historical data as input of LSTM-Inv, which will be a kernel for the second LSTM
        config_data_1 = GagesConfig.set_subdir(self.config_file_1, self.subdir)
        # choose some small basins, unit: SQKM
        basin_area_screen = 100
        source_data_1 = GagesSource.choose_some_basins(config_data_1, config_data_1.model_dict["data"]["tRangeTrain"],
                                                       basin_area_screen)
        df1 = DataModel(source_data_1)

        # data2 is made for second layer, which need to be combined with theta that is generated by lstm-inv and
        # final dim of lstm-inv
        config_data_2 = GagesConfig.set_subdir(self.config_file_2, self.subdir)
        source_data_2 = GagesSource.choose_some_basins(config_data_2, config_data_1.model_dict["data"]["tRangeTrain"],
                                                       basin_area_screen)
        df2 = DataModel(source_data_2)
        dataset = GagesInvDataset(df1, df2)
        train_lstm_inv(dataset)


if __name__ == '__main__':
    unittest.main()