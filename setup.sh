#!/bin/bash

# input for setting .env file

envfilename=".env"

echo "Enter instance name: "
read -r instance

echo "Enter tanent name: "
read -r tanent_name

echo "Enter client-id: "
read -r client_id

echo "Enter client secret: "
read -r client_secret

echo INSTANCE_NAME=\""$instance"\" > $envfilename
echo TANENT=\""$tanent_name"\" >> $envfilename
echo CLIENT_ID=\""$client_id"\" >> $envfilename
echo USER_KEY=\""$client_secret"\" >> $envfilename

# set python env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
