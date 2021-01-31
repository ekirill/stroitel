from django.contrib import admin

from core.models import StroiPhone, StroiUser


class StroiUserAdmin(admin.ModelAdmin):
    pass


class StroiPhoneAdmin(admin.ModelAdmin):
    pass


admin.site.register(StroiUser, StroiUserAdmin)
admin.site.register(StroiPhone, StroiPhoneAdmin)

