import os
import sys
import logging


def main():

    # set-up parallel reading via dask; parallel by LTLA/LAD area code
    area_code = 'E06000022'

    # un-nested measures of interest are declared in the config.py file
    fields = config.Config().fields

    # reading-in the un-nested measures
    frame = src.virusportal.measures.Measures(fields=fields).exc(area_code=area_code)
    logger.info(frame.head())

    # reading-in the nested demographic data
    supplement = src.virusportal.demographics.Demographics(field='newCasesBySpecimenDateAgeDemographics')\
        .exc(area_code=area_code)
    logger.info(supplement.head())

    # area codes for England
    area_codes = src.ingest.areacodes.AreaCodes().exc()
    logger.info(area_codes.head())


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
    import src.virusportal.measures
    import src.virusportal.demographics

    import src.ingest.areacodes

    main()
