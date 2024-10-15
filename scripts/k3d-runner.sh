#!/bin/bash

set -e

k3d_installer="/tmp/k3d.sh"
action="$1"

if [ "$action" = "start" ]; then
  echo "Installing k3d..."
  curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh >"$k3d_installer"
  chmod +x "$k3d_installer"
  "$k3d_installer"
  rm -rf "$k3d_installer"
  k3d cluster create opw-local-cluster

elif [ "$action" = "stop" ]; then
  k3d cluster delete opw-local-cluster
fi
