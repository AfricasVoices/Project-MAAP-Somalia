#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 8 ]; then
    echo "Usage: ./07_merge_coda_files.sh <user> <data-root> <json-input-path> <variable-name> <coded-coda-file-path> <coding-scheme-path> <is-multi-coded> <has-yes-no>"
    echo "Merges coded CODA files into a single traceddata object"
    exit
fi

USER=$1
DATA_ROOT=$2
INPUT_JSON=$3
VARIABLE_NAME=$4
INPUT_CODA_PATH=$5
CODING_SCHEME_PATH=$6True=$7
HAS_YES_NO=$8


cd "../merge_coda_files"

mkdir -p "$DATA_ROOT/07 Coded CODA with Messages"



echo "Merging Gender Coded"
./docker-run.sh "$USER" "$JSON_INPUT_PATH" "Gender" "$DATA_ROOT/coded_coda_files/gender_coded.json"\
    "../coding_schemes/Gender.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "False" "False"

# After the first file is processed the input and output files are the same

echo "Merging Age"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "Age" "$DATA_ROOT/coded_coda_files/gender_coded.json"\
    "../coding_schemes/Age.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "False" "False"

echo "Merging Clan"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "Clan" "$DATA_ROOT/coded_coda_files/clan_coded.json"\
    "../coding_schemes/Clan.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "False" "False"

echo "Merging Needs Met"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "Needs_Met_Yesno" "$DATA_ROOT/coded_coda_files/needs_met_coded.json"\
    "../coding_schemes/Needs_Met_Yesno.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "True" "True"

echo "Merging Cash_Modality_Yesno"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "$Cash_Modality_Yesno" "$$DATA_ROOT/coded_coda_files/cash_modality_coded.json"\
    "../coding_schemes/Cash_Modality_Yesno.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "True" "True"

echo "Merging Community_Priorities CODA"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "Community_Priorities" "$$DATA_ROOT/coded_coda_files/communtiry_priorities.json"\
    "../coding_schemes/Community_Priorities.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "True" "False"

echo "Merging $Inclusion_Yes_No CODA"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "Inclusion_Yes_No" "$$DATA_ROOT/coded_coda_files/inclusion_coded.json"\
    "../coding_schemes/Inclusion_Yes_No.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "True" "True"

