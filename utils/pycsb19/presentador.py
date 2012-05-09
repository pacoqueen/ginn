#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gtk.glade
import gobject
import sqlite

class Presentador:
    def __init__(self):
        self.Llamada=""
        self.Nif=""
        self.Sufijo=""
        
        glPresentador = gtk.glade.XML("./gld/presentador.glade")
        self.ventana=glPresentador.get_widget("Presentador")
        self.ventana.connect("destroy", self.Salir)
        
        self.Status=glPresentador.get_widget("Status")
        con = self.Status.get_context_id("Informacion")
        
        self.tvPresentador=glPresentador.get_widget("tvPresentador")
        self.tvPresentador.connect("button_press_event",self.SacaCampos)
        self.tvPresentador.connect("leave_notify_event", self.Identifica, con)
        
        self.Fondo1=glPresentador.get_widget("frame2")
        self.Fondo2=glPresentador.get_widget("fixed1")
        
        self.Fondo1.connect("leave_notify_event", self.Identifica, con)
        self.Fondo2.connect("leave_notify_event", self.Identifica, con)
        
        self.tNif=glPresentador.get_widget("tNif")
        self.tNif.connect("leave_notify_event", self.Identifica, con)
        
        self.tSufijo=glPresentador.get_widget("tSufijo")
        self.tSufijo.connect("key_release_event",self.SoloNumeros)
        self.tSufijo.connect("leave_notify_event", self.Identifica, con)
        
        
        self.tNombre=glPresentador.get_widget("tNombre")
        self.tNombre.connect("leave_notify_event", self.Identifica, con)
        
        self.tBanco=glPresentador.get_widget("tBanco")
        self.tBanco.connect("key_release_event",self.SoloNumeros)
        self.tBanco.connect("leave_notify_event", self.Identifica, con)
        
        self.tOficina=glPresentador.get_widget("tOficina")
        self.tOficina.connect("key_release_event",self.SoloNumeros)
        self.tOficina.connect("leave_notify_event", self.Identifica, con)
        
        self.btnCancelar=glPresentador.get_widget("btnSalir")
        self.btnCancelar.connect("clicked", self.Salir)
        self.btnCancelar.connect("leave_notify_event", self.Identifica, con)
        

        self.btnAnadir=glPresentador.get_widget("btnAnadir")
        self.btnAnadir.connect("clicked", self.Anadir)
        self.btnAnadir.connect("leave_notify_event", self.Identifica, con)

        self.btnEliminar=glPresentador.get_widget("btnEliminar")
        self.btnEliminar.connect("clicked", self.Eliminar)
        self.btnEliminar.connect("leave_notify_event", self.Identifica, con)

        self.btnModificar=glPresentador.get_widget("btnModificar")
        self.btnModificar.connect("clicked", self.Modificar)
        self.btnModificar.connect("leave_notify_event", self.Identifica, con)

        self.btnAyuda=glPresentador.get_widget("btnAyuda")
        self.btnAyuda.connect("clicked", self.Ayuda)
        self.btnAyuda.connect("leave_notify_event", self.Identifica, con)

        
        
        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvPresentador.set_model(data)
        
        column = gtk.TreeViewColumn("Nif                   ", gtk.CellRendererText(), text=0)
        self.tvPresentador.append_column(column)
        column = gtk.TreeViewColumn("Sufijo", gtk.CellRendererText(), text=1)
        self.tvPresentador.append_column(column)
        column = gtk.TreeViewColumn("Nombre                                                                                                    ", gtk.CellRendererText(), text=2)
        self.tvPresentador.append_column(column)
        column = gtk.TreeViewColumn("Banco", gtk.CellRendererText(), text=3)
        self.tvPresentador.append_column(column)
        column = gtk.TreeViewColumn("Oficina", gtk.CellRendererText(), text=4)
        self.tvPresentador.append_column(column)
        
        self.LeeDatos()
        

    def AbreDb(self):
        self.conexion= sqlite.connect(db="./dbCsb19/db", mode=077)
        
    def CierraDb(self):
        self.conexion.close()
        
        
    def Identifica(self, Widget, con, x):
        if Widget.name=="tNif":
            self.Status.push(x, "Introducir el nif del presentador")
        elif Widget.name=="tSufijo":
            self.Status.push(x, "Introducir el sufijo")
        elif Widget.name=="tNombre":
            self.Status.push(x, "Introducir el nombre del presentador")
        elif Widget.name=="tBanco":
            self.Status.push(x, "Introducir el codigo del banco (numerico de 4 caracteres)")
        elif Widget.name=="tOficina":
            self.Status.push(x, "Introducir el codigo de la oficina (numerico de 4 caracteres)")
        elif Widget.name=="tvPresentador":
            self.Status.push(x, "Haga doble click para seleccionar un presentador")
        elif Widget.name=="btnSalir":
            self.Status.push(x, "Salir de esta ventana")
        elif Widget.name=="btnAnadir":
            self.Status.push(x, "Grabar los datos del presentador")
        elif Widget.name=="btnModificar":
            self.Status.push(x, "Modificar los datos del presentador")
        elif Widget.name=="btnEliminar":
            self.Status.push(x, "Elimina los datos del presentador")
        elif Widget.name=="btnAyuda":
            self.Status.push(x, "Visualiza la ayuda")
        else:
            self.Status.push(x, Widget.name)
        return
        
    def VisualizaDatos(self,Datos):
        store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        store=self.tvPresentador.get_model()
        iter=store.append()
        store.set(iter,0,Datos[0],1,Datos[1],2,Datos[2],3,Datos[3],4,Datos[4])
        self.tvPresentador.set_model(store)
        
    def GrabaDatos(self,datos):
        self.AbreDb()
        cursor = self.conexion.cursor()
        sql="insert into presentadores(nif,sufijo,nombre,banco,oficina) values("
        for x in datos:
            sql=sql+"'"+x+"',"
        sql=sql[0:len(sql)-1]+")"
        cursor.execute(sql)
        self.conexion.commit()
        self.CierraDb()

    def LeeDatos(self):
        self.AbreDb()
        cursor = self.conexion.cursor()
        sql="select nif,sufijo,nombre,banco,oficina from presentadores"
        cursor.execute(sql)
        for x in cursor.fetchall():
            item=[]
            for n in x:
               item.append(n)
            self.VisualizaDatos(item)
        self.CierraDb()
        
    def Modificar(self,widget):
        if self.CompruebaCampos()==0:
            datos=[""]
            datos.append(self.tNif.get_text())
            datos.append(self.tSufijo.get_text())
            datos.append(self.tNombre.get_text())
            datos.append(self.tBanco.get_text())
            datos.append(self.tOficina.get_text())
            datos.remove("")
            self.Eliminar(None)
            self.GrabaDatos(datos)
            self.VisualizaDatos(datos)
            self.LimpiaCampos()
        
        
    def Eliminar(self,widget):
        if self.tNif.get_text()<>"":
            #Primero borro los datos del TreeView
            store=self.tvPresentador.get_model()
            store.remove(self.tvPresentador.get_selection().get_selected()[1])
            self.tvPresentador.set_model(store)            

            #Ahora borro los datos de la base de datos
            self.AbreDb()
            cursor = self.conexion.cursor()
            sql="Delete from presentadores where nif='"+self.tNif.get_text()+"' and sufijo='"+self.tSufijo.get_text()+"'"
            cursor.execute(sql)
            self.conexion.commit()
            self.LimpiaCampos()
            self.CierraDb()
            

    def Anadir(self,widget):
        #print "Estudiar el meter los datos en un diccionario"
        if self.CompruebaCampos()==0:
            datos=[""]
            datos.append(self.tNif.get_text())
            datos.append(self.tSufijo.get_text())
            datos.append(self.tNombre.get_text())
            datos.append(self.tBanco.get_text())
            datos.append(self.tOficina.get_text())
            datos.remove("")
            if self.CompruebaDuplicados()==False:
                self.GrabaDatos(datos)
                self.VisualizaDatos(datos)
                self.LimpiaCampos()
            else:
                self.Dialogo("Este nif y este sufijo ya se estan utilizando. No se pueden dar de alta otra vez",1)
            
    def CompruebaDuplicados(self):
        self.AbreDb()
        cursor = self.conexion.cursor()
        sql="Select nombre from presentadores where nif='"+self.tNif.get_text()+"' and sufijo='"+self.tSufijo.get_text()+"'"
        cursor.execute(sql)
        if cursor.fetchall()<>[]:
            #Es un duplicado
            self.CierraDb()
            return True
        else:
            #No es un duplicado
            self.CierraDb()
            return False
        

    def CompruebaCampos(self):
        Salida=""
        if self.tNif.get_text()=="":
            self.Dialogo("No se ha introducido el nif",1)
            return 1
        elif self.tSufijo.get_text()=="":
            self.Dialogo("No se ha introducido el sufijo",1)
            return 1
        elif self.tNombre.get_text()=="":
            self.Dialogo("No se ha introducido el nombre",1)
            return 1
        elif self.tBanco.get_text()=="":
            self.Dialogo("No se ha introducido el banco",1)
            return 1
        elif len(self.tBanco.get_text())<4:
            self.Dialogo("El codigo del banco ha de ser de 4 caracteres",1)
            return 1
        elif self.tOficina.get_text()=="":
            self.Dialogo("No se ha introducido la oficina",1)
            return 1
        elif len(self.tOficina.get_text())<4:
            self.Dialogo("El codigo de la oficina ha de ser de 4 caracteres",1)
            return 1
        else:
            return 0
        
    def SacaCampos(self, widget, event):
        #El 5 es doble click y el 4 es el simple
        if event.type==5:
            self.LimpiaCampos()
            try:
                Linea=self.tvPresentador.get_cursor()
                store=self.tvPresentador.get_model()
                iter=store[Linea[0][0]]
                self.tNif.set_text(iter[0])
                self.tSufijo.set_text(iter[1])
                self.tNombre.set_text(iter[2])
                self.tBanco.set_text(iter[3])
                self.tOficina.set_text(iter[4])
                self.tNif.set_editable(0)
                self.tSufijo.set_editable(0)
            except:
                pass
    
    def LimpiaCampos(self):
        self.tNif.set_editable(1)
        self.tSufijo.set_editable(1)
        self.tNif.set_text("")
        self.tSufijo.set_text("")
        self.tNombre.set_text("")
        self.tBanco.set_text("")
        self.tOficina.set_text("")
        
    def SoloNumeros(self,widget,x):
        #Comprueba lo que se teclea
        texto=widget.get_text()
        if texto.isdigit()==0:
            if len(texto)>0:
                texto=texto[0:len(texto)-1]
                widget.set_text(texto)
                widget.set_position(len(texto))
            
    def Dialogo(self,msg,Tipo):
        if Tipo==1:
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,msg)
        elif Tipo==2:
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_CLOSE,msg)
        elif Tipo==3:
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,msg)
        elif Tipo==4:
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL,msg)
        dialog.connect('response', lambda dialog, response: dialog.destroy())
        dialog.show()
        return dialog

    def Ayuda(self,widget):
        os.system("presentador.html")
        
    def Salir(self,*args):
        #True
        if self.Llamada<>"":
            if self.tNif.get_text()<>"":
                self.Nif=self.tNif.get_text()
                self.Sufijo=self.tSufijo.get_text()
            else:
                self.Nif=""
                self.Sufijo=""

            self.ventana.hide()
            return True
        else:
            gtk.main_quit()

    def Main(self):
        self.Llamada=""
        gtk.main()

if __name__ == "__main__":
    gtk.rc_parse("gtkrc.txt")
    ven = Presentador()
    ven.Main()

    
