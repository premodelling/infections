import os
import pandas as pd
import numpy as np

import config


class AggregatedCases:

    def __init__(self):

        configurations = config.Config()
        self.dates = configurations.dates()

        self.source_path = os.path.join('warehouse', 'virus', 'ltla', 'measures')
        self.field = 'dailyCases'

    def __read(self, code: str):

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.source_path, '{}.csv'.format(code)))
        except RuntimeError as err:
            raise Exception(err)

        return frame[['date', self.field]]

    def exc(self, parent: pd.DataFrame):
        """
        The parent weights of a single trust, w.r.t. contributing LTLA entities

        :param parent: data frame of 'ltla', 'tfp_ltla'
        :return:
        """

        codes = parent.ltla.values

        computations = []
        for code in codes:

            # weight: constant
            factor = parent.loc[parent.ltla == code, :]
            constant = factor.loc[factor.index[0], :].tfp_ltla

            # frame of date & daily cases; of a LTLA
            readings = self.__read(code=code)

            # assigning proportions of the LTLA daily cases to the trust
            frame = readings.copy()
            frame.loc[:, self.field] = np.multiply(frame[self.field], constant)
            frame.rename(columns={self.field: code}, inplace=True)

            # dates
            reference = self.dates[['date']].merge(frame, how='left', on='date')
            reference.fillna(value=0, inplace=True)

            reference.set_index(keys='date', inplace=True)
            computations.append(reference)

        if len(computations) > 1:
            alt = pd.concat(computations, ignore_index=False, axis=1)
        else:
            alt = computations[0]

        finale = alt.sum(axis=1).to_frame(name='daily_cases')
        finale.reset_index(drop=False, inplace=True)

        print(alt)
        print(finale)
