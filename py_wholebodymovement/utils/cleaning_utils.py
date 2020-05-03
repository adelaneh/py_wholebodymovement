#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import scipy
import pywt

def clean_gaussian_outliers(sig, sigmas=3):
	"""Fills forward the values more than `sigmas` standard deviations away from `sig`'s mean. 
	If the first value is an outlier, it is replaced with `sig`'s mean.

	Args:
		sig: iterable, the input data to be cleaned
		sigmas: int, number of standard deviations to be used for cleaning

	Returns:
		cleaned version of the input data `sig`
	"""
	for sigidx in range(len(sig)):
		if (sig[sigidx] > np.mean(sig) + sigmas * np.std(sig) or 
			sig[sigidx] < np.mean(sig) - sigmas * np.std(sig)):
			if sigidx > 0:
				sig[sigidx] = sig[sigidx-1]
			else:
				sig[sigidx] = np.mean(sig)
	return sig

def clean_dimensions_gaussian_outliers(df, sigmas=3):
	"""Cleans all the columns in the input data `df` by calling the function `clean_gaussian_outliers` 
	on them.

	Args:
		df: DataFrame, the input data
		sigmas: int, number of standard deviations to be used for cleaning

	Returns:
		a cleaned of the input data `df`
	"""
	res = pd.DataFrame(columns=df.columns)
	for col in df.columns:
		res.loc[:, col] = clean_gaussian_outliers(df.loc[:, col], sigmas=sigmas)
	return res

def denoise_data(sig, method='wavelet', **kwargs):
	"""Denoise the input data `sig` using the denoising method specified by the other arguments. 

	Note: at this moment, only the wavelet method for denoising is implemented.
	For `method='wavelet'`, we use Haar wavelet and there are two arguments that need to be specified: 
	(1) 'haarlevel' to be used to discard high-frequency components, and 
	(2) 'shrinking_factor' which determines how much the denoised signal should be shruk/expanded.

	Args:
		sig: iterable, the input data to be denoised
		method: str, the denoising method to be used
		**kwargs: dict, input arguments for the denoising method. 
	"""
	if method is None:
		raise TypeError("No denoising method provided.")
	if method not in ['wavelet', ]:
		raise ValueError("Invalid denoising method.")

	if method == 'wavelet':
		haarlevel = int(kwargs['haarlevel']) if 'haarlevel' in kwargs else 2
		shrinking_factor = float(kwargs['shrinking_factor']) if 'shrinking_factor' in kwargs else 1

		coeffs = pywt.wavedec(sig, "haar", level=haarlevel, mode="periodization")
		sig_dn = coeffs[0]

		# Cubic Spline Interpolation
		x = np.linspace(1, len(sig), len(sig_dn))
		tck = scipy.interpolate.splrep(x, sig_dn, s=0)
		xnew = np.linspace(1, len(sig), int(len(sig)/shrinking_factor))
		sig_dn_scaled = scipy.interpolate.splev(xnew, tck, der=0)

		# Calculate the Rescaling Factor
		rx = np.linspace(1, len(sig), len(sig_dn))
		rtck = scipy.interpolate.splrep(rx, sig_dn, s=0)
		rxnew = np.linspace(1, len(sig), len(sig))
		rsig_dn = scipy.interpolate.splev(rxnew, rtck, der=0)

		scale = np.mean(rsig_dn/sig)
		sig_dn_scaled /= scale

		return sig_dn_scaled

