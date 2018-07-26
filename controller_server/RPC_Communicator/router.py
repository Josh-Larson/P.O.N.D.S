from flask import Flask, request, jsonify


import rpc_client

app = Flask(__name__)

ALL_PIS = {'east':["localhost", "8000"]}
rpc_client.connect(ALL_PIS)

@app.route('/getAllPondStatus', methods=['GET'])
def getAllPondStatus():
    status = rpc_client.getAllPondStatus(ALL_PIS)
    return status


@app.route('/setPondStatus', methods=['GET'])
def setPondStatus():
    status = rpc_client.setPondStatus('east', "True" )
    return status

@app.route('/setPondStatusF', methods=['GET'])
def setPondStatusF():
    status = rpc_client.setPondStatus('east', "False" )
    return status