import hashlib

def md5_function(value):
    secret_key = 'username'.encode('utf-8')

    ret = hashlib.md5(secret_key)
    ret.update(value.encode('utf-8'))

    return ret.hexdigest()