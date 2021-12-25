import glob
import logging
import os
import pathlib

import dask.dataframe
import numpy as np


class InitialLTLA:

    def __init__(self):
        """
        Constructor
        """

        self.variables_aggregated = ['year', 'ltla', 'ppln_ltla', 'patients_from_ltla_to_trust',
                                     'total_patients_of_ltla', 'tfp_ltla', 'etc_ltla', 'total_trust_patients',
                                     'ltla_frac_tp']

        # the source files
        self.source_path = os.path.join(os.getcwd(), 'warehouse', 'weights', 'segments', 'ltla')
        self.source_files = glob.glob(os.path.join(self.source_path, '*', '*.csv'), recursive=True)

        # storage
        path = os.path.join(os.getcwd(), 'warehouse', 'weights', 'series', 'ltla')
        self.path_disaggregated = os.path.join(path, 'baseline')
        self.path_aggregated = os.path.join(path, 'aggregated')
        self.__path(paths=[self.path_aggregated, self.path_disaggregated])

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def __path(paths: list):
        """

        :param paths:
        :return:
        """

        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

    def __source_names(self):
        """
        A Trust ca have data within the directory of one or more years.  This function/method
        returns unique trust names.

        :return:
        """

        # the distinct source file names
        names = np.array([pathlib.Path(source_file).stem for source_file in self.source_files])
        return np.unique(names)

    def exc(self):

        source_names = self.__source_names()

        # per trust, this snippet will search for the trust's files across all years, merge
        # the data, then save
        computations = []
        for source_name in source_names:

            # source name
            self.logger.info(source_name)

            # search for and read all the trust's files at once
            frame = dask.dataframe.read_csv(urlpath=os.path.join(self.source_path, '*', '{}.csv'.format(source_name)))

            # save the trust's data in a single file
            dask.dataframe.to_csv(df=frame,
                                  filename=os.path.join(self.path_disaggregated, '{}.csv'.format(source_name)),
                                  single_file=True, index=False)

            reduced = frame[self.variables_aggregated].drop_duplicates()
            dask.dataframe.to_csv(df=reduced,
                                  filename=os.path.join(self.path_aggregated, '{}.csv'.format(source_name)),
                                  single_file=True, index=False)

            computations.append('{}: succeeded'.format(source_name))

        return computations
