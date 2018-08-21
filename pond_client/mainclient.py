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

"""


# WS client example

import asyncio, websockets, json, socket, os, ssl

CENTRAL_SERVER = None
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
        await CENTRAL_SERVER.send(val)

        login_confirm = await CENTRAL_SERVER.recv()
        login_confirm = json.loads(login_confirm)
        TOKEN = login_confirm['token']
        print(login_confirm)
        await CENTRAL_SERVER.send(json.dumps({'cmd':'update_clients', 'user':USER_NAME, 'flow_value':'true', 'token':TOKEN}))
        while True:
            msg = await CENTRAL_SERVER.recv()
            msg = json.loads(msg)
            print(msg)
            if msg['msgtype'] == "cmd" and msg['cmd'] == "set_flow":
                flow_value = msg['flow_value']
                #API.setPumpStatus(API CALL HERE TO SET THE PUMP)
                await CENTRAL_SERVER.send(json.dumps({'cmd':'update_clients', 'user':USER_NAME, 'token':TOKEN, 'flow_value':flow_value}))
        CENTRAL_SERVER.close()

asyncio.get_event_loop().run_until_complete(handler())
