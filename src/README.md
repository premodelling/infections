

## preprocessing

### districts

the [districts](./preprocessing/districts.py) program [creates data files](../warehouse/geography/districts) of 
geographic mappings between middle super output area (MSOA) codes & lower tier local authority (LTLA) codes consists of

variable | description
 :--- | :---
``MSOA11CD`` | middle super output area code
``MSOA11NM`` | middle super output area name
``LAD{}CD`` | local area district code, { } &rarr; double-digit year
``LAD{}NM`` | local area district name, { } &rarr; double-digit year

The lower tier local authority (LTLA) is also known as local authority district (LAD).

<br>
<br>

### patients

the [patients](./preprocessing/patients.py) program creates each 
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
<br>

### populations: msoa

The office for national statistics (ONS) creates MSOA population estimates by age and sex. The MSOA
[populations](./preprocessing/populationsmsoa.py) & [age groups](./preprocessing/agegroupsmsoa.py) programs merge, structure, and aggregate the data 
to create [data sets](../warehouse/populations/msoa) with headers

<ul>
    <li><div style='font-size: small'>msoa,ltla,sex,0-4,5-9,10-14,15-19,20-24,25-29,30-34,35-39,40-44,45-49,50-54,55-59,60-64,65-69,70-74,<br>
        75-79,80-84,85-89,90+</div></li>
    <li><div style='font-size: small'>msoa,ltla,sex,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,<br>
        32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,<br>
        64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90+</div></li>
</ul>

<br>
<br>

### populations: ltla

The LTLA [populations](./preprocessing/populationsltla.py) & [age groups](./preprocessing/agegroupsltla.py) programs depend on the created MSOA 
data sets, and create [data sets](../warehouse/populations/ltla) with headers

<ul>
    <li><div style='font-size: small'>ltla,sex,0-4,5-9,10-14,15-19,20-24,25-29,30-34,35-39,40-44,45-49,50-54,55-59,60-64,65-69,70-74,<br>
        75-79,80-84,85-89,90+</div></li>
    <li><div style='font-size: small'>ltla,sex,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,<br>
        33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,<br>
        64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90+</div></li>
</ul>


<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>


