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

from model import tag_reader_key, TagEvent


class LogEventHandler(webapp2.RequestHandler):
    def post(self, reader_id):
        event_json = self.request.json
        timestamp = datetime.datetime.fromtimestamp(event_json['timestamp'], tz=None)
        event = TagEvent(tag_id=event_json['tag_id'], timestamp=timestamp, parent=tag_reader_key(reader_id))
        event.put()

        self.response.status_int = 201
        self.response.location = "{}/{}".format(self.request.uri, event.key.id())
        self.response.write('Event logged')


class LogEventDisplayHandler(webapp2.RequestHandler):
    def get(self):
        events = TagEvent.query_last().fetch(20)
        stringified_events = map(lambda event: {
            'tag_id': event.tag_id,
            'timestamp': event.timestamp.isoformat(),
            'reader': event.key.parent().id()
        }, events)

        self.response.status_int = 200
        self.response.content_type = "application/json"
        self.response.charset = "utf-8"
        self.response.json = {'data': stringified_events}


app = webapp2.WSGIApplication([
    webapp2.Route(r'/rest/readers/<reader_id>/events', handler=LogEventHandler, name='tag_read'),
    webapp2.Route(r'/rest/lastEvents', handler=LogEventDisplayHandler, name='tag_read')
], debug=True)
