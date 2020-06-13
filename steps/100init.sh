#!/bin/bash
source /home/zdiscord/.bash_profile
if [ -z ${APP_ROOT_DIR+x} ];then
echo "app root dir not set"
echo "export APP_ROOT_DIR=/home/zdiscord/app" >> /home/zdiscord/.bash_profile
cat /home/zdiscord/.bash_profile
fi
echo $APP_ROOT_DIR
