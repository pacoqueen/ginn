#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008 Francisco José Rodríguez Bogado                     #
#                         (pacoqueen@users.sourceforge.net)                   #
#                                                                             #
# This file is part of GeotexInn.                                             #
#                                                                             #
# GeotexInn is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# GeotexInn is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################


###################################################################
## DONE: "wrap" de líneas automático y tal.
## DONE: colores en ComboBoxEntry con el "blue", "red", etc... ya 
##   metidos y poder meter colores hexadecimales (#FF0000) 
##   a manopla en el «child».
## BUG: El portapapeles me da violaciones de segmento. ¿Por qué?
##      De momento lo deshabilito.
###################################################################

import pygtk
pygtk.require('2.0')
import gtk
import pango

from ventana import Ventana
from utils import textview_get_all_text

class Postomatic(Ventana):
    """
    Permite escribir texto con el formato típico de phpBB en el 
    campo "notas" del objeto recibido. Tiene también las funciones 
    típicas de cualquier editor de texto simple: abrir, guardar, etc.
    El texto del objeto (si lo hay) se va actualizando constantemente
    -"a la" google- y el deshacer vuelve a la copia original. No soporta
    deshacer por pasos.
    """
    # TODO: Falta el control de permisos de usuario.
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        self._objetoreciencreado = None
        self.objeto = objeto
        Ventana.__init__(self, 'postomatic.glade', objeto, self.usuario)
        self.fileabierto = None
        connections = {'b_negrita/clicked': self.negrita,
                       'b_cursiva/clicked': self.cursiva,
                       'b_subrayado/clicked': self.subrayado,
                       'b_cita/clicked': self.cita,
                       'b_codigo/clicked': self.codigo,
                       'b_imagen/clicked': self.imagen,
                       'b_lista/clicked': self.lista,
                       'b_listao/clicked': self.listao,
                       'b_enlace/clicked': self.enlace,
                       'b_color/clicked': self.color,
                       'b_size/clicked': self.size,
                       'nuevo1/activate': self.nuevo,
                       'abrir1/activate': self.abrir,
                       'guardar1/activate': self.guardar,
                       'guardar_como1/activate': self.guardar_como,
                       'salir1/activate': self.salir,
                       'cortar1/activate': self.cortar,
                       'copiar1/activate': self.copiar,
                       'pegar1/activate': self.pegar,
                       'borrar1/activate': self.borrar,
                       'copiar_todo1/activate': self.copiar_todo,
                       'b_undo/clicked': self.deshacer,} 
        self.add_connections(connections)
        self.wids['tv_texto'].get_buffer().connect('changed', self.actualizar_vista_previa)
        self.wids['tv_preview'].connect("key_release_event", 
            lambda w, e: self.wids['tv_texto'].get_buffer().set_text(w.get_buffer().get_text(*w.get_buffer().get_bounds())))
        nombres_tags = self.crear_tags(self.wids['tv_preview'].get_buffer())  # @UnusedVariable
        # Valores por defecto:
        self.wids['cbe_color'].child.set_text('blue')
        self.wids['cbe_size'].child.set_text('9')
        if self.objeto != None and hasattr(self.objeto, "notas") and isinstance(self.objeto.notas, str):
            self.wids['tv_texto'].get_buffer().set_text(self.objeto.notas)
            self.actualizar_vista_previa(None)
        self.texto_original = textview_get_all_text(self.wids['tv_texto'])
        self.wids['vpaned1'].set_position(0)
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def get_texto_seleccionado(self):
        buff = self.wids['tv_texto'].get_buffer()
        selection = buff.get_selection_bounds()
        if selection == ():
            res = ''
        else:
            res = buff.get_text(selection[0], selection[1])
        return res

    def deshacer(self, boton):
        self.wids['tv_texto'].get_buffer().set_text(self.texto_original)
        self.actualizar_vista_previa(boton)

    def reemplazar_texto(self, txt):
        """
        Reemplaza el texto seleccionado por el recibido.
        Si no hay texto seleccionado, escribe el 
        nuevo texto en la posición de inserción.
        """
        buff = self.wids['tv_texto'].get_buffer()
        selection = buff.get_selection_bounds()
        if selection != ():
            buff.delete(selection[0], selection[1])
        buff.insert_at_cursor(txt)

    def build_texto(self, tag):
        """
        Construye el texto con el tag recibido a partir
        del seleccionado y lo reemplaza en el TextView.
        Devuelve el foco al TextView.
        """
        texto = self.get_texto_seleccionado()
        nuevotexto = tag % texto
        self.reemplazar_texto(nuevotexto)
        self.wids['tv_texto'].grab_focus()

    # --------------- Manejadores de eventos ----------------------------
    def negrita(self, boton):
        tag = """[b]%s[/b]"""
        self.build_texto(tag)

    def cursiva(self, boton):
        tag = """[i]%s[/i]"""
        self.build_texto(tag)

    def subrayado(self, boton):
        tag = """[u]%s[/u]"""
        self.build_texto(tag)

    def cita(self, boton):
        citado = self.wids['e_citado'].get_text()
        tag = '[quote="%s"]' % citado
        tag += """%s[/quote]"""
        self.build_texto(tag)

    def codigo(self, boton):
        tag = """[code]%s[/code]"""
        self.build_texto(tag)

    def imagen(self, boton):
        tag = """[img]%s[/img]"""
        self.build_texto(tag)

    def lista(self, boton):
        tag = """[list]%s[/list]"""
        self.build_texto(tag)

    def listao(self, boton):
        tag = """[list=]%s[/list]"""
        self.build_texto(tag)

    def enlace(self, boton):
        url = self.wids['e_url'].get_text()
        tag = "[url=%s]" % url
        tag += """%s[/url]"""
        self.build_texto(tag)

    def color(self, boton):
        color = self.wids['cbe_color'].child.get_text()
        tag = "[color=%s]" % color
        tag += """%s[/color]"""
        self.build_texto(tag)

    def size(self, boton):
        size = self.wids['cbe_size'].child.get_text()
        tag = "[size=%s]" % size
        tag += """%s[/size]"""
        self.build_texto(tag)

    def nuevo(self, menuitem):
        buf = self.wids['tv_texto'].get_buffer()
        buf.set_text('')
        self.wids['tv_texto'].grab_focus()

    def abrir(self, menuitem):
        opendialog = gtk.FileChooserDialog('Abrir archivo',
                                action = gtk.FILE_CHOOSER_ACTION_OPEN,
                                buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                           gtk.STOCK_OK, gtk.RESPONSE_OK))
        opendialog.set_current_folder('/home/queen/bin/post-o-matic')
        respuesta = opendialog.run()
        if respuesta == gtk.RESPONSE_OK:
            nombre_archivo = opendialog.get_filename()
            f = open(nombre_archivo)
            self.wids['tv_texto'].get_buffer().set_text('')
            for linea in f.readlines():
                self.wids['tv_texto'].get_buffer().insert_at_cursor(linea)
            self.fileabierto = nombre_archivo
        opendialog.destroy()

    def guardar(self, menuitem):
        if self.fileabierto == None:
            self.guardar_como(None)
        else:
            f = open(self.fileabierto, 'w')
            widget = self.wids['tv_texto']
            buf = widget.get_buffer()
            txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
            f.write(txt)

    def guardar_como(self, menuitem):
        opendialog = gtk.FileChooserDialog('Guardar a archivo',
                                  action = gtk.FILE_CHOOSER_ACTION_SAVE,
                                  buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                             gtk.STOCK_OK, gtk.RESPONSE_OK))
        opendialog.set_current_folder('/home/queen/bin/post-o-matic')
        respuesta = opendialog.run()
        if respuesta == gtk.RESPONSE_OK:
            nombre_archivo = opendialog.get_filename()
            f = open(nombre_archivo, 'w')
            widget = self.wids['tv_texto']
            buf = widget.get_buffer()
            txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
            f.write(txt)
        opendialog.destroy()

    def cortar(self, menuitem):
        # Estas dos líneas se repiten: REFACTORINGGGGGÑE
        buf = self.wids['tv_texto'].get_buffer()  # @UnusedVariable
