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
        sudo(env.serverurl % \
            (env.webuser, webpass, ' '.join(env.profiles)),
            user = env.sudouser)

def createSite():
    """ Create a new recensio site. Does not delete old one! """
    update()
    _build()
    webpass = config.get('instance-settings', 'user').split(':')[1]
    with cd(env.path):
        sudo(env.create_page_command % \
            (env.webuser, webpass),
            user = env.sudouser)
    reloadProfilesAndResetCatalog()

def deleteEverythingAndRebuild():
    """ Deletes you checkout and rebuilds it. DANGEROUS"""
    with cd(env.path):
        sudo('./bin/supervisorctl shutdown || echo Ignoring Error',
             user = env.sudouser)
        sudo('rm -rf parts var', user = env.sudouser)
    createSite()

def _build():
    with cd(env.path):
        sudo('./bin/supervisorctl shutdown || echo Ignoring Error',
             user = env.sudouser)
        sudo('./bin/buildout -c ' + env.buildoutcfg, user = env.sudouser)
        sudo('./bin/supervisord || echo Ignoring Error', user = env.sudouser)
    sudo('sleep 20', user = env.sudouser)

def full_update():
    """ A full update """
    update()
    _build()
    reloadProfilesAndResetCatalog()

def update():
    """ Update svn and development eggs """
    with cd(env.path):
        sudo('svn up', user = env.sudouser)
        sudo('./bin/develop update -f', user = env.sudouser)

def withDemoContent():
    """ The next steps will also add example data """
    if not env.profiles:
        env.profiles = []
    env.profiles.append('profile-recensio.contenttypes:example_content')

def local():
    """ Work on local environment """
    env.hosts = [config.get('local', 'host')]
    env.webuser = 'admin'
    env.sudouser = config.get('local', 'sudouser')
    env.path = config.get('local', 'path')
    env.serverurl = './bin/recensio-policy-reset http://127.0.0.1:8010/recensio %s %s %s'
    env.create_page_command = './bin/createSite http://127.0.0.1:8010 %s %s'
    env.buildoutcfg = 'buildout.cfg'

def test():
    """ Work on test environment """
    env.hosts = ['zope@ext4.syslab.com']
    env.webuser = 'admin'
    env.sudouser = 'zope'
    env.path = '/home/zope/recensio'
    env.serverurl = './bin/recensio-policy-reset http://recensio.syslab.com %s %s %s'
    env.create_page_command = './bin/createSite http://recensio.syslab.com:8012 %s %s'
    env.buildoutcfg = 'test-env.cfg'

def production():
    """ Work on production environment """
    env.hosts = ['%s@recensio00.syslab.com' % config.get('production', 'user')]
    env.webuser = 'admin'
    env.sudouser = 'recensio'
    env.path = '/home/recensio/recensio'
    env.serverurl = './bin/recensio-policy-reset http://recensio00.syslab.com:8080/recensio %s %s'
    env.create_page_command = './bin/createSite http://recensio.syslab.com:8080 %s %s'
    env.buildoutcfg = 'production-env.cfg'

def demo():
    """ Work on test environment """
    env.hosts = ['zope@ext4.syslab.com']
    env.webuser = 'admin'
    env.sudouser = 'zope'
    env.path = '/home/zope/recensio_demo'
    env.serverurl = './bin/recensio-policy-reset http://recensio.syslab.com:8013/recensio %s %s %s'
    env.create_page_command = './bin/createSite http://recensio.syslab.com:8013 %s %s recensio.policy:demo'
    env.buildoutcfg = 'demo-env.cfg'

def production():
    """ Work on production environment """
    env.hosts = ['guest@localhost']
    env.webuser = 'admin'
    env.path = '/home/guest/denso-esc'
    env.serverurl = 'http_proxy=;./bin/recensio-policy-reset http://127.0.0.1:8082/denso-esc %s %s %s'
    env.buildoutcfg = 'production.cfg'
