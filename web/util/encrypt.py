import hashlib
from django.conf import settings


# md5加密
def md5(string):
    hash_object = hashlib.md5(string.encode('utf-8'))
    hash_object.update(string.encode('utf-8'))
    return hash_object.hexdigest()

