# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    depends_on = (
        ('namespaces', '0002_move_data'),
    )

    def forwards(self, orm):
        # Deleting model 'Namespace'
        db.delete_table(u'common_namespace')

        # Removing M2M table for field view_website on 'Namespace'
        db.delete_table(db.shorten_name(u'common_namespace_view_website'))

        # Removing M2M table for field view_menu on 'Namespace'
        db.delete_table(db.shorten_name(u'common_namespace_view_menu'))


    def backwards(self, orm):
        # Adding model 'Namespace'
        db.create_table(u'common_namespace', (
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(related_name='children', null=True, to=orm['common.Namespace'], blank=True)),
            ('view_type', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('view_dash', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dashboard.Dash'], null=True, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'common', ['Namespace'])

        # Adding M2M table for field view_website on 'Namespace'
        m2m_table_name = db.shorten_name(u'common_namespace_view_website')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('namespace', models.ForeignKey(orm[u'common.namespace'], null=False)),
            ('website', models.ForeignKey(orm[u'website.website'], null=False))
        ))
        db.create_unique(m2m_table_name, ['namespace_id', 'website_id'])

        # Adding M2M table for field view_menu on 'Namespace'
        m2m_table_name = db.shorten_name(u'common_namespace_view_menu')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('namespace', models.ForeignKey(orm[u'common.namespace'], null=False)),
            ('menuitem', models.ForeignKey(orm[u'reports.menuitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['namespace_id', 'menuitem_id'])


    models = {

    }

    complete_apps = ['common']
