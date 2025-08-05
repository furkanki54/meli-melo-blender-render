FROM ubuntu:22.04

# Sistem güncelle ve Blender bağımlılıklarını kur
RUN apt update && \
    apt install -y wget ca-certificates libgl1 libxi6 libxrender1 libxrandr2 libxcursor1 libxinerama1 libglu1-mesa libsm6 libxext6 libxfixes3 libx11-6 && \
    apt install -y ffmpeg

# Blender'ı indir ve kur
RUN wget https://ftp.nluug.nl/pub/graphics/blender/release/Blender3.6/blender-3.6.0-linux-x64.tar.xz && \
    tar -xf blender-3.6.0-linux-x64.tar.xz && \
    mv blender-3.6.0-linux-x64 /blender

WORKDIR /app
COPY . .

# Blender ile çalıştır
CMD ["/blender/blender", "-b", "-P", "main.py"]
