"""
In progress:

Reads the lower tier local authority (LTLA), i.e., local area districts (LAD), data
mapped to its middle super output area children.  The data is read via the Open
Geographic Portal API (https://geoportal.statistics.gov.uk)

"""
import requests
import collections
import os
import logging
import pandas as pd
import dask
import json


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
        with open(file='data/gis/districts/properties.json', mode='r') as blob:
            self.sources = json.load(blob)

    def __path(self):
        """

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __read(self, url: str, segment: str):
        """

        :param url:
        :param segment:
        :return:
        """

        try:
            response = requests.get(url=url)
            response.raise_for_status()
        except requests.RequestException as err:
            raise err.strerror

        dictionary = response.json()
        readings = pd.json_normalize(data=dictionary[segment])
        readings.rename(mapper=lambda x: x.split('.')[1], axis=1, inplace=True)

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
        Detail = collections.namedtuple(typename='Detail', field_names=['year', 'api', 'segment'])

        computations = []
        for source in self.sources:
            detail = Detail(**source)
            readings = self.__read(url=detail.api, segment=detail.segment)
            message = self.__write(frame=readings, year=detail.year)
            computations.append(message)

        dask.visualize(computations, filename='districts', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
