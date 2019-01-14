#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 9 ]; then
    echo "Usage: ./06_create_coda_files.sh <user> <data-root> <json-input-path> <flow-name> <variable-name> <coding-scheme> <is-multi-coded> <has-yes-no> <auto-cleaner>"
    echo "Merges survey data with demog data into a single traceddata object"
    exit
fi
USER=$1
DATA_ROOT=$2
JSON_INPUT_PATH=$3
FLOW_NAME=$4
VARIABLE_NAME=$5
CODING_SCHEME=$6
IS_MULTI_CODED=$7
HAS_YES_NO=$8
AUTO_CLEANER=$9

cd "../create_coda_files"

mkdir -p "$DATA_ROOT/06 CODA with Messages"
mkdir -p "$DATA_ROOT/06 Uncoded CODA files"



echo "Creating CODA files for $VARIABLE_NAME"
./docker-run.sh "$USER" "$JSON_INPUT_PATH" "$FLOW_NAME" "$VARIABLE_NAME"\
     "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" \
    "$DATA_ROOT/06 Uncoded CODA files/${VARIABLE_NAME}_uncoded.json" \
    "$CODING_SCHEME" "$IS_MULTI_CODED" "$HAS_YES_NO" "$AUTO_CLEANER"
