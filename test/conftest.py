import pytest
import glob

@pytest.fixture(scope="session")
def ref_fits():
    filenames = glob.glob("test/ref/*.fits")
    fitsfile = fits.open(filenames[0])[0]
    yield fitsfile
    fitsfile.close()
     
@pytest.fixture(scope="session")
def sources_fits():
    filenames = glob.glob("test/sources/*.fits")
    fitsfiles = [fits.open(f)[0] for f in filenames]
    yield fitsfiles
    for f in fitsfiles:
        f.close()
