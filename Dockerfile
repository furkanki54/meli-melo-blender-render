FROM ubuntu:22.04

# Sistem paketleri (Blender + headless çalışması için)
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    blender \
    python3 python3-pip \
    ffmpeg \
    xvfb x11-xserver-utils \
    libgl1 libgl1-mesa-glx libxi6 libxrender1 libxxf86vm1 libxfixes3 libxkbcommon0 libx11-6 \
    && apt-get clean

# Python paketleri (sabit kurulum; cache sorunlarını bypass)
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir Flask==3.0.0 moviepy==1.0.3 imageio==2.31.1 imageio-ffmpeg==0.4.9 numpy Pillow==10.3.0

WORKDIR /app
COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["python3", "app.py"]
