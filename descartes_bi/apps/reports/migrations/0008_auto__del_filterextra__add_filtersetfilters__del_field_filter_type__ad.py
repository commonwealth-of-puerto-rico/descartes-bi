# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'FilterExtra'
        db.delete_table(u'reports_filterextra')

        # Adding model 'FiltersetFilters'
        db.create_table(u'reports_filtersetfilters', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filterset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filterset_filters', to=orm['reports.Filterset'])),
            ('filter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Filter'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'reports', ['FiltersetFilters'])

        # Deleting field 'Filter.type'
        db.delete_column(u'reports_filter', 'type')

        # Adding field 'Filter.filter_type'
        db.add_column(u'reports_filter', 'filter_type',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=2),
                      keep_default=False)


        # Changing field 'Filter.description'
        db.alter_column(u'reports_filter', 'description', self.gf('django.db.models.fields.CharField')(default='', max_length=32))

        # Changing field 'Filter.default'
        db.alter_column(u'reports_filter', 'default', self.gf('django.db.models.fields.CharField')(default='', max_length=32))

        # Changing field 'Filter.options'
        db.alter_column(u'reports_filter', 'options', self.gf('django.db.models.fields.TextField')(default=''))

    def backwards(self, orm):
        # Adding model 'FilterExtra'
        db.create_table(u'reports_filterextra', (
            ('filter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Filter'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filterset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Filterset'])),
        ))
        db.send_create_signal(u'reports', ['FilterExtra'])

        # Deleting model 'FiltersetFilters'
        db.delete_table(u'reports_filtersetfilters')


        # User chose to not deal with backwards NULL issues for 'Filter.type'
        raise RuntimeError("Cannot reverse this migration. 'Filter.type' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Filter.type'
        db.add_column(u'reports_filter', 'type',
                      self.gf('django.db.models.fields.CharField')(max_length=2),
                      keep_default=False)

        # Deleting field 'Filter.filter_type'
        db.delete_column(u'reports_filter', 'filter_type')


        # Changing field 'Filter.description'
        db.alter_column(u'reports_filter', 'description', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'Filter.default'
        db.alter_column(u'reports_filter', 'default', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'Filter.options'
        db.alter_column(u'reports_filter', 'options', self.gf('django.db.models.fields.TextField')(null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        },
        u'reports.filter': {
            'Meta': {'ordering': "['name']", 'object_name': 'Filter'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'filter_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'options': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'reports.filterset': {
            'Meta': {'ordering': "['name']", 'object_name': 'Filterset'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'reports.filtersetfilters': {
            'Meta': {'ordering': "['order']", 'object_name': 'FiltersetFilters'},
            'filter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Filter']"}),
            'filterset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filterset_filters'", 'to': u"orm['reports.Filterset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'reports.grouppermission': {
            'Meta': {'object_name': 'GroupPermission'},
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reports.Filter']", 'through': u"orm['reports.GroupPermissionFilterValues']", 'symmetrical': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reports': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Report']", 'null': 'True', 'blank': 'True'})
        },
        u'reports.grouppermissionfiltervalues': {
            'Meta': {'object_name': 'GroupPermissionFilterValues'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'filter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Filter']"}),
            'grouppermission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.GroupPermission']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'reports.menuitem': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Menuitem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reports': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Report']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'reports.report': {
            'Meta': {'ordering': "['title']", 'object_name': 'Report'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'filtersets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Filterset']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'renderer': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'renderer_options': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'reports.reportseries': {
            'Meta': {'object_name': 'ReportSeries'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'properties': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'report_series'", 'to': u"orm['reports.Report']"}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Serie']"})
        },
        u'reports.serie': {
            'Meta': {'ordering': "['name']", 'object_name': 'Serie'},
            'data_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['db_drivers.DataSource']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'tick_format1': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'tick_format2': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'validated_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'validated_person': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'validation_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'reports.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reports.Filter']", 'through': u"orm['reports.UserPermissionFilterValues']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reports': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Report']", 'null': 'True', 'blank': 'True'}),
            'union': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'reports.userpermissionfiltervalues': {
            'Meta': {'object_name': 'UserPermissionFilterValues'},
            'default': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'filter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Filter']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'userpermission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.UserPermission']"})
        }
    }

    complete_apps = ['reports']