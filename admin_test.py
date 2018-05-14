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
import unittest
import webtest
from google.appengine.ext import testbed, ndb

import admin
from model import TagEvent, tag_reader_key


class AdminTest(unittest.TestCase):

    def setUp(self):
        self.testapp = webtest.TestApp(admin.app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def testGet(self):
        reader_key = tag_reader_key(1234)
        TagEvent(timestamp=datetime.datetime.now(), tag_id='243F4AD56', parent=reader_key).put()
        TagEvent(timestamp=datetime.datetime.now(), tag_id='465AEA477', parent=reader_key).put()
        TagEvent(timestamp=datetime.datetime.now(), tag_id='243F4AD56', parent=reader_key).put()

        response = self.testapp.get('/admin/lastEvents')
        self.assertEqual(200, response.status_int)


if __name__ == '__main__':
    unittest.main()
