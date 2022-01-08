import os.path

import dask

import pandas as pd

import src.design.trustdata
import src.design.disaggregatedCases
import src.design.aggregatedMeasures

import config


class Matrix:

    def __init__(self):

        # initiating
        self.am = src.design.aggregatedMeasures.AggregatedMeasures()

        # configurations
        configurations = config.Config()
        self.trusts = configurations.trusts()

        # storage
        self.storage = os.path.join('warehouse', 'design', 'raw')
        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

    @dask.delayed
    def __trust(self, trust_code):
        """

        :param trust_code:
        :return: trust level data
        """

        return src.design.trustdata.TrustData().exc(trust_code=trust_code)

    @dask.delayed
    def __disaggregated_cases(self, trust_code):
        """

        :param trust_code: NHS Trust code
        :return: returns disaggregated trust level cases per age group determined via weights & LTLA cases
        """

        return src.design.disaggregatedCases.DisaggregatedCases().exc(trust_code=trust_code)

    @dask.delayed
    def __aggregated_measures(self, trust_code, field):
        """

        :param trust_code: NHS Trust code
        :param field: measure of interest, e.g., dailyCases, etc.
        :return: returns estimated trust level measures determined via weights & LTLA level measures
        """

        return self.am.exc(trust_code=trust_code, field=field)

    @dask.delayed
    def __merge(self, trust, disaggregated_cases, cases_, first_, second_):
        """

        :param trust:
        :param disaggregated_cases:
        :param cases_:
        :param first_:
        :param second_:
        :return: a raw design matrix
        """

        return pd.concat((trust, disaggregated_cases, cases_, first_, second_), axis=1, ignore_index=False)

    @dask.delayed
    def __write(self, frame: pd.DataFrame, trust_code: str):
        """

        :param frame:
        :param trust_code:
        :return:
        """

        try:
            frame.to_csv(path_or_buf=os.path.join(self.storage, '{}.csv'.format(trust_code)),
                         index=True, header=True, encoding='utf-8')
            return '{} succeeded'.format(trust_code)
        except RuntimeError as err:
            raise Exception(err)

    def exc(self):

        trust_codes = self.trusts.trust_code.unique()
        trust_codes = list(set(trust_codes) - {'RD3', 'RDZ'})

        computations = []
        for trust_code in trust_codes:

            trust = self.__trust(trust_code=trust_code)
            disaggregated_cases = self.__disaggregated_cases(trust_code=trust_code)

            cases_ = self.__aggregated_measures(trust_code=trust_code, field='dailyCases')
            first_ = self.__aggregated_measures(trust_code=trust_code, field='dailyFirstDoseByVaccinationDate')
            second_ = self.__aggregated_measures(trust_code=trust_code, field='dailySecondDoseByVaccinationDate')

            frame = self.__merge(trust, disaggregated_cases, cases_, first_, second_)

            message = self.__write(frame=frame, trust_code=trust_code)
            computations.append(message)

        dask.visualize(computations, filename='designMatrix', format='pdf')
        messages = dask.compute(computations, scheduler='processes')

        return messages
