# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the workdir to avoid the "pytest Collecting hang"
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Install pytest for lab3(Even though it's ugly, from my perspective we should not add test codes in docker.)
RUN pip3 install pytest
RUN pytest

# Run the command to start the application
CMD ["python3", "app.py"]
