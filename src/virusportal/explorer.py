"""
For exploring https://coronavirus.data.gov.uk/details/developers-guide/main-api, i.e., the UK government's API
for SARS-CoV-2 related data.
"""

import os
import sys
import logging


def main():
    """
    Use this small program to explore the variates/measures available via the aforementioned API.  Note
    that data is available for the area types

        overview: Overview data for the United Kingdom
        nation: Nation data (England, Northern Ireland, Scotland, and Wales)
        region: Region data
        nhsRegion: NHS Region data
        utla: Upper-tier local authority data
        ltla: Lower-tier local authority data

    only.  Additionally, each area type is associated with a different range of variates/measures;
    each variate/measure is not available for all area type.

    There is a hidden option - NHS Trust: nhsTrust - but the data is incomplete, hence we have to rely
    on other area types; specifically LTLA, i.e., LAD, data

    :return:
    """

    # Fields of interest
    fields = {'date': 'date',
              'dailyCases': 'newCasesBySpecimenDate',
              'dailyAdmissions': 'newAdmissions',
              'covidOccupiedMVBeds': 'covidOccupiedMVBeds',
              'hospitalCases': 'hospitalCases',
              'dailyONSDeathsByDeathDate': 'newDailyNsoDeathsByDeathDate',
              'dailyFirstDoseByVaccinationDate': 'newPeopleVaccinatedFirstDoseByVaccinationDate',
              'dailySecondDoseByVaccinationDate': 'newPeopleVaccinatedSecondDoseByVaccinationDate',
              'dailyThirdInjectionByVaccinationDate': 'newPeopleVaccinatedThirdInjectionByVaccinationDate',
              'VaccineRegisterPopulationByVaccinationDate': 'VaccineRegisterPopulationByVaccinationDate',
              'newVirusTestsBySpecimenDate': 'newVirusTestsBySpecimenDate',
              'newPCRTestsBySpecimenDate': 'newPCRTestsBySpecimenDate'}

    # Demarcations of interest
    #
    # Example
    #   Case LTLA: area_code = 'E06000022'
    #
    example = src.virusportal.measures.Measures(fields=fields).exc(area_code='E06000022')

    # previews
    logger.info(example)
    logger.info('Latest record: %s', example.date.max())


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
    import src.virusportal.measures

    main()
