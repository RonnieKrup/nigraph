from nigraph import scan,read_files
import warnings

def test_set_file():
    data=scan.Scan()
    with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
    # Trigger a warning.
        data.set_file(r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\README.r')
    # Verify some things
        assert len(w) > 0
    
def test_set_atlas_wrong_suffix():
    data=scan.Scan()
    with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
    # Trigger a warning.
        data.set_atlas(r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\README.r')
    # Verify some things
        assert len(w) > 0

def test_set_atlas_no_file():
    data=scan.Scan()
    with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
    # Trigger a warning.
        data.set_atlas(r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\README.txt')
    # Verify some things
        assert len(w) > 0

def test_set_roi():
    data=scan.Scan()
    with warnings.catch_warnings(record=True) as w:
    # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
    # Trigger a warning.
        data.set_roi(r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\README.r')
    # Verify some things
        assert len(w) > 0

def test_read_fmri():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        read_files.read_fmri(r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\README.rst')
        assert len(w)>0

def test_read_tracts():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        read_files.read_tracts(r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\README.rst')
        assert len(w)>0

def test_read_metadata():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        read_files.read_metadata_atlas(r'C:\Users\YossiYNB9\Desktop\hackathon\nigraph\README.rst')
        assert len(w)>0    