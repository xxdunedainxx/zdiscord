#!/bin/bash
whoami
source /home/zdiscord/.bash_profile

source "${APP_ROOT_DIR}/env/bin/activate"

echo $(which python)

python3 -m pip install -U pip

python3 -m pip install "${APP_ROOT_DIR}" "${APP_ROOT_DIR}/"