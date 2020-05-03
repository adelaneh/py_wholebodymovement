#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import unittest
from nose.tools import *
import os
import itertools

import numpy as np
import pandas as pd

import py_wholebodymovement.utils.predefined_schemas as psc

from py_wholebodymovement.utils.generic_helper import get_install_path

from py_wholebodymovement.utils.cleaning_utils import clean_gaussian_outliers
from py_wholebodymovement.utils.cleaning_utils import clean_dimensions_gaussian_outliers
from py_wholebodymovement.utils.cleaning_utils import denoise_data

from py_wholebodymovement.articulated_figure import calculate_2d_articulated_figure_angle
from py_wholebodymovement.articulated_figure import calculate_2d_articulated_figure_angles
from py_wholebodymovement.articulated_figure import extend_2d_articulated_figure
from py_wholebodymovement.articulated_figure import calculate_3d_articulated_figure_angle
from py_wholebodymovement.articulated_figure import calculate_3d_articulated_figure_angles
from py_wholebodymovement.articulated_figure import extend_3d_articulated_figure
from py_wholebodymovement.articulated_figure import calculate_phase_locking_value
from py_wholebodymovement.articulated_figure import calculate_phase_angles
from py_wholebodymovement.articulated_figure import calculate_phase_angle_measures

datasets_path   = os.sep.join([get_install_path(), 'tests', 'test_datasets'])

class ArticulatedFigureTestCases(unittest.TestCase):
    def setUp(self):
        # self._test_data_filename = os.sep.join([datasets_path, 'sample_1.csv'])
        # self._test_data          = pd.read_csv(self._test_data_filename)
        return

    def test_calculate_3d_articulated_figure_angle(self):
        _joint_names = ['Head', 'RightShoulder', 'Torso']
        _dim_names   = ['_X', '_Y', '_Z']
        _columns     = [jn + dn for jn, dn in itertools.product(_joint_names, _dim_names)]

        _test_data   = pd.DataFrame(columns=_columns)
        _test_data.loc[_test_data.shape[0], :] = [0, 0, 0, 
                                                  1, 0, 0, 
                                                  0, 1, 0]

        _angles      = calculate_3d_articulated_figure_angle(_test_data, 'Head', 'RightShoulder', 'Torso')

        self.assertEqual(_angles[-1], 90.)

        _test_data.loc[_test_data.shape[0], :] = [0, 0, 0, 
                                                  0, 1, 0, 
                                                  0, -1, 0]

        _angles      = calculate_3d_articulated_figure_angle(_test_data, 'Head', 'RightShoulder', 'Torso')

        self.assertEqual(_angles[-1], 180.)

        _test_data.loc[_test_data.shape[0], :] = [0, 0, 0, 
                                                  1, 0, 1, 
                                                  0, 1, 0]

        _angles      = calculate_3d_articulated_figure_angle(_test_data, 'Head', 'RightShoulder', 'Torso')

        self.assertEqual(_angles[-1], 90.)

        _test_data.loc[_test_data.shape[0], :] = [0, 0, 0, 
                                                  1, 0, 1, 
                                                  1, 0, 0]

        _angles      = calculate_3d_articulated_figure_angle(_test_data, 'Head', 'RightShoulder', 'Torso')

        self.assertEqual(_angles[-1], 45.)

        _test_data.loc[_test_data.shape[0], :] = [0, 0, 0, 
                                                  -1, 0, 1, 
                                                  1, 0, 0]

        _angles      = calculate_3d_articulated_figure_angle(_test_data, 'Head', 'RightShoulder', 'Torso')

        self.assertEqual(_angles[-1], 135.)

        _test_data.loc[_test_data.shape[0], :] = [0, 0, 0, 
                                                  1, 0, 0,
                                                  -1, 0, 1,] 

        _angles      = calculate_3d_articulated_figure_angle(_test_data, 'Head', 'RightShoulder', 'Torso')

        self.assertEqual(_angles[-1], 135.)

        print(_angles)
