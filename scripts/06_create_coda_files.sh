#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 2 ]; then
    echo "Usage: ./06_create_coda_files.sh <user> <data-root>"
    echo "Merges survey data with demog data into a single traceddata object"
    exit
fi
USER=$1
DATA_ROOT=$2

cd "../create_coda_files"

mkdir -p "$DATA_ROOT/06 CODA with Messages"
mkdir -p "$DATA_ROOT/06 Uncoded CODA files"


echo "Creating CODA files for Gender"
./docker-run.sh "$USER" "$DATA_ROOT/04 SCOPE with Messages/maap_pdm_demogs_scope.json" "emergency_maap_new_demogs" \
    "Gender" "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" \
    "$DATA_ROOT/06 Uncoded CODA files/gender_uncoded.json" \
    "../coding_schemes/Gender.json" "False" "False" "gender"

# After the first file is processed the input and output files are the same

echo "Creating CODA files for Age"
./docker-run.sh "$USER" "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "emergency_maap_new_demogs" "Age" \
    "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "$DATA_ROOT/06 Uncoded CODA files/age_uncoded.json" \
    "../coding_schemes/Age.json" "False" "False" "age"

echo "Creating CODA files for Clan"
./docker-run.sh "$USER" "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "emergency_maap_new_demogs" "Clan" \
    "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "$DATA_ROOT/06 Uncoded CODA files/clan_uncoded.json" \
    "../coding_schemes/Clan.json" "False" "False" "None"

echo "Creating CODA files for Needs Met"
./docker-run.sh "$USER" "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "emergency_maap_new_pdm" "Needs_Met_Yesno" \
    "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "$DATA_ROOT/06 Uncoded CODA files/needs_met_uncoded.json" \
    "../coding_schemes/Needs_Met_Yesno.json" "True" "True" "None"

echo "Creating CODA files for Cash Modality"
./docker-run.sh "$USER" "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "emergency_maap_new_pdm" "Cash_Modality_Yesno" \
    "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "$DATA_ROOT/06 Uncoded CODA files/cash_modality_uncoded.json" \
    "../coding_schemes/Cash_Modality_Yesno.json" "True" "True" "None"

echo "Creating CODA files for Community Priorities"
./docker-run.sh "$USER" "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "emergency_maap_new_pdm" "Community_Priorities" \
    "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "$DATA_ROOT/06 Uncoded CODA files/community_priorities_uncoded.json" \
    "../coding_schemes/Community_Priorities.json" "True" "False" "None"

echo "Creating CODA files for Inclusion"
./docker-run.sh "$USER" "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "emergency_maap_new_pdm" "Inclusion_Yes_No" \
    "$DATA_ROOT/06 CODA with Messages/coda_with_messages.json" "$DATA_ROOT/06 Uncoded CODA files/inclusion_uncoded.json" \
    "../coding_schemes/Inclusion_Yes_No.json" "True" "True" "None"
