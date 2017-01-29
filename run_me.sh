#!/bin/bash

export HOME_AUTO_DIR=/home/pi/apps/automation-on-a-stick

# virtualenvwrapper thing
export WORKON_HOME=$HOME/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh


echo "Killing old processes.."
ps aux | grep flask | awk '{print $2}' | xargs kill
sleep 2
echo "Starting server.."
workon homeauto
cd ${HOME_AUTO_DIR}/web/
nohup ${HOME_AUTO_DIR}/web/start.sh &
echo "Done"
