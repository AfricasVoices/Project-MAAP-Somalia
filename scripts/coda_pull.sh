#!/usr/bin/env bash

set -e

TOOLS_ROOT=""
DATA_ROOT=""
PROJECT_NAME="MAAP"
AUTH=""

DATASETS=(
    "community_priorities"
    "demogs_gender"
    "demogs_age"
    "demogs_clan"
    "needs_met"
    "cash_modality"
    "inclusion"
)

cd "$TOOLS_ROOT"

for DATASET in ${DATASETS[@]}
do
    echo "Pulling $DATASET"

    pipenv run python get.py "$AUTH" "${PROJECT_NAME}_${DATASET}" messages >"$DATA_ROOT/coded_coda_files/${DATASET}_coded.json"
done
