from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^(?P<id>\w+)$',ContentClass.as_view()),
    url('content-list',search_content)
]