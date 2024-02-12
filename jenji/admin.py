from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Helper Class for creating user admin pages
from django.utils.html import format_html

from .models import NewUser, Entry


class CustomUserAdmin(UserAdmin):

    model = NewUser

    list_display = ('username', 'car_number', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('username',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class EntryAdmin(admin.ModelAdmin):
    model = NewUser

    list_display = ('user', 'date', 'time', 'car_number')
    search_fields = ('user','car_number')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    actions = ['delete_selected']

    def car_number(self, obj):
        related_object = obj.user
        return format_html(f'<a href="/admin/jenji/newuser/{related_object.id}/">{obj.user.car_number}</a>')
    car_number.short_description = 'Car Number'
    car_number.allow_tags = True

    def delete_selected(self, request, queryset):
        queryset.delete()

admin.site.register(NewUser, CustomUserAdmin)
admin.site.register(Entry, EntryAdmin)