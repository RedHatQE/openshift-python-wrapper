#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


setup(
    name="ocp-python-wrapper",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "kubernetes",
        "openshift",
        "xmltodict",
        "urllib3",
        "netaddr",
        "paramiko",
        "pbr",
    ],
    python_requires=">=3.6",
)
