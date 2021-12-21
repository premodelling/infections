import pandas as pd
import numpy as np


class AggregatesMSOA:

    def __init__(self, patients: pd.DataFrame, populations: pd.DataFrame):
        """

        :param patients: The data frame of MSOA/NHS Trust patients for the year self.year
        :param populations: The populations of the year self.year
        """

        self.patients = patients.drop(columns='catchment_year')
        self.populations = populations.drop(columns='ppln_ltla')

    def exc(self):

        aggregates = self.populations.merge(self.patients, how='right', on='msoa')

        # trust fraction of patients (tfp) w.r.t. a MSOA
        aggregates.loc[:, 'tfp_msoa'] = np.true_divide(aggregates.patients_from_msoa_to_trust, aggregates.total_patients_of_msoa)

        # estimated trust catchment (etc) w.r.t. a MSOA
        aggregates.loc[:, 'etc_msoa'] = np.multiply(aggregates.tfp_msoa, aggregates.ppln_msoa)

        return aggregates
