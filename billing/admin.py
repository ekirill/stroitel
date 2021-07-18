from django.contrib import admin

from billing.models import Tariff, Counter, CounterHistory


class TariffAdmin(admin.ModelAdmin):
    list_display = ('service', 'start_date', 'end_date', 'price')
    ordering = ('service',)


class CounterAdmin(admin.ModelAdmin):
    list_display = ('house', 'service_type')
    ordering = ('house', 'service_type')


class CounterHistoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'counter', 'service', 'value')
    ordering = ('date', 'counter__house', 'service', 'counter__description')
    list_filter = ('counter__house', 'counter__service_type')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('counter')
        return qs


admin.site.register(Tariff, TariffAdmin)
admin.site.register(Counter, CounterAdmin)
admin.site.register(CounterHistory, CounterHistoryAdmin)
