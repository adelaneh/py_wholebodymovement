#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import scipy.signal as spsig

from py_wholebodymovement.utils.cleaning_utils import clean_gaussian_outliers

def calculate_2d_articulated_figure_angle(df, o_dim, e1_dim, e2_dim, z_dir=1, pos_angles=True, x_suffix='_X', y_suffix='_Y'):
    """Calculate the angle :math:`\\angle UTS` where U, T and S are specified by the arguments `e1_dim`, 
    `o_dim` and `e2_dim` respectively. This function uses the :math:`(x,y)` coordinates of the input dimensions.

    Args:
        df: DataFrame, input data
        o_dim: str, name of the angle vertex point of interest (POI) which is the prefix of the columns corresponding to its coordinates
        e1_dim: str, name of the first end point of the angle which is the prefix of the columns corresponding to its coordinates
        e2_dim: str, name of the second end point of the angle which is the prefix of the columns corresponding to its coordinates
        z_dir: float, determines whether the angle should be calculated clockwise or counterclockwise.
        pos_angles: bool, determines whether the output angle should always be a positive number between 0 and 360 (True) or could be negative (False)
        x_suffix: str, the suffix of the x ccordinate column. For example, if `o_dim` is 'Head' then its x column in `df` should be 'Head_x'.
        y_suffix: str, the suffix of the y ccordinate column. For example, if `e1_dim` is 'RightKnee' then its y column in `df` should be 'RightKnee_y'.

    Returns:
        the angle :math:`\\angle UTS` where U, T and S are specified by the arguments `e1_dim`, `o_dim` and `e2_dim` respectively

    """
    if o_dim  is None or o_dim  == "" or \
       e1_dim is None or e1_dim == "" or \
       e2_dim is None or e2_dim == "":
        raise TypeError("Invalid dimension name(s).")

    o_e1_vecs = np.array([df[e1_dim + x_suffix] - df[o_dim + x_suffix],
                          df[e1_dim + y_suffix] - df[o_dim + y_suffix],
                          df.shape[0]*[0.,]]).transpose()
    o_e2_vecs = np.array([df[e2_dim + x_suffix] - df[o_dim + x_suffix],
                          df[e2_dim + y_suffix] - df[o_dim + y_suffix],
                          df.shape[0]*[0.,]]).transpose()
    cc = np.cross(o_e1_vecs, o_e2_vecs)
    _thetas = np.arctan2(np.einsum('ij,ij->i', cc, np.array(df.shape[0]*[(0,0,z_dir)])), 
                         np.einsum('ij,ij->i', o_e1_vecs, o_e2_vecs)
                        )*180./np.pi
    if pos_angles:
        thetas = pd.Series(_thetas).apply(lambda x: x if x >= 0 else 360. + x).values
    else:
        thetas = _thetas
    if thetas is None or np.any(np.isnan(thetas)):
        raise ValueError("nan theta value for vectors " + str(o_e1_vecs) + " and " + str(o_e2_vecs))

    return thetas

def calculate_2d_articulated_figure_angles(df, angles, face=1, x_suffix='_X', y_suffix='_Y'):
    """Calculate the articulated figure angles determined by `angles` on the data in `df`. This function calls 
    `calculate_2d_articulated_figure_angle` for the angles in `angles`.

    Args:
        df: DataFrame, input data
        angles: dict, specification of the articulated figure angles to be calculated
        face: float, whether participnt is walking away from (1) or towards (-1) the recording/display device
        x_suffix: str, the suffix of the x ccordinate column
        y_suffix: str, the suffix of the y ccordinate column

    Returns:
        a DataFrame containing the articulated figure angles determined by `angles`
    """
    if angles is None or not isinstance(angles, dict):
        raise TypeError("Invalid angles.")

    if df.shape[0] == 0:
        return

    res = {}

    for angle_name in angles:
        o_dim, e1_dim, e2_dim, z_dir, pos_angles = angles[angle_name]
        _theta  		= calculate_2d_articulated_figure_angle(df, o_dim, e1_dim, e2_dim, z_dir*face, pos_angles, x_suffix, y_suffix)
        res[angle_name] = _theta
    return pd.DataFrame(res)

