"""
Module

Uses a data set of ages to create a data set of age groups

"""
import glob
import os

import dask
import numpy as np
import pandas as pd

import config


class AgeGroups:

    def __init__(self):
        """

        """

        configurations = config.Config()

        # The (1) required age groups, (2) the length of each age group, excluding age group 90+, (3) the
        # available ages, (4) grouping the ages, excluding 90+, into groups of length 5 each
        self.age_groups = configurations.age_groups
        age_group_length = configurations.age_group_length
        ages = configurations.ages
        self.ages = [str(age) for age in ages]
        self.groupings = [index // age_group_length for index in np.arange(0, len(self.ages) - 1)]

        # The data source & storage paths
        self.source = os.path.join(os.getcwd(), 'warehouse', 'populations', 'msoa', 'single')
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'populations', 'msoa', 'group')
        self.__path()

    def __path(self):
        """
        Ascertains the existence of warehouse/populations/group

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __read(self, filepath: str) -> pd.DataFrame:
        """

        :param filepath: The path to the data source
        :return:
        """

        try:
            frame = pd.read_csv(filepath_or_buffer=filepath, header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        return frame

    @dask.delayed
    def __calculate(self, frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        groups = pd.DataFrame(data=frame[self.ages[:-1]].groupby(by=self.groupings, axis=1).sum())
        groups.set_axis(labels=self.age_groups[0:-1], axis=1, inplace=True)

        reference = pd.concat((frame[['msoa', 'sex']], groups, frame[['90+']]), axis=1, ignore_index=False)

        return reference

    @dask.delayed
    def __write(self, frame: pd.DataFrame, filename: str) -> str:
        """

        :param frame:
        :param filename:
        :return:
        """

        try:
            frame.to_csv(path_or_buf=os.path.join(self.storage, filename),
                         index=False, header=True, encoding='utf-8')
            return '{}: succeeded'.format(filename.split('.')[0])
        except RuntimeError as err:
            raise Exception(err)

    def exc(self):
        """

        :return:
        """

        # the list of data files of ages
        filepaths = glob.glob(pathname=os.path.join(os.getcwd(), 'warehouse', 'populations', 'single', '*.csv'))

        # read & process the data sets in parallel
        computations = []
        for filepath in filepaths:

            readings = self.__read(filepath=filepath)
            calculations = self.__calculate(frame=readings)
            message = self.__write(frame=calculations, filename=os.path.basename(filepath))

            computations.append(message)

        dask.visualize(computations, filename='ageGroups', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
