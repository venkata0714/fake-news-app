# Use Python slim base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc curl npm && \
    rm -rf /var/lib/apt/lists/*

# Install localtunnel globally
RUN npm install -g localtunnel

# Copy and install Python dependencies
COPY requirements.txt ./
COPY nltk_data ./nltk_data
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py ./
COPY model.pkl ./
COPY tfidfvect.pkl ./

# Expose Streamlit default port
EXPOSE 8501

# Start Streamlit and LocalTunnel together
CMD sh -c "\
  streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & \
  sleep 5 && \
  lt --port 8501"
