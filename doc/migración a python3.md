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

---

En los `.py` hay que cambiar:

```python
import pygtk
pygtk.require('2.0')
import gtk
```

Por:

```python
import gi
gi.require_version("Gtk", '3.0')
from gi import pygtkcompat

try:
    from gi import pygtkcompat
except ImportError:
    pygtkcompat = None
    from gi.repository import Gtk as gtk
    from gi.repository import GObject as gobject

if pygtkcompat is not None:
    pygtkcompat.enable()
    pygtkcompat.enable_gtk(version='3.0')
    import gtk
    import gobject
```

Y todas las referencias a `mx` por su equivalente en `datetime`. Esto a mano y caso por caso:

`import mx.DateTime` → `import datetime`

`mx.DateTime.oneDay` → `datetime.timedelta(days=1)`

`mx.DateTime.localtime()` → `datetime.datetime.today()`

`mx.DateTime.DateTimeDelta(dias, horas, minutos, segundos)` → `datetime.timedelta((24*dias)+horas, minutos, segundos)`

`mx.DateTime.DateTimeDeltaFrom(horas)` → `datetime.timedelta(horas)`

`mx.DateTime.DateTimeFrom(dia, mes, año, hora, minuto)` → `datetime.datetime(dia, mes, año, hora, minuto)`

---

Para depurar widgets GTK: https://wiki.gnome.org/action/show/Projects/GTK/Inspector?action=show&redirect=Projects%2FGTK%2B%2FInspector

`gsettings set org.gtk.Settings.Debug enable-inspector-keybinding true`

y Ctrl+Shift+D o Ctrl+Shift+I.

