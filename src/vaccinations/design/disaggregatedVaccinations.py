import os

import numpy as np
import pandas as pd

import src.vaccinations.design.weights
import config


class DisaggregatedVaccinations:

    def __init__(self, weights_of_year: int):

        configurations = config.Config()
        self.dates = configurations.dates()

        # age groups
        self.age_groups = ['12-15', '16-17', '18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54',
                           '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']

        # weights
        self.weights = src.vaccinations.design.weights.Weights(weights_of_year=weights_of_year)

        # path
        self.source_path = os.path.join('warehouse', 'virus', 'ltla', 'demographic', 'vaccinations')

    def __weights(self, trust_code):

        return self.weights.disaggregated(trust_code=trust_code)

    def __read(self, ltla_code: str):
        """

        :param ltla_code: a LTLA code
        :return: the data set of a LTLA
        """

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, '{}.csv'.format(ltla_code)))
        except RuntimeError as err:
            raise Exception(err)

        return frame[['date'] + self.age_groups]

    def __constants(self, ltla_code: str, weights: pd.DataFrame) -> pd.DataFrame:

        factors = weights.loc[weights.ltla == ltla_code, ['ltla', 'ag', 'tfp_ltla_ag']]
        factors = factors.pivot(index='ltla', columns='ag', values='tfp_ltla_ag')
        factors.reset_index(drop=True, inplace=True)
        constants = factors[self.age_groups]

        return constants

    def __melt(self, frame: pd.DataFrame, ltla_code: str) -> pd.DataFrame:

        # foremost, ensure all dates within the dates range exists
        reference = self.dates[['date']].merge(frame, how='left', on='date')
        reference.fillna(value=0, inplace=True)

        # hence, melt
        temporary = reference.melt(id_vars='date', var_name='age_group', value_name=ltla_code)
        temporary.set_index(keys=['date', 'age_group'], inplace=True)

        return temporary

    def __aggregates(self, computations: list) -> pd.DataFrame:

        if len(computations) > 1:
            blob = pd.concat(computations, ignore_index=False, axis=1)
        else:
            blob = computations[0]

        frame = blob.sum(axis=1).to_frame(name='daily_vaccinations')
        frame.reset_index(drop=False, inplace=True)
        restructured: pd.DataFrame = frame.pivot(index='date', columns='age_group', values='daily_vaccinations')
        restructured.set_axis(labels=['EDV{}'.format(age_group) for age_group in self.age_groups],
                              axis='columns', inplace=True)

        return restructured

    def exc(self, trust_code):
        """

        :return:
        """

        weights = self.__weights(trust_code=trust_code)
        ltla_codes = weights.ltla.unique()

        computations = []
        for ltla_code in ltla_codes:

            if os.path.exists(os.path.join(self.source_path, '{}.csv'.format(ltla_code))):
                # row of weight per age group: constants
                constants = self.__constants(ltla_code=ltla_code, weights=weights)

                # matrix of daily cases, of a LTLA, per age group: values
                readings = self.__read(ltla_code=ltla_code)
                values = readings[self.age_groups]
                totals = values.sum(axis=1).values.reshape((values.shape[0], -1))

                # special
                conditions = (values > 0).astype(int)
                states = np.multiply(conditions, constants)
                denominators = states.sum(axis=1).values
                denominators = np.repeat(denominators.reshape((denominators.shape[0], -1)),
                                         len(self.age_groups), axis=1)

                np.seterr(invalid='ignore')
                adjuster = np.true_divide(states.values, denominators)
                np.seterr(invalid='warn')
                adjuster = constants.sum(axis=1).values[0] * adjuster

                # assigning proportions of the LTLA daily cases to the trust via the weights
                frame = readings.copy()
                frame.loc[:, self.age_groups] = np.multiply(adjuster, totals)

                # melt
                temporary = self.__melt(frame=frame, ltla_code=ltla_code)

                # append
                computations.append(temporary)

        return self.__aggregates(computations=computations)
