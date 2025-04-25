# === Dockerfile ===
FROM python:3.11-slim

# playwright 실행을 위한 기본 패키지 설치
RUN apt-get update && \
    apt-get install -y wget curl gnupg build-essential \
    libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 \
    libasound2 libxtst6 libxrandr2 libatk1.0-0 libgtk-3-0 libx11-xcb1 && \
    apt-get clean

WORKDIR /code

# 종속성 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 전체 코드 복사
COPY . .

# Playwright 설치 및 브라우저 설치
RUN pip install playwright && playwright install --with-deps