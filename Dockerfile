FROM python:3.11
LABEL authors="Jairo Matos da Rocha"
# Use an official Python runtime as a parent image
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/
COPY install.py /app/

# Install any needed packages specified in requirements.txt
RUN apt update && \
    apt install --no-install-recommends -y  nano \
    screen && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt && \
    python install.py

CMD ["tail", "-f", "/dev/null"]