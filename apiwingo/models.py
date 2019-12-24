# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Cuando quiero generar una nueva migracion
# python manage.py makemigrations --empty apiwingo
# python manage.py migrate


from __future__ import unicode_literals

from django.conf import settings
from django.db.models import Sum
from django.db import models
from django.db import connection
from django.utils.encoding import smart_text as smart_unicode
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# ***  SIGNALS
from django.core.signals import request_finished
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver

# *** EMAIL
from django.core.mail import send_mail, send_mass_mail, BadHeaderError
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, Http404
from rest_framework.response import Response
from rest_framework import generics, authentication, permissions, status, viewsets
from api_wingo import settings

# *** CELERY
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task


import uuid
import datetime
import django.conf as conf
import json
import computed_property



"""
from .managers import (
                      TbleventoManager,

                      )
"""


"""
class singleton:

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
"""


class User(AbstractUser):
    email = models.CharField(max_length=254, blank=True, null=True)
    cellphone = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    pin = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=36, blank=True, null=True)
    picture = models.CharField(max_length=100, blank=False, null=False, default='user.png')

"""
#******************************************************* djando models ********************************************************
class CustomUser(AbstractUser):
    cellphone = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.email
"""



#______________________________________ PERSONA
#@singleton
class Tblpersona(models.Model):

    cidpersona = models.CharField(db_column='CIdPersona', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnompersona = models.CharField(db_column='CNomPersona', max_length=150, blank=False, null=False)  # Field name made lowercase.
    capepersona = models.CharField(db_column='CApePersona', max_length=150, blank=False, null=False)  # Field name made lowercase.
    ccepersona = models.CharField(db_column='CCePersona', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    dfxnacimiento = models.DateField(db_column='DFxNacimiento', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.cidpersona + ' / ' + self.capepersona + ', ' + self.cnompersona)

    class Meta:
        managed = True
        db_table = 'tblpersona'
        verbose_name_plural = 'tblpersonas'
        ordering = ('capepersona','cnompersona', )


#______________________________________ PROPIEDAD
class Tblpropiedad(models.Model):
    cidpropiedad = models.CharField(db_column='CIdPropiedad', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnompropiedad = models.CharField(db_column='CNomPropiedad', unique=True, max_length=100, blank=False, null=False)  # Field name made lowercase.
    ctxetiqueta = models.CharField(db_column='CTxEtiqueta', max_length=50, blank=False, null=False)  # Field name made lowercase.
    ccitipodato = models.CharField(db_column='CCiTipoDato', max_length=1, blank=False, null=False)  # Field name made lowercase.
    nnulongitud = models.SmallIntegerField(db_column='NNuLongitud', default=0, blank=False, null=False)  # Field name made lowercase.
    ccepropiedad = models.CharField(db_column='CCePropiedad', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.cidpropiedad + ' / ' + self.cnompropiedad)

    class Meta:
        managed = True
        db_table = 'tblpropiedad'
        verbose_name_plural = 'tblpropiedades'
        ordering = ('cnompropiedad', )


#______________________________________ PERSONA PROPIEDAD
class Tblpersonapropiedad(models.Model):
    cidpersonapropiedad = models.CharField(db_column='CIdPersonaPropiedad', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidpropiedad = models.ForeignKey('Tblpropiedad', models.DO_NOTHING, db_column='CIdPropiedad')  # Field name made lowercase.
    cidpersona = models.ForeignKey('Tblpersona', models.DO_NOTHING, db_column='CIdPersona')  # Field name made lowercase.
    ctxvalorpropiedad = models.TextField(db_column='CTxValorPropiedad')  # Field name made lowercase.

    def __str__(self):
        return str(self.cidpersonapropiedad)

    class Meta:
        managed = True
        db_table = 'tblpersonapropiedad'
        verbose_name_plural = 'tblpersonapropiedades'
        ordering = ('cidpersonapropiedad', )



#______________________________________ USUARIO
class Tblusuario(models.Model):
    cidusuario = models.CharField(db_column='CIdUsuario', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidpersona = models.ForeignKey('Tblpersona', models.DO_NOTHING, db_column='CIdPersona')  # Field name made lowercase.
    cnomusuario = models.CharField(db_column='CNomUsuario', unique=True, max_length=50, blank=False, null=False)  # Field name made lowercase.
    ctxclave = models.CharField(db_column='CTxClave', max_length=255, blank=False, null=False)  # Field name made lowercase.
    ctxcorreo = models.CharField(db_column='CTxCorreo', unique=True, max_length=150, blank=False, null=False)  # Field name made lowercase.
    cnucelular = models.CharField(db_column='CNuCelular', unique=True, max_length=20, blank=False, null=False)  # Field name made lowercase.
    cceusuario = models.CharField(db_column='CCeUsuario', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    csnvalidado = models.CharField(db_column='CSNValidado', max_length=1, default='N', blank=False, null=False)  # Field name made lowercase.
    ctxurlicono = models.CharField(db_column='CTxUrlIcono', max_length=500, blank=True, null=True)  # Field name made lowercase.
    nnupin = models.IntegerField(db_column='NNuPin', default=0, blank=False, null=False)  # Field name made lowercase.
    cidpais = models.ForeignKey('Tblpais', models.DO_NOTHING, db_column='CIdPais', default='')  # Field name made lowercase.

    def __str__(self):
        return str(self.cidusuario + ' / ' + self.cnomusuario)

    class Meta:
        managed = True
        db_table = 'tblusuario'
        verbose_name_plural = 'tblusuarios'
        ordering = ('cnomusuario', )


#______________________________________ ROL
class Tblrol(models.Model):
    cidrol = models.CharField(db_column='CIdRol', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnomrol = models.CharField(db_column='CNomRol', unique=True, max_length=100)  # Field name made lowercase.
    ccerol = models.CharField(db_column='CCeRol', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    ctxurlicono = models.CharField(db_column='CTxUrlIcono', max_length=500, default='', blank=False, null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.cidrol + ' / ' + self.cnomrol)

    class Meta:
        managed = True
        db_table = 'tblrol'
        verbose_name_plural = 'roles'
        ordering = ('cnomrol', )


#______________________________________ ROL USUARIO
class Tblrolusuario(models.Model):
    cidrolusuario = models.CharField(db_column='CIdRolUsuario', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidrol = models.ForeignKey('Tblrol', models.DO_NOTHING, db_column='cidrol', default='', related_name='rol')  # Field name made lowercase.CIdRol
    cidusuario = models.ForeignKey('Tblusuario', models.DO_NOTHING, db_column='CIdUsuario', default='', related_name='rol_usuario')  # Field name made lowercase.
    ccerolusuario = models.CharField(db_column='CCeRolUsuario', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.cidrolusuario + ',' + self.cidrolusuario)

    class Meta:
        managed = True
        db_table = 'tblrolusuario'
        verbose_name_plural = 'tblrolusuarios'
        ordering = ('cidrolusuario', )



#______________________________________ TIPO EVENTO
class Tbltipoevento(models.Model):
    #def hex_uuid():
    #   return uuid.uuid4()

    cidtipoevento = models.CharField(db_column='CIdTipoEvento', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnomtipoevento = models.CharField(db_column='CNomTipoEvento', unique=True, max_length=50, blank=False, null=False)  # Field name made lowercase.
    ctxurlicono = models.CharField(db_column='CTxUrlIcono', max_length=500, blank=False, null=False)  # Field name made lowercase.
    ccetipoevento = models.CharField(db_column='CCeTipoEvento', max_length=1, default='A' , blank=False, null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.cidtipoevento + ' / ' + self.cnomtipoevento)

    class Meta:
        managed = True
        db_table = 'tbltipoevento'
        verbose_name_plural = 'tbltipoeventos'
        ordering = ('cnomtipoevento', )


#______________________________________ EVENTO
class Tblevento(models.Model):

    cidevento = models.CharField(db_column='CIdEvento', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidtipoevento = models.ForeignKey('Tbltipoevento', models.DO_NOTHING, db_column='CIdTipoEvento')  # Field name made lowercase.
    cnomevento = models.CharField(db_column='CNomEvento', max_length=255, blank=False, null=False)  # Field name made lowercase.
    ctxurlicono = models.CharField(db_column='CTxUrlIcono', max_length=500, blank=False, null=False)  # Field name made lowercase.
    cceevento = models.CharField(db_column='CCeEvento', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    dfxinicio = models.DateTimeField(db_column='DFxInicio')  # Field name made lowercase.
    dfxfin = models.DateTimeField(db_column='DFxFin')  # Field name made lowercase.
    nflporcganadores = models.FloatField(db_column='NFlPorcGanadores', default=0, blank=False, null=False)  # Field name made lowercase.
    nflporcutilidad = models.FloatField(db_column='NFlPorcUtilidad', default=0, blank=False, null=False)  # Field name made lowercase.
    nflporcimpuestos = models.FloatField(db_column='NFlPorcImpuestos', default=0, blank=False, null=False)  # Field name made lowercase.
    nflporccomision = models.FloatField(db_column='NFlPorcComision', default=0, blank=False, null=False)  # Field name made lowercase.
    csnmultiple = models.CharField(db_column='CSNMultiple', max_length=1, default='N', blank=False, null=False)  # Field name made lowercase.
    nvrevento = models.FloatField(db_column='NVrEvento', default=0.00, blank=False, null=False)  # Field name made lowercase.
    nvrdobles = models.FloatField(db_column='NVrDobles', default=0.00, blank=False, null=False)  # Field name made lowercase.
    nvrtriples = models.FloatField(db_column='NVrTriples', default=0.00, blank=False, null=False)  # Field name made lowercase.
    ncandobles = models.IntegerField(db_column='NCanDobles', default=0, blank=False, null=False)  # Field name made lowercase.
    ncantriples = models.IntegerField(db_column='NCanTriples', default=0, blank=False, null=False)  # Field name made lowercase.
    csnliquidado = models.CharField(db_column='CSNLiquidado', max_length=1, default='N', blank=False, null=False)  # Field name made lowercase.
    dfxliquidado = models.DateTimeField(db_column='DFxLiquidado' ,blank=True, null=True)  # Field name made lowercase.
    cidpais = models.ForeignKey('Tblpais', models.DO_NOTHING, db_column='CIdPais', default='')  # Field name made lowercase.

    #objects = TbleventoManager()

    def __str__(self):
        return self.cidevento + ' / ' + self.cnomevento

    class Meta:
        managed = True
        db_table = 'tblevento'
        verbose_name_plural = 'tbleventos'
        ordering = ('cnomevento', )


#______________________________________ EVENTO DETALLE
class Tbleventodetalle(models.Model):
    cideventodetalle = models.CharField(db_column='CIdEventoDetalle', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidevento = models.ForeignKey('Tblevento', models.DO_NOTHING, db_column='CIdEvento')  # Field name made lowercase.
    cnomdetalle = models.CharField(db_column='CNomDetalle', max_length=255, blank=False, null=False)  # Field name made lowercase.
    ctxurliconodetalle = models.CharField(db_column='CTxUrlIconoDetalle', max_length=500, blank=False, null=False)  # Field name made lowercase.
    cceeventodetalle = models.CharField(db_column='CCeEventoDetalle', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.cideventodetalle + ' / ' + self.cnomdetalle)

    class Meta:
        managed = True
        db_table = 'tbleventodetalle'
        verbose_name_plural = 'tbleventodetalles'
        ordering = ('cnomdetalle', )


#______________________________________ EVENTO DETALLE COMPETIDOR
class Tbleventodetcompetidor(models.Model):
    cideventodetcompetidor = models.CharField(db_column='CIdEventoDetCompetidor', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cideventodetalle = models.ForeignKey('Tbleventodetalle', models.DO_NOTHING, db_column='CIdEventoDetalle')  # Field name made lowercase.
    cnomcompetidora = models.CharField(db_column='CNomCompetidorA', max_length=255, blank=False, null=False)  # Field name made lowercase.
    cnomcompetidorb = models.CharField(db_column='CNomCompetidorB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cceeventodetcompetidor = models.CharField(db_column='CCeEventoDetCompetidor', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    ctxurliconoa = models.CharField(db_column='CTxUrlIconoA', max_length=500, default='', blank=False, null=False)  # Field name made lowercase.
    ctxurliconob = models.CharField(db_column='CTxUrlIconoB', max_length=500, default='', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.cideventodetcompetidor + ' / ' + self.cnomcompetidora + ' / ' + self.cnomcompetidorb)

    class Meta:
        managed = True
        db_table = 'tbleventodetcompetidor'
        verbose_name_plural = 'tbleventodetcompetidores'
        ordering = ('cnomcompetidora', )



#______________________________________ EVENTO DETALLE PRONOSTICO
class Tbleventodetpronostico(models.Model):
    cideventodetpronostico = models.CharField(db_column='CIdEventoDetPronostico', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cideventodetalle = models.ForeignKey('Tbleventodetalle', models.DO_NOTHING, db_column='CIdEventoDetalle')  # Field name made lowercase.
    cnomeventopronostico = models.CharField(db_column='CNomEventoPronostico', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cceeventopronostico = models.CharField(db_column='CCeEventoPronostico', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    ccicompetidor = models.CharField(db_column='CCiCompetidor', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.cideventodetpronostico + ' / ' + self.cnomeventopronostico)

    class Meta:
        managed = True
        db_table = 'tbleventodetpronostico'
        verbose_name_plural = 'tbleventodetpronosticos'
        ordering = ('cnomeventopronostico', )



#______________________________________ EVENTO RESULTADO PRONOSTICO
class Tbleventoresulpronostico(models.Model):
    cideventoresulpronostico = models.CharField(db_column='CidEventoResulPronostico', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cideventodetpronostico = models.ForeignKey('Tbleventodetpronostico', models.DO_NOTHING, db_column='CIdEventoDetPronostico')  # Field name made lowercase.
    cideventodetcompetidor = models.ForeignKey('Tbleventodetcompetidor', models.DO_NOTHING, db_column='CIdEventoDetCompetidor', default='', related_name='resultado_competidor')  # Field name made lowercase.
    ctxeventoresulcoma = models.CharField(db_column='CTxEventoResulComA', max_length=50, default='', blank=False, null=False)  # Field name made lowercase.
    ctxeventoresulcomb = models.CharField(db_column='CTxEventoResulComB', max_length=50, default='', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.cideventoresulpronostico)

    class Meta:
        managed = True
        db_table = 'tbleventoresulpronostico'
        verbose_name_plural = 'tbleventoresulpronosticos'
        ordering = ('cideventoresulpronostico', )


#______________________________________ EVENTO PUNTO
class Tbleventopunto(models.Model):
    cideventopunto = models.CharField(db_column='CIdEventoPunto', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidevento = models.ForeignKey(Tblevento, models.DO_NOTHING, db_column='CIdEvento')  # Field name made lowercase.
    ncanpuntos = models.SmallIntegerField(db_column='NCanPuntos', default=0, blank=False, null=False)  # Field name made lowercase.
    nflporcpuntos = models.FloatField(db_column='NFlPorcPuntos', default=0, blank=False, null=False)  # Field name made lowercase.
    cceeventopunto = models.CharField(db_column='CCeEventoPunto', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tbleventopunto'
        verbose_name_plural = 'tbleventopuntos'
        ordering = ('ncanpuntos', )


#______________________________________ CLIENTE EVENTO DETALLE
class Tblclienteeventodet(models.Model):
    cidclienteventodet = models.CharField(db_column='CIdClientEventoDet', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase. #default=uuid.uuid4, editable=False,
    cidcliente = models.ForeignKey('Tblcliente', models.DO_NOTHING, db_column='CIdCliente')  # Field name made lowercase.
    cideventodetalle = models.ForeignKey('Tbleventodetalle', models.DO_NOTHING, db_column='CIdEventoDetalle')  # Field name made lowercase.
    cceclienteeventodet = models.CharField(db_column='CCeClienteEventoDet', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    nfltotalevento = models.FloatField(db_column='NFlTotalEvento', default=0, blank=False, null=False)  # Field name made lowercase.
    dfxclienteeventodet = models.DateTimeField(db_column='DFxClienteEventoDet', default='CURRENT_DATETIME', blank=False, null=False)  # Field name made lowercase.
    nflcreditoevento = models.FloatField(db_column='NFlCreditoEvento', default=0, blank=False, null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.cidclienteventodet)

    class Meta:
        managed = True
        db_table = 'tblclienteeventodet'
        verbose_name_plural = 'tblclienteeventodetalles'
        ordering = ('cidclienteventodet', )



#______________________________________ CLIENTE EVENTO DETALLE COMPETIDOR
class Tblclienteeventodetcomp(models.Model):
    cidclienteeventodetcomp = models.CharField(db_column='CIdClienteEventoDetComp', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase. #default=uuid.uuid4, editable=False,
    cidclienteventodet = models.ForeignKey('Tblclienteeventodet', models.DO_NOTHING, db_column='CIdClientEventoDet', related_name='cliente_competidores')  # Field name made lowercase.
    cideventodetcompetidor = models.ForeignKey('Tbleventodetcompetidor', models.DO_NOTHING, db_column='CIdEventoDetCompetidor')  # Field name made lowercase.
    cceclienteeventodetcomp = models.CharField(db_column='CCeClienteEventoDetComp', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    def __str__(self):
        return str(self.cidclienteeventodetcomp)
    class Meta:
        managed = True
        db_table = 'tblclienteeventodetcomp'
        verbose_name_plural = 'tblclienteeventodetcompetidores'
        ordering = ('cidclienteeventodetcomp', )

#______________________________________ CLIENTE EVENTO DETALLE COMPETIDOR PRONOSTICO
class Tblclienteeventodetcomppronos(models.Model):
    cidclienteeventodetcomppronos = models.CharField(db_column='CIdClienteEventoDetCompPronos', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cideventodetpronostico = models.ForeignKey('Tbleventodetpronostico', models.DO_NOTHING, db_column='CIdEventoDetPronostico')  # Field name made lowercase.
    cidclienteeventodetcomp = models.ForeignKey('Tblclienteeventodetcomp', models.DO_NOTHING, db_column='CIdClienteEventoDetComp', related_name='cliente_pronosticos')  # Field name made lowercase.
    cceclienteeventodetcomppronos = models.CharField(db_column='CCeClienteEventoDetCompPronos', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    nvrtarifa = models.FloatField(db_column='NVrTarifa', default=0, blank=False, null=False)  # Field name made lowercase.
    def __str__(self):
        return str(self.cidclienteeventodetcomppronos)
    class Meta:
        managed = True
        db_table = 'tblclienteeventodetcomppronos'
        verbose_name_plural = 'tblclienteeventodetcomppronosticos'
        ordering = ('cidclienteeventodetcomppronos', )
#______________________________________ TIPO TRANSACCION
class Tbltipotrans(models.Model):
    cidtipotrans = models.CharField(db_column='CIdTipoTrans', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnomtipotrans = models.CharField(db_column='CNomTipoTrans', unique=True, max_length=50)  # Field name made lowercase.
    ccetipotrans = models.CharField(db_column='CCeTipoTrans', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    def __str__(self):
        return str(self.cidtipotrans + ' / ' + self.cnomtipotrans)
    class Meta:
        managed = True
        db_table = 'tbltipotrans'
        verbose_name_plural = 'tbltipotransacciones'
        ordering = ('cnomtipotrans', )
#______________________________________ CLIENTE TRANSACCION
class Tblclientetrans(models.Model):
    cidclientetrans = models.CharField(db_column='CIdClienteTrans', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidtipotrans = models.ForeignKey('Tbltipotrans', models.DO_NOTHING, db_column='CIdTipoTrans')  # Field name made lowercase.
    cidcliente = models.ForeignKey('Tblcliente', models.DO_NOTHING, db_column='CIdCliente')  # Field name made lowercase.
    dfxtrans = models.DateTimeField(db_column='DFxTrans')  # Field name made lowercase.
    nflvalor = models.FloatField(db_column='NFlValor')  # Field name made lowercase.
    cdstrans = models.CharField(db_column='CDsTrans', max_length=500, blank=True, null=True)  # Field name made lowercase.
    cceclientetrans = models.CharField(db_column='CCeClienteTrans', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    cidusuario = models.ForeignKey('Tblusuario', models.DO_NOTHING, db_column='CIdUsuario', default='')  # Field name made lowercase.
    def __str__(self):
        return str(self.cidclientetrans)

    class Meta:
        managed = True
        db_table = 'tblclientetrans'
        verbose_name_plural = 'tblclientetransacciones'
        ordering = ('cidclientetrans', )



#______________________________________ CLIENTE
class Tblcliente(models.Model):
    cidcliente = models.CharField(db_column='CIdCliente', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidrolusuario = models.ForeignKey('Tblrolusuario', models.DO_NOTHING, db_column='CIdRolUsuario')  # Field name made lowercase.
    ccecliente = models.CharField(db_column='CCeCliente', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    nflcreditocliente = models.FloatField(db_column='NFlCreditoCliente', default=0, blank=False, null=False)  # Field name made lowercase.

    @property
    def total_creditos(self):
        qs = Tblclientetrans.objects.values('cidcliente').anotate(total_creditos=Sum('nflvalor'))
        return qs['total_creditos']

    def __str__(self):
        return str(self.cidcliente)

    class Meta:
        managed = True
        db_table = 'tblcliente'
        verbose_name_plural = 'tblclientes'
        ordering = ('cidcliente', )



#______________________________________ MENSAJE
class Tblmensaje(models.Model):
    cidmensaje = models.CharField(db_column='CIdMensaje', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cdstipoalerta = models.CharField(db_column='CDsTipoAlerta', default='success', max_length=20, blank=False, null=False)  # Field name made lowercase.
    nnuduracion = models.SmallIntegerField(db_column='NNuDuracion', default=3, blank=False, null=False)  # Field name made lowercase.
    cdstitle_en = models.CharField(db_column='CDsTitle_en', default='', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cdstitle_es = models.CharField(db_column='CDsTitle_es', default='', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cdstitle_ru = models.CharField(db_column='CDsTitle_ru', default='', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cdstitle_zh = models.CharField(db_column='CDsTitle_zh', default='', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cdsmsje_en = models.CharField(db_column='CDsMsje_en', default='', max_length=500, blank=False, null=False)  # Field name made lowercase.
    cdsmsje_es = models.CharField(db_column='CDsMsje_es', default='', max_length=500, blank=False, null=False)  # Field name made lowercase.
    cdsmsje_ru = models.CharField(db_column='CDsMsje_ru', default='', max_length=500, blank=False, null=False)  # Field name made lowercase.
    cdsmsje_zh = models.CharField(db_column='CDsMsje_zh', default='', max_length=500, blank=False, null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.cidmensaje + ' / ' + self.cdsmsjecorto)

    class Meta:
        managed = True
        db_table = 'tblmensaje'
        verbose_name_plural = 'tblmensajes'
        ordering = ('cidmensaje', )



#**********************************************************************************************************************************************************************


#______________________________________ PARAMETRO
class Tblparametro(models.Model):
    cidparametro = models.CharField(db_column='CIdParametro', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnomparametro = models.CharField(db_column='CNomParametro', unique=True, max_length=255)  # Field name made lowercase.
    ctxtexto = models.CharField(db_column='CTxTexto', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nnuvalor = models.FloatField(db_column='NNuValor')  # Field name made lowercase.
    cdsvaloresposibles = models.CharField(db_column='CDsValoresPosibles', max_length=500)  # Field name made lowercase.

    def __str__(self):
        return str(self.cidparametro + ' / ' + self.cnomparametro)

    class Meta:
        managed = True
        db_table = 'tblparametro'
        verbose_name_plural = 'tblparametros'
        ordering = ('cidparametro', )


#______________________________________ RECURSO
class Tblrecurso(models.Model):
    cidrecurso = models.CharField(db_column='CIdRecurso', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    ccitiporecurso = models.CharField(db_column='CCiTipoRecurso', max_length=3)  # Field name made lowercase.
    cnomrecurso = models.CharField(db_column='CNomRecurso', max_length=255)  # Field name made lowercase.
    ctxrutarecurso = models.CharField(db_column='CTxRutaRecurso', max_length=500)  # Field name made lowercase.
    ccerecurso = models.CharField(db_column='CCeRecurso', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblrecurso'
        verbose_name_plural = 'tblrecursos'
        ordering = ('cidrecurso', )



#**********************************************************************************************************************************************************************


#______________________________________ APLICACION
class Tblaplicacion(models.Model):
    cidapp = models.CharField(db_column='CIdApp', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnomapp = models.CharField(db_column='CNomApp', unique=True, max_length=100, blank=False, null=False)  # Field name made lowercase.
    csnocultaropcnoautr = models.CharField(db_column='CSNOcultarOpcNoAutr', max_length=1, blank=False, null=False)  # Field name made lowercase.
    csnaccesorapido = models.CharField(db_column='CSNAccesoRapido', max_length=1, blank=False, null=False)  # Field name made lowercase.
    cceapp = models.CharField(db_column='CCeApp', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblaplicacion'
        verbose_name_plural = 'tblaplicaciones'
        ordering = ('cidapp', )


#______________________________________ EVENTO OPCION
class Tbleventoopcion(models.Model):
    cideventoopc = models.CharField(db_column='CIdEventoOpc', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    ccievento = models.CharField(db_column='CCiEvento', max_length=20, blank=False, null=False)  # Field name made lowercase.
    cnomevento_en = models.CharField(db_column='CNomEvento_en', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cnomevento_es = models.CharField(db_column='CNomEvento_es', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cnomevento_ru = models.CharField(db_column='CNomEvento_ru', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cnomevento_zh = models.CharField(db_column='CNomEvento_zh', max_length=100, blank=False, null=False)  # Field name made lowercase.
    ccisiglas = models.CharField(db_column='CCiSiglas', max_length=3, blank=False, null=False)  # Field name made lowercase.
    nidpos = models.SmallIntegerField(db_column='NIdPos', blank=False, null=False)  # Field name made lowercase.
    cceevento = models.CharField(db_column='CCeEvento', max_length=1)  # Field name made lowercase.
    cidapp = models.ForeignKey('Tblaplicacion', models.DO_NOTHING, db_column='CIdApp')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tbleventoopcion'
        verbose_name_plural = 'tbleventoopciones'
        ordering = ('cideventoopc', )

#______________________________________ FUNCION
class Tblfuncion(models.Model):
    cidfun = models.CharField(db_column='CIdFun', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidapp = models.ForeignKey('Tblaplicacion', models.DO_NOTHING, db_column='CIdApp')  # Field name made lowercase.
    ccifun = models.CharField(db_column='CCiFun', max_length=3, blank=False, null=False)  # Field name made lowercase.
    cnomfun_en = models.CharField(db_column='CNomFun_en', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cnomfun_es = models.CharField(db_column='CNomFun_es', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cnomfun_ru = models.CharField(db_column='CNomFun_ru', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cnomfun_zh = models.CharField(db_column='CNomFun_zh', max_length=100, blank=False, null=False)  # Field name made lowercase.
    nidpos = models.SmallIntegerField(db_column='NIdPos')  # Field name made lowercase.
    ccefun = models.CharField(db_column='CCeFun', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblfuncion'
        verbose_name_plural = 'tblfunciones'
        ordering = ('cidfun', )


#______________________________________ MODULO
class Tblmodulo(models.Model):
    cidmod = models.CharField(db_column='CIdMod', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidapp = models.ForeignKey('Tblaplicacion', models.DO_NOTHING, db_column='CIdApp')  # Field name made lowercase.
    cnommod_en = models.CharField(db_column='CNomMod_en', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cnommod_es = models.CharField(db_column='CNomMod_es', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cnommod_ru = models.CharField(db_column='CNomMod_ru', max_length=100, blank=False, null=False)  # Field name made lowercase.
    cnommod_zh = models.CharField(db_column='CNomMod_zh', max_length=100, blank=False, null=False)  # Field name made lowercase.
    ccimod = models.CharField(db_column='CCiMod', max_length=3, blank=False, null=False)  # Field name made lowercase.
    nidpos = models.SmallIntegerField(db_column='NIdPos')  # Field name made lowercase.
    ccemod = models.CharField(db_column='CCeMod', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblmodulo'
        verbose_name_plural = 'tblmodulos'
        ordering = ('cidmod', )

#______________________________________ OPCION
class Tblopcion(models.Model):
    cidopc = models.CharField(db_column='CIdOpc', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidapp = models.ForeignKey('Tblaplicacion', models.DO_NOTHING, db_column='CIdApp')  # Field name made lowercase.
    cidfun = models.ForeignKey('Tblfuncion', models.DO_NOTHING, db_column='CIdFun')  # Field name made lowercase.
    ctxmenu_en = models.CharField(db_column='CTxMenu_en', max_length=100, blank=False, null=False)  # Field name made lowercase.
    ctxmenu_es = models.CharField(db_column='CTxMenu_es', max_length=100, blank=False, null=False)  # Field name made lowercase.
    ctxmenu_ru = models.CharField(db_column='CTxMenu_ru', max_length=100, blank=False, null=False)  # Field name made lowercase.
    ctxmenu_zh = models.CharField(db_column='CTxMenu_zh', max_length=100, blank=False, null=False)  # Field name made lowercase.
    nnunivel = models.SmallIntegerField(db_column='NNuNivel')  # Field name made lowercase.
    nnupos = models.SmallIntegerField(db_column='NNuPos')  # Field name made lowercase.
    cidopcpadre = models.CharField(db_column='CIdOpcPadre', max_length=36)  # Field name made lowercase.
    csnultimonivel = models.CharField(db_column='CSNUltimoNivel', max_length=1)  # Field name made lowercase.
    csnseparador = models.CharField(db_column='CSNSeparador', max_length=1)  # Field name made lowercase.
    cciclase = models.CharField(db_column='CCiClase', max_length=1)  # Field name made lowercase.
    ctxclase = models.CharField(db_column='CTxClase', max_length=500, blank=False, null=False)  # Field name made lowercase.
    ctxargumento = models.CharField(db_column='CTxArgumento', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ctxurlicono = models.CharField(db_column='CTxUrlIcono', max_length=500, blank=False, null=False)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblopcion'
        verbose_name_plural = 'tblopciones'
        ordering = ('cidopc', )


#______________________________________ PERMISO OPCION
class Tblpermisoopcion(models.Model):
    cidpermopc = models.CharField(db_column='CIdPermOpc', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidrol = models.ForeignKey('Tblrol', models.DO_NOTHING, db_column='CIdRol', default='', related_name='permiso_rol')  # Field name made lowercase.
    cidopc = models.ForeignKey('Tblopcion', models.DO_NOTHING, db_column='CIdOpc', default='', related_name='permiso_opcion')  # Field name made lowercase.
    ccepermopc = models.CharField(db_column='CCePermOpc', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblpermisoopcion'
        verbose_name_plural = 'tblpermisoopciones'
        ordering = ('cidpermopc', )



#______________________________________ PERMISO EVENTO OPCION
class Tblpermisoeventoopcion(models.Model):
    cidpermevenopc = models.CharField(db_column='CIdPermEvenOpc', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cideventoopc = models.ForeignKey('Tbleventoopcion', models.DO_NOTHING, db_column='CIdEventoOpc', default='', related_name='permisoevento_evento')  # Field name made lowercase.
    cidpermopc = models.ForeignKey('Tblpermisoopcion', models.DO_NOTHING, db_column='CIdPermOpc', default='', related_name='permisoevento_opcion')  # Field name made lowercase.
    ccepermevenopc = models.CharField(db_column='CCePermEvenOpc', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblpermisoeventoopcion'
        verbose_name_plural = 'tblpermisoeventoopciones'
        ordering = ('cidpermevenopc', )


# ______________________________________ TIPO CUENTA BANCO
class Tbltipocuentabanco(models.Model):
    cidtpctabco = models.CharField(db_column='CIdTpCtaBco', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnomtpctabco = models.CharField(db_column='CNomTpCtaBco', unique=True, max_length=50)  # Field name made lowercase.
    ccetpctabco = models.CharField(db_column='CCeTpCtaBco', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tbltipocuentabanco'
        verbose_name_plural = 'tbltipocuentasbancos'


# ______________________________________ BANCO
class Tblbanco(models.Model):
    cidbanco = models.CharField(db_column='CIdBanco', primary_key=True, default=uuid.uuid4, editable=False, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnombanco = models.CharField(db_column='CNomBanco', unique=True, max_length=100)  # Field name made lowercase.
    ccebanco = models.CharField(db_column='CCeBanco', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblbanco'
        verbose_name_plural = 'tblbancos'



# ______________________________________ CLIENTE SOLICITUD
class Tblclientesolicitud(models.Model):
    cidclientesolicitud = models.CharField(db_column='CIdClienteSolicitud', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidbanco = models.CharField(db_column='CIdBanco', max_length=100, null=True, blank=True, default= '')  # Field name made lowercase.
    cidtpctabco = models.CharField(db_column='CIdTpCtaBco', max_length=20, null=True, blank=True, default= '')  # Field name made lowercase.
    cidcliente = models.ForeignKey(Tblcliente, models.DO_NOTHING, db_column='CIdCliente')  # Field name made lowercase.
    nidsolicitud = models.IntegerField(db_column='NIdSolicitud', unique=True)  # Field name made lowercase.
    cnucuenta = models.CharField(db_column='CNuCuenta', max_length=20, null=True, blank=True, default= '')  # Field name made lowercase.
    cnucelular = models.CharField(db_column='CNuCelular', max_length=20)  # Field name made lowercase.
    cnucedula = models.CharField(db_column='CNuCedula', max_length=10)  # Field name made lowercase.
    dfxsolicitud = models.DateTimeField(db_column='DFxSolicitud')  # Field name made lowercase.
    dfxaprobado = models.DateTimeField(db_column='DFxAprobado', blank=True, null=True)  # Field name made lowercase.
    csnacreditado = models.CharField(db_column='CSNAcreditado', max_length=1, default='N', blank=False, null=False)  # Field name made lowercase.
    dfxacreditado = models.DateField(db_column='DFxAcreditado', blank=True, null=True)  # Field name made lowercase.
    nvrsolicitado = models.FloatField(db_column='NVrSolicitado', default=0, blank=False, null=False)  # Field name made lowercase.
    nvracreditado = models.FloatField(db_column='NVrAcreditado', default=0, blank=False, null=False)  # Field name made lowercase.
    ccesolicitud = models.CharField(db_column='CCeSolicitud', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    cnomcliente = models.CharField(db_column='CNomCliente', max_length=255, default='', blank=False, null=False)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblclientesolicitud'
        verbose_name_plural = 'tblclientesolicitudes'



#______________________________________ PAIS
class Tblpais(models.Model):
    cidpais = models.CharField(db_column='CIdPais', primary_key=True, max_length=36, default='', blank=False, null=False)  # Field name made lowercase.
    cnompais = models.CharField(db_column='CNomPais', unique=True, max_length=100, blank=False, null=False)  # Field name made lowercase.
    cciareacode = models.CharField(db_column='CCiAreaCode', max_length=20, blank=False, null=False)  # Field name made lowercase.
    ccepais = models.CharField(db_column='CCePais', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'tblpais'
        verbose_name_plural = 'tblpaises'


#______________________________________ PASS RECOVERY
class Tblpassrecovery(models.Model):
    cidpassrecovery = models.CharField(db_column='CIdPassRecovery', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cnomusuario = models.CharField(db_column='CNomUsuario', max_length=50, default='', blank=False, null=False)  # Field name made lowercase.
    dfxpassrecovery = models.DateTimeField(db_column='DFxPassRecovery')  # Field name made lowercase.
    ccepassrecovery = models.CharField(db_column='CCePassRecovery', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    nnuminutos = computed_property.ComputedIntegerField(compute_from='_get_minutos', default=0)

    def _get_minutos(self):
        duration = datetime.now() - dfxpassrecovery
        return duration
        #duration_in_s = duration.total_seconds()
        #minutes = divmod(duration_in_s, 60)[0]
        #return 1 #minutes

    class Meta:
        managed = True
        db_table = 'tblpassrecovery'
        verbose_name_plural = 'tblpassrecoveries'


###################################  VISTAS ###################
#______________________________________ PERMISO EVENTO OPCION
class Vwclientecreditos(models.Model):
    cidcliente      = models.CharField(db_column='CIdCliente', primary_key=True, max_length=36, blank=False, null=False)  # Field name made lowercase.
    cidrolusuario   = models.ForeignKey('Tblrolusuario', models.DO_NOTHING, db_column='CIdRolUsuario')  # Field name made lowercase.
    ccecliente      = models.CharField(db_column='CCeCliente', max_length=1, default='A', blank=False, null=False)  # Field name made lowercase.
    nflcreditocliente = models.FloatField(db_column='NFlCreditoCliente', default=0, blank=False, null=False)  # Field name made lowercase.
    cnompersona     = models.CharField(db_column='CNomPersona', max_length=300)  # Field name made lowercase.
    ctxcorreo       = models.CharField(db_column='CTxCorreo', max_length=150)  # Field name made lowercase.
    cnucelular      = models.CharField(db_column='CNuCelular', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vwclientecreditos'
        ordering = ('cnompersona', )


#______________________________________ CLIENTE EVENTOS
class Vwclienteeventos(models.Model):
    cidclienteventodet      = models.CharField(db_column='CIdClientEventoDet', primary_key=True, max_length=36, default='', blank=False, null=False)
    cidcliente              = models.CharField(db_column='CIdCliente', max_length=36, blank=False, null=False)
    cnomdetalle             = models.CharField(db_column='CNomDetalle', max_length=255, blank=False, null=False)
    cnomevento              = models.CharField(db_column='CNomEvento', max_length=255, blank=False, null=False)
    csnmultiple             = models.CharField(db_column='CSNMultiple', max_length=1, blank=False, null=False)
    nfltotalevento          = models.FloatField(db_column='NFlTotalEvento', blank=False, null=False)
    dfxclienteeventodet     = models.DateTimeField(db_column='DFxClienteEventoDet', blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'vwclienteeventos'



#______________________________________ EVENTOS CON RESULTADOS
class Vweventoconresultado(models.Model):
    cidevento               = models.CharField(db_column='CIdEvento', primary_key=True, max_length=36, default='', blank=False, null=False)
    cnomevento              = models.CharField(db_column='CNomEvento', max_length=255, blank=False, null=False)
    ctxurlicono             = models.CharField(db_column='CTxUrlIcono', max_length=500, blank=False, null=False)  # Field name made lowercase.
    dfxinicio               = models.DateTimeField(db_column='DFxInicio')  # Field name made lowercase.
    csnliquidado            = models.CharField(db_column='CSNLiquidado', max_length=1, default='N', blank=False, null=False)
    dfxliquidado            = models.DateTimeField(db_column='DFxLiquidado')  # Field name made lowercase.
    dfxfin               = models.DateTimeField(db_column='DFxFin')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vweventoconresultado'




###############################  STORE PROCEDURES ###########

#______________________________________ MENU
class SPMenu(models.Model):
    # fields
    #ID = models.CharField(max_length=10, default = '')
    CIdOpcPadre = models.CharField(max_length=10, default = '')
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    home = models.CharField(max_length=5)

    # static method to perform a fulltext search
    @staticmethod
    def get_menu(rol, lenguaje):
        conf.settings.DATABASES['default']['NAME'] = 'wingodb'
        cur = connection.cursor()
        cur.execute("CALL `sps_menu`(@cidrol:={cidrol}, @ccilenguaje:={ccilenguaje});".format(cidrol=rol, ccilenguaje=lenguaje))
        results = cur.fetchall()
        cur.close()
        conf.settings.DATABASES['default']['NAME'] = 'djangodb'
        return [SPMenu(*row) for row in results]


#______________________________________ PREMIOS EVENTO LISTADO
class SPPremiosEventoListado(models.Model):
    # fields
    #CIdClientEventoDet = models.CharField(max_length=10, default = '')
    #ID = models.IntegerField(primary_key=True)
    CIdClienteEventoDetCompPronos = models.CharField(primary_key=True, max_length=36, default='')
    CIdEventoDetPronostico = models.CharField(max_length=36, default='')
    CIdClienteEventoDetComp = models.CharField(max_length=36, default='')
    CCeClienteEventoDetCompPronos = models.CharField(max_length=1, default='A')
    NVrTarifa = models.FloatField(default=0.00)
    CIdEventoDetalle = models.CharField(max_length=36, default='')
    CIdCliente = models.CharField(max_length=36, default='')
    NFlValorGanador = models.FloatField(default=0.00)
    CNomEvento = models.CharField(max_length=255, default='')
    CNomCompetidor = models.CharField(max_length=255, default='')
    CNomEventoPronostico = models.CharField(max_length=255, default='')
    CNomPersona = models.CharField(max_length=255, default='')
    CSNMultiple = models.CharField(max_length=1, default='')
    CIdClienteEventoDetalle = models.CharField(max_length=36, default='')

    # static method to perform a fulltext search
    @staticmethod
    def get_premioseventolistado(evento):
        conf.settings.DATABASES['default']['NAME'] = 'wingodb'
        cur = connection.cursor()
        cur.execute("CALL `sps_premiosEventoListado`(@prmCIdEvento:='"+evento+"', @prmCSNCliente:= False, @prmCSNResumen:= False, @prmCSNReturnData := True);")
        results = cur.fetchall()

        cur.close()
        conf.settings.DATABASES['default']['NAME'] = 'djangodb'

        return [SPPremiosEventoListado(*row) for row in results]


#______________________________________ PREMIOS EVENTO PUNTOS
class SPPremiosEventoPuntos(models.Model):
    # fields
    #CIdClientEventoDet = models.CharField(max_length=10, default = '')
    #ID = models.IntegerField(primary_key=True)
    CIdCliente = models.CharField(primary_key=True, max_length=36)
    NNuPuntos = models.IntegerField(default=0)

    # static method to perform a fulltext search
    @staticmethod
    def get_premioseventopuntos(evento, cliente):
        conf.settings.DATABASES['default']['NAME'] = 'wingodb'
        cur = connection.cursor()
        cur.execute("CALL `sps_premiosEventoPuntos`(@prmCIdEvento:='"+evento+"', @prmCIdCliente:= '" + cliente + "');")
        results = cur.fetchall()

        cur.close()
        conf.settings.DATABASES['default']['NAME'] = 'djangodb'

        return [SPPremiosEventoPuntos(*row) for row in results]


#______________________________________ PREMIOS EVENTO
class SPPremiosEvento(models.Model):
    # fields
    #CIdClientEventoDet = models.CharField(max_length=10, default = '')
    #ID = models.IntegerField(primary_key=True)
    CIdEventoDetalle = models.CharField(primary_key=True, max_length=36)
    CIdEventoDetPronostico = models.CharField(max_length=36)
    CNomEventoPronostico = models.CharField(max_length=255)
    NNuCanGanadores = models.IntegerField(default=0)
    NFlTotalAcumulado = models.FloatField(default=0.00)
    NFlTotalPremios = models.FloatField(default=0.00)
    NFlPorcDistrib = models.FloatField(default=0.00)
    NFlTotalDistrib = models.FloatField(default=0.00)
    NFlValorGanador = models.FloatField(default=0.00)
    NFlTotalEvento = models.FloatField(default=0.00)
    CNomEvento = models.CharField(max_length=255, default='')
    CNomDetalle = models.CharField(max_length=255, default='')
    CTxUrlIconoDetalle = models.CharField(max_length=500, default='')
    CSNMultiple = models.CharField(max_length=1, default='')

    # static method to perform a fulltext search
    @staticmethod
    def get_premiosevento(evento):
        conf.settings.DATABASES['default']['NAME'] = 'wingodb'
        cur = connection.cursor()
        #cur.execute("CALL `sps_premiosEvento`(@prmCIdEvento:='"+evento+"');")
        cur.execute("CALL `sps_premiosEventoListado`(@prmCIdEvento:='"+evento+"', @prmCSNCliente:= False, @prmCSNResumen:= True, @prmCSNReturnData := True);")
        results = cur.fetchall()

        cur.close()
        conf.settings.DATABASES['default']['NAME'] = 'djangodb'

        return [SPPremiosEvento(*row) for row in results]


#______________________________________ PREMIOS EVENTO LIQUIDAR
class SPPremiosEventoLiquidar(models.Model):
    # fields
    # CTxResultado = models.CharField(primary_key=True, max_length=10, default='')
    CIdClienteEventoDetCompPronos = models.CharField(primary_key=True, max_length=36, default='')
    CIdEventoDetPronostico = models.CharField(max_length=36, default='')
    CIdClienteEventoDetComp = models.CharField(max_length=36, default='')
    CCeClienteEventoDetCompPronos = models.CharField(max_length=1, default='A')
    NVrTarifa = models.FloatField(default=0.00)
    CIdEventoDetalle = models.CharField(max_length=36, default='')
    CIdCliente = models.CharField(max_length=36, default='')
    NFlValorGanador = models.FloatField(default=0.00)
    CNomEvento = models.CharField(max_length=255, default='')
    CNomCompetidor = models.CharField(max_length=255, default='')
    CNomEventoPronostico = models.CharField(max_length=255, default='')
    CNomPersona = models.CharField(max_length=255, default='')
    CSNMultiple = models.CharField(max_length=1, default='')
    CIdClienteEventoDetalle = models.CharField(max_length=36, default='')
    CTxCorreo = models.CharField(max_length=255, default='')

    # static method to perform a fulltext search
    @staticmethod
    def get_premioseventoliquidar(evento):
        conf.settings.DATABASES['default']['NAME'] = 'wingodb'
        cur = connection.cursor()
        cur.execute("CALL `sps_premiosEventoLiquidar`(@prmCIdEvento:='"+evento+"');")
        results = cur.fetchall()
        #results = cur.fetchone()[0]

        cur.close()
        conf.settings.DATABASES['default']['NAME'] = 'djangodb'

        return [SPPremiosEventoLiquidar(*row) for row in results]


#______________________________________ EVENTO ACTIVO ACUMULADO
class SPEventoActivoAcumulado(models.Model):
    # fields

    CIdEvento = models.CharField(primary_key=True, max_length=36, default='')
    CIdEventoDetalle = models.CharField(max_length=36, default='')
    CNomEvento = models.CharField(max_length=255, default='')
    CNomDetalle = models.CharField(max_length=255, default='')
    DFxFin = models.DateTimeField()  # Field name made lowercase.
    CTxUrlIconoDetalle = models.CharField(max_length=500)
    CIdTipoEvento = models.CharField(max_length=36, default='')
    NFlTotalAcumulado = models.FloatField(default=0.00)
    NNuParticipantes = models.IntegerField(default=0)

    # static method to perform a fulltext search
    @staticmethod
    def get_eventoactivoacumulado():
        conf.settings.DATABASES['default']['NAME'] = 'wingodb'
        cur = connection.cursor()
        cur.execute("CALL `sps_eventoactivoacumulado`();")
        results = cur.fetchall()

        cur.close()
        conf.settings.DATABASES['default']['NAME'] = 'djangodb'

        return [SPEventoActivoAcumulado(*row) for row in results]




"""
class SPClienteEventos(models.Model):
    # fields
    #CIdClientEventoDet = models.CharField(max_length=10, default = '')
    ID = models.IntegerField(primary_key=True)
    CIdCliente = models.CharField(max_length=36)
    CNomDetalle = models.CharField(max_length=255)
    CNomEvento = models.CharField(max_length=255)
    CSNMultiple = models.CharField(max_length=1)
    NFlTotalEvento = models.FloatField()
    DFxClienteEventoDet = models.DateTimeField()
    CNomCompetidorA = models.CharField(max_length=255)
    CNomCompetidorB = models.CharField(max_length=255)
    CTxUrlIconoA = models.CharField(max_length=500)
    CTxUrlIconoB = models.CharField(max_length=500)
    CNomEventoPronostico = models.CharField(max_length=100)
    CCiCompetidor = models.CharField(max_length=1)

    # static method to perform a fulltext search
    @staticmethod
    def get_clienteeventos(cliente):
        conf.settings.DATABASES['default']['NAME'] = 'wingodb'
        cur = connection.cursor()
        cur.execute("CALL `sps_clienteeventos`(@prm_cidcliente:={cidcliente});".format(cidcliente=cliente))
        results = cur.fetchall()
        cur.close()
        conf.settings.DATABASES['default']['NAME'] = 'djangodb'

        return [SPClienteEventos(*row) for row in results]
"""



@receiver(post_save, sender=Tblevento, dispatch_uid=uuid.uuid4())
def evento_save_handler(sender, instance, created, raw, using, **kwargs):
    urlimg = Tblparametro.objects.filter(cidparametro='imgurlGET')
    mensaje= Tblparametro.objects.filter(cidparametro='msgNuevoEvento')

    nuevo_evento_task.delay(
            ('NUEVO EVENTO EN HIT: ' + instance.cnomevento),
            mensaje[0].ctxtexto,
            instance.cnomevento,
            (urlimg[0].ctxtexto+instance.ctxurlicono)
            )







# ----------------------------------------------------------------- TASKS ---------------------------------------------------------------
@shared_task
def nuevo_evento_task(subject, message, evento, imagen):

    usuarios = Tblusuario.objects.filter(csnvalidado='S')

    for usuario in usuarios:
        send_mail_nuevo_evento_task(usuario.ctxcorreo,
                             usuario.cnomusuario,
                             subject,
                             message,
                             evento,
                             imagen
                            )

    return 'Emails was sent with success!'


def send_mail_nuevo_evento_task(correo, username, subject, message, evento, imagen):

    from_email = settings.DEFAULT_FROM_EMAIL

    if (from_email and correo):
        html_content = render_to_string('new_event_email.html',
                                        {
                                            'username': username,
                                            'message': message,
                                            'imagen': imagen,
                                            'evento': evento,
                                            'host': settings.APP_HOST,
                                        })

        try:
            msg = EmailMessage(subject, html_content, from_email, [correo])
            msg.content_subtype = "html"
            msg.send()
        except BadHeaderError:
            return Response(
                data={
                    "Invalid header found sending mail."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={
                "Email was sent."
            },
            status=status.HTTP_200_OK
        )

