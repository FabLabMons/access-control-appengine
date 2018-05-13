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

from google.appengine.ext import ndb
from google.appengine.ext import testbed
import json
import unittest
import webtest

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
        event_log = {
            'timestamp': '2018-05-12T10:25:32Z',
            'tag_id': '243F4AD56',
            'signature': '9234E84CBA42'
        }
        event = json.dumps(event_log)

        response = self.testapp.post('/rest/reader/123a456b/events', event)
        self.assertEquals(201, response.status_int)
        self.assertEquals('http://localhost/rest/reader/123a456b/events/1234', response.headers['Location'])
        query = rest.TagEvent.query()
        results = query.fetch(2)
        self.assertEquals(1, len(results))


if __name__ == '__main__':
    unittest.main()
