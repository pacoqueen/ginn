> Conversión automática de python 2 a 3. No es perfecta. Requerirá retoques casi seguro.

python3 -m lib2to3 -wn fichero.py

> Conversión automática de Glade 2 a Glade 3

gtk-builder-convert fichero.glade2 fichero.glade

rm fichero.glade2

vi fichero.glade

> Cambiar los GtkHBox por GtkBox (tienen orientación horizontal por defecto)

:%s/GtkHBox/GtkBox/g

> Cambiar los GtkVBox por GtkBox y agregar en la línea siguiente

<property name="orientation">vertical</property>

> Y comprobar que todos los widgets son compatibles.

glade fichero.glade