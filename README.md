
<br>

**SCC460 Group Project: Infections**

* [Project](#project)
  * [Data Notes](#data-notes)
    * [Features](#features)
    * [SARS-CoV-2 Data](#sars-cov-2-data)
    * [Addressing Multi-granularity](#addressing-multi-granularity)
  
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

### Data Notes

#### Features

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

#### SARS-CoV-2 Data

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

variable | [LTLA](./warehouse/virus/ltla/measures) | [NHS Trust](./warehouse/virus/trusts/measures) | Possible<br>Outcome
 :--- | :--- | :--- | :---
``date`` | &#10004; | &#10004; |
``dailyCases`` | &#10004; | |
``newDeaths28DaysByDeathDate`` | &#10004; | |
``dailyFirstDoseByVaccinationDate`` | &#10004; | |
``dailySecondDoseByVaccinationDate`` | &#10004; | |
``dailyThirdInjectionByVaccinationDate`` | &#10004; | |
``VaccineRegisterPopulationByVaccinationDate`` | &#10004; | |
``newVirusTestsBySpecimenDate`` | &#10004; | |
``newPCRTestsBySpecimenDate`` | &#10004; | |
``covidOccupiedBeds`` | | &#10004; | &#10004;
``covidOccupiedMVBeds`` | | &#10004; |
``estimatedNewAdmissions`` | | &#10004; | &#10004;


<br>
<br>

#### Addressing Multi-Granularity

The differing granularity of the variables can be addressed via estimated flow/mapping factors.  More notes, and graphs, upcoming.  Visit 
[warehouse/trusts/segments/ltla](./warehouse/trusts/segments/ltla) for the calculated factors per NHS Trust, from a LTLA, per year  


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
* [Coronavirus Pandemic, Our World in Data, University of Oxford](https://ourworldindata.org/coronavirus)<br>The portal as excellent exploratory data analysis ideas & suggestions

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


