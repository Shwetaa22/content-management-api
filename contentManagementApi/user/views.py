import jwt
from django.contrib.auth import authenticate, user_logged_in
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_payload_handler
from .serializers import UserSerializer
from .models import User
from contentManagementApi import settings

@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    data = request.data
    try:
        print(data)
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            user_data = user_serializer.data
            u = User.objects.get(id=user_data["id"])
            u.set_password(data["password"])
            u.save()
        else:
            print(user_serializer.errors)
            return Response({'code': '400', 'message': user_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'code': '200', 'message': "Data added successfully ", 'data': user_data},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"code": 500, "message": "something went wrong"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    try:
        email_id = request.data.get("email_id", None)
        password = request.data.get("password", None)
        if email_id is None or password is None:
            return Response({"code": 400, "message": "Email Id and Password both are required"},
                        status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email_id=email_id, password=password)
        if user is not None:
            try:
                user_data = User.objects.get(email_id=email_id)
                payload = jwt_payload_handler(user_data)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {
                    "name" : user_data.full_name,
                    "email_id": user_data.email_id,
                    "token" : token
                }

                user_logged_in.send(sender=user_data.__class__,
                                    request=request, user=user_data)

            except Exception as e:
                raise e
        else:
            return Response({"code": 401, "message": "Email or Password is wrong"},
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response({'code': '200', 'message': "Login successfully ", 'data': user_details},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"code": 500, "message": "something went wrong"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
