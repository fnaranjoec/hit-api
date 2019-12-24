from rest_framework.exceptions import APIException

from django.db import transaction

from .models import (
                    #CustomUser,
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
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('id', 'username', 'email', 'first_name', 'last_name', 'cellphone', 'password',)
        fields = '__all__'


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)



class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data



#________________________________________________ PERSONA
class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblpersona
        fields = '__all__'

    def update(self, instance, validate_data):
         if Tblusuario.objects.filter(cidpersona =instance.cidpersona, cceusuario='A').count()>0 and validate_data.get('ccepersona', instance.ccepersona)=='X':
              raise APIException("000000014")

         instance.cnompersona = validate_data.get('cnompersona', instance.cnompersona)
         instance.capepersona = validate_data.get('capepersona', instance.capepersona)
         instance.ccepersona = validate_data.get('ccepersona', instance.ccepersona)
         instance.dfxnacimiento = validate_data.get('dfxnacimiento', instance.dfxnacimiento)
         instance.save()
         return instance


#________________________________________________ PROPIEDAD
class PropiedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblpropiedad
        fields = '__all__'


#________________________________________________ PERSONA PROPIEDAD
class PersonaPropiedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblpersonapropiedad
        fields = '__all__'


#________________________________________________ USUARIO
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblusuario
        fields = '__all__'


#________________________________________________ ROL
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblrol
        fields = ('cidrol', 'cnomrol', 'ccerol', 'ctxurlicono')

    def update(self, instance, validate_data):
        if Tblrolusuario.objects.filter(cidrol= instance.cidrol, ccerolusuario = 'A').count() > 0  and validate_data.get('ccerol', instance.ccerol) == 'X' :
              raise APIException("000000014")
        instance.cnomrol = validate_data.get('cnomrol', instance.cnomrol)
        instance.ccerol = validate_data.get('ccerol', instance.ccerol)
        instance.ctxurlicono = validate_data.get('ctxurlicono', instance.ctxurlicono)
        instance.save()
        return instance


#________________________________________________ ROL USUARIO
class RolUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblrolusuario
        fields = ('cidrolusuario', 'cidrol', 'cidusuario', 'ccerolusuario')

    #verifico que no existan clientes  o ususarios con este rol
    def update(self, instance, validate_data):
        if Tblcliente.objects.filter(cidrolusuario= instance.cidrolusuario, ccecliente = 'A').count() > 0  and validate_data.get('ccerolusuario', instance.ccerolusuario) == 'X' :
              raise APIException("000000014")

        instance.cidrol         = validate_data.get('cidrol', instance.cidrol)
        instance.cidusuario     = validate_data.get('cidusuario', instance.cidusuario)
        instance.ccerolusuario  = validate_data.get('ccerolusuario', instance.ccerolusuario)
        instance.save()
        return instance


class RolUsuarioListSerializer(serializers.ModelSerializer):
    cidrol = RolSerializer();
    cidusuario = UsuarioSerializer();
    class Meta:
        model = Tblrolusuario
        fields = ('cidrolusuario', 'cidrol', 'cidusuario', 'ccerolusuario') #, 'cidrol', 'cidusuario'



#________________________________________________ TIPO EVENTO
class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbltipoevento
        fields = '__all__'
    def update(self, instance, validate_data):
        if Tblevento.objects.filter(cidtipoevento = instance.cidtipoevento, cceevento = 'A').count() > 0  and validate_data.get('ccetipoevento', instance.ccetipoevento) == 'X' :
            raise APIException("000000014")

        instance.cnomtipoevento = validate_data.get('cnomtipoevento', instance.cnomtipoevento)
        instance.ctxurlicono = validate_data.get('ctxurlicono', instance.ctxurlicono)
        instance.ccetipoevento = validate_data.get('ccetipoevento', instance.ccetipoevento)
        instance.save()
        return instance


