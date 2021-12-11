
<br>

**SCC460 Group Project: Infections**

* [Project](#project)
  * [Predicting Hospitalisation Trends](#predicting-hospitalisations-trend)
  * [Critical Considerations](#critical-considerations)
  * [Data Sources](#data-sources)
  * [References](#references)
  
* [Development Environment](#development-environment)
  * [Virtual Environment](#virtual-environment)


<br>

## Project

### Predicting Hospitalisations Trend

Features of interest, sometimes disaggregated by geography:

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


<br>
<br>
<br>

## Development Environment

### Virtual Environment

**Windows Operating System & `cmd`**

Within the prospective project directory, and via[`venv`](https://docs.python.org/3/library/venv.html)

```
>> python -m venv env
```

Activate the environment via

```
>> env\Scripts\activate.bat
```

This can be deactivated via the command `env\Scripts\deactivate.bat`.  Use the command

```
>> env\Scripts\pip list
```

to list the set of directly & indirectly installed packages.  Always remember to upgrade pip before populating the environment

```
>> python -m pip install --upgrade pip==21.3.1
```

The [requirements](requirements.txt) document lists the directly installed packages and their versions; and a few
indirectly installed pckages.  Thus far, the TensorFlow version used by this project is TensorFlow 2.7.0

```
>> env\Scripts\pip install --upgrade tensorflow==2.7.0
```



<br>
<br>
<br>
<br>

<br>
<br>
<br>
<br>


