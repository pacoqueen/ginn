#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import gtk
import gtk.glade
import gobject

class Devoluciones:
    def __init__(self):
        #Esta variable nos va a decir si esta ventana se abre por si sola o la llamo otra ventana
        self.Llamada=""
        self.Fichero=""
        self.NifSufijo=""
        
        glDevoluciones = gtk.glade.XML("./devoluciones.glade")
        self.ventana=glDevoluciones.get_widget("Devoluciones")
        self.ventana.connect("destroy", self.Salir)
        self.ventana.connect("delete_event",self.Salir)

        self.tvOrdenantes=glDevoluciones.get_widget("tvOrdenantes")
        self.tvOrdenantes.connect("button_press_event",self.SacaCampos)

        self.tvDevoluciones=glDevoluciones.get_widget("tvDevoluciones")
        #self.tvDevoluciones.connect("button_press_event",self.SacaCampos)

        self.btnSalir=glDevoluciones.get_widget("btnSalir")
        self.btnSalir.connect("clicked", self.Salir)

        self.btnAbrir=glDevoluciones.get_widget("btnAbrir")
        self.btnAbrir.connect("clicked", self.SeleccionarFichero)

        self.btnImprimir=glDevoluciones.get_widget("btnImprimir")
        self.btnImprimir.connect("clicked", self.Imprimir)

        self.btnImprimirTodo=glDevoluciones.get_widget("btnImprimirTodo")
        self.btnImprimirTodo.connect("clicked", self.ImprimirTodo)

        self.btnAcercade=glDevoluciones.get_widget("btnAcercade")
        self.btnAcercade.connect("clicked", self.Acercade)

        self.tPresentador=glDevoluciones.get_widget("tPresentador")
        
        
        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvOrdenantes.set_model(data)
        
        column = gtk.TreeViewColumn("NIF                    ", gtk.CellRendererText(), text=0)
        self.tvOrdenantes.append_column(column)
        column = gtk.TreeViewColumn("Sufijo  ", gtk.CellRendererText(), text=1)
        self.tvOrdenantes.append_column(column)
        column = gtk.TreeViewColumn("Ordenante                                                                                  ", gtk.CellRendererText(), text=2)
        self.tvOrdenantes.append_column(column)



        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvDevoluciones.set_model(data)
        
        column = gtk.TreeViewColumn("Nombre                                                                ", gtk.CellRendererText(), text=0)
        self.tvDevoluciones.append_column(column)
        column = gtk.TreeViewColumn("CCC                                ", gtk.CellRendererText(), text=1)
        self.tvDevoluciones.append_column(column)
        render=gtk.CellRendererText()
        render.set_property('xalign', 1.0)
        column = gtk.TreeViewColumn("Importe       ", render, text=2)
        self.tvDevoluciones.append_column(column)
        column = gtk.TreeViewColumn("Motivo                                                      ", gtk.CellRendererText(), text=3)
        self.tvDevoluciones.append_column(column)

        
    def VisualizaDatosOrdenantes(self,Datos):
        store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        store=self.tvOrdenantes.get_model()
        iter=store.append()
        store.set(iter,0,Datos[0],1,Datos[1],2,Datos[2])
        self.tvOrdenantes.set_model(store)

    def VisualizaDatosDevoluciones(self,Datos):
        store=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        store=self.tvDevoluciones.get_model()
        iter=store.append()
        store.set(iter,0,Datos[0],1,Datos[1],2,Datos[2],3,Datos[3])
        self.tvDevoluciones.set_model(store)

    def SeleccionarFichero(self, Widget):
        self.Fiche = gtk.FileSelection("Seleccionar fichero de devoluciones")
        self.Fiche.connect("destroy", self.Cerrar_AbrirFichero)
        self.Fiche.ok_button.connect("clicked", self.FicheroSeleccionado)
        self.Fiche.cancel_button.connect("clicked", self.Cerrar_AbrirFichero)
        self.Fiche.set_filename("")
        self.Fiche.set_modal(True)
        self.Fiche.show()
        

    def Cerrar_AbrirFichero(self, Widget):
        self.Fiche.destroy()

    def FicheroSeleccionado(self, Widget):
        self.Fichero=self.Fiche.get_filename()
        self.Fiche.destroy()
        
        #Limpio los datos de los treeview
        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvOrdenantes.set_model(data)
        data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
        data.clear()
        self.tvDevoluciones.set_model(data)
        
        if self.Fichero<>"":
            f=open(self.Fichero)
            while 1:
                linea=f.readline()
                if linea=="":
                    break
                else:
                    if linea[0:4]=="5190": #Presentador
                        self.tPresentador.set_text(linea[28:68])
                    
                    if linea[0:4]=="5390": #Ordenante
                        pp=[]
                        pp.append(linea[4:13])
                        pp.append(linea[13:16])
                        pp.append(linea[28:68])
                        self.VisualizaDatosOrdenantes(pp)
                        
            f.close()
        
        self.Fiche.destroy()



                
    def SacaCampos(self, widget, event):
        #El 5 es doble click y el 4 es el simple
        self.NifSufijo=""
        if event.type==5:
            try:
                Linea=self.tvOrdenantes.get_cursor()
                store=self.tvOrdenantes.get_model()
                iter=store[Linea[0][0]]
                self.NifSufijo=iter[0]+iter[1]
                data=gtk.ListStore(gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING)
                data.clear()
                self.tvDevoluciones.set_model(data)
            except:
                pass
        
        if self.Fichero<>"" and self.NifSufijo<>"":
            f=open(self.Fichero)
            while 1:
                linea=f.readline()
                if linea=="":
                    break
                else:
                    #Mirar a ver si es el ordenante que buscamos
                    #if linea[0:4]=="5390" and self.NifSufijo==linea[4:16]:
                        #Leemos la siguiente linea que deberia ser un 5690
                    #    linea=f.readline()
                    if linea[0:4]=="5690" and self.NifSufijo==linea[4:16]:
                            pp=[]
                            pp.append(linea[28:68])
                            pp.append(linea[68:72]+" "+linea[72:76]+" "+linea[76:78]+" "+linea[78:88])
                            pp.append(str(int(linea[88:96]))+","+linea[96:98])
                            motivo=""
                            if linea[154:155]=="0":
                                motivo="Importe a 0"
                            elif linea[154:155]=="1":
                                motivo="Incorriente"
                            elif linea[154:155]=="2":
                                motivo="No domiciliado o cuenta cancelada"
                            elif linea[154:155]=="3":
                                motivo="Oficina domiciliadora inexistente"
                            elif linea[154:155]=="4":
                                motivo="Aplicacion R.D. 338/90 sobre el NIF"
                            elif linea[154:155]=="5":
                                motivo="Por orden del cliente: error o baja en la domiciliacion"
                            elif linea[154:155]=="6":
                                motivo="Por orden del cliente: disconformidad con el importe"
                            elif linea[154:155]=="7":
                                motivo="Adeudo duplicado, indebido, erroneo o faltan datos"
                            elif linea[154:155]=="8":
                                motivo="Sin determinar"
                            else:
                                motivo="Sin determinar"

                            pp.append(motivo)
                            self.VisualizaDatosDevoluciones(pp)
                        
                        
            f.close()

    def ImprimirTodo(self, Widget):
        if self.Fichero<>"":
            html=open(self.Fichero+".html","w")
            
            #Cabecera del fichero
            html.write("<HTML>\n")
            html.write("<HEAD>\n")
            html.write("<TITLE>"+self.tPresentador.get_text()+"</TITLE>\n")
            html.write("<META HTTP-EQUIV='Content-Type' CONTENT='text/html; charset=iso-8859-1'>\n")
            html.write("<style type='text/css'>\n")
            html.write("<!-- \n")
            html.write(".cabtabla {\n")
            html.write("	font-family: Verdana, Arial, Helvetica, sans-serif;\n")
            html.write("	font-size: 10px;\n")
            html.write("	color: #FFFFFF;\n")
            html.write("	background-color: #2296D3;\n")
            html.write("	font-weight: bold;\n")
            html.write("}\n")
            html.write(".cabtabla1 {\n")
            html.write("	font-family: Verdana, Arial, Helvetica, sans-serif;\n")
            html.write("	font-size: 15px;\n")
            html.write("	color: #FFFFFF;\n")
            html.write("	background-color: #2296D3;\n")
            html.write("	font-weight: bold;\n")
            html.write("}\n")
            html.write(".cabtabla2 {\n")
            html.write("	font-family: Verdana, Arial, Helvetica, sans-serif;\n")
            html.write("	font-size: 10px;\n")
            html.write("	background-color: #FFCC33;\n")
            html.write("	font-weight: bold;\n")
            html.write("}\n")
            html.write(".nombre {\n")
            html.write("	FONT-SIZE: 10pt; COLOR: #2d348a; FONT-FAMILY: Verdana; TEXT-DECORATION: none; font-weight: bold;\n")
            html.write("}\n")
            html.write(".otros {\n")
            html.write("	FONT-SIZE: 10px; COLOR: #2d348a; FONT-FAMILY: Verdana; TEXT-DECORATION: none; font-weight: bold;\n")
            html.write("}\n")
            html.write(".importe {\n")
            html.write("	FONT-SIZE: 10px; COLOR: #FF403B; FONT-FAMILY: Verdana; TEXT-DECORATION: none; font-weight: bold;\n")
            html.write("}\n")
            html.write(".total {\n")
            html.write("FONT-SIZE: 15px; COLOR: #2296D3; FONT-FAMILY: Verdana; TEXT-DECORATION: none; font-weight: bold;\n")
            html.write("}\n")            
            html.write(".totalgeneral {\n")
            html.write("FONT-SIZE: 16px;COLOR: #FF403B ;background-color: #FFCC33; FONT-FAMILY: Verdana; TEXT-DECORATION: none; font-weight: bold;\n")
            html.write("}\n")            
            html.write("-->\n")
            html.write("</style>\n")
            html.write("</HEAD>\n")
            html.write("<BODY BGCOLOR=#FFFFFF  LEFTMARGIN=0 TOPMARGIN=0 MARGINWIDTH=0 MARGINHEIGHT=0>\n")
            html.write("<br>\n")
            
            f=open(self.Fichero)
            sumatorio=0
            sumatorioTotal=0
            while 1:
                linea=f.readline()
                if linea=="":
                    break
                else:
                    #si es el presentador
                    if linea[0:4]=="5190":
                        Presen=linea[28:68].strip()+" - "+linea[108:148].strip()
                        html.write("<table width='80%' align='center' border='1' cellspacing='1' cellpadding='3'>\n")
                        html.write("<tr>\n")
                        html.write("<td width='100%' align='center'><strong>"+Presen+"</strong></td>\n")
                        html.write("</tr></table>\n")

                    #Si es total de ordenante
                    if linea[0:4]=="5890" and sumatorio<>0:
                        html.write("</table>\n")
                        html.write("<table width='100%' border='0' cellspacing='1' cellpadding='3'>\n")
                        html.write("<tr>\n")
                        html.write("<td width='60%' align='right' class='total' >Total:</td>\n")
                        html.write("<td width='10%' align='right' class='total' bgcolor='#EEEEEE'>"+str(sumatorio)+"</td>\n")
                        html.write("<td width='30%' align='left'></td>\n")
                        html.write("</tr></table>\n")
                        #html.write("<br>\n")
                        html.write("<hr>\n")
                        #html.write("<br>\n")
                        
                    #Si es cabecera de ordenante                        
                    if linea[0:4]=="5390":
                        sumatorio=0
                        #Ordenante
                        html.write("<br><br>\n")
                        html.write("<table width='100%' border='0' cellspacing='1' cellpadding='3'>\n")

                        html.write("<tr>\n")
                        html.write("<td width='10%' align='center' class='cabtabla2'>Fecha</td>\n")            
                        html.write("<td width='70%' align='Left' class='cabtabla2'>Ordenante</td>\n")            
                        html.write("<td width='20%' align='Left' class='cabtabla2'>Nif - Sufijo</td>\n")
                        html.write("</tr>\n")
                        
                        html.write("<tr>\n")
                        fecha=linea[22:24]+"-"+linea[24:26]+"-20"+linea[26:28]
                        html.write("<td width='10%' align='center' class='cabtabla1'>"+fecha+"</td>\n")            
                        html.write("<td width='70%' align='Left' class='cabtabla1'>"+linea[28:68]+"</td>\n")            
                        html.write("<td width='20%' align='Left' class='cabtabla1'>"+linea[4:13]+" - "+linea[13:16]+"</td>\n")
                        html.write("</tr>\n")
                        html.write("</table>\n")
                        html.write("<br>\n")
                        
                        
                        #Cabeceras de Devoluciones
                        html.write("<table width='100%' border='0' cellspacing='1' cellpadding='3'>\n")
                        html.write("<tr class='cabtabla2'> \n")
                        html.write("<td width='40%' align='left'>Nombre</td>\n")
                        html.write("<td width='20%' align='center'>Cuenta</td>\n")
                        html.write("<td width='10%' align='right'>Importe</td>\n")
                        html.write("<td width='30%' align='left'>Motivo</td>\n")
                        html.write("</tr>\n")
                        
                        
                        #Ahora leemos la siguiente linea que deberia ser un 5690
                        #linea=f.readline()
                        
                    if linea[0:4]=="5690":
                        motivo=""
                        if linea[154:155]=="0":
                            motivo="Importe a 0"
                        elif linea[154:155]=="1":
                            motivo="Incorriente"
                        elif linea[154:155]=="2":
                            motivo="No domiciliado o cuenta cancelada"
                        elif linea[154:155]=="3":
                            motivo="Oficina domiciliadora inexistente"
                        elif linea[154:155]=="4":
                            motivo="Aplicacion R.D. 338/90 sobre el NIF"
                        elif linea[154:155]=="5":
                            motivo="Por orden del cliente: error o baja en la domiciliacion"
                        elif linea[154:155]=="6":
                            motivo="Por orden del cliente: disconformidad con el importe"
                        elif linea[154:155]=="7":
                            motivo="Adeudo duplicado, indebido, erroneo o faltan datos"
                        elif linea[154:155]=="8":
                            motivo="Sin determinar"
                        else:
                            motivo="Sin determinar"
                        
                        #detalle de Devoluciones
                        html.write("<tr bgcolor='#EEEEEE'> \n")
                        html.write("<td class='nombre'  align='left'  >"+linea[28:68]+"</td>\n")
                        html.write("<td class='otros'   align='center'>"+linea[68:72]+" "+linea[72:76]+" "+linea[76:78]+" "+linea[78:88]+"</td>\n")
                        html.write("<td class='importe' align='right' >"+str(int(linea[88:96]))+","+linea[96:98]+"</td>\n")
                        html.write("<td class='otros'   align='left'>"+motivo+"</td>\n")
                        html.write("</tr>\n")
                        sumatorio=sumatorio+float(str(int(linea[88:96]))+"."+linea[96:98])
                        sumatorioTotal=sumatorioTotal+float(str(int(linea[88:96]))+"."+linea[96:98])
                    
                    #Total General
                    if linea[0:4]=="5990":
                        html.write("</table>\n")
                        html.write("<table width='100%' border='0' cellspacing='1' cellpadding='3'>\n")
                        html.write("<tr>\n")
                        html.write("<td width='60%' align='right'><strong>Total General:</strong></td>\n")
                        html.write("<td width='10%' align='right' class='totalgeneral'>"+str(sumatorioTotal)+"</td>\n")
                        html.write("<td width='30%' align='left'></td>\n")
                        html.write("</tr></table>\n")
                        html.write("<br>")
                        
            html.write("<br><br>\n")
            html.write("<br><br>\n")
            html.write("</BODY></HTML>\n")
            
            
            
            html.close()
            f.close()
            #os.system("pdf.py "+self.Fichero+".html")
            os.system(self.Fichero+".html")
        else:
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,"Para poder imprimir las devoluciones debe de abrir el fichero de devoluciones")
            dialog.connect('response', lambda dialog, response: dialog.destroy())
            dialog.show()

    def Imprimir(self, Widget):

        if self.Fichero<>"" and self.NifSufijo<>"":
            html=open(self.Fichero+".html","w")
            
            #Cabecera del fichero
            html.write("<HTML>\n")
            html.write("<HEAD>\n")
            html.write("<TITLE>"+self.tPresentador.get_text()+"</TITLE>\n")
            html.write("<META HTTP-EQUIV='Content-Type' CONTENT='text/html; charset=iso-8859-1'>\n")
            html.write("<style type='text/css'>\n")
            html.write("<!-- \n")
            html.write(".cabtabla {\n")
            html.write("	font-family: Verdana, Arial, Helvetica, sans-serif;\n")
            html.write("	font-size: 10px;\n")
            html.write("	color: #FFFFFF;\n")
            html.write("	background-color: #2296D3;\n")
            html.write("	font-weight: bold;\n")
            html.write("}\n")
            html.write(".cabtabla1 {\n")
            html.write("	font-family: Verdana, Arial, Helvetica, sans-serif;\n")
            html.write("	font-size: 15px;\n")
            html.write("	color: #FFFFFF;\n")
            html.write("	background-color: #2296D3;\n")
            html.write("	font-weight: bold;\n")
            html.write("}\n")
            html.write(".cabtabla2 {\n")
            html.write("	font-family: Verdana, Arial, Helvetica, sans-serif;\n")
            html.write("	font-size: 10px;\n")
            html.write("	background-color: #FFCC33;\n")
            html.write("	font-weight: bold;\n")
            html.write("}\n")
            html.write(".nombre {\n")
            html.write("	FONT-SIZE: 10pt; COLOR: #2d348a; FONT-FAMILY: Verdana; TEXT-DECORATION: none; font-weight: bold;\n")
            html.write("}\n")
            html.write(".otros {\n")
            html.write("	FONT-SIZE: 10px; COLOR: #2d348a; FONT-FAMILY: Verdana; TEXT-DECORATION: none; font-weight: bold;\n")
            html.write("}\n")
            html.write(".importe {\n")
            html.write("	FONT-SIZE: 10px; COLOR: #FF403B; FONT-FAMILY: Verdana; TEXT-DECORATION: none; font-weight: bold;\n")
            html.write("}\n")
            html.write(".total {\n")
            html.write("FONT-SIZE: 15px; COLOR: #2296D3; FONT-FAMILY: Verdana; TEXT-DECORATION: none; font-weight: bold;\n")
            html.write("-->\n")
            html.write("</style>\n")
            html.write("</HEAD>\n")
            html.write("<BODY BGCOLOR=#FFFFFF  LEFTMARGIN=0 TOPMARGIN=0 MARGINWIDTH=0 MARGINHEIGHT=0>\n")
            html.write("<br>\n")
            html.write("<table width='100%' border='0' cellspacing='1' cellpadding='3'>\n")
            html.write("<tr>\n")
            
            #Ordenante
            Linea=self.tvOrdenantes.get_cursor()
            store=self.tvOrdenantes.get_model()
            iter=store[Linea[0][0]]
            self.NifSufijo=iter[0]+iter[1]
            html.write("<td width='80%' align='Left' class='cabtabla1'>"+iter[2]+"</td>\n")            
            html.write("<td width='20%' align='center' class='cabtabla'>"+iter[0]+"-"+iter[1]+"</td>\n")
            html.write("</tr>\n")
            html.write("</table>\n")
            html.write("<br><br>\n")


            #Cabeceras de Devoluciones
            html.write("<table width='100%' border='0' cellspacing='1' cellpadding='3'>\n")
            html.write("<tr class='cabtabla2'> \n")
            html.write("<td width='40%' align='left'>Nombre</td>\n")
            html.write("<td width='20%' align='center'>Cuenta</td>\n")
            html.write("<td width='10%' align='right'>Importe</td>\n")
            html.write("<td width='30%' align='left'>Motivo</td>\n")
            html.write("</tr>\n")

        if self.Fichero<>"" and self.NifSufijo<>"":
            f=open(self.Fichero)
            sumatorio=0
            while 1:
                linea=f.readline()
                if linea=="":
                    break
                else:
                    #Mirar a ver si es el ordenante que buscamos
                    if linea[0:4]=="5390" and self.NifSufijo==linea[4:16]:
                        #Leemos la siguiente linea que deberia ser un 5690
                        linea=f.readline()
                        if linea[0:4]=="5690":
                            motivo=""
                            if linea[154:155]=="0":
                                motivo="Importe a 0"
                            elif linea[154:155]=="1":
                                motivo="Incorriente"
                            elif linea[154:155]=="2":
                                motivo="No domiciliado o cuenta cancelada"
                            elif linea[154:155]=="3":
                                motivo="Oficina domiciliadora inexistente"
                            elif linea[154:155]=="4":
                                motivo="Aplicacion R.D. 338/90 sobre el NIF"
                            elif linea[154:155]=="5":
                                motivo="Por orden del cliente: error o baja en la domiciliacion"
                            elif linea[154:155]=="6":
                                motivo="Por orden del cliente: disconformidad con el importe"
                            elif linea[154:155]=="7":
                                motivo="Adeudo duplicado, indebido, erroneo o faltan datos"
                            elif linea[154:155]=="8":
                                motivo="Sin determinar"
                            else:
                                motivo="Sin determinar"

                            #detalle de Devoluciones
                            html.write("<tr bgcolor='#EEEEEE'> \n")
                            html.write("<td class='nombre'  align='left'  >"+linea[28:68]+"</td>\n")
                            html.write("<td class='otros'   align='center'>"+linea[68:72]+" "+linea[72:76]+" "+linea[76:78]+" "+linea[78:88]+"</td>\n")
                            html.write("<td class='importe' align='right' >"+str(int(linea[88:96]))+","+linea[96:98]+"</td>\n")
                            html.write("<td class='otros'   align='left'>"+motivo+"</td>\n")
                            html.write("</tr>\n")
                            sumatorio=sumatorio+float(str(int(linea[88:96]))+"."+linea[96:98])
            f.close()
            html.write("</table><table width='100%' border='0' cellspacing='1' cellpadding='3'>\n")
            html.write("<tr>\n")
            html.write("<td width='60%' align='center'></td>\n")
            html.write("<td width='10%' align='right' class='total' bgcolor='#EEEEEE'>"+str(sumatorio)+"</td>\n")
            html.write("<td width='30%' align='left'></td>\n")
            html.write("</tr></table>\n")
            
            html.write("</BODY></HTML>\n")
            

            
            
            html.close()
            f.close()
            os.system(self.Fichero+".html")
        else:
            dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK,"Para poder imprimir las devoluciones debe de seleccionar el ordenante haciendo doble click sobe el")
            dialog.connect('response', lambda dialog, response: dialog.destroy())
            dialog.show()

        
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
        
    def Acercade(self, widget):
        glAcercade= gtk.glade.XML("./acercade.glade")
        self.vent_acercade=glAcercade.get_widget("acercade")
        
        self.okbutton1=glAcercade.get_widget("okbutton1")
        self.okbutton1.connect("clicked", lambda glAcercade, response: self.vent_acercade.destroy(),None)
        
        
    def Salir(self,*args):
        #True
        if self.Llamada<>"":
            self.ventana.hide()
            return True
        else:
            gtk.main_quit()

    def Main(self):
        self.Llamada=""
        gtk.main()
        
if __name__ == "__main__":
    gtk.rc_parse("gtkrc.txt")
    ven = Devoluciones()
    ven.Main()
    
    
