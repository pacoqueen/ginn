#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gtk  # @UnusedImport
import gtk.glade
import gobject
import ordenante  # @UnusedImport
import presentador  # @UnusedImport
import sqlite3 as sqlite


class Importar:
    def __init__(self):
        #Estas variables las pasa a otras ventanas
        self.Modificacion=""
        
        glImportar=gtk.glade.XML("./gld/importar.glade")
        self.ventana=glImportar.get_widget("Importar")
        self.ventana.connect("destroy", self.Salir)
        
        self.menu=glImportar.get_widget("Menu")
        self.tNombre=glImportar.get_widget("tNombre")
        
        self.btnFichero=glImportar.get_widget("btnFichero")
        self.btnFichero.connect("clicked", self.SeleccionarFichero)

        self.tvPresentador=glImportar.get_widget("tvPresentador")
        
        self.tvOrdenante=glImportar.get_widget("tvOrdenante")
        
        self.tvRecibos=glImportar.get_widget("tvRecibos")





        self.btnSalir=glImportar.get_widget("btnSalir")
        self.btnSalir.connect("clicked", self.Salir)
        
        self.btnAceptar=glImportar.get_widget("btnAceptar")
        self.btnAceptar.connect("clicked", self.Aceptar)
        
        #pongo las cabeceras del tv del presentador
        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvPresentador.set_model(data)
        
        column = gtk.TreeViewColumn("NIF                   ", gtk.CellRendererText(), text=0)
        self.tvPresentador.append_column(column)
        column = gtk.TreeViewColumn("Sufijo", gtk.CellRendererText(), text=1)
        self.tvPresentador.append_column(column)
        column = gtk.TreeViewColumn("Nombre                                                                                                                                                                            ", gtk.CellRendererText(), text=2)
        self.tvPresentador.append_column(column)
        column = gtk.TreeViewColumn("Banco", gtk.CellRendererText(), text=3)
        self.tvPresentador.append_column(column)
        column = gtk.TreeViewColumn("Oficina", gtk.CellRendererText(), text=4)
        self.tvPresentador.append_column(column)
        
        #Pongo las cabeceras del tv del ordenante

        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvOrdenante.set_model(data)
        
        column = gtk.TreeViewColumn("NIF                   ", gtk.CellRendererText(), text=0)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Sufijo", gtk.CellRendererText(), text=1)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Nombre                                                                                                                                   ", gtk.CellRendererText(), text=2)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Banco", gtk.CellRendererText(), text=3)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Oficina", gtk.CellRendererText(), text=4)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("DC", gtk.CellRendererText(), text=5)
        self.tvOrdenante.append_column(column)
        column = gtk.TreeViewColumn("Cuenta", gtk.CellRendererText(), text=6)
        self.tvOrdenante.append_column(column)


        #Pongo las cabeceras del tv de los recibos

        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvRecibos.set_model(data)
        
        column = gtk.TreeViewColumn("REF.                   ", gtk.CellRendererText(), text=0)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Cliente                                                                                              ", gtk.CellRendererText(), text=1)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Banco", gtk.CellRendererText(), text=2)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Oficina", gtk.CellRendererText(), text=3)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("DC", gtk.CellRendererText(), text=4)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Cuenta", gtk.CellRendererText(), text=5)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Importe   ", gtk.CellRendererText(), text=6)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto1                                                       ", gtk.CellRendererText(), text=7)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto2                                                       ", gtk.CellRendererText(), text=8)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto3                                                       ", gtk.CellRendererText(), text=9)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto4                                                       ", gtk.CellRendererText(), text=10)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto5                                                       ", gtk.CellRendererText(), text=11)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto6                                                       ", gtk.CellRendererText(), text=12)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto7                                                       ", gtk.CellRendererText(), text=13)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto8                                                       ", gtk.CellRendererText(), text=14)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto9                                                       ", gtk.CellRendererText(), text=15)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto10                                                       ", gtk.CellRendererText(), text=16)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto11                                                       ", gtk.CellRendererText(), text=17)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto12                                                       ", gtk.CellRendererText(), text=18)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto13                                                       ", gtk.CellRendererText(), text=19)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto14                                                       ", gtk.CellRendererText(), text=20)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto15                                                       ", gtk.CellRendererText(), text=21)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Concepto16                                                       ", gtk.CellRendererText(), text=22)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Titular                                                       ", gtk.CellRendererText(), text=23)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Domicilio                                                       ", gtk.CellRendererText(), text=24)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Plaza                                    ", gtk.CellRendererText(), text=25)
        self.tvRecibos.append_column(column)
        column = gtk.TreeViewColumn("Cp        ", gtk.CellRendererText(), text=26)
        self.tvRecibos.append_column(column)



    def SeleccionarFichero(self, Widget):
        self.Fiche = gtk.FileSelection("Seleccionar fichero para importar")
        self.Fiche.connect("destroy", self.CerrarAbrirFichero)
        self.Fiche.ok_button.connect("clicked", self.FicheroSeleccionado)
        self.Fiche.cancel_button.connect("clicked", self.CerrarAbrirFichero)
        self.Fiche.set_filename("")
        self.Fiche.set_modal(True)
        self.Fiche.show()
        

    def CerrarAbrirFichero(self, Widget):
        self.Fiche.destroy()

    def FicheroSeleccionado(self, Widget):
        self.tNombre.set_text(self.Fiche.get_filename())
        self.Fiche.destroy()
        self.SacaPresentador()
        self.SacaOrdenante()
        self.SacaRecibos()

    def SacaPresentador(self):
        Datos=[]
        fich = open(self.tNombre.get_text(),"r")
        #Solo leemos la primera linea porque es donde deberia de estar el presentador
        linea=fich.readline()
        
        if linea[0:4]=="5180":
            Datos.append(linea[4:13]) #nif
            Datos.append(linea[13:16]) #Sufijo
            Datos.append(unicode(linea[28:68], 'latin-1').encode('utf-8')) #Nombre
            Datos.append(linea[88:92]) #Banco
            Datos.append(linea[92:96]) #Oficina
        fich.close()
        
        if Datos<>[]:
            store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
            store=self.tvPresentador.get_model()
            itr=store.append()
            store.set(itr,0,Datos[0],1,Datos[1],2,Datos[2],3,Datos[3],4,Datos[4])
            self.tvPresentador.set_model(store)
        else:
            d=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,"El fichero parece no tener presentador, puede que no sea un fichero del cuaderno 19 valido")
            d.connect('response', lambda dialog, response: dialog.destroy())
            d.show()
            
        
    def SacaOrdenante(self):        
        Datos=[]
        fich = open(self.tNombre.get_text(),"r")
        while 1:
            linea=fich.readline()

            if linea[0:4]=="5380":
                Datos.append(linea[4:13]) #nif
                Datos.append(linea[13:16]) #Sufijo
                Datos.append(unicode(linea[28:68], 'latin-1').encode('utf-8')) #Nombre
                Datos.append(linea[68:72]) #Banco
                Datos.append(linea[72:76]) #Oficina
                Datos.append(linea[76:78]) #dc
                Datos.append(linea[78:88]) #cuenta
                
                store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
                store=self.tvOrdenante.get_model()
                itr=store.append()
                store.set(itr,0,Datos[0],1,Datos[1],2,Datos[2],3,Datos[3],4,Datos[4],5,Datos[5],6,Datos[6])
                self.tvOrdenante.set_model(store)
                Datos=[]

            #Mira a ver si se acaba el fichero
            if linea=="":
                break
       
        fich.close()
        
    def SacaRecibos(self):
        fich = open(self.tNombre.get_text(),"r")
        sw=0
        while 1:

            linea=fich.readline()
            if linea[0:4]=="5680":
                data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)  # @UnusedVariable
                store=self.tvRecibos.get_model()
                itr=store.append()
                if sw<>0:
                    self.tvRecibos.set_model(store)
                    sw=0
                
                Datos=[]
                #Los inicializo primero por si no hay datos que los meta igualmente con null
                for n in range (0,27):  # @UnusedVariable
                    Datos.append("")
                    
                sw=1
                Datos[0]=unicode(linea[16:28], 'latin-1').encode('utf-8')       #referencia
                Datos[1]=unicode(linea[28:68], 'latin-1').encode('utf-8')      #nombre
                Datos[2]=linea[68:72]      #banco
                Datos[3]=linea[72:76]      #oficina
                Datos[4]=linea[76:78]      #dc
                Datos[5]=linea[78:88]      #cuenta
                Datos[6]=str(int(linea[88:96]))+","+linea[96:98]      #importe
                Datos[7]=unicode(linea[114:154], 'latin-1').encode('utf-8')      #concepto1
                store.set(itr,0,Datos[0],1,Datos[1],2,Datos[2],3,Datos[3],4,Datos[4],5,Datos[5],6,Datos[6],7,Datos[7])
                    
            elif linea[0:4]=="5681":
                Datos[8]=unicode(linea[28:68], 'latin-1').encode('utf-8')      #concepto2
                Datos[9]=unicode(linea[68:108], 'latin-1').encode('utf-8')      #concepto3
                Datos[10]=unicode(linea[108:148], 'latin-1').encode('utf-8')      #concepto4
                store.set(itr,8,Datos[8],9,Datos[9],10,Datos[10])
            

            elif linea[0:4]=="5682":
                Datos[11]=unicode(linea[28:68], 'latin-1').encode('utf-8')      #concepto5
                Datos[12]=unicode(linea[68:108], 'latin-1').encode('utf-8')      #concepto6
                Datos[13]=unicode(linea[108:148], 'latin-1').encode('utf-8')      #concepto7
                store.set(itr,11,Datos[11],12,Datos[12],13,Datos[13])
            

            elif linea[0:4]=="5683":
                Datos[14]=unicode(linea[28:68], 'latin-1').encode('utf-8')      #concepto8
                Datos[15]=unicode(linea[68:108], 'latin-1').encode('utf-8')      #concepto9
                Datos[16]=unicode(linea[108:148], 'latin-1').encode('utf-8')      #concepto10
                store.set(itr,14,Datos[14],15,Datos[15],16,Datos[16])
                

            elif linea[0:4]=="5684":
                Datos[17]=unicode(linea[28:68], 'latin-1').encode('utf-8')      #concepto11
                Datos[18]=unicode(linea[68:108], 'latin-1').encode('utf-8')      #concepto12
                Datos[19]=unicode(linea[108:148], 'latin-1').encode('utf-8')      #concepto13
                store.set(itr,17,Datos[17],18,Datos[18],19,Datos[19])

            elif linea[0:4]=="5685":
                Datos[20]=unicode(linea[28:68], 'latin-1').encode('utf-8')      #concepto14
                Datos[21]=unicode(linea[68:108], 'latin-1').encode('utf-8')      #concepto15
                Datos[22]=unicode(linea[108:148], 'latin-1').encode('utf-8')      #concepto16
                store.set(itr,20,Datos[20],21,Datos[21],22,Datos[22])

            elif linea[0:4]=="5686":
                Datos[23]=unicode(linea[28:68], 'latin-1').encode('utf-8')      #Titular
                Datos[24]=unicode(linea[68:108], 'latin-1').encode('utf-8')      #Domicilio
                Datos[25]=unicode(linea[108:143], 'latin-1').encode('utf-8')      #plaza
                Datos[26]=unicode(linea[143:148], 'latin-1').encode('utf-8')      #cp
                store.set(itr,23,Datos[23],24,Datos[24],25,Datos[25],26,Datos[26])


            elif linea[0:4]=="5880":
                #Para meter el ultimo recibo
                self.tvRecibos.set_model(store)


            #Mira a ver si se acaba el fichero
            if linea=="":
                break
       
        fich.close()
        

        
    def Aceptar(self,Widget):
        glDialogo=gtk.glade.XML("./gld/dialogo.glade")
        self.Dialogo=glDialogo.get_widget("Dialogo")
        self.Dialogo.connect("destroy", self.DialogoSalir)

        self.DialogobtnSalir=glDialogo.get_widget("btnCancelar")
        self.DialogobtnSalir.connect("clicked", self.DialogoSalir)

        self.DialogobtnAceptar=glDialogo.get_widget("btnAceptar")
        self.DialogobtnAceptar.connect("clicked", self.DialogoAceptar)

        self.DialogoNombre=glDialogo.get_widget("tTexto")
        self.Dialogo.show()

    def DialogoSalir(self,widget):
        self.DialogoNombre.set_text("")
        self.Dialogo.hide()
    
        
    def DialogoAceptar(self,widget):
        presentador=""
        ordenante=""
        CodRem=""
        if self.DialogoNombre.get_text()<>"":
            store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING)
            #Comprobar que la remesa no exista
            self.AbreDb()
            c = self.conexion.cursor()
            #comprobar que este presentador no este dado de alta
            store=self.tvPresentador.get_model()
            sql="select count(titulo) from remesas where titulo='"+self.DialogoNombre.get_text()+"'"
            c.execute(sql)
            sw=0
            if int(c.fetchall()[0][0])<>0:
                self.Mensaje("Ya existe una remesa con este nombre. No se importaran los datos")
                sw=1
            else:
                sql="select count(codigo) from remesas"
                c.execute(sql)
                if c.fetchall()[0][0]<>None:
                    sql="select count(codigo) from remesas"
                    c.execute(sql)
                    CodRem=int(c.fetchall()[0][0])+1
                else:
                    CodRem=1
                
                
            self.CierraDb()
            if sw==0:
        #Importar presentador
                self.AbreDb()
                c = self.conexion.cursor()
                #comprobar que este presentador no este dado de alta
            
                store=self.tvPresentador.get_model()
                store[0][0]=self.CompruebaLongitud(store[0][0],9,"TEXT")         #NIF
                store[0][1]=self.CompruebaLongitud(store[0][1],3,"NUM")         #Sufijo
                store[0][2]=self.CompruebaLongitud(store[0][2],40,"TEXT")         #Nombre
                store[0][3]=self.CompruebaLongitud(store[0][3],4,"NUM")         #Banco
                store[0][4]=self.CompruebaLongitud(store[0][4],4,"NUM")         #Oficina
                
                presentador=store[0][0]+":"+store[0][1]
                sql="select count(nif) from presentadores where nif='"+store[0][0]+"' and sufijo='"+store[0][1]+"'"
                
                c.execute(sql)
                if int(c.fetchall()[0][0])==0:
                    #Se graba el presentador
                    sql="INSERT INTO presentadores (nif, sufijo, nombre, banco, oficina) VALUES ('"+store[0][0]+"','"+store[0][1]+"','"+store[0][2]+"','"+store[0][3]+"','"+store[0][4]+"')"
                    c.execute(sql)
                    self.conexion.commit()   
                self.CierraDb()
            
        #importar ordenante
                self.AbreDb()
                c = self.conexion.cursor()
                #comprobar que este ordenante no este dado de alta
            
                store=self.tvOrdenante.get_model()
                store[0][0]=self.CompruebaLongitud(store[0][0],9,"TEXT")         #NIF
                store[0][1]=self.CompruebaLongitud(store[0][1],3,"NUM")         #Sufijo
                store[0][2]=self.CompruebaLongitud(store[0][2],40,"TEXT")         #Nombre
                store[0][3]=self.CompruebaLongitud(store[0][3],4,"NUM")         #Banco
                store[0][4]=self.CompruebaLongitud(store[0][4],4,"NUM")         #Oficina
                store[0][5]=self.CompruebaLongitud(store[0][5],2,"NUM")         #DC
                store[0][6]=self.CompruebaLongitud(store[0][6],10,"NUM")         #Cuenta
                
                ordenante=store[0][0]+":"+store[0][1]
                sql="select count(nif) from ordenantes where nif='"+store[0][0]+"' and sufijo='"+store[0][1]+"'"
                
                c.execute(sql)
                if int(c.fetchall()[0][0])==0:
                    #Se graba el ordenante
                   
                    sql="INSERT INTO ordenantes (nif, sufijo, nombre, banco, oficina, dc, cuenta) VALUES ('"+store[0][0]+"','"+store[0][1]+"','"+store[0][2]+"','"+store[0][3]+"','"+store[0][4]+"','"+store[0][5]+"','"+store[0][6]+"')"
                    c.execute(sql)
                    self.conexion.commit()
                self.CierraDb()
                
        #importar clientes
                self.AbreDb()
                c = self.conexion.cursor()
                store=self.tvRecibos.get_model()
                
                SumaImporte=0.0
                indice=0
                for n in store:
                    n[0]=self.CompruebaLongitud(n[0],12,"TEXT")         #Codigo
                    n[1]=self.CompruebaLongitud(n[1],40,"TEXT")         #nombre
                    n[24]=self.CompruebaLongitud(n[24],40,"TEXT")       #Direccion
                    n[25]=self.CompruebaLongitud(n[25],35,"TEXT")       #Ciudad
                    n[26]=self.CompruebaLongitud(n[26],5,"NUM")         #cp
                    n[2]=self.CompruebaLongitud(n[2],4,"NUM")           #banco
                    n[2]=self.QuitaCaracteres(n[2])
                    n[3]=self.CompruebaLongitud(n[3],4,"NUM")           #oficina
                    n[3]=self.QuitaCaracteres(n[3])
                    n[4]=self.CompruebaLongitud(n[4],2,"NUM")           #dc
                    if n[4]=="  ":
                        n[4]="**"
                    n[5]=self.CompruebaLongitud(n[5],10,"NUM")          #cuenta
                    n[5]=self.QuitaCaracteres(n[5])
                    
                    nif=n[0][0:10]
                    sql="select count(codigo) from clientes where codigo='"+n[0]+"'"
                    c.execute(sql)
                    if int(c.fetchall()[0][0])==0:
                        sql="INSERT INTO clientes (codigo ,nif , nombre, direccion, ciudad, cp, banco, oficina, dc, cuenta) VALUES ('"+n[0]+"','"+nif+"','"+n[1]+"','"+n[24]+"','"+n[25]+"','"+n[26]+"','"+n[2]+"','"+n[3]+"','"+n[4]+"','"+n[5]+"')"
                        try:
                            c.execute(sql)
                            self.conexion.commit()
                        except:
                            print sql
                        
        #importar recibos
                    importe=float(n[6].split(",")[0]+"."+n[6].split(",")[1])
                    SumaImporte=SumaImporte+importe
                    indice=indice+1
                    conceptos=""
                    for a in range(7,23):
                        n[a]=self.CompruebaLongitud(n[a],40,"TEXT")
                       
                    conceptos=n[7]+"�"+n[8]+"�"+n[9]+"�"+n[10]+"�"+n[11]+"�"+n[12]+"�"+n[13]+"�"+n[14]+"�"+n[15]+"�"+n[16]+"�"+n[17]+"�"+n[18]+"�"+n[19]+"�"+n[20]+"�"+n[21]+"�"+n[22]
                    sql="INSERT INTO det_remesas (codigo, indice, cliente, importe, conceptos) VALUES ("+str(CodRem)+","+str(indice)+",'"+n[0]+"',"+str(importe)+",'"+conceptos+"')"
                    #print sql
                    c.execute(sql)
                    self.conexion.commit()

        #Importar Remesas
                sql="INSERT INTO remesas (codigo, titulo, importe, generada, presentador, ordenante) VALUES ("+str(CodRem)+",'"+self.DialogoNombre.get_text()+"',"+str(SumaImporte)+",'NO','"+presentador+"','"+ordenante+"')"
                #print sql
                c.execute(sql)
                self.conexion.commit()
                
                self.CierraDb()
                
        
                
        self.Dialogo.hide()

    def CambiaCaracter(self,Dato):
        nuev=""
        for a in Dato:
            if a=="'":
                a=" "
            nuev=nuev+a
        return nuev

    def CalculaDC(self,Dato):
        #Dato es el conjunto de BANCO+OFICINA+NUMERO_DE_CUENTA. En total deben de ser 18 caracteres
        if Dato=="":
            return "**"
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
            return DC
                
    def QuitaCaracteres(self,Dato):
        #Comprueba a ver si tiene caracteres no numericos y si es asi los sustituye por 0
        nuevo=""
        if Dato.isdigit()==0:
            for a in Dato:
                if a.isdigit()==0:
                    a="0"
                nuevo=nuevo+a
            #print Dato+"-"+nuevo
            return nuevo
        else:
            return Dato
            


    def CompruebaLongitud(self,Dato,Numero,Tipo):
        if Tipo=="TEXT":
            if Dato==None:
                Dato=self.Espacios(Numero)
            if Dato=="":
                Dato=self.Espacios(Numero)
            if len(Dato)>Numero:
                Dato=Dato[0:Numero]
            if len(Dato)<Numero:
                Dato=Dato.strip()+self.Espacios(Numero-len(Dato.strip()))
            Dato=self.CambiaCaracter(Dato)
        else:
            if Dato=="" or Dato==None:
                Dato=self.Ceros(Numero)
            if len(Dato)>Numero:
                Dato=Dato[0:Numero]
            if len(Dato)<Numero:
                Dato=self.Ceros(Numero-len(Dato))+Dato
        
#        print str(len(Dato))+":"+Dato
        return Dato

    def Ceros(self,Numero):
        d=""
        for n in range(0,Numero):  # @UnusedVariable
            d=d+"0"
        return d

    def Espacios(self,Numero):
        d=""
        for n in range(0,Numero):  # @UnusedVariable
            d=d+" "
        return d

    def Respuesta_Menu(self, Valor):
        self.TpFich=Valor

    def AbreDb(self):
        self.conexion= sqlite.connect(db="./dbCsb19/db", mode=077)  # @UndefinedVariable
        
    def CierraDb(self):
        self.conexion.close()

    def Salir(self,Widget):
        #True
        if self.Llamada<>"":
            if self.Llamada<>"Aceptar":
                self.Llamada="Salir"
            self.ventana.hide()
            return True
        else:
            gtk.main_quit()

    def Main(self):
        self.Llamada=""
        gtk.main()
    
    def Mensaje(self,msg):
        d=gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,msg)
        d.connect('response', lambda dialog, response: dialog.destroy())
        d.show()

if __name__ == "__main__":
    gtk.rc_parse("gtkrc.txt")
    ven = Importar()
    ven.Main()
