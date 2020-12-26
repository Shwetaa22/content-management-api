from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


# from rest_framework.request from Request
class AuthenticationMiddlewareJWT(object):
    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JSONWebTokenAuthentication()
        if jwt_authentication.get_jwt_value(request):
            user, jwt = jwt_authentication.authenticate(request)
        return user

    def __init__(self, next_layer=None):
        """We allow next_layer to be None because old-style middlewares
        won't accept any argument.
        """
        self.get_response = next_layer

    def process_request(self, request):
        """Let's handle old-style request processing here, as usual."""
        # Do something with request
        # Probably return None
        # Or return an HttpResponse in some cases
        if request.user is None:
            return self.get_response(request)

        if not request.user.is_active:
            return self.get_response(request)

        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))
        if not request.user.is_authenticated:
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            print(token)
            data = {'token': token}
            try:
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                request.user = user
            except ValidationError as v:
                print("validation error", v)
            return self.get_response(request)


    def process_response(self, request, response):
        """Let's handle old-style response processing here, as usual."""
        # Do something with response, possibly using request.
        return response

    def __call__(self, request):
        """Handle new-style middleware here."""
        response = self.process_request(request)
        print("2",response)

        if response is None:
            # If process_request returned None, we must call the next middleware or
            # the view. Note that here, we are sure that self.get_response is not
            # None because this method is executed only in new-style middlewares.
            response = self.get_response(request)
            print("3", response)

        response = self.process_response(request, response)
        return response

