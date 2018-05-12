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

import webtest

import rest


def post_reader_event():
    app = webtest.TestApp(rest.app)
    response = app.post('/rest/reader/123a456b/events')
    return response


def test_post_content_type():
    response = post_reader_event()

    assert response.content_type == 'application/json'


def test_post_charset():
    response = post_reader_event()

    assert response.charset == 'utf-8'


def test_post_status():
    response = post_reader_event()

    assert response.status_int == 201


def test_post_location():
    response = post_reader_event()

    assert response.headers['Location'] == 'http://localhost/rest/reader/123a456b/events/1234'
