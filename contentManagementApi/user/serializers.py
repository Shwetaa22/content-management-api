import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField('getState')

    def getState(self, instance):
        return instance.state

    class Meta(object):
        model = User
        fields = ('id', 'email_id', 'full_name', 'phone', 'address', 'city', 'state', 'country', 'password', 'pincode')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if len(data["password"]) > 8:
            raise ValidationError({"password":["Password should contain maximum 8 characters."]})

        if re.search('[A-Z]', data['password']) is None or re.search('[a-z]', data['password']) is None:
            raise ValidationError(
                {'password': ['Password should contain 1 uppercase letter and 1 lowercase letter.']})
        return data
