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

# Function to stop old Docker image
stop_and_remove() {
	local version=$(extract_image_version "$COMPOSE_FILE")
	local image_tag="$REPO:$version"
	# Stop the currently running container (if any) for the image
	echo "Stopping the current container for $image_tag"
	CURRENT_CONTAINER=$(docker ps -q -f ancestor=$image_tag)
	if [ -n "$CURRENT_CONTAINER" ]; then
		docker stop $CURRENT_CONTAINER
		echo "Removing the current container for $CURRENT_CONTAINER"
		docker rm $CURRENT_CONTAINER
	else
		echo "No running container found for $REPO."
	fi

	# Remove the existing image
	echo "Removing the existing image $image_tag..."
	docker rmi $image_tag
}

# Function to pull and start the new Docker image
pull_and_start() {
	local version=$(extract_image_version "$COMPOSE_FILE")
	local image_tag="$REPO:$version"
	# Pull the latest version of the image with the specified tag
	echo "Pulling the latest version of $image_tag..."
	docker pull $image_tag

	# Run the new image
	echo "Running the new image $image_tag..."
	docker run -d -p 8081:8081 $image_tag

	echo "Update and run completed successfully."
}

# Main function to handle command-line arguments
function main() {
	case "$1" in
	stop)
		stop_and_remove
		;;
	start)
		pull_and_start
		;;
	*)
		echo "Usage: $0 {stop|start}"
		exit 1
		;;
	esac
}

# Call the main function with the first command-line argument
main "$1"
