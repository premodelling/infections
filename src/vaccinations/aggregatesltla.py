import pandas as pd
import numpy as np


class AggregatesLTLA:

    def __init__(self, patients: pd.DataFrame, populations: pd.DataFrame):
        """

        :param patients:
        :param populations:
        """

        self.patients = patients
        self.populations = populations

        # age groups
        self.age_groups = ['12-15', '16-17', '18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54',
                           '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']

    def __patients_to_trust(self) -> pd.DataFrame:
        """

        :return: data frame of {trust_code, ltla, patients_from_ltla_to_trust}
        """

        left = self.patients.copy()[['trust_code', 'msoa', 'ltla', 'patients_from_msoa_to_trust']]
        right = self.populations.copy()[['msoa', 'ltla', 'ppln_ltla']]
        reference = left.merge(right, how='left', on=['msoa', 'ltla'])
        reference.drop_duplicates(inplace=True)

        values = reference.groupby(by=['trust_code', 'ltla', 'ppln_ltla']).agg(
            patients_from_ltla_to_trust=('patients_from_msoa_to_trust', sum))
        values.reset_index(drop=False, inplace=True)

        return values

    def __patients(self):
        """

        :return: data frame of {ltla, total_patients_of_ltla}
        """

        left = self.patients.copy()[['msoa', 'total_patients_of_msoa']]
        right = self.populations.copy()[['msoa', 'ltla']]
        reference = left.merge(right, how='left', on='msoa')
        reference.drop_duplicates(inplace=True)

        values = reference.groupby(by='ltla').agg(total_patients_of_ltla=('total_patients_of_msoa', sum))
        values.reset_index(drop=False, inplace=True)

        return values

    @staticmethod
    def __total_trust_patients(blob):

        # thus far, how many patients has a trust received per year?
        frame = blob.copy()[['trust_code', 'ltla', 'patients_from_ltla_to_trust']].drop_duplicates()
        reduced = frame.groupby(by='trust_code').agg(total_trust_patients=('patients_from_ltla_to_trust', sum))

        # re-structure
        reduced.reset_index(drop=False, inplace=True)

        return blob.copy().merge(reduced, how='left', on='trust_code')

    def __age_groups(self):
        """

        :return: data frame of {ltla, sex, age group fields ...}
        """

        reference = self.populations.copy()[['msoa', 'ltla', 'sex'] + self.age_groups]
        reference.drop_duplicates(inplace=True)

        values = reference.copy().drop(columns='msoa').groupby(by=['ltla', 'sex']).agg('sum')
        values.reset_index(drop=False, inplace=True)

        return values

    def exc(self):
        """

        :return:
        """

        # patients from LTLA to Trust based on MSOA patient numbers, age groups
        aggregates = self.__patients_to_trust().merge(self.__patients(), how='left', on='ltla')
        aggregates = aggregates.merge(self.__age_groups(), how='left', on='ltla')

        # trust fraction of patients w.r.t. LTLA
        aggregates.loc[:, 'tfp_ltla'] = np.true_divide(aggregates.patients_from_ltla_to_trust,
                                                       aggregates.total_patients_of_ltla)

        # estimated [nhs] trust catchment w.r.t. LTLA
        aggregates.loc[:, 'etc_ltla'] = np.multiply(aggregates.tfp_ltla, aggregates.ppln_ltla)

        # append total trust patients per trust
        aggregates = self.__total_trust_patients(blob=aggregates)

        return aggregates
