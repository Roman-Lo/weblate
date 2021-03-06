# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2017 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from unittest import TestCase

from django.http import HttpRequest
from django.test.utils import override_settings

import httpretty

from weblate.utils.antispam import is_spam
import weblate.trans.tests.mypretty  # noqa


class SpamTest(TestCase):
    @override_settings(AKISMET_API_KEY=None)
    def test_disabled(self):
        self.assertFalse(is_spam('text', HttpRequest()))

    def mock_akismet(self, body):
        httpretty.register_uri(
            httpretty.POST,
            'https://key.rest.akismet.com/1.1/comment-check',
            body=body,
        )
        httpretty.register_uri(
            httpretty.POST,
            'https://rest.akismet.com/1.1/verify-key',
            body='valid',
        )

    @httpretty.activate
    @override_settings(AKISMET_API_KEY='key')
    def test_akismet_spam(self):
        self.mock_akismet('true')
        self.assertTrue(is_spam('text', HttpRequest()))

    @httpretty.activate
    @override_settings(AKISMET_API_KEY='key')
    def test_akismet_nospam(self):
        self.mock_akismet('false')
        self.assertFalse(is_spam('text', HttpRequest()))
