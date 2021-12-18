"""
In progress:

Reads the lower tier local authority (LTLA), i.e., local area districts (LAD), data
mapped to its middle super output area children.  Refer to data/gis/districts/README.md

"""
import collections
import json
import logging
import os

import dask
import pandas as pd


class Districts:

    def __init__(self):
        """
        Constructor
        """

        # logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d')
        self.logger = logging.getLogger(__name__)

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'geography', 'districts')
        self.__path()

        # sources
        self.sourcepath = os.path.join(os.getcwd(), 'data', 'gis', 'districts')
        with open(file='data/gis/districts/properties.json', mode='r') as blob:
            self.sources = json.load(blob)

    def __path(self):
        """

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __read(self, detail):
        """
        
        :param detail: a named tuple of features w.r.t. a file to be read
        :return: 
        """

        try:
            readings = pd.read_csv(filepath_or_buffer=os.path.join(self.sourcepath, detail.filename),
                                   header=0, usecols=detail.fields, encoding='utf8')
        except RuntimeError as err:
            raise Exception(err)

        readings.drop_duplicates(inplace=True)

        return readings

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

    def exc(self):
        """

        :return:
        """

        # the details of the metadata of each of the source records
        Detail = collections.namedtuple(typename='Detail', field_names=['year', 'filename', 'fields'])

        computations = []
        for source in self.sources:
            detail = Detail(**source)
            readings = self.__read(detail=detail)
            message = self.__write(frame=readings, year=detail.year)
            computations.append(message)

        dask.visualize(computations, filename='districts', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
