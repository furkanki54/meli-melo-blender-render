FROM ubuntu:22.04

# Blender + headless çalışması için gereken paketler
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    blender \
    python3 python3-pip \
    ffmpeg \
    xvfb x11-xserver-utils \
    libgl1 libgl1-mesa-glx libxi6 libxrender1 libxxf86vm1 libxfixes3 libxkbcommon0 libx11-6 \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]
