#!/bin/bash

set -e

IMAGE_NAME=maap-merge-pdm-demogs

# Check that the correct number of arguments were provided.
if [ $# -ne 4 ]; then
    echo "Usage: sh docker-run.sh <user> <pdm-json-path> <demogs-json-path> <json-output-path>"
    exit
fi

# Assign the program arguments to bash variables.
USER=$1
INPUT_PDM_JSON=$2
INPUT_DEMOGS_JSON=$3
OUTPUT_JSON=$4

# Build an image for this pipeline stage.
docker build -t "$IMAGE_NAME" .

# Create a container from the image that was just built.
container="$(docker container create --env USER="$USER" "$IMAGE_NAME")"

function finish {
    # Tear down the container when done.
    docker container rm "$container" >/dev/null
}
trap finish EXIT

# Copy input data into the container
docker cp "$INPUT_PDM_JSON" "$container:/data/pdm.json"
docker cp "$INPUT_DEMOGS_JSON" "$container:/data/demogs.json"


# Run the container
docker start -a -i "$container"

# Copy the output data back out of the container
mkdir -p "$(dirname "$OUTPUT_JSON")"
docker cp "$container:/data/output.json" "$OUTPUT_JSON"
