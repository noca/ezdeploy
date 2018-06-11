# -*- coding: utf-8 -*-
'''
Deploy
'''
import os
import logging

from ansible.runner import Runner

from ezdeploy.cf import DEPLOY_DIR


class EZCommonDeploy(object):
    """Documentation for Deploy
    
    """
    def __init__(self, config):
        super(EZCommonDeploy, self).__init__()
        self.config = config
        self.deploy_dir = "{}/{}/".format(DEPLOY_DIR,
                                          self.config['name'])
        if not os.path.exists(self.deploy_dir):
            os.makedirs(self.deploy_dir)

    def deploy(self, deploy_script=None):
        if deploy_script is None:
            if not os.path.isfile(
                    self.git_dir + '/conf/deploy.sh'):
                logging.error(
                    "No deploy script")
                return False

            deploy_script = self.git_dir + '/conf/deploy.sh'

        arg = "{} {} {} {}".format(
            deploy_script,
            self.config['package_url'],
            self.deploy_dir,
            self.config['target_dir'],
            self.config['name'],
        )
            
        for s in self.config['servers']:
            results = Runner(
                pattern=s,
                module_name='script',
                module_args=arg,
                ).run()

            print results
            for (h, r) in results['contacted'].items():
                if r['rc'] != 0:
                    logging.error("{} deploy failed.".format(
                        s
                    ))
                    return False

        return True

    
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Usage: {} <yaml file>".format(sys.argv[0])
        exit(1)

