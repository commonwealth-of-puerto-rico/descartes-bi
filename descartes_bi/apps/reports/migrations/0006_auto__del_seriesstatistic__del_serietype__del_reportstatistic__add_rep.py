# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SeriesStatistic'
        db.delete_table(u'reports_seriesstatistic')

        # Deleting model 'SerieType'
        db.delete_table(u'reports_serietype')

        # Deleting model 'ReportStatistic'
        db.delete_table(u'reports_reportstatistic')

        # Adding model 'ReportSeries'
        db.create_table(u'reports_reportseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='report_series', to=orm['reports.Report'])),
            ('series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Serie'])),
            ('properties', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'reports', ['ReportSeries'])

        # Deleting field 'Report.tracking'
        db.delete_column(u'reports_report', 'tracking')

        # Deleting field 'Report.highlighter'
        db.delete_column(u'reports_report', 'highlighter')

        # Deleting field 'Report.pointlabels_location'
        db.delete_column(u'reports_report', 'pointlabels_location')

        # Deleting field 'Report.legend_location'
        db.delete_column(u'reports_report', 'legend_location')

        # Deleting field 'Report.zoom'
        db.delete_column(u'reports_report', 'zoom')

        # Deleting field 'Report.trendline'
        db.delete_column(u'reports_report', 'trendline')

        # Deleting field 'Report.legend'
        db.delete_column(u'reports_report', 'legend')

        # Deleting field 'Report.pointlabels'
        db.delete_column(u'reports_report', 'pointlabels')

        # Deleting field 'Report.use_one_scale'
        db.delete_column(u'reports_report', 'use_one_scale')

        # Deleting field 'Report.scale_label_override'
        db.delete_column(u'reports_report', 'scale_label_override')

        # Deleting field 'Report.type'
        db.delete_column(u'reports_report', 'type')

        # Deleting field 'Report.orientation'
        db.delete_column(u'reports_report', 'orientation')

        # Adding field 'Report.renderer'
        db.add_column(u'reports_report', 'renderer',
                      self.gf('django.db.models.fields.TextField')(default=1),
                      keep_default=False)

        # Adding field 'Report.renderer_options'
        db.add_column(u'reports_report', 'renderer_options',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'Serie.avg_execution_time'
        db.delete_column(u'reports_serie', 'avg_execution_time')

        # Deleting field 'Serie.last_execution_time'
        db.delete_column(u'reports_serie', 'last_execution_time')


    def backwards(self, orm):
        # Adding model 'SeriesStatistic'
        db.create_table(u'reports_seriesstatistic', (
            ('execution_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('serie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Serie'])),
            ('params', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'reports', ['SeriesStatistic'])

        # Adding model 'SerieType'
        db.create_table(u'reports_serietype', (
            ('zerobase', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('serie', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Serie'])),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Report'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='BA', max_length=2)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'reports', ['SerieType'])

        # Adding model 'ReportStatistic'
        db.create_table(u'reports_reportstatistic', (
            ('execution_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('params', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Report'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'reports', ['ReportStatistic'])

        # Deleting model 'ReportSeries'
        db.delete_table(u'reports_reportseries')

        # Adding field 'Report.tracking'
        db.add_column(u'reports_report', 'tracking',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Report.highlighter'
        db.add_column(u'reports_report', 'highlighter',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Report.pointlabels_location'
        db.add_column(u'reports_report', 'pointlabels_location',
                      self.gf('django.db.models.fields.CharField')(default='n', max_length=2),
                      keep_default=False)

        # Adding field 'Report.legend_location'
        db.add_column(u'reports_report', 'legend_location',
                      self.gf('django.db.models.fields.CharField')(default='ne', max_length=2),
                      keep_default=False)

        # Adding field 'Report.zoom'
        db.add_column(u'reports_report', 'zoom',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Report.trendline'
        db.add_column(u'reports_report', 'trendline',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Report.legend'
        db.add_column(u'reports_report', 'legend',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Report.pointlabels'
        db.add_column(u'reports_report', 'pointlabels',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Report.use_one_scale'
        db.add_column(u'reports_report', 'use_one_scale',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Report.scale_label_override'
        db.add_column(u'reports_report', 'scale_label_override',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Report.type'
        db.add_column(u'reports_report', 'type',
                      self.gf('django.db.models.fields.CharField')(default='SI', max_length=2),
                      keep_default=False)

        # Adding field 'Report.orientation'
        db.add_column(u'reports_report', 'orientation',
                      self.gf('django.db.models.fields.CharField')(default='v', max_length=1),
                      keep_default=False)

        # Deleting field 'Report.renderer'
        db.delete_column(u'reports_report', 'renderer')

        # Deleting field 'Report.renderer_options'
        db.delete_column(u'reports_report', 'renderer_options')

        # Adding field 'Serie.avg_execution_time'
        db.add_column(u'reports_serie', 'avg_execution_time',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Serie.last_execution_time'
        db.add_column(u'reports_serie', 'last_execution_time',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)


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
            'default': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'options': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'reports.filterextra': {
            'Meta': {'object_name': 'FilterExtra'},
            'filter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Filter']"}),
            'filterset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Filterset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'reports.filterset': {
            'Meta': {'ordering': "['name']", 'object_name': 'Filterset'},
            'filters': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reports.Filter']", 'through': u"orm['reports.FilterExtra']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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
            'renderer': ('django.db.models.fields.TextField', [], {}),
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