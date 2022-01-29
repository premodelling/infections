import os

import pandas as pd
import config


class DataSample:

    def __init__(self, parent: str):
        """

        :param parent:
        """

        configurations = config.Config()
        self.modelling = configurations.modelling()

        self.__uri = os.path.join(parent, 'warehouse', 'design', 'raw', 'R1H.csv')

    def __data(self):
        """

        :return:
        """

        try:
            data = pd.read_csv(filepath_or_buffer=self.__uri, header=0,
                               encoding='utf-8', usecols=self.modelling.variables)
        except RuntimeError as err:
            raise Exception(err)

        # set the date field as the index field
        data.loc[:, 'date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        data.set_index(keys='date', drop=True, inplace=True)

        return data

    def exc(self):

        return self.__data()
