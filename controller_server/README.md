# Pond Controller

In this folder is the "Pond Controller" i.e. the code for the Raspberry Pi in the central hallway. 
All code for the central Pi controller will be in this folder.

The central server has the following requirements:

1. Serve as a webserver (Python Flask)
    * Serves pond status information from both ponds
    * Serves an authentication portal which will allow administrators to turn pumps on and off
    * Change LEDS in pond (API provided by @AzureUmbra)
    * Provided other status information? (To be continued)
2. Serve as a RPC server
    * Clients (Pond Pis) connect to the controller to serve status information


## Environment Setup 

``` 
pip install -r requirements.txt
```
