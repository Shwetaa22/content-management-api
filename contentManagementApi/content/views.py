import ast

from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ContentSerializer, ContentListSerializer
from .models import *
from contentManagementApi.token_authentication import tokenAuth

from user.models import User

from contentManagementApi.settings import BASE_DIR


def verifyTokenAuth(request):
    token_data = tokenAuth(request)
    user_id = token_data.get("user_id")
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return False


class ContentClass(APIView):

    def get(self, request, id=''):
        try:
            content = Contents.objects.get(id=id)
            content_serializer = ContentListSerializer(content)

            return Response({'code': '200', 'message': "Data updated successfully ", 'data': content_serializer.data},
                            status=status.HTTP_200_OK)
        except Contents.DoesNotExist:
            return Response({'code': '404', 'message': "Data not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"code": 500, "message": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, id=''):
        data = request.data
        transaction.set_autocommit(False)
        userAuthenticate = verifyTokenAuth(request)
        if not userAuthenticate :
            return Response({'code': '401', 'message': "UnAuhhorized User"}, status=status.HTTP_401_UNAUTHORIZED)

        if not type(data) is dict:
            data._mutable = True
        data['user'] = userAuthenticate.id

        try:
            content_serializer = ContentSerializer(data=data)
            if content_serializer.is_valid():
                content_serializer.save()
                transaction.commit()
                content_data = content_serializer.data
            else:
                transaction.rollback()
                print(content_serializer.errors, 'kj')
                return Response({'code': '400', 'message': content_serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

            transaction.commit()
            return Response({'code': '200', 'message': "Data added successfully ", 'data': content_data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"code": 500, "message": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            transaction.set_autocommit(True)

    def put(self, request, id=''):
        if (not id):
            return Response({'code': '400', 'message': "Invalid inputs"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        userAuthenticate = verifyTokenAuth(request)
        if not userAuthenticate:
            return Response({'code': '401', 'message': "UnAuhhorized User"}, status=status.HTTP_401_UNAUTHORIZED)

        transaction.set_autocommit(False)
        try:
            content = Contents.objects.get(id=id)
            if content.user_id == userAuthenticate.id or userAuthenticate.is_superuser :
                content_serializer = ContentSerializer(content, data=data)
                print(data)
                if content_serializer.is_valid():
                    content_serializer.save()
                    transaction.commit()
                    content_data = content_serializer.data
                else:
                    transaction.rollback()
                    print(content_serializer.errors)
                    return Response({'code': '400', 'message': content_serializer.errors},
                                    status=status.HTTP_400_BAD_REQUEST)

                transaction.commit()
                self.get(request, id)
                return Response({'code': '200', 'message': "Data updated successfully ", 'data': content_data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'code': '401', 'message': "User can not edit other users content."},
                                status=status.HTTP_401_UNAUTHORIZED)
        except Contents.DoesNotExist:
            return Response({'code': '404', 'message': "Data Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"code": 500, "message": "something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            transaction.set_autocommit(True)

    def delete(self, request, id=''):
        if not id:
            return Response({'code': '400', 'message': "Invalid inputs"}, status=status.HTTP_400_BAD_REQUEST)

        userAuthenticate = verifyTokenAuth(request)
        if not userAuthenticate:
            return Response({'code': '401', 'message': "UnAuhhorized User"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            content = Contents.objects.get(id=id)
            if content.user_id == userAuthenticate.id or userAuthenticate.is_superuser :
                fs = FileSystemStorage()
                if fs.exists(BASE_DIR + "/" + str(content.document)):
                    fs.delete(BASE_DIR + "/" + str(content.document))
                content.delete()
            else:
                return Response({'code': '401', 'message': "User can not edit other users content."},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({'code': '200', 'message': "Data deleted successfully ", }, status=status.HTTP_200_OK)
        except Contents.DoesNotExist:
            return Response({'code': '404', 'message': "Data not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def search_content(request):
    userAuthenticate = verifyTokenAuth(request)
    if not userAuthenticate:
        return Response({'code': '401', 'message': "UnAuhhorized User"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        search = request.query_params.get("search")
        print(search)
        if search:
            content = Contents.objects.filter(Q(title__icontains=search) | Q(body__icontains=search) | Q(summary__icontains=search) | Q(categories__icontains=search))
        else:
            content = Contents.objects.all()

        content_serializer = ContentListSerializer(content, many=True)
        return Response({'code': '200', 'message': "Data retrieved successfully ", 'data': content_serializer.data},
                        status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"code": 500, "message": "something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
