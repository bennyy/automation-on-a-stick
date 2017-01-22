#!/bin/bash

export HOME_AUTO_DIR=/home/pi/dev/homeauto

echo "Killing old processes.."
ps aux | grep flask | awk '{print $2}' | xargs kill
sleep 2
echo "Starting server.."
source ${HOME_AUTO_DIR}/env/bin/activate
cd ${HOME_AUTO_DIR}/web/
nohup ${HOME_AUTO_DIR}/web/start.sh &
echo "Done"
