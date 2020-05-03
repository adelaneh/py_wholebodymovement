.. image:: https://travis-ci.org/adelaneh/py_wholebodymovement.svg?branch=master
  :target: https://travis-ci.org/adelaneh/py_wholebodymovement

.. image:: https://ci.appveyor.com/api/projects/status/kj19k1w8q9v8b4tf?svg=true
  :target: https://ci.appveyor.com/project/adelaneh/py-wholebodymovement

.. image:: https://coveralls.io/repos/github/adelaneh/py_wholebodymovement/badge.svg
  :target: https://coveralls.io/github/adelaneh/py_wholebodymovement


py_wholebodymovement
=================

This repository provides abstractions and utilities for modeling, analysis and 
visualization of whole body movement data. These tools have emerged from many 
years of experience and ongoing efforts in analyzing such data in the context 
of studying motor challenges in individuals with neurodevelopmental disorders 
and as such, subject to change, improvement and expansion.

.. raw:: html

    <p align="center"><img src="https://github.com/adelaneh/py_wholebodymovement/blob/master/docs/images/silhouette.png" height="400px"></p>
    
*More details to come!*

The package is free, open-source, and BSD-licensed.

Important links
===============

* Project Homepage: http://www.columbia.edu/~aa4348/py_wholebodymovement
* Code repository: https://github.com/adelaneh/py_wholebodymovement
* Issue Tracker: https://github.com/adelaneh/py_wholebodymovement/issues

Dependencies
============

The required dependencies to build the packages are:

* pandas (provides data structures to store and manage tables)
* numpy (used to store similarity matrices and required by pandas)
* scipy (provides mathematical functionalities, for example, for interpolation)
* scikit-learn (provides mathematical and machine learning functionalities)
* matplotlib (provides tools to create plots and animations)
* pywt (used to denoise the data using wavelet transform)

Platforms
=========

py_wholebodymovement **is to be** tested on Linux, OS X and Windows.

Installation
============

See `installation instructions <docs/user_manual/installation.rst>`_.

Usage
=====

See the accompanying notebooks:

* `Preliminary analysis of gameplay data captured by PlayingForward's Gaitway toollkit <notebooks/GaitWayCapturedDataPrelimAnalysis.ipynb>`_
* More notebooks to come.

References
==========
Some of the main ideas and analysis procedures have been developed as part of
the research culminating in the following paper::

    @article{
        author={Ardalan,Adel and Assadi,Amir H. and Surgent,Olivia J. and Travers,Brittany G.},
        year={2019},
        month={12},
        title={Whole-Body Movement during Videogame Play Distinguishes Youth with Autism from Youth with Typical Development},
        journal={Scientific Reports (Nature Publisher Group)},
        volume={9},
        pages={1-11},
    } 
