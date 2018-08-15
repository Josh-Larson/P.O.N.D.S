#This file generates the certificate and private key pair for nginx to encrypt communications

openssl req -x509 -newkey rsa:2048 -keyout ./config/nginx-selfsigned.pass.key -out ./config/nginx-selfsigned.crt -days 9999 -subj "/C=US/ST=MS/L=Biloxi/O=cMadDucksLimited/OU=Com/CN=madducks.com" -passout pass:ABCABCDAB

openssl rsa -in ./config/nginx-selfsigned.pass.key -out ./config/nginx-selfsigned.key -passin pass:ABCABCDAB

rm ./config/nginx-selfsigned.pass.key
