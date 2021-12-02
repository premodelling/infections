
<br>

**SCC460 Group Project: Infections**

* [Focus & Options](#focus--options)
  * [Triple Forecasts](#triple-forecasts)
  * [Predicting Hospitalisation Trends](#predicting-hospitalisations-trend)
  * [Prognostic Predictions](#prognostic-predictions)
* [Critical Considerations](#critical-considerations)
* [Data Sources](#data-sources)
* [Research](#research)
  * [Modelling & Analysis](#modelling--analysis)
  * [Ethics, Privacy, Confidentiality](#ethics-privacy-confidentiality)

<br>

## Focus & Options

Dr. Jiang asked us to consider a SARS-CoV-2 project in relation to either

* Predicting measures, e.g., predicting expected hospitalisations.
* Patient prognosis

A few options below.  In general, what we can do depends on the type & range of data we eventually have access to. 

<br>

### Triple Forecasts

Predicting cases/hospitalisations/death.  Possible features of interest, sometimes disaggregated by geography:

* tests, cases, hospitalisations, deaths
* vaccination rates
* lock-down policies
* incidence, prevalence
* demographic, socioeconomic
* built environment, residential housing quality, air quality
* population density

It might be quite tricky/difficult to use some variables effectively.  Some variables might be irrelevant, 
modelling & analysis will address this.

<br>

### Predicting Hospitalisations Trend

Possible features of interest, sometimes disaggregated by geography:

* variant features
  * [EU Variants of Concern, of Interest, Under Monitoring, De-escalated](https://www.ecdc.europa.eu/en/covid-19/variants-concern)<br>
  * [US CDC SARS-CoV-2 Variant Classifications and Definitions](https://www.cdc.gov/coronavirus/2019-ncov/variants/variant-info.html)
* transmission rates by variant
* tests, cases, hospitalisations by variant
* vaccination rates
* lock-down policies
* incidence, prevalence
* demographic, socioeconomic
* built environment, residential housing quality, air quality
* population density
* etc

<br>

### Prognostic Predictions

Recovery prospects of a patient.  Possible features of interest, sometimes disaggregated by geography:

* electronic health records (EHR) data
* hospitalisations & recoveries
* patients' residential area  ... possible proxy for quality of housing, built environment, and air
* patient's occupation
* etc.

<br>
<br>

## Critical Considerations

Important considerations w.r.t. data collection, data handling, data representativeness, modelling, and analysis

* Ethics
* Privacy
* Data Bias (Model Bias)
* [General Data Protection Regulation (GDPR)](https://gdpr-info.eu)
* Fair AI

<br>
<br>

## Data Sources

For preliminary investigations whilst the team awaits the project data.

Official UK Data
* [data.gov.uk](https://coronavirus.data.gov.uk)
* [dowload](https://coronavirus.data.gov.uk/details/download)
* [API](https://coronavirus.data.gov.uk/details/developers-guide)


Unofficial Sources
* [Coronavirus Pandemic, Our World in Data, University of Oxford](https://ourworldindata.org/coronavirus)<br>The portal as excellent exploratory data analysis ideas & suggestions
* [Worldometer](https://www.worldometers.info/coronavirus/country/uk/)


<br>
<br>

## Research

### Modelling & Analysis

Med-BERT
* [Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction](https://www.nature.com/articles/s41746-021-00455-y)
* [Predictive Modeling on Electronic Health Records(EHR) using Pytorch](https://github.com/ZhiGroup/pytorch_ehr)

BERT: Bidirectional Encoder Representations from Transformers
* [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805)
* [GitHub: BERT](https://github.com/google-research/bert)


### Ethics, Privacy, Confidentiality

BERT & Clinical Data
* [Does BERT Pretrained on Clinical Notes Reveal Sensitive Data?](https://aclanthology.org/2021.naacl-main.73.pdf)
* [GitHub: Does BERT leak Patient Data ?](https://github.com/elehman16/exposing_patient_data_release)

Fair AI
* [Co-Designing Checklists to Understand Organizational Challenges and Opportunities around Fairness in AI](https://dl.acm.org/doi/10.1145/3313831.3376445)


<br>
<br>
<br>
<br>

<br>
<br>
<br>
<br>


