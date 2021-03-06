import unittest
import torch

from hydroDL.model import LSTM, VariationalDropout


class MyTestCase(unittest.TestCase):

    def is_close(self, x, val, thres=1e-5):
        return abs(x - val) < thres

    def test_run_standard(self):
        lstm = LSTM(5, 10)
        x = torch.rand(3, 4, 5)
        a, (hn, cn) = lstm(x)
        assert a.size(0) == x.size(0)
        assert a.size(1) == x.size(1)
        assert a.size(2) == 10

    def test_run_weight_dropout(self):
        # when weight dropout, there will be "To compact weights again call flatten_parameters()" warning!
        lstm = LSTM(5, 10, dropoutw=0.2).cuda()
        x = torch.rand(3, 4, 5, device='cuda')
        a, (hn, cn) = lstm(x)

    def test_run_input_output_dropout(self):
        lstm = LSTM(5, 10, dropouti=0.2, dropouto=0.5).cuda()
        x = torch.rand(3, 4, 5, device='cuda')
        a, (hn, cn) = lstm(x)

    def test_variational_dropout(self):
        dr = 0.3
        seq_len = 10
        do = VariationalDropout(dr, batch_first=True).cuda()
        x = torch.ones(3, seq_len, 5, device='cuda')
        dropped_x = do(x)
        x = dropped_x.sum(1)
        for i in range(3):
            for j in range(5):
                assert self.is_close(x[i, j], 0) or self.is_close(x[i, j],
                                                                  seq_len / (1 - dr)), f"Element {i},{j} was {x[i, j]}"


if __name__ == '__main__':
    unittest.main()
