# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory
from forms import *

# Create your views here.

@login_required
def create_edit_empresa(request, id = None):
    if id is not None:
        empresa = get_object_or_404(Empresa, id = id)
    else:
        empresa = None
    form = FormEmpresa(data = request.POST or None, instance = empresa)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/empresa/added/")
    return render_to_response("empresas/empresa_form.html", {'form': form})

def create_edit_delegado(request, id_delegado = None):
    if id is not None:
        delegado = get_object_or_404(Delegado, id = id_delegado)
    else:
        delegado = None
    form = FormDelegado(data = request.POST or None, instance = delegado)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/delegado/added/")
    return render_to_response("delegados/delegado_form.html", {'form': form})



def listado_empresas(request):
    empresas = Empresa.objects.order_by("nombre")
    return render_to_response("empresas.html", locals())

@login_required
def principal(request):
    return render_to_response("principal.html")

def primera_visita(request):
    return HttpResponseRedirect("/admin/comerciales/primeravisita/add/")

def manage_fichas(request):
    from django.forms.models import inlineformset_factory
    FichaFormSet = inlineformset_factory(Empresa, Ficha, extra = 1)
    VisitaFormSet = inlineformset_factory(Empresa, Visita, extra = 1)
    empresa = Empresa.objects.get(id = 1)
    if request.method == 'POST':
        formempresa = FormEmpresa(request.POST, 
                                  request.FILES, 
                                  instance = empresa)
        formset = FichaFormSet(request.POST, 
                               request.FILES, 
                               instance = empresa)
        formsetvisita = VisitaFormSet(request.POST, 
                                      request.FILES, 
                                      instance = empresa)
        if (formempresa.is_valid() and formset.is_valid() 
            and formsetvisita.is_valid()):
            formempresa.save()
        #if formset.is_valid():
            formset.save()
            formsetvisita.save()
            return HttpResponseRedirect("/fichas/")
    else:
        formempresa = FormEmpresa(instance = empresa)
        formset = FichaFormSet(instance = empresa)
        formsetvisita = VisitaFormSet(instance = empresa)
    return render_to_response("ficha_form.html", locals()
                                             #    {"formset": formset, 
                                             #     "formempresa": formempresa, 
                                             #    }
                             )

def manage_empresas(request):
    from django.forms.models import inlineformset_factory
    FichaFormSet = inlineformset_factory(Empresa, Ficha, extra = 1)
    empresa = Empresa.objects.get(id = 1)
    if request.method == 'POST':
        formset = FichaFormSet(request.POST, 
                               request.FILES, 
                               instance = empresa)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect("/fichas/")
    else:
        formset = FichaFormSet(instance = empresa)
    return render_to_response("ficha_form.html", {"formset": formset,})

@login_required
def megaform(request):
    from django.forms.models import inlineformset_factory
    ContactosFormSet = inlineformset_factory(Empresa, Contacto, extra = 1)
    ReferenciasFormSet = inlineformset_factory(Empresa, Referencia, extra = 1)
    ProyectosFormSet = inlineformset_factory(Empresa, Proyecto, extra = 1)
    PreciosFormSet = inlineformset_factory(Empresa, Precio, extra = 3)
    FichasFormSet = inlineformset_factory(Empresa, Ficha, extra = 1)
    CatalogosFormSet = inlineformset_factory(Empresa, Catalogo, extra = 1)
    MuestrasFormSet = inlineformset_factory(Empresa, Muestra, extra = 1)
    PrimeraVisitaFormSet = inlineformset_factory(Empresa, PrimeraVisita, 
                                                 max_num = 1, extra = 1)
    VisitasFormSet = inlineformset_factory(Empresa, Visita, extra = 1)
    empresas = Empresa.objects.all()
    eid = request.GET.get("eid", None)
    if eid != None:
        empresa = get_object_or_404(Empresa, id = eid)
        #empresa = Empresa.objects.get(id = eid)
    else:
        empresa = Empresa() # Nueva empresa. No toca la BD hasta el .save() 
    if request.method == "POST":
        formempresa = FormEmpresa(request.POST, request.FILES, 
                                  instance = empresa)
        fscontactos = ContactosFormSet(request.POST, request.FILES, 
                                       instance = empresa)
        fsreferencias = ReferenciasFormSet(request.POST, request.FILES, 
                                       instance = empresa)
        fsproyectos = ProyectosFormSet(request.POST, request.FILES, 
                                       instance = empresa)
        fsprecios = PreciosFormSet(request.POST, request.FILES, 
                                       instance = empresa)
        fsfichas = FichasFormSet(request.POST, request.FILES, 
                                       instance = empresa)
        fscatalogos = CatalogosFormSet(request.POST, request.FILES, 
                                       instance = empresa)
        fsmuestras = MuestrasFormSet(request.POST, request.FILES, 
                                       instance = empresa)
        fsprimeravisita = PrimeraVisitaFormSet(request.POST, request.FILES, 
                                       instance = empresa)
        fsvisitas = VisitasFormSet(request.POST, request.FILES, 
                                       instance = empresa)
        forms = (formempresa, fscontactos, fsreferencias, fsproyectos, 
                 fsprecios, fsfichas, fscatalogos, fsmuestras, 
                 fsprimeravisita, fsvisitas)
        all_valid = True
        for f in forms:
            if f.is_valid():
                f.save()
            else:
                all_valid = False
            #if [f for f in forms if f.is_valid()]:
            #    for f in forms:
            #        f.save()
        if all_valid:
            return HttpResponseRedirect("/general/?eid=%d" % empresa.id)
    else:
        formempresa = FormEmpresa(instance = empresa)
        fscontactos = ContactosFormSet(instance = empresa)
        fsreferencias = ReferenciasFormSet(instance = empresa)
        fsproyectos = ProyectosFormSet(instance = empresa)
        fsprecios = PreciosFormSet(instance = empresa)
        fsfichas = FichasFormSet(instance = empresa)
        fscatalogos = CatalogosFormSet(instance = empresa)
        fsmuestras = MuestrasFormSet(instance = empresa)
        fsprimeravisita = PrimeraVisitaFormSet(instance = empresa)
        fsvisitas = VisitasFormSet(instance = empresa)
    return render_to_response("general_form.html", locals())

    
