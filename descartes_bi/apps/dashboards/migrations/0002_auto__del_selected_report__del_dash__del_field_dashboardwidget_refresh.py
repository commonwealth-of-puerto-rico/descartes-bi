# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Selected_report'
        db.delete_table(u'dashboards_selected_report')

        # Deleting model 'Dash'
        db.delete_table(u'dashboards_dash')

        # Removing M2M table for field selection_list on 'Dash'
        db.delete_table(db.shorten_name(u'dashboards_dash_selection_list'))

        # Deleting field 'DashboardWidget.refresh_rate'
        db.delete_column(u'dashboards_dashboardwidget', 'refresh_rate')


    def backwards(self, orm):
        # Adding model 'Selected_report'
        db.create_table(u'dashboards_selected_report', (
            ('visual_type', self.gf('django.db.models.fields.CharField')(default='chart', max_length=7)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Website'], null=True, blank=True)),
            ('values', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('refresh_rate', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('filtersets', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Filterset'], null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rep_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Report'], null=True, blank=True)),
        ))
        db.send_create_signal(u'dashboards', ['Selected_report'])

        # Adding model 'Dash'
        db.create_table(u'dashboards_dash', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'dashboards', ['Dash'])

        # Adding M2M table for field selection_list on 'Dash'
        m2m_table_name = db.shorten_name(u'dashboards_dash_selection_list')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dash', models.ForeignKey(orm[u'dashboards.dash'], null=False)),
            ('selected_report', models.ForeignKey(orm[u'dashboards.selected_report'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dash_id', 'selected_report_id'])


        # User chose to not deal with backwards NULL issues for 'DashboardWidget.refresh_rate'
        raise RuntimeError("Cannot reverse this migration. 'DashboardWidget.refresh_rate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'DashboardWidget.refresh_rate'
        db.add_column(u'dashboards_dashboardwidget', 'refresh_rate',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(),
                      keep_default=False)


    models = {
        u'dashboards.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'dashboards.dashboardwidget': {
            'Meta': {'object_name': 'DashboardWidget'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'widgets'", 'to': u"orm['dashboards.Dashboard']"}),
            'filtersets': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Filterset']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Report']", 'null': 'True', 'blank': 'True'}),
            'span': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'values': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'visual_type': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Website']", 'null': 'True', 'blank': 'True'})
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
        u'reports.report': {
            'Meta': {'ordering': "['title']", 'object_name': 'Report'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'filtersets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Filterset']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'renderer': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'renderer_options': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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
        u'website.website': {
            'Meta': {'object_name': 'Website'},
            'base_URL': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'filterset': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Filterset']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Serie']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dashboards']