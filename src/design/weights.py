import os
import pandas as pd


class Weights:

    def __init__(self, weights_of_year: int):
        """

        """

        self.weights_of_year = weights_of_year

    def disaggregated(self, trust_code: str):
        """

        :return:
        """

        path = os.path.join('warehouse', 'weights', 'series', 'ltla', 'baseline', 'disaggregated')

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(path, '{}.csv'.format(trust_code)))
        except RuntimeError as err:
            raise Exception(err)

        frame = frame.loc[frame['year'] == self.weights_of_year, :]

        fields = ['year', 'ltla', 'ppln_ltla', 'patients_from_ltla_to_trust', 'total_patients_of_ltla',
                  'tfp_ltla', 'etc_ltla', 'total_trust_patients', 'ltla_frac_tp', 'ag']

        aggregates = frame.drop(columns='sex').groupby(by=fields).agg(
            ag_ppln_ltla=('ags_ppln_ltla', sum), 
            agf_ppln_ltla=('agsf_ppln_ltla', sum),
            tfp_ltla_ag=('tfp_ltla_ags', sum),
            ag_ltla_frac_tp=('ags_ltla_frac_tp', sum))
        
        aggregates.reset_index(drop=False, inplace=True)

        return aggregates

    def aggregated(self, trust_code: str):
        """

        :return:
        """

        path = os.path.join('warehouse', 'weights', 'series', 'ltla', 'baseline', 'aggregated')

        try:
            frame = pd.read_csv(filepath_or_buffer=os.path.join(path, '{}.csv'.format(trust_code)))
        except RuntimeError as err:
            raise Exception(err)

        frame = frame.loc[frame['year'] == self.weights_of_year, :]

        fields = ['year', 'ltla', 'ppln_ltla', 'patients_from_ltla_to_trust', 'total_patients_of_ltla',
                  'tfp_ltla', 'etc_ltla', 'total_trust_patients', 'ltla_frac_tp']

        frame = frame[fields].drop_duplicates()

        return frame
