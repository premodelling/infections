import os

import pandas as pd


class TrustData:

    def __init__(self):
        """

        """

        self.source_path = os.path.join('warehouse', 'virus', 'trusts', 'measures')

    def __read(self, trust_code):

        try:
            return pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, '{}.csv'.format(trust_code)),
                               header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

    def exc(self, trust_code):
        """

        :param trust_code:
        :return:
        """

        return self.__read(trust_code=trust_code)
