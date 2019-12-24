"""api_wingo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include, url

from django.contrib import admin
from django.conf import settings

admin.autodiscover()

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from apiwingo.views import LoginView, RegisterView


from apiwingo.views import (
                    #MAIL
                    SendMailSignup,
                    SendMailEvento,
                    SendMailLiquidacion,
                    ChangePasswordView,
                    ResetPasswordView,
                    )

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(('apiwingo.urls', 'apiwingo'), namespace='api-wingo')),

    ##url(r'^api/v1/rest-auth/', obtain_jwt_token),
    #url(r'^api/v1/api-token-auth/', obtain_jwt_token, name='create-token'),

    url(r'^api/v1/auth/login', LoginView.as_view(), name="create-token"),
    url(r'^api/v1/auth/register', RegisterView.as_view(), name="auth-register"),
    url(r'^api/v1/auth/password/change', ChangePasswordView.as_view(), name="request-password"),
    url(r'^api/v1/auth/password/reset', ResetPasswordView.as_view(), name="reset-password"),

    #url(r'^api/v1/api-token-refresh/', refresh_jwt_token),
    #url(r'^api/v1/api-token-verify/', verify_jwt_token),

    url(r'^api/v1/sendmail/signup$', SendMailSignup.as_view(), name='sendmail-signup'),
    url(r'^api/v1/sendmail/evento$', SendMailEvento.as_view(), name='sendmail-evento'),
    url(r'^api/v1/sendmail/liquidacion$', SendMailLiquidacion.as_view(), name='sendmail-liquidacion'),


    ]

