#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 8 ]; then
    echo "Usage: sh 07_merge_coda_files.sh <user> <data-root> <json-input-path> <variable-name> <coded-coda-file-path> <coding-scheme-path> <is-multi-coded> <has-yes-no>"
    echo "Merges survey data with demog data into a single traceddata object"
    exit
fi

USER=$1
DATA_ROOT=$2
INPUT_JSON=$3
VARIABLE_NAME=$4
INPUT_CODA_PATH=$5
CODING_SCHEME_PATH=$6
IS_MULTI_CODED=$7
HAS_YES_NO=$8


cd "../merge_coda_files"

mkdir -p "$DATA_ROOT/07 Coded CODA with Messages"



echo "Merging $VARIABLE_NAME CODA"
./docker-run.sh "$USER" "$JSON_INPUT_PATH" "$VARIABLE_NAME" "$INPUT_CODA_PATH"\
    "$CODING_SCHEME_PATH" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" "$IS_MULTI_CODED" "$HAS_YES_NO"
