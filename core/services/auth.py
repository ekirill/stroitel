from functools import lru_cache

from core.models import StroiKnownPhone


@lru_cache(maxsize=200)
def is_stroi_staff(phone):
    return StroiKnownPhone.objects.filter(phone=phone).exists()


def normalize_phone(phone):
    result = ""
    for ch in phone.strip():
        if ch.isdigit():
            result += ch

    if result.startswith('7'):
        result = '8' + result[1:]

    return result
