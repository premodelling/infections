
<br>

**SCC460 Group Project: Infections**

* [Project](#project)
  * [Plausible Features](#plausible-features)
  * [SARS-CoV-2 & Supplementary Data](#sars-cov-2--supplementary-data)
  * [Addressing Disparate Data](#addressing-disparate-data)
  * [Design Matrices for Modelling](#design-matrices-for-modelling)
  
* [Preliminaries](#preliminaries)
  * [Critical Considerations](#critical-considerations)
  * [Data Sources](#data-sources)
  * [References](#references)
  
* [Development Notes](development/README.md#development-notes)
  * [Virtual Development Environment](development/README.md#virtual-development-environment)
  * [Code Snippets](development/README.md#code-snippets)


<br>

## Project

**Aim**
> Predicting hospitalisation trends of NHS Trusts

<br>

**Objectives**
> * Understanding, determining, the range of predictors that influence SARS-CoV-2 hospital admissions per NHS Trust
> 
> * Forecasting N weeks ahead

<br>
<br>

### Plausible Features

There a number of features of interest, sometimes disaggregated by geography, for the forecasting problem in question.  Including:

* variant features
  * [EU Variants of Concern, of Interest, Under Monitoring, De-escalated](https://www.ecdc.europa.eu/en/covid-19/variants-concern)<br>
  * [US CDC SARS-CoV-2 Variant Classifications and Definitions](https://www.cdc.gov/coronavirus/2019-ncov/variants/variant-info.html)
* transmission rate measures by variant
* vaccination, tests, cases, hospitalisations and deaths measures
* demographic, socioeconomic, and environmental variables
* SARS-CoV-2 related policies
* etc.

<br>
<br>

### SARS-CoV-2 & Supplementary Data

Thus far, the focus is the [coronavirus.data.gov.uk](https://coronavirus.data.gov.uk) SARS-CoV-2 data; data extraction via 
the [API](https://coronavirus.data.gov.uk/details/developers-guide/main-api).  The table below outlines the variables 
in focus thus far.  A few points

* Data variables, i.e., SARS-CoV-2 data measures, are not available at equivalent granularity.  For example, only a
  handful of un-aggregated measures are available at NHS Trust level; the aggregated measures depend on the un-aggregated measures.

* Age demarcations are inconsistent: At the lower tier local authority (LTLA) level, the age groups used for  
  ``newCasesBySpecimenDateAgeDemographics``, differ from the age groups used for ``vaccinationsAgeDemographics``.  
  Although the API does not include NHS Trust level age group decompositions, such decompositions are available
  via [COVID-19 Hospital Activity](https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/),
  which – amazingly – uses a third different set of age group demarcations.
  
* A few API variables have misleading names, these [are renamed](https://github.com/premodelling/infections/blob/develop/config.py); the NHS Trust level 
  variables have been renamed to reflect their original 
  [COVID-19 Hospital Activity](https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/) 
  labels.
  
<br>

The variables can be explored via the extracted data sets
* [LTLA](./warehouse/virus/ltla/measures): Each file has the data of a single LTLA; the file name is the LTLA code.
* [NHS Trust](./warehouse/virus/trusts/measures): A single trust's data per file; the file name is the NHS Trust code. 

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

### Addressing Disparate Data

The prospective modelling measures exists at either NHS Trust or Lower Tier Local Authority (LTLA) level, and because our interest is in 
NHS Trust level admissions, we need the NHS Trust level forms of the LTLA measures.

<br>

**Approach**

In brief, a section of NHS England records the number of patients that each Middle Super Output Area (MSOA) contributes to each NHS Trust 
each year; each MSOA contributes patients to one or more NHS Trusts.  However, each MSOA region is a member of one LTLA region, hence 
the number of patients that each LTLA contributes to a NHS Trust, per year, can be calculated via appropriate aggregates.

Via these LTLA level aggregates the questions ... *per LTLA that contributes to a NHS Trust* 

* what fraction of the LTLA's patients did the trust receive?
* what fraction of the LTLA's patients, within age group 5 - 9, did the trust receive?  

are calculable, and the resulting fractions guide the apportioning of LTLA level COVID measures
to NHS Trusts.    The key values are within the data files that are linked to via the variables below

<br>

variable | description
 :--- | :---
[``tfp_ltla``](./warehouse/weights/series/ltla/focus/parent) | The trust fraction of the patients that originated from the<br>LTLA in question.
[``tfp_ltla_ag``](./warehouse/weights/series/ltla/focus/child) | The trust fraction of the patients, **w.r.t. an age group**, that originated<br>from the LTLA in question.
[``tfp_ltla_ag``](./warehouse/weights/series/ltla/baseline/disaggregated) | The trust fraction of the patients, **w.r.t. an age group and sex**,<br>that originated from the LTLA in question.<br><br>In future, this variable name will be changed to ``tfp_ltla_ags``.  At<br>present the age-group & age-group-sex fractions can only exist<br>in separate files.

<br>

**Of interest**, if we have time, a map that illustrates the fraction of LTLA patients that a NHS trust receives from each
contributing LTLA, and perhaps catchment estimates.

<br>

**Assumptions**

* The 2019 patient flow fractions from a LTLA to a NHS Trust, for all admissions types, are reasonable estimates of flow 
  fractions for any admission type.  Not ideal.  There are several arguments against this assumption.  In the case of SARS-CoV-2
  * Are all trusts equally equipped to deal with a respiratory pandemic?
  * Capacity

* The population characteristics of each LTLA change minimally within a short period.  Not ideal either.

* etc.

<br>
<br>

### Design Matrix & Outcomes Series for Modelling

The raw series for design matrices and outcomes, wherein all measures are at NHS Trust level, are available at

* [warehouse/design/raw](./warehouse/design/raw)

**Please do not use the *age group cases series/fields* yet**, they need to be adjusted for zero cases; meanwhile use 
the ``dailyCases`` field instead.  Each *data file* has the data of a single NHS Trust, hence each file's name is 
the trust code.  Readers may explore the data at [Tableau Public](https://public.tableau.com/app/profile/greyhypotheses); the 
explorable options are

* Hospital Activity & Estimated Cases
* Estimated Vaccination & Case Measures

Upcoming

* Estimated Cases by Age Group

<br>

**Required for the report**, an illustration of the data sources, the weights calculations steps, and the data 
integration steps/processes.

<br>
<br>
<br>


## Preliminaries


### Critical Considerations

Important considerations w.r.t. data collection, data handling, data representativeness, modelling, and analysis

* Ethics, Privacy ([Institute for Ethics in AI](https://www.oxford-aiethics.ox.ac.uk): [podcasts](https://podcasts.ox.ac.uk/series/ethics-ai))
* Data & Model Bias ([Mitigating bias in machine learning for medicine](https://www.nature.com/articles/s43856-021-00028-w), 
  [Understanding the Bias-Variance Tradeoff](https://scott.fortmann-roe.com/docs/BiasVariance.html))
* [General Data Protection Regulation (GDPR)](https://gdpr-info.eu)
* [Fairness in Artificial Intelligence](https://dl.acm.org/doi/10.1145/3313831.3376445)

<br>
<br>

### Data Sources

For preliminary investigations whilst the team awaits the project data.

Official UK Data
* [coronavirus.data.gov.uk](https://coronavirus.data.gov.uk)
* [coronavirus.data.gov.uk: dowload](https://coronavirus.data.gov.uk/details/download)
* [coronavirus.data.gov.uk: API](https://coronavirus.data.gov.uk/details/developers-guide/main-api)
* [COVID-19 Hospital Activity](https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/)

Unofficial Sources
* [Coronavirus Pandemic, Our World in Data, University of Oxford](https://ourworldindata.org/coronavirus)<br>The portal has excellent exploratory data analysis ideas & suggestions

<br>
<br>

### References

* Med-BERT
  * [Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction](https://www.nature.com/articles/s41746-021-00455-y)
  * [Predictive Modeling on Electronic Health Records(EHR) using Pytorch](https://github.com/ZhiGroup/pytorch_ehr)

* BERT: Bidirectional Encoder Representations from Transformers
  * [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)
  * [GitHub: BERT](https://github.com/google-research/bert)
  
* Prediction models for diagnosis and prognosis of COVID-19: systematic review and critical appraisal, BMJ 2020; 369
  doi: https://doi.org/10.1136/bmj.m1328

* [Prediction models for COVID-19 clinical decision making](https://www.thelancet.com/journals/landig/article/PIIS2589-7500(20)30226-0/fulltext) 

* BERT & Clinical Data
  * [Does BERT Pretrained on Clinical Notes Reveal Sensitive Data?](https://aclanthology.org/2021.naacl-main.73.pdf)
  * [GitHub: Does BERT leak Patient Data ?](https://github.com/elehman16/exposing_patient_data_release)

* Fairness in Artificial Intelligence
  * [Co-Designing Checklists to Understand Organizational Challenges and Opportunities around Fairness in AI](https://dl.acm.org/doi/10.1145/3313831.3376445)
  
* [Rapid Coronavirus Tests](https://www.gov.uk/government/news/roll-out-of-2-new-rapid-coronavirus-tests-ahead-of-winter)


<br>
<br>
<br>
<br>

<br>
<br>
<br>
<br>


