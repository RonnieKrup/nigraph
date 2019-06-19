import numpy as np
import nibabel as nib
import pandas as pd 
import xml.etree.ElementTree as ET
import scipy.io as spio


def read_nifty_fmri(file_path):
    nif=nib.load(file_path).get_data()
    nifshape = nif.shape
    dtseries = nif.reshape((nifshape[3],nifshape[0]*nifshape[1]*nifshape[2]))
    return dtseries


def read_cifty(file_path):
    cif=nib.load(file_path).get_data()
    return cif


def read_nifty(file_path):
    nif=nib.load(file_path).get_data()
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
    if file_path[-3:]=='xml':
        tree = ET.parse(file_path)
        root = tree.getroot()
        ind=[]
        name=[]
        for i in root[1]:
            ind.append(i.attrib['index'])
            name.append(i.text)
        return pd.DataFrame(np.transpose([ind,name] ))

    elif file_path[-3:]=='txt':
        label=pd.read_csv(file_path,header=None,sep=' ',names=['ind','area','real_index'])
        label=label.set_index('real_index')
        return label
    

