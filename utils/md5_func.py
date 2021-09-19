import hashlib


def mkMd5(value):
    secret_key = 'username'.encode('utf-8')   # 加盐
    ret = hashlib.md5(secret_key)
    ret.update(value.encode('utf-8'))
    return ret.hexdigest()


