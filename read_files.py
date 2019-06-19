import os
import numpy as np
from nibabel.testing import data_path
import nibabel as nib


def read_nifty(file_path):
    if file_path[-3:]=='nii':
        img=nib.load('testSarit_14_B1000_FA.nii')
        return img
    else:
        raise
    

sec_img=nib.streamlines.tck.TckFile('corpus_tracts.tck')
print(sec_img)