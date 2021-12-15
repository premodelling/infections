
<br>

**SCC460 Group Project: Infections**

* [Project](#project)
  * [Critical Considerations](#critical-considerations)
  * [Data Sources](#data-sources)
  * [References](#references)
  
* [Development Notes](development/README.md#development-notes)
  * [Virtual Development Environment](development/README.md#virtual-development-environment)
  * [Code Snippets](development/README.md#code-snippets)


<br>

## Project

Aim
> Predicting localised hospitalisation trends

<br>

Objectives
> * Understanding, determining, the range of predictors that influence SARS-CoV-2 hospital admissions per NHS Trust
> 
> * Forecasting N weeks ahead

<br>

Features of interest, sometimes disaggregated by geography:

* variant features
  * [EU Variants of Concern, of Interest, Under Monitoring, De-escalated](https://www.ecdc.europa.eu/en/covid-19/variants-concern)<br>
  * [US CDC SARS-CoV-2 Variant Classifications and Definitions](https://www.cdc.gov/coronavirus/2019-ncov/variants/variant-info.html)
* transmission rate measures by variant
* incidence & prevalence measures disaggregated by variant  
* tests, cases, hospitalisations and deaths measures
* vaccination rates
* lock-down policies
* demographic & socioeconomic variables; population density
* environmental variables; built environment, residential housing quality, air quality, etc.
* etc

<br>
<br>

### Critical Considerations

Important considerations w.r.t. data collection, data handling, data representativeness, modelling, and analysis

* Ethics
* Privacy
* Data Bias (Model Bias)
* [General Data Protection Regulation (GDPR)](https://gdpr-info.eu)
* Fair AI

<br>
<br>

### Data Sources

For preliminary investigations whilst the team awaits the project data.

Official UK Data
* [data.gov.uk](https://coronavirus.data.gov.uk)
* [dowload](https://coronavirus.data.gov.uk/details/download)
* [API](https://coronavirus.data.gov.uk/details/developers-guide)

Unofficial Sources
* [Coronavirus Pandemic, Our World in Data, University of Oxford](https://ourworldindata.org/coronavirus)<br>The portal as excellent exploratory data analysis ideas & suggestions

Of import
* [A generic ONS API](https://developer.ons.gov.uk)

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

* Fair AI
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


