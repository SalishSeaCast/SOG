# Makefile for SOG Code Development & Run Environment

HG_REPOS     = /ocean/sallen/hg_repos
PROJECT_NAME = SOG-project
BUILDBOT_VERSION = 0.8.1
BUILDBOT_ENV = /ocean/dlatorne/.virtualenvs/buildbot-$(BUILDBOT_VERSION)
PYTHON = /usr/local/python26/bin/python

.PHONY:	help env patch_hgrc project

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  env      to make a full SOG environment"
	@echo "  project  to make a new project directory for running SOG"
	@echo "  patch_hgrc  patch hgrc files so pushes to ocean trigger buildbot"
	@echo ""
	@echo "Change hg repository source with \`make env HG_REPOS=<path>'"
	@echo "where <path> defaults to $(HG_REPOS)"
	@echo ""
	@echo "Set new project name with \`make project PROJECT_NAME=<name>'"
	@echo "where <name> defaults to $(PROJECT_NAME)"

env:
	hg clone $(HG_REPOS)/SOG-code SOG-code-ocean
	hg clone SOG-code-ocean SOG-code-dev
	hg clone $(HG_REPOS)/SOG-initial
	hg clone $(HG_REPOS)/SOG-forcing
	make patch-hgrc
	make project PROJECT_NAME=SOG-test/SOG-ocean-`date "+%Y-%m-%d"`
	make project PROJECT_NAME=SOG-test/SOG-dev-`date "+%Y-%m-%d"`
	make project

patch-hgrc:
	$(PYTHON) patch_hgrc.py .hg/hgrc $(BUILDBOT_VERSION)
	$(PYTHON) patch_hgrc.py SOG-code-ocean/.hg/hgrc $(BUILDBOT_VERSION)
	$(PYTHON) patch_hgrc.py SOG-initial/.hg/hgrc $(BUILDBOT_VERSION)
	$(PYTHON) patch_hgrc.py SOG-forcing/.hg/hgrc $(BUILDBOT_VERSION)

project:
	mkdir -p $(PROJECT_NAME)/profiles $(PROJECT_NAME)/timeseries
