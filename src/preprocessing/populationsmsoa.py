"""
Reads the data.gov.uk population files, structures, and maps MSOA & LTLA/LAD codes
"""

import collections
import json
import os

import dask
import numpy as np
import pandas as pd

import config


class PopulationsMSOA:

    def __init__(self):
        """
        Constructor
        """

        # the expected age fields
        self.ages = config.Config().ages

        # LTLA <--> MSOA
        self.districts = config.Config().districts()

        # sources
        self.sources_path = os.path.join(os.getcwd(), 'data', 'populations')
        with open(file=os.path.join(os.getcwd(), 'data', 'populations', 'properties.json'), mode='r') as blob:
            self.sources = json.load(blob)

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'populations', 'msoa', 'single')
        self.__path()

    def __path(self):
        """

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __read(self, detail) -> pd.DataFrame:
        """
        Reads population files, # exclude extraneous data, if any, associated with field detail.overflow

        :param detail:
        :return:
        """

        readings = []
        for index in np.arange(len(detail.sheets)):

            try:
                frame = pd.read_excel(io=os.path.join(self.sources_path, detail.filename),
                                      sheet_name=detail.sheets[index],
                                      header=detail.header, usecols=detail.cells)
                if detail.overflow and detail.overflow.strip():
                    frame = frame.copy().loc[~frame[detail.overflow].notna(), :]
            except RuntimeError as err:
                raise Exception(err)

            frame.rename(columns={detail.keys[0]: 'msoa'}, inplace=True)
            frame = frame.copy().loc[frame['msoa'].str.startswith('E'), :]
            frame = frame.copy()[['msoa'] + self.ages]
            frame.loc[:, 'sex'] = detail.sex[index]
            readings.append(frame)

        return pd.concat(readings, axis=0, ignore_index=True)

    @dask.delayed
    def __merge(self, population: pd.DataFrame):
        """
        
        :param population: 
        :return: 
        """

        merged = population.merge(self.districts, how='left', on='msoa')

        return merged[['msoa', 'ltla', 'sex'] + self.ages]

    @dask.delayed
    def __write(self, frame: pd.DataFrame, year: int) -> str:
        """

        :param frame:
        :param year:
        :return:
        """

        try:
            frame.to_csv(path_or_buf=os.path.join(self.storage, '{}.csv'.format(year)),
                         index=False, header=True, encoding='utf-8')
            return '{}: succeeded'.format(year)
        except RuntimeError as err:
            raise Exception(err)

    def exc(self) -> list:
        """

        :return:
        """

        # metadata of each of the source records
        field_names = ['filename', 'year', 'sex', 'sheets', 'header', 'cells', 'keys', 'overflow']
        Detail = collections.namedtuple(typename='Detail', field_names=field_names)

        # read & process the data sets in parallel
        computations = []
        for source in self.sources:

            detail = Detail(**source)

            population = self.__read(detail=detail)
            merged = self.__merge(population=population)
            message = self.__write(frame=merged, year=detail.year)

            computations.append(message)

        dask.visualize(computations, filename='populations', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
