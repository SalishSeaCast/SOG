# Makefile for Sphinx documentation
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


# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = _build
EOS_HOST	  = sable

# Internal variables.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .
EOS_WEB = /home/sallen/public_html/SOG-docs/

.PHONY: help clean html

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  rsync-eos  to rsync HTML files to EOS public web space"

clean:
	-rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

rsync-eos:
	chmod -R g+w _build/html
	rsync -rlpgoDvhz _build/html/ $(EOS_HOST):$(EOS_WEB)
	@echo "rsync to EOS public web complete."
