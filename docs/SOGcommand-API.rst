.. :Author: Doug Latornell <djl@douglatornell.ca>
.. :License: Apache License, Version 2.0
..
..
.. Copyright 2010-2013 Doug Latornell and The University of British Columbia
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


.. _SOG_CommandProcessorAPI-section:

SOG Command Processor API
=========================

This section documents the SOG command processor
Application Programming Interface (API).
The API allows software that runs :program:`SOG`
(e.g. :program:`SoG-bloomcast`)
so that :program:`SOG` commands can be used dirctly,
rather than by way of a subprocess.

.. autofunction:: SOGcommand.api.batch

.. autofunction:: SOGcommand.api.read_infile

.. autofunction:: SOGcommand.api.run