def extend_2d_articulated_figure(df, dims=None, copy=True, x_suffix='_X', y_suffix='_Y'):
    """Calculate extra points of interest (POIs) specified by `dims` based on the POIs in `df`. 
    This function uses the :math:`(x,y)` coordinates of the input dimensions.

    Args:
        df: DataFrame, input data
        angles: dict, specification of the extra articulated figure angles to be calculated
        copy: bool, whether to use a copy of the input data or add the calculated angles to the input DataFrame
        x_suffix: str, the suffix of the x ccordinate column
        y_suffix: str, the suffix of the y ccordinate column

    Returns:
        a DataFrame containing the consisting of the data in `df` as well as the extra points of interest (POIs) specified by `dims` based on the POIs in `df`
    """
    if dims is None or not isinstance(dims, dict):
        raise TypeError("Invalid dimension(s).")
    if len(dims) == 0:
        return df

    res = df.copy() if copy else df

    for dim_name in dims:
        x1_dim, x2_dim, y1_dim, y2_dim	= dims[dim_name]
        for idx, row in df.iterrows():
            res.loc[idx, dim_name+x_suffix] = (row[x1_dim+x_suffix] + row[x2_dim+x_suffix]) / 2.
            res.loc[idx, dim_name+y_suffix] = (row[y1_dim+y_suffix] + row[y2_dim+y_suffix]) / 2.

        return res

def calculate_3d_articulated_figure_angle(df, o_dim, e1_dim, e2_dim, pos_angles=True, x_suffix='_X', y_suffix='_Y', z_suffix='_Z'):
    """Calculate the angle :math:`\\angle UTS` where U, T and S are specified by the arguments `e1_dim`, 
    `o_dim` and `e2_dim` respectively. This function uses the :math:`(x,y,z)` coordinates of the input dimensions.

    Args:
        df: DataFrame, input data
        o_dim: str, name of the angle vertex point of interest (POI) which is the prefix of the columns corresponding to its coordinates
        e1_dim: str, name of the first end point of the angle which is the prefix of the columns corresponding to its coordinates
        e2_dim: str, name of the second end point of the angle which is the prefix of the columns corresponding to its coordinates
        z_dir: float, determines whether the angle should be calculated clockwise or counterclockwise.
        pos_angles: bool, determines whether the output angle should always be a positive number between 0 and 360 (True) or could be negative (False)
        x_suffix: str, the suffix of the x ccordinate column. For example, if `o_dim` is 'Head' then its x column in `df` should be 'Head_x'.
        y_suffix: str, the suffix of the y ccordinate column. For example, if `e1_dim` is 'RightKnee' then its y column in `df` should be 'RightKnee_y'.
        z_suffix: str, the suffix of the z ccordinate column. For example, if `e2_dim` is 'LeftElbow' then its z column in `df` should be 'LeftElbow_z'.

    Returns:
        the angle :math:`\\angle UTS` where U, T and S are specified by the arguments `e1_dim`, `o_dim` and `e2_dim` respectively

    """
    if o_dim  is None or o_dim  == "" or \
       e1_dim is None or e1_dim == "" or \
       e2_dim is None or e2_dim == "":
        raise TypeError("Invalid dimension name(s).")

    thetas = []

    for idx, row in df.iterrows():
        o_e1_vec = (row[e1_dim + x_suffix] - row[o_dim + x_suffix],
                    row[e1_dim + y_suffix] - row[o_dim + y_suffix],
                    row[e1_dim + z_suffix] - row[o_dim + z_suffix])
        o_e2_vec = (row[e2_dim + x_suffix] - row[o_dim + x_suffix],
                    row[e2_dim + y_suffix] - row[o_dim + y_suffix],
                    row[e2_dim + z_suffix] - row[o_dim + z_suffix])
        _theta = np.arctan2(np.linalg.norm(np.cross(o_e1_vec, o_e2_vec)), np.dot(o_e1_vec, o_e2_vec))*180./np.pi
        if pos_angles:
            theta = _theta if _theta > 0 else 360. + _theta
        else:
            theta = _theta
        if theta is None or np.isnan(theta):
            raise ValueError("nan theta value for vectors " + str(o_e1_vec) + " and " + str(o_e2_vec))
        thetas.append(theta)
    return thetas

