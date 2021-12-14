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
