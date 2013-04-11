#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################################################
# 10 de julio de 2006.
# Script temporal para ajustar los precios de LDV de algunas 
# facturas antiguas DEBIDO A UN ERROR EN LAS MACROS EXCEL que
# usaban antes de la implantación de ginn. Para respetar la 
# contabilidad de enero-mayo '06, este script ajusta los 
# precios unitarios a los calculados (con chorromil decimales)
# por excel y que así coincidan los totales de facturación.
#################################################################
import sys, os
sys.path.append(os.path.join('..', 'framework'))
from framework import pclases

# Lista de pares (idldv, preciounidad):
ldvs = ((69, 0.39169906),
        (77, 0.36143386),
        (131, 0.21685764),
        (141, 0.51147259),
        (275, 0.23219231),
        (149, 0.27408263),
        (534, 0.3329553),
        (561, 0.29571618),
        (604, 1.4923387),
        (558, 0.33879479),
        (565, 0.39169958),
        (540, 1.4923384),
        (566, 0.50392024),
        (612, 0.29134587),
        (616, 0.29479676),
        (567, 0.21685841),
        (379, 0.50392043),
        (339, 0.32200196),
        (403, 0.31724339),
        (412, 0.67335334),
        (513, 0.21685887),
        (516, 0.26690208),
        (864, 0.21687323),
        (167, 0.21685885),
        (169, 0.39169906),
        (300, 1.4923393),
        (178, 0.29134589),
        (575, 0.29134666),
        (186, 0.39169576),
        (194, 0.21365343),
        (203, 0.21685893),
        (204, 0.50392024)
        )

for id, precio in ldvs:
    ldv = pclases.LineaDeVenta.get(id)
    print "Ajustando LDV %d de %f a %f..." % (id, ldv.precio, precio), 
    ldv.precio = precio
    print "OK (%f)" % ldv.precio

print "Ajustando IVA factura O60001...", 
fra = pclases.FacturaVenta.get(197)
fra.iva = 0
print "OK (%f)" % (fra.iva)
print "Ajustando IVA factura O60008...", 
fra = pclases.FacturaVenta.get(204)
fra.iva = 0
print "OK (%f)" % (fra.iva)
print "Cambiando número factura O60008 dupliacada a O60011 y el IVA a 0...", 
fra = pclases.FacturaVenta.get(207)
fra.numfactura = "O60011"
fra.iva = 0
print "OK (%s, %f)" % (fra.numfactura, fra.iva)
print "Ajustando IVA factura O60013...", 
fra = pclases.FacturaVenta.get(209)
fra.iva = 0
print "OK (%f)" % (fra.iva)
print "Cambiando número factura G60003 dupliacada a G60004...", 
fra = pclases.FacturaVenta.get(199)
fra.numfactura = "G60004"
print "OK (%s)" % (fra.numfactura)

