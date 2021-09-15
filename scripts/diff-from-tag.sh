#!/usr/bin/env bash

# Simple script to show diff from specific tag
# usage: ./diff-from-tag.sh v2.0.3

TAG=$1
echo "Diff from tag: $TAG"
echo ""
git log --pretty="%h - %s (%an)" $TAG..HEAD | grep Merge
