#!/bin/bash

set -e

# Check that the correct number of arguments were provided.
if [ $# -ne 2 ]; then
    echo "Usage: ./08_create_analysis_files.sh <user> <data-root>"
    echo "Creates the files for analysis"
    exit
fi

USER=$1
DATA_ROOT=$2


cd "../analysis_file"

mkdir -p "$DATA_ROOT/08 Analysis Files"



echo "Creating analysis files"
./docker-run.sh "$USER" "$DATA_ROOT/07 Coded CODA with Messages/coded_coda_with_messages.json"\
    "$DATA_ROOT/08 Analysis Files/analysis.json" "$DATA_ROOT/08 Analysis Files/analysis_by_message.json"\
    "$DATA_ROOT/08 Analysis Files/analysis_by_individual.json"
