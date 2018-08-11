#NOTE: To build:
# docker build -t rpi .
# To run:
# ./startContainer.sh
#


FROM ubuntu:bionic

RUN apt-get update --fix-missing && \
    apt-get install --no-install-recommends scons swig build-essential git python3 python3-dev \
    python3-setuptools python3-wheel python3-pip -y && \
    pip3 install websockets rpi.gpio && \
    git clone https://github.com/jgarff/rpi_ws281x.git && \
    cd rpi_ws281x && \
    scons && \ 
    cd python && \ 
    python3 setup.py install && \
    apt-get remove scons swig git python3-pip \
    python3-dev python3-setuptools python3-wheel build-essential python -y && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

VOLUME /usr/src/

ENV CENTRAL_SERVER_IP=0.0.0.0 WEB_SOCKET_PORT=8765

CMD ["python3", "/usr/src/mainclient.py"]
