### imports ###
import numpy as np
import nibabel as nib
import pandas as pd 
import xml.etree.ElementTree as ET
import scipy.io as spio
import pathlib
import warnings
from scipy import signal
###


def read_nifti_fmri(file_path, get_shape):
    nif = nib.load(file_path).get_data()
    nifshape = nif.shape
    if len(nifshape) == 4:
        dtseries = nif.reshape((nifshape[3], nifshape[0] * nifshape[1] * nifshape[2]))
        dtseries = signal.detrend(dtseries)
    else:
        dtseries = nif.reshape((nifshape[0] * nifshape[1] * nifshape[2]))
    if get_shape:
        return dtseries, nifshape
    return dtseries


def read_cifti(file_path):
    cif = nib.load(file_path).get_data()
    if cif.shape[0] == 1:
        cif = np.transpose(cif)
    return cif


def read_nifti(file_path):
    nif = nib.load(file_path).get_data()
    return nif


def read_tck(file_path):
    tck = nib.streamlines.load(file_path)
    tck = tck.tractogram
    st = np.array([i for i in tck.streamlines])
    return st


def read_mat(file_path):
    tracts = spio.loadmat(file_path)
    tract_data = np.transpose(tracts['Tracts'])
    for i in range(len(tract_data)):
        tract_data[i][0] = tract_data[i][0]/tracts['VDims']
    return tract_data


def read_metadata_atlas(file_path):
    if file_path[-3:] == 'xml':
        tree = ET.parse(file_path)
        root = tree.getroot()
        ind = []
        name = []
        for i in root[1]:
            ind.append(i.attrib['index'])
            name.append(i.text)
        x = pd.DataFrame(np.transpose([ind, name]), columns=['index', 'area'])
        x = x.set_index('index')
        return x

    elif file_path[-3:] == 'txt':
        label = pd.read_csv(file_path, header=None, sep=' ', names=['ind', 'area', 'real_index'])
        label = label.set_index('real_index')
        return label
    warnings.warn('The file type is not compatible. File not saved!')


def read_tracts(file_path):
    suff = pathlib.Path(file_path).suffixes
    if suff == '.tck':
        return read_tck(file_path)
    elif suff == '.mat':
        return read_mat(file_path)
    else:
        warnings.warn('The file type is not compatible. File not saved!')


def read_fmri(file_path, get_shape=False):
    suff = pathlib.Path(file_path).suffixes
    if '.nii' in suff:
        if suff[0] == '.nii':
            return read_nifti_fmri(file_path, get_shape)
        else:
            return read_cifti(file_path)
    else:
        warnings.warn('The file type is not compatible. File not saved!')