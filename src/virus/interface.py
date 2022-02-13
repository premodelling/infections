"""
Systematically reads UK SARS-CoV-2 data from coronavirus.data.gov.uk via its API

"""

import collections
import logging
import os
import sys
import time


def main():

    # Lower Tier Local Authority Level Measures
    measures = src.virus.measures.Measures(fields=fields_ltla, path=os.path.join('ltla', 'measures')) \
        .exc(area_codes=codes_ltla, area_type='ltla')
    logger.info(measures)
    time.sleep(60)

    # trust Level measures
    measures = src.virus.measures.Measures(fields=fields_trusts, path=os.path.join('trusts', 'measures')) \
        .exc(area_codes=codes_trusts, area_type='nhsTrust')
    logger.info(measures)
    time.sleep(60)

    # lower tier local authority level measures: Cases disaggregated by Age Group
    measures = src.virus.agegroupcases.AgeGroupCases().exc(area_codes=codes_ltla, area_type='ltla')
    logger.info(measures)
    time.sleep(60)

    # lower tier local authority level measures: Vaccinations disaggregated by Age Group
    # a few areas do not have any data, albeit their request response status is 200
    area_codes = list(set(codes_ltla) - {'E06000053', 'E09000001', 'E06000060'})
    measures = src.virus.agegroupvaccinations.AgeGroupVaccinations().exc(area_codes=area_codes, area_type='ltla')
    logger.info(measures)


if __name__ == '__main__':

    # Paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # API filter parameters
    FilterParameters = collections.namedtuple(
        typename='FilterParameters', field_names=['area_code', 'area_type', 'area_name', 'date'], defaults=None)

    # libraries
    import config
    import src.virus.measures
    import src.virus.agegroupcases
    import src.virus.agegroupvaccinations

    # Setting-up
    configurations = config.Config()

    fields_ltla = configurations.fields_ltla
    districts = configurations.districts()
    codes_ltla = districts.ltla.unique()

    fields_trusts = configurations.fields_trust
    trusts = configurations.trusts()
    codes_trusts = trusts.trust_code.unique()

    main()
