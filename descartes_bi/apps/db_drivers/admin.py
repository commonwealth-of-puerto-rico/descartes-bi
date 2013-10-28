from __future__ import absolute_import

from django.contrib import admin

from .models import DataSource, Server


class ServerAdmin(admin.ModelAdmin):
    list_display = ('label', 'backend', 'user', 'host', 'port')
    list_editable = ('backend', 'user', 'host', 'port')


class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('label', 'server', 'name')
    list_editable = ('server', 'name')


admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(Server, ServerAdmin)
