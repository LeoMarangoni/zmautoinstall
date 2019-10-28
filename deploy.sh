#!/bin/bash

mkdir files
python run.py

SSHKEY=$(echo files/zimbrainstall.$RANDOM)
ssh-keygen -N "" -f $SSHKEY
PUBK=$(cat $SSHKEY.pub)
DOMAIN=$(egrep "^domain" config.py | sed "s/[ '\"]//g" | cut -d "=" -f2)

# Authorize installer to don't ask SSH password
while read LINE
do
    IP=$(echo $LINE | awk '{print $1}')
    ssh root@$IP 'bash -s' << EOF
    echo $PUBK >> .ssh/authorized_keys
EOF
done < <(cat files/etchosts.tmp| egrep -v "127.0.0.1|localhost")

# Configure and install zimbra
while read LINE
do
    IP=$(echo $LINE | awk '{print $1}')
    HOST=$(echo $LINE | awk '{print $3}')    
    scp -i $SSHKEY files/etchosts.tmp root@$IP:/etc/hosts
    scp -i $SSHKEY  files/autoinstall_$HOST root@$IP:/tmp/autoinstall
    ssh -i $SSHKEY  root@$IP 'wget https://files.zimbra.com/downloads/8.8.15_GA/zcs-8.8.15_GA_3869.UBUNTU16_64.20190918004220.tgz'
    ssh -i $SSHKEY  root@$IP 'tar -xvf zcs-8.8.15_GA_3869.UBUNTU16_64.20190918004220.tgz'
    ssh -i $SSHKEY  root@$IP 'cd zcs-8.8.15_GA_3869.UBUNTU16_64.20190918004220 && ./install.sh /tmp/autoinstall'
done < <(cat files/etchosts.tmp| egrep -v "127.0.0.1|localhost")




# Remove authorization
while read LINE
do
    IP=$(echo $LINE | awk '{print $1}')
    ssh -i $SSHKEY root@$IP 'bash -s' << EOF
    grep -v "$PUBK" .ssh/authorized_keys > temp && mv temp .ssh/authorized_keys
EOF
done < <(cat files/etchosts.tmp| egrep -v "127.0.0.1|localhost")
rm -rf files/