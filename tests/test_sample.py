from nigraph.nigraph import Scan
import numpy as np
# Sample Test passing with nose and pytest


data = Scan()
data.set_file(r'C:\Users\Ronnie\Documents\PHD\schoolwork\pythonCourse\nigraph\nigraph\example_data\fmri\nifti_subject.nii.gz')
data.set_atlas(r'C:\Users\Ronnie\Documents\PHD\schoolwork\pythonCourse\nigraph\nigraph\example_data\fmri\nifti_atlas.nii.gz')
x = data.connectivity_matrix
print(x.shape)
print(np.min(x))