import collections

import numpy as np


class Config:

    def __init__(self):
        """
        https://coronavirus.data.gov.uk/details/developers-guide/main-api#query-parameters
        """

        self.fields = {'date': 'date',
                       'dailyCases': 'newCasesBySpecimenDate',
                       'dailyAdmissions': 'newAdmissions',
                       'covidOccupiedMVBeds': 'covidOccupiedMVBeds',
                       'hospitalCases': 'hospitalCases',
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

        self.age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44',
                           '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']
        self.age_group_length = 5

    @staticmethod
    def population():
        ages = list(np.arange(start=0, stop=90))
        ages = ages + ['90+']

        field_names = ['filename', 'year', 'sex', 'sheets', 'header', 'cells', 'keys', 'overflow']
        Details = collections.namedtuple(typename='Details', field_names=field_names)

        details = [Details._make(('SAPE20DT3-mid-2012-msoa-syoa-estimates-formatted.XLS', 2012, ['female', 'male'],
                                  ['Mid-2012 Females', 'Mid-2012 Males'], 4, 'A:CQ', ['Area Codes'], 'Area Names')),
                   Details._make(('SAPE20DT3-mid-2013-msoa-syoa-estimates-formatted.XLS', 2013, ['female', 'male'],
                                  ['Mid-2013 Females', 'Mid-2013 Males'], 4, 'A:CQ', ['Area Codes'], 'Area Names')),
                   Details._make(('SAPE20DT3-mid-2014-msoa-syoa-estimates-formatted.XLS', 2014, ['female', 'male'],
                                  ['Mid-2014 Females', 'Mid-2014 Males'], 4, 'A:CQ', ['Area Codes'], 'Area Names')),
                   Details._make(('SAPE20DT3-mid-2015-msoa-syoa-estimates-formatted.XLS', 2015, ['female', 'male'],
                                  ['Mid-2015 Females', 'Mid-2015 Males'], 4, 'A:CQ', ['Area Codes'], 'Area Names')),
                   Details._make(('SAPE20DT3-mid-2016-msoa-syoa-estimates-formatted.XLS', 2016, ['female', 'male'],
                                  ['Mid-2016 Females', 'Mid-2016 Males'], 4, 'A:CQ', ['Area Codes'], 'Area Names')),
                   Details._make(('SAPE20DT3-mid-2017-msoa-syoa-estimates-formatted.XLS', 2017, ['female', 'male'],
                                  ['Mid-2017 Females', 'Mid-2017 Males'], 4, 'A:CQ', ['Area Codes'], 'Area Names')),
                   Details._make(('SAPE21DT3a-mid-2018-msoa-on-2019-LA-syoa-estimates-formatted.xlsx',
                                  2018, ['female', 'male'], ['Mid-2018 Females', 'Mid-2018 Males'], 4, 'A:CQ',
                                  ['Area Codes'], 'LA (2019 boundaries)')),
                   Details._make(('SAPE22DT4-mid-2019-msoa-syoa-estimates-unformatted.xlsx',
                                  2019, ['female', 'male'], ['Mid-2019 Females', 'Mid-2019 Males'], 4, 'A:CT',
                                  ['MSOA Code'], None)),
                   Details._make(('sape23dt4mid2020msoasyoaestimatesunformatted.xlsx',
                                  2020, ['female', 'male'], ['Mid-2020 Females', 'Mid-2020 Males'], 4, 'A:CT',
                                  ['MSOA Code'], None))]

        return details, ages
