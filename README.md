# recensio.buildout


## Install


```
echo "[buildout]" > custom.cfg
ln -s profiles/development.cfg buildout.cfg
make
./bin/supervisord
./bin/instance fg
```
