# Multi-stage build for React + FastAPI
FROM node:18-slim as frontend-builder

# Build React frontend
WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
COPY public/ ./public/
COPY src/ ./src/
RUN npm run build

# Python backend with CloudHSM client
FROM python:3.11-slim

# Install system dependencies and CloudHSM client
RUN apt-get update && apt-get install -y \
    wget \
    sudo \
    build-essential \
    swig \
    libssl-dev \
    && wget -O cloudhsm-client.deb https://s3.amazonaws.com/cloudhsmv2-software/CloudHsmClient/Jammy/cloudhsm-pkcs11_latest_u22.04_amd64.deb \
    && dpkg -i cloudhsm-client.deb || apt-get install -f -y \
    && rm cloudhsm-client.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create required directories
RUN mkdir -p /opt/cloudhsm/etc /app

# Disable key availability check for single HSM clusters
RUN /opt/cloudhsm/bin/configure-pkcs11 --disable-key-availability-check


# Copy backend code
WORKDIR /app
COPY pkcs11_api/ ./pkcs11_api/

# Copy built frontend
COPY --from=frontend-builder /app/frontend/build ./build

# Install Python dependencies (excluding PyKCS11)
RUN pip install --no-cache-dir fastapi==0.104.1 uvicorn[standard]==0.24.0 pydantic==2.5.0 python-multipart==0.0.6 sqlalchemy==2.0.23 fastapi-cors==0.0.6

# Install compatible SWIG version and then PyKCS11
RUN pip install --no-cache-dir swig==4.1.1.post1
RUN pip install --no-cache-dir pykcs11==1.5.12

# Create non-root user with sudo privileges
RUN useradd -m -s /bin/bash appuser && \
    echo "appuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 8000

# Start the application
WORKDIR /app/pkcs11_api
CMD ["python", "main.py"]