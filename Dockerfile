# Use a smaller base image
FROM python:3.10-alpine

# Install system dependencies for numpy, scikit-learn, psycopg2
RUN apk add --no-cache gcc musl-dev libffi-dev python3-dev postgresql-dev build-base

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser -D appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"] 