import os
import pandas as pd
import numpy as np

import config


class DisaggregatedCases:

    def __init__(self, weights):
        """

        :param weights: The weights of a single NHS Trust, w.r.t. contributing LTLA entities.  A data frame
                        of 'ltla', 'ag', 'tfp_ltla_ag'
        """

        self.weights = weights
        self.codes = self.weights.ltla.unique()

        configurations = config.Config()
        self.age_groups = configurations.age_groups
        self.dates = configurations.dates()

        self.source_path = os.path.join('warehouse', 'virus', 'ltla', 'demographic', 'cases')

    def __read(self, code: str):
        """
        Reads the data set of a LTLA via its code

        :param code: a LTLA code
        :return:
        """

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, '{}.csv'.format(code)))
        except RuntimeError as err:
            raise Exception(err)

        return frame[['date'] + self.age_groups]

    def __constants(self, code: str):
        """

        :param code: a LTLA code
        :return:
        """

        factors = self.weights.loc[self.weights.ltla == code, ['ltla', 'ag', 'tfp_ltla_ag']]
        factors = factors.pivot(index='ltla', columns='ag', values='tfp_ltla_ag')
        factors.reset_index(drop=True, inplace=True)
        constants = factors[self.age_groups]

        return constants

    def __melt(self, frame: pd.DataFrame, code: str):
        """

        :param frame:
        :param code: a LTLA code
        :return:
        """

        # foremost, ensure all dates within the dates range exists
        reference = self.dates[['date']].merge(frame, how='left', on='date')
        reference.fillna(value=0, inplace=True)

        # hence,melt
        temporary = reference.melt(id_vars='date', var_name='age_group', value_name=code)
        temporary.set_index(keys=['date', 'age_group'], inplace=True)

        return temporary

    def __aggregates(self, computations: list):
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

    def exc(self):
        """

        :return:
        """

        computations = []
        for code in self.codes:

            # row of weight per age group: constants
            constants = self.__constants(code=code)

            # matrix of daily cases, of a LTLA, per age group: values
            readings = self.__read(code=code)
            values = readings[self.age_groups]

            # assigning proportions of the LTLA daily cases to the trust via the weights
            frame = readings.copy()
            frame.loc[:, self.age_groups] = np.multiply(values, constants)

            # melt
            temporary = self.__melt(frame=frame, code=code)

            # append
            computations.append(temporary)

        return self.__aggregates(computations=computations)
