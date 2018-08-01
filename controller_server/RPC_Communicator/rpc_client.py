# Author: Connor Hamlet et. al. 
# Description: This is code for the central Raspberry Pi server. 
# It retrieves information from the pond Pi's.

import xmlrpc.client, uuid, threading


POND_STATUS = {}

#ENV variables
POND_PIS = {}
def connect(pondPiMap):
    
    for remotePiName in pondPiMap:    
        POND_PIS[remotePiName] = xmlrpc.client.ServerProxy('http://'
                + pondPiMap[remotePiName][0]
                + ':'
                + pondPiMap[remotePiName][1])
        getAllPondStatus(pondPiMap)


    # WEST_IP_ADDRESS = 'localhost'
    # WEST_IP_PORT = '8001'
    # POND_PIS['west'] = xmlrpc.remotePiName.ServerProxy('http://'
    #             +WEST_IP_ADDRESS
    #             +':'
    #             +WEST_IP_PORT)
    
#    POND_PIS[remotePiName].system.listMethods()

def getAllPondStatus(pondPiMap):
    # For all remotePiNames, get and cache the status
    for remotePiName in pondPiMap: 
        POND_STATUS[remotePiName] = POND_PIS[remotePiName].getPondStatus()
    return str(POND_STATUS)
 
def setPondStatus(remotePiName, status):
    POND_STATUS[remotePiName] = POND_PIS[remotePiName].setPondStatus(status)
    return str({remotePiName: POND_STATUS[remotePiName]})
