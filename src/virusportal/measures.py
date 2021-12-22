import collections
import json
import os.path

import dask

import pandas as pd


class Measures:

    def __init__(self, fields):
        """

        :param fields:
        """
        
        # the API endpoint 
        self.endpoint = 'https://api.coronavirus.data.gov.uk/v1/data'
        
        # the structure object of the API fields of interest
        self.structure = json.dumps(obj=fields, separators=(',', ':'))

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'virus', 'ltla')
        self.__path()

    def __path(self):
        """

        :return:
        """

        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __url(self, parameters: collections.namedtuple):
        """

        :param parameters:
        :return:
        """

        dictionary = {'areaType': parameters.area_type,
                      'areaCode': parameters.area_code,
                      'areaName': parameters.area_name,
                      'date': parameters.date}
        dictionary = ['{}={}'.format(key, value) for key, value in dictionary.items() if value is not None]
        filters = str.join(';', dictionary)

        url = self.endpoint + '?filters={filters}&structure={structure}&format={format}'
        url = url.format(filters=filters, structure=self.structure, format='csv')

        return url

    @dask.delayed
    def __read(self, url):
        """

        :param url:
        :return:
        """

        try:
            frame = pd.read_csv(filepath_or_buffer=url)
        except RuntimeError as err:
            raise Exception(err)

        return frame

    @dask.delayed
    def __write(self, frame: pd.DataFrame, parameters: collections.namedtuple) -> str:
        """

        :param frame:
        :param parameters:
        :return:
        """

        try:
            frame.to_csv(path_or_buf=os.path.join(self.storage, '{}.csv'.format(parameters.area_code)),
                         index=False, header=True, encoding='utf-8')
            return '{}: succeeded'.format(parameters.area_code)
        except RuntimeError as err:
            raise Exception(err)

    def exc(self, parameters_: list):
        """

        :param parameters_:
        :return:
        """

        computations = []
        for parameters in parameters_:

            url = self.__url(parameters=parameters)
            frame = self.__read(url=url)
            message = self.__write(frame=frame, parameters=parameters)
            computations.append(message)

        dask.visualize(computations, filename='measures', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
