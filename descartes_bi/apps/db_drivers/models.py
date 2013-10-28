from django.conf import settings
from django.db import models, load_backend as django_load_backend
from django.utils.translation import ugettext_lazy as _

BACKEND_POSTGRESQL_PSYCOPG2 = 1
BACKEND_POSTGRESQL = 2
BACKEND_MYSQL = 3
BACKEND_SQLITE3 = 4
BACKEND_ORACLE = 5
BACKEND_LIBRE = 6

BACKEND_CHOICES = (
    (BACKEND_POSTGRESQL_PSYCOPG2, _('PostgreSQL (psycopg2)')),
    (BACKEND_POSTGRESQL, _('PostgreSQL')),
    (BACKEND_MYSQL, _('MySQL')),
    (BACKEND_SQLITE3, _('SQLite')),
    (BACKEND_ORACLE, _('Oracle')),
    (BACKEND_LIBRE, _('LIBRE')),
)

BACKEND_CLASSES = {
    BACKEND_POSTGRESQL_PSYCOPG2: 'django.db.backends.postgresql_psycopg2',
    BACKEND_POSTGRESQL: 'django.db.backends.postgresql',
    BACKEND_MYSQL: 'django.db.backends.mysql',
    BACKEND_SQLITE3: 'django.db.backends.sqlite3',
    BACKEND_ORACLE: 'django.db.backends.oracle',
    BACKEND_LIBRE: 'libre_driver.backend',
}


class Server(models.Model):
    label = models.CharField(max_length=128, verbose_name=_('label'), help_text=_('A text by which this server will be identified.'))
    backend = models.PositiveIntegerField(choices=BACKEND_CHOICES, verbose_name=_('database backend'))
    user = models.CharField(max_length=64, blank=True, verbose_name=_('user'), help_text=_('Not used with sqlite3.'))
    password = models.CharField(max_length=64, blank=True, verbose_name=_('password'), help_text=_('Not used with sqlite3.'))
    host = models.CharField(max_length=64, blank=True, verbose_name=_('host'), help_text=_('Set to empty string for localhost. Not used with sqlite3.'))
    port = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('port'))

    def __unicode__(self):
        return self.label

    class Meta:
        ordering = ['label']
        verbose_name = _('server')
        verbose_name_plural = _('servers')


class DataSource(models.Model):
    label = models.CharField(max_length=128, verbose_name=_('label'), help_text=_('A text by which this data source will be identified.'))
    server = models.ForeignKey(Server, verbose_name=_('server'))
    name = models.CharField(max_length=128, blank=True, verbose_name=_('name'), help_text=_('Name or path to database.'))

    def load_backend(self):
        database_settings = {}

        database_settings['ENGINE'] = BACKEND_CLASSES[self.server.backend]
        database_settings.setdefault('OPTIONS', {})
        database_settings.setdefault('TIME_ZONE', 'UTC' if settings.USE_TZ else settings.TIME_ZONE)
        database_settings['NAME'] = self.name
        database_settings['USER'] = self.server.user
        database_settings['PASSWORD'] = self.server.password
        database_settings['HOST'] = self.server.host
        database_settings['PORT'] = self.server.port if self.server.port else ''

        backend = django_load_backend(database_settings['ENGINE'])
        connection = backend.DatabaseWrapper(database_settings, 'data_source')

        return connection

    def __unicode__(self):
        return self.label

    @property
    def backend(self):
        return self.server.backend

    class Meta:
        ordering = ['label']
        verbose_name = _('data source')
        verbose_name_plural = _('data sources')
