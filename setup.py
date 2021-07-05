#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


setup(
    name="openshift-python-wrapper",
    license="apache-2.0",
    description="Wrapper around https://github.com/openshift/openshift-restclient-python",
    author="Meni Yakove, Ruth Netser",
    author_email="myakove@redhat.com",
    url="https://github.com/RedHatQE/openshift-python-wrapper",
    download_url="https://github.com/RedHatQE/openshift-python-wrapper/archive/refs/tags/v1.0.tar.gz",
    keywords=["Openshift", "Kubevirt", "CNV"],
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
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
