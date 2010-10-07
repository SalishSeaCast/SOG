# Makefile for SOG Code Development & Run Environment

HG_REPOS     = /ocean/sallen/hg_repos
PROJECT_NAME = SOG-project

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
	hg clone $(HG_REPOS)/SOG-code SOG-code-ocean
	hg clone SOG-code-ocean SOG-code-dev
	hg clone $(HG_REPOS)/SOG-initial
	hg clone $(HG_REPOS)/SOG-forcing

project:
	mkdir -p $(PROJECT_NAME)/profiles $(PROJECT_NAME)/timeseries
