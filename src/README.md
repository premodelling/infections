
<br>

* [Extraction, Transformation, Integration](#extraction-transformation-integration)
  * [virus](#virus)
  * [preprocessing](#preprocessing)
  * [catchments](#catchments)
  * [weights](#weights)
  * [design](#design)  

* [Modelling, Evaluation, Analysis](#modelling-evaluation-analysis) <br>
  Upcoming

<br>

## Extraction, Transformation, Integration

<br>

![](../notebooks/notes/images/outline.png)

<br>

### virus

A few of the raw COVID-19 measures extractable via 
the [coronavirus.data.gov.uk API](https://coronavirus.data.gov.uk/details/developers-guide/main-api) using the 
[virus directory programs](./virus).  Note that the time series are available at different segmentation levels.

variable | [LTLA](../warehouse/virus/ltla/measures) | [NHS Trust](../warehouse/virus/trusts/measures) | Prospective<br>Outcome<br>Variable
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

<sup>1</sup> [daily cases disaggregated by age, per LTLA, are available](../warehouse/virus/ltla/demographic/cases)<br>
<sup>2</sup> The values of this field are probably erroneous.  
<sup>3</sup> [age disaggregated vaccinations series, per LTLA, are available](../warehouse/virus/ltla/demographic/vaccinations)


The variables can be explored via the extracted data sets
* [LTLA](../warehouse/virus/ltla/measures): Each file has the data of a single LTLA; the file name is the LTLA code.
* [NHS Trust](../warehouse/virus/trusts/measures): A single trust's data per file; the file name is the NHS Trust code.

<br>
<br>

### preprocessing

Baseline geographic, patient flow, and population data have been extracted/downloaded from official U.K. 
government site.  The programs of the [preprocessing directory](./preprocessing) process & integrate the data sets.

<br>

#### districts

The [districts](./preprocessing/districts.py) program [creates data files](../warehouse/geography/districts) of 
geographic mappings between middle super output area (MSOA) codes & lower tier local authority (LTLA) codes consists of

variable | description
 :--- | :---
``MSOA11CD`` | middle super output area code
``MSOA11NM`` | middle super output area name
``LAD{}CD`` | local area district code, { } is a year placeholder, e.g., LAD19CD, LAD20CD, etc.
``LAD{}NM`` | local area district name, { } is a year placeholder, e.g., LAD13NM, LAD19NM, etc.

The lower tier local authority (LTLA) is also known as local authority district (LAD).

<br>

#### patients

The [patients](./preprocessing/patients.py) program creates each 
year's [*patients flow from MSOA to trust*](../warehouse/patients) data file

variable | description
 :--- | :---
``catchment_year`` | year
``msoa``| the code of the MSOA whence the patients originated 
``trust_code`` | the code of the NHS trust that received the MSOA patients
``patients_from_msoa_to_trust`` | the number of patients from the MSOA to the NHS Trust
``total_patients_of_msoa`` | the total number of patients that originated from<br>the MSOA during the catchment year in question
``ltla``| the code of the LTLA that the MSOA belongs to


<br>

#### populations: msoa

The office for national statistics (ONS) creates MSOA population estimates by age and sex. The MSOA
[populations](./preprocessing/populationsmsoa.py) & [age groups](preprocessing/agegroupsexmsoa.py) programs merge, structure, and aggregate the data 
to create [data sets](../warehouse/populations/msoa) with headers

<ul>
    <li><div style='font-size: xx-small'>msoa,ltla,sex,0-4,5-9,10-14,15-19,20-24,25-29,30-34,35-39,40-44,45-49,50-54,55-59,60-64,65-69,70-74,<br>
        75-79,80-84,85-89,90+</div></li>
    <li><div style='font-size: xx-small'>msoa,ltla,sex,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,<br>
        32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,<br>
        64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90+</div></li>
</ul>

<br>

#### populations: ltla

The LTLA [populations](./preprocessing/populationsltla.py) & [age groups](preprocessing/agegroupsexltla.py) programs depend on the created MSOA 
data sets, and create [data sets](../warehouse/populations/ltla) with headers

<ul>
    <li><div style='font-size: xx-small'>ltla,sex,0-4,5-9,10-14,15-19,20-24,25-29,30-34,35-39,40-44,45-49,50-54,55-59,60-64,65-69,70-74,<br>
        75-79,80-84,85-89,90+</div></li>
    <li><div style='font-size: xx-small'>ltla,sex,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,<br>
        33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,<br>
        64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90+</div></li>
</ul>

<br>
<br>


### catchments

The programs of [catchments](./catchments) are focused on raw weights calculations.  Refer to the [PDF notes](../notebooks/notes/notes.pdf).

<br>
<br>

### weights

The programs of [weights](./weights) pool the weights required for design matrix calculations. 

variable | description
 :--- | :---
[``tfp_ltla``](../warehouse/weights/series/ltla/focus/parent) | The trust fraction of the patients that originated from the<br>LTLA in question.
[``tfp_ltla_ag``](../warehouse/weights/series/ltla/focus/child) | The trust fraction of the patients, **w.r.t. an age group**, that originated<br>from the LTLA in question.
[``tfp_ltla_ag``](../warehouse/weights/series/ltla/baseline/disaggregated) | The trust fraction of the patients, **w.r.t. an age group and sex**,<br>that originated from the LTLA in question.<br><br>In future, this variable name will be changed to ``tfp_ltla_ags``.  At<br>present the age-group & age-group-sex fractions can only exist<br>in separate files.

<br>
<br>

### design

The raw series for design matrices and outcomes, wherein all measures are at NHS Trust level, are available at

* [warehouse/design/raw](../warehouse/design/raw)

Each *data file* has the data of a single NHS Trust, hence each file's name is the trust code.  The data is explorable
via [Tableau Public](https://public.tableau.com/app/profile/greyhypotheses) graphs; the
explorable options are

* Hospital Activity & Estimated Cases
* Estimated Vaccination & Case Measures
* Estimated Trust Level Cases by Age Group

<br>
<br>
<br>

## Modelling, Evaluation, Analysis
Upcoming

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
