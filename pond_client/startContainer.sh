#This script will create a docker container. Note, you will have to build the image first.
# The run command runs a privileged docker container, which is needed to expose the GPIO pins to the container.
# It sets the hostname of the container as the hostname of the device. Make hostnames 
#for both RPI clients to be:
# "pondPiEast" and "pondPiWest".

echo "Starting container script...\n"

echo "What is the ip address of the central server you are connecting to?"

read CENTRAL_SERVER_IP  

echo "Enter the number to select your choice: "
echo " 1. Set this pi up as pondPiEast. "
echo " 2. Set this pi up as pondPiWest. "
read HOSTNAME

if [ $HOSTNAME -eq 1 ]
then HOSTNAME=pondPiEast
fi

if [ $HOSTNAME -eq 2 ]
then HOSTNAME=pondPiWest
fi

echo "Setting as $HOSTNAME"

docker run -h $HOSTNAME -e "CENTRAL_SERVER_IP=$CENTRAL_SERVER_IP" -v $(pwd):/usr/src --name pondPi --restart unless-stopped -d  --device /dev/ttyAMA0:/dev/ttyAMA0 --device /dev/mem:/dev/mem --device /dev/gpiomem:/dev/gpiomem --privileged cphamlet/duxnet-client
