#!/bin/bash

set -e

IMAGE_NAME=maap-concatenate-pdms

# Check that the correct number of arguments were provided.
if [ $# -ne 7 ]; then
    echo "Usage: sh docker-run.sh <user> <pdm1> <pdm2> <pdm3> <pdm4> <pdm5> <combined_json>"
    exit
fi

# Assign the program arguments to bash variables.
USER=$1
INPUT_PDM1=$2
INPUT_PDM2=$3
INPUT_PDM3=$4
INPUT_PDM4=$5
INPUT_PDM5=$6
OUTPUT_COMBINED_JSON=$7

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
docker cp "$INPUT_PDM1" "$container:/data/pdm1.json"
docker cp "$INPUT_PDM2" "$container:/data/pdm2.json"
docker cp "$INPUT_PDM3" "$container:/data/pdm3.json"
docker cp "$INPUT_PDM4" "$container:/data/pdm4.json"
docker cp "$INPUT_PDM5" "$container:/data/pdm5.json"

# Run the container
docker start -a -i "$container"

# Copy the output data back out of the container
mkdir -p "$(dirname "$OUTPUT_COMBINED_JSON")"
docker cp "$container:/data/combined_data.json" "$OUTPUT_COMBINED_JSON"
