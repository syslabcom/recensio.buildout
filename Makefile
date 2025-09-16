.PHONY: all
all: .installed.cfg

.venv/bin/buildout: .venv/bin/pip3 requirements.txt $(wildcard config/*.txt)
	./.venv/bin/pip3 uninstall -y setuptools
	./.venv/bin/pip3 install -IUr requirements.txt

.venv/bin/pip3:
	python3.11 -m venv .venv

.installed.cfg: .venv/bin/buildout $(wildcard *.cfg config/*.cfg profiles/*.cfg)
	./.venv/bin/buildout

.PHONY: upgrade
upgrade:
	./bin/upgrade plone_upgrade -A &&  ./bin/upgrade install -Ap

.PHONY: clean
clean:
	rm -rf ./.venv

.PHONY: read_registry
read_registry: .installed.cfg
	./bin/instance run scripts/read_registry.py etc/registry/*.xml

.PHONY: graceful
graceful: .installed.cfg
	./bin/supervisord 2> /dev/null || ( \
	    ./bin/supervisorctl reread && \
		./bin/supervisorctl update && \
		for process in `./bin/supervisorctl status | egrep -v '(zeo|HttpOk|MemoryMonitor)' | awk '{print $$1}'`; do \
			./bin/supervisorctl restart "$$process" && \
			sleep 30; \
		done \
	)
