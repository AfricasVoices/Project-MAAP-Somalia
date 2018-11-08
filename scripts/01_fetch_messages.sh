#!/usr/bin/env bash

set -e

if [ $# -ne 6 ]; then
    echo "Usage: sh 01_fetch_messages.sh <user> <rapid-pro-root> <rapid-pro-server> <rapid-pro-token> <data-root> <test-contacts-path>"
    echo "Downloads radio show answers from each show"
    exit
fi

USER=$1
RP_DIR=$2
RP_SERVER=$3
RP_TOKEN=$4
DATA_ROOT=$5
TEST_CONTACTS_PATH=$6

./checkout_rapid_pro_tools.sh "$RP_DIR"

cd "$RP_DIR/fetch_runs"

mkdir -p "$DATA_ROOT/01 Raw Messages"
# TODO: retrieving the demogs in 'lastest_only' mode rather than 'all'
SHOWS=(
    "emergency_maap_pdm1_survey"
    "emergency_maap_pdm2_survey"
    "emergency_maap_pdm3_survey"
    "emergency_maap_pdm4_survey"
    "emergency_maap_pdm5_survey"
    "emergency_maap_demogs"
    )

for SHOW in ${SHOWS[@]}
do
    echo "Exporting show $SHOW"

    ./docker-run.sh --flow-name "$SHOW" --test-contacts-path "$TEST_CONTACTS_PATH" \
        "$RP_SERVER" "$RP_TOKEN" "$USER" all \
        "$DATA_ROOT/00 UUIDs/phone_uuids.json" "$DATA_ROOT/01 Raw Messages/$SHOW.json"
done
