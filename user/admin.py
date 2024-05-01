from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = 'user'


class CustomUserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline, )
    list_display = (
        'get_name',
        'screen_name',
        'email',
        'is_staff',
        'user_type'
    )
    search_fields = ('screen_name', 'email', 'profile__first_name', 'profile__last_name')

    # def save_model(self, request, obj, form, change):
    #     obj.username = obj.email
    #     obj.save()
    #     super().save_model(request, obj, form, change)

    @admin.display(ordering='user__profile', description='Name')
    def get_name(self, obj):
        return '{0} {1}'.format(obj.profile.first_name, obj.profile.last_name)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# admin.site.unregister(User)x
admin.site.register(User, CustomUserAdmin)
