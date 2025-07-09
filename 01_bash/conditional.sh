#!/bin/bash

read -p "Enter hostname to ping: " hostname
if [ "$hostname" == "google.com" ]
then
	ping -c 2 google.com
elif [ "$hostname" == "microsoft.com" ]
then
	ping -c 2 microsoft.com
else
	echo "Only google.com or microsoft.com are allowed."
fi
