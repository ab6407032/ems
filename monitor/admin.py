from django.contrib import admin
#from .models import Host, Port, Fiber, Dio, RouterLog
from .models import Node, NodeLogFile, NodeMetric
from helpers import load_file_contents_db
from django.urls import path
from django.http import HttpResponseRedirect


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('node_name', 'active')
    search_fields = ('node_name',)
    exclude = ('created_by', 'modified_by',)

# class AbstractModelAdmin(admin.ModelAdmin):
#     """Classe to dont repeat same fields to all"""

#     actions = None
#     list_per_page = 15


# class PortInLines(admin.TabularInline):
#     model = Port
#     extra = 1
#     classes = ["collapse"]


# class HostAdmin(AbstractModelAdmin):
#     fieldsets = [
#         (
#             None,
#             {"fields": ["local", "circuit", "name", "ipv4", "network", "max_retries"]},
#         ),
#         (
#             "Daemon Fields",
#             {
#                 "fields": [
#                     "status",
#                     "status_info",
#                     "last_status_change",
#                     "last_check",
#                     "retries",
#                 ],
#                 "classes": ["collapse"],
#             },
#         ),
#     ]
#     list_display = (
#         "ipv4",
#         "name",
#         "local",
#         "network",
#         "status",
#         "switch_manager",
#         "max_retries",
#         "circuit",
#     )
#     search_fields = ["ipv4", "name", "local", "circuit", "network", "status"]
#     ordering = ("-switch_manager",)
#     inlines = [PortInLines]


# class FibraAdmin(AbstractModelAdmin):
#     model = Fiber
#     list_display = ("dio", "get_pop", "number", "port", "description")
#     search_fields = ["dio__name", "number", "port", "description"]
#     actions = None

#     def get_pop(self, obj):
#         return obj.dio.pop

#     get_pop.short_description = "Pop"


# class FibraInLines(admin.TabularInline):
#     model = Fiber


# class DioAdmin(AbstractModelAdmin):
#     list_display = ("name", "pop")
#     search_fields = ["name", "pop__name"]
#     inlines = [FibraInLines]


# class PortAdmin(AbstractModelAdmin):
#     list_display = (
#         "host",
#         "ip_",
#         "number",
#         "error_counter",
#         "counter_last_change",
#         "is_monitored",
#     )
#     search_fields = ["host__name", "host__ipv4", "number"]
#     ordering = ("-counter_last_change",)

#     def ip_(self, obj):
#         return obj.host.ipv4
# class RouterLogScoreInline(admin.StackedInline):
#     model = RouterLogScore
#     can_delete = False
#     fk_name = 'logfile'

class NodeLogFileAdmin(admin.ModelAdmin):
    # inlines = (RouterLogScoreInline, )
    list_filter = ('node', 'start_time', 'processed', 'metric_calculation',)
    list_display = (
        'pkid',
        'node',
        'file',
        'name',
        'start_time',
        'size',
        'processed',
        'metric_calculation'
    )
    search_fields = ('node__node_name', 'name', 'size', 'start_time',)
    # list_display_links = ('dummy',)
    # list_editable = ('name', 'code', 'active', )
    exclude = ('created_by', 'modified_by',)
    readonly_fields = ('pkid',)
    fieldsets = (("", {'fields': ((
        'file',
        'node',
    )),
    'description': ''})),

admin.site.register(NodeLogFile, NodeLogFileAdmin)

# def load_data(modeladmin, request, queryset):
#     data = load_file_contents_db()
#     RouterLog.objects.bulk_create(data)
#     modeladmin.message_user(request, "Data Load executed successfully")

# load_data.short_description = "Load Data"
    
class NodeMetricAdmin(admin.ModelAdmin):
    # actions = [load_data]
    list_filter = ('node', 'logfile', 'metric',)
    list_display = (
        "node",
        "logfile",
        "metric",
        "value",
    )
    search_fields = ["node__node_name", "logfile__name", "keyword", "metric"]
    ordering = ("-created_on",)
    #list_editable = ('timestamp', 'keyword', 'keyword_no', 'counter', 'counter_no', 'counter_value')
    exclude = ('created_by', 'modified_by',)
    readonly_fields = ('pkid',)
    fieldsets = (("", {'fields': (('node', 'logfile', 'metric', 'value')),
                       'description': ''})),
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('load-data/', self.admin_site.admin_view(self.load_data), name='load_data'),
    #     ]
    #     return custom_urls + urls

    # def load_data(self, request):
    #     # Logic for the custom action
    #     # Redirect or render a response
    #     self.message_user(request, "Load Data executed successfully")
    #     return HttpResponseRedirect("../")


# admin.site.register(Host, HostAdmin)
# admin.site.register(Dio, DioAdmin)
# admin.site.register(Fiber, FibraAdmin)
# admin.site.register(Port, PortAdmin)
admin.site.register(NodeMetric, NodeMetricAdmin)
