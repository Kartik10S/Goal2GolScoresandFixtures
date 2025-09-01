# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Start the app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
