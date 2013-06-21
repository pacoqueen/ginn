#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, gtk.glade  # No es verdad, pero PyDev lo quiere así: @UnusedImport
from formularios import clientes


class Recibo:
    def __init__(self):
        #Estas variables las pasa a otras ventanas
        self.CodCliente=""
        self.NomCliente=""
        self.Importe=""
        self.Conceptos=[""]
        self.Modificacion=""
        
        glRecibo=gtk.glade.XML("./gld/recibo.glade")
        self.ventana=glRecibo.get_widget("recibo")
        self.ventana.connect("destroy", self.Salir)
      
        self.tCodCliente=glRecibo.get_widget("tCodCliente")
        self.tNomCliente=glRecibo.get_widget("tNomCliente")
        self.tBanco=glRecibo.get_widget("tBanco")
        self.tOficina=glRecibo.get_widget("tOficina")
        self.tDc=glRecibo.get_widget("tDc")
        self.tCuenta=glRecibo.get_widget("tCuenta")

        self.tImporte=glRecibo.get_widget("tImporte")
        self.tImporte.connect("key_release_event",self.SoloNumeros)
        
        self.tConcepto1=glRecibo.get_widget("tConcepto1")
        self.tConcepto2=glRecibo.get_widget("tConcepto2")
        self.tConcepto3=glRecibo.get_widget("tConcepto3")
        self.tConcepto4=glRecibo.get_widget("tConcepto4")
        self.tConcepto5=glRecibo.get_widget("tConcepto5")
        self.tConcepto6=glRecibo.get_widget("tConcepto6")
        self.tConcepto7=glRecibo.get_widget("tConcepto7")
        self.tConcepto8=glRecibo.get_widget("tConcepto8")
        self.tConcepto9=glRecibo.get_widget("tConcepto9")
        self.tConcepto10=glRecibo.get_widget("tConcepto10")
        self.tConcepto11=glRecibo.get_widget("tConcepto11")
        self.tConcepto12=glRecibo.get_widget("tConcepto12")
        self.tConcepto13=glRecibo.get_widget("tConcepto13")
        self.tConcepto14=glRecibo.get_widget("tConcepto14")
        self.tConcepto15=glRecibo.get_widget("tConcepto15")
        self.tConcepto16=glRecibo.get_widget("tConcepto16")
        
        self.btnBuscar=glRecibo.get_widget("btnBuscar")
        self.btnBuscar.connect("clicked", self.Buscar)
        
        self.btnCancelar=glRecibo.get_widget("btnCancelar")
        self.btnCancelar.connect("clicked", self.Salir)
        
        self.btnAceptar=glRecibo.get_widget("btnAceptar")
        self.btnAceptar.connect("clicked", self.Aceptar)

    def mira(self):
        if self.w.CodCliente<>"x":
            if self.w.CodCliente<>"":
                self.tCodCliente.set_text(self.w.CodCliente)
                self.tNomCliente.set_text(self.w.NomCliente)
                self.tBanco.set_text(self.w.ccc[0:4])
                self.tOficina.set_text(self.w.ccc[4:8])
                self.tDc.set_text(self.w.ccc[8:10])
                self.tCuenta.set_text(self.w.ccc[10:20])
            return 0
        else:
            return 1
        


    def Buscar(self,widget):
        self.w=clientes.Clientes()
        self.w.Llamada="Recibos"
        #self.w.ventana.set_modal(True)
        self.w.CodCliente="x"
        self.timeout= gtk.timeout_add(250, self.mira)
        
    def Aceptar(self,widget):
        if self.tCodCliente.get_text()=="":
            self.Salir()
        elif self.tImporte.get_text()=="":
            self.Dialogo("No se puede grabar si no se pone nada en el importe",1)
        elif float(self.tImporte.get_text())==0:
            self.Dialogo("El importe ha de ser distinto de 0",1)
        else:
            self.CodCliente=self.tCodCliente.get_text()
            self.NomCliente=self.tNomCliente.get_text()
            self.Importe=self.tImporte.get_text()
            self.CapturaConceptos()
            self.ventana.hide()
            self.Llamada="Aceptar"
            return True
            
    def CapturaConceptos(self):
        #Los pasamos a un string separados por |
        self.Conceptos=""
        self.Conceptos=self.tConcepto1.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto2.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto3.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto4.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto5.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto6.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto7.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto8.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto9.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto10.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto11.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto12.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto13.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto14.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto15.get_text()
        self.Conceptos=self.Conceptos+"Ç"+self.tConcepto16.get_text()
        
        
        
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

    def SoloNumeros(self,widget,x):
        #Comprueba lo que se teclea.
        #Solo admite numeros o un punto
        
        texto=widget.get_text()
        if texto[len(texto)-1:len(texto)].isdigit()==0 and len(texto)>0 and texto[len(texto)-1:len(texto)]<>".":
            #if len(texto)>0:
            texto=texto[0:len(texto)-1]
            widget.set_text(texto)
            widget.set_position(len(texto))



    def Salir(self,*args):
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
        
if __name__ == "__main__":
    gtk.rc_parse("gtkrc.txt")
    ven = Recibo()
    ven.Main()
