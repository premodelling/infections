import collections
import os
import pandas as pd

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
