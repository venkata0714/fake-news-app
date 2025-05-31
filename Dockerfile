# Use Python slim base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc curl unzip gnupg apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

# Install ngrok v3 via official Debian .deb package
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | gpg --dearmor -o /usr/share/keyrings/ngrok-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/ngrok-archive-keyring.gpg] https://ngrok-agent.s3.amazonaws.com buster main" > /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install -y ngrok

# Copy and install Python dependencies
COPY requirements.txt ./
COPY nltk_data ./nltk_data
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and model files
COPY app.py ./
COPY model.pkl ./
COPY tfidfvect.pkl ./

# Expose the Streamlit port
EXPOSE 8501

# Start Streamlit and ngrok
CMD ["sh", "-c", "streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & sleep 5 && ngrok http --authtoken 2xrv3USJiIwB4XjqbIDWYhtxYT8_2XFcUXgWoYejthqwfN1th 8501 --log=stdout"]
