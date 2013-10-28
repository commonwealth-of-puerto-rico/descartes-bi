# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
    depends_on = (
        ('common', '0003_auto'),
    )

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for node in orm['common.namespace'].objects.all():
            new_node = orm['namespaces.namespace'](
                pk = node.pk,
                parent = None,
                label = node.label,
                lft = node.lft,
                rght = node.rght,
                tree_id = node.level,
                level = node.level,
                icon = node.icon,
                view_type = node.view_type,
                view_dash = node.view_dash
            )
            new_node.save()
            for menu in node.view_menu.all():
                new_node.view_menu.add(menu)

            for website in node.view_website.all():
                new_node.view_website.add(website)
            new_node.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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
            'view_dash': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dashboard.Dash']", 'null': 'True', 'blank': 'True'}),
            'view_menu': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Menuitem']", 'null': 'True', 'blank': 'True'}),
            'view_type': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'view_website': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['website.Website']", 'null': 'True', 'blank': 'True'})
        },
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
            'rep_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Report']", 'null': 'True', 'blank': 'True'}),
            'values': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'visual_type': ('django.db.models.fields.CharField', [], {'default': "'chart'", 'max_length': '7'}),
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
        u'namespaces.namespace': {
            'Meta': {'object_name': 'Namespace'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['namespaces.Namespace']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'view_dash': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dashboard'", 'null': 'True', 'to': u"orm['dashboard.Dash']"}),
            'view_menu': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'menus'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['reports.Menuitem']"}),
            'view_type': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'view_website': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'websites'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['website.Website']"})
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

    complete_apps = ['common', 'namespaces']
    symmetrical = True
