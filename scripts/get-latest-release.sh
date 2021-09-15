#!/usr/bin/env bash

# From: https://gist.github.com/lukechilds/a83e1d7127b78fef38c2914c4ececc3c#file-get_latest_release-sh

curl --silent "https://api.github.com/repos/RedHatQE/openshift-python-wrapper/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'
