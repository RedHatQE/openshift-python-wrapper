# openshift-python-wrapper
Pypi: [openshift-python-wrapper](https://pypi.org/project/openshift-python-wrapper)  
A python wrapper for [openshift-restclient-python](https://github.com/openshift/openshift-restclient-python) with support for RedHat Container Virtualization. ([Openshift Virtualization](https://www.openshift.com/learn/topics/virtualization))  
Docs: [openshift-python-wrapper docs](https://openshift-python-wrapper.readthedocs.io/en/latest/)

## Installation
From source:
```bash
git clone https://github.com/RedHatQE/openshift-python-wrapper.git
cd openshift-python-wrapper
python setup.py install --user
```
From pypi:
```bash
pip install openshift-python-wrapper --user
```

## Release new version
### requirements:
* Export GitHub token
```bash
export GITHUB_TOKEN=<your_github_token>
```
* [release-it](https://github.com/release-it/release-it)
```bash
sudo npm install --global release-it
npm install --save-dev @release-it/bumper
```
### usage:
* Create a release, run from the relevant branch.  
To create a 4.11 release, run:
```bash
git checkout v4.11
git pull
release-it # Follow the instructions
```

## docs
Hosted on readthedocs.io [openshift-python-wrapper](https://openshift-python-wrapper.readthedocs.io/en/latest/)

## PR dependency
For PR dependency we use [dpulls](https://www.dpulls.com/)  
To make PR depends on other PR add `depends on #<PR NUMBER>` in the PR description.

## Logging configuration
To change log level export OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL:  

```bash
export OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL=<LOG_LEVEL> # can be: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
```

## Code check
We use pre-commit for code check.
```bash
pre-commit install
```

Some code examples locate at `examples` directory
