# Use Python slim base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc curl unzip && \
    rm -rf /var/lib/apt/lists/*

#  Install ngrok v3 (not v2)
RUN curl -L https://bin.ngrok.com/linux/ngrok-stable-linux-amd64.tgz -o ngrok.tgz && \
    tar -xvzf ngrok.tgz && \
    mv ngrok /usr/local/bin && \
    rm ngrok.tgz

# Copy and install Python dependencies
COPY requirements.txt ./
COPY nltk_data ./nltk_data
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app and model files
COPY app.py ./
COPY model.pkl ./
COPY tfidfvect.pkl ./

# Expose the Streamlit default port
EXPOSE 8501

# Run Streamlit and ngrok in parallel
CMD sh -c "\
  streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & \
  sleep 5 && \
  ngrok http --authtoken 2xrv3USJiIwB4XjqbIDWYhtxYT8_2XFcUXgWoYejthqwfN1th 8501 --log=stdout"
