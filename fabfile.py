from __future__ import with_statement
from fabric.api import *
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('buildout.cfg')
env.profiles = []

def get_option(config, option):
    """ Return the value of a config option if it e
    """

def reloadProfilesAndResetCatalog():
    """ Only update profiles """
    with cd(env.path):
        env.execute(env.serverurl % \
            (env.webuser, env.webpass, ' '.join(env.profiles)))

def createSite():
    """ Create a new recensio site. Does not delete old one! """
    update()
    _build()
    with cd(env.path):
        env.execute(env.create_page_command % \
            (env.webuser, env.webpass))
    reloadProfilesAndResetCatalog()

def deleteEverythingAndRebuild():
    """ Deletes you checkout and rebuilds it. DANGEROUS"""
    with cd(env.path):
        env.execute('./bin/supervisorctl shutdown || echo Ignoring Error')
        env.execute('rm -rf parts var')
    createSite()

def _build():
    with cd(env.path):
        env.execute('./bin/supervisorctl shutdown || echo Ignoring Error')
        env.execute('./bin/buildout -c ' + env.buildoutcfg)
        env.execute('./bin/supervisord || echo Ignoring Error')
    env.execute('sleep 20')

def full_update():
    """ A full update """
    update()
    _build()
    reloadProfilesAndResetCatalog()

def restart():
    """ Restart instance """
    with cd(env.path):
        env.execute('bin/supervisorctl restart all')

def update():
    """ Update svn and development eggs """
    with cd(env.path):
        env.execute('svn up')
        env.execute('./bin/develop update -f')

def withDemoContent():
    """ The next steps will also add example data """
    if not env.profiles:
        env.profiles = []
    env.profiles.append('profile-recensio.contenttypes:example_content')

def local():
    """ Work on local environment """
    env.hosts = [config.get('local', 'host')]
    if config.has_option('local', 'key_filename'):
        env.key_filename = config.get('local', 'key_filename')
    env.webuser = 'admin'
    env.webpass = config.get('instance-settings', 'user').split(':')[1]
    env.sudouser = config.get('local', 'sudouser')
    env.execute = lambda cmd: run(cmd)
    env.path = config.get('local', 'path')
    env.serverurl = './bin/recensio-policy-reset http://127.0.0.1:8010/recensio %s %s %s'
    env.create_page_command = './bin/createSite http://127.0.0.1:8010 %s %s'
    env.buildoutcfg = 'buildout.cfg'

def test():
    """ Work on test environment """
    env.hosts = ['zope@ext4.syslab.com']
    env.webuser = 'admin'
    env.webpass = config.get('instance-settings', 'user').split(':')[1]
    env.sudouser = 'zope'
    env.execute = lambda cmd: run(cmd)
    env.path = '/home/zope/recensio'
    env.serverurl = './bin/recensio-policy-reset http://recensio.syslab.com %s %s %s'
    env.create_page_command = './bin/createSite http://recensio.syslab.com:8012 %s %s'
    env.buildoutcfg = 'test-env.cfg'

def production():
    """ Work on production environment """
    env.hosts = ['%s@recensio00.gocept.net' % config.get('production', 'user')]
    env.webuser = 'admin'
    env.webpass = config.get('production', 'web_password')
    env.sudouser = 'recensio'
    env.execute = lambda cmd: sudo(cmd, user = env.sudouser)
    env.path = '/home/recensio/recensio'
    env.serverurl = './bin/recensio-policy-reset http://localhost:8080/recensio %s %s %s'
    env.create_page_command = './bin/createSite http://localhost:8080 %s %s'
    env.buildoutcfg = 'production-env.cfg'

def demo():
    """ Work on test environment """
    env.hosts = ['zope@ext4.syslab.com']
    env.webuser = 'admin'
    env.sudouser = 'zope'
    env.execute = lambda cmd: run(cmd)
    env.path = '/home/zope/recensio_demo'
    env.serverurl = './bin/recensio-policy-reset http://recensio.syslab.com:8013/recensio %s %s %s'
    env.create_page_command = './bin/createSite http://recensio.syslab.com:8013 %s %s recensio.policy:demo'
    env.buildoutcfg = 'demo-env.cfg'

def beta():
    """ Work on beta environment """
    env.hosts = ['%s@recensio00.gocept.net' % config.get('beta', 'user')]
    env.webuser = 'admin'
    env.webpass = config.get('beta', 'web_password')
    env.sudouser = 'recensio'
    env.execute = lambda cmd: sudo(cmd, user = env.sudouser)
    env.path = '/home/recensio/recensio-phase2'
    env.serverurl = './bin/recensio-policy-reset http://localhost:8081/recensio %s %s %s'
    env.create_page_command = './bin/createSite http://localhost:8081 %s %s'
    env.buildoutcfg = 'beta-env.cfg'

