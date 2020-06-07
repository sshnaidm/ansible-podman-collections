#!/bin/bash

set -eux

if [[ -z "$1" ]]; then
    echo "Please provide a tag!"
    exit 1
fi

echo "Start building collection"
echo "Generating galaxy.yml for version $1"
./contrib/build.py "$1"

rm -rf build_artifact
mkdir -p build_artifact

ansible-galaxy collection build --force --output-path build_artifact/
COLLECTION_P=$(ls build_artifact/*tar.gz)

echo "Publishing collection $COLLECTION_P"

output=$(python -m galaxy_importer.main $COLLECTION_P)
if echo $output | grep ERROR: ; then
    echo "Failed check of galaxy importer!"
    exit 1
fi

echo "Running: ansible-galaxy collection publish --token HIDDEN $COLLECTION_P"
ansible-galaxy collection publish --token $API_GALAXY_TOKEN $COLLECTION_P
