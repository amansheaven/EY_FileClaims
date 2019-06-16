FROM ubuntu:18.04
MAINTAINER Aman Singh "amanggnlps@gmail.com"
CMD apt-get install tesseract-ocr
CMD tesseract -v
CMD apt-get install -y python3-pip python3-dev
CMD pip3 --version
CMD apt-get install git
CMD git clone "https://github.com/amansheaven/EY_FileClaims"
WORKDIR /EY_FileClaims
CMD pip install -r requirements.txt
COPY ./weights.npz /app/static/models/
CMD export FLASK_APP='main'
CMD export FLAKS_ENV='development'
