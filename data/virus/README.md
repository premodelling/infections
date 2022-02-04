
### Data Sources

For preliminary investigations whilst the team awaits the project data.

Official UK Data
* [coronavirus.data.gov.uk](https://coronavirus.data.gov.uk)
* [coronavirus.data.gov.uk: dowload](https://coronavirus.data.gov.uk/details/download)
* [coronavirus.data.gov.uk: API](https://coronavirus.data.gov.uk/details/developers-guide/main-api)
* [COVID-19 Hospital Activity](https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/)

Unofficial Sources
* [Coronavirus Pandemic, Our World in Data, University of Oxford](https://ourworldindata.org/coronavirus) <br>The portal has excellent exploratory data analysis ideas & suggestions


#### data.gov.uk SARS-CoV-2 Infection Measures

The government's coronavirus measures have been a challenge due to their disparate units of measure.  The table below outlines this point, and it is this issue that underlies
the need for the additional data sets, i.e., the above-listed patients, populations, and geographic data sets.

<br>

variable | [LTLA](./warehouse/virus/ltla/measures) | [NHS Trust](./warehouse/virus/trusts/measures) | Prospective<br>Outcome<br>Variable
 :--- | :--- | :--- | :---
``date`` | &#10003; | &#10003; |
``dailyCases`` <sup>1</sup> | &#10003; | |
``newDeaths28DaysByDeathDate`` | &#10003; | |
``dailyFirstDoseByVaccinationDate`` | &#10003; | |
``dailySecondDoseByVaccinationDate`` | &#10003; | |
``dailyThirdInjectionByVaccinationDate`` | &#10003; | |
``VaccineRegisterPopulationByVaccinationDate`` <sup>2, 3</sup> | &#10003; | |
``newVirusTestsBySpecimenDate`` | &#10003; | |
``newPCRTestsBySpecimenDate`` | &#10003; | |
``covidOccupiedBeds`` | | &#10003; |
``covidOccupiedMVBeds`` | | &#10003; |
``estimatedNewAdmissions`` | | &#10003; | &#10003;

<sup>1</sup> [daily cases disaggregated by age, per LTLA, are available](./warehouse/virus/ltla/demographic/cases)<br>
<sup>2</sup> The values of this field are probably erroneous.  
<sup>3</sup> [age disaggregated vaccinations series, per LTLA, are available](./warehouse/virus/ltla/demographic/vaccinations)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>