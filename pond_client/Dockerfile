#NOTE: To build:
# docker build -t rpi .
# To run:
# ./startContainer.sh
#


FROM ubuntu:bionic

RUN apt-get update && \
apt-get install git python3 python3-pip scons swig -y

RUN pip3 install websockets rpi.gpio && \
git clone https://github.com/jgarff/rpi_ws281x.git && \
cd rpi_ws281x &&\
scons

RUN cd rpi_ws281x/python && \ 
python3 setup.py install

#TODO: Change to volumes
COPY ["*.py", "/usr/src/"]


CMD ["python3", "/usr/src/app.py"]
