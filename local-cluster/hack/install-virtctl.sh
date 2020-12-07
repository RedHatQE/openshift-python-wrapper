#!/bin/bash -e

VIRTCTL_BIN_SOURCE=https://github.com/kubevirt/kubevirt/releases/download/${VIRTCTL_VERSION}/virtctl-${VIRTCTL_VERSION}-linux-amd64

wget ${VIRTCTL_BIN_SOURCE} -O ${VIRTCTL_DEST}
chmod +x ${VIRTCTL_DEST}