#________________________________________________ EVENTO
class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblevento
        fields = '__all__'

    def update(self, instance, validate_data):
        if Tbleventodetalle.objects.filter(cidevento = instance.cidevento, cceeventodetalle = 'A').count() >0 and validate_data.get('cceevento', instance.cceevento) == 'X':
            raise APIException("000000014")

        instance.cidtipoevento = validate_data.get('cidtipoevento', instance.cidtipoevento)
        instance.cnomevento = validate_data.get('cnomevento', instance.cnomevento)
        instance.ctxurlicono = validate_data.get('ctxurlicono', instance.ctxurlicono)
        instance.cceevento = validate_data.get('cceevento', instance.cceevento)
        instance.dfxinicio = validate_data.get('dfxinicio', instance.dfxinicio)
        instance.dfxfin = validate_data.get('dfxfin', instance.dfxfin)
        instance.nflporcganadores = validate_data.get('nflporcganadores', instance.nflporcganadores)
        instance.nflporcutilidad = validate_data.get('nflporcutilidad', instance.nflporcutilidad)
        instance.nflporcimpuestos = validate_data.get('nflporcimpuestos', instance.nflporcimpuestos)
        instance.nflporccomision = validate_data.get('nflporccomision', instance.nflporccomision)
        instance.csnmultiple = validate_data.get('csnmultiple', instance.csnmultiple)
        instance.nvrevento = validate_data.get('nvrevento', instance.nvrevento)
        instance.nvrdobles = validate_data.get('nvrdobles', instance.nvrdobles)
        instance.nvrtriples = validate_data.get('nvrtriples', instance.nvrtriples)
        instance.ncandobles = validate_data.get('ncandobles', instance.ncandobles)
        instance.ncantriples = validate_data.get('ncantriples', instance.ncantriples)
        instance.csnliquidado = validate_data.get('csnliquidado', instance.csnliquidado)
        instance.dfxliquidado = validate_data.get('dfxliquidado', instance.dfxliquidado)
        instance.cidpais = validate_data.get('cidpais', instance.cidpais)
        instance.save()
        return instance

class EventoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblevento
        fields = '__all__'


#________________________________________________ EVENTO DETALLE
class EventoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbleventodetalle
        fields = ('cideventodetalle', 'cidevento', 'cnomdetalle', 'ctxurliconodetalle', 'cceeventodetalle')

    def update(self, instance, validate_data):
        if Tblclienteeventodet.objects.filter(cideventodetalle = instance.cideventodetalle, cceclienteeventodet = 'A').count() >0 and validate_data.get('cceeventodetalle', instance.cceeventodetalle) == 'X':
             raise APIException("000000014")

        if Tbleventodetpronostico.objects.filter(cideventodetalle = instance.cideventodetalle, cceeventopronostico = 'A').count() >0 and validate_data.get('cceeventodetalle', instance.cceeventodetalle) == 'X':
             raise APIException("000000014")

        if Tbleventodetcompetidor.objects.filter(cideventodetalle = instance.cideventodetalle, cceeventodetcompetidor = 'A').count() >0 and validate_data.get('cceeventodetalle', instance.cceeventodetalle) == 'X':
             raise APIException("000000014")

        instance.cidevento = validate_data.get('cidevento', instance.cidevento)
        instance.cnomdetalle = validate_data.get('cnomdetalle', instance.cnomdetalle)
        instance.ctxurliconodetalle = validate_data.get('ctxurliconodetalle', instance.ctxurliconodetalle)
        instance.cceeventodetalle = validate_data.get('cceeventodetalle', instance.cceeventodetalle)
        instance.save()
        return instance

class EventoDetalleListSerializer(serializers.ModelSerializer):
    cidevento = EventoListSerializer()
    class Meta:
        model = Tbleventodetalle
        fields = ('cideventodetalle', 'cidevento', 'cnomdetalle', 'ctxurliconodetalle', 'cceeventodetalle')


#________________________________________________ EVENTO RESULTADO PRONOSTICO
class EventoResultadoPronosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbleventoresulpronostico
        fields = '__all__'

#________________________________________________ EVENTO DETALLE PRONOSTICO
class EventoDetallePronosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbleventodetpronostico
        #fields = '__all__'
        fields = ('cideventodetpronostico', 'cnomeventopronostico', 'cceeventopronostico', 'ccicompetidor', 'cideventodetalle')


#________________________________________________ EVENTO DETALLE COMPETIDOR
class EventoDetalleCompetidorSerializer(serializers.ModelSerializer):

    #resultado_competidor = serializers.StringRelatedField(many=True)           # Solo devuelve la PK
    #resultado_competidor = EventoResultadoPronosticoSerializer(many=True)       # Devulve el objeto completo


    class Meta:
        model = Tbleventodetcompetidor
        fields = ('cideventodetcompetidor', 'cideventodetalle', 'cnomcompetidora',
                  'cnomcompetidorb', 'cceeventodetcompetidor', 'ctxurliconoa',
                  'ctxurliconob')


class EventoDetalleCompetidorListSerializer(serializers.ModelSerializer):

    #resultado_competidor = serializers.StringRelatedField(many=True)           # Solo devuelve la PK
    resultado_competidor = EventoResultadoPronosticoSerializer(many=True)       # Devuelve el objeto completo
    class Meta:
        model = Tbleventodetcompetidor
        fields = ('cideventodetcompetidor', 'cideventodetalle', 'cnomcompetidora',
                  'cnomcompetidorb', 'cceeventodetcompetidor', 'ctxurliconoa',
                  'ctxurliconob', 'resultado_competidor')


