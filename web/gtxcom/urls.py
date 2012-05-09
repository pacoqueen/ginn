from django.conf.urls.defaults import *

from comerciales.views import * 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
    # Example:
    # (r'^gtxcom/', include('gtxcom.foo.urls')),
    #(r"^empresas/", listado_empresas), 
    #(r"^empresa_edit/", create_edit_empresa), 
    (r"^$", megaform), 
    (r"^principal", principal), 
    (r"^databrowse/(.*)", login_required(databrowse.site.root)), 
    (r'^accounts/login/$', 'django.contrib.auth.views.login', 
                           {"template_name": "login.html"}),
    (r"^primera_visita/", primera_visita), 

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    
)

ROOT_URL = "/"

lista_delegados = {'queryset': Delegado.objects.all(), 
                   "template_name": "delegado_list.html"}
modelo_delegados = {'model': Delegado, 
                    'post_save_redirect': "%sdelegados/" % ROOT_URL, 
                    "template_name": "delegado_form.html", 
                    "extra_context": {"delegados": Delegado.objects.all()}}

urlpatterns += patterns("django.views.generic", 
    (r"^delegados/nuevo/$", "create_update.create_object", modelo_delegados), 
    (r"^delegados/(?P<object_id>\d+)/editar/$", 'create_update.update_object', 
        modelo_delegados),
    (r'^delegados/$', 'list_detail.object_list', lista_delegados),
    (r'^delegados/(?P<object_id>\d+)/$', 'list_detail.object_detail', 
        lista_delegados),
)

lista_empresas = {'queryset': Empresa.objects.all(), 
                  "template_name": "empresa_list.html"}
modelo_empresas = {'model': Empresa, 
                   'post_save_redirect': "%sempresas/" % ROOT_URL, 
                   "template_name": "empresa_form.html", 
                   "extra_context": {"empresas": Empresa.objects.all(), 
                                     #"formsfichas": manage_fichas
                                    }
                  }

urlpatterns += patterns("django.views.generic", 
    (r"^empresas/crud/$", "create_update.create_object", modelo_empresas), 
    (r"^empresas/(?P<object_id>\d+)/editar/$", 'create_update.update_object', 
        modelo_empresas),
    (r'^empresas/$', 'list_detail.object_list', lista_empresas),
    (r'^empresas/(?P<object_id>\d+)/$', 'list_detail.object_detail', 
        lista_empresas),
)

urlpatterns += patterns("", 
    (r"^fichas/", manage_fichas))

urlpatterns += patterns("", 
    (r"^general/", megaform))

lista_sectores = {'queryset': Sector.objects.all(), 
                   "template_name": "sector_list.html"}
modelo_sectores = {'model': Sector, 
                    'post_save_redirect': "%ssectores/" % ROOT_URL, 
                    "template_name": "sector_form.html", 
                    "extra_context": {"sectores": Sector.objects.all()}}

urlpatterns += patterns("django.views.generic", 
    (r"^sectores/nuevo/$", "create_update.create_object", modelo_sectores), 
    (r"^sectores/(?P<object_id>\d+)/editar/$", 'create_update.update_object', 
        modelo_sectores),
    (r'^sectores/$', 'list_detail.object_list', lista_sectores),
    (r'^sectores/(?P<object_id>\d+)/$', 'list_detail.object_detail', 
        lista_sectores),
)


