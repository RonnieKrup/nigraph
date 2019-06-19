### imports ###
import pathlib
from typing import Union, Tuple
import numpy as np
import nibabel as nb
import os
import warnings
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
        self.rois = {}
        self.saved_results = {}

    def set_file(self, filepath: Union[pathlib.Path, str]):
        """ file can be nifti or cifti for fMRI, .tck or .mat (output from eDTI) for tracts"""
        if os.path.isfile(filepath):
            self.path = filepath
        else:
            warnings.warn('ROI file not found. ROI not loaded')

    def set_atlas(self, parc_path: Union[pathlib.Path, str]):
        """ atlas can be nifti or cifti"""
        if os.path.isfile(parc_path):
            self.atlas['parc'] = parc_path
            self.atlas['meta'] = ''
        else:
            warnings.warn('One of the files was not found, Parcellation not loaded')

    def set_metadata(self, meta_path: Union[pathlib.Path, str]):
        """metadata must have index and label. can be .txt or .xml"""
        if os.path.isfile(meta_path):
            self.atlas['meta'] = meta_path
        else:
            warnings.warn('One of the files was not found, Parcellation not loaded')


    def add_roi(self, roi_path, roi_name):
        if os.path.isfile(roi_path):
            self.rois[roi_name] = roi_path
        else:
            warnings.warn('ROI file not found. ROI not loaded')

    @save_results
    @property
    def connectivity_matrix(self) -> Tuple[np.ndarray, np.ndarray]:
        return ''

    def measure(self, measure_name) -> float:
        return getattr(self, measure_name)

    def seed_based(self, roi_name, save_path = '') -> nb.nifti1:
        return ''
