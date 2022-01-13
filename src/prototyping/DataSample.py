import os

import pandas as pd


class DataSample:

    def __init__(self, parent: str):
        """

        """

        self.__uri = os.path.join(parent, 'warehouse', 'design', 'raw', 'R1H.csv')

    def __data(self):

        try:
            data = pd.read_csv(filepath_or_buffer=self.__uri, header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

        # the data object includes disaggregated alternatives of the first three, the last a relatively new field
        data.drop(columns=['dailyCases', 'dailyFirstDoseByVaccinationDate', 'dailySecondDoseByVaccinationDate',
                           'dailyThirdInjectionByVaccinationDate'],
                  inplace=True)

        # set the date field as the index field
        data.loc[:, 'date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        data.set_index(keys='date', drop=True, inplace=True)

        return data

    def exc(self):

        return self.__data()
