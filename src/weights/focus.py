import os

import dask
import pandas as pd

import config


class Focus:

    def __init__(self, year: int):
        """

        """

        # focus
        self.year = year

        # configurations
        configurations = config.Config()
        self.trusts = configurations.trusts()

        # source
        self.source_path = os.path.join('warehouse', 'weights', 'series', 'ltla', 'baseline', 'disaggregated')

        # storage
        path = os.path.join('warehouse', 'weights', 'series', 'ltla', 'focus')
        self.child = os.path.join(path, 'child')
        self.parent = os.path.join(path, 'parent')
        self.__path([self.child, self.parent])

    @staticmethod
    def __path(paths):
        """

        :param paths:
        :return:
        """

        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

    @dask.delayed
    def __read(self, trust_code: str):
        """
        a trust's flow properties data that outlines associated LTLA entities

        :param trust_code:
        :return:
        """

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, '{}.csv'.format(trust_code)))
        except RuntimeError as err:
            raise Exception(err)

        frame = frame.loc[frame['year'] == self.year, :]

        return frame

    @dask.delayed
    def __parent(self, trust_code: str, blob: pd.DataFrame):
        """

        :param trust_code:
        :param blob:
        :return:
        """

        fields = ['year', 'ltla', 'ppln_ltla', 'patients_from_ltla_to_trust', 'total_patients_of_ltla',
                  'tfp_ltla', 'etc_ltla', 'total_trust_patients', 'ltla_frac_tp']

        frame = blob.copy()[fields].drop_duplicates()

        frame.to_csv(path_or_buf=os.path.join(self.parent, '{}.csv'.format(trust_code)),
                     index=False, header=True, encoding='utf-8')

        return frame

    @dask.delayed
    def __child(self, trust_code: str, blob: pd.DataFrame, parent: pd.DataFrame):
        """

        :param trust_code:
        :param blob:
        :param parent:
        :return:
        """

        keys = ['year', 'ltla', 'sex', 'ag', 'ag_ppln_ltla', 'agf_ppln_ltla', 'tfp_ltla_ag', 'ag_ltla_frac_tp']
        aggregates = blob[keys].drop(columns='sex').groupby(by=['year', 'ltla', 'ag']).agg('sum')
        aggregates.reset_index(drop=False, inplace=True)

        aggregates = aggregates.merge(parent, how='left', on=['year', 'ltla'])

        aggregates.to_csv(path_or_buf=os.path.join(self.child, '{}.csv'.format(trust_code)),
                          index=False, header=True, encoding='utf-8')

        return '{}: succeeded'.format(trust_code)

    def exc(self):
        """

        :return:
        """

        trust_codes = self.trusts.trust_code.unique()
        trust_codes = list(set(trust_codes) - {'RDZ', 'RD3'})

        computations = []
        for trust_code in trust_codes:
            print(trust_code)

            data = self.__read(trust_code=trust_code)
            parent = self.__parent(trust_code=trust_code, blob=data)
            message = self.__child(trust_code=trust_code, blob=data, parent=parent)

            computations.append(message)

        dask.visualize(computations, filename='temporary', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
