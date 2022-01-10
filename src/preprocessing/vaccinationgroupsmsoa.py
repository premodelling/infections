"""
Uses data sets of ages to create data sets of age groups
"""
import glob
import os

import dask
import numpy as np
import pandas as pd


class VaccinationGroupsMSOA:

    def __init__(self):
        """
        Constructor
        """

        # data sources
        self.sources_path = os.path.join(os.getcwd(), 'warehouse', 'populations', 'msoa', 'single')
        self.sources = glob.glob(pathname=os.path.join(self.sources_path, '*.csv'))

        # storage path
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'populations', 'msoa', 'reference', 'vaccinations')
        self.__path()

    def __path(self):
        """
        Ascertains the existence of warehouse/populations/group

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __read(self, source: str) -> pd.DataFrame:
        """

        :param source: The path to the data source
        :return:
        """

        try:
            frame = pd.read_csv(filepath_or_buffer=source, header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        return frame

    @dask.delayed
    def __uneven(self, frame: pd.DataFrame) -> pd.DataFrame:

        agegroups = ['12-15', '16-17', '18-24']

        ages = list(np.arange(start=12, stop=25))
        agestext = [str(age) for age in ages]

        def label(x): return 0 if (x < 16) else (2 if x > 17 else 1)
        labels = [label(age) for age in ages]

        groups = pd.DataFrame(data=frame[agestext].groupby(by=labels, axis=1).sum())
        groups.set_axis(labels=agegroups, axis=1, inplace=True)

        return groups

    @dask.delayed
    def __standard(self, frame: pd.DataFrame) -> pd.DataFrame:

        agegroups = ['25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64',
                     '65-69', '70-74', '75-79', '80-84', '85-89']
        agegrouplength = 5

        ages = list(np.arange(start=25, stop=90))
        agestext = [str(age) for age in ages]

        labels = [index // agegrouplength for index in np.arange(0, len(agestext))]

        groups = pd.DataFrame(data=frame[agestext].groupby(by=labels, axis=1).sum())
        groups.set_axis(labels=agegroups, axis=1, inplace=True)

        return groups

    @dask.delayed
    def __merge(self, frame: pd.DataFrame, initial: pd.DataFrame, inbetween: pd.DataFrame):

        return pd.concat((frame[['msoa', 'ltla', 'sex']], initial, inbetween,
                          frame[['90+']]), axis=1, ignore_index=False)

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

        # read & process the data sets in parallel
        computations = []
        for source in self.sources:
            readings = self.__read(source=source)
            initial = self.__uneven(frame=readings)
            inbetween = self.__standard(frame=readings)
            reference = self.__merge(frame=readings, initial=initial, inbetween=inbetween)
            message = self.__write(frame=reference, filename=os.path.basename(source))

            computations.append(message)

        dask.visualize(computations, filename='vaccinationGroupsMSOA', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
