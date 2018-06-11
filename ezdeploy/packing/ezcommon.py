# -*- coding: utf-8 -*-
import os
import commands
import shutil
import logging
import yaml

from ezdeploy.cmdbclient import CMDBClient
from ezdeploy.interface import Packing
from ezdeploy.cf import GIT_DIR
from ezdeploy.cf import PACKING_DIR
from ezdeploy.cf import PACKAGE_DIR


class EZCommonPacking(Packing):
    """
    Check out Source and Config by branch, and copy config to source
    """
    def __init__(self, config):
        super(EZCommonPacking, self).__init__(config)
        self.config = config
        self.git_dir = '{}/{}'.format(
            GIT_DIR, self.config['name']
        )
        self.packing_dir = '{}/{}'.format(
            PACKING_DIR, self.config['name']
        )
        self.package_dir = '{}/{}'.format(
            PACKAGE_DIR, self.config['name']
        )
        if not os.path.exists(self.git_dir):
            os.makedirs(self.git_dir)
        if not os.path.exists(self.packing_dir):
            os.makedirs(self.packing_dir)
        if not os.path.exists(self.package_dir):
            os.makedirs(self.package_dir)

    def _checkout(self, repo, path, branch):
        if not os.path.exists(path):
            (ret, out) = commands.getstatusoutput("git clone {} {}".format(
                repo,
                path))
            
            print out
            if ret != 0:
                logging.error("fetch git repo failed")
                return False
        
        (ret, out) = commands.getstatusoutput("git -C {} pull  && git -C {} checkout {}"
                                              " && git -C {} pull &&"
					      " git -C {} submodule update --init --recursive &&"
                                              " git -C {} submodule foreach git pull origin master"
                                              .format(path,
                                                  path, branch, path, path, path))

        print out
        if ret != 0:
            logging.error("fetch git branch failed")
            return False

        return True
                
    def _fetch(self):
        if not self._checkout(
                self.config['git']['repo'],
                self.git_dir + '/git',
                self.config['git']['branch']):
            return False

        if not self._checkout(
                self.config['conf']['repo'],
                self.git_dir + '/conf',
                self.config['conf']['branch']):
            return False
        
        return True

    def _copy_and_clear(self, source, dest):
        if os.path.exists(dest):
            (ret, out) = commands.getstatusoutput("rm -rf {}".format(dest))
            if ret != 0:
                logging.error("Remove {} failed".format(dest))
                return False
        
        (ret, out) = commands.getstatusoutput("cp -rf {} {}".format(
            source, dest))
        if ret != 0:
            logging.error("Copy {} repo failed".format(source))
            return False
        
        (ret, out) = commands.getstatusoutput("rm -rf {}".format(
            dest + '/.git'))
        if ret != 0:
            logging.error("Remove {} .git failed".format(source))
            return False

        return True

    def _replace(self, source, dest):
        for root, dirs, files in os.walk(source, followlinks=True):
            for f in files:
                f = os.path.join(root, f)
                f = f.replace(source, '')
                shutil.copyfile(source + f, dest + f)

        return False
        
    def _merge(self):
        if not self._copy_and_clear(self.git_dir + '/git',
                                    self.packing_dir):
            return False
        
        if self._replace(self.git_dir + '/conf/' +
                         self.config['conf']['service'] +
                         '/' + self.config['env'],
                         self.packing_dir):
            logging.error("Replace {} files failed".format(
                self.config.data))
            return False

        return True

    def get_package(self):
        if not self._fetch():
            logging.error("fetch source failed")
            return False
        if not self._merge():
            logging.error("merge source failed")
            return False
        
        return True
    
    def packing(self, packing_script=None):
        if packing_script is None:
            if not os.path.isfile(
                    self.git_dir + '/conf/packing.sh'):
                logging.error(
                    "No packing script")
                return None

            packing_script = self.git_dir + '/conf/packing.sh'

        ret, fp = commands.getstatusoutput(
            "{} {} {}".format(
                packing_script,
                self.packing_dir,
                self.package_dir
            ))
        print fp
        if ret != 0:
            logging.error("packaging {} failed.".format(
                self.packing_dir))
            return None

        return fp

    def run(self):
        if not self._pack():
            logging.error("pack source failed")
            return False
        logging.info("Pack source successfully.")

        logging.info("Pack {} successfully.".format(
            self.config.data['name']))

        print "{} is packaged.".format(
            self.config.data['target'])
        return True

    
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Usage: {} <yaml file>".format(sys.argv[0])
        exit(1)

    pack = Packing(config)
    pack.run()
