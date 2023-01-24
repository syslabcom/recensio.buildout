# recensio.buildout

## Install

```
echo "[buildout]" > custom.cfg
ln -s profiles/development.cfg buildout.cfg
make
./bin/supervisord
./bin/instance fg
```

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
