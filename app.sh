#!/bin/bash

source /home/zdiscord/.bash_profile

source "${APP_ROOT_DIR}/env/bin/activate"

which python

python "${APP_ROOT_DIR}/app.py"

#nohup python3 "${APP_ROOT_DIR}/app.py" >/dev/null 2>&1 &   # doesn't create nohup.out