import os

import dask
import numpy as np
import pandas as pd

import config


class MSOA:

    def __init__(self, year: int):
        """

        :param year:
        """

        # the year in focus
        self.year = year

        # the expected age groups
        self.age_groups = config.Config().age_groups

        # the variables that will be part of the melted data frame that provides
        # a record per age group
        self.id_vars = ['msoa', 'ltla', 'ppln_msoa', 'ppln_ltla', 'patients_from_msoa_to_trust',
                        'total_patients_of_msoa', 'tfp_msoa', 'etc_msoa', 'sex']

        # storage path
        self.storage = os.path.join(os.getcwd(), 'warehouse', 'segments', 'msoa', 'trusts')
        self.__path(self.storage)

    @staticmethod
    def __path(path: str):

        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def __trust(frame: pd.DataFrame):
        """
        * trust fraction of patients (tfp) w.r.t. a MSOA
        * estimated trust catchment (etc) w.r.t. a MSOA

        :param frame:
        :return:
        """

        frame.loc[:, 'tfp_msoa'] = np.true_divide(frame.patients_from_msoa_to_trust, frame.total_patients_of_msoa)
        frame.loc[:, 'etc_msoa'] = np.multiply(frame.tfp_msoa, frame.ppln_msoa)

        return frame

    @dask.delayed
    def __segment(self, trust: str, reference) -> pd.DataFrame:
        """

        :param trust: the NHS Trust in focus
        :param reference:
        :return:
        """

        frame = reference.copy().loc[reference.trust_code == trust, :]
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

        :return: Status message > Did the calculation & writing of trust patient fractions,
                 estimated trust catchments, etc., succeed?
        """

        path = os.path.join(self.storage, trust)
        self.__path(path=os.path.join(self.storage, trust))

        try:
            frame.to_csv(path_or_buf=os.path.join(path, '{}.csv'.format(self.year)),
                         index=False, header=True, encoding='utf-8')
            return '{year}: {trust} succeeded'.format(trust=trust, year=self.year)
        except RuntimeError as err:
            raise Exception(err)

    def exc(self, patients: pd.DataFrame, populations: pd.DataFrame):
        """

        :param patients: The data frame of MSOA/NHS Trust patients for the year self.year
        :param populations: The populations of the year self.year

        :return: Processing status messages > Did the calculation & writing of trust patient fractions,
                 estimated trust catchments, etc., per trust succeed?
        """

        reference = populations.merge(patients.drop(columns='catchment_year'), how='right', on='msoa')
        reference = self.__trust(frame=reference.copy())
        trusts = reference.trust_code.unique()

        computations = []
        for trust in trusts:
            segment = self.__segment(trust=trust, reference=reference)
            message = self.__write(frame=segment, trust=trust)
            computations.append(message)

        dask.visualize(computations, filename='trustsMSOA', format='pdf')
        messages = dask.compute(computations, scheduler='processes')[0]

        return messages
