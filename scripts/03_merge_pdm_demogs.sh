#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 2 ]; then
    echo "Usage: sh 03_maap_pdm_demogs.sh <user> <data-root>"
    echo "Merges the flows together."
    exit
fi

USER=$1
DATA_ROOT=$2

mkdir -p "$DATA_ROOT/03 PDM Demogs Merged"

INPUT_FOLDER="$DATA_ROOT/01 Raw Messages"
OUTPUT_FOLDER="$DATA_ROOT/03 PDM Demogs Merged"

cd ../merge_pdm_demog

PDM="emergency_maap_new_pdm"
DEMOGS="emergency_maap_new_demogs"

echo "Merging PDM survey and demographics"

./docker-run.sh "$USER" "$INPUT_FOLDER/$PDM.json" "$INPUT_FOLDER/$DEMOGS.json" \
    "$OUTPUT_FOLDER/maap_pdm_demogs.json" \
