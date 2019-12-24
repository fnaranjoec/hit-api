#Create your views here.

from .models import (
                    User,

                    Tblpersona,
                    Tblpersonapropiedad,
                    Tblusuario,
                    Tblrol,
                    Tblrolusuario,
                    Tblcliente,
                    Tblpropiedad,
                    Tbltipoevento,
                    Tblevento,
                    Tbleventodetalle,
                    Tbleventodetcompetidor,
                    Tbleventodetpronostico,
                    Tbleventoresulpronostico,
                    Tbleventopunto,
                    Tblclienteeventodet,
                    Tblclienteeventodetcomp,
                    Tblclienteeventodetcomppronos,
                    Tbltipotrans,
                    Tblclientetrans,
                    Tblmensaje,
                    Tblparametro,
                    Tblrecurso,
                    #Seguridad
                    Tblaplicacion,
                    Tbleventoopcion,
                    Tblfuncion,
                    Tblmodulo,
                    Tblopcion,
                    Tblpermisoeventoopcion,
                    Tblpermisoopcion,

                    Tblbanco,
                    Tbltipocuentabanco,
                    Tblclientesolicitud,
                    Tblpais,
                    Tblpassrecovery,


                    #VISTAS
                    Vwclientecreditos,
                    Vwclienteeventos,
                    Vweventoconresultado,


                    #STORE PROCEDURES
                    SPMenu,
                    #SPClienteEventos,
                    SPPremiosEventoListado,
                    SPPremiosEventoPuntos,
                    SPPremiosEvento,
                    SPPremiosEventoLiquidar,
                    SPEventoActivoAcumulado,


)

from .serializers import (
                          TokenSerializer,

                          UserSerializer,
                          PersonaSerializer,
                          PropiedadSerializer,
                          PersonaPropiedadSerializer,
                          UsuarioSerializer,
                          RolSerializer,

                          RolUsuarioSerializer,
                          RolUsuarioListSerializer,

                          ClienteSerializer,
                          TipoEventoSerializer,
                          EventoSerializer,
                          EventoDetalleSerializer,

                          EventoDetalleCompetidorSerializer,
                          EventoDetalleCompetidorListSerializer,

                          EventoDetallePronosticoSerializer,
                          EventoResultadoPronosticoSerializer,

                          EventoPuntoSerializer,

                          ClienteEventoDetalleSerializer,
                          ClienteEventoDetalleListSerializer,

                          ClienteEventoDetalleCompetidoresSerializer,

                          ClienteEventoDetalleCompetidoresPronosticoSerializer,
                          TipoTransaccionSerializer,
                          ClienteTransaccionSerializer,
                          MensajeSerializer,
                          ParametroSerializer,
                          RecursoSerializer,
                          #Seguridad
                          AplicacionSerializer,
                          EventoOpcionSerializer,
                          FuncionSerializer,
                          ModuloSerializer,
                          OpcionSerializer,

                          PermisoOpcionSerializer,
                          PermisoOpcionListSerializer,

                          PermisoEventoOpcionSerializer,

                          BancoSerializer,
                          TipoCuentaBancoSerializer,
                          ClienteSolicitudSerializer,
                          PaisSerializer,
                          PassRecoverySerializer,

                        #VISTAS
                          ClienteCreditosSerializer,
                          EventosConResultadoSerializer,


                          #STORE PROCEDURES,
                          MenuSerializer,
                          ClienteEventosSerializer,
                          PremiosEventoListadoSerializer,
                          PremiosEventoPuntosSerializer,
                          PremiosEventoSerializer,
                          PremiosEventoLiquidarSerializer,
                          EventoActivoAcumuladoSerializer,


)

from django.core.mail import send_mail, send_mass_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string

from django.http import HttpResponse, HttpResponseRedirect, Http404
from api_wingo import settings

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework import generics,authentication,permissions,status,viewsets
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from rest_framework_jwt.settings import api_settings
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


import logging
import uuid


class BaseView():

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token


