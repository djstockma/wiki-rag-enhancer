FROM python:3.11-slim

# Install system dependencies (MariaDB Connector/C + build tools)
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    gcc \
    g++ \
    make \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

RUN pip install --upgrade pip

# Install wheel (for wikipedia)
RUN pip install --no-cache-dir wheel

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

CMD ["python", "main.py"]
