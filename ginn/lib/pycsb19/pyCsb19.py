#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, gtk.glade  # @UnusedImport
import gobject
from lib.pycsb19 import remesas
from lib.pycsb19 import ordenante
from lib.pycsb19 import presentador
from lib.pycsb19 import importar
import sqlite3 as sqlite



class GesRemesas:
    def __init__(self):

        glRemesas=gtk.glade.XML("./gld/gesremesas.glade")
        self.ventana=glRemesas.get_widget("GesRemesas")
        self.ventana.connect("destroy", self.Salir)
        
        self.btnPresentador=glRemesas.get_widget("btnPresentador")
        self.btnPresentador.connect("clicked",self.LlamaPresentador)

        self.btnOrdenante=glRemesas.get_widget("btnOrdenante")
        self.btnOrdenante.connect("clicked",self.LlamaOrdenante)
        
        
        self.tvRemesas=glRemesas.get_widget("tvRemesas")
        self.tvRemesas.connect("button_press_event",self.SacaCampos)
 
 
        self.btnNueva=glRemesas.get_widget("btnNueva")
        self.btnNueva.connect("clicked", self.Nueva)
        
        self.btnAbrir=glRemesas.get_widget("btnAbrir")
        self.btnAbrir.connect("clicked", self.Abrir)
        
        self.btnEliminar=glRemesas.get_widget("btnEliminar")
        self.btnEliminar.connect("clicked", self.Eliminar)

        self.btnEspeciales=glRemesas.get_widget("btnEspeciales")
        self.btnEspeciales.connect("clicked", self.Especiales)

        self.btnImportar=glRemesas.get_widget("btnImportar")
        self.btnImportar.connect("clicked", self.Importar)
        
        self.btnAyuda=glRemesas.get_widget("btnAyuda")
        self.btnAyuda.connect("clicked", self.Ayuda)

        self.btnSalir=glRemesas.get_widget("btnSalir")
        self.btnSalir.connect("clicked", self.Salir)
        
        self.btnAcercade=glRemesas.get_widget("btnAcercade")
        self.btnAcercade.connect("clicked", self.Acercade)

        
        self.v=glRemesas.get_widget("vbuttonbox1")
        
        
        self.tNombre=glRemesas.get_widget("tNombre")
        
        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvRemesas.set_model(data)
        
        column = gtk.TreeViewColumn(" Remesa                                                                                    ", gtk.CellRendererText(), text=0)
        self.tvRemesas.append_column(column)
        
        render=gtk.CellRendererText()
        render.set_property('xalign', 1.0)
        column = gtk.TreeViewColumn(" Importe",render, text=1)
        self.tvRemesas.append_column(column)

        self.Comprueba()

        self.CargaDatos()
        
        gtk.main()

    def Comprueba(self):
        try:
            f=open("./dbCsb19/db")
            f.close()
        except:
            #Creamos la base de datos
            conn = sqlite.connect(db="./dbCsb19/db", mode=077)  # @UndefinedVariable
            cursor = conn.cursor()
            cursor.execute("create table presentadores (nif varchar, sufijo varchar, nombre varchar, banco varchar,oficina varchar)")
            conn.commit()
            cursor.execute("create table ordenantes (nif varchar, sufijo varchar, nombre varchar, banco varchar,oficina varchar, dc varchar, cuenta varchar)")
            conn.commit()
            cursor.execute("create table clientes (codigo varchar, nif varchar, nombre varchar, direccion varchar, ciudad varchar, cp varchar, banco varchar, oficina varchar, dc varchar, cuenta varchar)")
            conn.commit()
            cursor.execute("create table remesas (codigo integer, titulo varchar, importe float, generada varchar, presentador varchar, ordenante varchar, fecha date)")
            conn.commit()
            cursor.execute("create table det_remesas (codigo integer, indice integer, cliente varchar, importe float, conceptos varchar)")
            conn.commit()
            conn.close()

        
    def AbreDb(self):
        self.conexion= sqlite.connect(db="./dbCsb19/db", mode=077)  # @UndefinedVariable
        
    def CierraDb(self):
        self.conexion.close()

    def SacaCampos(self,widget,event):
            if event.type==5:
                self.Abrir(widget)
                
    def CargaDatos(self):
        #Tengo que abrir otra conexion porque sino no me actualiza los datos
        self.AbreDb()
        c = self.conexion.cursor()
        sql="select titulo, importe from remesas"
        c.execute(sql)
            
        for x in c.fetchall():
            item=[]
            numero=0
            for n in x:
                numero=numero+1
                if numero==2:
                    #Todo este rollo es para completar el importe con dos decimales en el treeview
                    cadena=str(n)
                    if cadena.find(".")==-1:
                        if cadena=="0":
                            cadena="0.00"
                        elif cadena=="":
                            cadena="0.00"
                        elif cadena==" ":
                            cadena="0.00"
                        else:
                            cadena=cadena+".00"
                    elif (len(cadena)-1)-cadena.find(".")<2:
                        cadena=cadena+"0"
                    item.append(cadena)
                else:
                    item.append(n)
                
            self.VisualizaDatos(item)
        self.CierraDb()

    def VisualizaDatos(self,Datos):
        store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING)  # @UnusedVariable
        store=self.tvRemesas.get_model()
        itr=store.append()
        store.set(itr,0,Datos[0],1,Datos[1])
        self.tvRemesas.set_model(store)

    def LlamaPresentador(self,widget):
        Presen=presentador.Presentador()
        Presen.Llamada="gesremesas"
        #Presen.ventana.set_modal(True)
        

    def LlamaOrdenante(self,widget):
        Orden=ordenante.Ordenante()
        Orden.Llamada="gesremesas"
        #Orden.ventana.set_modal(True)
    
    def Eliminar(self,widget):
        store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING)  # @UnusedVariable
        store=self.tvRemesas.get_model()
        if self.tvRemesas.get_cursor()[0]<>None:
            #cone=gadfly.gadfly("csb19","./dbCsb19/")
            
            self.AbreDb()
            c=self.conexion.cursor()
            sql="Select codigo from remesas where titulo='"+store[self.tvRemesas.get_cursor()[0][0]][0]+"'"
            c.execute(sql)
            Cod=str(c.fetchall()[0][0])
            
            c=self.conexion.cursor()
            sql="delete from det_remesas where codigo='"+Cod+"'"
            c.execute(sql)
            self.conexion.commit()
            
            c = self.conexion.cursor()
            sql="delete from remesas where codigo='"+Cod+"'"
            c.execute(sql)
            self.conexion.commit()
            

            store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING)
            self.tvRemesas.set_model(store)
            self.CierraDb()
            
            self.CargaDatos()
            
        else:
            d=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,"Debe de seleccionar una remesa para poder eliminarla")
            d.connect('response', lambda dialog, response: dialog.destroy())
            d.show()
            
        
        
    def Abrir(self,widget):
        # self.tvRemesas.get_cursor()
        # lista de dos elementos: 
        # 1 -> numero de elemento del tree view
        # 2 -> gtk.TreeViewColumn object
        store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING)  # @UnusedVariable
        store=self.tvRemesas.get_model()
        if self.tvRemesas.get_cursor()[0]<>None:
            self.RemAbrir=remesas.Remesas()
            self.RemAbrir.Llamada="gesremesas"
            self.RemAbrir.tNombre.set_text(store[self.tvRemesas.get_cursor()[0][0]][0])
            self.RemAbrir.MiraRemesa(store[self.tvRemesas.get_cursor()[0][0]][0])
            #self.RemAbrir.ventana.set_modal(True)
            #self.timeout= gtk.timeout_add(250, self.ActualizaTreeView)
            self.timeout= gobject.timeout_add(250, self.ActualizaTreeView)
        else:
            d=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,"Debe de seleccionar una remesa para poder abrirla")
            d.connect('response', lambda dialog, response: dialog.destroy())
            d.show()

    def Nueva(self,widget):
        glDialogo=gtk.glade.XML("./gld/dialogo.glade")
        self.Dialogo=glDialogo.get_widget("Dialogo")
        self.Dialogo.connect("destroy", self.DialogoSalir)

        self.DialogobtnSalir=glDialogo.get_widget("btnCancelar")
        self.DialogobtnSalir.connect("clicked", self.DialogoSalir)

        self.DialogobtnAceptar=glDialogo.get_widget("btnAceptar")
        self.DialogobtnAceptar.connect("clicked", self.DialogoAceptar)

        self.DialogoNombre=glDialogo.get_widget("tTexto")
        self.Dialogo.show()

    def ActualizaTreeView(self):
        if self.RemAbrir.Llamada<>"gesremesas":
            store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING)
            self.tvRemesas.set_model(store)
            self.CargaDatos()
            return 0
        else:
            return 1

    def Especiales(self,widget):
        pass

    def Importar(self,widget):
        Imp=importar.Importar()
        Imp.Llamada="gesremesas"


    def Ayuda(self,widget):
        msg="Futuras opciones:\n"
        msg=msg+"- Importar datos desde otros ficheros de texto (cvs)\n"
        msg=msg+"- Conversiones generales de los conceptos\n"
        msg=msg+"- Conversiones generales de los importes\n"
        msg=msg+"- Estudiar el poder definir grupos de clientes para poder hacer "
        msg=msg+"  estas operaciones y generar remesas en funcion de los grupos\n"
        msg=msg+"- Poder serializar los recibos indicando el numero de factura y que "
        msg=msg+"  se lo ponga de forma correlativa a todas los recibos\n"
        msg=msg+"- Poder visualizar los ficheros de devoluciones\n"
        msg=msg+"- lo que se me ocurra\n"
        d=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,msg,)
        d.connect('response', lambda dialog, response: dialog.destroy())
        d.show()

    def DialogoSalir(self,widget):
        self.DialogoNombre.set_text("")
        self.Dialogo.hide()
    
        
    def DialogoAceptar(self,widget):
        if self.DialogoNombre.get_text()<>"":
            self.RemAbrir=remesas.Remesas()
            self.RemAbrir.Llamada="gesremesas"
            self.RemAbrir.tNombre.set_text(self.DialogoNombre.get_text())
            self.RemAbrir.MiraRemesa(self.DialogoNombre.get_text())
            #self.RemAbrir.ventana.set_modal(True)
            self.timeout= gtk.timeout_add(250, self.ActualizaTreeView)
        self.Dialogo.hide()

    def Acercade(self, widget):
        glAcercade= gtk.glade.XML("./gld/acercade.glade")
        self.vent_acercade=glAcercade.get_widget("acercade")
        
        self.okbutton1=glAcercade.get_widget("okbutton1")
        self.okbutton1.connect("clicked", lambda glAcercade, response: self.vent_acercade.destroy(),None)

    def Salir(self,widget):
        gtk.main_quit()
        
if __name__ == "__main__":
    gtk.rc_parse("gtkrc.txt")
    ven = GesRemesas()
