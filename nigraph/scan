### imports ###
import pathlib
from typing import Union, Tuple
import numpy as np
import nibabel as nb
###


def save_results(func):
    def new_function(self):
        if func.__name__ not in self.func_results:
            self.saved_results = func(self)
        return self.func_results[func.__name__]
    return new_function


class Scan:
    def __init__(self, filepath: Union[pathlib.Path, str]):
        self.path = filepath
        self.atlas = {'parc': '', 'meta:': ''}
        self.rois = {}
        self.saved_results = {}

    def set_atlas(self, parc_path: Union[pathlib.Path, str], meta_path: Union[pathlib.Path, str]):
        self.atlas['parc'] = parc_path
        self.atlas['meta'] = meta_path

    def add_roi(self, roi_path, roi_name):
        self.rois[roi_name] = roi_path

    @save_results
    @property
    def connectivity_matrix(self) -> Tuple[np.ndarray, np.ndarray]:
        return ''

    def measure(self, measure_name) -> float:
        return getattr(self, measure_name)

    def seed_based(self, roi_name, save_path = '') -> nb.nifti1:
        return ''
