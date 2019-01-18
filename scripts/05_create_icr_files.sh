#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 2 ]; then
    echo "Usage: ./05_create_icr_files.sh <user> <data-root>"
    echo "Creates a file for intercoder reliability"
    exit
fi

USER=$1
DATA_ROOT=$2
VARIABLE_NAME=$3

FLOW_NAME="emergency_maap_new_pdm"
INPUT_FILE_NAME="maap_pdm_demogs_scope"
VARIABLES=(
    "Needs_Met_Yesno"
    "Cash_Modality_Yesno"
    "Community_Priorities"
    "Inclusion_Yes_No"
    )
cd "../create_icr_file"

mkdir -p "$DATA_ROOT/05 ICR"

for VAR in ${VARIABLES[@]}
do
    echo "Creating ICR file for $VAR"

    ./docker-run.sh "$USER" "$DATA_ROOT/04 SCOPE with Messages/$INPUT_FILE_NAME.json" \
        "$FLOW_NAME" "$VAR" "$DATA_ROOT/05 ICR/${VAR}_icr.csv"
done
