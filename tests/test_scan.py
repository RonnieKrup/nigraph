from nigraph import scan
import numpy as np
import warnings

def test_dti():
    data = scan.Scan()
    dti_path = r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\mri\subject_mat.mat'
    atlas_path = r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\mri\atlas_mat.nii.gz'
    metadata_path = r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\mri\atlas_meta.txt'
    data.set_file(dti_path)
    data.set_atlas(atlas_path, metadata_path)
    connectivity = data.connectivity_matrix
    assert isinstance(connectivity, np.ndarray)

    size = len(data.labels)
    assert connectivity.shape == size




def test_fmri():
    data=scan.Scan()
    fmri_path = r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\fmri\nifti_subject.nii.gz'
    atlas_path = r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\fmri\nifti_atlas.nii.gz'
    metadata_path = '' # test without metadata file
    data.set_file(fmri_path)
    with warnings.catch_warnings(record = True) as w:
        warnings.simplefilter("always")
        data.set_atlas(atlas_path, metadata_path)
        connectivity = data.connectivity_matrix
        assert isinstance(connectivity, np.ndarray)
        size = len(data.labels)
        assert connectivity.shape == size
        assert len(w) == 1
