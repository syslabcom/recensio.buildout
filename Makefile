.PHONY: all
all: .installed.cfg solr

.venv/bin/buildout: .venv/bin/pip3 requirements.txt $(wildcard config/*.txt)
	# To really be sure we have the desired setuptools we need to uninstall it first
	./.venv/bin/pip3 uninstall -y setuptools
	# ... and reinstall it later
	./.venv/bin/pip3 install -IUr config/requirements-venv.txt -c config/constraints.txt
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
	rm -rf ./.venv .installed.cfg

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


solr-9.9.0.tgz:
	curl -o solr-9.9.0.tgz https://dlcdn.apache.org/solr/solr/9.9.0/solr-9.9.0.tgz

solr-9.9.0/server/solr/plone/conf/schema.xml: solr-9.9.0.tgz
	tar xvzf solr-9.9.0.tgz
	mkdir -p solr-9.9.0/server/solr/plone
	cp -r etc/solr/* solr-9.9.0/server/solr/plone/

.PHONY: solr
solr: solr-9.9.0/server/solr/plone/conf/schema.xml
