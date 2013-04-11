#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm
from models import *

# CRUD Autoforms:

class FormEmpresa(ModelForm):
    class Meta:
        model = Empresa
        #fields = ("nombre", "sector", "grupo", "dar_precio", "motivo")
        #status = MyEmpresaField()

class FormDelegado(ModelForm):
    class Meta:
        model = Delegado

class FormPrimeraVisita(ModelForm):
    class Meta:
        model = PrimeraVisita

class FormVisita(ModelForm):
    class Meta:
        model = Visita

class FormFicha(ModelForm):
    class Meta:
        model = Ficha
        #exclude = ("empresa", )

