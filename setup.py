#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


setup(
    name="openshift-python-wrapper",
    license="apache-2.0",
    keywords=["Openshift", "Kubevirt", "CNV"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kubernetes",
        "openshift!=0.13.0",  # 0.13.0 is broken https://github.com/openshift/openshift-restclient-python/issues/425
        "xmltodict",
        "urllib3",
        "colorlog",
    ],
    python_requires=">=3.6",
)
