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

# Stop Solr before upgrading (bin/supervisorctl stop solr), then start it
# again afterwards. Never unpack a release over an existing installation:
# versioned JARs from older releases would remain on the classpath.
# Keep this version in sync with config/solr.cfg (the buildout test instance).
$(SOLR_INSTALLED): $(SOLR_ARCHIVE)
	@set -eu; \
	if test -d solr && pgrep -f -- "-Dsolr\.install\.dir=$$(cd solr && pwd -P)( |$$)" >/dev/null; then \
		echo "Solr is running from $$(cd solr && pwd -P). Stop it first: bin/supervisorctl stop solr" >&2; \
		exit 1; \
	fi; \
	stage=$$(mktemp -d .solr-install.XXXXXX); \
	trap 'rm -rf "$$stage"' EXIT HUP INT TERM; \
	chmod 755 "$$stage"; \
	tar xzf $(SOLR_ARCHIVE) -C "$$stage" --strip-components=1; \
	test -f "$$stage/server/solr/solr.xml"; \
	test -f "$$stage/server/solr-webapp/webapp/WEB-INF/lib/solr-core-$(SOLR_VERSION).jar"; \
	if test -d solr; then \
		for entry in solr/server/solr/* solr/server/solr/.[!.]* solr/server/solr/..?*; do \
			test -e "$$entry" || test -L "$$entry" || continue; \
			case "$${entry##*/}" in solr.xml|configsets|README*) continue ;; esac; \
			cp -a "$$entry" "$$stage/server/solr/"; \
		done; \
		if test -d solr/server/solr/configsets; then \
			cp -a solr/server/solr/configsets/. "$$stage/server/solr/configsets/"; \
		fi; \
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