#________________________________________________ EVENTO PUNTOS
class EventoPuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbleventopunto
        fields = '__all__'


#________________________________________________ CLIENTE EVENTO DETALLE COMPETIDOR PRONOSTICO
class ClienteEventoDetalleCompetidoresPronosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblclienteeventodetcomppronos
        fields = ('cidclienteeventodetcomppronos', 'cideventodetpronostico', 'cidclienteeventodetcomp', 'cceclienteeventodetcomppronos', 'nvrtarifa')

class ClienteEventoDetalleCompetidoresPronosticoListSerializer(serializers.ModelSerializer):
    cideventodetpronostico = EventoDetallePronosticoSerializer()
    class Meta:
        model = Tblclienteeventodetcomppronos
        fields = ('cidclienteeventodetcomppronos', 'cideventodetpronostico', 'cidclienteeventodetcomp', 'cceclienteeventodetcomppronos', 'nvrtarifa')


#________________________________________________ CLIENTE EVENTO DETALLE COMPETIDOR
class ClienteEventoDetalleCompetidoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblclienteeventodetcomp
        fields = ('cidclienteeventodetcomp', 'cidclienteventodet', 'cideventodetcompetidor', 'cceclienteeventodetcomp')


class ClienteEventoDetalleCompetidoresListSerializer(serializers.ModelSerializer):
    cideventodetcompetidor = EventoDetalleCompetidorListSerializer()
    cliente_pronosticos = ClienteEventoDetalleCompetidoresPronosticoListSerializer(many=True)

    class Meta:
        model = Tblclienteeventodetcomp
        fields = ('cidclienteeventodetcomp', 'cidclienteventodet', 'cideventodetcompetidor', 'cceclienteeventodetcomp', 'cideventodetcompetidor', 'cliente_pronosticos')



#________________________________________________ CLIENTE EVENTO DETALLE
class ClienteEventoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblclienteeventodet
        fields = ('cidclienteventodet', 'cidcliente', 'cideventodetalle', 'cceclienteeventodet', 'nfltotalevento', 'dfxclienteeventodet', 'nflcreditoevento')


class ClienteEventoDetalleListSerializer(serializers.ModelSerializer):
    cideventodetalle = EventoDetalleListSerializer()
    cliente_competidores = ClienteEventoDetalleCompetidoresListSerializer(many=True)
    class Meta:
        model = Tblclienteeventodet
        fields = ('cidclienteventodet', 'cidcliente', 'cideventodetalle', 'cceclienteeventodet', 'nfltotalevento', 'dfxclienteeventodet', 'nflcreditoevento', 'cliente_competidores')





#________________________________________________ TIPO TRANSACCION
class TipoTransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbltipotrans
        fields = '__all__'


#________________________________________________ CLIENTE TRANSACCION
class ClienteTransaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblclientetrans
        #fields = '__all__'
        fields = ('cidclientetrans', 'cidtipotrans', 'cidcliente', 'dfxtrans', 'nflvalor', 'cdstrans', 'cceclientetrans', 'cidusuario')



#________________________________________________ CLIENTE
class ClienteSerializer(serializers.ModelSerializer):
    #transacciones = ClienteTransaccionSerializer(many=True)
    class Meta:
        model = Tblcliente
        fields = ('cidcliente','cidrolusuario','ccecliente','nflcreditocliente', 'total_creditos')

"""
    def create(self, validated_data):
        transacciones = validated_data.pop('transacciones')
        instance = Order.objects.create(**validated_data)
        for transaccion in transacciones:
            instance.transacciones.add(transaccion)

        return instance
"""


#________________________________________________ MENSAJE
class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblmensaje
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MensajeSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.query_params.get('fields'):
           fields = request.query_params.get('fields')
           if fields:
              fields = fields.split(',')
              allowed = set(fields)
              existing = set(self.fields.keys())
              for field_name in existing - allowed:
                  self.fields.pop(field_name)


#**********************************************************************************************************************************************************************


#________________________________________________ PARAMETRO
class ParametroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblparametro
        fields = '__all__'


#________________________________________________ RECURSO
class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblrecurso
        fields = '__all__'



#**********************************************************************************************************************************************************************

#________________________________________________ APLICACION
class AplicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblaplicacion
        fields = '__all__'


#________________________________________________ EVENTO OPCION
class EventoOpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tbleventoopcion
        fields = '__all__'


#________________________________________________ FUNCION
class FuncionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblfuncion
        fields = '__all__'


