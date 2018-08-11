pip3 install -r /usr/src/app/requirements.txt

#Starts flask and websocket servers
python3 /usr/src/app/flaskApp.py &
python3 /usr/src/app/socketServer.py 
