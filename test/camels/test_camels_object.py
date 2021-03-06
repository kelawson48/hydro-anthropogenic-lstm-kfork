"""模块测试"""
import os
import unittest
from data import *
from utils import *
import definitions


class TestDataClassCase(unittest.TestCase):
    config_file = definitions.CONFIG_FILE
    project_dir = definitions.ROOT_DIR
    dataset = 'camels'
    dir_db = os.path.join(project_dir, 'example/data', dataset)
    dir_out = os.path.join(project_dir, 'example/output', dataset)
    dir_temp = os.path.join(project_dir, 'example/temp', dataset)
    model_dict_file = os.path.join(dir_temp, 'master.json')
    data_source_dump = os.path.join(dir_temp, 'data_source.txt')

    def setUp(self):
        self.config_data = CamelsConfig(self.config_file)
        print('setUp...')

    def test_data_source(self):
        # 读取模型配置文件，并写入json
        serialize_json(self.config_data.model_dict, self.model_dict_file)
        # 准备训练数据
        source_data = CamelsSource(self.config_data, self.config_data.model_dict["data"]["tRangeTrain"])
        # 序列化保存对象
        dir_temp = source_data.all_configs["temp_dir"]
        if not os.path.isdir(dir_temp):
            os.mkdir(dir_temp)
        my_file = os.path.join(dir_temp, 'data_source.txt')
        serialize_pickle(source_data, my_file)

    def test_read_data_source_temp(self):
        d = unserialize_pickle(self.data_source_dump)
        print(d)

    def test_data_model(self):
        source_data = unserialize_pickle(self.data_source_dump)
        print(source_data)
        data_model = DataModel(source_data)
        print(data_model)

        # 序列化保存对象
        dir_temp = source_data.all_configs["temp_dir"]
        stat_file = os.path.join(dir_temp, 'Statistics.json')
        flow_file = os.path.join(dir_temp, 'flow')
        forcing_file = os.path.join(dir_temp, 'forcing')
        attr_file = os.path.join(dir_temp, 'attr')
        f_dict_file = os.path.join(dir_temp, 'dictFactorize.json')
        var_dict_file = os.path.join(dir_temp, 'dictAttribute.json')
        t_s_dict_file = os.path.join(dir_temp, 'dictTimeSpace.json')

        # 存储data_model，因为data_model里的数据如果直接序列化会比较慢，所以各部分分别序列化，dict的直接序列化为json文件，数据的HDF5
        serialize_json(data_model.stat_dict, stat_file)
        serialize_numpy(data_model.data_flow, flow_file)
        serialize_numpy(data_model.data_forcing, forcing_file)
        serialize_numpy(data_model.data_attr, attr_file)
        # dictFactorize.json is the explanation of value of categorical variables
        serialize_json(data_model.f_dict, f_dict_file)
        serialize_json(data_model.var_dict, var_dict_file)
        serialize_json(data_model.t_s_dict, t_s_dict_file)


if __name__ == '__main__':
    unittest.main()
