# Pond Clients

All of the code of the two Raspberry Pis that actually control fountain pumps will be in this folder. 

The two pond Pis meet the following requirements:

1. Clients (Pond Pis) connect to the central controller to serve status information
    * Sends pump to the controller
2. Both of the pond Pis share the exact same codebase.

## Environment Setup

1. Install Docker

```
curl -sSL https://get.docker.com | sh -
```

2. Build the image, OR pull the image from Docker Hub (recommended. 

To pull the image:

```
docker pull cphamlet/duxnet-client
```

To build the image (Takes approx 20 minutes):
```
docker build -t cphamlet/duxnet-client .
```

3. Run the container. Note: The central server must be running first
```
sh startContainer.sh
```

### Misc:

Delete the container with:

```
docker stop pondPi && docker rm pondPi
```

Delete the image with:
```
docker rmi cphamlet/dexnet-client
```

