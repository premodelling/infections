"""
The 2011 populations estimate file is different from those of other years.  Instead
of population values per age it consists of population values per age group.  This
program extracts the required age groups data for the year 2011

2011 Population Estimates: data/populations/mid2011msoaquinaryageestimates.xls
"""

import os
import collections

import numpy as np
import pandas as pd

import config


class Exceptions:

    def __init__(self):
        """
        Constructor
        """

        self.age_groups = config.Config().age_groups

        # focus
        field_names = ['filename', 'year', 'sex', 'sheets', 'header', 'cells', 'keys', 'overflow']
        Detail = collections.namedtuple(typename='Detail', field_names=field_names)
        self.detail = Detail._make(('mid2011msoaquinaryageestimates.xls', 2011, ['female', 'male'],
                                    ['Mid-2011 Females', 'Mid-2011 Males'], 3, 'A:W', ['Area Codes'], 'Area Names'))

        # The data source & storage paths
        self.source = os.path.join(os.getcwd(), 'data', 'populations')
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'populations', 'msoa', 'group')
        self.__path()

    def __path(self):
        """
        Ascertains the existence of warehouse/populations/group/

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    def __read(self) -> pd.DataFrame:
        """

        :return:
        """

        readings = []
        for index in np.arange(len(self.detail.sheets)):

            try:
                frame = pd.read_excel(io=os.path.join(self.source, self.detail.filename),
                                      sheet_name=self.detail.sheets[index], header=self.detail.header,
                                      usecols=self.detail.cells)
                print(frame.head())
                if self.detail.overflow is not None:
                    frame = frame.copy().loc[~frame[self.detail.overflow].notna(), :]
            except RuntimeError as err:
                raise Exception(err)

            frame.rename(columns={self.detail.keys[0]: 'msoa'}, inplace=True)
            frame = frame.copy().loc[frame['msoa'].str.startswith('E'), :]
            frame.loc[:, 'sex'] = self.detail.sex[index]
            frame = frame.copy()[['msoa', 'sex'] + self.age_groups]
            print(frame.head())
            
            readings.append(frame)

        return pd.concat(readings, axis=0, ignore_index=True)

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
        
    def exc(self):
        
        readings = self.__read()
        message = self.__write(frame=readings, year=self.detail.year)

        return message
