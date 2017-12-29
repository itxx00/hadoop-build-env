#!/usr/bin/env python3

from scripts.basis import Basis
from scripts.basis import logger
import os


class Custom(Basis):

    def __parse(self, param):
        if 'hdfs' == param:
            return 'sbin/start-dfs.sh'

        if 'yarn' == param:
            return 'sbin/start-yarn.sh'

        # TODO, add more
        return

    # override
    def action(self):
        logger.info('--> common.start <--')

        ssh_option = '-o StrictHostKeyChecking=no -o ConnectTimeout=600'

        rm_list = self.getHosts(roles=['resourcem', ])

        cluster_binary_dir = self.getClusterBinaryDir()

        candidates = list()
        for p in self.ys['params']:
            candidates.append(os.path.join(
                cluster_binary_dir, self.__parse(p)))

        if len(candidates) == 0:
            candidates.append(os.path.join(
                cluster_binary_dir, 'sbin/start-all.sh'))

        instructions = list()
        for host in rm_list:
            #!!! donot use -tt option
            ins = "ssh {0} {2}@{1} -T '{3}' ".format(
                ssh_option, host['ip'], host['usr'],
                ' && '.join(candidates))

            instructions.append(ins)

        return Command.parallel(instructions)


def trigger(ys):
    e = Custom(ys, attempts=3, interval=3, auto=True)
    return e.status
