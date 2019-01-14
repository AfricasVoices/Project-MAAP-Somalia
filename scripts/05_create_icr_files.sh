#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 3 ]; then
    echo "Usage: sh 05_create_icr_files.sh <user> <data-root> <variable-name>"
    echo "Creates a file for intercoder reliability"
    exit
fi

USER=$1
DATA_ROOT=$2
VARIABLE_NAME=$3

FLOW_NAME="emergency_maap_new_pdm"
INPUT_FILE_NAME="maap_pdm_demogs_scope"

cd "../create_icr_file"

mkdir -p "$DATA_ROOT/05 ICR"


echo "Creating ICR file"
./docker-run.sh "$USER" "$DATA_ROOT/04 SCOPE with Messages/$INPUT_FILE_NAME.json" \
    "$FLOW_NAME" "$VARIABLE_NAME" "$DATA_ROOT/05 ICR/${VARIABLE_NAME}_icr.csv"
