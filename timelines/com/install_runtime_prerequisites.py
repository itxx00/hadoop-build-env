#!/usr/bin/env python3

from timelines.basis import BasisEvent
from timelines.basis import Commands as cmd
from timelines.basis import logger

#---------------------------------------------------------------------------
#   Definitions
#---------------------------------------------------------------------------

#
# _runtime_codepath indicates the code location as runtime
#
_runtime_codepath = '/opt/rose/'

class CustomEvent(BasisEvent):

    # override
    def action(self):
        logger.info('--> timelines.com.install_runtime_prerequisites <--')

        #
        # Remote Commands
        #
        # .create runtime codepath
        part = dict(filter(lambda x: x[0] != 'ag', self.ys['roles'].items()))
        nlist = list()
        for k, v in part.items():
            nlist += [v['usr'] + '@' + n for n in v['hosts']]
        str = ','.join(set(nlist))

        _shell = "pdsh -R ssh -w %s 'mkdir -p /opt/rose/tmp/'" % (nodes_list)
        retcode = cmd.do(_shell)
        if retcode != 0:
            return False


        debian_shell = './utilities/t.install_runtime_prerequisites.sh'
        
        
        # retcode = cmd.do(debian_shell)
        # if retcode != 0:
        #     return False

        # debian_shell = 'sudo -S ./utilities/t.install_compile_prerequistes.sh'
        # retcode = cmd.sudo(debian_shell, self.ys['roles']['ag']['pwd'])
        # if retcode != 0:
        #     return False

        return True


def trigger(ys):
    e = CustomEvent(ys, attempts=5, interval=10, auto=True)
    return e.status