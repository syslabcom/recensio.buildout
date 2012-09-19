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
               'elinks',
               'zlib1g-dev',
               'libbz2-dev',]:
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
    exec {'wget https://launchpad.net/plone/4.2/4.2.1/+download/Plone-4.2.1-UnifiedInstaller.tgz':
        creates => '/home/vagrant/tmp/Plone-4.2.1-UnifiedInstaller.tgz',
        cwd => '/home/vagrant/tmp',
        before => Exec["untar1"],
    }

    exec {'tar xzf Plone-4.2.1-UnifiedInstaller.tgz':
        alias => "untar1",
        creates => '/home/vagrant/tmp/Plone-4.2.1-UnifiedInstaller',
        cwd => '/home/vagrant/tmp',
        before => Exec["untar2"],
    }

    exec {'tar -C /home/vagrant/.buildout/ -xjf buildout-cache.tar.bz2':
        alias => "untar2",
        creates => '/home/vagrant/.buildout/buildout-cache/eggs/Products.CMFPlone-4.2.1.1-py2.7.egg',
        cwd => '/home/vagrant/tmp/Plone-4.2.1-UnifiedInstaller/packages/',
    }

    exec {'wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py':
        alias => "get-virtualenv",
        creates => '/home/vagrant/tmp/virtualenv.py',
        cwd => '/home/vagrant/tmp',
        before => Exec["virtualenv"],
    }

    exec {'python2.7 tmp/virtualenv.py --no-site-packages -p python2.7 py27':
        alias => "virtualenv",
        creates => '/home/vagrant/py27',
        cwd => '/home/vagrant',
        before => Exec["bootstrap"],
    }

    exec {'/home/vagrant/py27/bin/python bootstrap.py':
        alias => "bootstrap",
        creates => '/vagrant/bin/buildout',
        cwd => '/vagrant',
    }

}
