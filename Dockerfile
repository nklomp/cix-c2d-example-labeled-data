# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

FROM gcr.io/kaggle-images/python

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set MPLCONFIGDIR to a temporary directory to avoid a warning message.
ENV MPLCONFIGDIR=/tmp/

# Make sure libmagic is installed for mimetype detection
RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 && rm -rf /var/lib/apt/lists/*

# Copy the source code into the container.

WORKDIR /app
COPY algo/ .

RUN python -m pip install -r requirements.txt

# Run the application. Please note that the below line will be provided by the C2D environment and run-local.sh script
#ENTRYPOINT python algo/algo.py
