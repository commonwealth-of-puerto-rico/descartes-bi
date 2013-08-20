# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Selected_report.from_date'
        db.delete_column(u'dashboard_selected_report', 'from_date')

        # Deleting field 'Selected_report.to_date'
        db.delete_column(u'dashboard_selected_report', 'to_date')

        # Deleting field 'Selected_report.id_regional'
        db.delete_column(u'dashboard_selected_report', 'id_regional')

        # Adding field 'Selected_report.filtersets'
        db.add_column(u'dashboard_selected_report', 'filtersets',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Filterset'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Selected_report.values'
        db.add_column(u'dashboard_selected_report', 'values',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Selected_report.from_date'
        db.add_column(u'dashboard_selected_report', 'from_date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'Selected_report.to_date'
        db.add_column(u'dashboard_selected_report', 'to_date',
                      self.gf('django.db.models.fields.DateField')(default=None),
                      keep_default=False)

        # Adding field 'Selected_report.id_regional'
        db.add_column(u'dashboard_selected_report', 'id_regional',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None),
                      keep_default=False)

        # Deleting field 'Selected_report.filtersets'
        db.delete_column(u'dashboard_selected_report', 'filtersets_id')

        # Deleting field 'Selected_report.values'
        db.delete_column(u'dashboard_selected_report', 'values')


    models = {
        u'dashboard.dash': {
            'Meta': {'object_name': 'Dash'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'selection_list': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dashboard.Selected_report']", 'symmetrical': 'False'})
        },
        u'dashboard.selected_report': {
            'Meta': {'object_name': 'Selected_report'},
            'filtersets': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Filterset']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refresh_rate': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'rep_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Report']"}),
            'values': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'visual_type': ('django.db.models.fields.CharField', [], {'default': "'chart'", 'max_length': '5'})
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
            'highlighter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legend': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legend_location': ('django.db.models.fields.CharField', [], {'default': "'ne'", 'max_length': '2'}),
            'orientation': ('django.db.models.fields.CharField', [], {'default': "'v'", 'max_length': '1'}),
            'pointlabels': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pointlabels_location': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '2'}),
            'scale_label_override': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'series': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reports.Serie']", 'through': u"orm['reports.SerieType']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'tracking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trendline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'SI'", 'max_length': '2'}),
            'use_one_scale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zoom': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'reports.serie': {
            'Meta': {'ordering': "['name']", 'object_name': 'Serie'},
            'avg_execution_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'last_execution_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'tick_format': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'validated_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'validated_person': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'validation_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'reports.serietype': {
            'Meta': {'object_name': 'SerieType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Report']"}),
            'serie': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Serie']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'BA'", 'max_length': '2'}),
            'zerobase': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['dashboard']