# Use the official Python runtime as a parent image
FROM python:3.10.12-slim

# Set the working directory in the container
WORKDIR /{{cookiecutter.__directory_name}}

# Copy the contents of the directory into the container
COPY . /{{cookiecutter.__directory_name}}

# Install packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD sleep infinity