import unittest
from read_ice.get_geo_coords import get_dims, piomas_grid, polar_stereo

class TestTools(unittest.TestCase):

    """This class tests the geocoordinate systems."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ps25(self):

        ps25_coords_n = polar_stereo(resolution=25, hemisphere='n')
        self.assertEqual(ps25_coords_n['lon'].shape, (448, 304))
        self.assertEqual(ps25_coords_n['lon'].shape,
                         ps25_coords_n['lat'].shape)
        self.assertTrue((ps25_coords_n['lat'] > 0).all())

        ps25_coords_s = polar_stereo(resolution=25, hemisphere='s')
        self.assertEqual(ps25_coords_s['lon'].shape, (332, 316))
        self.assertEqual(ps25_coords_s['lon'].shape,
                         ps25_coords_s['lat'].shape)
        self.assertTrue((ps25_coords_s['lat'] < 0).all())

    def test_ps12(self):

        ps12_coords_n = polar_stereo(resolution=12.5, hemisphere='n')
        self.assertEqual(ps12_coords_n['lon'].shape, (896, 608))
        self.assertEqual(ps12_coords_n['lon'].shape,
                         ps12_coords_n['lat'].shape)
        self.assertTrue((ps12_coords_n['lat'] > 0).all())

        ps12_coords_s = polar_stereo(resolution=12.5, hemisphere='s')
        self.assertEqual(ps12_coords_s['lon'].shape, (664, 632))
        self.assertEqual(ps12_coords_s['lon'].shape,
                         ps12_coords_s['lat'].shape)
        self.assertTrue((ps12_coords_s['lat'] < 0).all())

    def test_piomas_coords(self):

        pio_coords_n = piomas_grid()
        self.assertEqual(pio_coords_n['lon'].shape, (360, 120))
        self.assertEqual(pio_coords_n['lon'].shape,
                         pio_coords_n['lat'].shape)
        self.assertTrue((pio_coords_n['lat'] > 0).all())



if __name__ == '__main__':

    # ps25_coords_n = polar_stereo(resolution=12.5, hemisphere='s')
    #
    # print(ps25_coords_n['lon'].shape)

    unittest.main()