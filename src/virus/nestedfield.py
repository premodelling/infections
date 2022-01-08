import collections
import json
import logging

import requests


class NestedField:

    def __init__(self, field: str):
        """

        :param field:
        """

        self.field = field

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def endpoint():

        return 'https://api.coronavirus.data.gov.uk/v1/data'

    @staticmethod
    def filters(parameters: collections.namedtuple) -> str:
        """

        :param parameters:
        :return:
        """

        dictionary = {'areaType': parameters.area_type, 'areaCode': parameters.area_code,
                      'areaName': parameters.area_name, 'date': parameters.date}
        dictionary = ['{}={}'.format(key, value) for key, value in dictionary.items() if value is not None]

        return str.join(';', dictionary)

    def structure(self) -> str:
        """

        :return:
        """

        fields = {'date': 'date', self.field: self.field}

        return json.dumps(obj=fields, separators=(',', ':'))

    def __request(self, params: dict):

        try:
            response = requests.get(url=self.endpoint(), params=params)
            response.raise_for_status()
        except requests.RequestException as err:
            raise Exception(err)

        # status check
        if response.status_code > 204:
            raise RuntimeError(response.text)
        elif response.status_code == 204:
            return None
        else:
            return response.json()

    def exc(self, parameters: collections.namedtuple):

        params = {'filters': self.filters(parameters=parameters), 'structure': self.structure()}

        return self.__request(params=params)
