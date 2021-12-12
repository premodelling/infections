import json
import pandas as pd


class Measures:

    def __init__(self, fields):
        """

        :param fields:
        """

        self.fields = fields

    @staticmethod
    def url():
        """

        :return:
        """

        endpoint = 'https://api.coronavirus.data.gov.uk/v1/data'

        return endpoint + '?filters={filters}&structure={structure}&format={format}'

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

        :param fields:
        :return:
        """

        return json.dumps(obj=self.fields, separators=(',', ':'))

    def exc(self, area_code) -> pd.DataFrame:
        """

        :param area_code:
        :return:
        """

        url = self.url().format(filters=self.filters(area_code=area_code),
                                structure=self.structure(),
                                format='csv')

        try:
            frame = pd.read_csv(filepath_or_buffer=url)
        except RuntimeError as err:
            raise Exception(err)

        return frame
