import json
import requests
import logging


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
    def filters(area_code: str, area_type: str = 'ltla', area_name: str = None, date: str = None) -> str:
        """

        :param area_code:
        :param area_type: the default value is Lower-tier local authority
        :param area_name:
        :param date:
        :return:
        """

        dictionary = {'areaType': area_type, 'areaCode': area_code, 'areaName': area_name, 'date': date}
        dictionary = ['{}={}'.format(key, value) for key, value in dictionary.items() if value is not None]

        return str.join(';', dictionary)

    def structure(self) -> str:
        """

        :return:
        """

        fields = {'date': 'date', self.field: self.field}

        return json.dumps(obj=fields, separators=(',', ':'))

    def exc(self, area_code: str):

        params = {'filters': self.filters(area_code=area_code), 'structure': self.structure()}

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
