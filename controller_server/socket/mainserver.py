#!/usr/bin/env python

# WS server example

import asyncio, uuid, json
import websockets

pi_clients= {}
web_clients = {}
POND_STATUS = {'pondPiEast': "pending", 'pondPiWest':"pending"}


#This funciton takes a password as input, and outputs a session token.
#Used to authenticate the web_clients
async def client_login(msg, websocket):
    if  msg['pass'] == "secret":
        token = str(uuid.uuid1())
        web_clients[token] = websocket
        await websocket.send(json.dumps({'msgtype': 'notify', 'login': 'true', 'token': token, 'POND_STATUS':POND_STATUS}))
        #Push flow status to client right after client-login.
        #Remove from client map after x seconds?

#This function takes a username and pword as input, outputs a session token. 
#Used to authenticate the pi's 
async def pi_login(msg, websocket):
    user, password = msg['user'], msg['pass']

    if  password=="secret":
        token = str(uuid.uuid1())
        pi_clients[user] = (websocket,token)
        await websocket.send(json.dumps({'msgtype': 'notify', 'login': 'true', 'token':token }))

#This function, initiated by a web client, sets the flow status of a particular pump
async def set_flow(msg, websocket):
    target, flow_value, token = msg['target'], msg['flow_value'], msg['token']
    if target in pi_clients and token in web_clients:
        #Below cmd vulnerable to replay
        await pi_clients[target][0].send(json.dumps({'msgtype':'set_flow', 'flow_value':flow_value}))
    else:
        await websocket.send(json.dumps({'msgtype': 'error', 'msg': 'Login failed. Incorrect token.'}))

#This function, when authenticated, pushes the stauts of all fountains to all connected web clients
async def update_clients(msg, websocket):

    user, token = msg['user'], msg['token']
    POND_STATUS[user] = msg['flow_value']
    print("UPDATING CLIENTS")
    if user in pi_clients and pi_clients[user][1] == token:
        #If web clients are connected.
        if web_clients:
            #Below cmd vulnerable to replay
            await asyncio.wait([web_clients[k].send(json.dumps({'msgtype':'update','POND_STATUS':POND_STATUS})) for k in web_clients])
            
        print("EXITING UPDATE")
    else:
        await websocket.send(json.dumps({'msgtype': 'error', 'msg': 'Login failed.'}))

#A dictionary of available functions 
switcher = {
    'client_login':client_login,
    'pi_login':pi_login,
    'set_flow':set_flow,
    'update_clients':update_clients
}

#This handler waits for a message from anybody, regardless whether it is a msg from a web client or the raspberry Pi. 
async def handler(websocket, path):
    while True:
        msg = await websocket.recv()    
        msg = json.loads(msg)
        print(msg)
        await switcher[msg['cmd']](msg, websocket)


start_server = websockets.serve(handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()