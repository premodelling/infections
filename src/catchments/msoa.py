import pandas as pd
import numpy as np

import config


class MSOA:

    def __init__(self):
        """

        """

        self.age_groups = config.Config().age_groups

        self.keys = ['trust_code', 'msoa', 'ltla', 'ppln_msoa', 'ppln_ltla', 'sex'] + self.age_groups + \
                    ['patients_from_msoa_to_trust', 'total_patients_of_msoa', 'tfp_msoa', 'etc_msoa']

    def __trust(self, frame: pd.DataFrame):
        """
        * trust fraction of patients (tfp) w.r.t. a MSOA
        * estimated trust catchment (etc) w.r.t. a MSOA

        :param frame:
        :return:
        """

        frame.loc[:, 'tfp_msoa'] = np.true_divide(frame.patients_from_msoa_to_trust, frame.total_patients_of_msoa)
        frame.loc[:, 'etc_msoa'] = np.multiply(frame.tfp_msoa, frame.ppln_msoa)

        return frame

    def exc(self, patients: pd.DataFrame, populations: pd.DataFrame, year: int):
        """

        :param patients:
        :param populations:
        :param year:
        :return:
        """

        reference = populations.merge(patients.drop(columns='catchment_year'), how='right', on='msoa')
        reference = self.__trust(frame=reference.copy())
