#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk  # @UnusedImport
import gtk.glade
import gobject
import sqlite3 as sqlite

class Cliente:
    def __init__(self):
        #Esta variable nos va a decir si esta ventana se abre por si sola o la llamo otra ventana
        self.Llamada=""
        self.CodCliente=""
        self.NomCliente=""
        self.ccc=""
        
        glClientes = gtk.glade.XML("./gld/clientes.glade")
        self.ventana=glClientes.get_widget("Clientes")
        self.ventana.connect("destroy", self.Salir)
        self.ventana.connect("delete_event",self.Salir)

        self.Status=glClientes.get_widget("Status")
        con = self.Status.get_context_id("Informacion")
        
        self.tvClientes=glClientes.get_widget("tvClientes")
        self.tvClientes.connect("button_press_event",self.SacaCampos)
        self.tvClientes.connect("leave_notify_event", self.Identifica, con)
        
        self.tNif=glClientes.get_widget("tNif")
        self.tNif.connect("leave_notify_event", self.Identifica, con)
        
        self.tCodigo=glClientes.get_widget("tCodigo")
        self.tCodigo.connect("leave_notify_event", self.Identifica, con)
        
        
        self.tNombre=glClientes.get_widget("tNombre")
        self.tNombre.connect("leave_notify_event", self.Identifica, con)
        
        self.tDireccion=glClientes.get_widget("tDireccion")
        
        self.tCiudad=glClientes.get_widget("tCiudad")
        
        self.tCp=glClientes.get_widget("tCp")
        self.tCp.connect("key_release_event",self.SoloNumeros)
       
        self.tBanco=glClientes.get_widget("tBanco")
        self.tBanco.connect("key_release_event",self.SoloNumeros)
        self.tBanco.connect("leave_notify_event", self.Identifica, con)
        
        self.tOficina=glClientes.get_widget("tOficina")
        self.tOficina.connect("key_release_event",self.SoloNumeros)
        self.tOficina.connect("leave_notify_event", self.Identifica, con)

        self.tDc=glClientes.get_widget("tDc")
        self.tDc.connect("key_release_event",self.SoloNumeros)
        self.tDc.connect("leave_notify_event", self.Identifica, con)

        self.tCuenta=glClientes.get_widget("tCuenta")
        self.tCuenta.connect("key_release_event",self.SoloNumeros)
        self.tCuenta.connect("leave_notify_event", self.Identifica, con)

        self.btnCancelar=glClientes.get_widget("btnSalir")
        self.btnCancelar.connect("clicked", self.Salir)
        self.btnCancelar.connect("leave_notify_event", self.Identifica, con)
        

        self.btnAnadir=glClientes.get_widget("btnAnadir")
        self.btnAnadir.connect("clicked", self.Anadir)
        self.btnAnadir.connect("leave_notify_event", self.Identifica, con)

        self.btnEliminar=glClientes.get_widget("btnEliminar")
        self.btnEliminar.connect("clicked", self.Eliminar)
        self.btnEliminar.connect("leave_notify_event", self.Identifica, con)

        self.btnModificar=glClientes.get_widget("btnModificar")
        self.btnModificar.connect("clicked", self.Modificar)
        self.btnModificar.connect("leave_notify_event", self.Identifica, con)

        self.btnAyuda=glClientes.get_widget("btnAyuda")
        self.btnAyuda.connect("clicked", self.Ayuda)
        self.btnAyuda.connect("leave_notify_event", self.Identifica, con)

        
        
        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvClientes.set_model(data)
        
        column = gtk.TreeViewColumn("Codigo     ", gtk.CellRendererText(), text=0)
        self.tvClientes.append_column(column)
        column = gtk.TreeViewColumn("Nif                 ", gtk.CellRendererText(), text=1)
        self.tvClientes.append_column(column)
        column = gtk.TreeViewColumn("Nombre                                                                                  ", gtk.CellRendererText(), text=2)
        self.tvClientes.append_column(column)
        column = gtk.TreeViewColumn("Banco", gtk.CellRendererText(), text=3)
        self.tvClientes.append_column(column)
        column = gtk.TreeViewColumn("Oficina", gtk.CellRendererText(), text=4)
        self.tvClientes.append_column(column)
        column = gtk.TreeViewColumn("DC", gtk.CellRendererText(), text=5)
        self.tvClientes.append_column(column)
        column = gtk.TreeViewColumn("Cuenta", gtk.CellRendererText(), text=6)
        self.tvClientes.append_column(column)
        
        
        self.LeeFichero()
        
    def AbreDb(self):
        self.conexion= sqlite.connect(db="./dbCsb19/db", mode=077)
        
    def CierraDb(self):
        self.conexion.close()
        
       
    def Identifica(self, Widget, con, x):
        if Widget.name=="tCodigo":
            self.Status.push(x, "Introducir el codigo del cliente")
        elif Widget.name=="tNif":
            self.Status.push(x, "Introducir el N.I.F. del cliente")
        elif Widget.name=="tNombre":
            self.Status.push(x, "Introducir el nombre del cliente")
        elif Widget.name=="tBanco":
            self.Status.push(x, "Introducir el codigo del banco (numerico de 4 caracteres)")
        elif Widget.name=="tOficina":
            self.Status.push(x, "Introducir el codigo de la oficina (numerico de 4 caracteres)")
        elif Widget.name=="tDc":
            self.Status.push(x, "Introducir los digitos de control de la cuenta (numerico de 2 caracteres)")
        elif Widget.name=="tCuenta":
            self.Status.push(x, "Introducir el numero de cuenta (numerico de 10 caracteres)")            
        elif Widget.name=="tvClientes":
            self.Status.push(x, "Haga doble click para seleccionar un cliente")
        elif Widget.name=="btnSalir":
            self.Status.push(x, "Salir de esta ventana")
        elif Widget.name=="btnAnadir":
            self.Status.push(x, "Grabar los datos del cliente")
        elif Widget.name=="btnModificar":
            self.Status.push(x, "Modificar los datos del cliente")
        elif Widget.name=="btnEliminar":
            self.Status.push(x, "Elimina los datos del cliente")
        elif Widget.name=="btnAyuda":
            self.Status.push(x, "Visualiza la ayuda")
        else:
            self.Status.push(x, Widget.name)
        return
        
    def VisualizaDatos(self,Datos):
        #store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        store=self.tvClientes.get_model()
        itr=store.append()
        store.set(itr,0,Datos[0],1,Datos[1],2,Datos[2],3,Datos[6],4,Datos[7],5,Datos[8],6,Datos[9])
        self.tvClientes.set_model(store)

        
    def GrabaDatos(self,datos):
        self.AbreDb()
        cursor = self.conexion.cursor()
        sql="insert into clientes(codigo, nif, nombre, direccion, ciudad, cp, banco, oficina, dc, cuenta) values("
        for x in datos:
            sql=sql+"'"+x+"',"
        sql=sql[0:len(sql)-1]+")"
        cursor.execute(sql)
        self.conexion.commit()
        self.CierraDb()

    def LeeFichero(self):
        self.AbreDb()
        cursor = self.conexion.cursor()
        sql="select codigo, nif, nombre, direccion, ciudad, cp, banco, oficina, dc, cuenta from clientes"
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
            datos.append(self.tCodigo.get_text())
            datos.append(self.tNif.get_text())
            datos.append(self.tNombre.get_text())
            datos.append(self.tDireccion.get_text())
            datos.append(self.tCiudad.get_text())
            datos.append(self.tCp.get_text())
            datos.append(self.tBanco.get_text())
            datos.append(self.tOficina.get_text())
            datos.append(self.tDc.get_text())
            datos.append(self.tCuenta.get_text())
            datos.remove("")
            self.Eliminar(None)
            self.GrabaDatos(datos)
            self.VisualizaDatos(datos)
            self.LimpiaCampos()
        
        
    def Eliminar(self,widget):
        if self.tCodigo.get_text()<>"":
            #Vamos a comprobar que no este en alguna remesa
            self.AbreDb()
            cursor = self.conexion.cursor()
            sql="select count(cliente) from det_remesas where cliente='"+self.tCodigo.get_text()+"'"
            cursor.execute(sql)
            pp=int(cursor.fetchall()[0][0])
            self.CierraDb()
            if pp==0:
                #Primero borro los datos del TreeView
                store=self.tvClientes.get_model()
                store.remove(self.tvClientes.get_selection().get_selected()[1])
                self.tvClientes.set_model(store)            
            
                #Ahora borro los datos de la base de datos
                self.AbreDb()
                cursor = self.conexion.cursor()
                sql="Delete from clientes where codigo='"+self.tCodigo.get_text()+"'"
                cursor.execute(sql)
                self.conexion.commit()
                self.LimpiaCampos()
                self.CierraDb()
            else:
                self.Dialogo("Este cliente tiene un recibo en alguna remesa. Debe de eliminarlo de las remesas donde este antes de eliminarlo",1)
                self.LimpiaCampos()
            
            
            
    def Anadir(self,widget):
        if self.CompruebaCampos()==0:
            datos=[""]
            datos.append(self.tCodigo.get_text())
            datos.append(self.tNif.get_text())
            datos.append(self.tNombre.get_text())
            datos.append(self.tDireccion.get_text())
            datos.append(self.tCiudad.get_text())
            datos.append(self.tCp.get_text())
            datos.append(self.tBanco.get_text())
            datos.append(self.tOficina.get_text())
            datos.append(self.tDc.get_text())
            datos.append(self.tCuenta.get_text())
            datos.remove("")
            if self.CompruebaDuplicados()==False:
                self.GrabaDatos(datos)
                self.VisualizaDatos(datos)
                self.LimpiaCampos()
            else:
                self.Dialogo("Este codigo de cliente ya se estan utilizando. No se puede dar de alta otra vez",1)

    def CompruebaDuplicados(self):
        self.AbreDb()
        cursor = self.conexion.cursor()
        sql="Select nombre from clientes where codigo='"+self.tCodigo.get_text()+"'"
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
        if self.tCodigo.get_text()=="":
            self.Dialogo("No se ha introducido el nif",1)
            return 1
        elif self.tNif.get_text()=="":
            self.Dialogo("No se ha introducido el sufijo",1)
            return 1
        elif self.tNombre.get_text()=="":
            self.Dialogo("No se ha introducido el nombre",1)
            return 1
        elif self.tDireccion.get_text()=="":
            self.tDireccion.set_text(" ")
            return 0
        elif self.tCiudad.get_text()=="":
            self.tCiudad.set_text(" ")
            return 0
        elif self.tCp.get_text()=="":
            self.tCp.set_text(" ")
            return 0
        elif self.tBanco.get_text()=="":
            self.Dialogo("No se ha introducido el banco",1)
            return 1
        elif len(self.tBanco.get_text())<4:
            self.Dialogo("El codigo del banco ha de ser de 4 caracteres",1)
            return 1
        elif self.tBanco.get_text()=="0000":
            self.Dialogo("El codigo de banco no puede ser ceros",1)
            return 1            
        elif self.tOficina.get_text()=="":
            self.Dialogo("No se ha introducido la oficina",1)
            return 1
        elif len(self.tOficina.get_text())<4:
            self.Dialogo("El codigo de la oficina ha de ser de 4 caracteres",1)
            return 1
        elif self.tOficina.get_text()=="0000":
            self.Dialogo("El codigo de la oficina no puede ser ceros",1)
            return 1
        elif self.tDc.get_text()=="":
            self.tDc.set_text("**")
            return 0
        elif len(self.tDc.get_text())<2:
            self.Dialogo("El dc ha de ser de 2 caracteres",1)
            return 1
        elif self.tCuenta.get_text()=="":
            self.Dialogo("No se ha introducido el numero de cuenta",1)
            return 1
        elif len(self.tCuenta.get_text())<10:
            self.Dialogo("El codigo de cuenta ha de ser de 10 caracteres",1)
            return 1
        elif self.tCuenta.get_text()=="0000000000":
            self.Dialogo("El codigo de la cuenta no puede ser ceros",1)
            return 1
        else:
            if len(self.tDc.get_text())==2 and self.tDc.get_text()<>"**":
            #Calculamos a ver si el DC es correcto
                #if self.CalculaDC(self.tBanco.get_text()+self.tOficina.get_text()+self.tCuenta.get_text())==1:
                #    self.tDc.set_text("**")
                #    self.Dialogo("El DC introducido es erroneo. Se ha sustituido por **.",1)
                if self.CalcCC(self.tBanco.get_text(),self.tOficina.get_text(),self.tCuenta.get_text())<>self.tDc.get_text():
                    self.tDc.set_text("**")
                    self.Dialogo("El DC introducido es erroneo. Se ha sustituido por **.",1)
            return 0
        
    def CalculaDC(self,Dato):
        #Dato es el conjunto de BANCO+OFICINA+NUMERO_DE_CUENTA. En total deben de ser 18 caracteres
        if Dato=="":
            return 1
        else:
            pesos=[6,3,7,9,10,5,8,4,2,1]
            
            #Banco+oficina
            suma=0
            pe=0
            for n in range(7 ,-1,-1):
                #print "Valor: "+Dato[n:n+1]+" X "+str(pesos[pe])
                suma=suma+(int(Dato[n:n+1])*pesos[pe])
                pe=pe+1
            num=11-(suma%11)
            if num==10:
                num=1
            if num==11:
                num=0
            D=str(num)
            
            
            #Cuenta            
            suma=0
            pe=0
            for n in range(17 ,8,-1):
                #print "Valor: "+Dato[n:n+1]+" X "+str(pesos[pe])
                suma=suma+(int(Dato[n:n+1])*pesos[pe])
                pe=pe+1
            num=11-(suma%11)
            if num==10:
                num=1
            if num==11:
                num=0
            C=str(num)
            DC=D+C
            if DC<>self.tDc.get_text():
                return 1
            else:
                return 0

    def CRC(self,cTexto):
        factor=(1,2,4,8,5,10,9,7,3,6)
        # Cálculo CRC
        nCRC=0
        for n in range(10):
            nCRC += int(cTexto[n])*factor[n]
        # Reducción del CRC a un dígito
        nValor=11 - nCRC%11
        if nValor==10: nValor=1
        elif nValor==11: nValor=0
        return nValor
    def CalcCC(self,cBanco,cSucursal,cCuenta):
        cTexto="00%04d%04d" % (int(cBanco),int(cSucursal))
        DC1=self.CRC(cTexto)
        cTexto="%010d" % long(cCuenta)
        DC2=self.CRC(cTexto)
        return "%1d%1d" % (DC1,DC2)

    def SacaCampos(self, widget, event):
        #El 5 es doble click y el 4 es el simple
        if event.type==5:
                self.LimpiaCampos()
            #try:
                Linea=self.tvClientes.get_cursor()
                store=self.tvClientes.get_model()
                itr=store[Linea[0][0]]
                
                self.AbreDb()
                cursor = self.conexion.cursor()
                sql="select codigo, nif, nombre, direccion, ciudad, cp, banco, oficina, dc, cuenta from clientes where codigo='"+itr[0]+"'"
                cursor.execute(sql)
                for x in cursor.fetchall():
                    item=[]
                    for n in x:
                        item.append(n)
                self.CierraDb()
                
                self.tCodigo.set_text(item[0])
                self.tNif.set_text(item[1])
                self.tNombre.set_text(item[2])
                self.tDireccion.set_text(item[3])
                self.tCiudad.set_text(item[4])
                self.tCp.set_text(item[5])
                self.tBanco.set_text(item[6])
                self.tOficina.set_text(item[7])
                self.tDc.set_text(item[8])
                self.tCuenta.set_text(item[9])
                
                self.tCodigo.set_editable(0)
                self.tNif.set_editable(0)

               
            #except:
            #    print "Se salio por el pass de SacaCampos"
            #    pass
    
    def LimpiaCampos(self):
        self.tCodigo.set_editable(1)
        self.tNif.set_editable(1)
        self.tCodigo.set_text("")
        self.tNif.set_text("")
        self.tNombre.set_text("")
        self.tDireccion.set_text("")
        self.tCiudad.set_text("")
        self.tCp.set_text("")
        self.tBanco.set_text("")
        self.tOficina.set_text("")
        self.tDc.set_text("")
        self.tCuenta.set_text("")
        
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
            if self.tCodigo.get_text()<>"":
                self.CodCliente=self.tCodigo.get_text()
                self.NomCliente=self.tNombre.get_text()
                self.ccc=self.tBanco.get_text()+self.tOficina.get_text()+self.tDc.get_text()+self.tCuenta.get_text()
            else:
                self.CodCliente=""
                self.NomCliente=""
                self.ccc=""
                        
            self.ventana.hide()
            return True
        else:
            gtk.main_quit()

    def Main(self):
        self.Llamada=""
        gtk.main()
        
if __name__ == "__main__":
    gtk.rc_parse("gtkrc.txt")
    ven = Cliente()
    ven.Main()
