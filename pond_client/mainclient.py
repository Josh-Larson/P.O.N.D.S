#!/usr/bin/env python
"""
  Author: Connor Hamlet
  Description: This code is the websocket client for the pondPis.
  When this launches, it will connect to the central websocket server, and 
  it will 'authenticate' using a weak form of authentication. It will 
  encrypt the connection with the self-signed certificate on the server,
  but it will not attempt to verify the validity of the certificate. 

  This file is responsible for updatiing the central server the pump's status,
  along with any other configuration information if applicable.

  Currently, if the pondPi is powered off abruptly, the pond status will not change. 
  TODO: In the central server code, catch websocket close exceptions. 
  If a websocket closes which is a pond Pi, make sure to mark that client as offline
"""


# WS client example

import asyncio, websockets, json, socket, os, ssl

# Websocket object of the central server
CENTRAL_SERVER = None
#The access token for a websocket session. Is sent with every message
TOKEN = ""
USER_NAME = socket.gethostname() #Make sure the hostname on the host device is "pondPiEast" and "pondPiWest" for each respective pond. 

async def handler():

    # ssl._create_unverified_context() will allow this client to use tls
    # without trusting the cert. This should never be used in practice, 
    # But for this exercise it opens a mitm vulnerability
    async with websockets.connect(
            'wss://'+os.environ['CENTRAL_SERVER_IP']+'/socket', ssl=ssl._create_unverified_context()) as websocket:
        CENTRAL_SERVER = websocket

        val = json.dumps({'cmd':'pi_login', 'user':USER_NAME, 'pass':'secret'})

        print(val)
        #Sends login credentials to central server. 
        await CENTRAL_SERVER.send(val)

        #Waits for login confirmation. 
        login_confirm = await CENTRAL_SERVER.recv()

        #Decodes the JSON
        login_confirm = json.loads(login_confirm)
        TOKEN = login_confirm['token']
        print(login_confirm)

        #After logging in, send a message to the server which states the flow_value, or whether or not the pond is flowing. 
        await CENTRAL_SERVER.send(json.dumps({'cmd':'update_clients', 'user':USER_NAME, 'flow_value':'true', 'token':TOKEN}))
        
        
        #While true, listen for messages.
        while True:
            msg = await CENTRAL_SERVER.recv()
            msg = json.loads(msg)
            print(msg)

            #If the command is a set_flow command, set the flow and send the update_clients function back.
            #Update clients will tell the central server to message all connected webclients the pond status

            if msg['msgtype'] == "cmd" and msg['cmd'] == "set_flow":
                flow_value = msg['flow_value']
                #API.setPumpStatus(API CALL HERE TO SET THE PUMP)
                await CENTRAL_SERVER.send(json.dumps({'cmd':'update_clients', 'user':USER_NAME, 'token':TOKEN, 'flow_value':flow_value}))
        CENTRAL_SERVER.close()


#Run forever
asyncio.get_event_loop().run_until_complete(handler())
