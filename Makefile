# Makefile for SOG Code Development & Run Environment

HG_REPOS     = /ocean/sallen/hg_repos
PROJECT_NAME = SOG-project
BUILDBOT_ENV = /ocean/dlatorne/.virtualenvs/buildbot-0.8.1
HG_REMOTECMD = \\n[ui]\\nremotecmd = $(BUILDBOT_ENV)/bin/hg

.PHONY:	help env project

help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  env      to make a full SOG environment"
	@echo "  project  to make a new project directory for running SOG"
	@echo ""
	@echo "Change hg repository source with \`make env HG_REPOS=<path>'"
	@echo "where <path> defaults to $(HG_REPOS)"
	@echo ""
	@echo "Set new project name with \`make project PROJECT_NAME=<name>'"
	@echo "where <name> defaults to $(PROJECT_NAME)"

env:
	echo $(HG_REMOTECMD) >> .hg/hgrc
	hg clone $(HG_REPOS)/SOG-code SOG-code-ocean
	echo $(HG_REMOTECMD) >> SOG-code-ocean/.hg/hgrc
	hg clone SOG-code-ocean SOG-code-dev
	hg clone $(HG_REPOS)/SOG-initial
	echo $(HG_REMOTECMD) >> SOG-initial/.hg/hgrc
	hg clone $(HG_REPOS)/SOG-forcing
	echo $(HG_REMOTECMD) >> SOG-forcing/.hg/hgrc
	make project

project:
	mkdir -p $(PROJECT_NAME)/profiles $(PROJECT_NAME)/timeseries
