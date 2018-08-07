FROM ubuntu:bionic

RUN apt update && \
apt-get install git python3 python3-pip scons swig -y

RUN pip3 install websockets && \
git clone https://github.com/jgarff/rpi_ws281x.git && \
cd rpi_ws281x &&\
scons

COPY app.py /usr/src/

CMD ["python3", "app.py"]
