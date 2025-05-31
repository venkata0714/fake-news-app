# Use Python slim base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Install ngrok
RUN curl -s https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -o ngrok.zip && \
    unzip ngrok.zip && mv ngrok /usr/local/bin/ngrok && rm ngrok.zip

# Copy and install Python dependencies
COPY requirements.txt ./
COPY nltk_data ./nltk_data
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py ./
COPY model.pkl ./
COPY tfidfvect.pkl ./

# Expose Streamlit port
EXPOSE 8501

# Start both Streamlit and ngrok together
CMD sh -c "\
  streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & \
  sleep 5 && \
  ngrok http 8501 --authtoken=2xrv3USJiIwB4XjqbIDWYhtxYT8_2XFcUXgWoYejthqwfN1th --log=stdout"
