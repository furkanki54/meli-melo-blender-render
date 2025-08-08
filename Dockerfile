FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# FFmpeg gerekli (moviepy için)
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Önce reqs, sonra install (cache için)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Proje dosyaları
COPY . .

# Debug: kurulan paketleri göster (ilk çalıştırmada logda görürüz)
RUN python -c "import sys, pkgutil; print('PY:',sys.version); import moviepy, imageio; print('moviepy OK', moviepy.__version__)"

CMD ["python","app.py"]
