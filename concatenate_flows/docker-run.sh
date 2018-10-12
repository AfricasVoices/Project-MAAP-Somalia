#!/bin/bash

set -e

IMAGE_NAME=maap-concatenate_pdms

# Check that the correct number of arguments were provided.
if [ $# -ne 76 ]; then
    echo "Usage: sh docker-run.sh <user> <pdm1> <pdm2> <pdm3> <pdm4> <pdm5> <combined_json>"
    exit
fi

# Assign the program arguments to bash variables.
USER = $1
PDM1 = $2
PDM2 = $3
PDM3 = $4
PDM4 = $5
PDM5 = $6
COMBINED_JSON = $7

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
docker cp "$PDM1" "$container:/data/pdm1.json"
docker cp "$PDM2" "$container:/data/pdm2.json"
docker cp "$PDM3" "$container:/data/pdm3.json"
docker cp "$PDM4" "$container:/data/pdm4.json"
docker cp "$PDM5" "$container:/data/pdm5.json"

# Run the container
docker start -a -i "$container"

# Copy the output data back out of the container
mkdir -p "$(dirname "$COMBINED_JSON")"
docker cp "$container:/data/combined_data.json" "$COMBINED_JSON"
