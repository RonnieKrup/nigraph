from nigraph.nigraph import Scan
import numpy as np
# Sample Test passing with nose and pytest


data = Scan()
data.set_file(r'C:\Users\Ronnie\Documents\PHD\schoolwork\pythonCourse\nigraph\nigraph\example_data\mri\subjects_tck.tck')
data.set_atlas(r'C:\Users\Ronnie\Documents\PHD\schoolwork\pythonCourse\nigraph\nigraph\example_data\mri\atlas_tck.nii.gz')
x = data.connectivity_matrix
print(x.shape)
print(np.max(x))