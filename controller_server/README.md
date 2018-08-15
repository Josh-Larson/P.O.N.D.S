# Pond Controller

In this folder is the "Pond Controller" i.e. the code for the Raspberry Pi in the central hallway. 
All code for the central Pi controller will be in this folder.

The central server has the following requirements:

1. Serve as a webserver (Python Flask)
    * Serves pond status information from both ponds
    * Serves an authentication portal which will allow administrators to turn pumps on and off
    * Change LEDS in pond (API provided by @AzureUmbra) (In development)
    * Serve web files
2. Serve as a websocket server
    * Clients (Pond Pis) connect to the controller to serve status information
    * Web clients connect to the websocket server in JavaScript to retrieve status information from the pond Pis.


## Environment Setup 

Launching the controller server is made easy via docker. 

1. Install Docker

```
curl -sSL https://get.docker.com | sh - 
```

2. Install Docker Compose 

```
sudo apt install python-pip
pip install docker-compose -y
```

3. Generate ssl private keys and certificate

```
sh gen_certs.sh
```

4. Launch docker compose to start server
```
docker-compose up -d
```