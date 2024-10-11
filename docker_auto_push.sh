#!/bin/bash

# Define the path to the docker-compose.yml file
COMPOSE_FILE="docker-compose.yml"

# Define the Docker Hub repository and tag prefix
REPO="adamma1024/cvcoach_web"
TAG_PREFIX="v"

# Function to extract the image version from the docker-compose.yml file
extract_image_version() {
	local compose_file=$1
	local version=$(grep -A 5 "image:" "$compose_file" | grep -E "image: $REPO:$TAG_PREFIX[0-9]+\.[0-9]+" | awk -F':' '{print $3}')
	echo "$version"
}

# Function to build, tag, and push the Docker image
build_and_push() {
	local version=$1
	local image_tag="$REPO:$version"

	echo "Building image: $REPO"
	docker compose build

	echo "Tagging image: $image_tag"
	docker tag "$REPO" "$image_tag"

	echo "Pushing image: $image_tag"
	docker push "$image_tag"
}

# Main script execution
main() {
	# Ensure the docker-compose.yml file exists
	if [[ ! -f "$COMPOSE_FILE" ]]; then
		echo "Error: $COMPOSE_FILE not found."
		exit 1
	fi

	# Extract the image version for the 'web' service
	local version=$(extract_image_version "$COMPOSE_FILE")

	if [[ -z "$version" ]]; then
		echo "Error: Unable to extract image version."
		exit 1
	fi
	echo "Version: " $version

	# Build, tag, and push the Docker image
	build_and_push "$version"
}

# Run the main function
main
