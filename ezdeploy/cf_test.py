# -*- coding: utf-8 -*-
'''
Global configuration macro
'''
import os

REPO_PATH = '/data/service_repo'
REPO_URL = 'http://127.0.0.1:10081'

GIT_DIR = '/data/ezdeploy_data/git/'
PACKING_DIR = '/data/ezdeploy_data/packing/'
PACKAGE_DIR = "/data/ezdeploy_data/package/"
DEPLOY_DIR = "/data/ezdeploy_data/deploy/"

CMDB_F = os.path.dirname(os.path.realpath(__file__)) + "/../conf/cmdb.yaml"
