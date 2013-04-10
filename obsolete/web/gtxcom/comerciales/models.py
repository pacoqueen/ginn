# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin 
from django.contrib import databrowse

class Delegado(models.Model):
    nombre = models.CharField(max_length = 32)
    apellidos = models.CharField(max_length = 64)

    def __unicode__(self):
        return "%s, %s" % (self.apellidos, self.nombre)

class Sector(models.Model):
    nombre = models.CharField(max_length = 128)

    def __unicode__(self):
        return self.nombre

class Empresa(models.Model):
    nombre = models.CharField(max_length = 128)
    cif = models.CharField(max_length = 10)
    sector = models.ForeignKey(Sector, null = True)
    direccion = models.CharField(max_length = 256, blank = True)
    grupo = models.CharField(max_length = 256, blank = True)
    telefono = models.CharField(max_length = 9, blank = True)
    fax = models.CharField(max_length = 9, blank = True)
    mail = models.EmailField(blank = True, null = True)
    www = models.URLField(blank = True, null = True)
    cp = models.CharField(max_length = 5, blank = True)
    localidad = models.CharField(max_length = 128, blank = True)
    pais = models.CharField(max_length = 64, blank = True)
    conoce = models.BooleanField()
    dar_precio = models.BooleanField()
    motivo = models.TextField(blank = True, null = True)

    def __unicode__(self):
        return self.nombre

class PrimeraVisita(models.Model):
    empresa = models.ForeignKey(Empresa)
    delegado = models.ForeignKey(Delegado)
    fecha = models.DateField()
    conoce_el_producto = models.BooleanField()
    compra_material = models.BooleanField()
    proveedor = models.TextField(blank = True, null = True) # Esto podría ser 
                                                    # una entidad en el futuro.
    consumo_anual = models.FloatField()
    precio = models.FloatField()
    contactos_terceros = models.TextField(blank = True, null = True)
    comentarios = models.TextField(blank = True, null = True)
    fecha_proxima_visita = models.DateField(null = True) # No tira blank = True

    def __unicode__(self):
        return self.empresa.nombre

class Visita(models.Model):
    empresa = models.ForeignKey(Empresa)
    delegado = models.ForeignKey(Delegado)
    fecha = models.DateField()
    comentarios = models.TextField(blank = True, null = True)
    compra_material = models.BooleanField()
    proveedor = models.TextField(blank = True, null = True) # Esto podría ser 
                                                    # una entidad en el futuro.
    consumo_anual = models.FloatField()
    precio = models.FloatField()

    def __unicode__(self):
        return "%s (%s)" % (self.empresa.nombre, 
                            self.fecha.strftime("%d/%m/%Y"))

class Contacto(models.Model):
    empresa = models.ForeignKey(Empresa)
    nombre = models.CharField(max_length = 32)
    apellidos = models.CharField(max_length = 64)
    cargo = models.CharField(max_length = 128, blank = True)
    movil = models.CharField(max_length = 9, blank = True)
    mail = models.EmailField(blank = True, null = True)

    def __unicode__(self):
        res = self.apellidos, ", " + self.nombre 
        if self.movil:
            res += "(%s)" % self.movil
        return res

class Referencia(models.Model):
    empresa = models.ForeignKey(Empresa)
    descripcion = models.TextField()

    def __unicode__(self):
        return self.descripcion

class Proyecto(models.Model):
    empresa = models.ForeignKey(Empresa)
    descripcion = models.TextField()
    def __unicode__(self):
        return self.descripcion

class Precio(models.Model):
    empresa = models.ForeignKey(Empresa)
    fecha = models.DateField()
    precio = models.FloatField()
    producto = models.TextField()   # Esto *debe* ser una entidad en el futuro.

class Ficha(models.Model):
    empresa = models.ForeignKey(Empresa)
    ficha_tecnica = models.CharField(max_length = 16)
    fecha = models.DateField()
    gtx = models.BooleanField()
    fibra = models.BooleanField()
    geocem = models.BooleanField()
    geop_otros = models.BooleanField()
    
    def __unicode__(self):
        return self.ficha_tecnica

class Muestra(models.Model):
    empresa = models.ForeignKey(Empresa)
    muestra = models.TextField()
    fecha = models.DateField()
    gtx = models.BooleanField()
    fibra = models.BooleanField()
    geocem = models.BooleanField()
    geop_otros = models.BooleanField()
    
    def __unicode__(self):
        return self.muestra

class Catalogo(models.Model):
    empresa = models.ForeignKey(Empresa)
    catalogo = models.TextField()
    fecha = models.DateField()
    gtx = models.BooleanField()
    fibra = models.BooleanField()
    geocem = models.BooleanField()
    geop_otros = models.BooleanField()

    def __unicode__(self):
        return self.catalogo

admin.site.register(Delegado)
admin.site.register(Empresa)
admin.site.register(Sector)
admin.site.register(PrimeraVisita)
admin.site.register(Visita)
admin.site.register(Contacto)
admin.site.register(Referencia)
admin.site.register(Proyecto)
admin.site.register(Precio)
admin.site.register(Ficha)
admin.site.register(Muestra)
admin.site.register(Catalogo)

databrowse.site.register(Delegado)
databrowse.site.register(Empresa)
databrowse.site.register(Sector)
databrowse.site.register(PrimeraVisita)
databrowse.site.register(Visita)
databrowse.site.register(Contacto)
databrowse.site.register(Referencia)
databrowse.site.register(Proyecto)
databrowse.site.register(Precio)
databrowse.site.register(Ficha)
databrowse.site.register(Muestra)
databrowse.site.register(Catalogo)


