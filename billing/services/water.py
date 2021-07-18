from billing.models import Counter, SERVICE_TYPE_WATER, CounterHistory





def get_water_history(house):
    q = CounterHistory.objects.filter(
        counter__service_type=SERVICE_TYPE_WATER, counter__house=house
    ).order_by(
        '-date', 'counter__description', 'counter__id'
    ).select_related(
        'counter'
    )


