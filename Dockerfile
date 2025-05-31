# Use Python slim base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and NLTK data
COPY requirements.txt .
COPY nltk_data ./nltk_data

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model files
COPY app.py .
COPY model.pkl .
COPY tfidfvect.pkl .

# Expose Streamlit port
EXPOSE 80
CMD ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]
