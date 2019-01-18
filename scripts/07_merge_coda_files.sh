#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 2 ]; then
    echo "Usage: ./07_merge_coda_files.sh <user> <data-root>"
    echo "Merges coded CODA files into a single traceddata object"
    exit
fi

USER=$1
DATA_ROOT=$2


cd "../merge_coda_files"

mkdir -p "$DATA_ROOT/07 Coded CODA with Messages"



echo "Merging Gender Coded"
./docker-run.sh "$USER" "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" \
    "Gender" "$DATA_ROOT/coded_coda_files/gender_coded.json" \
    "../coding_schemes/Gender.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "False" "False"

# After the first file is processed the input and output files are the same

echo "Merging Age"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "Age" "$DATA_ROOT/coded_coda_files/gender_coded.json" \
    "../coding_schemes/Age.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "False" "False"

echo "Merging Clan"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "Clan" "$DATA_ROOT/coded_coda_files/clan_coded.json" \
    "../coding_schemes/Clan.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "False" "False"

echo "Merging Needs Met"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "Needs_Met_Yesno" "$DATA_ROOT/coded_coda_files/needs_met_coded.json" \
    "../coding_schemes/Needs_Met_Yesno.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "True" "True"

echo "Merging Cash Modality"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "Cash_Modality_Yesno" "$DATA_ROOT/coded_coda_files/cash_modality_coded.json" \
    "../coding_schemes/Cash_Modality_Yesno.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "True" "True"

echo "Merging Community Priorities"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "Community_Priorities" "$DATA_ROOT/coded_coda_files/community_priorities_coded.json" \
    "../coding_schemes/Community_Priorities.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "True" "False"

echo "Merging Inclusion"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "Inclusion_Yes_No" "$DATA_ROOT/coded_coda_files/inclusion_coded.json" \
    "../coding_schemes/Inclusion_Yes_No.json" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json" \
    "True" "True"

