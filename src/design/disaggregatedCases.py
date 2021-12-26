import os
import pandas as pd
import numpy as np

import config


class DisaggregatedCases:

    def __init__(self):

        configurations = config.Config()
        self.age_groups = configurations.age_groups
        self.dates = configurations.dates()

        self.source_path = os.path.join('warehouse', 'virus', 'ltla', 'demographic', 'cases')
        self.weights_path = os.path.join('warehouse', 'weights', 'series', 'ltla', 'focus', 'child')

    def __weights(self, trust_code):

        try:
            return pd.read_csv(filepath_or_buffer=os.path.join(self.weights_path, '{}.csv'.format(trust_code)))
        except RuntimeError as err:
            raise Exception(err)

    def __read(self, ltla_code: str):
        """
        Reads the data set of a LTLA via its code

        :param ltla_code: a LTLA code
        :return:
        """

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, '{}.csv'.format(ltla_code)))
        except RuntimeError as err:
            raise Exception(err)

        return frame[['date'] + self.age_groups]

    def __constants(self, ltla_code: str, weights: pd.DataFrame):
        """

        :param ltla_code: a LTLA code
        :return:
        """

        factors = weights.loc[weights.ltla == ltla_code, ['ltla', 'ag', 'tfp_ltla_ag']]
        factors = factors.pivot(index='ltla', columns='ag', values='tfp_ltla_ag')
        factors.reset_index(drop=True, inplace=True)
        constants = factors[self.age_groups]

        return constants

    def __melt(self, frame: pd.DataFrame, ltla_code: str):
        """

        :param frame:
        :param ltla_code: a LTLA code
        :return:
        """

        # foremost, ensure all dates within the dates range exists
        reference = self.dates[['date']].merge(frame, how='left', on='date')
        reference.fillna(value=0, inplace=True)

        # hence,melt
        temporary = reference.melt(id_vars='date', var_name='age_group', value_name=ltla_code)
        temporary.set_index(keys=['date', 'age_group'], inplace=True)

        return temporary

    @staticmethod
    def __aggregates(computations: list):
        """

        :param computations:
        :return:
        """

        if len(computations) > 1:
            blob = pd.concat(computations, ignore_index=False, axis=1)
        else:
            blob = computations[0]

        frame = blob.sum(axis=1).to_frame(name='daily_cases')
        frame.reset_index(drop=False, inplace=True)

        restructured = frame.pivot(index='date', columns='age_group', values='daily_cases')

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

                # assigning proportions of the LTLA daily cases to the trust via the weights
                frame = readings.copy()
                frame.loc[:, self.age_groups] = np.multiply(values, constants)

                # melt
                temporary = self.__melt(frame=frame, ltla_code=ltla_code)

                # append
                computations.append(temporary)

        return self.__aggregates(computations=computations)
