FROM alpine:latest

# Update the package index and install Python 3 and pip
RUN apk update && \
    apk add python3 py3-pip

# Make Python 3 the default Python interpreter
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Clean up the package cache to reduce the image size
RUN rm -rf /var/cache/apk/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000/tcp

# Run app.py when the container launches
CMD ["python", "/app/main.py"]
