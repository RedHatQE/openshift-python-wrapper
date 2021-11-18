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
        "openshift",
        "xmltodict",
        "urllib3",
    ],
    python_requires=">=3.6",
)
