FROM python:3.10-slim
WORKDIR /app

# Install system deps for Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libjpeg-dev zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

COPY Phase_5/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "Phase_5.scripts.app:app"]
