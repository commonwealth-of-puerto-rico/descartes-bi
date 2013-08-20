# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Namespace'
        db.create_table(u'common_namespace', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['common.Namespace'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('view_type', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'common', ['Namespace'])

        # Adding M2M table for field view_menu on 'Namespace'
        m2m_table_name = db.shorten_name(u'common_namespace_view_menu')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('namespace', models.ForeignKey(orm[u'common.namespace'], null=False)),
            ('menuitem', models.ForeignKey(orm[u'reports.menuitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['namespace_id', 'menuitem_id'])

        # Adding M2M table for field view_dash on 'Namespace'
        m2m_table_name = db.shorten_name(u'common_namespace_view_dash')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('namespace', models.ForeignKey(orm[u'common.namespace'], null=False)),
            ('dash', models.ForeignKey(orm[u'dashboard.dash'], null=False))
        ))
        db.create_unique(m2m_table_name, ['namespace_id', 'dash_id'])


    def backwards(self, orm):
        # Deleting model 'Namespace'
        db.delete_table(u'common_namespace')

        # Removing M2M table for field view_menu on 'Namespace'
        db.delete_table(db.shorten_name(u'common_namespace_view_menu'))

        # Removing M2M table for field view_dash on 'Namespace'
        db.delete_table(db.shorten_name(u'common_namespace_view_dash'))


    models = {
        u'common.namespace': {
            'Meta': {'object_name': 'Namespace'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['common.Namespace']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'view_dash': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['dashboard.Dash']", 'null': 'True', 'blank': 'True'}),
            'view_menu': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Menuitem']", 'null': 'True', 'blank': 'True'}),
            'view_type': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dashboard.dash': {
            'Meta': {'object_name': 'Dash'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'selection_list': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dashboard.Selected_report']", 'symmetrical': 'False'})
        },
        u'dashboard.selected_report': {
            'Meta': {'object_name': 'Selected_report'},
            'from_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_regional': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'refresh_rate': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'rep_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Report']"}),
            'to_date': ('django.db.models.fields.DateField', [], {}),
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
        u'reports.menuitem': {
            'Meta': {'ordering': "['order', 'title']", 'object_name': 'Menuitem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reports': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reports.Report']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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

    complete_apps = ['common']