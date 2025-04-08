FROM python:3.11-slim

# Install system dependencies (MariaDB Connector/C + build tools)
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

CMD ["python", "main.py"]
