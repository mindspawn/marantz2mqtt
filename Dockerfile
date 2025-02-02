# Use a lightweight Python base image
FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Copy the Python script into the container
COPY marantz2mqtt.py .

# Install Python dependencies
RUN pip install --no-cache-dir \
    paho-mqtt \
    pyserial \
    python-dotenv

# By default, run the main script
CMD ["python", "marantz2mqtt.py"]
