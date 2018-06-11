# -*- coding: utf-8 -*-
'''
This is now just a temp wrapper for cmdb
'''
import os
import yaml
import commands
import logging
from ezdeploy import cf


class CMDBClient(object):
    """Documentation for CMDBClient
    
    """
    def __init__(self):
        super(CMDBClient, self).__init__()
        self.r_servers = list()
        with open(cf.CMDB_F, 'r') as f:
            data = yaml.load(f)
            if 'servers' in data:
                self.r_servers = data['servers']

    def q_server(self, qs, detail=False):
        r_servers = self.r_servers

        # boundary condition for no pair
        legal_qs = False
        
        qlist = qs.split('&')
        for q in qlist:
            qpair = q.split('=')
            # must be a k=v pair
            if len(qpair) != 2:
                continue

            # got at least one pair
            legal_qs = True

            qk = qpair[0]
            qv = qpair[1]
            tmp_servers = list()
            for s in r_servers:
                if qk not in s['tags'].keys():
                    continue
                if qv not in s['tags'][qk] and qv != '*':
                    continue

                tmp_servers.append(s)

            r_servers = tmp_servers

        # judge the condition
        if not legal_qs:
            r_servers = list()
        
        if detail:
            return r_servers
        return [s['host'] for s in r_servers]


if __name__ == '__main__':
    import sys
    cc = CMDBClient()

    if len(sys.argv) != 2:
        print "Usage: python {} <QUERY STRING>".format(sys.argv[0])
        exit(1)
    
    print cc.q_server(sys.argv[1])
