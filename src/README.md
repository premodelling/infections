
<br>

* [Extraction, Transformation, Integration](#extraction-transformation-integration)
  * [The design matrix & outcomes vectors](#the-design-matrix--outcomes-vectors)

* [Modelling, Evaluation, Analysis](#modelling-evaluation-analysis)

<br>

## Extraction, Transformation, Integration

<br>

![](../notebooks/notes/images/outline.png)

<br>

The diagram is a high level illustration of the baseline data sources, transformations, and integrations 
required for the project.  The programs used thus far are hosted here.  In brief

* The [virus](./virus) programs extract raw England COVID-19 data from the official United Kingdom government's repository
  
* The [pre-processing](./preprocessing) programs extract data from a variety of sources & files, then structures & integrates 
  into forms required by the project.
  
* The [catchment](./catchments) programs focus on weight calculations.
  
* The [vaccination](./vaccinations) programs extract, structure, integrate, and weight vaccinations data that have a disaggregated 
  age groups structure different from the standard form.
  
* The [design](./design) programs integrate the aforementioned into matrices that are ready for time series forecasting via 
  machine learning, statistical modelling, signal processing, etc., algorithms.
  
<br>

### The design matrix & outcomes vectors

A range of variables that can be used for time series forecasting are hosted 
within the files of [warehouse/design/raw](../warehouse/design/raw).  Each file has the data of a single NHS 
Trust; each file's name it the trust's code.  The variables per file are

<br>

variable | Estimated<br>NHS Trust<br>Level <sup>1</sup> | NHS Trust<br>Level | description<br>(per day)
 :--- | :--- | :--- | :---
``date`` |  |  |
``covidOccupiedBeds`` | | &#10003; | The \# of beds occupied by coronavirus disease<br> patients.
``covidOccupiedMVBeds`` | | &#10003; | The \# of mechanical ventilation beds occupied by <br> coronavirus disease patients
``estimatedNewAdmissions`` | | &#10003; | The day's/date's estimated new admissions, estimated<br>by an NHS England entity.
``EDC0-4``, ``EDC5-9``, ``EDC10-14``, ...<br> ``EDC80-84``, ``EDC85-89``, ``EDC90+``  | &#10003; | | The estimated \# of daily cases (EDC) by age group.
``dailyCases`` | &#10003; | | The \# of estimated daily cases.
``newDeaths28DaysByDeathDate`` | &#10003; | | The \# of estimated daily deaths, whereby each death<br>occurred *within 28 days of a first positive*<br>*laboratory-confirmed test*. <sup>2</sup>
``dailyFirstDoseByVaccinationDate`` | &#10003; | | The daily estimated \# of first vaccinations<br> by vaccination date.
``dailySecondDoseByVaccinationDate`` | &#10003; | | The daily estimated \# of second vaccinations<br> by vaccination date.
``dailyThirdInjectionByVaccinationDate`` | &#10003; | | The daily estimated \# of third vaccinations<br> by vaccination date.
``EDV12-15``, ``EDV16-17``, ``EDV18-24``,<br> ``EDV25-29``, ``EDV30-34``, ``EDV35-39``, ...,<br> ``EDV80-84``, ``EDV85-89``, ``EDV90+``  | &#10003; | | The estimated \# of daily vaccinations (EDV)<br>by age group; second vaccinations.

<sup>1</sup> Project estimates based on the government's lower tier local authority (LTLA) level COVID-19 measures, and Public Health England 
patients flow data; yearly flow patterns from middle super output area (MSOA) entities to NHS Trusts.

<sup>2</sup> [Deaths](https://www.gov.uk/government/news/new-uk-wide-methodology-agreed-to-record-covid-19-deaths)

<br>
<br>
<br>

## Modelling, Evaluation, Analysis

Thus far, prototypes.  The directory [prototyping](./prototyping) hosts the underlying programs of the prototype notebooks

* [multiple steps ahead](../notebooks#exploration-notebooks)
* [single step ahead](../notebooks#exploration-notebooks)



<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
