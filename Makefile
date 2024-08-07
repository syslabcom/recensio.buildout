.PHONY: all
all: .installed.cfg

py3/bin/buildout: py3/bin/pip3 requirements.txt $(wildcard config/*.txt)
	# To really be sure we have the desired setuptools we need to uninstall it first
	./py3/bin/pip3 uninstall -y setuptools
	# ... and reinstall it later
	./py3/bin/pip3 install -IUr config/requirements-venv.txt -c config/constraints.txt
	./py3/bin/pip3 install -IUr requirements.txt
	./py3/bin/pip list | grep "plone.recipe.zope2instance.*6.12.2$$" && ./py3/bin/pip3 install plone.recipe.zope2instance==6.13.0

py3/bin/pip3:
	python3 -m venv py3

.installed.cfg: py3/bin/buildout $(wildcard *.cfg config/*.cfg profiles/*.cfg)
	./py3/bin/buildout

.PHONY: upgrade
upgrade:
	./bin/upgrade plone_upgrade -A &&  ./bin/upgrade install -Ap

.PHONY: clean
clean:
	rm -rf ./py3

.PHONY: read_registry
read_registry: .installed.cfg
	./bin/instance run scripts/read_registry.py etc/registry/*.xml

.PHONY: graceful
graceful: .installed.cfg
	./bin/supervisord 2> /dev/null || ( \
	    ./bin/supervisorctl reread && \
		./bin/supervisorctl update && \
		for process in `./bin/supervisorctl status | grep -v zeo | awk '{print $$1}'`; do \
			./bin/supervisorctl restart "$$process" && \
			sleep 30; \
		done \
	)
