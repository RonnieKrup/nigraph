### imports ###
import pathlib
from typing import Union, Tuple
import numpy as np
import nibabel as nb
import os
import warnings
from . import connectivity, read_files
import pandas as pd
import networkx as nx
###


def save_results(func):
    """ decorator to save property data for further use"""
    def new_function(self):
        if func.__name__ not in self.saved_results:
            self.saved_results[func.__name__] = func(self)
        return self.saved_results[func.__name__]
    return new_function


class Scan:
    def __init__(self):
        self.path = ''
        self.atlas = {'parc': '', 'meta:': ''}
        self.roi = ''
        self.saved_results = {}
        self.data_type = ''
        self.seed_prefix = ''

    def set_file(self, filepath: Union[pathlib.Path, str]):
        """ file can be nifti or cifti for fMRI, .tck or .mat (output from eDTI) for tracts"""
        if os.path.isfile(filepath):
            self.path = filepath
            self.saved_results = {}
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
        if metadata is not available, indices and labels are the unique values of parc
        """
        if os.path.isfile(parc_path) and (os.path.isfile(meta_path) or meta_path == ''):
            self.atlas['parc'] = parc_path
            self.atlas['meta'] = meta_path
            self.saved_results = {}
        else:
            warnings.warn('One of the files was not found, Parcellation not loaded')

    def set_roi(self, roi_path, prefix=''):
        """roi will be nifti"""
        if os.path.isfile(roi_path):
            self.roi = roi_path
            self.seed_prefix = prefix
        else:
            warnings.warn('ROI file not found. ROI not loaded')

    @property
    @save_results
    def connectivity_matrix(self) -> np.ndarray:
        """computes connectivity matrix"""
        if self.data_type == 'tracts':
            parc = read_files.read_nifti(self.atlas['parc'])
            tracts = read_files.read_tracts(self.path)
            matrix = connectivity.connectivity_matrix_diffusion(tracts, self.labels, parc)
        else:
            parc = read_files.read_fmri(self.atlas['parc'])
            dat = read_files.read_fmri(self.path)
            matrix = connectivity.connectivity_matrix_fmri(dat, self.labels, parc)
        return matrix

    @property
    @save_results
    def connectivity_graph(self):
        graph = nx.from_numpy_matrix(self.connectivity_matrix)
        return graph

    @property
    @save_results
    def labels(self):
        if self.atlas['meta'] == '':
            if self.data_type == 'tracts':
                parc = read_files.read_nifti(self.atlas['parc'])
            else:
                parc = read_files.read_fmri(self.atlas['parc'])
            indices = [x for x in np.unique(parc) if x > 0]
            meta = pd.DataFrame(np.transpose([indices, indices]), columns=['index', 'area'])
            meta = meta.set_index('index')
        else:
            meta = read_files.read_metadata_atlas(self.atlas['meta'])
        return meta

    def measure(self, measure_name) -> float:
        """computes given measure.
        measure name can accept both full name and abbreviation:
        - cc: closness centrality
        - msp: mean shortest path
        - dd: degree distribution
        - nc: node connectivity
        - ec: edge connectivity"""
        measures = {'closness centrality': 'cc',
                    'mean shortest path': 'msp',
                    'degree distribution': 'dd',
                    'node connectivity': 'nc',
                    'edge connectivity': 'ec',
                    'mean clustering coefficient': 'mcc'}
        if measure_name in measures.keys():
            measure_name = measures[measure_name]
        elif measure_name not in measures.values():
            warnings.warn('no such measure implemented')
            return 0
        return getattr(self, measure_name)

    @property
    def seed_based(self) -> nb.nifti1:
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
            return_val = seed_map
        else:
            return_val = None
        if self.seed_prefix == '':
            warnings.warn('no prefix added, map will not be saved')
        else:
            img = nb.Nifti1Image(seed_map, affine=None)
            split_roi = os.path.split(self.roi)
            path = os.path.join(split_roi[0], self.seed_prefix + '_' + split_roi[-1])
            nb.save(img, path)
        return return_val

    @property
    @save_results
    def msp(self):
        """compute mean shortest path.
        Distances are computed by 1/correlation for fMRI and by 1/number_of_tracts for diffusion.
        connectivity.
        For non-binary map dijkstra algorithm is used.
        """
        if np.any(self.connectivity_matrix.astype(int) > 1):
            cm2 = 1 / self.connectivity_matrix
            cm2[self.connectivity_matrix == 0] = 0
            cm2 = 200 * cm2
            g = nx.from_numpy_matrix(cm2)
            msp = dict(nx.all_pairs_dijkstra_path_length(g))
            mean_ds = []
            for i in msp:
                pairs = msp[i]
                d = 1 / np.array([x for x in pairs.values() if x > 0])
                if len(d) > 0:
                    mean_ds.append(np.mean(d))
            msp = 1 / np.mean(np.array(mean_ds))

        else:
            cm = self.connectivity_matrix.astype(int)
            g = nx.from_numpy_matrix(cm)
            msp = nx.average_shortest_path_length(g)
        return msp

    @property
    @save_results
    def cc(self):
        """compute the closeness centrality"""
        cc = nx.closeness_centrality(self.connectivity_graph)
        return np.mean(list(cc.values()))

    @property
    @save_results
    def dd(self):
        """compute mean degree for this graph"""
        vec = list(dict(self.connectivity_graph.degree).values())
        mean_deg = np.mean(vec)
        return mean_deg

    @property
    @save_results
    def nc(self):
        """compute node connectivity for this graph"""
        return nx.average_node_connectivity(self.connectivity_graph)

    @property
    @save_results
    def ec(self):
        """compute edge connectivity for this graph"""
        return nx.edge_connectivity(self.connectivity_graph)

    @property
    @save_results
    def mcc(self):
        """compute mean clustering coefficient"""
        return nx.edge_connectivity(self.connectivity_graph)
