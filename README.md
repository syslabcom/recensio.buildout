# recensio.buildout

## Install

```
echo "[buildout]" > custom.cfg
ln -s profiles/development.cfg buildout.cfg
make
./bin/supervisord
./bin/instance fg
```

## Solr

Note that the buildout configured ./bin/solr is to be used only for unit/integration tests.

There's a separate Solr installation in ./solr-9.9.9.0/bin/solr that is set up
via the Makefile, not via buildout. You run the development solr with supervisor.

Note that for this to work properly it needs specific flags in the environment::

    SOLR_ENABLE_REMOTE_STREAMING=true SOLR_ENABLE_STREAM_BODY=true SOLR_OPTS="-Dsolr.allowPaths=${instance:blob-storage}"

These flags are provided via the supervisord config in buildout; the supervisor
entry in turn depends on the non-buildout Solr install. Yes it's convoluted.

- buildout provides the test solr
- buildout provides supervisor which has a configuration for the development solr
- the development solr is provisioned by the Makefile, without buildout

## Scripts

There is a scripts folder in the package that contains some useful
scripts that can be run from the command line.

### `scripts/configure_smtp_queue.py`

This script configures the Plone site to use the `smtp_queue`.
It accepts two positional parameters:

1. The Plone site id
2. The target folder for the queue

You can run it with:

```bash
./bin/instance run scripts/configure_smtp_queue.py Plone var/smtp-queue
```

The target folder (in the example `var/smtp-queue`), has to be created manually.
It should contain three subfolders:

- `cur`
- `new`
- `tmp`

and it is probably a good idea to only allow the user running the Plone instance to access them:

```bash
mkdir -p var/smtp-queue/
mkdir -p var/smtp-queue/{cur,new,tmp}
chmod 700 var/smtp-queue/{cur,new,tmp}
```

### `scripts/read_registry.py`

This script scan the `etc/registry` folder for `xml` files and tries to read them
to configure your portal_registry.

You can use it with:

```bash
make read_registry
```
