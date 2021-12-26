import logging
import os
import sys


def main():

    # per trust
    trust_codes = trusts.trust_code.unique()
    for trust_code in trust_codes[2:4]:

        # trust data
        data = src.design.trustdata.TrustData().exc(trust_code=trust_code)
        logger.info(data.tail())

        # trust cases per age group determined via weights& LTLA cases
        disaggregated = src.design.disaggregatedCases.DisaggregatedCases(trust_code=trust_code).exc()
        logger.info(disaggregated.tail())

        # weighted aggregated cases
        # src.design.aggregatedCases.AggregatedCases(trust_code=trust_code).exc()

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
