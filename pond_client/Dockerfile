#NOTE: To build:
# docker build -t rpi .
# To run:
# ./startContainer.sh
#


FROM ubuntu:bionic

RUN apt-get update --fix-missing && \
    apt-get install --no-install-recommends git python3 python3-pip scons && \
    swig build-essential python3-dev python3-setuptools && \
    python3-wheel -y && \ 
    rm -rf /var/lib/apt/lists/*



#RUN pip3 install websockets rpi.gpio && \
#git clone https://github.com/jgarff/rpi_ws281x.git && \
#cd rpi_ws281x && \
#scons

#RUN cd rpi_ws281x/python && \ 
#python3 setup.py install

RUN pip3 install websockets rpi.gpio

RUN apt-get remove scons swig python git python3-pip build-essential && \
    python3-dev python3-setuptools -y && \ 
    rm -rf /var/lib/apt/lists && \
    apt-get autoremove -y 

COPY ["*.py", "/usr/src/"]

ENV CENTRAL_SERVER_IP=0.0.0.0 WEB_SOCKET_PORT=8765

CMD ["python3", "/usr/src/mainclient.py"]
