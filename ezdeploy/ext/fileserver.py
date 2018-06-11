# -*- coding: utf-8 -*-
'''
Simple Repo Server
'''
import os
import json
from datetime import datetime
import yaml
import bottle
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 1024
from bottle import request, static_file, view, template, redirect
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, \
    Integer, String, DateTime, ForeignKey, and_
from sqlalchemy.ext.declarative import declarative_base

from ezdeploy import cf
from ezdeploy.env import ENV


Base = declarative_base()
engine = create_engine('sqlite:///deploy.db', echo=True)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(engine, Base.metadata, create=True)
app.install(plugin)


class Package(Base):
    __tablename__ = 'packages'

    purl = Column(String(1024), primary_key=True)
    service = Column(String(256))
    env = Column(String(256))
    changelog = Column(String(1024))
    pdate = Column(DateTime())


class Deploy(Base):
    __tablename__ = 'deploys'

    did = Column(Integer(), primary_key=True, autoincrement=True)
    purl = Column(String(1024), ForeignKey("packages.purl"))
    dservice = Column(String(256))
    denv = Column(String(256))
    comment = Column(String(1024))
    ddate = Column(DateTime())


@app.route('/deploy/', method="POST")
def do_deploy(db):
    data = json.loads(request.body.read())
    purl = data['purl'].replace('//', '/')
    dservice = data['dservice'] if 'dservice' in \
        data else ''
    denv = data['denv'] if 'denv' in \
        data else ''
    comment = data['comment'] if 'comment' in \
        data else ''
    d = datetime.now()

    dp = Deploy()
    dp.purl = purl
    dp.dservice = dservice
    dp.denv = denv
    dp.comment = comment
    dp.ddate = d
    db.add(dp)


@app.route('/<fp:re:.*[^\/]$>', method='POST')
def do_upload(fp, db):
    fp = fp.replace('//', '/')
    upload = request.body.read()
    changelog = request.params.changelog if \
        'changelog' in request.params else ''
    name, ext = os.path.splitext(fp)
    if ext.split("_")[0] not in ('.zip', '.png', '.jpg', '.jpeg', '.bz2',
                                 '.gz', '.tar', '.war', '.jar', '.deb',
                                 '.rar'):
        return "File extension not allowed."

    save_path = "{}/{}".format(cf.REPO_PATH, fp)
    if not os.path.exists(
            os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))

    with open(save_path, 'wb') as f:
        print save_path
        f.write(upload)
        f.flush()
        f.close()

    ps = fp.split('/')
    service = ps[0]
    env = ps[1]
    d = datetime.now()
    pp = Package()
    pp.purl = '/' + fp
    pp.service = service
    pp.changelog = changelog
    pp.env = env
    pp.pdate = d

    db.add(pp)
    return "File successfully saved to '{0}'.".format(save_path)


@app.route('/<fp:re:.*[^\/]$>', method='GET')
def do_get(fp):
    fp = fp.replace('//', '/')
    print fp
    return static_file(fp, root=cf.REPO_PATH)


@app.route('/', method='GET')
def do_deploy_page(db):
    dps = db.query(Deploy).order_by(Deploy.ddate.desc()).limit(50).all()

    dlist = list()
    for d in dps:
        pitem = db.query(Package).filter(Package.purl == d.purl).one()
        if pitem:
            new_d = {
                'ddate': str(d.ddate),
                'purl': d.purl,
                'service': pitem.service,
                'penv': pitem.env,
                'changelog': pitem.changelog,
                'pdate': str(pitem.pdate),
                'dservice': d.dservice,
                'denv': d.denv,
                'comment': d.comment
            }
            dlist.append(new_d)

    return template('deploy_list', dlist=dlist)


@app.route('/<fp:re:.*\/$>', method='GET')
def do_list(fp, db):
    fp = fp.replace('//', '/')
    pks = db.query(Package).filter(Package.purl.like('%' + fp + '%')).all()
    dps = db.query(Deploy).filter(Deploy.purl.like('%' + fp + '%')).\
        order_by(Deploy.ddate.desc())
    list_dp = list()
    for dp in dps:
         list_dp.append(dp)

    list_pk = list()
    for pk in pks:
        new_pk = {
            'date': str(pk.pdate),
            'purl': pk.purl,
            'status': '',
            'changelog': pk.changelog
        }
        if len(list_dp) > 0 and pk.purl == list_dp[0].purl:
            new_pk['status'] = 'ONLINE'

        if len(list_dp) > 1 and pk.purl == list_dp[1].purl:
            new_pk['status'] = 'ROLLBACK'

        list_pk.append(new_pk)
        
    return json.dumps(list_pk)


if __name__ == '__main__':
    app.run(host='localhost', port=10081)

