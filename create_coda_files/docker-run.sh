#!/bin/bash

set -e

IMAGE_NAME=maap-get-coda-files

# Check that the correct number of arguments were provided.
if [[ $# -ne 8 ]]; then
    echo "Usage: sh docker-run.sh <user> <json-input-path> <flow-name> <variable-name> <json-output-path> <coda-output-path> <coding-scheme> <auto-cleaner>"
    exit
fi

# Assign the program arguments to bash variables.
USER=$1
INPUT_JSON=$2
FLOW_NAME=$3
VARIABLE_NAME=$4
OUTPUT_JSON=$5
OUTPUT_CODA=$6
CODING_SCHEME=$7
AUTO_CLEANER=$8

# Build an image for this pipeline stage.
docker build -t "$IMAGE_NAME" .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" --env FLOW_NAME="$FLOW_NAME" --env VARIABLE_NAME="$VARIABLE_NAME" --env "AUTO_CLEANER" "$IMAGE_NAME")"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT

# Copy input data into the container
docker cp "$INPUT_JSON" "$container:/data/input.json"

# Run the container
docker start -a -i "$container"

# Copy the output data back out of the container
mkdir -p "$(dirname "$OUTPUT_JSON")"
docker cp "$container:/data/output-json.json" "$OUTPUT_CODA"

mkdir -p "$(dirname "$OUTPUT_CODA")"
docker cp "$container:/data/output-coda.json" "$OUTPUT_CODA"
