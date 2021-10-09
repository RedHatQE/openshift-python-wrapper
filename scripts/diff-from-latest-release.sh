#!/usr/bin/env bash

DIR=$(dirname $(readlink -f $0))
echo $DIR
LATEAST_RELEASE=$($DIR/get-latest-release.sh)
$DIR/diff-from-tag.sh $LATEAST_RELEASE
