FROM python:3.9-slim-buster

RUN apt-get update &&\
    apt-get install -y git 

RUN pip3 install yapf

RUN pip3 install numpy matplotlib scipy scikit-image sklearn

RUN pip3 install cryptography

RUN pip3 install pillow opencv-python

RUN pip3 install BitVector==3.5.0