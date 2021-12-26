import logging
import os
import sys

import pandas as pd


def main():

    # the source of each trust's LTLA properties data file
    endpoint = os.path.join('warehouse', 'weights', 'series', 'ltla', 'focus', 'child')

    # per trust
    trust_codes = trusts.trust_code.unique()
    for trust_code in trust_codes[2:4]:

        # pending: dates check, fill NaN
        data = src.design.trustdata.TrustData().exc(trust_code=trust_code)
        logger.info(data.tail())

        # pending: move into disaggregated
        # a trust's age group flow/weights properties data that outlines associated LTLA entities
        weights = pd.read_csv(filepath_or_buffer=os.path.join(endpoint, '{}.csv'.format(trust_code)))

        # trust cases per age group determined via weights& LTLA cases
        disaggregated = src.design.disaggregatedCases.DisaggregatedCases(weights=weights).exc()
        logger.info(disaggregated.tail())

        # weighted aggregated cases
        # src.design.aggregatedCases.AggregatedCases().exc(...)

        # weighted vaccination numbers

        # finally, the design matrix for the ML/forecasting algorithms


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
    import src.design.trustdata

    # configurations
    configurations= config.Config()
    trusts = configurations.trusts()

    main()
