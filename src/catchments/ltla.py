import os

import dask
import numpy as np
import pandas as pd

import config


class LTLA:

    def __init__(self, reference: pd.DataFrame, year: int):
        """

        :param reference:
        :param year:
        """

        # the data & year in focus
        self.reference = reference
        self.reference.loc[:, 'year'] = year
        self.year = year

        # the expected age groups
        self.age_groups = config.Config().age_groups

        # the variables that will be part of the melted data frame that provides
        # a record per age group
        self.id_vars = ['year', 'ltla', 'ppln_ltla', 'total_trust_patients', 'patients_from_ltla_to_trust',
                        'total_patients_of_ltla', 'tfp_ltla', 'etc_ltla', 'sex']

        # storage path
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'weights', 'segments', 'ltla', str(self.year))
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
        segment = frame.copy().melt(id_vars=self.id_vars, var_name='ag', value_name='ag_ppln_ltla')

        # age group fraction of LTLA population, age group [nhs] trust factor
        segment.loc[:, 'agf_ppln_ltla'] = np.true_divide(segment.ag_ppln_ltla, segment.ppln_ltla)
        segment.loc[:, 'tfp_ltla_ag'] = np.multiply(segment.tfp_ltla, segment.agf_ppln_ltla)

        # LTLA fraction of total trust patients
        segment.loc[:, 'ltla_frac_tp'] = np.true_divide(segment.patients_from_ltla_to_trust, segment.total_trust_patients)
        segment.loc[:, 'ag_ltla_frac_tp'] = np.multiply(segment.ltla_frac_tp, segment.agf_ppln_ltla)

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

    def exc(self):
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

        dask.visualize(computations, filename='trustsLTLA', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
