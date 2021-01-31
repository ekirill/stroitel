from functools import lru_cache

from core.models import StroiPhone


@lru_cache(maxsize=200)
def is_stroi_staff(phone):
    return StroiPhone.objects.filter(phone=phone).exists()
