{% if cookiecutter.include_docker == "yes" -%}
FROM python:{{cookiecutter.python_version}}-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE {{cookiecutter.api_port}}

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "{{cookiecutter.api_port}}"]
{% endif -%}