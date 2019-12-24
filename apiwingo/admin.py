from django.contrib import admin
from . import models


from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


#from .forms import CustomUserCreationForm, CustomUserChangeForm
#from .models import CustomUser

"""
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'cellphone']


admin.site.register(CustomUser, CustomUserAdmin)
"""


# Register your models here.
admin.site.register(models.Tblpersona)
admin.site.register(models.Tblpropiedad)
admin.site.register(models.Tblpersonapropiedad)
admin.site.register(models.Tblusuario)
admin.site.register(models.Tblrol)
admin.site.register(models.Tblrolusuario)
admin.site.register(models.Tblcliente)
admin.site.register(models.Tbltipoevento)
admin.site.register(models.Tblevento)
admin.site.register(models.Tbleventodetalle)
admin.site.register(models.Tbleventodetcompetidor)
admin.site.register(models.Tbleventodetpronostico)
admin.site.register(models.Tbleventoresulpronostico)
admin.site.register(models.Tblclienteeventodet)
admin.site.register(models.Tblclienteeventodetcomp)
admin.site.register(models.Tblclienteeventodetcomppronos)
admin.site.register(models.Tbltipotrans)
admin.site.register(models.Tblclientetrans)
admin.site.register(models.Tblmensaje)
admin.site.register(models.Tblparametro)

admin.site.register(models.Tblrecurso)
admin.site.register(models.Tblaplicacion)
admin.site.register(models.Tbleventoopcion)
admin.site.register(models.Tblfuncion)
admin.site.register(models.Tblmodulo)
admin.site.register(models.Tblopcion)
admin.site.register(models.Tblpermisoopcion)
admin.site.register(models.Tblpermisoeventoopcion)



###############################  VISTAS ###########
admin.site.register(models.Vwclientecreditos)



###############################  STORE PROCEDURES ###########
admin.site.register(models.SPMenu)