#________________________________________________ MODULO
class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblmodulo
        fields = '__all__'

#________________________________________________ OPCION
class OpcionSerializer(serializers.ModelSerializer):
   class Meta:
        model = Tblopcion
        fields = '__all__'



#________________________________________________ PERMISO OPCION
class PermisoOpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblpermisoopcion
        fields = ('cidpermopc', 'cidrol', 'cidopc', 'ccepermopc')


class PermisoOpcionListSerializer(serializers.ModelSerializer):
    cidopc = OpcionSerializer();
    permisoevento_opcion = serializers.SerializerMethodField('_get_children')

    def _get_children(self, obj):
        serializer = PermisoEventoOpcionSerializer(obj.child_list(), many=True)
        return serializer.data

    class Meta:
        model = Tblpermisoopcion
        fields = ('cidpermopc', 'cidrol', 'cidopc', 'ccepermopc', 'permisoevento_opcion')


#________________________________________________ PERMISO EVENTO OPCION
class PermisoEventoOpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tblpermisoeventoopcion
        fields = ('cidpermevenopc', 'cideventoopc', 'cidpermopc', 'ccepermevenopc')

class PermisoEventoOpcionListSerializer(serializers.ModelSerializer):
    cideventoopc = EventoOpcionSerializer();
    cidpermopc =  PermisoOpcionSerializer();
    class Meta:
        model = Tblpermisoeventoopcion
        fields = ('cidpermevenopc', 'cideventoopc', 'cidpermopc', 'ccepermevenopc')


#________________________________________________ BANCO
class BancoSerializer(serializers.ModelSerializer):
   class Meta:
        model = Tblbanco
        fields = '__all__'

#________________________________________________ TIPO CUENTA BANCO
class TipoCuentaBancoSerializer(serializers.ModelSerializer):
   class Meta:
        model = Tbltipocuentabanco
        fields = '__all__'

#________________________________________________ CLIENTE SOLICITUD
class ClienteSolicitudSerializer(serializers.ModelSerializer):
   class Meta:
        model = Tblclientesolicitud
        fields = '__all__'

#________________________________________________ PAIS
class PaisSerializer(serializers.ModelSerializer):
   class Meta:
        model = Tblpais
        fields = '__all__'

#________________________________________________ PASS RECOVERY
class PassRecoverySerializer(serializers.ModelSerializer):
   class Meta:
        model = Tblpassrecovery
        #fields = ('cidpassrecovery', 'cnomusuario', 'dfxpassrecovery', 'ccepassrecovery', 'nnuminutos')
        fields = '__all__'

##################################  VISTAS  #############################################
#________________________________________________ CLIENTE CREDITOS
class ClienteCreditosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vwclientecreditos
        fields = '__all__'

#________________________________________________ CLIENTE CREDITOS
class ClienteEventosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vwclienteeventos
        fields = '__all__'

#________________________________________________ EVENTOS CON RESULTADO
class EventosConResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vweventoconresultado
        fields = '__all__'


##################################  STORE PROCEDURE  #############################################
#________________________________________________ MENU
class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = SPMenu
        fields = '__all__' #('title', 'icon', 'link', 'home',)


#________________________________________________ PREMIOS EVENTO LISTADO
class PremiosEventoListadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SPPremiosEventoListado
        fields = '__all__'

#________________________________________________ PREMIOS EVENTO PUNTOS
class PremiosEventoPuntosSerializer(serializers.ModelSerializer):

    class Meta:
        model = SPPremiosEventoPuntos
        fields = '__all__'

#________________________________________________ PREMIOS EVENTO
class PremiosEventoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SPPremiosEvento
        fields = '__all__'

#________________________________________________ PREMIOS EVENTO LIQUIDAR
class PremiosEventoLiquidarSerializer(serializers.ModelSerializer):

    class Meta:
        model = SPPremiosEventoLiquidar
        fields = '__all__'

#________________________________________________ EVENTO ACTIVO ACUMULADO
class EventoActivoAcumuladoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SPEventoActivoAcumulado
        fields = '__all__'



"""
#________________________________________________ CLIENTE EVENTOS
class ClienteEventosSerializer(serializers.ModelSerializer):

    class Meta:
        model = SPClienteEventos
        fields = ('ID', 'CIdCliente', 'CNomDetalle', 'CNomEvento', 'CSNMultiple', 'NFlTotalEvento', 'DFxClienteEventoDet', 'CNomCompetidorA', 'CNomCompetidorB', 'CTxUrlIconoA', 'CTxUrlIconoB', 'CNomEventoPronostico', 'CCiCompetidor')
"""
