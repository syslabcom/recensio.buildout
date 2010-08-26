from __future__ import with_statement
from fabric.api import *
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('secret.cfg')
env.profiles = []

def refresh():
    webpass = config.get('instance-settings', 'user').split(':')[1]
    with cd(env.path):
        run(env.serverurl % \
            (env.webuser, webpass, ' '.join(env.profiles)))

def createSite():
    webpass = config.get('instance-settings', 'user').split(':')[1]
    with cd(env.path):
        run(env.create_page_command % \
            (env.webuser, webpass))

def deleteEverythingAndRebuild():
    with cd(env.path):
        run('rm -rf .')
        run('svn up')
    build()
    full_update()

def build():
    with cd(env.path):
        run('./bin/supervisord || echo Ignoring Error')
        run('./bin/supervisorctl stop solr')
        run('./bin/buildout -c ' + env.buildoutcfg)
        run('./bin/supervisorctl start solr')

def update():
    with cd(env.path):
        run('./bin/supervisord || echo Ignoring Error')
        run('svn up')
        run('./bin/develop update -f')
        run('./bin/supervisorctl stop all || echo Ignoring Error')
    build()
    with cd(env.path):
        run('./bin/supervisorctl start all')
        run('sleep 20')
    refresh()

def withDemoContent():
    env.profiles = ['example-data']

def local():
    env.hosts = [config.get('local', 'host')]
    env.webuser = 'admin'
    env.path = config.get('local', 'path')
    env.serverurl = './bin/reset http://127.0.0.1:8010/recensio %s %s %s'
    env.create_page_command = './bin/createSite http://127.0.0.1:8010 %s %s'
    env.buildoutcfg = 'buildout.cfg'

def test():
    1/0
    env.hosts = ['zope@ext4.syslab.com']
    env.webuser = 'admin'
    env.path = '/home/zope/recensio'
    env.serverurl = './bin/reset http://recensio.syslab.com %s %s %s'
    env.create_page_command = './bin/createSite https://recensio.syslab.com %s %s'
    env.buildoutcfg = 'test.cfg'

def production():
    env.hosts = ['guest@localhost']
    env.webuser = 'admin'
    env.path = '/home/guest/denso-esc'
    env.serverurl = 'http_proxy=;./bin/reset http://127.0.0.1:8082/denso-esc %s %s %s'
    env.buildoutcfg = 'production.cfg'
