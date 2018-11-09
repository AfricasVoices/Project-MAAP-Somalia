#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 3 ]; then
    echo "Usage: sh 04_create_icr_files.sh <user> <data-root> <variable-name>"
    echo "Creates a file for intercoder reliability"
    exit
fi

USER=$1
DATA_ROOT=$2
VARIABLE_NAME=$3

FLOW_NAME="emergency_maap_pdm"

cd "../create_icr_file"

mkdir -p "$DATA_ROOT/04 ICR"


echo "Creating ICR file"
./docker-run.sh "$USER" "$DATA_ROOT/01 Raw Messages/${FLOW_NAME}.json" \
    "$FLOW_NAME" "$VARIABLE_NAME" "$DATA_ROOT/04 ICR/${VARIABLE_NAME}_icr.csv"