class LoginView(generics.CreateAPIView):
    """
    POST auth/login
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(generics.CreateAPIView):
    """
    POST auth/password/change
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)


    def post(self, request, *args, **kwargs):

        correo = request.data.get("email", "")
        user = User.objects.all().filter(email=correo)
        from_email = settings.DEFAULT_FROM_EMAIL
        username = user.values_list('username', flat=True)[0]
        recoveryid = str(uuid.uuid4())

        # Insert into tblpassrecovery to validate expiration time: Fredy Naranjo
        passrecovery= Tblpassrecovery(
            cidpassrecovery=recoveryid,
            cnomusuario=username
        )
        passrecovery.save()

        if (len(user)>0):
            if (from_email and correo):

                #subject = "Usted ganó $ %s en el evento HIT: %s " % (premio, evento)
                subject = "HIT: Password recovery instructions."
                text_content = "Hi!\nThis is an email instructions to recovery your password.\nClick on this link:, to reset your password"
                # html_content = "<form action='http://localhost:4200/pages/validar?ID=%s'><p>Usted se ha registrado un Evento <strong>HIT</strong>, Predice - Acierta y Gana</p><br><br>.<br><br><br><br></form>" % evento
                html_content = render_to_string('changepassword_email.html',
                                                {
                                                    'username': username,
                                                    'requestid': recoveryid,
                                                    'host': settings.APP_HOST,
                                                })

                # print(html_content)

                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                # msg.attach_alternative(html_content, "text/html")

                try:
                    msg = EmailMessage(subject, html_content, from_email, [correo])
                    msg.content_subtype = "html"
                    msg.send()

                    # send_mail(subject, html_content, from_email, [to_email])

                except BadHeaderError:
                    return Response(
                            data={
                                "Invalid header found sending mail."
                            },
                            status=status.HTTP_400_BAD_REQUEST
                            )

                return Response(
                        data={
                            "Change password email instructions was sent."
                        },
                        status=status.HTTP_200_OK
                        )

            return Response(
                        data={
                            "Make sure all fields are entered and valid."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                        )

        return Response(
               data={
                        "message": "Email " + correo + ", is not registered..."
                    },
                    status=status.HTTP_400_BAD_REQUEST
               )



class ResetPasswordView(generics.CreateAPIView):
    """
    POST auth/password/reset
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)


    def post(self, request, *args, **kwargs):

        correo = request.data.get("password", "")
        print(correo)
        #user = User.objects.all().filter(email=correo)
        #username = user.values_list('username', flat=True)[0]

        return Response(
            data={
                "Password was reseted."
            },
            status=status.HTTP_200_OK
        )



class RegisterView(generics.CreateAPIView):
    """
    POST auth/register
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        cellphone = request.data.get("cellphone", "")
        pin = request.data.get("pin", "")
        dob = request.data.get("dob", "")
        country = request.data.get("country", "")
        picture = request.data.get("picture", "")

        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
              username=username
            , password=password
            , email=email
            , first_name=first_name
            , last_name=last_name
            , cellphone=cellphone
            , pin=pin
            , dob=dob
            , country=country
            , picture=picture
        )
        return Response(status=status.HTTP_201_CREATED)




class DefaultsMixin(object):
    """Default settings for view authentication, permissions, filtering and pagination."""
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

    def get_queryset(self):
         queryset = User.objects.all().order_by('username')
         username = self.request.GET.get('username')

         if username:
             queryset = queryset.filter(username = username)

         return queryset


#______________________________________________________ PERSONA
class PersonaViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblpersona.objects.all().order_by('capepersona')
    serializer_class    = PersonaSerializer

    def get_queryset(self):
         queryset = Tblpersona.objects.all().order_by('capepersona')

         estado = self.request.GET.get('e')

         persona = self.request.GET.get('p')

         if estado:
             queryset = queryset.filter(ccepersona = estado)

         if persona:
             queryset = queryset.filter(cidpersona = persona)

         return queryset




#______________________________________________________ PROPIEDAD
class PropiedadViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblpropiedad.objects.all().order_by('cnompropiedad')
    serializer_class    = PropiedadSerializer
    def get_queryset(self):
         queryset = Tblpropiedad.objects.all().order_by('cnompropiedad')

         estado = self.request.GET.get('e')

         if estado:
             queryset = queryset.filter(ccepropiedad = estado)

         return queryset


#______________________________________________________ PERSONA PROPIEDAD
class PersonaPropiedadViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblpersonapropiedad.objects.all().order_by('cidpersonapropiedad')
    serializer_class    = PersonaPropiedadSerializer
    def get_queryset(self):
        queryset = Tblpersonapropiedad.objects.all().order_by('cidpersonapropiedad')

        persona = self.request.GET.get('p')

        if persona:
            queryset = queryset.filter(cidpersona = persona)

        return queryset



#______________________________________________________ USUARIO
class UsuarioViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblusuario.objects.all().order_by('cnomusuario')
    serializer_class    = UsuarioSerializer
    def get_queryset(self):
         queryset = Tblusuario.objects.all().order_by('cnomusuario')

         estado = self.request.GET.get('e')
         username = self.request.GET.get('u')
         celular = self.request.GET.get('c')
         validado = self.request.GET.get('v')
         correo = self.request.GET.get('co')

         if estado:
             queryset = queryset.filter(cceusuario = estado)

         if username:
             queryset = queryset.filter(cnomusuario = username)

         if validado:
             queryset = queryset.filter(csnvalidado = validado)

         if celular:
             queryset = queryset.filter(cnucelular = celular)

         if correo:
             queryset = queryset.filter(ctxcorreo = correo)

         return queryset

