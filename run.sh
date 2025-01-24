#!/bin/bash

# Build the Docker image
echo "Building the Docker image..."
docker build -t magic-ai .
if [ $? -ne 0 ]; then
  echo "Docker build failed. Exiting."
  exit 1
fi
echo "Docker image built successfully."

# Run the Docker container
echo "Running the Docker container..."
docker run -d -p 5000:5000 --name magic-ai-container magic-ai
if [ $? -ne 0 ]; then
  echo "Failed to run the Docker container. Exiting."
  exit 1
fi
echo "Docker container is running on port 5000:5000."

# Verify the container is running
echo "Verifying the container status..."
docker ps | grep magic-ai-container > /dev/null
if [ $? -ne 0 ]; then
  echo "Container is not running as expected. Check logs for details."
  exit 1
fi
echo "Container is running successfully."
