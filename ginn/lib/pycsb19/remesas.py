#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gtk  # @UnusedImport
import gtk.glade
import gobject
import recibo
import ordenante
import sqlite3 as sqlite
import time

class Remesas:
    def __init__(self):
        self.Llamada=""
        self.NifOrdenante=""
        self.CodRemesa=""
        self.fecha=""
        glRemesas=gtk.glade.XML("./gld/remesas.glade")
        self.ventana=glRemesas.get_widget("Remesas")
        self.ventana.connect("destroy", self.Salir)
      
        self.tvRecibos=glRemesas.get_widget("tvRecibos")
        self.tvRecibos.connect("button_press_event",self.SacaCampos)
 
        
        self.tNombre=glRemesas.get_widget("tNombre")
        self.tOrdenante=glRemesas.get_widget("tOrdenante")
        self.tImporte=glRemesas.get_widget("tImporte")
        self.fecha=glRemesas.get_widget("tFecha")
        
        self.btnOrdenante=glRemesas.get_widget("btnSeleccionar")
        self.btnOrdenante.connect("clicked", self.SelOrdenante)
        
        
        
        self.btnSalir=glRemesas.get_widget("btnSalir")
        self.btnSalir.connect("clicked", self.Salir)
        
        self.btnAnadir=glRemesas.get_widget("btnAnadir")
        self.btnAnadir.connect("clicked", self.Anadir)


        self.btnEliminar=glRemesas.get_widget("btnEliminar")
        self.btnEliminar.connect("clicked", self.Eliminar)

        self.btnModificar=glRemesas.get_widget("btnModificar")
        self.btnModificar.connect("clicked", self.Modificar)

        self.btnImprimir=glRemesas.get_widget("btnImprimir")
        self.btnImprimir.connect("clicked", self.Imprimir)

        self.btnGenerar=glRemesas.get_widget("btnGenerar")
        self.btnGenerar.connect("clicked", self.Generar)

        self.btnAyuda=glRemesas.get_widget("btnAyuda")
