
<br>

* [Extraction, Transformation, Integration](#extraction-transformation-integration)
  * [The design matrix & outcomes vectors](#the-design-matrix--outcomes-vectors)

* [Modelling, Evaluation, Analysis](#modelling-evaluation-analysis)
  * Upcoming

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

variable | Estimated<br>NHS Trust<br>Level <sup>1</sup> | NHS Trust<br>Level | description
 :--- | :--- | :--- | :---
``date`` |  |  |
``covidOccupiedBeds`` | | &#10003; | A bed occupied by a coronavirus disease<br> patient
``covidOccupiedMVBeds`` | | &#10003; | A mechanical ventilation bed occupied by a<br> coronavirus disease patient
``estimatedNewAdmissions`` | | &#10003; | Estimated by NHS England
``EDC0-4``, ``EDC5-9``, ``EDC10-14``, ...<br> ``EDC80-84``, ``EDC85-89``, ``EDC90+``  | &#10003; | | Estimated daily cases (EDC) by age group ...
``dailyCases`` | &#10003; | | Estimated daily cases
``newDeaths28DaysByDeathDate`` | &#10003; | | Estimated daily deaths count, 28 days ...
``dailyFirstDoseByVaccinationDate`` | &#10003; | | Estimated daily number of first vaccination<br> doses by ...
``dailySecondDoseByVaccinationDate`` | &#10003; | | Estimated daily number of second vaccination<br> doses by ...
``dailyThirdInjectionByVaccinationDate`` | &#10003; | | Estimated daily number of third vaccination<br> doses by ...
``EDV12-15``, ``EDV16-17``, ``EDV18-24``,<br> ``EDV25-29``, ``EDV30-34``, ``EDV35-39``, ...,<br> ``EDV80-84``, ``EDV85-89``, ``EDV90+``  | &#10003; | | Estimated daily vaccinations (EDV) by age group ...

<sup>1</sup> Project estimates based on the government's lower tier local authority (LTLA) level COVID-19 measures, and Public Health England 
patients flow data; yearly flow patterns from middle super output area (MSOA) entities to NHS Trusts.

<br>
<br>
<br>

## Modelling, Evaluation, Analysis

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
