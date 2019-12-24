from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.GET.get("username")
        password = request.GET.get("password")

        if ((not username) or (not password)): # no username or password passed in request headers
            return None # authentication did not succeed

        try:
            user = User.objects.get((username == username) and (password == password)) # get the user
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Usuario no existe o clave invalida') # raise exception if user does not exist

        return (user, None) # authentication successful
