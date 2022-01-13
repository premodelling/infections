<br>

# Development Notes

* [Virtual Development Environment](#virtual-development-environment)
  * [Anaconda, Conda](#anaconda-conda)
  * [venv](#venv)
  
* [Code Snippets](#code-snippets)
  * [data.gov.uk SARS-CoV-2 API](#sars-cov-2-api)
  
* [References](#references)
    
<br>
<br>

## Virtual Development Environment

### Anaconda, Conda

```bash
  conda create --prefix .../environmentName
  conda activate environmentName
```

Hence

```bash
    conda install -c anaconda python==3.7.11
    
    # tensorflow
    pip install tensorflow==2.7.0
    
    conda install -c anaconda pandas # installs: numpy, etc.    
    conda install -c anaconda seaborn # installs: matplotlib, scipy, etc. 
    conda install -c anaconda pytest coverage pytest-cov pylint flake8
    conda install -c anaconda nodejs pywin32 jupyterlab # installs: requests, urllib3, etc.
    conda install -c anaconda python-graphviz
    conda install -c anaconda arviz
    
    # distributed computing
    conda install -c anaconda dask
    
    # For Excel
    conda install -c anaconda xlrd
    
    

```

For more about Dask, refer to https://docs.dask.org/en/latest/install.html

<br>
<br>

### venv

<br>

Focusing the **Windows Operating System & `cmd`**, within the prospective project directory the command

```
# Visit https://docs.python.org/3/library/venv.html for more details about venv

>> python -m venv env

```

<br>

will create a virtual environment.  Activate the environment via

```
>> env\Scripts\activate.bat
```

<br>

This can be deactivated via the command `env\Scripts\deactivate.bat`.  Use the command

```
>> env\Scripts\pip list
```

<br>

to list the set of directly & indirectly installed packages.  Always remember to upgrade pip before populating the environment

```
>> python -m pip install --upgrade pip==21.3.1
```

<br>

Hence, install ``tensorflow`` via command


```
>> env\Scripts\pip install --upgrade tensorflow==2.7.0
```

<br>
<br>

## Code Snippets

### SARS-CoV-2 API

Reading measures via JSON

```python

import requests
import logging

# noinspection PyTypeChecker
logging.basicConfig(level=logging.INFO,
                    format='%(message)s\n%(asctime)s.%(msecs)03d', 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# url string
url = ''

# data request via url string
try:
    response = requests.get(url=url)
    response.raise_for_status()
except requests.RequestException as err:
    raise Exception(err)

# status check
if response.status_code > 204:
    raise RuntimeError(response.text)

logger.info(response.json())

```

<br>

### Periodicity

````python
import tensorflow as tf

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


class FFT:

  def __init__(self):
    """
    Constructor
    """

  @staticmethod
  def fft(data: pd.DataFrame):
    fourier = tf.signal.rfft(data['dailyCases'])

    indices = np.arange(0, len(fourier))

    n_samples = data.shape[0]
    days_per_week = 7
    n_weeks = n_samples / days_per_week

    return indices / n_weeks

  def exc(self, data: pd.DataFrame):
    frequencies = self.fft(data=data)

    plt.step(frequencies, np.abs(FFT))
    plt.xscale('log')

    for spine in plt.gca().spines.values():
      spine.set_visible(False)
    plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')
    plt.xticks([1, 7], labels=['1/week', '1/day'])

````

<br>
<br>

## References

**dask**
* [dask.dataframe.read_csv](https://docs.dask.org/en/stable/generated/dask.dataframe.read_csv.html)
* [dask.dataframe.to_csv](https://docs.dask.org/en/stable/generated/dask.dataframe.to_csv.html)
* [DataFrame API](https://docs.dask.org/en/stable/dataframe-api.html)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>