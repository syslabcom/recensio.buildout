from __future__ import with_statement
from fabric.api import *
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('profiles/secret.cfg')
env.profiles = []

def reloadProfilesAndResetCatalog():
    """ Only update profiles """
    with cd(env.path):
        run(env.serverurl % \
            (env.webuser, env.webpass, ' '.join(env.profiles)))

def createSite():
    """ Create a new recensio site. Does not delete old one! """
    update()
    _build()
    with cd(env.path):
        run(env.create_page_command % \
            (env.webuser, env.webpass))
    reloadProfilesAndResetCatalog()

def deleteEverythingAndRebuild():
    """ Deletes you checkout and rebuilds it. DANGEROUS"""
    with cd(env.path):
        run('./bin/supervisorctl shutdown || echo Ignoring Error')
        run('rm -rf var parts || echo Ignoring Error')
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

def restart():
    """ Restart instance """
    with cd(env.path):
        run('bin/supervisorctl restart all || bin/supervisord')

def update():
    """ Update svn and development eggs """
    for host in env.hosts:
        local("rsync -r --rsh=ssh src %s@%s:%s" % (env.user, host, env.path))
    with cd(env.path):
        run('svn up')
        run('./bin/develop update -f')

def pullback():
    """Copy src from remote to local"""
    for host in env.hosts:
        local("rsync -r --rsh=ssh %s@%s:%s/src ." % (env.user, host, env.path))

def withDemoContent():
    """ The next steps will also add example data """
    if not env.profiles:
        env.profiles = []
    env.profiles.append('profile-recensio.contenttypes:example_content')

def patrick_cloud():
    env.hosts = [config.get('cloud', 'host')]
    env.webuser = 'admin'
    env.user = 'zope'
    env.webpass = config.get('instance-settings', 'user').split(':')[1]
    env.path = '/home/zope/recensio'
    env.serverurl = './bin/recensio-policy-reset http://localhost:8010/recensio %s %s %s'
    env.create_page_command = './bin/createSite http://localhost:8010 %s %s'
    env.buildoutcfg = 'buildout.cfg'
