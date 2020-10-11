import unittest
import pickle
import numpy as np
from read_ice.read_file import SSMI_Tb, concentration, piomas

class TestTools(unittest.TestCase):

    """This class tests the read_binary functionality against
    pre-prepared, pickled arrays"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_SSMI_37_GHz_nh(self):

        with open('tests/test_results/SSMI_37_GHz_nh.p', 'rb') as f:

            array_for_comparison = pickle.load(f)

        array = SSMI_Tb('tests/test_files/tb_f17_20190711_v5_n37h.bin',
                        'n', 37)

        test_result = np.array_equal(array, array_for_comparison)

        self.assertTrue(test_result)

    def test_SSMI_91_GHz_nh(self):

        with open('tests/test_results/SSMI_91_GHz_nh.p', 'rb') as f:

            array_for_comparison = pickle.load(f)

        array = SSMI_Tb('tests/test_files/tb_f17_20190727_v5_n91h.bin',
                        'n', 91)

        test_result = np.array_equal(array, array_for_comparison)

        self.assertTrue(test_result)

    def test_SSMI_91_GHz_sh(self):

        with open('tests/test_results/SSMI_91_GHz_sh.p', 'rb') as f:

            array_for_comparison = pickle.load(f)

        array = SSMI_Tb('tests/test_files/tb_f17_20190727_v5_s91h.bin', 's', 91)

        test_result = np.array_equal(array, array_for_comparison)

        self.assertTrue(test_result)

    def test_SSMI_19_GHz_sh(self):

        with open('tests/test_results/SSMI_19_GHz_sh.p', 'rb') as f:

            array_for_comparison = pickle.load(f)

        array = SSMI_Tb('tests/test_files/tb_f17_20190710_v5_s19v.bin', 's', 19)

        test_result = np.array_equal(array, array_for_comparison)

        self.assertTrue(test_result)


    def test_concentration_nh(self):

        with open('tests/test_results/concentration_nh.p', 'rb') as f:

            array_for_comparison = pickle.load(f)

        array = concentration('tests/test_files/nt_19781111_n07_v1.1_n.bin',
                              'n')
        test_result = np.array_equal(array, array_for_comparison)

        self.assertTrue(test_result)

    def test_concentration_sh(self):

        with open('tests/test_results/concentration_sh.p', 'rb') as f:

            array_for_comparison = pickle.load(f)

        array = concentration('tests/test_files/nt_19781113_n07_v1.1_s.bin',
                              's')

        test_result = np.array_equal(array, array_for_comparison)

        self.assertTrue(test_result)

    def test_piomas(self):

        with open('tests/test_results/piomas.p', 'rb') as f:

            array_for_comparison = pickle.load(f)

        array = piomas('tests/test_files/heff.H1993')

        test_result = np.array_equal(array, array_for_comparison)

        self.assertTrue(test_result)

if __name__ == '__main__':
    unittest.main()