### imports ###
import pathlib
from typing import Union, Tuple
import numpy as np
import nibabel as nb
import os
import warnings
from . import connectivity, read_files
import pandas as pd
###


def save_results(func):
    """ decorator to save property data for further use"""
    def new_function(self):
        if func.__name__ not in self.func_results:
            self.saved_results = func(self)
        return self.func_results[func.__name__]
    return new_function


class Scan:
    def __init__(self):
        self.path = ''
        self.atlas = {'parc': '', 'meta:': ''}
        self.roi = ''
        self.saved_results = {}
        self.data_type = ''

    def set_file(self, filepath: Union[pathlib.Path, str]):
        """ file can be nifti or cifti for fMRI, .tck or .mat (output from eDTI) for tracts"""
        if os.path.isfile(filepath):
            self.path = filepath
            extention = pathlib.Path(filepath).suffixes
            if '.nii' in extention:
                self.data_type = 'fMRI'
            else:
                self.data_type = 'tracts'
        else:
            warnings.warn('ROI file not found. ROI not loaded')

    def set_atlas(self, parc_path: Union[pathlib.Path, str], meta_path: Union[pathlib.Path, str]=''):
        """ atlas can be nifti or cifti
        metadata must have index and label. can be .txt or .xml
        """
        if os.path.isfile(parc_path) and os.path.isfile(meta_path):
            self.atlas['parc'] = parc_path
            self.atlas['meta'] = meta_path
            self.saved_results = {}
        else:
            warnings.warn('One of the files was not found, Parcellation not loaded')

    def set_roi(self, roi_path):
        """roi will be nifti"""
        if os.path.isfile(roi_path):
            self.roi = roi_path
        else:
            warnings.warn('ROI file not found. ROI not loaded')

    @save_results
    @property
    def connectivity_matrix(self) -> np.ndarray:
        """computes connectivity matrix"""
        ##################################
        if self.data_type == 'tracts':
            parc = read_files.read_nifti(self.atlas['parc'])
            tracts = read_files.read_tracts(self.path)
            matrix = connectivity.connectivity_matrix_diffusion(tracts, self.labels, parc)
        else:
            parc = read_files.read_fmri(self.atlas['parc'])
            dat = read_files.read_fmri(self.path)
            matrix = connectivity.connectivity_matrix_fmri(dat, self.labels, parc)
        return matrix

    @save_results
    @property
    def labels(self):
        if self.atlas['meta'] == '':
            if self.data_type == 'tracts':
                parc = read_files.read_nifti(self.atlas['parc'])
            else:
                parc = read_files.read_fmri(self.atlas['parc'])
            indices = [x for x in np.unique(parc) if x > 0]
            meta = pd.DataFrame([indices, indices], index=0, columns=['index', 'area'])
        else:
            meta = read_files.read_metadata_atlas(self.atlas['meta'])
        return meta

    def measure(self, measure_name) -> float:
        """computes given measure.
        measure name can accept:
        - cc: closness centrality
        - msp: mean shortest path
        - dd: degree distribution
        - nc: node connectivity
        - ec: edge connectivity"""
        return getattr(self, measure_name)

    def seed_based(self, prefix='') -> nb.nifti1:
        """computes seed based connectivity matrix for fMRI.
        if save_path is not empty, saves the map as nifti"""
        roi_data = read_files.read_fmri(self.roi)
        data = read_files.read_fmri(self.path, get_shape=True)
        shape = None
        if isinstance(data, tuple):
            shape = data[1]
            data = data[0]
        seed_map = connectivity.seed_map(roi_data, data)
        if shape is not None:
            seed_map = seed_map.reshape(shape)

        if prefix == '':
            warnings.warn('no prefix added, map will not be saved')
        else:
            img = nb.Nifti1Image(seed_map)
            split_roi = os.path.split(self.roi)
            path = os.path.join(split_roi[0], prefix + split_roi[-1])
            nb.save(img, path)
        return seed_map

    @save_results
    @property
    def msp(self):
        pass
