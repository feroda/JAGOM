# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 BeFair s.n.c <www.befair.it>
# 
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://trac.edgewall.org/wiki/TracLicense.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://trac.edgewall.org/log/.
#
# Author: Luca Ferroni <fero@jagom.org>

from fnmatch import fnmatch
from itertools import groupby
import os

from trac.core import *
from trac.config import Option
from trac.web.api import IAuthenticator
from trac.util.text import to_unicode

import datetime, base64
try:
    import cPickle as pickle
except ImportError:
    import pickle

sqlite3 = None
try:
    import sqlite3
except ImportError:
    pass

class DjangoLogin(Component):
    """Authenticate versus a Django sessions table.

    Now it works only with sqlite Django db.
    Needs sqlite3 module.
    
    === Installation ===
    
    Enabling this plugin requires listing it in `trac.ini:
    {{{
    [django_login]
    django_db = /path/to/django/sqlite.db
    }}}
    
    """
    implements(IAuthenticator)

    django_db = Option('django_login', 'django_db', None,
                        'Location of django sqlite db file.')

    AUTHID_SESSION_KEY = '_auth_user_id'

    # IAuthenticator methods
    
    def authenticate(self, req):

        if sqlite3 is None:
            self.log.error('sqlite3 package not found')
            return None

        authname = None
        if req.incookie.has_key('sessionid'):
            cookie = req.incookie['sessionid']
            db = sqlite3.connect(self.django_db)
            cursor = db.cursor()
            cursor.execute("SELECT session_data FROM django_session "
                           "WHERE session_key=? AND expire_date > ?",
                           (cookie.value, datetime.datetime.now()))
            row = cursor.fetchone()
            if row:
                session_dict = self._decode_django_session_data(row[0])
                if self.AUTHID_SESSION_KEY in session_dict:
                    django_user_id = session_dict[self.AUTHID_SESSION_KEY]
                    cursor.execute("SELECT username FROM auth_user where id=?", (django_user_id,))
                    authname = cursor.fetchone()[0]

                else:
                    authname = None

            else:
#                # The cookie is invalid (or has been purged from the database), so
#                # tell the user agent to drop it as it is invalid
#                self._expire_cookie(req)
                authname = None

        return authname

    def _decode_django_session_data(self, session_data):
        encoded_data = base64.decodestring(session_data)
        pickled, tamper_check = encoded_data[:-32], encoded_data[-32:]
#        if md5_constructor(pickled + settings.SECRET_KEY).hexdigest() != tamper_check:
#            raise SuspiciousOperation("User tampered with session cookie.")
        try:
            return pickle.loads(pickled)
        # Unpickling can cause a variety of exceptions. If something happens,
        # just return an empty dictionary (an empty session).
        except:
            return {}

