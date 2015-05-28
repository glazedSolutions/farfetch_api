#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Farfetch API
# Copyright (C) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Farfetch API.
#
# Hive Farfetch API is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Farfetch API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Farfetch API. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import appier

from . import product

BASE_URL = "https://publicapi.farfetch.com/v1/"
""" The default base url to be used when no other
base url value is provided to the constructor """

AUTH_URL = "https://publicapi.farfetch.com/authentication"
""" The complete url for the authentication process
and retrieval of (authentication) token """

class Api(
    appier.Api,
    product.ProductApi
):

    def __init__(self, *args, **kwargs):
        appier.Api.__init__(self, *args, **kwargs)
        self.base_url = appier.conf("FF_BASE_URL", BASE_URL)
        self.auth_url = appier.conf("FF_AUTH_URL", AUTH_URL)
        self.client_id = appier.conf("FF_CLIENT_ID", None)
        self.client_secret = appier.conf("FF_CLIENT_SECRET", None)
        self.base_url = kwargs.get("base_url", self.base_url)
        self.auth_url = kwargs.get("auth_url", self.auth_url)
        self.client_id = kwargs.get("client_id", self.client_id)
        self.client_secret = kwargs.get("client_secret", self.client_secret)
        self.token = kwargs.get("token", None)

    def build(self, method, url, headers, kwargs):
        auth = kwargs.get("auth", True)
        if auth: headers["Authentication"] = self.get_token()

    def get_token(self):
        if self.token: return self.token
        contents = self.post(
            self.auth_url,
            auth = False,
            grant_type = "client_credentials",
            scope = "api",
            client_id = self.client_id,
            client_secret = self.client_secret
        )
        token_type = contents["token_type"]
        access_token = contents["access_token"]
        self.token = "%s %s" % (token_type, access_token)
        return self.token
