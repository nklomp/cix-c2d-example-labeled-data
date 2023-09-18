#!/bin/bash
# We are overriding the entrypoint here, so we can use the docker image for testing and in the c2d environment at the same time
docker run -v "$(pwd)"/data:/data --entrypoint python sphereon/cix-labeled-data-example:latest algo.py
