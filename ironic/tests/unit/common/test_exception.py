#    Copyright (c) 2015 IBM, Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
import six

from ironic.common import exception
from ironic.tests import base


class DeprecatedException(exception.IronicException):
    message = 'Using message is deprecated %(foo)s'


class TestIronicException(base.TestCase):
    def test____init__(self):
        expected = b'\xc3\xa9\xe0\xaf\xb2\xe0\xbe\x84'
        if six.PY3:
            expected = expected.decode('utf-8')
            message = chr(233) + chr(0x0bf2) + chr(3972)
        else:
            message = unichr(233) + unichr(0x0bf2) + unichr(3972)
        exc = exception.IronicException(message)
        self.assertEqual(expected, exc.__str__())

    @mock.patch.object(exception.LOG, 'warning', autospec=True)
    def test_message_deprecated(self, mock_logw):
        exc = DeprecatedException(foo='spam')
        mock_logw.assert_called_once_with(
            "Exception class: %s Using the 'message' "
            "attribute in an exception has been deprecated. The exception "
            "class should be modified to use the '_msg_fmt' attribute.",
            'DeprecatedException')
        self.assertEqual('Using message is deprecated spam', str(exc))
