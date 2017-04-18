#!/usr/bin/env python
from __future__ import absolute_import
import unittest

from mock import patch

from xref_service import xref_service


class TestGet(unittest.TestCase):
    results = {'global': 'foobar', 'foo-system': 'foo', 'bar-system': 'bar'}

    @patch('xref_service.xref_service._get_by_global_id', return_value=results)
    def test_get_by_global_id(self, mock_get_global_id):
        global_system_object = {'system': 'global', 'id': 'foobar'}
        self.assertEqual(xref_service.get_ids('table', global_system_object),
                         self.results)
        mock_get_global_id.assert_called_once_with('table', 'foobar')

    @patch('xref_service.xref_service._get_by_system_id', return_value=results)
    def test_get_by_system_id(self, mock_get_system_id):
        system_object = {'system': 'foo-system', 'id': 'foo'}
        self.assertEqual(xref_service.get_ids('table', system_object),
                         self.results)
        mock_get_system_id.assert_called_once_with('table', system_object)


if __name__ == '__main__':
    unittest.main()
