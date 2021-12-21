"""
For exploring https://coronavirus.data.gov.uk/details/developers-guide/main-api, i.e., the UK government's API
for SARS-CoV-2 related data.
"""

import os
import sys
import logging
import json

import pandas as pd


def main():
    """
    Use this small program to explore the variates/measures available via the aforementioned API.  Note
    that data is available for the area types (areaType)

        overview: Overview data for the United Kingdom
        nation: Nation data (England, Northern Ireland, Scotland, and Wales)
        region: Region data
        nhsRegion: NHS Region data
        utla: Upper-tier local authority data
        ltla: Lower-tier local authority data

    only.  Additionally, each area type is associated with a different range of variates/measures;
    each variate/measure is not available for all area type.

    There is a hidden option - NHS Trust: nhsTrust - but the data is incomplete, hence we have to rely
    on other area types; specifically LTLA, i.e., LAD, data.

    The areaType is one of 4 authorised filters for acquiring data via the API.  In brief, the filters are

        areaType: Area type as string
        areaName: Area name as string
        areaCode: Area Code as string
        date: Date as string [YYYY-MM-DD]

    :return:
    """

    # filters
    area_type = 'ltla'
    area_code='E06000022'
    dictionary = {'areaType': area_type, 'areaCode': area_code, 'areaName': None, 'date': None}
    dictionary = ['{}={}'.format(key, value) for key, value in dictionary.items() if value is not None]
    filters = str.join(';', dictionary)

    # fields of interest
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
    structure = json.dumps(obj=fields, separators=(',', ':'))

    # url
    url = 'https://api.coronavirus.data.gov.uk/v1/data?filters={filters}&structure={structure}&format={format}'
    url = url.format(filters=filters, structure=structure, format='csv')

    # read the data of interest via the constructed API URL
    try:
        frame = pd.read_csv(filepath_or_buffer=url)
    except RuntimeError as err:
        raise Exception(err)

    # previews
    logger.info(frame)
    logger.info('Latest record: %s', frame.date.max())


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    main()
