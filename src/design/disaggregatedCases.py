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

    def __read(self, code: str):

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, '{}.csv'.format(code)))
        except RuntimeError as err:
            raise Exception(err)

        return frame[['date'] + self.age_groups]

    def exc(self, weights):
        """
        The weights of a single trust, w.r.t. contributing LTLA entities

        :param weights: data frame of 'ltla', 'ag', 'ag_trust_factor'
        :return:
        """

        codes = weights.ltla.unique()

        computations = []
        for code in codes:

            # row vector of weight per age group: constants
            factors = weights.loc[weights.ltla == code, :]
            factors = factors.pivot(index='ltla', columns='ag', values='tfp_ltla_ag')
            factors.reset_index(drop=True, inplace=True)
            constants = factors[self.age_groups]

            # matrix of daily cases, of a LTLA, per age group: values
            readings = self.__read(code=code)
            values = readings[self.age_groups]

            # assigning proportions of the LTLA daily cases to the trust via the weights
            frame = readings.copy()
            frame.loc[:, self.age_groups] = np.multiply(values, constants)

            # dates
            reference = self.dates[['date']].merge(frame, how='left', on='date')
            reference.fillna(value=0, inplace=True)

            temporary = reference.melt(id_vars='date', var_name='age_group', value_name=code)
            temporary.set_index(keys=['date', 'age_group'], inplace=True)
            computations.append(temporary)

        if len(computations) > 1:
            alt = pd.concat(computations, ignore_index=False, axis=1)
        else:
            alt = computations[0]

        finale = alt.sum(axis=1).to_frame(name='daily_cases')
        finale.reset_index(drop=False, inplace=True)

        print(finale.pivot(index='date', columns='age_group', values='daily_cases'))