def calculate_3d_articulated_figure_angles(df, angles, face=1, x_suffix='_X', y_suffix='_Y', z_suffix='_Z'):
    """Calculate the articulated figure angles determined by `angles` on the data in `df`. This function calls 
    `calculate_3d_articulated_figure_angle` for the angles in `angles`.

    Args:
        df: DataFrame, input data
        angles: dict, specification of the articulated figure angles to be calculated
        face: float, whether participnt is walking away from (1) or towards (-1) the recording/display device
        x_suffix: str, the suffix of the x ccordinate column
        y_suffix: str, the suffix of the y ccordinate column
        z_suffix: str, the suffix of the z ccordinate column

    Returns:
        a DataFrame containing the articulated figure angles determined by `angles`
    """
    if angles is None or not isinstance(angles, dict):
        raise TypeError("Invalid angles.")

    if df.shape[0] == 0:
        return

    res = {}

    for angle_name in angles:
        o_dim, e1_dim, e2_dim, _, pos_angles = angles[angle_name]
        _theta          = calculate_3d_articulated_figure_angle(df, o_dim, e1_dim, e2_dim, pos_angles, x_suffix, y_suffix, z_suffix)
        res[angle_name] = _theta
    return pd.DataFrame(res)

def extend_3d_articulated_figure(df, dims=None, copy=True, x_suffix='_X', y_suffix='_Y', z_suffix='_Z'):
    """Calculate extra points of interest (POIs) specified by `dims` based on the POIs in `df`. 
    This function uses the :math:`(x,y,z)` coordinates of the input dimensions.

    Args:
        df: DataFrame, input data
        angles: dict, specification of the extra articulated figure angles to be calculated
        copy: bool, whether to use a copy of the input data or add the calculated angles to the input DataFrame
        x_suffix: str, the suffix of the x ccordinate column
        y_suffix: str, the suffix of the y ccordinate column
        z_suffix: str, the suffix of the z ccordinate column

    Returns:
        a DataFrame containing the consisting of the data in `df` as well as the extra points of interest (POIs) specified by `dims` based on the POIs in `df`
    """
    if dims is None or not isinstance(dims, dict):
        raise TypeError("Invalid dimension(s).")
    if len(dims) == 0:
        return df

    res = df.copy() if copy else df

    for dim_name in dims:
        x1_dim, x2_dim, y1_dim, y2_dim, z1_dim, z2_dim  = dims[dim_name]
        for idx, row in df.iterrows():
            res.loc[idx, dim_name+x_suffix] = (row[x1_dim+x_suffix] + row[x2_dim+x_suffix]) / 2.
            res.loc[idx, dim_name+y_suffix] = (row[y1_dim+y_suffix] + row[y2_dim+y_suffix]) / 2.
            res.loc[idx, dim_name+z_suffix] = (row[z1_dim+z_suffix] + row[z2_dim+z_suffix]) / 2.

        return res

def calculate_phase_locking_value(df, dims, should_remove_outliers=False):
    """Calculate phase locking value (PLV)

    See https://doi.org/10.1109/IEMBS.2006.259673 for details.

    Args:
        df: DataFrame, input data
        dims: tuple, the two dimensions (angle) in `df` to compute the PLV for
        should_remove_outliers: bool, whether to remove outliers before calculating PLV

    Returns:
        tuple:

            - instantaneous phase difference of the input angles
            - PLV of the input dimensions, which is the average instantaneous phase difference
            - Hilbert transform of the first angle
            - Hilbert transform of the second angle
            - phase of the first angle
            - phase of the second angle
    """

    if df is None:
        raise TypeError("No input data provided.")
    if dims is None or not isinstance(dims, (tuple, list)):
        raise TypeError("Invalid input dimensions.")
    if len(dims) != 2:
        raise ValueError("Need two angles to compute the PLV for; %d provided."%len(dims))

    sig1        = df.loc[:, dims[0]].values
    yy1         = clean_gaussian_outliers(sig1) if should_remove_outliers else sig1
    yy1         = yy1 - np.mean(yy1)
    yy1_hilbert = spsig.hilbert(yy1)
    yy1_phase   = np.unwrap(np.angle(yy1_hilbert))

    sig2        = df.loc[:, dims[1]].values
    yy2         = clean_gaussian_outliers(sig2) if should_remove_outliers else sig2
    yy2         = yy2 - np.mean(yy2)
    yy2_hilbert = spsig.hilbert(yy2)
    yy2_phase   = np.unwrap(np.angle(yy2_hilbert))
    
    instantaneous_phase_diff = yy1_phase - yy2_phase
    avg_phase_diff = np.average(instantaneous_phase_diff)
    
    return instantaneous_phase_diff, avg_phase_diff, yy1_hilbert, yy2_hilbert, yy1_phase, yy2_phase

