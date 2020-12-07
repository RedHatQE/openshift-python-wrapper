#!/bin/bash -e

set -x

HCO_NS='kubevirt-hyperconverged'
HCO_VERSION='master'
HCO_SOURCES="https://raw.githubusercontent.com/kubevirt/hyperconverged-cluster-operator/${HCO_VERSION}"
HCO_RESOURCES='crds/hco00.crd.yaml
crds/hco01.crd.yaml
crds/hco02.crd.yaml
crds/hostpath-provisioner00.crd.yaml
crds/kubevirt00.crd.yaml
crds/containerized-data-importer00.crd.yaml
crds/cluster-network-addons00.crd.yaml
crds/scheduling-scale-performance00.crd.yaml
crds/scheduling-scale-performance02.crd.yaml
crds/scheduling-scale-performance03.crd.yaml
crds/node-maintenance00.crd.yaml
crds/scheduling-scale-performance01.crd.yaml
crds/vm-import-operator00.crd.yaml
cluster_role.yaml
service_account.yaml
cluster_role_binding.yaml
operator.yaml
hco.cr.yaml
'

# Create the namespaces for the HCO
if [[ $(${KUBECTL} get ns ${HCO_NS}) == '' ]]; then
    ${KUBECTL} create ns ${HCO_NS}
fi

# Create additional namespaces needed for HCO components
namespaces=('openshift' 'openshift-machine-api')
for namespace in ${namespaces[@]}; do
    if [[ $(${KUBECTL} get ns ${namespace}) == '' ]]; then
        ${KUBECTL} create ns ${namespace}
    fi
done

# Switch to the HCO namespace.
${KUBECTL} config set-context $(${KUBECTL} config current-context) --namespace=kubevirt-hyperconverged

# Create all resources of HCO and its operators
for resource in ${HCO_RESOURCES}; do
    ${KUBECTL} apply -f ${HCO_SOURCES}/deploy/${resource}
done

function wait_until_available() {
  ${KUBECTL} wait hyperconverged kubevirt-hyperconverged --for condition=Available --timeout=1m
  return $?
}

function setup_virt_emulation() {
  # Turn virtualization emulation if requested
  if [[ "${VIRT_EMULATION}" == "1" ]]; then
      echo "Enabling virt emulation"
      ${KUBECTL} patch configmap kubevirt-config -p '{"data": {"debug.useEmulation": "true"}}'

      ${KUBECTL} rollout restart deployment virt-controller -n ${HCO_NS}
  fi
}

set +e
for i in {0..30}
do
  echo "Try Number: $i"
  wait_until_available
  [ $? -eq 0 ] && setup_virt_emulation && exit 0
done
set -e


${KUBECTL} get hyperconverged kubevirt-hyperconverged -o yaml
# TODO WIP, checking why linux-bridge CNI doesn't get up withing the timeout
${KUBECTL} get ds --all-namespaces -o yaml | grep bridge
${KUBECTL} describe ds -n linux-bridge
${KUBECTL} get pods --all-namespaces -o yaml | grep bridge
echo 'Timed out while waiting for HyperConverged to become ready'
exit 1
