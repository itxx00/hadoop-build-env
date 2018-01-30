#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
from scripts.command import Command
import copy
import os


class Custom(Basis):

    def __parse(self, param):
        cluster_binary_dir = self.getClusterBinaryDir()

        if 'hdfs' == param:
            return os.path.join(
                cluster_binary_dir, 'sbin/stop-dfs.sh')

        if 'yarn' == param:
            return os.path.join(
                cluster_binary_dir, 'sbin/stop-yarn.sh')

        if 'jobhistory' == param:
            return os.path.join(
                cluster_binary_dir, 'bin/mapred --daemon stop historyserver')

        if 'timelineserver' == param:
            return os.path.join(
                cluster_binary_dir, 'bin/yarn --daemon stop timelineserver')

        # TODO, add more
        return

    def action(self):
        logger.info('--> common.stop <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=600'

        host_list = self.getHosts()
        rm_list = self.getHosts(roles=['resourcem', ])

        # -- step1
        params = copy.deepcopy(self.ys['params'])
        if params is None:
            params = []

        if len(params) == 0:
            params.append('hdfs')
            params.append('yarn')
            params.append('jobhistory')
            params.append('timelineserver')

        # -- step2
        EACH_HOST_INS = [] # such as 'nodemanager' and datanode

        instructions = list()

        for p in params:
            tlist = None
            if p in EACH_HOST_INS:
                tlist = host_list
            else:
                tlist = rm_list

            for host in tlist:
                if self.__parse(p) is None:
                    continue

                #!!! donot use -tt option
                ins = "ssh {0} {2}@{1} -T '{3}' ".format(
                    ssh_option, host['ip'], host['usr'],
                    self.__parse(p))
                instructions.append(ins)

        return Command.parallel(instructions)

def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    # return e.status
    return True
