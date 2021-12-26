import os
import pandas as pd
import numpy as np

import config


class AggregatedMeasures:

    def __init__(self):
        """
        Constructor
        """
        
        # the range of dates
        configurations = config.Config()
        self.dates = configurations.dates()

        # sources
        self.measures_path = os.path.join('warehouse', 'virus', 'ltla', 'measures')
        self.weights_path = os.path.join('warehouse', 'weights', 'series', 'ltla', 'focus', 'parent')

    def __weights(self, trust_code):
        """

        :param trust_code:
        :return:
        """

        try:
            return pd.read_csv(filepath_or_buffer=os.path.join(self.weights_path, '{}.csv'.format(trust_code)),
                               header=0, encoding='utf-8')
        except RuntimeError as err:
            raise Exception(err)

    def __read(self, ltla_code: str, field: str):
        """

        :param ltla_code:
        :param field:
        :return:
        """

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(self.measures_path, '{}.csv'.format(ltla_code)))
        except RuntimeError as err:
            raise Exception(err)

        # focus on field of interest
        frame = frame[['date', field]]

        # ensure all dates within the date range exists
        reference = self.dates[['date']].merge(frame, how='left', on='date')
        reference.fillna(value=0, inplace=True)

        return reference

    def __aggregates(self, computations: list, field: str):
        """

        :param computations:
        :param field:
        :return:
        """

        if len(computations) > 1:
            blob = pd.concat(computations, ignore_index=False, axis=1)
        else:
            blob = computations[0]

        frame = blob.sum(axis=1).to_frame(name=field)

        return frame

    def exc(self, trust_code:str, field: str):
        """

        :param trust_code:
        :param field:
        :return:
        """

        # the weights and the codes of the LTLA regions associated with the NHS Trust
        weights = self.__weights(trust_code=trust_code)
        ltla_codes = weights.ltla.values

        computations = []
        for ltla_code in ltla_codes:

            # weight: constant
            factor = weights.loc[weights.ltla == ltla_code, :]
            constant = factor.loc[factor.index[0], :].tfp_ltla

            # frame of date & daily cases; of a LTLA
            readings = self.__read(ltla_code=ltla_code, field=field)

            # assigning proportions of the LTLA daily cases to the trust
            frame = readings.copy()
            frame.loc[:, field] = np.multiply(frame[field], constant)
            frame.rename(columns={field: ltla_code}, inplace=True)

            # setting the date as the index
            frame.set_index(keys='date', inplace=True)
            computations.append(frame)

        return self.__aggregates(computations=computations, field=field)
