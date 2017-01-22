#!/bin/bash

echo "Killing old processes.."
ps aux | grep python | awk '{print $2}' | xargs kill
sleep 2
echo "Starting server.."
source /home/pi/dev/homeauto/env/bin/activate
cd /home/pi/dev/homeauto/web/
nohup /home/pi/dev/homeauto/web/start.sh &
echo "Done"
