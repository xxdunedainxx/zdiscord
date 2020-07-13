#!/bin/bash

source /home/zdiscord/.bash_profile

cd "${APP_ROOT_DIR}"

source "${APP_ROOT_DIR}/env/bin/activate"

which python

nohup redis-server >/dev/null 2>&1 &

python "${APP_ROOT_DIR}/app.py"

#nohup python3 "${APP_ROOT_DIR}/app.py" >/dev/null 2>&1 &   # doesn't create nohup.out