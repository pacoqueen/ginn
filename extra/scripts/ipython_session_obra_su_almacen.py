# coding: utf-8
# %save en ipython is wonderful. Cargar con ipython -i para continuar.
from framework import pclases
a = pclases.Obra.selectBy(nombre = "SU ALMACEN")[0]
len(a.clientes)
for c in a.clientes:
    print c.nombre
    
vacidas = [o for o in pclases.Obra.select() if not o.clientes]
len(vacidas)
for o in vacidas:
    if o.presupuestos:
        for f in o.presupuestos:
            o.addCliente(f.cliente)
    else:
        o.destroySelf()
vacidas = [o for o in pclases.Obra.select() if not o.clientes]
len(vacidas)
for c in a.clientes:
    nueva_obra = a.clone(nombre = c.nombre)
    nueva_obra.direccion = c.direccion
    nueva_obra.cp = c.cp
    nueva_obra.ciudad = c.ciudad
    nueva_obra.provincia = c.provincia
    nueva_obra.pais = c.pais
    nueva_obra.observaciones = "[admin] splitted from SU ALMACEN. (8/9/2014)."
    nueva_obra.addCliente(c)
    if len(c.obras) == 1:
        nueva_obra.generica = True
        
sus = pclases.Cliente.get(1589)
osus = sus.get_obra_generica()
osus.nombre
contactos_sus = [c for c in a.contactos if "sustraia" in c.correoe]
len(contactos_sus)
for c in contactos_sus:
    c.removeObra(a)
    c.addObra(osus)
    c.sync()
    
ref = pclases.Cliente.select(pclases.Cliente.q.nombre.contains("REFRESCO I"))[0]
oref = ref.get_obra_generica()
for c in a.contactos:
    c.removeObra(a)
    c.addObra(oref)
    c.sync()
    
len(a.presupuestos)
len(a.facturasVenta)
len(a.pedidosVenta)
