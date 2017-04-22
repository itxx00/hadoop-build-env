#!/bin/bash
#
source 0.*

# ----------------------------
# Edit the files <hadoop code path>/[etc, bin, share...]
#   to define some parameters as follows:
#
# >> etc/hadoop/hadoop-env.sh
FILE=${HADOOP_CODE_PATH}'/etc/hadoop/hadoop-env.sh'
#
# * set to the root of your Java installation
grep 'export JAVA_HOME=' ${FILE} > /dev/null
if [[ 0 == $? ]]; then
    sed -i 's#.*export JAVA_HOME=.*#export JAVA_HOME=/usr/lib/jvm/java-8-oracle#g' ${FILE}
else
    echo 'export JAVA_HOME=/usr/lib/jvm/java-8-oracle' >> ${FILE}
fi

# ----------------------------
# Setup passphraseless ssh
#   ssh localhost without a passphrase
#   -- ssh localhost # check
if [[ ! -f ~/.ssh/id_rsa.pub ]]; then
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
fi
grep "`cat ~/.ssh/id_rsa.pub`" ~/.ssh/authorized_keys > /dev/null
if [[ 0 != $? ]]; then
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
fi
chmod 700 ~/.ssh
chmod 644 ~/.ssh/authorized_keys

# ----------------------------
# Fix issues:
# ----------------------------
#   pdsh set rsh to connect default,
#       reset ssh and reconnect terminal
#   -- echo 'export PDSH_RCMD_TYPE=ssh' >>  ~/.profile # add
#   -- pdsh -w localhost -l root uptime # test
FILE=~/.profile
grep 'export PDSH_RCMD_TYPE=' ${FILE} > /dev/null
if [[ 0 == $? ]]; then
    sed -i 's#.*export PDSH_RCMD_TYPE=.*#export PDSH_RCMD_TYPE=ssh#g' ${FILE}
else
    echo 'export PDSH_RCMD_TYPE=ssh' >> ${FILE}
fi
