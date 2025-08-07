FROM python:3.10-slim

# Gerekli sistem bağımlılıkları (FFmpeg için)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını yükle
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Çalıştırılacak dosya
CMD ["python3", "app.py"]
