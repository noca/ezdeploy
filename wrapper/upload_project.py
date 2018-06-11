#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from ezdeploy import repoclient


DEFAULT_ENV = 'production'

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {} <service> <filename>".format(sys.argv[0]))
        exit(1)

    service = sys.argv[1]
    env = 'production'
    filename = sys.argv[2]

    rc = repoclient.RepoClient(service, env)
    rc.update(filename, service + '.tar.gz', False)
    exit(0)
