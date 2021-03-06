import os
import collections
import datetime

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

    @staticmethod
    def dates():
        """
        In order to limit errors, the end date of the data sets will be 5 days before the current, today's, date

        :return:
        """

        pattern = '%Y-%m-%d'
        starting: str = '2020-03-01'
        ending: str = (datetime.datetime.today() - datetime.timedelta(days=5)).strftime('%Y-%m-%d')

        values = pd.DataFrame(pd.date_range(start=starting, end=ending, freq='D'), columns=['datetimeobject'])
        values.loc[:, 'date'] = values.datetimeobject.apply(lambda x: x.strftime(pattern))

        return values

    @staticmethod
    def modelling():

        Modelling = collections.namedtuple(typename='Modelling', field_names=['variables'])

        variables = ['date', 'covidOccupiedBeds', 'covidOccupiedMVBeds', 'estimatedNewAdmissions',
                     'EDC0-4', 'EDC5-9', 'EDC10-14', 'EDC15-19', 'EDC20-24', 'EDC25-29',
                     'EDC30-34', 'EDC35-39', 'EDC40-44', 'EDC45-49', 'EDC50-54', 'EDC55-59',
                     'EDC60-64', 'EDC65-69', 'EDC70-74', 'EDC75-79', 'EDC80-84', 'EDC85-89',
                     'EDC90+', 'newDeaths28DaysByDeathDate', 'EDV12-15', 'EDV16-17',
                     'EDV18-24', 'EDV25-29', 'EDV30-34', 'EDV35-39', 'EDV40-44', 'EDV45-49',
                     'EDV50-54', 'EDV55-59', 'EDV60-64', 'EDV65-69', 'EDV70-74', 'EDV75-79',
                     'EDV80-84', 'EDV85-89', 'EDV90+']

        return Modelling(variables=variables)
