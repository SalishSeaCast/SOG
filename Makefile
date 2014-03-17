# Makefile for SOG Run & Code Development Environment
#
# :Author: Doug Latornell <djl@douglatornell.ca>
# :License: Apache License, Version 2.0
#
#
# Copyright 2010-2014 Doug Latornell and The University of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
	make project PROJECT_NAME=SOG-test/SOG-ocean-`date "+%Y-%m-%d"`
	make project PROJECT_NAME=SOG-test/SOG-dev-`date "+%Y-%m-%d"`
	(cd SOG-test && ln -s ../SOG-initial SOG-initial)
	(cd SOG-test && ln -s ../SOG-forcing SOG-forcing)
	make project

project:
	mkdir -p $(PROJECT_NAME)/profiles $(PROJECT_NAME)/timeseries
