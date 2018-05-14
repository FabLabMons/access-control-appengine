#!/usr/bin/env python

# Copyright 2018 FabLabMons.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import time
import json
import unittest
import webtest
from google.appengine.ext import testbed, ndb

import rest


class RestTest(unittest.TestCase):

    def setUp(self):
        self.testapp = webtest.TestApp(rest.app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def testLogTagHandler(self):
        localtimestamp = time.strptime(r'2018-05-14T13:19:17', '%Y-%m-%dT%H:%M:%S')
        event_log = {
            'timestamp': time.mktime(localtimestamp),
            'tag_id': '243F4AD56',
            'signature': '9234E84CBA42'
        }
        event = json.dumps(event_log)

        response = self.testapp.post('/rest/reader/123a456b/events', event)
        self.assertEqual(201, response.status_int)
        query = rest.TagEvent.query()
        results = query.fetch(2)
        self.assertEqual(1, len(results))
        self.assertEqual('Reader', results[0].key.parent().kind())
        self.assertEqual('123a456b', results[0].key.parent().id())
        self.assertEqual('243F4AD56', results[0].tag_id)
        self.assertEqual(localtimestamp, results[0].timestamp.timetuple())
        self.assertEqual('http://localhost/rest/reader/123a456b/events/{}'.format(results[0].key.id()),
                         response.headers['Location'])


if __name__ == '__main__':
    unittest.main()
