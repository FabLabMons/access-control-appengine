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

import webapp2
import ujson


class TagReadHandler(webapp2.RequestHandler):
    def post(self, reader_id):
        event_body = ujson.loads(self.request.body)


        self.response.content_type = 'application/json; charset=utf-8'
        self.response.status_code = 201
        self.response.headers['Location'] = self.request.uri + '/' + '1234'
        self.response.write('Event logged')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/rest/reader/<reader_id>/events', handler=TagReadHandler, name='tag_read')
], debug=True)
