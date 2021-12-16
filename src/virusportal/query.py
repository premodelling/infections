"""
For exploring the query parameters of ...
"""

import os
import sys
import logging


def main():

    # fields of interest
    fields = {'date': 'date', 'newAdmissions': 'newAdmissions',
              'covidOccupiedMVBeds': 'covidOccupiedMVBeds',
              'hospitalCases': 'hospitalCases',
              'femaleDeaths28Days': 'femaleDeaths28Days'}

    # demarcation of interest
    # Data?
    #   * area_code='RT5', area_type='nhsTrust': yes
    example = src.virusportal.measures.Measures(fields=fields).exc(area_code='RT5', area_type='nhsTrust')

    # previews
    logger.info(example)
    logger.info('Latest record: %s', example.date.max())


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO, format='\n\n%(message)s\n%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # libraries
    import src.virusportal.measures

    main()
