import setuptools


NAME = 'infections'
VERSION = '0.0.1'
DESCRIPTION = 'SCC460 Project'
AUTHOR = 'greyhypotheses'
URL = 'https://github.com/premodelling/infections'
PYTHON_REQUIRES = '=3.7.5'

with open('README.md') as f:
    readme_text = f.read()

setuptools.setup()(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme_text,
    author=AUTHOR,
    url=URL,
    python_requires=PYTHON_REQUIRES,
    packages=setuptools.find_packages(exclude=['docs', 'tests'])
)