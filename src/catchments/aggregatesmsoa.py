import pandas as pd
import numpy as np


class AggregatesMSOA:

    def __init__(self, patients: pd.DataFrame, populations: pd.DataFrame):
        """

        :param patients: The data frame of MSOA/NHS Trust patients for the year in focus
        :param populations: The populations of the year in focus
        """

        self.patients = patients.rename(columns={'catchment_year': 'year'})
        self.populations = populations.drop(columns='ppln_ltla')

    def __total_trust_patients(self, blob):

        # thus far, how many patients has a trust received per year?
        frame = blob.copy()[['trust_code', 'msoa', 'patients_from_msoa_to_trust']].drop_duplicates()
        reduced = frame.groupby(by='trust_code').agg(total_trust_patients=('patients_from_msoa_to_trust', sum))

        # re-structure
        reduced.reset_index(drop=False, inplace=True)

        return blob.copy().merge(reduced, how='left', on='trust_code')

    def exc(self):

        aggregates = self.populations.merge(self.patients, how='right', on=['msoa', 'ltla'])

        # trust fraction of patients (tfp) w.r.t. a MSOA
        aggregates.loc[:, 'tfp_msoa'] = np.true_divide(aggregates.patients_from_msoa_to_trust, aggregates.total_patients_of_msoa)

        # estimated trust catchment (etc) w.r.t. a MSOA
        aggregates.loc[:, 'etc_msoa'] = np.multiply(aggregates.tfp_msoa, aggregates.ppln_msoa)

        # append total trust patients per trust
        aggregates = self.__total_trust_patients(blob=aggregates)

        return aggregates
