#!/usr/bin/env python
from __future__ import absolute_import
import os
import unittest

import requests

service_endpoint = os.environ['SERVICE_ENDPOINT']
service_name = os.environ.get('SERVICE_NAME', 'xref-service')


class TestPost(unittest.TestCase):
    def test_create_new_global_id_returns_just_global_id(self):
        new_global_id_path = '/global'
        url = service_endpoint + '/' + service_name + new_global_id_path
        r = requests.post(url, data={})
        self.assertEqual(type(r.json()), type({}))
        self.assertTrue('global' in r.json())
        self.assertEqual(len(r.json()), 1)


if __name__ == '__main__':
    unittest.main()
