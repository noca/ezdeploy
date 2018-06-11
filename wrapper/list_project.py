#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from ezdeploy import repoclient


DEFAULT_ENV = 'production'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <service>".format(sys.argv[0]))
        exit(1)

    service = sys.argv[1]
    env = 'production'

    rc = repoclient.RepoClient(service, env)
    print("Repo Info:")
    for d in rc.list(fullpath=True):
        print(d['purl'] + '\t' + d['status'] + '\t' + d['changelog'])

    exit(0)
