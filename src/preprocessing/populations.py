import collections
import json
import os

import numpy as np
import pandas as pd

import config


class Populations:

    def __init__(self):
        """
        Constructor
        """

        # the expected age fields
        self.ages = config.Config().ages

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'populations', 'single')
        self.__path()

        # sources
        self.source = os.path.join(os.getcwd(), 'data', 'populations')
        with open(file=os.path.join(os.getcwd(), 'data', 'populations', 'properties.json'), mode='r') as blob:
            self.sources = json.load(blob)

    def __path(self):
        """
        Ascertains the existence of warehouse/populations/single

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    def __read(self, detail) -> pd.DataFrame:
        """
        Reads population files

        :param detail:
        :return:
        """

        readings = []
        for index in np.arange(len(detail.sheets)):

            try:
                # read
                frame = pd.read_excel(io=os.path.join(self.source, detail.filename),
                                      sheet_name=detail.sheets[index], header=detail.header,
                                      usecols=detail.cells)
                # exclude extraneous data, if any, associated with field detail.overflow
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
        """

        :return:
        """

        # metadata of each of the source records
        field_names = ['filename', 'year', 'sex', 'sheets', 'header', 'cells', 'keys', 'overflow']
        Detail = collections.namedtuple(typename='Detail', field_names=field_names)

        messages = []
        for source in self.sources:
            detail = Detail(**source)

            estimates = self.__read(detail=detail)
            message = self.__write(frame=estimates, year=detail.year)
            messages.append(message)

        return messages
