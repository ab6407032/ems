from django.contrib import admin
from .models import Keyword, Counter


class CounterInlineAdmin(admin.TabularInline):
    model = Counter
    fields = ('name', 'active',)
    extra = 0
    classes = ('collapse',)

class KeywordAdmin(admin.ModelAdmin):
    inlines = [
        CounterInlineAdmin
    ]
    list_filter = ('name', 'code', 'active',)
    list_display = (
        'pkid',
        'name',
        'code',
        'active',
    )
    search_fields = ('name', 'code', 'description',)
    # list_display_links = ('dummy',)
    list_editable = ('name', 'code', 'active', )
    exclude = ('created_by', 'modified_by',)
    readonly_fields = ('pkid',)
    fieldsets = (("", {'fields': (('name', 'code', 'active')),
                       'description': ''})),

admin.site.register(Keyword, KeywordAdmin)
