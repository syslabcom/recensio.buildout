class buildout {

    exec { "aptitude update --quiet --assume-yes":
        alias => "aptupdate",
        path => "/usr/bin",
        user => "root",
        timeout => 0,
        before => Package['python-virtualenv'],
    }

    user { "vagrant":
        groups => [
            "sudo"
        ]
    }

    group { "puppet":
        ensure => "present",
    }

    package { 'python-virtualenv':
        ensure => installed,
        before => Exec["virtualenv"],
    }

    package { ['python-dev',
               'libjpeg62-dev',
               'libxslt1-dev',
               'git-core',
               'subversion',
               'wget',
               'default-jdk',
               'elinks',]:
        ensure => installed,
        before => Exec["virtualenv"],
    }

    file { ['/vagrant/src',
            '/vagrant/var',
            '/home/vagrant/tmp',
            '/home/vagrant/.buildout',
            '/home/vagrant/.buildout/buildout-cache',
            '/home/vagrant/.buildout/buildout-cache/eggs',
            '/home/vagrant/.buildout/buildout-cache/downloads',
            '/home/vagrant/.buildout/buildout-cache/extends',]:
        ensure => directory,
        owner => 'vagrant',
        group => 'vagrant',
        mode => '0664',
    }

    file { '/home/vagrant/.buildout/default.cfg':
        ensure => present,
        content => template('buildout/default.cfg'),
        owner => 'vagrant',
        group => 'vagrant',
        mode => '0664',
    }

    Exec {
        path => [
           '/usr/local/bin',
           '/opt/local/bin',
           '/usr/bin',
           '/usr/sbin',
           '/bin',
           '/sbin'],
        logoutput => true,
        user => 'vagrant',
    }

    # Get the unified installer and unpack the buildout-cache
    exec {'wget http://launchpad.net/plone/4.0/4.0.3/+download/Plone-4.0.3-20110720-UnifiedInstaller.tgz':
        alias => "unified_installer",
        creates => '/home/vagrant/tmp/Plone-4.0.3-20110720-UnifiedInstaller.tgz',
        cwd => '/home/vagrant/tmp',
    }

    exec {'tar xzf Plone-4.0.3-20110720-UnifiedInstaller.tgz':
        creates => '/home/vagrant/tmp/Plone-4.0.3-UnifiedInstaller',
        cwd => '/home/vagrant/tmp',
    }

    exec {'tar -C /home/vagrant/.buildout/ -xjf buildout-cache.tar.bz2':
        creates => '/home/vagrant/.buildout/buildout-cache/eggs/Products.CMFPlone-4.0.3-py2.6.egg',
        cwd => '/home/vagrant/tmp/Plone-4.0.3-UnifiedInstaller/packages/',
    }

    exec {'virtualenv --no-site-packages py26':
        alias => "virtualenv",
        creates => '/home/vagrant/py26',
        cwd => '/home/vagrant',
        before => Exec["bootstrap"],
    }

    exec {'/home/vagrant/py26/bin/python bootstrap.py':
        alias => "bootstrap",
        creates => '/vagrant/bin/buildout',
        cwd => '/vagrant',
    }

}
