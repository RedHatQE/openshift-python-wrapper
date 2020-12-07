# Local cluster preparations
CLUSTER_DIR := local-cluster/kubevirtci/cluster-up
CLUSTER_UP := $(CLUSTER_DIR)/up.sh
CLUSTER_DOWN := $(CLUSTER_DIR)/down.sh
CLI := $(CLUSTER_DIR)/cli.sh
SSH := $(CLUSTER_DIR)/ssh.sh
export KUBECTL ?= $(CLUSTER_DIR)/kubectl.sh
export VIRTCTL ?= $(CLUSTER_DIR)/virtctl.sh
export KUBEVIRT_PROVIDER ?= k8s-1.19
export KUBEVIRTCI_TAG ?= latest
export KUBEVIRT_NUM_NODES ?= 2
export KUBEVIRT_NUM_SECONDARY_NICS ?= 4
export VIRTCTL_VERSION ?= v0.34.2

# Helper scripts
HACK_DIR := local-cluster/hack
install_kubevirtci := $(HACK_DIR)/install-kubevirtci.sh
install_hco := $(HACK_DIR)/install-hco.sh
install_virtctl := $(HACK_DIR)/install-virtctl.sh

# virtctl binary
BIN_DIR := local-cluster/_out/bin

# If not specified otherwise, local cluster's KUBECONFIG will be used
export KUBECONFIG ?= local-cluster/kubevirtci/_ci-configs/$(KUBEVIRT_PROVIDER)/.kubeconfig

# Expose local binaries to tests
export PATH := $(BIN_DIR):$(PATH)

$(CLUSTER_DIR)/%: $(install_kubevirtci)
	$(install_kubevirtci)

cluster-up: $(CLUSTER_UP) $(VIRTCTL)
	$(CLUSTER_UP)

cluster-down: $(CLUSTER_DOWN)
	$(CLUSTER_DOWN)

cluster-install-hco: $(KUBECTL)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(VIRTCTL): $(BIN_DIR)
	VIRTCTL_DEST=$(VIRTCTL) $(install_virtctl)
	touch $(VIRTCTL)

.PHONY: \
	cluster-down \
	cluster-install-hco \
	cluster-up
