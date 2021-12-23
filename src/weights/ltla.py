"""
This program collates the LTLA/Trust calculations; per trust, each year's LTLA/Trust weights
are saved in a single file.

"""

import glob
import logging
import os
import pathlib
import sys

import dask.dataframe
import numpy as np


def main():

    # the distinct source file names
    names = np.array([pathlib.Path(file).stem for file in files])
    names = np.unique(names)

    # per trust, this snippet will search for the trust's files across all years, merge
    # the data, then save
    for name in names:
        logger.info(name)

        # search
        # members = glob.glob(os.path.join(source, '*', '{}.csv'.format(name)), recursive=True)

        # search for and read all the trust's files at once
        frame = dask.dataframe.read_csv(urlpath=os.path.join(source, '*', '{}.csv'.format(name)))

        # save the trust's data in a single file
        dask.dataframe.to_csv(df=frame,
                              filename=os.path.join(storage, '{}.csv'.format(name)),
                              single_file=True, index=False)


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # the source files
    source = os.path.join(root, 'warehouse', 'trusts', 'segments', 'ltla')
    files = glob.glob(os.path.join(source, '*', '*.csv'), recursive=True)

    # storage
    storage = os.path.join('warehouse', 'trusts', 'weights', 'series', 'ltla')
    if not os.path.exists(storage):
        os.makedirs(storage)

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    main()
