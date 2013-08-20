# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Server'
        db.create_table(u'db_drivers_server', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('backend', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'db_drivers', ['Server'])

        # Deleting field 'DataSource.port'
        db.delete_column(u'db_drivers_datasource', 'port')

        # Deleting field 'DataSource.host'
        db.delete_column(u'db_drivers_datasource', 'host')

        # Deleting field 'DataSource.password'
        db.delete_column(u'db_drivers_datasource', 'password')

        # Deleting field 'DataSource.user'
        db.delete_column(u'db_drivers_datasource', 'user')

        # Deleting field 'DataSource.backend'
        db.delete_column(u'db_drivers_datasource', 'backend')

        # Adding field 'DataSource.server'
        db.add_column(u'db_drivers_datasource', 'server',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['db_drivers.Server']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Server'
        db.delete_table(u'db_drivers_server')

        # Adding field 'DataSource.port'
        db.add_column(u'db_drivers_datasource', 'port',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DataSource.host'
        db.add_column(u'db_drivers_datasource', 'host',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'DataSource.password'
        db.add_column(u'db_drivers_datasource', 'password',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'DataSource.user'
        db.add_column(u'db_drivers_datasource', 'user',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'DataSource.backend'
        raise RuntimeError("Cannot reverse this migration. 'DataSource.backend' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'DataSource.backend'
        db.add_column(u'db_drivers_datasource', 'backend',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)

        # Deleting field 'DataSource.server'
        db.delete_column(u'db_drivers_datasource', 'server_id')


    models = {
        u'db_drivers.datasource': {
            'Meta': {'ordering': "['label']", 'object_name': 'DataSource'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['db_drivers.Server']"})
        },
        u'db_drivers.server': {
            'Meta': {'ordering': "['label']", 'object_name': 'Server'},
            'backend': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        }
    }

    complete_apps = ['db_drivers']