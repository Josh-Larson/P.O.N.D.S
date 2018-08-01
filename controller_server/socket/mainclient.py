#!/usr/bin/env python

# WS client example

import asyncio, websockets, json

#import socket; socket.gethostname()
CENTRAL_SERVER = None
TOKEN = "my_token"
USER_NAME = "pondPiEast"
async def handler():
    async with websockets.connect(
            'ws://localhost:8765', origin=USER_NAME) as websocket:
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