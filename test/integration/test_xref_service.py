#!/usr/bin/env python
from __future__ import absolute_import
import os
import unittest

import boto3

from xref_service import xref_service

dynamodb_host = os.environ.get('DYNAMODB_HOST', 'localhost')
dynamodb_table = os.environ.get('DYNAMODB_TABLE', 'xref-service')

dynamodb = boto3.resource('dynamodb', endpoint_url='http://{}:8000'.format(
    dynamodb_host
))

table = dynamodb.Table(dynamodb_table)


class TestGet(unittest.TestCase):
    results = {'global': '726c64bb-c7b2-457a-907f-207735b03262',
               'tp': '2930', 'm3': '480288'}

    def test_get_by_global_id(self):
        global_system_object = {'system': 'global',
                                'id': '726c64bb-c7b2-457a-907f-207735b03262'}
        self.assertEqual(xref_service.get_ids(table, global_system_object),
                         self.results)

    def test_get_by_system_id(self):
        system_object = {'system': 'tp', 'id': '2930'}
        self.assertEqual(xref_service.get_ids(table, system_object),
                         self.results)


if __name__ == '__main__':
    unittest.main()
