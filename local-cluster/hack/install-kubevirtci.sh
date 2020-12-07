#!/bin/bash -e

script_dir=$(dirname "$(readlink -f "$0")")
kubevirtci_dir=local-cluster/kubevirtci

rm -rf $kubevirtci_dir
git clone https://github.com/kubevirt/kubevirtci.git $kubevirtci_dir
