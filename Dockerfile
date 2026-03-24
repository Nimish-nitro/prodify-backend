FROM python:3.13-slim

HEAD
# Install system dependencies
RUN apt-get update && apt-get install -y \
    libxcb1 \
    libxcb-cursor1 \
    libxcb-compositor0 \
    libxcb-image0 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shippable-pool0 \
    libxcb-shm0 \
    libxcb-sync1 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libxcb-xkb1 \
    libxcb-icccm1 \
    libxcb-xinerama0 \
    libxcb-xinput0 \
    libxcb-xinerama0 \
    libxcb-xinput2 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxau6 \
    libxcb-dri3-0 \
    libxcb-dri2 \
    libxcb-shape0 \
    libxcb-render0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-xfixes0 \
    libxcb-xkb1 \
    libxcb-xinerama0 \
    libxcb-xinput0 \
    libxcb-xinerama0 \
    libxcb-xinput2 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port and run the app
EXPOSE 8000
CMD ["python", "app.py"]

  FROM python:3.13-slim

  WORKDIR /app

  RUN apt-get update && apt-get install -y \
      libgl1 \
      libxkbcommon0 \
      libxkbcommon-x11-0 \
      libglib2.0-0 \
      libsm6 \
      libxext6 \
      libxrender1 \
      libgomp1 \
      && rm -rf /var/lib/apt/lists/*

  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  COPY . .

  EXPOSE 8000
  CMD ["python", "app.py"]

