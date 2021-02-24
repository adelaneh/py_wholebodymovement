#!/usr/bin/env python
# coding: utf-8

# PEP0440 compatible formatted version, see:
# https://www.python.org/dev/peps/pep-0440/
#
# Generic release markers:
#   X.Y.0   # For first release after an increment in Y
#   X.Y.Z   # For bugfix releases
#
# Admissible pre-release markers:
#   X.Y.ZaN   # Alpha release
#   X.Y.ZbN   # Beta release
#   X.Y.ZrcN  # Release Candidate
#   X.Y.Z     # Final release
#
# Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
# 'X.Y.dev0' is the canonical version of 'X.Y.dev'
#
__version__ = '0.1.0'

from py_wholebodymovement.articulated_figure import calculate_2d_articulated_figure_angle
from py_wholebodymovement.articulated_figure import calculate_2d_articulated_figure_angles
from py_wholebodymovement.articulated_figure import extend_2d_articulated_figure
from py_wholebodymovement.articulated_figure import calculate_3d_articulated_figure_angle
from py_wholebodymovement.articulated_figure import calculate_3d_articulated_figure_angles
from py_wholebodymovement.articulated_figure import extend_3d_articulated_figure

from py_wholebodymovement.articulated_figure import calculate_phase_locking_value
from py_wholebodymovement.articulated_figure import calculate_phase_angles
from py_wholebodymovement.articulated_figure import calculate_phase_angle_measures
from py_wholebodymovement.articulated_figure import calculate_fft_based_synchrony_measures

import py_wholebodymovement.utils.predefined_schemas as predefined_schemas

from py_wholebodymovement.utils.cleaning_utils import clean_gaussian_outliers
from py_wholebodymovement.utils.cleaning_utils import clean_dimensions_gaussian_outliers
from py_wholebodymovement.utils.cleaning_utils import denoise_data
