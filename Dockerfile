FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for OpenCV, pytesseract, and Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxkbcommon0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port and run the app
EXPOSE 8000
CMD ["python", "app.py"]

