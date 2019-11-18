import os
import glob
import zipfile
import shutil
import numpy as np


def make_awful_file_wrangling_example():
    basepath = '/fileio/'
    dest_path = os.path.join(basepath, 'netcdf_data/zipped')
    years = range(1980, 2018)

    for year in years:
        outdir = os.path.join(dest_path, 'zipped_{}'.format(year))
        outfile = os.path.join('12270_{}'.format(year), 'prcp.nc')
        for folder in [outdir, '12270_{}'.format(year)]:
            if not os.path.isdir(folder):
                os.makedirs(folder)
        with open(outfile, 'w') as dest:
            data = np.random.randn(2, 2)
            for line in data:
                dest.write(' '.join(map(str, line))+'\n')
        zipname = os.path.join(dest_path, 'zipped_{}'.format(year), '12270_{}.zip'.format(year))
        with zipfile.ZipFile(zipname, 'w') as zipobj:
            zipobj.write(outfile)
        os.remove(outfile)
        os.rmdir(os.path.split(outfile)[0])


def file_wrangling_solution():

    zipfiles = sorted(glob.glob('fileio/netcdf_data/zipped/*/*.zip'))
    dest_path = 'extracted_data'
    if not os.path.isdir(dest_path):
        os.makedirs(dest_path)
    variable = 'prcp'

    for f in zipfiles:
        with zipfile.ZipFile(f) as src:
            # get the path to the source file and tye year
            _, fname = os.path.split(f)
            name = os.path.splitext(fname)[0].replace('.tar', '')
            srcfile = '{}/{}.nc'.format(name, variable)
            year = name.split('_')[1]

            # where we want the extracted .nc file to end up
            destfile = os.path.join(dest_path, '{}_{}.nc'.format(variable, year))

            # extract the srcfile path to the /daymet folder
            # unfortunately this extracts the whole path, not just the file
            src.extract(srcfile, dest_path)
            # move the file up from subfolders to /daymet
            shutil.move(os.path.join(dest_path, srcfile), dest_path)
            # rename to include year
            os.rename(os.path.join(dest_path, '{}.nc'.format(variable)),
                      destfile)
            # trash subfolders that were extracted
            os.rmdir(os.path.join(dest_path, name))
            print('{}/{} --> {}'.format(f, srcfile, destfile))


if __name__ == '__main__':
    file_wrangling_solution()
