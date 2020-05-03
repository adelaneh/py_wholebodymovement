# coding=utf-8

import os
import numpy as np

from py_wholebodymovement.utils import install_path

def get_install_path():
    path_list = install_path.split(os.sep)
    return os.sep.join(path_list[0:len(path_list) - 1])

