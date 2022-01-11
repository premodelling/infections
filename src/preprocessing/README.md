
<br>

### Preprocessing

The programs herein process baseline geographic, patient flow, and population data that have been extracted/downloaded 
from official U.K. government site.

<br>

#### Districts

The [districts](./districts.py) program [creates data files](../../warehouse/geography/districts) of geographic 
mappings between middle super output area (MSOA) codes & lower tier local authority (LTLA).  Note that the lower 
tier local authority (LTLA) is also known as local authority district (LAD).   The mapped codes are:

variable | description
 :--- | :---
``MSOA11CD`` | middle super output area code
``MSOA11NM`` | middle super output area name
``LAD{}CD`` | local area district code, { } is a year placeholder, e.g., LAD19CD, LAD20CD, etc.
``LAD{}NM`` | local area district name, { } is a year placeholder, e.g., LAD13NM, LAD19NM, etc.


<br>

#### Patients

The [patients](./patients.py) program creates each year's [*patients flow from MSOA to trust*](../../warehouse/patients)
 data file. The variables therein are:

variable | description
 :--- | :---
``catchment_year`` | year
``msoa``| the code of the MSOA whence the patients originated
``trust_code`` | the code of the NHS trust that received the MSOA patients
``patients_from_msoa_to_trust`` | the number of patients from the MSOA to the NHS Trust
``total_patients_of_msoa`` | the total number of patients that originated from<br>the MSOA during the catchment year in question
``ltla``| the code of the LTLA that the MSOA belongs to


<br>

#### Populations: MSOA

The office for national statistics (ONS) creates MSOA population estimates by age and sex. The MSOA
[populations](./populationsmsoa.py) & [age groups](./agegroupsexmsoa.py) programs merge, structure, and aggregate 
the data to create [data sets](../../warehouse/populations/msoa) that have the age groups required for the project.

variable | description
 :--- | :---
``msoa`` | The MSOA code
``ltla`` | The LTLA code
``sex`` | female, male
``0-4``, ``5-9``, ... <br>``85-89``, ``90+`` | The age group fields, each of length 5 years, except the last<br> group, which includes everyone of age ``90`` and over.

<br>

#### Populations: LTLA

The LTLA [populations](./populationsltla.py) & [age groups](./agegroupsexltla.py) programs depend on the created MSOA
data sets, and create [data sets](../../warehouse/populations/ltla) that have the age groups required for the project.

variable | description
 :--- | :---
``ltla`` | The LTLA code
``sex`` | female, male
``0-4``, ``5-9``, ... <br>``85-89``, ``90+`` | The age group fields, each of length 5 years, except the last<br> group, which includes everyone of age ``90`` and over.


<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>