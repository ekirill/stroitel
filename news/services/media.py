import hashlib

from news.models import MediaFile


def is_members_only(path):
    return MediaFile.objects.filter(file=path, members_only=True).exists()
