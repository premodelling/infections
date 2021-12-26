import logging
import os
import sys

import pandas as pd


def main():

    # per trust
    trust_codes = trusts.trust_code.unique()
    for trust_code in trust_codes[2:4]:

        logger.info(trust_code)

        # trust data
        data = src.design.trustdata.TrustData().exc(trust_code=trust_code)

        # trust cases per age group determined via weights& LTLA cases
        disaggregated = src.design.disaggregatedCases.DisaggregatedCases(trust_code=trust_code).exc()

        # weighted aggregated cases
        cases = src.design.aggregatedMeasures.AggregatedMeasures().exc(trust_code=trust_code, field='dailyCases')

        # weighted vaccination numbers
        first = src.design.aggregatedMeasures.AggregatedMeasures()\
            .exc(trust_code=trust_code, field='dailyFirstDoseByVaccinationDate')

        second = src.design.aggregatedMeasures.AggregatedMeasures()\
            .exc(trust_code=trust_code, field='dailySecondDoseByVaccinationDate')

        # finally, the design matrix for the ML/forecasting algorithms
        frame = pd.concat((data, disaggregated, cases, first, second), axis=1, ignore_index=False)
        logger.info(frame.info())
        logger.info(frame.head())


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
    import src.design.aggregatedMeasures
    import src.design.trustdata

    # configurations
    configurations= config.Config()
    trusts = configurations.trusts()

    main()
