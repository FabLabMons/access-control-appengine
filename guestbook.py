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

import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def reader_key(reader_id):
    """Constructs a Datastore key for a Reader entity.

    We use reader_id as the key.
    """
    return ndb.Key('Reader', reader_id)


class ReaderEvent(ndb.Model):
    """Sub model for representing a reader event."""
    badge = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty()


class Person(ndb.Model):
    """A main model for representing a person."""
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()


class BadgeAssignment(ndb.Model):
    """Sub model for representing a badge assignment to a person.

    A BadgeAssignment's ancestor is a Person.
    """
    rfid = ndb.StringProperty()
    begin = ndb.DateTimeProperty()
    end = ndb.DateTimeProperty()


class MainPage(webapp2.RequestHandler):

    def get(self):
        logout_url = users.create_logout_url(self.request.uri)

        template_values = {
            'logout_url': logout_url
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
], debug=True)