#    clipboard = gtk.Clipboard(gtk.gdk.display_get_default(), "PRIMARY")
#    buf.cut_clipboard(clipboard, wids['tv_texto'].get_editable())  #WTF?

    def copiar(self, menuitem):
        buf = self.wids['tv_texto'].get_buffer()  # @UnusedVariable
#    clipboard = gtk.Clipboard(gtk.gdk.display_get_default(), "PRIMARY")
#    buf.copy_clipboard(clipboard)

    def pegar(self, menuitem):
        buf = self.wids['tv_texto'].get_buffer()  # @UnusedVariable
#    clipboard = gtk.Clipboard(gtk.gdk.display_get_default(), "PRIMARY")
#    buf.paste_clipboard(clipboard, None, wids['tv_texto'].get_editable())

    def borrar(self, menuitem):
        self.wids['tv_texto'].get_buffer().set_text('')

    def copiar_todo(self, menuitem):
        buf = self.wids['tv_texto'].get_buffer()
        buf.select_range(buf.get_start_iter(), buf.get_end_iter())
#    clipboard = gtk.Clipboard(gtk.gdk.display_get_default(), "PRIMARY")
#    buf.copy_clipboard(clipboard)

    def insertar_imagen(self, 
                        file_name = "/usr/share/pixmaps/vim-32.xpm", 
                        buf = None,
                        pos = None):
        if buf == None:
            buf = self.wids['tv_texto'].get_buffer(),
