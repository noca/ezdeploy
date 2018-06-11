# -*- coding: utf-8 -*-
'''
Main interface for meicai deploy system
'''


class Deploy(object):
    """Documentation for Deploy
    
    """
    def __init__(self, config):
        super(Deploy, self).__init__()
        self.config = config

    def get_package(self):
        '''
        method to get the deploy package
        '''
        pass

    def deploy(self):
        '''
        method to deploy service on server
        '''
        pass


class Packing(object):
    """Documentation for Packing
    
    """
    def __init__(self, config):
        super(Packing, self).__init__()
        self.config = config
        
    def get_source(self):
        '''
        method to get the packing source code
        ret: packing source code path
        '''
        pass

    def packing(self):
        '''
        method to pack the source code
        ret: package source
        '''
        pass
        
    def get_changelog(self, pre_changelog):
        '''
        method to get changelog from previous changelog
        '''
