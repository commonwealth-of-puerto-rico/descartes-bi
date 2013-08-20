from django.contrib import admin

from dashboard.models import Dash, Selected_report


class DashAdmin(admin.ModelAdmin):
    filter_horizontal = ('selection_list',)

class SelectReportAdmin(admin.ModelAdmin):
    pass


admin.site.register(Dash, DashAdmin)
admin.site.register(Selected_report, SelectReportAdmin)
