from django.contrib import admin

from core.models import StroiKnownPhone, StroiUser
from core.services.auth import is_stroi_staff


class StroiUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone')


class StroiKnownPhoneAdmin(admin.ModelAdmin):
    list_display = ('phone', 'description')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        is_stroi_staff.cache_clear()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        is_stroi_staff.cache_clear()


admin.site.register(StroiUser, StroiUserAdmin)
admin.site.register(StroiKnownPhone, StroiKnownPhoneAdmin)
