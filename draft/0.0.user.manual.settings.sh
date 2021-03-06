#!/bin/bash
#
source ~/.profile
source 0.1.common.function.sh

# -----------------------------
# >> User vars <<
# -----------------------------

# Env vars
JAVA_HOME='/usr/lib/jvm/java-8-oracle'


# Version
#
# * HADOOP_VERSION='2.8.0'
# * HADOOP_VERSION='3.0.0-alpha1'
HADOOP_VERSION='3.0.0-alpha2'
#


# Hadoop Code Home
HADOOP_CODE_LOCATION=`cd ~;pwd`     # default
HADOOP_CODE_PATH=${HADOOP_CODE_LOCATION}'/hadoop-'${HADOOP_VERSION}
HADOOP_SRC_CODE_PATH=${HADOOP_CODE_LOCATION}'/hadoop-'${HADOOP_VERSION}'-src'

mkdir -p ${HADOOP_CODE_PATH}
mkdir -p ${HADOOP_SRC_CODE_PATH}


# Hadoop Cluster Mode
#
# * HADOOP_CLUSTER_MODE='LOCAL_MODE' # not support now
HADOOP_CLUSTER_MODE='PSEUDO_DIS_MODE'
# * HADOOP_CLUSTER_MODE='FULLY_DIS_MODE'
#
#
if [[ 'FULLY_DIS_MODE' == ${HADOOP_CLUSTER_MODE} ]]; then

    declare -A HADOOP_FDM_NODES

    HADOOP_FDM_NODES+=([num]=3);
    nlist=(
        'root@192.168.4.201'
        'root@192.168.4.202'
        'root@192.168.4.203'
    );
    HADOOP_FDM_NODES+=([list]=nlist);
    HADOOP_FDM_NODES+=([pw]='123456');
    HADOOP_FDM_NODES+=([rm]='192.168.4.201');
    HADOOP_FDM_NODES+=([dn]='192.168.4.201');
    HADOOP_FDM_NODES+=([sdn]='192.168.4.201');

fi


# -----------------------------
# >> Hadoop original env vars <<
# -----------------------------

# Hadoop Opportunistic container enable/disable
HADOOP_OPPORTUNISTIC_CONTAINER_ENABLE=true

# Hadoop Distributed scheduling enable/disbale
HADOOP_DISTRIBUTED_SCHEDULING_ENABLE=false

# Secure and insecure env vars
# * [start|stop]-dfs.sh
HDFS_DATANODE_USER=root
HADOOP_SECURE_DN_USER=hdfs
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
#
# * [start|stop]-yarn.sh
YARN_NODEMANAGER_USER=root
YARN_RESOURCEMANAGER_USER=root

