import jwt

from contentManagementApi import settings


def decodeToken(token):
    data = jwt.decode(token, settings.SECRET_KEY, options={'verify_exp': False})
    return data


def tokenAuth(request):
    token = request.META.get('HTTP_AUTHORIZATION').replace("Bearer ", "")
    data = decodeToken(token)
    return data
