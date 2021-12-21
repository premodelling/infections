import pandas as pd


class AggregatesLTLA:

    def __init__(self, patients: pd.DataFrame, populations: pd.DataFrame):
        """

        :param patients:
        :param populations:
        """

        self.patients = patients
        self.populations = populations

    def __patients_to_trust(self):
        """

        :return:
        """

        left = self.patients.copy()[['trust_code', 'msoa', 'patients_from_msoa_to_trust']]
        right = self.populations.copy()[['msoa', 'ltla', 'ppln_ltla']]
        reference = left.merge(right, how='left', on='msoa')
        reference.drop_duplicates(inplace=True)

        values = reference.groupby(by=['trust_code', 'ltla']).agg(
            patients_from_ltla_to_trust=('patients_from_msoa_to_trust', sum))
        values.reset_index(drop=False, inplace=True)

        return values

    def __patients(self):
        """

        :return:
        """

        left = self.patients.copy()[['msoa', 'total_patients_of_msoa']]
        right = self.populations.copy()[['msoa', 'ltla']]
        reference = left.merge(right, how='left', on='msoa')
        reference.drop_duplicates(inplace=True)

        values = reference.groupby(by='ltla').agg(total_patients_of_ltla=('total_patients_of_msoa', sum))
        values.reset_index(drop=False, inplace=True)

        return values

    def exc(self):
        """

        :return:
        """

        aggregates = self.__patients_to_trust().merge(self.__patients(), how='left', on='ltla')

        return aggregates
