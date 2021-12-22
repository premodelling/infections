import collections
import logging
import os
import sys


def main():
    """
    Systematically reads UK SARS-CoV-2 data from coronavirus.data.gov.uk via its API

    :return:
    """

    # API filter parameters
    FilterParameters = collections.namedtuple(
        typename='FilterParameters', field_names=['area_code', 'area_type', 'area_name', 'date'], defaults=None)
    parameters_ = [FilterParameters(area_code=code, area_type='ltla', area_name=None, date=None) for code in codes]

    # measures
    measures = src.virusportal.measures.Measures(fields=fields).exc(parameters_=parameters_)
    logger.info(measures)

    # At Trust level; ref. explorer.py
    # newAdmissions, covidOccupiedMVBeds

    # demographic data

    # merge


if __name__ == '__main__':

    # paths
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
    import src.virusportal.measures

    # API fields of interest
    fields = config.Config().fields

    # geographic codes
    districts = config.Config().districts()
    codes = districts.ltla.unique()

    main()
