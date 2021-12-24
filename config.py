import os

import numpy as np
import pandas as pd


class Config:

    def __init__(self):
        """
        https://coronavirus.data.gov.uk/details/developers-guide/main-api#query-parameters
        """

        # fields
        self.fields_ltla = {'date': 'date',
                            'dailyCases': 'newCasesBySpecimenDate',
                            'newDeaths28DaysByDeathDate': 'newDeaths28DaysByDeathDate',
                            'dailyFirstDoseByVaccinationDate': 'newPeopleVaccinatedFirstDoseByVaccinationDate',
                            'dailySecondDoseByVaccinationDate': 'newPeopleVaccinatedSecondDoseByVaccinationDate',
                            'dailyThirdInjectionByVaccinationDate': 'newPeopleVaccinatedThirdInjectionByVaccinationDate',
                            'VaccineRegisterPopulationByVaccinationDate': 'VaccineRegisterPopulationByVaccinationDate',
                            'newVirusTestsBySpecimenDate': 'newVirusTestsBySpecimenDate',
                            'newPCRTestsBySpecimenDate': 'newPCRTestsBySpecimenDate'}

        self.fields_trust = {'date': 'date',
                             'covidOccupiedBeds': 'hospitalCases',
                             'covidOccupiedMVBeds': 'covidOccupiedMVBeds',
                             'estimatedNewAdmissions': 'newAdmissions'}

        # age groups
        self.age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44',
                           '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']
        self.age_group_length = 5

        # ages
        ages = list(np.arange(start=0, stop=90))
        self.ages = ages + ['90+']
        self.ages_length = len(ages)

    @staticmethod
    def districts() -> pd.DataFrame:
        """

        :return:
        """

        datafile = os.path.join(os.getcwd(), 'warehouse', 'geography', 'districts', '2020.csv')

        try:
            frame = pd.read_csv(filepath_or_buffer=datafile, header=0,
                                    encoding='utf-8', usecols=['MSOA11CD', 'LAD20CD'])
        except RuntimeError as err:
            raise Exception(err)
        frame.rename({'MSOA11CD': 'msoa', 'LAD20CD': 'ltla'}, axis=1, inplace=True)

        return frame

    @staticmethod
    def trusts():

        uri = os.path.join('data', 'catchment', '2021 Trust Catchment Populations_Supplementary Trust Area lookup.xlsx')
        sheet_name = 'Trust Area Lookup'
        rename = {'TrustCode': 'trust_code', 'TrustName': 'trust_name'}

        try:
            frame = pd.read_excel(io=uri, sheet_name=sheet_name, header=0, usecols=['TrustCode', 'TrustName'])
        except RuntimeError as err:
            raise Exception(err)
        frame.rename(columns=rename, inplace=True)

        return frame

    @staticmethod
    def vaccinations():

        rename = {'12_15': '12-15', '16_17': '16-17', '18_24': '18-24', '25_29': '25-29', '30_34': '30-34',
                  '35_39': '35-39', '40_44': '40-44', '45_49': '45-49', '50_54': '50-54', '55_59': '55-59',
                  '60_64': '60-64', '65_69': '65-69', '70_74': '70-74', '75_79': '75-79', '80_84': '80-84',
                  '85_89': '85-89', '90+': '90+'}

        metric = 'vaccinationsAgeDemographics'

        variables = ['date', 'age', 'newPeopleVaccinatedCompleteByVaccinationDate',
                     'newPeopleVaccinatedFirstDoseByVaccinationDate',
                     'newPeopleVaccinatedSecondDoseByVaccinationDate',
                     'newPeopleVaccinatedThirdInjectionByVaccinationDate']

        return metric, variables, rename
