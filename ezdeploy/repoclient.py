# -*- coding: utf-8 -*-
import os
import logging
import requests
import time
import json

from ezdeploy.cf import REPO_URL
from ezdeploy.libs.commoncp import common_cp


class RepoClient(object):
    """Documentation for RepoClient
    
    Repo name rule:
    /<service>/<env>/<package name>_<date>_<version>
    """
    REPO_URL = REPO_URL

    def __init__(self, service, env):
        super(RepoClient, self).__init__()
        self.repo_url = '{}/{}/{}/'.format(
            self.REPO_URL, service, env
        )
        self.service = service
        self.env = env

    def list(self, fullpath=False):
        r = requests.get(self.repo_url)
        data = list()
        if r.status_code == 200:
            data = r.json()

        data.sort(reverse=True, key=lambda d: d['purl'])

        if fullpath:
            for d in data:
                d['purl'] = self.REPO_URL + '/' + d['purl']
            #data = [self.repo_url + '/' + p for d in data]

        return data
        
    def update(self, f, pname, replace=True, changelog=''):
        if not os.path.isfile(f):
            logging.error("No file exists {}".format(
                f
            ))

        # find the proper name
        r_list = [d['purl'] for d in self.list()]
        date_list = [r.split("_")[-2] for r in r_list]
        date_list.sort()

        td = time.strftime("%Y%m%d")
        name = "{}_{}_{}".format(pname, td, 1)
        if len(date_list) == 0 or (td > date_list[-1]):
            # new date version
            name = "{}_{}_{}".format(pname, td, 1)
        else:
            # new version
            today_list = list()
            for r in r_list:
                if td in r:
                    today_list.append(r)

            v_list = [int(r.split("_")[-1]) for r in today_list]
            v_list.sort()
            nv = v_list[-1] if replace else (v_list[-1] + 1)
            name = "{}_{}_{}".format(pname, td, nv)

        ret = common_cp("file://" + f,
                        self.repo_url + '/' + name
                        + "?changelog=%s" % (changelog))
        if not ret:
            logging.error("update repo {} failed.".format(
                self.repo_url + '/' + name
            ))
            return None
        
        logging.info("Update repo {} success.".format(
            self.repo_url + '/' + name))

        print "{} is update to repo.".format(
            self.repo_url + '/' + name)
        
        return self.repo_url + '/' + name

    def deploy(self, url, comment=''):
        r = requests.post(self.REPO_URL + '/deploy/',
                          data=json.dumps({'purl': url,
                                           'dservice': self.service,
                                           'denv': self.env,
                                           'comment': comment}),
                          headers={'content-type': 'application/json'})
        if r.status_code != 200:
            return False
        
        return True

        
if __name__ == "__main__":
    import sys
    '''
    if len(sys.argv) == 3:
        repo = RepoClient(sys.argv[1], 'staging')
        repo.update(sys.argv[2], sys.argv[1]+".tar.gz", False)
        exit(0)
    '''
    if len(sys.argv) == 3:
        repo = RepoClient(sys.argv[1], sys.argv[2])
        print "Repo Info:"
        i = 0
        for d in repo.list(fullpath=True):
            print d['purl'] + '\t' + d['status'] + '\t' + d['changelog']
            i += 1
        exit(0)

    print "Usage: {} <name> <environment>".format(sys.argv[0])
    exit(1)
