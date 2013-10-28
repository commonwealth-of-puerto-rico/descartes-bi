# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DashboardElement.visual_type'
        db.delete_column(u'dashboards_dashboardelement', 'visual_type')

        # Deleting field 'DashboardElement.website'
        db.delete_column(u'dashboards_dashboardelement', 'website_id')

        # Deleting field 'DashboardElement.filtersets'
        db.delete_column(u'dashboards_dashboardelement', 'filtersets_id')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'DashboardElement.visual_type'
        raise RuntimeError("Cannot reverse this migration. 'DashboardElement.visual_type' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'DashboardElement.visual_type'
        db.add_column(u'dashboards_dashboardelement', 'visual_type',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)

        # Adding field 'DashboardElement.website'
        db.add_column(u'dashboards_dashboardelement', 'website',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Website'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'DashboardElement.filtersets'
        db.add_column(u'dashboards_dashboardelement', 'filtersets',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Filterset'], null=True, blank=True),
                      keep_default=False)


    models = {
        u'dashboards.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'dashboards.dashboardelement': {
            'Meta': {'object_name': 'DashboardElement'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': u"orm['dashboards.Dashboard']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Report']", 'null': 'True', 'blank': 'True'}),
            'span': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'values': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'reports.filterset': {
            'Meta': {'ordering': "['name']", 'object_name': 'Filterset'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'reports.report': {
            'Meta': {'ordering': "['title']", 'object_name': 'Report'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filterset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Filterset']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'renderer': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'renderer_options': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['dashboards']