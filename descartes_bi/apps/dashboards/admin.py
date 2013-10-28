from __future__ import absolute_import

from django.contrib import admin

from .models import Dashboard, DashboardElement


class DashboardElementInline(admin.StackedInline):
    model = DashboardElement
    extra = 1


class DashboardAdmin(admin.ModelAdmin):
    inlines = [DashboardElementInline]


admin.site.register(Dashboard, DashboardAdmin)
