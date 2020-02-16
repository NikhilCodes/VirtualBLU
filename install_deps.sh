#!/bin/bash
read -r osname</etc/os-release
if [ $osname = "NAME=Fedora" ]
then
	sudo dnf install python3-pyaudio -y
elif [ $osname = "NAME=Ubuntu" ]
then
	sudo apt install python3-pyaudio -y
fi

pip install -r requirements.txt --user
