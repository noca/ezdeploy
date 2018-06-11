# -*- coding: utf-8 -*-
import logging
import random

import requests


def http2http(src_uri, dest_uri):
    tmp_file = '/tmp/common_cp_{}'.format(
        ''.join(random.choice('abcdefghijklopqrstuvwxyz')
                for _ in range(5)))
        
    r = requests.get(src_uri, stream=True)
    if r.status_code != 200:
        logging.error("Source {} doesn't exists".format(
            src_uri))
        return False

    with open(tmp_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    with open(tmp_file, 'rb') as f:
        data = f.read()
        r = requests.post(url=dest_uri,
                          data=data,
                          headers={
                              'Content-Type': 'application/octet-stream',
                          })
        
        if r.status_code != 200:
            logging.error('Dest {} doesn\'t success'.format(
                dest_uri))
            return False

    return True
    

def http2file(src_uri, dest_uri):
    r = requests.get(src_uri, stream=True)
    if r.status_code != 200:
        logging.error("Source {} doesn't exists".format(
            src_uri))
        return False

    with open(dest_uri.replace('file://', ''), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    return True


def file2http(src_uri, dest_uri):
    with open(src_uri.replace('file://', ''), 'rb') as f:
        data = f.read()
        r = requests.post(url=dest_uri,
                          data=data,
                          headers={
                              'Content-Type': 'application/octet-stream',
                          })
        
        if r.status_code != 200:
            logging.error('Dest {} doesn\'t success'.format(
                dest_uri))
            return False

    return True
    

def file2file(src_uri, dest_uri):
    with open(dest_uri.replace('file://', ''), 'wb') as wf:
        with open(src_uri.replace('file://', ''), 'rb') as rf:
            wf.write(rf.read())
            wf.flush()

    return True


def common_cp(src_uri='', dest_uri=''):
    if src_uri.startswith('http://') and dest_uri.startswith('http://'):
        return http2http(src_uri, dest_uri)
    elif src_uri.startswith('http://') and dest_uri.startswith('file://'):
        return http2file(src_uri, dest_uri)
    elif src_uri.startswith('file://') and dest_uri.startswith('http://'):
        return file2http(src_uri, dest_uri)
    elif src_uri.startswith('file://') and dest_uri.startswith('file://'):
        return file2file(src_uri, dest_uri)

    logging.error("Unrecognized source {} and dest {}".format(
        src_uri, dest_uri))
    return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print "Usage: python commoncp.py <SOURCE> <DEST>"
        exit(1)

    common_cp(sys.argv[1], sys.argv[2])
