# create this file
# rerouting all requests that have ‘api’ in the url to the <code>apps.core.urls

from django.conf.urls import url, include
from . import views as user_views
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
                    UserViewSet,

                    PersonaViewSet,
                    PropiedadViewSet,
                    PersonaPropiedadViewSet,
                    UsuarioViewSet,
                    RolViewSet,

                    RolUsuarioViewSet,
                    RolUsuarioListViewSet,

                    ClienteViewSet,
                    TipoEventoViewSet,
                    EventoViewSet,
                    EventoDetalleViewSet,

                    EventoDetalleCompetidorViewSet,
                    EventoDetalleCompetidorListViewSet,

                    EventoDetallePronosticoViewSet,
                    EventoResultadoPronosticoViewSet,

                    EventoPuntoViewSet,

                    ClienteEventoDetalleViewSet,
                    ClienteEventoDetalleListViewSet,

                    ClienteEventoDetalleCompetidoresViewSet,

                    ClienteEventoDetalleCompetidoresPronosticoViewSet,

                    TipoTransaccionViewSet,
                    ClienteTransaccionViewSet,
                    MensajeViewSet,
                    ParametroViewSet,
                    RecursoViewSet,
                    #Seguridad
                    AplicacionViewSet,
                    EventoOpcionViewSet,
                    FuncionViewSet,
                    ModuloViewSet,
                    OpcionViewSet,

                    PermisoOpcionViewSet,
                    PermisoOpcionListViewSet,

                    PermisoEventoOpcionViewSet,

                    BancoViewSet,
                    TipoCuentaBancoViewSet,
                    ClienteSolicitudViewSet,
                    PaisViewSet,
                    PassRecoveryViewSet,




                    #VISTAS
                    ClienteCreditosViewSet,
                    EventosConResultadoViewSet,

                    #STORE PROCEDURES
                    MenuViewSet,
                    ClienteEventosViewSet,
                    PremiosEventoListadoViewSet,
                    PremiosEventoPuntosViewSet,
                    PremiosEventoViewSet,
                    PremiosEventoLiquidarViewSet,
                    EventoActivoAcumuladoViewSet,


)

# API
#router = DefaultRouter()
router = DefaultRouter(trailing_slash = False)

router.register('user', UserViewSet, base_name='user')

router.register('persona', PersonaViewSet, base_name='persona')
router.register('propiedad', PropiedadViewSet, base_name='propiedad')
router.register('personapropiedad', PersonaPropiedadViewSet, base_name='personapropiedad')
router.register('usuario', UsuarioViewSet, base_name='usuario')
router.register('rol', RolViewSet, base_name='rol')

router.register('rolusuario', RolUsuarioViewSet, base_name='rolusuario')
router.register('rolusuariolist', RolUsuarioListViewSet, base_name='rolusuario')

router.register('cliente', ClienteViewSet, base_name='cliente')
router.register('tipoevento', TipoEventoViewSet, base_name='tipoevento')
router.register('evento', EventoViewSet, base_name='evento')
router.register('eventodetalle', EventoDetalleViewSet, base_name='eventodetalle')

router.register('eventodetallecompetidor', EventoDetalleCompetidorViewSet, base_name='eventodetallecompetidor')
router.register('eventodetallecompetidorlist', EventoDetalleCompetidorListViewSet, base_name='eventodetallecompetidorlist')

router.register('eventodetallepronostico', EventoDetallePronosticoViewSet, base_name='eventodetallepronostico')
router.register('eventoresultadopronostico', EventoResultadoPronosticoViewSet, base_name='eventoresultadopronostico')

router.register('eventopunto', EventoPuntoViewSet, base_name='eventopunto')

router.register('clienteeventodetalle', ClienteEventoDetalleViewSet, base_name='clienteeventodetalle')
router.register('clienteeventodetallelist', ClienteEventoDetalleListViewSet, base_name='clienteeventodetallelist')

router.register('clienteeventodetallecompetidores', ClienteEventoDetalleCompetidoresViewSet, base_name='clienteeventodetallecompetidores')

router.register('clienteeventodetallecompetidorespronostico', ClienteEventoDetalleCompetidoresPronosticoViewSet, base_name='clienteeventodetallecompetidorespronostico')
router.register('tipotransaccion', TipoTransaccionViewSet, base_name='tipotransaccion')
router.register('clientetransaccion', ClienteTransaccionViewSet, base_name='clientetransaccion')
router.register('mensaje', MensajeViewSet, base_name='mensaje')

#**********************************************************************************************************************************************************************

router.register('parametro', ParametroViewSet, base_name='parametro')
router.register('recurso', RecursoViewSet, base_name='recurso')

#**********************************************************************************************************************************************************************

router.register('aplicacion', AplicacionViewSet, base_name='aplicacion')
router.register('eventoopcion', EventoOpcionViewSet, base_name='eventoopcion')
router.register('funcion', FuncionViewSet, base_name='funcion')
router.register('modulo', ModuloViewSet, base_name='modulo')
router.register('opcion', OpcionViewSet, base_name='opcion')

router.register('permisoopcion', PermisoOpcionViewSet, base_name='permisoopcion')
router.register('permisoopcionlist', PermisoOpcionListViewSet, base_name='permisoopcionlist')

router.register('permisoeventoopcion', PermisoEventoOpcionViewSet, base_name='permisoeventoopcion')

router.register('banco', BancoViewSet, base_name='banco')
router.register('tipocuentabanco', TipoCuentaBancoViewSet, base_name='tipocuentabanco')
router.register('clientesolicitud', ClienteSolicitudViewSet, base_name='clientesolicitud')

router.register('pais', PaisViewSet, base_name='pais')
router.register('passrecovery', PassRecoveryViewSet, base_name='passrecovery')

###################################### VISTAS #####################################
router.register('clientescreditos', ClienteCreditosViewSet, base_name='clientescreditos')
router.register('eventosconresultado', EventosConResultadoViewSet, base_name='eventosconresultado')


###################################### STORE PROCEDURES #####################################
router.register('menu', MenuViewSet, base_name='menu')
router.register('clienteeventos', ClienteEventosViewSet, base_name='clienteeventos')
router.register('premioseventolistado', PremiosEventoListadoViewSet, base_name='premioseventolistado')
router.register('premioseventopuntos', PremiosEventoPuntosViewSet, base_name='premioseventopuntos')
router.register('premiosevento', PremiosEventoViewSet, base_name='premiosevento')
router.register('premioseventoliquidar', PremiosEventoLiquidarViewSet, base_name='premioseventoliquidar')
router.register('eventoactivoacumulado', EventoActivoAcumuladoViewSet, base_name='eventoactivoacumulado')

##esta es un prueba 
urlpatterns = router.urls


