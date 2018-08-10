#apt install python3-flask python3-flask-login python3-websockets python3-gunicorn -y
pip3 install -r /usr/src/app/requirements.txt
#python3 /usr/src/app/mainserver.py
#gunicorn3 -w 3 --bind 0.0.0.0:5000 flaskApp:wsgi
python3 /usr/src/app/socketServer.py &
python3 /usr/src/app/flaskApp.py 