class UsuarioList(generics.ListAPIView): # new
    queryset = Tblusuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDetail(generics.RetrieveAPIView): # new
    queryset = Tblusuario.objects.all()
    serializer_class = UsuarioSerializer

#______________________________________________________ ROL
class RolViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblrol.objects.all().order_by('cnomrol')
    serializer_class    = RolSerializer


    def get_queryset(self):
         queryset = Tblrol.objects.all().order_by('cnomrol')

         estado = self.request.GET.get('e')

         if estado:
             queryset = queryset.filter(ccerol = estado)

         return queryset



#______________________________________________________ ROL USUARIO
class RolUsuarioViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblrolusuario.objects.all().order_by('cidrolusuario')
    serializer_class     = RolUsuarioSerializer

    def get_queryset(self):
         serializer_class = RolUsuarioListSerializer

         queryset = Tblrolusuario.objects.all().order_by('cidrolusuario')
         estado = self.request.GET.get('e')
         rol = self.request.GET.get('r')
         usuario = self.request.GET.get('u')

         if estado:
             queryset = queryset.filter(ccerolusuario = estado)

         if rol:
             queryset = queryset.filter(cidrol = rol)

         if usuario:
             queryset = queryset.filter(cidusuario = usuario)

         return queryset


class RolUsuarioListViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblrolusuario.objects.all().order_by('cidrolusuario')
    serializer_class     = RolUsuarioListSerializer

    """
    # *** OJO NO BORRAR ***  Dependiendo del metodo HTTP seleccionamos el serializador es decir UNA VIEW CON DOS SERIALIZADORES
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RolUsuarioListSerializer

        return RolUsuarioSerializer
    """

    def get_queryset(self):

         queryset = Tblrolusuario.objects.all().order_by('cidrolusuario')
         estado = self.request.GET.get('e')
         rol = self.request.GET.get('r')
         usuario = self.request.GET.get('u')

         if estado:
             queryset = queryset.filter(ccerolusuario = estado)

         if rol:
             queryset = queryset.filter(cidrol = rol)

         if usuario:
             queryset = queryset.filter(cidusuario = usuario)

         return queryset


#______________________________________________________ CLIENTE
class ClienteViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblcliente.objects.all().order_by('cidcliente')
    serializer_class    = ClienteSerializer
    def get_queryset(self):
         queryset = Tblcliente.objects.all().order_by('cidcliente')

         estado = self.request.GET.get('e')
         rolusuario = self.request.GET.get('ru')

         if rolusuario:
             queryset = queryset.filter(cidrolusuario = rolusuario)

         if estado:
             queryset = queryset.filter(ccecliente = estado)

         return queryset



#______________________________________________________ TIPO EVENTO
class TipoEventoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tbltipoevento.objects.all().order_by('cnomtipoevento')
    serializer_class    = TipoEventoSerializer

    def get_queryset(self):
         queryset = Tbltipoevento.objects.all().order_by('cnomtipoevento')

         estado = self.request.GET.get('e')
         liquidado = self.request.GET.get('l')

         if estado:
             queryset = queryset.filter(ccetipoevento = estado)

         if liquidado:
             queryset = queryset.filter(csnliquidado = liquidado)

         return queryset
#______________________________________________________ EVENTO
class EventoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblevento.objects.all().order_by('cnomevento') #!! override --> def get_queryset(self)
    serializer_class    = EventoSerializer
    def get_queryset(self):
        queryset = Tblevento.objects.all().order_by('cnomevento')

        tipoEvento = self.request.GET.get('t')
        pais = self.request.GET.get('p')
        estado = self.request.GET.get('e')
        evento = self.request.GET.get('ev')


        if estado:
            queryset = queryset.filter(cceevento = estado)


        if tipoEvento:
            queryset = queryset.filter(cidtipoevento = tipoEvento)


        if pais:
            queryset = queryset.filter(cidpais = pais)


        if evento:
            queryset = queryset.filter(cidevento = evento)

        return queryset

