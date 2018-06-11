# -*- coding: utf-8 -*-
'''
Wrapper for command lines

'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import argparse
from urlparse import urlparse

from ezdeploy.packing.ezcommon import EZCommonPacking
from ezdeploy.deploy.ezcommon import EZCommonDeploy
from ezdeploy.cmdbclient import CMDBClient
from ezdeploy.repoclient import RepoClient


parser = argparse.ArgumentParser(description="Wrapper for deploy commands")
parser.add_argument('-s', help="Service name", required=True)
subparsers = parser.add_subparsers(help="sub-command help")

p_parser = subparsers.add_parser('pack', help="Package the project")
p_parser.add_argument('-r', help="repo path", required=True)
p_parser.add_argument('-b', help="repo branch", required=True)
p_parser.add_argument('-cr', help="config repo path", required=True)
p_parser.add_argument('-cb', help="config repo branch", required=True)
p_parser.add_argument('-cs', help="config repo service dir", required=True)
p_parser.add_argument('-pe', help="package environment", required=True)
p_parser.add_argument('-bs', help="build script", required=False)
p_parser.set_defaults(which="pack")
 
d_parser = subparsers.add_parser('deploy', help="Deploy the project")
d_parser.add_argument('-p', help="package url", required=True)
d_parser.add_argument('-de', help="deploy environment", required=True)
d_parser.add_argument('-wr', help="workspace directory", required=True)
d_parser.add_argument('-ds', help="deploy script", required=False)
d_parser.set_defaults(which="deploy")

pd_parser = subparsers.add_parser('deployinst',
                                  help="Deploy the project instantly")
pd_parser.add_argument('-r', help="repo path", required=True)
pd_parser.add_argument('-b', help="repo branch", required=True)
pd_parser.add_argument('-cr', help="config repo path", required=True)
pd_parser.add_argument('-cb', help="config repo branch", required=True)
pd_parser.add_argument('-cs', help="config repo service dir", required=True)
pd_parser.add_argument('-pe', help="package environment", required=True)
pd_parser.add_argument('-bs', help="build script", required=False)
pd_parser.add_argument('-de', help="deploy environment", required=True)
pd_parser.add_argument('-wr', help="workspace directory", required=True)
pd_parser.add_argument('-ds', help="deploy script", required=False)
pd_parser.set_defaults(which="deployinst")


def packing_now(env, git_repo, git_branch, conf_repo,
                conf_branch, conf_service):
    config['env'] = env
    config['git'] = dict()
    config['git']['repo'] = git_repo
    config['git']['branch'] = git_branch
    config['conf'] = dict()
    config['conf']['repo'] = conf_repo
    config['conf']['branch'] = conf_branch
    config['conf']['service'] = conf_service
    packing = EZCommonPacking(config)
    ret = packing.get_package()
    if not ret:
        print "Packing {} failed.".format(
            config['name']
        )
        return None
    
    path = packing.packing(
        args.bs if hasattr(args, 'bs') else None)
    if path is not None:
        name = os.path.basename(path)
        rc = RepoClient(args.s, args.pe)
        url = rc.update(path, name, replace=False,
                        changelog="Branch: %s" % (git_branch))
        return url

    return None


def deploy_now(env, package_url, target_dir, deploy_script=None):
    config['env'] = env
    config['package_url'] = package_url
    config['target_dir'] = target_dir
        
    cc = CMDBClient()
    config['servers'] = cc.q_server(
        "service={}&env={}".format(
            config['name'], config['env']
        ))
    deploy = EZCommonDeploy(config)
    ret = deploy.deploy(deploy_script)
    if not ret:
        print "Deploying {} failed.".format(
            config['name']
        )
        return None

    rc = RepoClient(args.s, args.de)
    o = urlparse(package_url)
    rc.deploy(o.path)

    return True


if __name__ == "__main__":
    args = parser.parse_args()

    config = dict()
    config['name'] = args.s

    if args.which == 'pack':
        ret = packing_now(args.pe,
                          args.r,
                          args.b,
                          args.cr,
                          args.cb,
                          args.cs)
        if ret is None:
            exit(1)
    elif args.which == 'deploy':
        ret = deploy_now(args.de,
                         args.p,
                         args.wr,
                         args.ds if hasattr(args, 'ds') else None)
        if ret is None:
            exit(1)
    elif args.which == 'deployinst':
        retp = packing_now(args.pe,
                           args.r,
                           args.b,
                           args.cr,
                           args.cb,
                           args.cs)
        if retp is None:
            exit(1)

        retd = deploy_now(args.de,
                          retp,
                          args.wr,
                          args.ds if hasattr(args, 'ds') else None)
        if retd is None:
            exit(1)
            
    exit(0)
