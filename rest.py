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

import webapp2
from google.appengine.ext import ndb


def tag_reader_key(reader_id):
    return ndb.Key('Reader', reader_id)


class TagEvent(ndb.Model):
    tag_id = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty()


class LogTagHandler(webapp2.RequestHandler):
    def post(self, reader_id):
        event_json = self.request.json
        timestamp = datetime.datetime.fromtimestamp(event_json['timestamp'], tz=None)
        event = TagEvent(tag_id=event_json['tag_id'], timestamp=timestamp, parent=tag_reader_key(reader_id))
        event.put()

        self.response.status_code = 201
        self.response.headers['Location'] = "{}/{}".format(self.request.uri, event.key.id())
        self.response.write('Event logged')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/rest/reader/<reader_id>/events', handler=LogTagHandler, name='tag_read')
], debug=True)
