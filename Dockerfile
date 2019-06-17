FROM ubuntu:18.04
MAINTAINER Aman Singh <amanggnlps@gmail.com>
 
RUN apt-get update && apt-get install -y curl

RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

COPY EY_FileClaims/requirements.txt /

# Python packages from conda
RUN conda install -y --file requirements.txt


RUN conda install -y -c jim-hart pytesseract
RUN conda install -y -c conda-forge python-levenshtein
RUN conda install -y -c conda-forge fuzzywuzzy
RUN conda install -y -c mlgill imutils

RUN conda install -y python==3.6
#RUN conda install -y -c conda-forge opencv
RUN apt-get -y install tesseract-ocr
RUN pip install opencv-python
RUN pip install pytesseract
RUN pip install fuzzywuzzy
RUN pip install flask_cachebuster
RUN conda install -c conda-forge python-levenshtein

RUN apt-get install -y libsm6 libxext6

# Setup application
COPY EY_FileClaims home/EY_FileClaims
ENTRYPOINT ["/miniconda/bin/python", "home/EY_FileClaims/main.py"]
#EXPOSE 5000
ENV PYTHONIOENCODING=utf-8

#pytesseract
#python-Levenshtein
#fuzzywuzzy
#imutils
