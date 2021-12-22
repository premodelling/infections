import os
import sys
import logging


def main():

    # a LTLA/LAD area code
    area_code = 'E06000022'

    # reading-in the nested demographic data
    supplement = src.virusportal.demographics.Demographics(field='newCasesBySpecimenDateAgeDemographics')\
        .exc(area_code=area_code)
    logger.info(supplement.head())


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
    import src.virusportal.demographics

    main()
