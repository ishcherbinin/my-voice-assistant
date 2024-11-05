# Use a base image with Python
FROM python:3.12.4

# Install gcc, essential libraries, and PortAudio
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    build-essential \
    libffi-dev \
    libssl-dev \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Copy your application code into the container
COPY . .

# Run your application
CMD ["python", "main.py"]
