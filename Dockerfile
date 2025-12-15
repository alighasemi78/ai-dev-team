FROM python:3.11

WORKDIR /app

# Prevent Python buffering (makes logs appear instantly)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system basics
RUN apt-get update && apt-get install -y git build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create output directory
RUN mkdir -p output

CMD ["python", "main.py"]