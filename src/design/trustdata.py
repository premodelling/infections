import os

import pandas as pd

import config


class TrustData:

    def __init__(self):
        """

        """

        self.dates = config.Config().dates()

        self.source_path = os.path.join('warehouse', 'virus', 'trusts', 'measures')

    def __read(self, trust_code):

        try:
            return pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, '{}.csv'.format(trust_code)),
                               header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

    def __dates(self, frame: pd.DataFrame):

        reference = self.dates[['date']].merge(frame, how='left', on='date')
        reference.fillna(value=0, inplace=True)

        return reference

    def exc(self, trust_code):
        """

        :param trust_code:
        :return:
        """

        frame = self.__read(trust_code=trust_code)
        frame = self.__dates(frame=frame.copy())
        frame.set_index(keys='date', drop=True, inplace=True)

        return frame
