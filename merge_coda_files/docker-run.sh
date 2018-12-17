#!/bin/bash

set -e

IMAGE_NAME=maap-merge-coda-files

# Check that the correct number of arguments were provided.
if [ $# -ne 7 ]; then
    echo "Usage: sh docker-run.sh <user> <json-input-path> <variable-name> <coda-input-path> <coding-scheme-path> <json-output-path> <is-yes-no>"
    exit
fi

# Assign the program arguments to bash variables.
USER=$1
INPUT_JSON=$2
VARIABLE_NAME=$3
INPUT_CODA=$4
CODING_SCHEME=$5
OUTPUT_JSON=$6
IS_YES_NO=$7

# Build an image for this pipeline stage.
docker build -t "$IMAGE_NAME" .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" --env VARIABLE_NAME="$VARIABLE_NAME" --env IS_YES_NO="$IS_YES_NO" "$IMAGE_NAME")"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT

# Copy input data into the container
docker cp "$INPUT_JSON" "$container:/data/input.json"
docker cp "$INPUT_CODA" "$container:/data/input_coda.json"
docker cp "$CODING_SCHEME" "$container:/data/coding_scheme.json"

# Run the container
docker start -a -i "$container"

# Copy the output data back out of the container
mkdir -p "$(dirname "$OUTPUT_JSON")"
docker cp "$container:/data/output.json" "$OUTPUT_JSON"