#    buf.create_tag ('center-image', justification = gtk.JUSTIFY_CENTER)
        pixbuf = gtk.gdk.pixbuf_new_from_file (file_name)
        if pos == None:
            # putting the image at the end.
            sob, eob = buf.get_bounds()  # @UnusedVariable
            pos = eob
#    mark = buf.create_mark (None, pos)
        buf.insert_pixbuf (pos, pixbuf)

    def vista_previa(self, boton):
        self.actualizar_vista_previa(None)
        self.wids['vpaned1'].set_position(0)

    def actualizar_vista_previa(self, widget):
        """
        Actualiza la vista previa, pero también se asegura de que 
        si hay un objeto relacionado su campo notas también esté 
        siempre actualizado y contenga lo mismo que aparece en 
        el TextView de texto.
        """
        # Si hay objeto, actualizo el campo notas primero
        if self.objeto:
            self.objeto.notas = textview_get_all_text(self.wids['tv_texto'])
        # Y posteriormente actualizo el textview de vista previa en sí.
        buf = self.wids['tv_texto'].get_buffer()
        sob, eob = buf.get_bounds()
        texto = buf.get_text(sob, eob)
        buf = self.wids['tv_preview'].get_buffer()
        buf.set_text("")
        self.insertar_con_imagenes_en_buffer(texto, buf)
        self.reemplazar_tags(buf)

    def reemplazar_tags(self, buf):
        """
        Reemplaza las etiquetas [size=], [color=], etc... por tags 
        en el buffer buf.
        """
        self.marcar_italic(buf)
        self.marcar_underline(buf)
        self.marcar_bold(buf)
        self.marcar_color(buf)
        self.marcar_size(buf)
        self.marcar_quote(buf)
        self.marcar_code(buf)

    def marcar_quote(self, buf):
        itr = buf.get_start_iter()
        while True:
            try:
                match_start, match_end = itr.forward_search("[quote=", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.delete(match_start, match_end)
                
                match_start2, match_end2 = match_end.forward_search("]", gtk.TEXT_SEARCH_TEXT_ONLY)
                citado = buf.get_text(match_start, match_start2)
                buf.delete(match_start, match_end2)
                buf.insert_with_tags_by_name(match_end2, "%s: " % (citado), "citado")
                
                match_start3, match_end3 = match_end2.forward_search("[/quote]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.apply_tag_by_name("quote", match_end2, match_end3)
                buf.delete(match_start3, match_end3)
                
                itr = match_end3
            except TypeError:   # unpack non-sequence. No hay más coincidencias
                return

    def marcar_size(self, buf):
        itr = buf.get_start_iter()
        while True:
            try:
                match_start, match_end = itr.forward_search("[size=", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.delete(match_start, match_end)
                
                match_start2, match_end2 = match_end.forward_search("]", gtk.TEXT_SEARCH_TEXT_ONLY)
                color = buf.get_text(match_start, match_start2)
                buf.delete(match_start, match_end2)
                
                match_start3, match_end3 = match_end2.forward_search("[/size]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.apply_tag_by_name(color, match_start, match_end3)
                buf.delete(match_start3, match_end3)
                
                itr = match_end3
            except TypeError:   # unpack non-sequence. No hay más coincidencias
                return

    def marcar_color(self, buf):
        itr = buf.get_start_iter()
        while True:
            try:
                match_start, match_end = itr.forward_search("[color=", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.delete(match_start, match_end)
                
                match_start2, match_end2 = match_end.forward_search("]", gtk.TEXT_SEARCH_TEXT_ONLY)
                color = buf.get_text(match_start, match_start2)
                buf.delete(match_start, match_end2)
                
                match_start3, match_end3 = match_end2.forward_search("[/color]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.apply_tag_by_name(color, match_start, match_end3)
                buf.delete(match_start3, match_end3)
                
                itr = match_end3
            except TypeError:   # unpack non-sequence. No hay más coincidencias
                return

    def marcar_underline(self, buf):
        itr = buf.get_start_iter()
        while True:
            try:
                match_start, match_end = itr.forward_search("[u]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.delete(match_start, match_end)
                match_start2, match_end2 = match_end.forward_search("[/u]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.apply_tag_by_name("underline", match_start, match_end2)
                buf.delete(match_start2, match_end2)
                itr = match_end2
            except TypeError:   # unpack non-sequence. No hay más coincidencias
                return

    def marcar_bold(self, buf):
        itr = buf.get_start_iter()
        while True:
            try:
                match_start, match_end = itr.forward_search("[b]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.delete(match_start, match_end)
                match_start2, match_end2 = match_end.forward_search("[/b]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.apply_tag_by_name("bold", match_start, match_end2)
                buf.delete(match_start2, match_end2)
                itr = match_end2
            except TypeError:   # unpack non-sequence. No hay más coincidencias
                return

    def marcar_italic(self, buf):
        itr = buf.get_start_iter()
        while True:
            try:
                match_start, match_end = itr.forward_search("[i]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.delete(match_start, match_end)
                match_start2, match_end2 = match_end.forward_search("[/i]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.apply_tag_by_name("italic", match_start, match_end2)
                buf.delete(match_start2, match_end2)
                itr = match_end2
            except TypeError:   # unpack non-sequence. No hay más coincidencias
                return

    def marcar_code(self, buf):
        itr = buf.get_start_iter()
        while True:
            try:
                match_start, match_end = itr.forward_search("[code]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.delete(match_start, match_end)
                buf.insert(match_start, "\n")
                match_start2, match_end2 = match_start.forward_search("[/code]", gtk.TEXT_SEARCH_TEXT_ONLY)
                buf.apply_tag_by_name("code", match_start, match_end2)
                buf.delete(match_start2, match_end2)
                buf.insert(match_start2, "\n")
                itr = match_start2
            except TypeError:   # unpack non-sequence. No hay más coincidencias
                return

    def crear_tags(self, buf):
        """
        Crea tags para aplicar con apply_tag_by_name.
        """
        tags = []
        tags.append(buf.create_tag("darkred", foreground="darkred"))
        tags.append(buf.create_tag("red", foreground="red"))
        tags.append(buf.create_tag("orange", foreground="orange"))
        tags.append(buf.create_tag("brown", foreground="brown"))
        tags.append(buf.create_tag("yellow", foreground="yellow"))
        tags.append(buf.create_tag("green", foreground="green"))
        tags.append(buf.create_tag("olive", foreground="#006000"))  # O el que sea.
        tags.append(buf.create_tag("cyan", foreground="cyan"))
        tags.append(buf.create_tag("blue", foreground="blue"))
        tags.append(buf.create_tag("darkblue", foreground="darkblue"))
        tags.append(buf.create_tag("indigo", foreground="#000060")) # O el que sea.
        tags.append(buf.create_tag("violet", foreground="violet"))
        tags.append(buf.create_tag("white", foreground="white"))
        tags.append(buf.create_tag("black", foreground="black"))

        tags.append(buf.create_tag("7", size_points=5))
        tags.append(buf.create_tag("9", size_points=7))
        tags.append(buf.create_tag("12", size_points=9))
        tags.append(buf.create_tag("18", size_points=18))
        tags.append(buf.create_tag("24", size_points=24))
       
        tags.append(buf.create_tag("underline", underline=pango.UNDERLINE_SINGLE))
        tags.append(buf.create_tag("bold", weight=pango.WEIGHT_BOLD))
        tags.append(buf.create_tag("italic", style=pango.STYLE_ITALIC))

        tags.append(buf.create_tag("quote", background="gray"))
        tags.append(buf.create_tag("citado", background="black", foreground="white"))
        tags.append(buf.create_tag("code", font="Monospace"))
        
        return tags

    def insertar_con_imagenes_en_buffer(self, texto, buf):
        """
        Recorre el texto buscando etiquetas "[img]", reemplazándolas
        por las imágenes correspondientes a la vez que inserta el 
        resto del texto en el buffer de destino.
        Las imágenes son descargadas de su localización en el 
        directorio temporal antes de insertarlas si se previsualizan
        por primera vez.
        NO REALIZA ANÁLISIS SINTÁCTICO. Todo esto con regexp sería mejón, ¿no?
        """
        import tempfile, urllib, os
        posl = texto.find('[img]')
        while posl != -1:
            subtexto = texto[:posl]
            buf.insert_at_cursor(subtexto)
            posr = texto.find("""[/img]""")+len("""[/img]""")
            imagen = texto[posl:posr]
            uri = imagen.replace("""[img]""", "").replace("""[/img]""", "")
            nombreimg = uri[uri.rfind('/')+1:]
            ruta = os.path.join(tempfile.gettempdir(), nombreimg)
            if not os.path.exists(ruta):
                urllib.urlretrieve(uri, ruta)
            self.insertar_imagen(ruta, buf)
            texto = texto[posr:]
            posl = texto.find('[img]')
        buf.insert_at_cursor(texto)

# --------------- Procedimientos auxiliares -------------------------
def attach_menu_notas(tv, clase, usuario, col = None):
    """
    Recibe un TreeView y le asocia un menú contextual con la
    opción "Notas" que lanza el editor de la clase con el 
    objeto cuyo ID sea el de la última columna del modelo 
    relacionado con el TextView. La clase del objeto cuyo ID
    buscará y sus notas intentará abrir en la ventana del 
    editor de texto se recibe como segundo parámetro.
    usuario es el usuario registrado de la ventana a la 
    que pertenece el treeview
    Si «col» es un entero, añade un icono "Notas" a la columna
    dentro de un nuevo Cell que por defecto no es visible.
    """
    ui_string = """<ui>
                    <popup name='Popup'>
                        <menuitem name='Notas' action='Notas'/>
                    </popup>
                   </ui>"""
    ag = gtk.ActionGroup('WindowActions')
    actions = [('Notas', gtk.STOCK_EDIT, '_Notas', '<Control>n',
                'Editar notas relacionadas.', 
                abrir_notas)]
    ag.add_actions(actions, (tv, clase, usuario))
    ui = gtk.UIManager() 
    ui.insert_action_group(ag, 0)
    ui.add_ui_from_string(ui_string)
    tv.connect('button_release_event', button_clicked, ui, tv, clase, usuario)
    if isinstance(col, int):
        cell = gtk.CellRendererPixbuf()
        columna = tv.get_column(col)
        columna.pack_end(cell, False)
        def check_notas(columna, cell, model, itr):
            try:
                uid = model[itr][-1]
                if isinstance(uid, str):
                    from framework import pclases
                    objeto = pclases.getObjetoPUID(uid)
                else:
                    objeto = clase.get(uid)
            # except pclases.SQLObjectNotFound:
            except Exception:  
                # Casi con total seguridad es un pclases.SQLObjectNotFound, pero paso de importar pclases aquí solo para eso.
                # El objeto se ha borrado.
                objeto = None
            if hasattr(objeto, 'notas') and objeto.notas:
                pb = gtk.STOCK_EDIT
                text = objeto.notas  # @UnusedVariable
            else:
                pb = None
                text = ""  # @UnusedVariable
            cell.set_property("stock-id", pb)
            # cell.set_tooltip_text(text) TODO: Los CellRenderer no derivan de Widget, la forma de poner un tooltip en un TreeView 
            # es meter el texto en una columna del model y hacer tv.set_tooltip_column(num_columna_del_model_que_contiene_el_texto).
            refcolorcell = [c for c in columna.get_cell_renderers() if c is not cell]
            if refcolorcell:
                #pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 1, 1)
                #pb.fill(0x00010000)
                refcolorcell = refcolorcell[0]
                color = refcolorcell.get_property("cell-background-gdk")
                if color.red == color.green == color.blue == 0: # HACK: Mi canal alfa particular. Si no, saldría con fondo negro 
                    cell.set_property("cell-background", None)  # en lugar del blanco (o el que sea) del theme GTK.
                else:
                    try:
                        cell.set_property("cell-background", color.to_string())
                    except AttributeError:  # PyGTK < 2.12
                        stringcolor = color_to_string(color)
                        cell.set_property("cell-background", stringcolor)
        columna.set_cell_data_func(cell, check_notas)

def color_to_string(color):
    stringcolor = "#"
    cadred = hex(color.red).replace("0x", "")
    cadgreen = hex(color.green).replace("0x", "")
    cadblue = hex(color.blue).replace("0x", "")
    while len(cadred) < 4:
        cadred = "0" + cadred
    while len(cadgreen) < 4:
        cadgreen = "0" + cadgreen
    while len(cadblue) < 4:
        cadblue = "0" + cadblue
    stringcolor += cadred + cadgreen + cadblue
    return stringcolor

def abrir_notas(algo, tv, clase, usuario):
    seleccion = tv.get_selection()
    model, paths = seleccion.get_selected_rows()
    itr = model.get_iter(paths[0])
    ide = model[itr][-1]
    try:
        objeto = clase.get(ide)
    except ValueError:  # Es un PUID
        from framework import pclases
        objeto = pclases.getObjetoPUID(ide)
    ventana = Postomatic(objeto, usuario)  # @UnusedVariable

def button_clicked(w, event, ui, tv, clase, usuario = None):
    if event.button == 3:
        seleccion = tv.get_selection()
        if seleccion != None:
            model, paths = seleccion.get_selected_rows()  # @UnusedVariable
            if len(paths) > 0:
                widget = ui.get_widget("/Popup")
                single_selection = len(paths) == 1
                menuitem = ui.get_widget("/Popup/Notas")
                menuitem.set_sensitive(single_selection)
                widget.popup(None, None, None, event.button, event.time)

# --------------- Rutina principal ----------------------------------
if __name__ == "__main__":
    v = Postomatic()

