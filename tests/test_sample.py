from nigraph.nigraph import Scan
import numpy as np
# Sample Test passing with nose and pytest


data = Scan()
data.set_file(r'C:\Users\Ronnie\Documents\PHD\schoolwork\pythonCourse\nigraph\nigraph\example_data\fmri\nifti_subject.nii.gz')
data.set_roi(r'C:\Users\Ronnie\Documents\PHD\schoolwork\pythonCourse\nigraph\nigraph\example_data\parcel34.nii.gz')
x = data.seed_based
print(x.shape)
print(np.max(x))
