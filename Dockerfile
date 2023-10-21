FROM python:3.11
LABEL authors="Jairo Matos da Rocha"
# Use an official Python runtime as a parent image
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to start an interactive shell
CMD [ "bash" ]