import os

import dask
import numpy as np
import pandas as pd

import config


class MSOA:

    def __init__(self, reference: pd.DataFrame, year: int):
        """

        :param reference:
        :param year:
        """

        # the data & year in focus
        self.reference = reference
        self.year = year

        # the expected age groups
        self.age_groups = config.Config().age_groups

        # the variables that will be part of the melted data frame that provides
        # a record per age group
        self.id_vars = ['year', 'msoa', 'ltla', 'ppln_msoa', 'patients_from_msoa_to_trust',
                        'total_patients_of_msoa', 'tfp_msoa', 'etc_msoa', 'sex']

        # storage path
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'trusts', 'segments', 'msoa', str(self.year))
        self.__path(self.storage)

    @staticmethod
    def __path(path: str):
        """

        :param path:
        :return:
        """

        if not os.path.exists(path):
            os.makedirs(path)

    @dask.delayed
    def __segment(self, trust: str) -> pd.DataFrame:
        """

        :param trust: the NHS Trust in focus
        :return: melted trust data, with age group level calculations
        """

        frame = self.reference.copy().loc[self.reference.trust_code == trust, :]
        frame.drop(columns='trust_code', inplace=True)
        segment = frame.copy().melt(id_vars=self.id_vars, var_name='ag', value_name='ag_ppln_msoa')

        # age group fraction of MSOA population, age group [nhs] trust factor
        segment.loc[:, 'agf_ppln_msoa'] = np.true_divide(segment.ag_ppln_msoa, segment.ppln_msoa)
        segment.loc[:, 'ag_trust_factor'] = np.multiply(segment.tfp_msoa, segment.agf_ppln_msoa)

        return segment

    @dask.delayed
    def __write(self, frame: pd.DataFrame, trust: str) -> str:
        """

        :param frame: a frame of calculations & numbers for a trust
        :param trust: the NHS Trust in focus

        :return: Status message.  Did the calculation & writing of trust patient fractions,
                 estimated trust catchments, etc., succeed?
        """

        try:
            frame.to_csv(path_or_buf=os.path.join(self.storage, '{}.csv'.format(trust)),
                         index=False, header=True, encoding='utf-8')
            return '{year}: {trust} succeeded'.format(trust=trust, year=self.year)
        except RuntimeError as err:
            raise Exception(err)

    def exc(self) -> list:
        """

        :return: Status messages.  Did the calculation & writing of trust patient fractions,
                 estimated trust catchments, etc., succeed?
        """

        trusts = self.reference.trust_code.unique()

        computations = []
        for trust in trusts:
            segment = self.__segment(trust=trust)
            message = self.__write(frame=segment, trust=trust)
            computations.append(message)

        dask.visualize(computations, filename='trustsMSOA', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