def calculate_phase_angles(df, dim, should_remove_outliers=False):
    """Calculate the phase angle (PA) time series of the dimension `dim` of input data `df`

    See https://doi.org/10.1016/j.ridd.2012.03.020 for details

    Args:
        df: DataFrame: input data
        dim: str, name of the `df` column to calculate PA for

    Returns:
        phase angle time series of dimension `dim` of input data `df`
    """
    if dim is None or not isinstance(dim, str):
        raise TypeError("Invalid input dimension.")

    sig    = df.loc[:, dim].values
    yy     = clean_gaussian_outliers(sig) if should_remove_outliers else sig
    yy     = yy - np.mean(yy)
    dyy_dt = np.gradient(yy)
    pa_ts  = np.array([np.arctan(dyy_dt[jj] / yy[jj])*180/np.pi for jj in range(len(yy))])
    return pa_ts

def calculate_phase_angle_measures(df, dims, should_remove_outliers=False):
    """Calculate various synchrony measures based on phase angle (PA)

    Args:
        df: DataFrame, input data
        dims: tuple, the two dimensions (angle) in `df` to compute the PA measures for
        should_remove_outliers: bool, whether to remove outliers before calculating the PA measures

    Returns:
        tuple:

            - crp: float, PA difference
            - marp: float, mean absolute relative phase over the gait cycle
            - mrp: float, sign of mean crp over the gait cycle
            - crpsd: float, standard deviation (SA) of crp over the gait cycle
    """
    if df is None:
        raise TypeError("No input data provided.")
    if dims is None or not isinstance(dims, (tuple, list)):
        raise TypeError("Invalid input dimensions.")
    if len(dims) != 2:
        raise ValueError("Need two angles to compute the measures; %d provided."%len(dims))

    pa_ts_1 = calculate_phase_angles(df, dims[0], should_remove_outliers)
    pa_ts_2 = calculate_phase_angles(df, dims[1], should_remove_outliers)

    crp       = pa_ts_1 - pa_ts_2
    marp      = np.mean(np.abs(crp))
    mrp       = np.sign(np.mean(crp))
    crpsd     = np.std(crp)

    return crp, marp, mrp, crpsd

def calculate_fft_based_synchrony_measures(df, dims, should_remove_outliers=False):
    """Calculate various synchrony measures using fast Fourier transform (FFT)

    Currently, the only calculated measure is the variance of the dominant frequencies 
    of the signals corresponding to the series in `dims` columns of `df`.

    Args:
        df: DataFrame, input data
        dims: tuple, the two dimensions (angle) in `df` to compute the PA measures for
        should_remove_outliers: bool, whether to remove outliers before calculating the PA measures

    Returns:
        tuple:

            - dominant_freqs_var: float, variance of the dominant frequencies in `dominant_freqs` (see below)
            - dominant_freqs: dict, dominant frequencies of each dimension in `dims`
    """
    if df is None:
        raise TypeError("No input data provided.")
    if dims is None or not isinstance(dims, (tuple, list)):
        raise TypeError("Invalid input dimensions.")
    if len(dims) < 2:
        raise ValueError("Need two or more angles to compute the measures; %d provided."%len(dims))

    dominant_freqs = {}

    for dim in dims:
        sig                 = df.loc[:, dim]
        yy                  = clean_gaussian_outliers(sig) if should_remove_outliers else sig
        yy                  = yy - np.mean(yy)

        yy_fft              = np.abs(np.fft.fft(yy))[0:int(len(yy)/2)]
        yy_top_freq         = np.argmax(yy_fft)
        dominant_freqs[dim] = yy_top_freq

    dominant_freqs_var = np.var(list(dominant_freqs.values()))

    return dominant_freqs_var, dominant_freqs

