FROM blender:3.6.0

WORKDIR /app
COPY . .

CMD ["blender", "-b", "-P", "main.py"]
