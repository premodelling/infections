import logging
import os
import sys

import pandas as pd


def main():

    # the source of each trust's LTLA properties data file
    endpoint = os.path.join('warehouse', 'weights', 'series', 'ltla', 'baseline', 'disaggregated')

    # per trust
    trust_codes = trusts.trust_code.unique()
    for trust_code in trust_codes[2:4]:

        # foremost, a trust's flow properties data that outlines associated LTLA entities
        data = pd.read_csv(filepath_or_buffer=os.path.join(endpoint, '{}.csv'.format(trust_code)))

        # focus on the latest year
        latest = data.year.max()
        data = data.loc[data.year == latest, :]

        # eliminate sex disaggregates
        keys = ['year', 'ltla', 'sex', 'ag', 'ag_ppln_ltla', 'agf_ppln_ltla', 'tfp_ltla_ag', 'ag_ltla_frac_tp']
        aggregates = data[keys].drop(columns='sex').groupby(by=['year', 'ltla', 'ag']).agg('sum')
        aggregates.reset_index(drop=False, inplace=True)

        # re-structure
        reference = data[['year', 'ltla', 'ppln_ltla', 'total_trust_patients', 'patients_from_ltla_to_trust',
                          'ltla_frac_tp', 'total_patients_of_ltla', 'tfp_ltla', 'etc_ltla']]
        reference = reference.drop_duplicates()
        reference = reference.merge(aggregates, how='left', on=['year', 'ltla'])

        # the weights
        # weights = reference[['ltla', 'ag', 'tfp_ltla_ag']]
        # src.design.disaggregatedCases.DisaggregatedCases().exc(weights=weights)

        parent = reference[['ltla', 'tfp_ltla']].drop_duplicates()
        src.design.aggregatedCases.AggregatedCases().exc(parent=parent)


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # libraries
    import config
    import src.design.disaggregatedCases
    import src.design.aggregatedCases

    # configurations
    configurations= config.Config()
    trusts = configurations.trusts()

    main()
