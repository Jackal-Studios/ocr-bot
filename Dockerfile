FROM ubuntu:latest
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv \
    tesseract-ocr-all
RUN python3 -m pip install -U \
    image \
    Pillow \
    opencv-python \
    pickle5 \
    aiogram 

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    tesseract-ocr
RUN python3 -m pip install -U \
    pytesseract 
WORKDIR /home/OCRBOT/
COPY ./pythonfiles/main.py ./pythonfiles/
#COPY ./db/my_ids.picke ./db/