#        self.btnAyuda.connect("clicked", self.Ayuda)


        
        
        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvRecibos.set_model(data)

        column = gtk.TreeViewColumn("Cod    ", gtk.CellRendererText(), text=0)
        self.tvRecibos.append_column(column)
        
        column = gtk.TreeViewColumn("Cliente                                                                                                                                                   ", gtk.CellRendererText(), text=1)
        self.tvRecibos.append_column(column)


        render=gtk.CellRendererText()
        render.set_property('xalign', 1.0)
        column = gtk.TreeViewColumn("Importe", render, text=2)
        self.tvRecibos.append_column(column)
        
    def AbreDb(self):
        self.conexion=sqlite.connect(db="./dbCsb19/db", mode=077)
        
    def CierraDb(self):
        self.conexion.close()

        
    def SacaCampos(self,widget,event):
            if event.type==5:
                self.Modificar(widget)
       
    def MiraRemesa(self,Nombre):
        con=sqlite.connect(db="./dbCsb19/db", mode=077)
        cursor = con.cursor()
                            
        #Mira a ver si ya existe la remesa
        sql="Select count(codigo) from remesas where titulo='"+self.tNombre.get_text()+"'"
        cursor.execute(sql)
        
        if int(cursor.fetchall()[0][0])<>0:
            #no hay ninguno dado de alta
            sql="Select titulo, ordenante, importe, codigo from remesas where titulo='"+Nombre+"'"
            cursor.execute(sql)
            for x in cursor.fetchall():
                item=[]
                for n in x:
                    item.append(n)
        
            # En item[2] esta el importe
        
            self.tImporte.set_text(str(item[2]))
            self.NifOrdenante=item[1]
            self.CodRemesa=str(item[3])
        
            # miramos el nombre del ordenante
            sql="Select nombre from ordenantes where nif='"+item[1].split(":")[0]+"' and sufijo='"+item[1].split(":")[1]+"'"
            cursor.execute(sql)
            self.tOrdenante.set_text(cursor.fetchall()[0][0])
        
            #Mira el detalle
            #Si no hay ningun detalle pasa de mirar mas porque si no da error
            sql="SELECT count(codigo) FROM det_remesas"
            cursor.execute(sql)
            if int(cursor.fetchall()[0][0])<>0:            
                sql="SELECT det_remesas.indice, clientes.nombre, det_remesas.importe FROM det_remesas,clientes WHERE clientes.codigo=det_remesas.cliente AND det_remesas.codigo='"+self.CodRemesa+"'"
                cursor.execute(sql)
                for x in cursor.fetchall():
                    item=[]
                    numero=0
                    for n in x:
                        numero=numero+1
                        if numero==3:
                            #Todo este rollo es para completar el importe con dos decimales en el treeview
                            cadena=str(n)
                            if cadena.find(".")==-1:
                                cadena=cadena+".00"
                            elif (len(cadena)-1)-cadena.find(".")<2:
                                cadena=cadena+"0"
                            item.append(cadena)
                        else:
                            item.append(n)
                
                    self.VisualizaDatos(item)
        
        con.close()
        

    def Eliminar(self, widget):
        if self.tvRecibos.get_selection().get_selected()[1]<>None:
            store=self.tvRecibos.get_model()
            
            self.AbreDb()
            c = self.conexion.cursor()

            #Borramos el recibo
            sql="delete from det_remesas where codigo="+self.CodRemesa+" and indice="+store[self.tvRecibos.get_cursor()[0][0]][0]
            c.execute(sql)
            self.conexion.commit()
            
            #Miramos a ver cuanto es el importe de la remesa ahora
            sql="Select sum(importe) from det_remesas where codigo='"+self.CodRemesa+"'"
            c.execute(sql)
            Importe=0.0
            Importe=float(c.fetchall()[0][0])
            
            #Mete el importe en la casilla del importe
            self.tImporte.set_text(str(Importe))
                    
            
            
            #Actualiza el importe en la base de datos de remesa
            sql="UPDATE remesas SET importe="+str(Importe)+" WHERE codigo="+self.CodRemesa
            c.execute(sql)
            self.conexion.commit()
            self.CierraDb()
            
            store.remove(self.tvRecibos.get_selection().get_selected()[1])
            self.tvRecibos.set_model(store)
        else:
            d=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,"Debe de seleccionar una recibo para poder eliminarlo")
            d.connect('response', lambda dialog, response: dialog.destroy())
            d.show()

        

    def MiraOrdenante(self):
        if self.Otro.CodOrdenante<>"x":
            if self.Otro.CodOrdenante<>"":
                self.tOrdenante.set_text(self.Otro.NomOrdenante)
                self.NifOrdenante=self.Otro.CodOrdenante
                
                self.AbreDb()
                cursor = self.conexion.cursor()
                
                #Hay que mirar a ver si es la primera remesa de la base de datos
                sql="Select count(codigo) from remesas"
                cursor.execute(sql)
                if int(cursor.fetchall()[0][0])==0:
                    #Es la primera remesa asin que el codigo es = 1 y solo hay que darla de alta

                    codigo="1"
                    self.CodRemesa=codigo
                    sql="insert into remesas(codigo, titulo, ordenante, generada, importe) values("+codigo+",'" +self.tNombre.get_text()+"','"+self.NifOrdenante+"','NO',0)"
                    cursor.execute(sql)
                    self.conexion.commit()
                else:
                    #Mira a ver si ya existe la remesa por si es una modificacion del ordenante
                    sql="Select count(codigo) from remesas where titulo='"+self.tNombre.get_text()+"'"
                    cursor.execute(sql)
                
                    if int(cursor.fetchall()[0][0])==0:
                        #"no hay ninguno dado de alta"
                        # "Ahora miramos a ver cual es el ultimo codigo dado de alta y le sumamos 1"
                        sql="Select max(codigo) from remesas"
                        cursor.execute(sql)
                        codigo=str(int(cursor.fetchall()[0][0])+1)
                        
                        self.CodRemesa=codigo

                        #Ahora la damos de alta
                        sql="insert into remesas(codigo, titulo, ordenante, generada, importe) values("+codigo+",'" +self.tNombre.get_text()+"','"+self.NifOrdenante+"','NO',0)"
                        cursor.execute(sql)
                        self.conexion.commit()

                    else:
                        # "ya esta dado de alta, Hay que hace un Update Tabla"
                        sql="Select codigo from remesas where titulo='"+self.tNombre.get_text()+"'"
                        cursor.execute(sql)
                        codigo=str(cursor.fetchall()[0][0])
                        self.CodRemesa=codigo
                        sql="UPDATE remesas SET titulo='" +self.tNombre.get_text()+"', ordenante='"+self.NifOrdenante+"' WHERE codigo="+codigo
                        cursor.execute(sql)
                        self.conexion.commit()
                        
                self.CierraDb()

            return 0
        else:
            return 1

    def VisualizaDatos(self,Datos):
        store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)  # @UnusedVariable
        store=self.tvRecibos.get_model()
        itr=store.append()
        store.set(itr,0,Datos[0],1,Datos[1],2,Datos[2])
        self.tvRecibos.set_model(store)
        
    def MiraRecibos(self):
        #Aqui se graban los recibos que devuelve la pantalla de recibos
        if self.VenRecibos.Llamada<>"remesas":
           
            if self.VenRecibos.Llamada<>"Salir":
                #Saca el codigo de la remesa en el improbable caso de que no exista
                if self.CodRemesa=="":
                    self.AbreDb()
                    cursor = self.conexion.cursor()
                    sql="Select codigo from remesas where titulo='"+self.tNombre.get_text()+"'"
                    cursor.execute(sql)
                    self.CodRemesa=str(cursor.fetchall()[0][0])
                    self.CierraDb()

                
                #lo primero es saber si es una modificacion de un recibo
                if self.VenRecibos.Modificacion<>"":
                    #Es una modificacion

                    self.AbreDb()
                    cursor = self.conexion.cursor()
                    
                    indice=self.VenRecibos.Modificacion
                    #Modificamos los datos del recibo
                    #sql="Update det_remesas SET cliente=?, importe=?, conceptos=? WHERE codigo='"+self.CodRemesa+"' AND indice='"+indice+"'"
                    #cursor.execute(sql, (self.VenRecibos.CodCliente,float(self.VenRecibos.Importe),self.VenRecibos.Conceptos))
                    
                    sql="Update det_remesas SET cliente='"+self.VenRecibos.CodCliente+"', importe="+self.VenRecibos.Importe+", conceptos='"+self.VenRecibos.Conceptos+"' WHERE codigo="+self.CodRemesa+" AND indice="+indice
                    cursor.execute(sql)
                    self.conexion.commit()


                    cursor = self.conexion.cursor()
                    #Miramos a ver cuanto es el importe de la remesa ahora
                    sql="Select sum(importe) from det_remesas where codigo="+self.CodRemesa
                    cursor.execute(sql)
                    
                    Importe=float(cursor.fetchall()[0][0])
                    
                    #Mete el importe en la casilla del importe
                    self.tImporte.set_text(str(Importe))
                    
                    cursor = self.conexion.cursor()
                    #Actualiza el importe en la base de datos de remesa
                    sql="UPDATE remesas SET importe="+str(Importe)+" WHERE codigo="+self.CodRemesa
                    cursor.execute(sql)
                    #sql="UPDATE remesas SET importe=? WHERE codigo=?"
                    #cursor.execute(sql,(Importe,self.CodRemesa))
                    self.conexion.commit()
                    
                    #Carga los datos en el treeview
                    store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
                    self.tvRecibos.set_model(store)
                    self.MiraRemesa(self.tNombre.get_text())
                    self.CierraDb()

                    
                else:
                    #Es un recibo nuevo
                    self.AbreDb()
                    cursor = self.conexion.cursor()
                    #miramos a ver si es el primer recibo de esta remesa (si el importe es 0)
                    sql="SELECT sum(importe) FROM remesas WHERE codigo="+self.CodRemesa
                    cursor.execute(sql)
                    if float(cursor.fetchall()[0][0])==0:
                        #Es el primero asin que le ponemos el numero 1
                        indice=1
                    else:
                        #No es el primero
                        #Miramos a ver el codigo que le corresponde a este recibo
                        sql="SELECT max(indice) FROM det_remesas WHERE codigo='"+self.CodRemesa+"'"
                        cursor.execute(sql)
                        indice=str(int(cursor.fetchall()[0][0])+1)
                    
                    #A�adimos los datos del recibo
                    #sql="insert into det_remesas (codigo,indice, cliente, importe, conceptos) values (?,?,?,?,?)"
                    #cursor.execute(sql, (str(self.CodRemesa),indice , self.VenRecibos.CodCliente, str(self.VenRecibos.Importe), self.VenRecibos.Conceptos))
                    sql="insert into det_remesas (codigo, indice, cliente, importe, conceptos) values ("+str(self.CodRemesa)+","+str(indice)+",'"+self.VenRecibos.CodCliente+"',"+str(self.VenRecibos.Importe)+",'"+self.VenRecibos.Conceptos+"')"
                    cursor.execute(sql)
                    self.conexion.commit()
                    
                    sql="SELECT sum(importe) FROM det_remesas WHERE codigo='"+self.CodRemesa+"'"
                    cursor.execute(sql)
                    Importe = float(cursor.fetchall()[0][0])
                    self.tImporte.set_text(str(Importe))
 
                    #Actualiza el importe en la base de datos de remesa
                    sql="UPDATE remesas SET importe="+str(Importe)+" WHERE codigo='"+self.CodRemesa+"'"
                    cursor.execute(sql)
                    self.conexion.commit()                
                    
                    #Mete los datos del recibo en el TreeView
                    store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
                    self.tvRecibos.set_model(store)
                    self.MiraRemesa(self.tNombre.get_text())
                    self.CierraDb()
                
            else:
                pass
            #   print "salio por aqui"
            return 0
        else:
            #print "no Es distinto"
            return 1

    def SelOrdenante(self,widget):
        #Se llama a la pantalla del ordenante
        self.Otro=ordenante.Ordenante()
        self.Otro.Llamada="remesas"
        #self.Otro.ventana.set_modal(True)
        self.Otro.CodOrdenante="x"
        self.timeout= gtk.timeout_add(250, self.MiraOrdenante)

    def Anadir(self,widget):
        if self.tNombre.get_text()=="":
            self.Dialogo("No se puede anadir un recibo si no se le ha dado un nombre a la remesa",2)
        elif self.tOrdenante.get_text()=="":
            self.Dialogo("No se puede anadir un recibo si no se ha selecionado el ordenante",2)
        else:
            self.VenRecibos=recibo.Recibo()
            self.VenRecibos.Llamada="remesas"
            self.VenRecibos.Modificacion=""
            self.VenRecibos.Remesa=self.tNombre.get_text()
            #self.VenRecibos.ventana.set_modal(True)
            self.timeout= gtk.timeout_add(250, self.MiraRecibos)
            
            
            
    def Modificar(self,widget):
        store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING)  # @UnusedVariable
        store=self.tvRecibos.get_model()
        if self.tvRecibos.get_cursor()[0]<>None:
            self.VenRecibos=recibo.Recibo()
            self.VenRecibos.Llamada="remesas"
            
            #Mete el numero de recibo de la remesa
            self.VenRecibos.Modificacion=store[self.tvRecibos.get_cursor()[0][0]][0]
            
            self.AbreDb()
            cClientes = self.conexion.cursor()
            sql="SELECT codigo, nombre, banco, oficina, dc, cuenta FROM clientes WHERE nombre='"+store[self.tvRecibos.get_cursor()[0][0]][1]+"'"
            cClientes.execute(sql)
            pp=[]
            pp=cClientes.fetchone()
                
            CodCliente=pp[0]
            self.VenRecibos.tCodCliente.set_text(CodCliente)
            self.VenRecibos.tNomCliente.set_text(pp[1])
            self.VenRecibos.tBanco.set_text(pp[2])
            self.VenRecibos.tOficina.set_text(pp[3])
            self.VenRecibos.tDc.set_text(pp[4])
            self.VenRecibos.tCuenta.set_text(pp[5])
            self.VenRecibos.tImporte.set_text(store[self.tvRecibos.get_cursor()[0][0]][2])
            
            cDetalle = self.conexion.cursor()
            sql="SELECT codigo, cliente, importe, conceptos FROM det_remesas WHERE codigo="+self.CodRemesa+" AND indice="+store[self.tvRecibos.get_cursor()[0][0]][0]
            cDetalle.execute(sql)
            n=cDetalle.fetchone()[3].split("�")
            self.VenRecibos.tConcepto1.set_text(n[0])
            self.VenRecibos.tConcepto2.set_text(n[1])
            self.VenRecibos.tConcepto3.set_text(n[2])
            self.VenRecibos.tConcepto4.set_text(n[3])
            self.VenRecibos.tConcepto5.set_text(n[4])
            self.VenRecibos.tConcepto6.set_text(n[5])
            self.VenRecibos.tConcepto7.set_text(n[6])
            self.VenRecibos.tConcepto8.set_text(n[7])
            self.VenRecibos.tConcepto9.set_text(n[8])
            self.VenRecibos.tConcepto10.set_text(n[9])
            self.VenRecibos.tConcepto11.set_text(n[10])
            self.VenRecibos.tConcepto12.set_text(n[11])
            self.VenRecibos.tConcepto13.set_text(n[12])
            self.VenRecibos.tConcepto14.set_text(n[13])
            self.VenRecibos.tConcepto15.set_text(n[14])
            self.VenRecibos.tConcepto16.set_text(n[15])

            self.VenRecibos.Remesa=self.tNombre.get_text()
            #self.VenRecibos.ventana.set_modal(True)
            self.timeout= gtk.timeout_add(250, self.MiraRecibos)
            self.CierraDb()
        else:
            d=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,"Debe de seleccionar un recibo para poder abrirlo")
            d.connect('response', lambda dialog, response: dialog.destroy())
            d.show()


    def Imprimir(self,widget):
        pass
        
    def Espacios(self,Numero):
        d=""
        for n in range(0,Numero):  # @UnusedVariable
            d=d+" "
        return d

    def Ceros(self,Numero):
        d=""
        for n in range(0,Numero):  # @UnusedVariable
            d=d+"0"
        return d

    def Generar(self,widget):
        self.Fiche = gtk.FileSelection("Seleccionar Fichero")
        self.Fiche.connect("destroy", self.CerrarAbrirFichero)
        self.Fiche.ok_button.connect("clicked", self.FicheroSeleccionado)
        self.Fiche.cancel_button.connect("clicked", self.CerrarAbrirFichero)
        self.Fiche.set_filename("")
        self.Fiche.set_modal(True)
        self.Fiche.show()
       
    def CerrarAbrirFichero(self,widget):
        self.Fiche.destroy()

    def FicheroSeleccionado(self, widget):
        #Cerramos la ventana de seleccionar fichero
        if self.Fiche.get_filename()[len(self.Fiche.get_filename())-1:len(self.Fiche.get_filename())]<>'\\':
            self.GrabaCSB(self.Fiche.get_filename())
        else:
            d=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,"Debe de introducir el nombre de un fichero para poder grabarlo")
            d.connect('response', lambda dialog, response: dialog.destroy())
            d.show()

        self.Fiche.destroy()

    def GrabaCSB(self,Fichero):
        #Aqui se crea el fichero con el formato CSB19
        self.AbreDb()
        f=open(Fichero,"w")

        #Cabecera de presentador
        cur=self.conexion.cursor()
        sql="SELECT ordenante FROM remesas WHERE codigo="+self.CodRemesa
        cur.execute(sql)
        ordenante=cur.fetchall()[0][0]
        
        rem=self.conexion.cursor()
        sql="SELECT nif, sufijo, nombre, banco, oficina, dc, cuenta FROM ordenantes WHERE nif='"+ordenante.split(":")[0]+"' and sufijo='"+ordenante.split(":")[1]+"'"
        rem.execute(sql)
        Linea=rem.fetchall()[0]
        nif=Linea[0]
        sufijo=Linea[1]
        nombre=Linea[2]
        banco=Linea[3]
        oficina=Linea[4]
        dc=Linea[5]
        cuenta=Linea[6]
        #a�o, mes, dia
        dia=str(time.localtime()[2])
        if len(dia)<2:
            dia="0"+dia
        mes=str(time.localtime()[1])
        if len(mes)<2:
            mes="0"+mes
        ano=str(time.localtime()[0])[2:4]
        FechaConfeccion=dia+mes+ano
        #FechaCargo=FechaConfeccion
        FechaCargo=self.fecha.get_text()
        #Cambiar la FechaCargo por el valor del texto (casi nada...)
        
        if len(nombre)<40:
            nombre=nombre+self.Espacios(40-len(nombre))
        Cadena="5180"+nif+sufijo+FechaConfeccion+self.Espacios(6)+nombre+self.Espacios(20)+banco+oficina+self.Espacios(12)+self.Espacios(40)+"***PyCsb19****"+"\r\n"
        f.write(Cadena)
        
        #Cabecera de Ordenante
        Cadena="5380"+nif+sufijo+FechaConfeccion+FechaCargo+nombre+banco+oficina+dc+cuenta+self.Espacios(8)+"01"+self.Espacios(10)+self.Espacios(40)+"***PyCsb19****"+"\r\n"
        f.write(Cadena)
        
        #Registros de recibos
        rec=self.conexion.cursor()
        sql="SELECT indice, cliente, importe, conceptos FROM det_remesas WHERE codigo="+self.CodRemesa
        rec.execute(sql)
        nNumDomiciliaciones=0
        nSuma=0.0
        nNumRegistrosOrdenante=2 #Se pone con dos porque el fichero ya tiene las 2 cabeceras escritas
        for remesa in rec.fetchall():
            #El indice lo voy a utilizar para el codigo de devolucion
            Indice=str(remesa[0])
            nNumDomiciliaciones=nNumDomiciliaciones+1

            if len(Indice)<6:
                Indice=Indice+self.Espacios(6-len(Indice))
            elif len(Indice)>6:
                Indice=Indice[0:5]
            
            
            Cliente=remesa[1]
            nSuma=nSuma+remesa[2]

            Importe=str(remesa[2])
            if Importe.find(".")==-1:
                Importe=Importe+self.Ceros(2)
            else:
                if len(Importe.split(".")[1])<2:
                    Importe=Importe.split(".")[0]+Importe.split(".")[1]+self.Ceros(2-len(Importe.split(".")[1]))
                elif len(Importe.split(".")[1])>2:
                    Importe=Importe.split(".")[0]+Importe.split(".")[1][0:1]
                else:
                    Importe=Importe.split(".")[0]+Importe.split(".")[1]
                    
            if len(Importe)<10:
                Importe=self.Ceros(10-len(Importe))+Importe

            Conceptos=[]
            for n in remesa[3].split("�"):
                if len(n)==0:
                    dato=""
                elif len(n)<40:
                    dato=n+self.Espacios(40-len(n))
                elif len(n)>40:
                    dato=n[0:40]
                else:
                    dato=n
                Conceptos.append(dato)

            
            #Vamos a por los datos del cliente
            cli=self.conexion.cursor()
            sql="SELECT codigo, nif, nombre, direccion, ciudad, cp, banco, oficina, dc, cuenta FROM clientes WHERE codigo='"+Cliente+"'"
            cli.execute(sql)
            c=cli.fetchall()[0]
            if len(c[0])<12:
                CodCliente=c[0]+self.Espacios(12-len(c[0]))
            else:
                CodCliente=c[0]
            #El nif lo voy a utilizar para el codigo de referencia interna
            NifCliente=c[1]
            if len(NifCliente)<10:
                NifCliente=NifCliente+self.Espacios(10-len(NifCliente))
            if len(c[2])<40:
                NombreCliente=c[2]+self.Espacios(40-len(c[2]))
            else:
                NombreCliente=c[2]

            DireCliente=c[3]  # @UnusedVariable
            CiudadCliente=c[4]  # @UnusedVariable
            CpCliente=c[5]  # @UnusedVariable
            BancoCliente=c[6]
            OficinaCliente=c[7]
            DcCliente=c[8]
            CuentaCliente=c[9]
            
            if len(Conceptos[0])<40:
                Conceptos[0]=Conceptos[0]+self.Espacios(40-len(Conceptos[0]))
            if len(Conceptos[0])>40:
                Conceptos[0]=Conceptos[0][0:40]
            
            Cadena="5680"+nif+sufijo+CodCliente+NombreCliente+BancoCliente+OficinaCliente+DcCliente+CuentaCliente+Importe+Indice+NifCliente+Conceptos[0]+self.Espacios(8)+"\r\n"
            f.write(Cadena)
            nNumRegistrosOrdenante=nNumRegistrosOrdenante+1

            #Vamos a ver que pasa con los otros conceptos.
            
            if len(Conceptos[1])<>0 or len(Conceptos[2])<>0 or len(Conceptos[3])<>0:
                if len(Conceptos[1])<>40:
                    Conceptos[1]=Conceptos[1]+self.Espacios(40-len(Conceptos[1]))
                if len(Conceptos[2])<>40:
                    Conceptos[2]=Conceptos[2]+self.Espacios(40-len(Conceptos[2]))
                if len(Conceptos[3])<>40:
                    Conceptos[3]=Conceptos[3]+self.Espacios(40-len(Conceptos[3]))
                Cadena="5681"+nif+sufijo+CodCliente+Conceptos[1]+Conceptos[2]+Conceptos[3]+self.Espacios(14)+"\r\n"
                f.write(Cadena)
                nNumRegistrosOrdenante=nNumRegistrosOrdenante+1

            if len(Conceptos[4])<>0 or len(Conceptos[5])<>0 or len(Conceptos[6])<>0:
                if len(Conceptos[4])<>40:
                    Conceptos[4]=Conceptos[4]+self.Espacios(40-len(Conceptos[4]))
                if len(Conceptos[5])<>40:
                    Conceptos[5]=Conceptos[5]+self.Espacios(40-len(Conceptos[5]))
                if len(Conceptos[6])<>40:
                    Conceptos[6]=Conceptos[6]+self.Espacios(40-len(Conceptos[6]))
                Cadena="5682"+nif+sufijo+CodCliente+Conceptos[4]+Conceptos[5]+Conceptos[6]+self.Espacios(14)+"\r\n"
                f.write(Cadena)
                nNumRegistrosOrdenante=nNumRegistrosOrdenante+1

            if len(Conceptos[7])<>0 or len(Conceptos[8])<>0 or len(Conceptos[9])<>0:
                if len(Conceptos[7])<>40:
                    Conceptos[7]=Conceptos[7]+self.Espacios(40-len(Conceptos[7]))
                if len(Conceptos[8])<>40:
                    Conceptos[8]=Conceptos[8]+self.Espacios(40-len(Conceptos[8]))
                if len(Conceptos[9])<>40:
                    Conceptos[9]=Conceptos[9]+self.Espacios(40-len(Conceptos[9]))                    
                Cadena="5683"+nif+sufijo+CodCliente+Conceptos[7]+Conceptos[8]+Conceptos[9]+self.Espacios(14)+"\r\n"
                f.write(Cadena)
                nNumRegistrosOrdenante=nNumRegistrosOrdenante+1

            if len(Conceptos[10])<>0 or len(Conceptos[11])<>0 or len(Conceptos[12])<>0:
                if len(Conceptos[10])<>40:
                    Conceptos[10]=Conceptos[10]+self.Espacios(40-len(Conceptos[10]))
                if len(Conceptos[11])<>40:
                    Conceptos[11]=Conceptos[11]+self.Espacios(40-len(Conceptos[11]))
                if len(Conceptos[12])<>40:
                    Conceptos[12]=Conceptos[12]+self.Espacios(40-len(Conceptos[12]))
                Cadena="5684"+nif+sufijo+CodCliente+Conceptos[10]+Conceptos[11]+Conceptos[12]+self.Espacios(14)+"\r\n"
                f.write(Cadena)
                nNumRegistrosOrdenante=nNumRegistrosOrdenante+1

            if len(Conceptos[13])<>0 or len(Conceptos[14])<>0 or len(Conceptos[15])<>0:
                if len(Conceptos[13])<>40:
                    Conceptos[13]=Conceptos[13]+self.Espacios(40-len(Conceptos[13]))
                if len(Conceptos[14])<>40:
                    Conceptos[14]=Conceptos[14]+self.Espacios(40-len(Conceptos[14]))
                if len(Conceptos[15])<>40:
                    Conceptos[15]=Conceptos[15]+self.Espacios(40-len(Conceptos[15]))
                Cadena="5685"+nif+sufijo+CodCliente+Conceptos[13]+Conceptos[14]+Conceptos[15]+self.Espacios(14)+"\r\n"
                f.write(Cadena)
                nNumRegistrosOrdenante=nNumRegistrosOrdenante+1
    
    
        #La linea de datos del cliente no se implementa de monento
        #Cadena="5686"+nif+sufijo+CodCliente
        
        
        #Linea de totales de ordenante
        Suma=str(nSuma)

        if Suma.find(".")==-1:
            Suma=Suma+self.Ceros(2)
        else:
            if len(Suma.split(".")[1])<2:
                Suma=Suma.split(".")[0]+Suma.split(".")[1]+self.Ceros(2-len(Suma.split(".")[1]))
            elif len(Suma.split(".")[1])>2:
                Suma=Suma.split(".")[0]+Suma.split(".")[1][0:1]
            else:
                Suma=Suma.split(".")[0]+Suma.split(".")[1]
        if len(Suma)<10:
            Suma=self.Ceros(10-len(Suma))+Suma
        
        
        NumDomiciliaciones=str(nNumDomiciliaciones)
        if len(NumDomiciliaciones)<10:
            NumDomiciliaciones=self.Ceros(10-len(NumDomiciliaciones))+NumDomiciliaciones
    
        NumRegistrosOrdenante=str(nNumRegistrosOrdenante)
        if len(NumRegistrosOrdenante)<10:
            NumRegistrosOrdenante=self.Ceros(10-len(NumRegistrosOrdenante))+NumRegistrosOrdenante

        Cadena="5880"+nif+sufijo+self.Espacios(12)+self.Espacios(40)+self.Espacios(20)+Suma+self.Espacios(6)+NumDomiciliaciones+NumRegistrosOrdenante+self.Espacios(20)+"*****PyCsb19******"+"\r\n"
        f.write(Cadena)
        nNumRegistrosOrdenante=nNumRegistrosOrdenante+1
        

        NumRegistrosOrdenante=str(nNumRegistrosOrdenante+1)
        if len(NumRegistrosOrdenante)<10:
            NumRegistrosOrdenante=self.Ceros(10-len(NumRegistrosOrdenante))+NumRegistrosOrdenante

        #Linea de total general
        Cadena="5980"+nif+sufijo+self.Espacios(12)+self.Espacios(40)+"0001"+self.Espacios(16)+Suma+self.Espacios(6)+NumDomiciliaciones+NumRegistrosOrdenante+self.Espacios(20)+"*****PyCsb19******"+"\r\n"
        f.write(Cadena)
            
        f.close()
        self.CierraDb()
        self.Dialogo("El fichero se ha generado correctamente",1)


    def Dialogo(self, msg, Tipo):
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
            
    def Salir(self,*args):
        #True
        if self.Llamada<>"":
            self.ventana.hide()
            self.Cliente=""
            self.Importe=""
            self.Llamada=""
            return True
        else:
            gtk.main_quit()

    def Main(self):
        self.Llamada=""
        gtk.main()
        
if __name__ == "__main__":
    gtk.rc_parse("gtkrc.txt")
    ven = Remesas()
    ven.Main()

    
