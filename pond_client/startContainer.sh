#This script will create a docker container. Note, you will have to build the image first.
# The run command runs a privileged docker container, which is needed to expose the GPIO pins to the container.
# It sets the hostname of the container as the hostname of the device. Make hostnames 
#for both RPI clients to be:
# "pondPiEast" and "pondPiWest".

HOSTNAME=$(hostname)
docker run -h $HOSTNAME --name pondPi -d  --device /dev/ttyAMA0:/dev/ttyAMA0 --device /dev/mem:/dev/mem --device /dev/gpiomem:/dev/gpiomem --privileged rpi
