#!/usr/bin/env bash

# Usage: ./release.sh v1.5.5

SETUP_CFG="setup.cfg"
VERSION="$1"
OLD_VERSION=$(grep version setup.cfg | awk -F' = ' '{print $2}')
REMOTE_ORIGIN=$(grep -A3 '\[remote "origin"\]' .git/config)

if [[ $REMOTE_ORIGIN != *"github.com:RedHatQE/openshift-python-wrapper"* ]]; then
  echo "This script shouldn't run from forked repo!"
fi

# Update setup.cfg with the new version and push to master
sed -i s/$OLD_VERSION/$VERSION/g $SETUP_CFG
git commit -a -m"Update version: $VERSION"
git push origin master

# Create release on Github
gh release create $VERSION

# Generate release notes
gren release -D prs --override

# Generate and push CHANGELOG.md
gren changelog --override
git commit -a -m"Update changelog for version $VERSION"
git push -f origin master

# Create branch for the new release
git checkout -b $VERSION
git push origin $VERSION
git checkout master
git pull origin master
