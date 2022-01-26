import collections
import os

import dask
import pandas as pd
import requests

import config


class AgeGroupVaccinations:

    def __init__(self):
        """

        """

        # the API endpoint
        self.endpoint = 'https://api.coronavirus.data.gov.uk/v2/data'

        # the vaccinations metric, variables, etc.
        self.metric, self.variables, self.rename = config.Config().vaccinations()

        # storage
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'virus', 'ltla', 'demographic', 'vaccinations')
        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __url(self, parameters: collections.namedtuple):
        """

        :param parameters:
        :return:
        """

        dictionary = {'areaType': parameters.area_type, 'areaCode': parameters.area_code,
                      'areaName': parameters.area_name, 'date': parameters.date}
        dictionary = ['{}={}'.format(key, value) for key, value in dictionary.items() if value is not None]
        filters = str.join('&', dictionary)

        url = self.endpoint + '?{filters}&metric={metric}&format={format}'
        url = url.format(filters=filters, metric=self.metric, format='csv')

        return url

    @dask.delayed
    def __read(self, url):
        """

        :param url:
        :return:
        """

        response = requests.get(url=url, timeout=25)
        try:
            if response.status_code == 200:
                frame = pd.read_csv(filepath_or_buffer=url)
            else:
                frame = pd.DataFrame()
        except RuntimeError as err:
            frame = pd.DataFrame()

        return frame

    @dask.delayed
    def __structure(self, frame: pd.DataFrame):
        """

        :param frame:
        :return:
        """

        if not frame.empty:
            data = frame.copy()[self.variables]
            pivoted = data.pivot(index='date', columns='age', values='newPeopleVaccinatedCompleteByVaccinationDate')
            pivoted.reset_index(drop=False, inplace=True)
            return pivoted.rename(columns=self.rename)
        else:
            return frame

    @dask.delayed
    def __write(self, frame: pd.DataFrame, parameters: collections.namedtuple) -> str:
        """

        :param frame:
        :param parameters:
        :return:
        """

        try:
            if not frame.empty:
                frame.to_csv(path_or_buf=os.path.join(self.storage, '{}.csv'.format(parameters.area_code)),
                             index=False, header=True, encoding='utf-8')
                return '{}: succeeded'.format(parameters.area_code)
            else:
                return '{}: no data'.format(parameters.area_code)
        except RuntimeError as err:
            raise Exception(err)

    def exc(self, area_codes: list, area_type: str):
        """

        :param area_codes:
        :param area_type:
        :return:
        """

        # API filter parameters
        FilterParameters = collections.namedtuple(
            typename='FilterParameters', field_names=['area_code', 'area_type', 'area_name', 'date'], defaults=None)
        parameters_ = [FilterParameters(area_code=area_code, area_type=area_type, area_name=None, date=None)
                       for area_code in area_codes]

        computations = []
        for parameters in parameters_:
            url = self.__url(parameters=parameters)
            frame = self.__read(url=url)
            frame = self.__structure(frame=frame)
            message = self.__write(frame=frame, parameters=parameters)
            computations.append(message)

        dask.visualize(computations, filename='vaccinations', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
