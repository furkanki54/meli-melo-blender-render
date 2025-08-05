FROM ubuntu:22.04

# Blender için gerekli bağımlılıklar
RUN apt update && apt install -y \
    blender \
    python3 \
    python3-pip \
    ffmpeg \
    && apt clean

# Çalışma dizini
WORKDIR /app

# Python bağımlılıkları
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Tüm proje dosyalarını kopyala
COPY . .

# Başlangıç komutu
CMD ["python3", "main.py"]
