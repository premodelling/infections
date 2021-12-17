"""
In progress

"""
import requests
import logging


class GeographicCodes:

    def __init__(self):
        """

        """
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d')
        self.logger = logging.getLevelName(__name__)

    @staticmethod
    def __read(url):
        """

        :param url:
        :return:
        """

        try:
            response = requests.get(url=url)
            response.raise_for_status()
        except requests.RequestException as err:
            raise err.strerror

        return response.json()

    def exc(self):
        """

        :return:
        """

        locators = ['https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/MSOA11_WD20_LAD20_EW_LU/'
                    'FeatureServer/0/query?where=1%3D1&outFields=MSOA11CD,MSOA11NM,LAD20CD,LAD20NM&outSR=4326&f=json',
                    'https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/MSOA11_WD19_LAD19_EW_LU/'
                    'FeatureServer/0/query?where=1%3D1&outFields=MSOA11CD,MSOA11NM,LAD19CD,LAD19NM&outSR=4326&f=json']

        for locator in locators:
            self.logger.info(self.__read(url=locator))
