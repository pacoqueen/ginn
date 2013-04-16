#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gtk  # @UnusedImport
import gtk.glade
import gobject
import sqlite3 as sqlite

# Mismo que en ../../formularios/utils.py. Prefiero este:
def cccCRC(cTexto):
    """Cálculo del CRC de un número de 10 dígitos
    ajustados con ceros por la izquierda"""
    factor=(1,2,4,8,5,10,9,7,3,6)
    # Cálculo CRC
    nCRC=0
    for n in range(10):
        nCRC += int(cTexto[n])*factor[n]
    # Reducción del CRC a un dígito
    nValor=11 - nCRC%11
    if nValor==10:
        nValor=1
    elif nValor==11:
        nValor=0
    return nValor


class Ordenante:
    def __init__(self):
        self.Llamada=""
        self.CodOrdenante=""
        self.NomOrdenante=""
        
        glOrdenante = gtk.glade.XML("./gld/ordenante.glade")
        self.ventana=glOrdenante.get_widget("Ordenante")
        self.ventana.connect("destroy", self.Salir)

        self.Status=glOrdenante.get_widget("Status")
        con = self.Status.get_context_id("Informacion")
        
        self.tvOrdenante=glOrdenante.get_widget("tvOrdenante")
        self.tvOrdenante.connect("button_press_event",self.SacaCampos)
        self.tvOrdenante.connect("leave_notify_event", self.Identifica, con)
        
        self.tNif=glOrdenante.get_widget("tNif")
        self.tNif.connect("leave_notify_event", self.Identifica, con)
        
        self.tSufijo=glOrdenante.get_widget("tSufijo")
        self.tSufijo.connect("key_release_event",self.SoloNumeros)
        self.tSufijo.connect("leave_notify_event", self.Identifica, con)
        
        
        self.tNombre=glOrdenante.get_widget("tNombre")
        self.tNombre.connect("leave_notify_event", self.Identifica, con)
        
        self.tBanco=glOrdenante.get_widget("tBanco")
        self.tBanco.connect("key_release_event",self.SoloNumeros)
        self.tBanco.connect("leave_notify_event", self.Identifica, con)
        
        self.tOficina=glOrdenante.get_widget("tOficina")
        self.tOficina.connect("key_release_event",self.SoloNumeros)
        self.tOficina.connect("leave_notify_event", self.Identifica, con)

        self.tDc=glOrdenante.get_widget("tDc")
        self.tDc.connect("key_release_event",self.SoloNumeros)
        self.tDc.connect("leave_notify_event", self.Identifica, con)

        self.tCuenta=glOrdenante.get_widget("tCuenta")
        self.tCuenta.connect("key_release_event",self.SoloNumeros)
        self.tCuenta.connect("leave_notify_event", self.Identifica, con)

        self.btnCancelar=glOrdenante.get_widget("btnSalir")
        self.btnCancelar.connect("clicked", self.Salir)
        self.btnCancelar.connect("leave_notify_event", self.Identifica, con)
        

        self.btnAnadir=glOrdenante.get_widget("btnAnadir")
        self.btnAnadir.connect("clicked", self.Anadir)
        self.btnAnadir.connect("leave_notify_event", self.Identifica, con)
        
        self.btnEliminar=glOrdenante.get_widget("btnEliminar")
        self.btnEliminar.connect("clicked", self.Eliminar)
        self.btnEliminar.connect("leave_notify_event", self.Identifica, con)
        
        self.btnModificar=glOrdenante.get_widget("btnModificar")
        self.btnModificar.connect("clicked", self.Modificar)
        self.btnModificar.connect("leave_notify_event", self.Identifica, con)
        
        self.btnAyuda=glOrdenante.get_widget("btnAyuda")
        self.btnAyuda.connect("clicked", self.Ayuda)
        self.btnAyuda.connect("leave_notify_event", self.Identifica, con)
        
        
        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvOrdenante.set_model(data)
        
        column = gtk.TreeViewColumn("Nif                   ", gtk.CellRendererText(), text=0)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Sufijo", gtk.CellRendererText(), text=1)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Nombre                                                                                  ", gtk.CellRendererText(), text=2)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Banco", gtk.CellRendererText(), text=3)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Oficina", gtk.CellRendererText(), text=4)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("DC", gtk.CellRendererText(), text=5)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Cuenta", gtk.CellRendererText(), text=6)
        self.tvOrdenante.append_column(column)
        
        self.LeeFichero()

    def AbreDb(self):
        self.conexion= sqlite.connect(db="./dbCsb19/db", mode=077)
        
    def CierraDb(self):
        self.conexion.close()
        
    def Identifica(self, Widget, con, x):
        if Widget.name=="tNif":
            self.Status.push(x, "Introducir el nif del ordenante")
        elif Widget.name=="tSufijo":
            self.Status.push(x, "Introducir el sufijo")
        elif Widget.name=="tNombre":
            self.Status.push(x, "Introducir el nombre del ordenante")
        elif Widget.name=="tBanco":
            self.Status.push(x, "Introducir el codigo del banco (numerico de 4 caracteres)")
        elif Widget.name=="tOficina":
            self.Status.push(x, "Introducir el codigo de la oficina (numerico de 4 caracteres)")
        elif Widget.name=="tDc":
            self.Status.push(x, "Introducir los digitos de control de la cuenta (numerico de 2 caracteres)")
        elif Widget.name=="tCuenta":
            self.Status.push(x, "Introducir el numero de cuenta (numerico de 10 caracteres)")            
        elif Widget.name=="tvOrdenante":
            self.Status.push(x, "Haga doble click para seleccionar un ordenante")
        elif Widget.name=="btnSalir":
            self.Status.push(x, "Salir de esta ventana")
        elif Widget.name=="btnAnadir":
            self.Status.push(x, "Grabar los datos del ordenante")
        elif Widget.name=="btnModificar":
            self.Status.push(x, "Modificar los datos del ordenante")
        elif Widget.name=="btnEliminar":
            self.Status.push(x, "Elimina los datos del ordenante")
        elif Widget.name=="btnAyuda":
            self.Status.push(x, "Visualiza la ayuda")
        else:
            self.Status.push(x, Widget.name)
        return
        
    def VisualizaDatos(self,Datos):
        store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)  # @UnusedVariable
        store=self.tvOrdenante.get_model()
        itr=store.append()
        store.set(itr,0,Datos[0],1,Datos[1],2,Datos[2],3,Datos[3],4,Datos[4],5,Datos[5],6,Datos[6])
        self.tvOrdenante.set_model(store)
        
    def GrabaDatos(self,datos):
        self.AbreDb()
        cursor = self.conexion.cursor()
        sql="insert into ordenantes(nif,sufijo,nombre,banco,oficina,dc,cuenta) values("
        for x in datos:
            sql=sql+"'"+x+"',"
        sql=sql[0:len(sql)-1]+")"
        cursor.execute(sql)
        self.conexion.commit()
        self.CierraDb()

    def LeeFichero(self):
        self.AbreDb()
        cursor = self.conexion.cursor()
        sql="select nif,sufijo,nombre,banco,oficina,dc,cuenta from ordenantes"
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
            datos.append(self.tDc.get_text())
            datos.append(self.tCuenta.get_text())
            datos.remove("")
            self.Eliminar(None)
            self.GrabaDatos(datos)
            self.VisualizaDatos(datos)
            self.LimpiaCampos()
        
        
    def Eliminar(self,widget):
        if self.tNif.get_text()<>"":
            #Vamos a comprobar que no este en alguna remesa no vaya a ser que la cagemos
            self.AbreDb()
            cursor = self.conexion.cursor()
            sql="select count(ordenante) from remesas where ordenante='"+self.tNif.get_text()+":"+self.tSufijo.get_text()+"'"
            cursor.execute(sql)
            pp=int(cursor.fetchall()[0][0])
            self.CierraDb()
            
            if pp==0:
                #Primero borro los datos del TreeView
                store=self.tvOrdenante.get_model()
                store.remove(self.tvOrdenante.get_selection().get_selected()[1])
                self.tvOrdenante.set_model(store)            

                #Ahora borro los datos de la base de datos
                self.AbreDb()
                cursor = self.conexion.cursor()
                sql="Delete from ordenantes where nif='"+self.tNif.get_text()+"' and sufijo='"+self.tSufijo.get_text()+"'"
                cursor.execute(sql)
                self.conexion.commit()
                self.CierraDb()
                self.LimpiaCampos()
            else:
                self.Dialogo("Este Ordenante esta activo en alguna remesa y no se puede eliminar",1)
                self.LimpiaCampos()

            
            

    def Anadir(self,widget):
        #print "Estudiar el meter los datos en un diccionario"
        if self.CompruebaCampos()==0:
            datos=[""]
            datos.append(self.tNif.get_text())
            datos.append(self.tSufijo.get_text())
            datos.append(self.tNombre.get_text())
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
                self.Dialogo("Este nif y este sufijo ya se estan utilizando. No se pueden dar de alta otra vez",1)
            
    def CompruebaDuplicados(self):
        self.AbreDb()
        cursor = self.conexion.cursor()
        sql="Select nombre from ordenantes where nif='"+self.tNif.get_text()+"' and sufijo='"+self.tSufijo.get_text()+"'"
        cursor.execute(sql)
        if cursor.fetchall()<>[]:
            #Es un duplicado
            self.CierraDb()
            return True
        else:
            #No es un duplicado
            self.CierraDb()
            return False
            
    def Ceros(self,Numero):
        d=""
        for n in range(0,Numero):  # @UnusedVariable
            d=d+"0"
        return d

    def CompruebaCampos(self):
        Sw=0
        if self.tNif.get_text()=="":
            self.Dialogo("No se ha introducido el nif",1)
            Sw=1
        elif self.tSufijo.get_text()=="":
            self.Dialogo("No se ha introducido el sufijo",1)
            Sw=1
        elif self.tNombre.get_text()=="":
            self.Dialogo("No se ha introducido el nombre",1)
            Sw=1
        elif self.tBanco.get_text()=="":
            self.Dialogo("No se ha introducido el banco",1)
            Sw=1
        elif len(self.tBanco.get_text())<4:
            self.Dialogo("El codigo del banco ha de ser de 4 caracteres",1)
            Sw=1
        elif self.tOficina.get_text()=="":
            self.Dialogo("No se ha introducido la oficina",1)
            Sw=1
        elif len(self.tOficina.get_text())<4:
            self.Dialogo("El codigo de la oficina ha de ser de 4 caracteres",1)
            Sw=1
        elif len(self.tDc.get_text())<2 and self.tDc.get_text()<>"":
            self.Dialogo("El dc ha de ser de 2 caracteres",1)
            Sw=1
        elif self.tCuenta.get_text()=="":
            self.Dialogo("No se ha introducido el numero de cuenta",1)
            Sw=1
        elif len(self.tCuenta.get_text())<10:
            self.Dialogo("El codigo de cuenta ha de ser de 10 caracteres",1)
            Sw=1
        
        if len(self.tNif.get_text())<9 and len(self.tNif.get_text())<>0:
            self.tNif.set_text(self.Ceros(9-len(self.tNif.get_text()))+self.tNif.get_text())
            
            

        if self.tDc.get_text()=="" and len(self.tNif.get_text())<>0:
            self.tDc.set_text("**")
            
        
        if len(self.tDc.get_text())==2 and self.tDc.get_text()<>"**":
        #Calculamos a ver si el DC es correcto
            if self.CalculaDC(self.tBanco.get_text()+self.tOficina.get_text()+self.tCuenta.get_text())<>0:
                self.Dialogo("Error:"+self.CalculaDC(self.tBanco.get_text()+self.tOficina.get_text()+self.tCuenta.get_text())+" - El DC introducido es erroneo, corrijalo antes de continuar",1)
                Sw=1
            else:
                Sw=0
        
        copia=""
        for n in self.tNif.get_text():
            if n.isalpha():
                n=n.upper()
            copia=copia+n
        
        self.tNif.set_text(copia)
        
        return Sw
        
    def SacaCampos(self, widget, event):
        #El 5 es doble click y el 4 es el simple
        if event.type==5:
            self.LimpiaCampos()
            try:
                Linea=self.tvOrdenante.get_cursor()
                store=self.tvOrdenante.get_model()
                itr=store[Linea[0][0]]
                self.tNif.set_text(itr[0])
                self.tSufijo.set_text(itr[1])
                self.tNombre.set_text(itr[2])
                self.tBanco.set_text(itr[3])
                self.tOficina.set_text(itr[4])
                self.tDc.set_text(itr[5])
                self.tCuenta.set_text(itr[6])
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
        
    def CalculaDC(self,Dato):
        #Dato es el conjunto de BANCO+OFICINA+NUMERO_DE_CUENTA. En total deben de ser 18 caracteres
        #if Dato=="":
        #    return 1
        #else:
        #    pesos=[6,3,7,9,10,5,8,4,2,1]
        #    suma=0
        #    pe=0
        #    for n in range(7 ,-1,-1):
        #        #print "Valor: "+Dato[n:n+1]+" X "+str(pesos[pe])
        #        suma=suma+(int(Dato[n:n+1])*pesos[pe])
        #        pe=pe+1
        #    num=11-(suma%11)
        #    if num==10:
        #        num=1
        #    if num==11:
        #        num=0
        #    D=str(num)
        #    
        #    suma=0
        #    pe=0
        #    for n in range(17 ,8,-1):
        #        #print "Valor: "+Dato[n:n+1]+" X "+str(pesos[pe])
        #        suma=suma+(int(Dato[n:n+1])*pesos[pe])
        #        pe=pe+1
        #    num=11-(suma%11)
        #    if num==10:
        #        num=1
        #    if num==11:
        #        num=0
        #    C=str(num)
        #    DC=D+C
        #    if DC<>self.tDc.get_text():
        #        return DC
        #    else:
        #        return 0
        d1 = Dato[:-10]
        while len(d1) < 10:
            d1 = "0" + d1
        d2 = Dato[-10:]
        DC = str(cccCRC(d1) * 10 + cccCRC(d2))
        if DC<>self.tDc.get_text():
            return DC
        else:
            return 0

    def Ayuda(self,widget):
        pass
        #os.system("./doc/presentador.html")

    def Salir(self,*args):
        #True
        if self.Llamada<>"":
            if self.tNif.get_text()<>"":
                self.CodOrdenante=self.tNif.get_text()+":"+self.tSufijo.get_text()
                self.NomOrdenante=self.tNombre.get_text()
            else:
                self.CodOrdenante=""
                self.NomOrdenante=""
            
            self.ventana.hide()
            return True
        else:
            gtk.main_quit()

    
    def Main(self):
        self.Llamada=""
        gtk.main()
        
if __name__ == "__main__":
    gtk.rc_parse("gtkrc.txt")
    ven = Ordenante()
    ven.Main()
  
    
