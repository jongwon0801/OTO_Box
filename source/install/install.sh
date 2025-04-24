# /home/pi/install.sh

#!/bin/bash
if [ "$#" -lt 2 ]; then
    echo "$# is Illegal number of parameters."
    echo "Usage: $0 10000 lte"
    exit 1
fi
id=$1
if [ $2 == "lte" ]; then
  sudo sed -i '5,9s/#//g' /etc/iptables-hs
else
  sudo sed -i '5,9s/^/#/' /etc/iptables-hs 
fi

let z=$id+30000
sudo sed -i "s/.*/O2OBOX-${id}/" /etc/hostname
sudo sed -i "s/^127\.0\.0\.1.*O2OBOX.*/127.0.0.1 O2OBOX-${id}/" /etc/hosts
sudo sed -i "s/^RemoteForward.*localhost:8000$/RemoteForward  ${id} localhost:8000/" /root/.ssh/config
sed -i "s/^RemoteForward.*localhost:22$/RemoteForward  ${z} localhost:22/" .ssh/config
sudo sed -i "/^ssid=/ s/=.*/=오투오박스-${id}/" /etc/hostapd/hostapd.conf 
cd /home/pi/Workspace/newapp/applelocker
/home/pi/.virtualenvs/o2obox/bin/python imp1.py "$id"
/home/pi/.virtualenvs/o2obox/bin/python syncdb_service.py







