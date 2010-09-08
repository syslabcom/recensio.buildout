from __future__ import with_statement
from fabric.api import *
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('secret.cfg')
env.profiles = []

def reloadProfilesAndResetCatalog():
    """ Only update profiles """
    webpass = config.get('instance-settings', 'user').split(':')[1]
    with cd(env.path):
        run(env.serverurl % \
            (env.webuser, webpass, ' '.join(env.profiles)))

def createSite():
    """ Create a new recensio site. Does not delete old one! """
    update()
    _build()
    webpass = config.get('instance-settings', 'user').split(':')[1]
    with cd(env.path):
        run(env.create_page_command % \
            (env.webuser, webpass))
    reloadProfilesAndResetCatalog()

def deleteEverythingAndRebuild():
    """ Deletes you checkout and rebuilds it. DANGEROUS"""
    with cd(env.path):
        run('./bin/supervisorctl shutdown || echo Ignoring Error')
        run('rm -rf parts var')
    createSite()

def _build():
    with cd(env.path):
        run('./bin/supervisorctl shutdown || echo Ignoring Error')
        run('./bin/buildout -c ' + env.buildoutcfg)
        run('./bin/supervisord || echo Ignoring Error')
    run('sleep 20')

def full_update():
    """ A full update """
    update()
    _build()
    reloadProfilesAndResetCatalog()

def update():
    """ Update svn and development eggs """
    with cd(env.path):
        run('svn up')
        run('./bin/develop update -f')

def withDemoContent():
    """ The next steps will also add example data """
    if not env.profiles:
        env.profiles = []
    env.profiles.append('profile-recensio.contenttypes:example_content')

def local():
    """ Work on local environment """
    env.hosts = [config.get('local', 'host')]
    env.webuser = 'admin'
    env.path = config.get('local', 'path')
    env.serverurl = './bin/reset http://127.0.0.1:8010/recensio %s %s %s'
    env.create_page_command = './bin/createSite http://127.0.0.1:8010 %s %s'
    env.buildoutcfg = 'buildout.cfg'

def test():
    """ Work on test environment """
    env.hosts = ['zope@ext4.syslab.com']
    env.webuser = 'admin'
    env.path = '/home/zope/recensio'
    env.serverurl = './bin/reset http://recensio.syslab.com %s %s %s'
    env.create_page_command = './bin/createSite http://recensio.syslab.com:8012 %s %s'
    env.buildoutcfg = 'test-env.cfg'

def demo():
    """ Work on test environment """
    if not env.profiles:
        env.profiles = []
    env.profiles.append('profile.recensio.policy:demo')
    env.hosts = ['zope@ext4.syslab.com']
    env.webuser = 'admin'
    env.path = '/home/zope/recensio_demo'
    env.serverurl = './bin/reset http://recensio.syslab.com %s %s %s'
    env.create_page_command = './bin/createSite http://recensio.syslab.com:8013 %s %s'
    env.buildoutcfg = 'demo-env.cfg'

def production():
    """ Work on production environment """
    env.hosts = ['guest@localhost']
    env.webuser = 'admin'
    env.path = '/home/guest/denso-esc'
    env.serverurl = 'http_proxy=;./bin/reset http://127.0.0.1:8082/denso-esc %s %s %s'
    env.buildoutcfg = 'production.cfg'
