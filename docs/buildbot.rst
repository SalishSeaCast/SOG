.. :Author: Doug Latornell <djl@douglatornell.ca>
.. :License: Apache License, Version 2.0
..
..
.. Copyright 2010-2014 Doug Latornell and The University of British Columbia
..
.. Licensed under the Apache License, Version 2.0 (the "License");
.. you may not use this file except in compliance with the License.
.. You may obtain a copy of the License at
..
..    http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.


.. _SOGbuildbot-section:

SOG buildbot Automated Testing System
=====================================

Development of SOG is supported by a buildbot_ installation on a
collection of the :kbd:`ocean` machines. Buildbot runs the code with a
variety of input files and compares the results to stored reference
results files. This serves to check that changes made in one area of
the code do not cause the model to break horribly for other
scenarios. The builds also produce timeseries graphs of key model
variables that compare the build results to the reference results.

.. _buildbot: http://buildbot.net/

A limited set of builds are triggered to run 20 minutes after the last
push of changes to any of the 4 repositories (:file:`SOG`,
:file:`SOG-code`, :file:`SOG-initial`, :file:`SOG-forcing`). A more
extensive set of builds run at night on any day when there have been
commits to any of the 4 repositories. The same set of builds is run
early every Saturday morning, whether or not there have been commits
during the preceding week. This provides a check that the buildbot
system is functional, and confirms that changes in the :kbd:`ocean`
machines operating system, configuration, or other platform issues
have not broken SOG.

The web interface to the SOG buildbot is at
http://bjossa.eos.ubc.ca:8010/ and the its operation and configuration
is documented at http://bjossa.eos.ubc.ca:8010/docs/. It is also
included in the :ref:`SOGtrac-section`:.

You can follow the buildbot's activities by subscribing to its
Atom/RSS feed, or via an email list. See the docs for details.

.. _docs: http://bjossa.eos.ubc.ca:8010/docs/

..
  Local variables:
  mode: rst
  End:
