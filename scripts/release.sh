#!/usr/bin/env bash

# Usage: ./scripts/release.sh main v1.5.3
# Run from main branch

set -e

SETUP_CFG="setup.cfg"
BASE_SOURCE_BRANCH="$1"
VERSION="$2"
STRIPPED_VERSION="${VERSION//v/}"
REMOTE_ORIGIN=$(grep -A3 '\[remote "origin"\]' .git/config)
main_BRANCH="main"
TARGET_BRANCH="branch-$VERSION" # New branch for the release; formatted: branch-vx.y.z[.i]

if [[ $REMOTE_ORIGIN != *"github.com:RedHatQE/openshift-python-wrapper"* ]]; then
  echo "This script shouldn't run from forked repo!"
  exit 1
fi

if [[ -z "${GREN_GITHUB_TOKEN}" ]]; then
  echo "GREN_GITHUB_TOKEN is undefined"
  exit 1
fi

if [[ $(git branch --show-current) != "$main_BRANCH" ]]; then
  echo "Script must be executed from main branch"
  exit 1
fi

# checkout source branch
if ! git checkout origin/"$BASE_SOURCE_BRANCH"; then
  echo "Source branch origin/$BASE_SOURCE_BRANCH does not exist"
  exit 1
fi

# update source branch
if ! git pull origin "$BASE_SOURCE_BRANCH"; then
  echo "Failed to pull latest code from origin/$BASE_SOURCE_BRANCH"
  exit 1
fi

if ! git checkout "$BASE_SOURCE_BRANCH"; then
  git switch -c "$BASE_SOURCE_BRANCH"
fi

OLD_VERSION=$(grep version setup.cfg | awk -F' = ' '{print $2}')

# Update setup.cfg with the new version and push to $TARGET_BRANCH
sed -i s/"$OLD_VERSION"/"$STRIPPED_VERSION"/g "$SETUP_CFG"
git commit -am "Update version: $TARGET_BRANCH"
git push origin -f "$BASE_SOURCE_BRANCH"

# Create branch for the new release
if ! git checkout -b "$TARGET_BRANCH" origin/"$BASE_SOURCE_BRANCH"; then
  echo "Failed to create new branch $TARGET_BRANCH"
  exit 1
fi

# Create release on Github
gh release create "$VERSION"

# Generate release notes
gren release -D prs --override

# Generate and push CHANGELOG.md
gren changelog --override
git commit -am "Update changelog for version $VERSION"
git push -f origin "$TARGET_BRANCH"

git pull origin "$TARGET_BRANCH"
git checkout "$main_BRANCH"
