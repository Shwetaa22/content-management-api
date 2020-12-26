from rest_framework import serializers
from .models import Contents
from user.serializers import UserSerializer


class ContentSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Contents
        fields = ('id', 'title', 'body', 'summary', 'user', 'document', 'categories')

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer()
        return super(ContentSerializer, self).to_representation(instance)


class ContentListSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField('getCategories')

    def getCategories(self, instance):
        cat = instance.categories.split(',')
        return cat

    class Meta(object):
        model = Contents
        fields = ('id', 'title', 'body', 'summary', 'user', 'document', 'categories')

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer()
        return super(ContentListSerializer, self).to_representation(instance)
