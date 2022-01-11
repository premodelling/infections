
<br>

### Virus

The United Kingdom's government provides raw COVID-19 measures via an 
API: [coronavirus.data.gov.uk API](https://coronavirus.data.gov.uk/details/developers-guide/main-api).  The [programs 
herein](.) extract raw England COVID-19 measures via this API.  Note that the time series are available at different 
segmentation levels.

variable | [LTLA](../../warehouse/virus/ltla/measures) | [NHS Trust](../../warehouse/virus/trusts/measures) | Prospective<br>Outcome<br>Variable
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

<sup>1</sup> [daily cases disaggregated by age, per LTLA, are available](../../warehouse/virus/ltla/demographic/cases)<br>
<sup>2</sup> The values of this field are probably erroneous.  
<sup>3</sup> [age disaggregated vaccinations series, per LTLA, are available](../../warehouse/virus/ltla/demographic/vaccinations)

The variables can be explored via the extracted data sets
* [LTLA](../../warehouse/virus/ltla/measures): Each file has the data of a single LTLA; the file name is the LTLA code.
* [NHS Trust](../../warehouse/virus/trusts/measures): A single trust's data per file; the file name is the NHS Trust code.


<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>