import collections


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

        # demographics: in progress
        self.age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44',
                           '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']

        Data = collections.namedtuple(typename='Data',
                                      field_names=['years', 'sheet_names', 'cell_ranges', 'starts', 'endings'])
        self.data = Data._make(([], [], ['A:W'], [], []))

        FieldNames = collections.namedtuple(typename='FieldNames', field_names=['cell_ranges', 'rows', 'to_drop'])
        self.fieldnames = FieldNames._make((['A:W'], [4], []))