#______________________________________________________ EVENTO DETALLE
class EventoDetalleViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tbleventodetalle.objects.all().order_by('cnomdetalle')
    serializer_class    = EventoDetalleSerializer
    search_fields       = ('cideventodetalle', 'cidevento', 'cnomdetalle', 'ctxurliconodetalle','cceeventodetalle')

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(EventoDetalleViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = Tbleventodetalle.objects.all().order_by('cnomdetalle')

        evento = self.request.GET.get('ev')
        estado = self.request.GET.get('e')
        detalle = self.request.GET.get('ed')

        if estado:
            queryset = queryset.filter(cceeventodetalle = estado)


        if evento:
            queryset = queryset.filter(cidevento = evento)

        if detalle:
            queryset = queryset.filter(cideventodetalle = detalle)

        return queryset



#______________________________________________________ EVENTO DETALLE COMPETIROR
class EventoDetalleCompetidorViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tbleventodetcompetidor.objects.all().order_by('cnomcompetidora')
    serializer_class    = EventoDetalleCompetidorSerializer
    search_fields       = ('cideventodetcompetidor', 'cideventodetalle', 'cnomcompetidora', 'cnomcompetidorb', 'cceeventodetcompetidor', 'ctxurliconoa', 'ctxurliconob')

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(EventoDetalleCompetidorViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_queryset(self):
        queryset = Tbleventodetcompetidor.objects.all().order_by('cnomcompetidora')

        eventoDetalle = self.request.GET.get('evd')
        estado = self.request.GET.get('e')
        competidor = self.request.GET.get('evdc')

        if estado:
            queryset = queryset.filter(cceeventodetcompetidor = estado)


        if eventoDetalle:
            queryset = queryset.filter(cideventodetalle = eventoDetalle)

        if competidor:
            queryset = queryset.filter(cideventodetcompetidor = competidor)

        return queryset

#______________________________________________________ EVENTO DETALLE COMPETIROR
class EventoDetalleCompetidorListViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tbleventodetcompetidor.objects.all().order_by('cnomcompetidora')
    serializer_class    = EventoDetalleCompetidorListSerializer

    def get_queryset(self):
        queryset = Tbleventodetcompetidor.objects.all().order_by('cnomcompetidora')

        eventoDetalle = self.request.GET.get('evd')
        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(cceeventodetcompetidor = estado)


        if eventoDetalle:
            queryset = queryset.filter(cideventodetalle = eventoDetalle)

        return queryset


#______________________________________________________ EVENTO DETALLE PRONOSTICO
class EventoDetallePronosticoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tbleventodetpronostico.objects.all().order_by('cnomeventopronostico')
    serializer_class    = EventoDetallePronosticoSerializer
    search_fields       = ('cideventodetpronostico', 'cideventodetalle', 'cnomeventopronostico', 'cceeventopronostico', 'ccicompetidor')

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(EventoDetallePronosticoViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_queryset(self):
        queryset = Tbleventodetpronostico.objects.all().order_by('cnomeventopronostico')

        eventoDetalle = self.request.GET.get('evd')
        competidor = self.request.GET.get('c')
        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(cceeventopronostico = estado)

        if eventoDetalle:
            queryset = queryset.filter(cideventodetalle = eventoDetalle)

        if competidor:
            queryset = queryset.filter(ccicompetidor = competidor)

        return queryset

#______________________________________________________ EVENTO RESULTADO PRONOSTICO
class EventoResultadoPronosticoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset            = Tbleventoresulpronostico.objects.all().order_by('cideventoresulpronostico')
    serializer_class    = EventoResultadoPronosticoSerializer
    search_fields       = ('cideventoresulpronostico','cideventodetpronostico', 'cideventodetcompetidor', 'ctxeventoresulcoma', 'ctxeventoresulcomb')

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(EventoResultadoPronosticoViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_queryset(self):
        queryset = Tbleventoresulpronostico.objects.all().order_by('cideventoresulpronostico')

        eventoDetCompetidor = self.request.GET.get('evdcom')
        eventoDetPronostico = self.request.GET.get('evdpro')

        if eventoDetCompetidor:
            queryset = queryset.filter(cideventodetcompetidor = eventoDetCompetidor)

        if eventoDetPronostico:
            queryset = queryset.filter(cideventodetpronostico = eventoDetPronostico)

        return queryset


#______________________________________________________ EVENTO PUNTO
class EventoPuntoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tbleventopunto.objects.all().order_by('ncanpuntos')
    serializer_class    = EventoPuntoSerializer
    search_fields       = ('cideventopunto', 'cidevento', 'ncanpuntos', 'nflporcpuntos', 'cceeventopunto')

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(EventoPuntoViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_queryset(self):
        queryset = Tbleventopunto.objects.all().order_by('ncanpuntos')

        estado = self.request.GET.get('e')
        evento = self.request.GET.get('ev')


        if estado:
            queryset = queryset.filter(cceeventopunto = estado)


        if evento:
            queryset = queryset.filter(cidevento = evento)

        return queryset


#______________________________________________________ CLIENTE EVENTO DETALLE
class ClienteEventoDetalleViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblclienteeventodet.objects.all().order_by('cidclienteventodet')
    serializer_class    = ClienteEventoDetalleSerializer
    def get_queryset(self):
        queryset = Tblclienteeventodet.objects.all().order_by('cidclienteventodet')

        cliente = self.request.GET.get('cli')
        eventoDetalle = self.request.GET.get('evd')
        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(cceclienteeventodet = estado)

        if cliente:
            queryset = queryset.filter(cidcliente = cliente)

        if eventoDetalle:
            queryset = queryset.filter(cideventodetalle = eventoDetalle)

        return queryset


class ClienteEventoDetalleListViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblclienteeventodet.objects.all().order_by('cidclienteventodet')
    serializer_class    = ClienteEventoDetalleListSerializer

    def get_queryset(self):
        queryset = Tblclienteeventodet.objects.all().order_by('cidclienteventodet')

        cliente = self.request.GET.get('cli')
        eventoDetalle = self.request.GET.get('evd')
        estado = self.request.GET.get('e')
        clienteEventoDetalle = self.request.GET.get('cevd')

        if estado:
            queryset = queryset.filter(cceclienteeventodet = estado)

        if cliente:
            queryset = queryset.filter(cidcliente = cliente)

        if eventoDetalle:
            queryset = queryset.filter(cideventodetalle = eventoDetalle)

        if clienteEventoDetalle:
            queryset = queryset.filter(cidclienteventodet = clienteEventoDetalle)



        return queryset

#______________________________________________________ CLIENTE EVENTO DETALLE COMPETIDORES
class ClienteEventoDetalleCompetidoresViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblclienteeventodetcomp.objects.all().order_by('cidclienteeventodetcomp')
    serializer_class    = ClienteEventoDetalleCompetidoresSerializer
    search_fields       = ('cidclienteeventodetcomp', 'cidclienteventodet', 'cideventodetcompetidor', 'cceclienteeventodetcomp')

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(ClienteEventoDetalleCompetidoresViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = Tblclienteeventodetcomp.objects.all().order_by('cidclienteeventodetcomp')

        cliEventoDetalle = self.request.GET.get('cevd')
        eventoDetalleCompetidor = self.request.GET.get('evdcom')
        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(cceclienteeventodetcomp = estado)

        if cliEventoDetalle:
            queryset = queryset.filter(cidclienteventodet = cliEventoDetalle)

        if eventoDetalleCompetidor:
            queryset = queryset.filter(cideventodetcompetidor = eventoDetalleCompetidor)

        return queryset


#______________________________________________________ CLIENTE EVENTO DETALLE COMPTEDORES PRONOSTICO
class ClienteEventoDetalleCompetidoresPronosticoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblclienteeventodetcomppronos.objects.all().order_by('cidclienteeventodetcomp')
    serializer_class    = ClienteEventoDetalleCompetidoresPronosticoSerializer
    search_fields       = ('cidclienteeventodetcomppronos', 'cideventodetpronostico', 'cidclienteeventodetcomp', 'cceclienteeventodetcomppronos', 'nvrtarifa')

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(ClienteEventoDetalleCompetidoresPronosticoViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def get_queryset(self):
        queryset = Tblclienteeventodetcomppronos.objects.all().order_by('cidclienteeventodetcomp')

        cliEventoDetalleCompetidor = self.request.GET.get('cevdcom')
        eventoDetallePronostico = self.request.GET.get('evdpro')
        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(cceclienteeventodetcomppronos = estado)

        if cliEventoDetalleCompetidor:
            queryset = queryset.filter(cidclienteeventodetcomp = cliEventoDetalleCompetidor)

        if eventoDetallePronostico:
            queryset = queryset.filter(cideventopronostico = eventoDetallePronostico)

        return queryset


#______________________________________________________ TIPO TRANSACCION
class TipoTransaccionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tbltipotrans.objects.all().order_by('cnomtipotrans')
    serializer_class    = TipoTransaccionSerializer
    def get_queryset(self):
         queryset = Tbltipotrans.objects.all().order_by('cnomtipotrans')

         estado = self.request.GET.get('e')

         if estado:
             queryset = queryset.filter(ccetipotrans = estado)

         return queryset


#______________________________________________________ CLIENTE TRANSACCION
class ClienteTransaccionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblclientetrans.objects.all().order_by('cidclientetrans')
    serializer_class    = ClienteTransaccionSerializer
    def get_queryset(self):
        queryset = Tblclientetrans.objects.all().order_by('cidclientetrans')

        cliente = self.request.GET.get('cli')
        tipoTransaccion = self.request.GET.get('tt')
        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(cceclientetrans = estado)

        if cliente:
            queryset = queryset.filter(cidcliente = cliente)

        if tipoTransaccion:
            queryset = queryset.filter(cidtipotrans = tipoTransaccion)

        return queryset

#**********************************************************************************************************************************************************************


#______________________________________________________ MENSAJE
class MensajeViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset            = Tblmensaje.objects.all().order_by('cdsmsjecorto')
    serializer_class     = MensajeSerializer

#______________________________________________________ PARAMETRO
class ParametroViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset            = Tblparametro.objects.all().order_by('cnomparametro')
    serializer_class    = ParametroSerializer

#______________________________________________________ RECURSO
class RecursoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblrecurso.objects.all().order_by('cnomrecurso')
    serializer_class    = RecursoSerializer

    def get_queryset(self):
        queryset = Tblrecurso.objects.all().order_by('cnomrecurso')

        tipoRecurso = self.request.GET.get('t')
        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(ccerecurso = estado)

        if tipoRecurso:
            queryset = queryset.filter(ccitiporecurso = tipoRecurso)

        return queryset


#**********************************************************************************************************************************************************************

#______________________________________________________ APLICACION
class AplicacionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblaplicacion.objects.all().order_by('cnomapp')
    serializer_class    = AplicacionSerializer

    def get_queryset(self):
        queryset = Tblaplicacion.objects.all().order_by('cnomapp')

        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(cceapp = estado)

        return queryset


#______________________________________________________ EVENTO OPCION
class EventoOpcionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset            = Tbleventoopcion.objects.all().order_by('nidpos')
    serializer_class    = EventoOpcionSerializer

#______________________________________________________ FUNCION
class FuncionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblfuncion.objects.all().order_by('nidpos')
    serializer_class    = FuncionSerializer

    def get_queryset(self):
        queryset = Tblfuncion.objects.all().order_by('nidpos')

        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(ccefun = estado)

        return queryset



#______________________________________________________ MODULO
class ModuloViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblmodulo.objects.all().order_by('nidpos')
    serializer_class    = ModuloSerializer

    def get_queryset(self):
        queryset = Tblmodulo.objects.all().order_by('nidpos')

        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(ccemod = estado)

        return queryset


#______________________________________________________ OPCION
class OpcionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset            = Tblopcion.objects.all().order_by('nnupos')
    serializer_class    = OpcionSerializer


#______________________________________________________ PERMISO OPCION
class PermisoOpcionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblpermisoopcion.objects.all().order_by('cidpermopc')
    serializer_class    = PermisoOpcionSerializer

    def get_queryset(self):
        queryset = Tblpermisoopcion.objects.all().order_by('cidpermopc')

        rol = self.request.GET.get('r')
        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(ccepermopc = estado)

        if rol:
            queryset = queryset.filter(cidrol = rol)

        return queryset

class PermisoOpcionListViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblpermisoopcion.objects.all().order_by('cidpermopc')
    serializer_class    = PermisoOpcionListSerializer

    def get_queryset(self):
        queryset = Tblpermisoopcion.objects.all().order_by('cidpermopc')

        rol = self.request.GET.get('r')
        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(ccepermopc = estado)

        if rol:
            queryset = queryset.filter(cidrol = rol)

        return queryset


#______________________________________________________ PERMISO EVENTO OPCION
class PermisoEventoOpcionViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset            = Tblpermisoeventoopcion.objects.all().order_by('cidpermevenopc')
    serializer_class    = PermisoEventoOpcionSerializer



#class PermisoOpcionesViewSet(viewsets.ViewSet):
#
#    def get(self, request, idOpcion):
#        opciones = Tblpermisoopcion.objects.get(cidpermopc = idOpcion)
#        opciones_serializer= PermisoEventoOpcionSerializer(opciones)
#        return Response(opciones_serializer.data) #queryset

#class PermisoEventosViewSet(viewsets.ViewSet):
#
#    def get(self, request, idEvento):
#        eventos = Tbleventoopcion.objects.get(cideventoopc = idEvento)
#        eventos_serializer= PermisoEventoOpcionSerializer(eventos)
#        return Response(eventos_serializer.data) #queryset


#______________________________________________________ BANCO
class BancoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset            = Tblbanco.objects.all().order_by('cnombanco')
    serializer_class    = BancoSerializer

#______________________________________________________ TIPO CUENTA BANCO
class TipoCuentaBancoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset            = Tbltipocuentabanco.objects.all().order_by('cnomtpctabco')
    serializer_class    = TipoCuentaBancoSerializer

#______________________________________________________ CLIENTE SOLICITUD
class ClienteSolicitudViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblclientesolicitud.objects.all().order_by('nidsolicitud')
    serializer_class    = ClienteSolicitudSerializer

    def get_queryset(self):
        queryset = Tblclientesolicitud.objects.all().order_by('nidsolicitud')

        cliente = self.request.GET.get('c')
        estado = self.request.GET.get('e')
        acreditado = self.request.GET.get('a')

        if estado:
            queryset = queryset.filter(ccesolicitud = estado)

        if acreditado:
            queryset = queryset.filter(csnacreditado = acreditado)

        if cliente:
            queryset = queryset.filter(cidcliente = cliente)


        return queryset


#______________________________________________________ PAIS
class PaisViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblpais.objects.all().order_by('cnompais')
    serializer_class    = PaisSerializer

    def get_queryset(self):
        queryset = Tblpais.objects.all().order_by('cnompais')

        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(ccepais = estado)

        return queryset


#______________________________________________________ PASS RECOVERY
class PassRecoveryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Tblpassrecovery.objects.all().order_by('dfxpassrecovery')
    serializer_class    = PassRecoverySerializer

    def get_queryset(self):
        queryset = Tblpassrecovery.objects.all().order_by('dfxpassrecovery')

        estado = self.request.GET.get('e')
        id = self.request.GET.get('id')

        if estado:
            queryset = queryset.filter(ccepais = estado)

        if id:
            queryset = queryset.filter(cidpassrecovery = id)

        return queryset


#############################################  VISTAS  #########################################
#______________________________________________________ PERMISO EVENTO OPCION
class ClienteCreditosViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Vwclientecreditos.objects.all().order_by('cnompersona')
    serializer_class    = ClienteCreditosSerializer

    def get_queryset(self):
        queryset = Vwclientecreditos.objects.all().order_by('cnompersona')

        estado = self.request.GET.get('e')

        if estado:
            queryset = queryset.filter(ccecliente = estado)

        return queryset


#______________________________________________________ CLIENTE EVENTOS
class ClienteEventosViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Vwclienteeventos.objects.all()
    serializer_class    = ClienteEventosSerializer

    def get_queryset(self):
        queryset = Vwclienteeventos.objects.all()

        cliente = self.request.GET.get('c')
        eventodetalle = self.request.GET.get('ced')
        tipo = self.request.GET.get('t')

        if cliente:
            queryset = queryset.filter(cidcliente = cliente)

        if eventodetalle:
            queryset = queryset.filter(cidclienteventodet = eventodetalle)

        if tipo:
            queryset = queryset.filter(csnmultiple = tipo)



        return queryset


#______________________________________________________ EVENTOS CON RESULTADOS
class EventosConResultadoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = Vweventoconresultado.objects.all().order_by('dfxinicio')
    serializer_class    = EventosConResultadoSerializer

    def get_queryset(self):
        queryset = Vweventoconresultado.objects.all()

        liquidado = self.request.GET.get('l')

        if liquidado:
            queryset = queryset.filter(csnliquidado = liquidado)

        return queryset



#############################################  STORE PROCEDURES  #########################################
#______________________________________________________ MENU VIEW SET
class MenuViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = SPMenu.objects.all().order_by('cidpermevenopc')
    serializer_class    = MenuSerializer

    def get_queryset(self):
        rol = self.request.GET.get('r')
        lenguaje = self.request.GET.get('l')

        queryset = SPMenu.get_menu(rol, lenguaje)

        return queryset


#______________________________________________________ PREMIOS EVENTO LISTADO
class PremiosEventoListadoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = SPPremiosEventoListado.objects.all()
    serializer_class    = PremiosEventoListadoSerializer

    def get_queryset(self):
        evento = self.request.GET.get('e')
        queryset = SPPremiosEventoListado.get_premioseventolistado(evento)

        return queryset

#______________________________________________________ PREMIOS EVENTO PUNTOS
class PremiosEventoPuntosViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = SPPremiosEventoPuntos.objects.all()
    serializer_class    = PremiosEventoPuntosSerializer

    def get_queryset(self):
        evento = self.request.GET.get('e')
        cliente = self.request.GET.get('c')
        queryset = SPPremiosEventoPuntos.get_premioseventopuntos(evento, cliente)

        return queryset


#______________________________________________________ PREMIOS EVENTO
class PremiosEventoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = SPPremiosEvento.objects.all()
    serializer_class    = PremiosEventoSerializer

    def get_queryset(self):
        evento = self.request.GET.get('e')
        queryset = SPPremiosEvento.get_premiosevento(evento)

        return queryset


#______________________________________________________ PREMIOS EVENTO LIQUIDAR
class PremiosEventoLiquidarViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = SPPremiosEventoLiquidar.objects.all()
    serializer_class    = PremiosEventoLiquidarSerializer

    def get_queryset(self):
        evento = self.request.GET.get('e')
        queryset = SPPremiosEventoLiquidar.get_premioseventoliquidar(evento)

        return queryset


#______________________________________________________ EVENTO ACTIVO ACUMULADO
class EventoActivoAcumuladoViewSet(DefaultsMixin, viewsets.ModelViewSet):
    #queryset            = SPEventoActivoAcumulado.objects.all()
    serializer_class    = EventoActivoAcumuladoSerializer

    def get_queryset(self):
        tipoevento = self.request.GET.get('te')

        queryset = SPEventoActivoAcumulado.get_eventoactivoacumulado()

        if tipoevento:
            #queryset.filter(CIdTipoEvento = tipoevento)
            queryset = filter(lambda x: x.CIdTipoEvento == tipoevento, queryset)


        return queryset



##################################################### MAIL ################################################
class SendMailSignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        username = self.request.GET.get('username')
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = self.request.GET.get('to')

        if username and from_email and to_email:

            print(username)
            print(to_email)
            print(from_email)

            subject = 'Activacion de Registro HIT'
            text_content = "Hi!\nHow are you?\nHere is the link to activate your account:\nhttp://localhost:4200/validar?id=%s" %(username)
            #html_content = "<form action='http://localhost:4200/pages/validar?ID=%S'><p>Usted se ha registrado en <strong>HIT.com</strong>, Gracias.</p><br><br>Para poder validar su registro favor presione en el boton VALIDAR REGISTRO.<br><br><br><br></form>" % username
            html_content = render_to_string('acc_active_email.html',
                                            {
                                               'username': username,
                                               'host': settings.APP_HOST,
                                            })

            #print(html_content)
            #msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            #msg.attach_alternative(html_content, "text/html")
            try:
                msg = EmailMessage(subject, html_content, from_email, [to_email])
                msg.content_subtype = "html"
                msg.send()
                #send_mail(subject, html_content, from_email, [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Email sent.') #HttpResponseRedirect('Email Sent')

        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')


##################################################### MAIL EVENTO ################################################
class SendMailEvento(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        evento = self.request.GET.get('evento')
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = self.request.GET.get('to')


        if evento and from_email and to_email:

            print(evento)
            print(to_email)
            print(from_email)

            subject = 'Registro en Evento HIT'
            text_content = "Hi!\nHow are you?\nHere is the link to activate your account:\nhttp://localhost:4200/validar?id=%s" %(evento)
            #html_content = "<form action='http://localhost:4200/pages/validar?ID=%s'><p>Usted se ha registrado un Evento <strong>HIT</strong>, Predice - Acierta y Gana</p><br><br>.<br><br><br><br></form>" % evento
            html_content = render_to_string('acc_active_email.html',
                                            {
                                               'evento': evento,
                                               'host': settings.APP_HOST,
                                            })

            #print(html_content)

            #msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            #msg.attach_alternative(html_content, "text/html")



            try:
                msg = EmailMessage(subject, html_content, from_email, [to_email])
                msg.content_subtype = "html"
                msg.send()

                #send_mail(subject, html_content, from_email, [to_email])

            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return HttpResponse('Email sent.') #HttpResponseRedirect('Email Sent')

        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')


##################################################### MAIL LIQUIDACION ################################################
class SendMailLiquidacion(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):

        from_email = settings.DEFAULT_FROM_EMAIL
        username = self.request.GET.get('username')
        to_email = self.request.GET.get('to')
        evento = self.request.GET.get('ev')
        competidor = self.request.GET.get('comp')
        pronostico = self.request.GET.get('pro')
        premio = self.request.GET.get('pre')


        if from_email and to_email:

            subject = "Usted ganó $ %s en el evento HIT: %s " % (premio, evento)
            text_content = "Hi!\nHow are you?\nHere is the  datail of your prize for event: %s" %(evento)
            #html_content = "<form action='http://localhost:4200/pages/validar?ID=%s'><p>Usted se ha registrado un Evento <strong>HIT</strong>, Predice - Acierta y Gana</p><br><br>.<br><br><br><br></form>" % evento
            html_content = render_to_string('pay_email.html',
                                            {
                                                'username': username,
                                                'evento': evento,
                                                'competidor': competidor,
                                                'pronostico': pronostico,
                                                'premio': premio,
                                            })

            #print(html_content)

            #msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            #msg.attach_alternative(html_content, "text/html")



            try:
                msg = EmailMessage(subject, html_content, from_email, [to_email])
                msg.content_subtype = "html"
                msg.send()

                #send_mail(subject, html_content, from_email, [to_email])

            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return HttpResponse('Email sent.') #HttpResponseRedirect('Email Sent')

        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')

