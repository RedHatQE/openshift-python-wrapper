# Local cluster preparations
CLUSTER_DIR := local-cluster/_hco
export KUBEVIRT_PROVIDER ?= k8s-1.18
export KUBEVIRT_NUM_NODES ?= 2
export KUBEVIRT_NUM_SECONDARY_NICS ?= 4
export KUBEVIRT_WITH_CNAO=true

# Helper scripts
HACK_DIR := local-cluster/hack
CLUSTER_UP := $(HACK_DIR)/cluster-up.sh
CLUSTER_DOWN := $(HACK_DIR)/cluster-down.sh

# If not specified otherwise, local cluster's KUBECONFIG will be used
export KUBECONFIG ?= $(CLUSTER_DIR)/_kubevirtci/_ci-configs/$(KUBEVIRT_PROVIDER)/.kubeconfig

all: check

cluster-up: $(CLUSTER_UP)
	$(CLUSTER_UP)

cluster-down: $(CLUSTER_DOWN)
	$(CLUSTER_DOWN)

check: cluster-down cluster-up
	tox

.PHONY: \
	cluster-down \
	cluster-up \
	check
