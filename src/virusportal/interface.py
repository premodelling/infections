import collections
import logging
import os
import sys


def main():
    """
    Systematically reads UK SARS-CoV-2 data from coronavirus.data.gov.uk via its API

    :return:
    """

    # lower tier local authority level measures
    parameters_ = [FilterParameters(area_code=code, area_type='ltla', area_name=None, date=None)
                   for code in codes_ltla]
    measures = src.virusportal.measures.Measures(fields=fields_ltla, path=os.path.join('ltla', 'measures'))\
        .exc(parameters_=parameters_)
    logger.info(measures)

    # trust level measures
    parameters_ = [FilterParameters(area_code=code, area_type='nhsTrust', area_name=None, date=None)
                   for code in codes_trusts]
    measures = src.virusportal.measures.Measures(fields=fields_trusts, path=os.path.join('trusts', 'measures'))\
        .exc(parameters_=parameters_)
    logger.info(measures)

    # demographic data


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
    import src.virusportal.measures

    # Setting-up
    configurations = config.Config()

    fields_ltla = configurations.fields_ltla
    districts = configurations.districts()
    codes_ltla = districts.ltla.unique()

    fields_trusts = configurations.fields_trust
    trusts = configurations.trusts()
    codes_trusts = trusts.trust_code.unique()

    main()
