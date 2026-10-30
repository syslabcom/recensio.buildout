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


SOLR_VERSION := 9.11.0
SOLR_ARCHIVE := downloads/solr-$(SOLR_VERSION).tgz
SOLR_INSTALLED := solr/.installed-$(SOLR_VERSION)

$(SOLR_ARCHIVE):
	mkdir -p downloads/
	curl --fail --location --output $@.tmp https://dlcdn.apache.org/solr/solr/$(SOLR_VERSION)/solr-$(SOLR_VERSION).tgz
	mv $@.tmp $@

# A Solr running under supervisor is stopped for the upgrade and started
# again afterwards (also when the upgrade fails). A Solr started by other
# means has to be stopped manually. Never unpack a release over an existing
# installation: versioned JARs from older releases would remain on the
# classpath. Only entries of server/solr/ and server/solr/configsets/ which
# the new release does not ship (e.g. the plone core) are carried over.
# Keep this version in sync with config/solr.cfg (the buildout test instance).
$(SOLR_INSTALLED): $(SOLR_ARCHIVE)
	@set -eu; \
	solr_running() { \
		test -d solr && pgrep -f -- "-Dsolr\.install\.dir=$$(cd solr && pwd -P)( |$$)" >/dev/null; \
	}; \
	stage=; \
	restart=; \
	trap 'rc=$$?; rm -rf "$$stage"; if test -n "$$restart"; then bin/supervisorctl start solr || rc=1; fi; exit $$rc' EXIT; \
	trap 'exit 1' HUP INT TERM; \
	stage=$$(mktemp -d .solr-install.XXXXXX); \
	chmod 755 "$$stage"; \
	tar xzf $(SOLR_ARCHIVE) -C "$$stage" --strip-components=1; \
	test -f "$$stage/server/solr/solr.xml"; \
	test -f "$$stage/server/solr-webapp/webapp/WEB-INF/lib/solr-core-$(SOLR_VERSION).jar"; \
	if solr_running; then \
		if test -x bin/supervisorctl && bin/supervisorctl stop solr; then \
			restart=1; \
		fi; \
		if solr_running; then \
			echo "Solr is running from $$(cd solr && pwd -P) and could not be stopped via bin/supervisorctl. Stop it manually." >&2; \
			exit 1; \
		fi; \
	fi; \
	if test -d solr; then \
		for dir in server/solr server/solr/configsets; do \
			for entry in solr/$$dir/* solr/$$dir/.[!.]* solr/$$dir/..?*; do \
				test -e "$$entry" || test -L "$$entry" || continue; \
				target="$$stage/$${entry#solr/}"; \
				if test -e "$$target" || test -L "$$target"; then continue; fi; \
				cp -a "$$entry" "$$target"; \
			done; \
		done; \
	fi; \
	touch "$$stage/.installed-$(SOLR_VERSION)"; \
	backup=; \
	if test -e solr; then \
		backup=$$(mktemp -d "solr.backup.$$(date +%Y%m%d-%H%M%S).XXXXXX"); \
		rmdir "$$backup"; \
		mv solr "$$backup"; \
	fi; \
	if ! mv "$$stage" solr; then \
		test -z "$$backup" || mv "$$backup" solr; \
		exit 1; \
	fi; \
	test -z "$$backup" || echo "Previous Solr installation preserved in $$backup"

solr/server/solr/solr.xml: $(SOLR_INSTALLED)
	@test -f $@

solr/server/solr/plone/conf/schema.xml: solr/server/solr/solr.xml
	mkdir -p solr/server/solr/plone
	cd solr/server/solr/plone && ln -sf ../../../../etc/solr/core.properties
	cd solr/server/solr/plone && ln -sf ../../../../etc/solr/conf
	touch solr/server/solr/plone/conf/schema.xml

.PHONY: solr
solr: solr/server/solr/plone/conf/schema.xml
