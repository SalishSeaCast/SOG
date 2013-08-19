"""Unit tests for SOG batch processor.

:Author: Doug Latornell <djl@douglatornell.ca>
:License: Apache License, Version 2.0


Copyright 2010-2013 Doug Latornell and The University of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
try:
    from unittest.mock import (
        mock_open,
        patch,
    )
except ImportError:
    from mock import (
        mock_open,
        patch,
    )
import pytest
from .. import batch_processor


class TestReadConfig():
    """Unit tests for batch_processor.read_config function.
    """
    @patch.object(batch_processor.os.path, 'exists', return_value=False)
    def test_batchfile_not_found(self, mock_os):
        """IOError raised if batchfile doesn't exist
        """
        with pytest.raises(IOError):
            batch_processor.read_config('foo')

    @patch.object(batch_processor.os.path, 'exists', return_value=True)
    def test_returns_config_dict(self, mock_os):
        """config is returned as a dict
        """
        m = mock_open(read_data='foo: bar')
        with patch.object(batch_processor, 'open', m, create=True):
            config = batch_processor.read_config('foo')
        assert config == {'foo': 'bar'}
