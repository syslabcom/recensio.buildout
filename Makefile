.PHONY: all
all: .installed.cfg solr/server/solr/plone/conf/schema.xml

.venv/bin/buildout: .venv/bin/uv requirements.txt $(wildcard config/*.txt)
	# To really be sure we have the desired setuptools we need to uninstall it first
	.venv/bin/uv pip uninstall setuptools
	# ... and reinstall it later
	.venv/bin/uv pip install -r config/requirements-venv.txt -c config/constraints.txt
	.venv/bin/uv pip install -r requirements.txt
	.venv/bin/uv pip install horse_with_no_namespace

.venv/bin/pip3:
	python3.11 -m venv .venv

.venv/bin/uv: .venv/bin/pip3
	./.venv/bin/pip3 install uv

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


downloads/solr-9.10.1.tgz:
	mkdir -p downloads/
	curl -o downloads/solr-9.10.1.tgz https://dlcdn.apache.org/solr/solr/9.10.1/solr-9.10.1.tgz

solr/server/solr/solr.xml: downloads/solr-9.10.1.tgz
	mkdir -p solr
	tar xvzf downloads/solr-9.10.1.tgz -C solr --strip-components=1
	touch solr/server/solr/solr.xml

solr/server/solr/plone/conf/schema.xml: solr/server/solr/solr.xml
	mkdir -p solr/server/solr/plone
	cd solr/server/solr/plone && ln -sf ../../../../etc/solr/core.properties
	cd solr/server/solr/plone && ln -sf ../../../../etc/solr/conf
	touch solr/server/solr/plone/conf/schema.xml

.PHONY: solr
solr: solr/server/solr/plone/conf/schema.xml
