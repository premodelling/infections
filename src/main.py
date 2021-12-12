import os
import sys
import logging


def main():
    """
    https://coronavirus.data.gov.uk/details/developers-guide/main-api#query-parameters


    :return:
    """

    # for dask
    area_code = 'E06000022'

    # Measures of interest
    fields = {'date': 'date',
              'dailyCases': 'newCasesBySpecimenDate',
              'femaleDeaths28Days': 'femaleDeaths28Days',
              'maleDeaths28Days': 'maleDeaths28Days',
              'newDeaths28DaysByDeathDate': 'newDeaths28DaysByDeathDate',
              'newDeathsByDeathDate': 'newDeathsByDeathDate',
              'dailyONSDeathsByDeathDate': 'newDailyNsoDeathsByDeathDate',
              'dailyFirstDoseByVaccinationDate': 'newPeopleVaccinatedFirstDoseByVaccinationDate',
              'dailySecondDoseByVaccinationDate': 'newPeopleVaccinatedSecondDoseByVaccinationDate',
              'dailyThirdInjectionByVaccinationDate': 'newPeopleVaccinatedThirdInjectionByVaccinationDate',
              'VaccineRegisterPopulationByVaccinationDate': 'VaccineRegisterPopulationByVaccinationDate',
              'newVirusTestsBySpecimenDate': 'newVirusTestsBySpecimenDate',
              'newPCRTestsBySpecimenDate': 'newPCRTestsBySpecimenDate'}

    frame = src.virusportal.measures.Measures(fields=fields).exc(area_code=area_code)
    logger.info(frame.head())

    # Nested demographic data
    supplement = src.virusportal.demographics.Demographics(field='newCasesBySpecimenDateAgeDemographics')\
        .exc(area_code=area_code)
    logger.info(supplement.head())


if __name__ == '__main__':
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO, format='%(message)s\n%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    import src.virusportal.measures
    import src.virusportal.demographics

    main()
