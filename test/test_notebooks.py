import os
import shutil
import glob
import pytest


def included_notebooks():
    include = ['notebooks/part1_python_intro',
               'notebooks/part2_flopy']
    files = []
    for folder in include:
        files += glob.glob(os.path.join(folder, '*.ipynb'))
    return sorted(files)


@pytest.fixture(params=included_notebooks(), scope='module')
def notebook(request):
    return request.param


@pytest.fixture(scope='module')
def testdir(request):
    outdir = os.path.join('test/temp')
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)

    def teardown():
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
    request.addfinalizer(teardown)
    return outdir


def test_notebook(notebook, testdir):
    # run autotest on each notebook
    path, fname = os.path.split(notebook)
    cmd = 'jupyter ' + 'nbconvert ' + \
          '--ExecutePreprocessor.timeout=600 ' + \
          '--to ' + 'notebook ' + \
          '--execute ' + '{} '.format(notebook) + \
          '--output-dir ' + '{} '.format(testdir) + \
          '--output ' + '{}'.format(fname)
    ival = os.system(cmd)
    assert ival == 0, 'could not run {}'.format(fname)
