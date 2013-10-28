"""
LIBRE database backend for Django.

#Each of these API functions, except connection.close(), raises
#ImproperlyConfigured.
"""
import logging

from django.core.exceptions import ImproperlyConfigured
from django.db.backends import (BaseDatabaseOperations,
    BaseDatabaseClient, BaseDatabaseIntrospection, BaseDatabaseWrapper,
    BaseDatabaseFeatures, BaseDatabaseValidation)
from django.db.backends.creation import BaseDatabaseCreation

import requests

logger = logging.getLogger(__name__)


def complain(*args, **kwargs):
    raise ImproperlyConfigured("settings.DATABASES is improperly configured. "
                               "Please supply the ENGINE value. Check "
                               "settings documentation for more details.")


def ignore(*args, **kwargs):
    pass


class DatabaseError(Exception):
    pass


class IntegrityError(DatabaseError):
    pass


class DatabaseOperations(BaseDatabaseOperations):
    quote_name = complain
    #def quote_name(self, name):
    #    if name.startswith('"') and name.endswith('"'):
    #        return name # Quoting once is enough.
    #    return '"%s"' % name


class DatabaseClient(BaseDatabaseClient):
    # Not used by the LIBRE driver
    runshell = complain


class DatabaseCreation(BaseDatabaseCreation):
    create_test_db = ignore
    destroy_test_db = ignore


class DatabaseIntrospection(BaseDatabaseIntrospection):
    get_table_list = complain
    get_table_description = complain
    get_relations = complain
    get_indexes = complain
    get_key_columns = complain


class Cursor():
    # TODO: Add support for LIBRE query errors
    # Capture and decode LIBRE HTTP 400 errors

    def __init__(self, host, name, port, user, password):
        self.url = '%(schema)s%(host)s:%(port)d/api/sources/%(name)s/data' % {
            'schema': 'http://',
            'host': host,
            'port': port or 80,
            'name': name
        }
        self.user = user
        self.password = password

    def execute(self, query, params=()):
        #TODO: In case we support kwargs bases query and params
        # query_string = '&'.join(['%s=%s' % (filter, value) for filter, value in query.items()])

        query_string = query % params

        self.query_url = ''.join([self.url, '?', query_string, '&_format=json'])
        # TODO: use proper URL fabrication
        if self.user and self.password:
            self.response = requests.get(self.query_url, auth=(self.user, self.password))
        else:
            self.response = requests.get(self.query_url)

        logger.debug('query_url: %s' % self.query_url)
        logger.debug('status_code: %s' % self.response.status_code)

    def fetchall(self):
        return self.response.json()


class DatabaseWrapper(BaseDatabaseWrapper):
    operators = {}
    # Override the base class implementations with null
    # implementations. Anything that tries to actually
    # do something raises complain; anything that tries
    # to rollback or undo something raises ignore.
    _commit = complain
    _rollback = ignore
    enter_transaction_management = complain
    leave_transaction_management = ignore
    set_dirty = complain
    set_clean = complain
    commit_unless_managed = complain
    rollback_unless_managed = ignore
    savepoint = ignore
    savepoint_commit = complain
    savepoint_rollback = ignore
    close = ignore

    def cursor(self):
        return Cursor(self.settings_dict.get('HOST'), self.settings_dict.get('NAME'), self.settings_dict.get('PORT'), self.settings_dict.get('USER'), self.settings_dict.get('PASSWORD'))

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)

        self.features = BaseDatabaseFeatures(self)
        self.ops = DatabaseOperations(self)
        self.client = DatabaseClient(self)
        self.creation = DatabaseCreation(self)
        self.introspection = DatabaseIntrospection(self)
        self.validation = BaseDatabaseValidation(self)
