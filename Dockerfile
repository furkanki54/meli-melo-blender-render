FROM ubuntu:22.04

# Blender ve bağımlılıklarını kur
RUN apt-get update && apt-get install -y \
    blender \
    python3 \
    python3-pip \
    ffmpeg \
    && apt-get clean

# Çalışma dizini
WORKDIR /app

# Gereken Python paketleri
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Varsayılan komut
CMD ["python3", "app.py"]
