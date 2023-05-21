import hashlib
from django.conf import settings


# md5加密,用来对一些重要信息加密
def md5(data_string):
    # settings.SECRET_KEY用做salt
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
