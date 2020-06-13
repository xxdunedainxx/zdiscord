 #!/bin/bash

echo "executing setup!"

apt-get update --assume-yes
apt-get upgrade --assume-yes
apt-get install openssl libssl1.0.0 --assume-yes
apt-get install python3 --assume-yes
apt-get install python3-venv --assume-yes
apt-get install python3-pip --assume-yes
openssl rand -base64 12 > pw.txt 
useradd -m -p $(<./pw.txt) zdiscord

mkdir -p /home/zdiscord/app

ls
pwd

cp -r ./ /home/zdiscord/app

cd /home/zdiscord/app

home=$(pwd)

chmod -R 755 $home

echo $home

if [ ! -e /home/zdiscord/.bash_profile ]; then 
echo "need to create bash_profile"
touch /home/zdiscord/.bash_profile
else
echo "profile exists?"
cat /home/zdiscord/.bash_profile
whoami
fi

chown -R zdiscord /home/zdiscord/.bash_profile

source /home/zdiscord/.bash_profile
rm -rf "${APP_ROOT_DIR}/env"
python3 -m venv env "${APP_ROOT_DIR}/env"
chown -R zdiscord "${APP_ROOT_DIR}/env"

for script in steps/*;
  do
    echo "RUNNING $script"

    # windows carriage return issue 
    sed -i 's/\r//g' ./$script

    # allow execute
    chmod 777 ./$script

    ./$script
    echo "FINISH RUNNING $script"

    # always reset to home dir
    cd $home
done