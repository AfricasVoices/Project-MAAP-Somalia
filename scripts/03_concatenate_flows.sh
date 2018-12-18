#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 2 ]; then
    echo "Usage: sh 03_concatenate_flows.sh <user> <data-root>"
    echo "Concatenates the flows together"
    exit
fi

USER=$1
DATA_ROOT=$2

MESSAGES_FOLDER="$DATA_ROOT/01 Raw Messages"

cd ../concatenate_flows

SURVEY="emergency_maap_pdm"

echo "Merging PDM surveys"

./docker-run.sh "$USER" "$MESSAGES_FOLDER/emergency_maap_pdm1_survey.json" \
    "$MESSAGES_FOLDER/emergency_maap_pdm2_survey.json" \
    "$MESSAGES_FOLDER/emergency_maap_pdm3_survey.json" \
    "$MESSAGES_FOLDER/emergency_maap_pdm4_survey.json" \
    "$MESSAGES_FOLDER/emergency_maap_pdm5_survey.json" \
    "$MESSAGES_FOLDER/$SURVEY.json"
