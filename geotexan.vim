" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 07 febrero 2014 at 14:49:00.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'light'
	set background=light
endif
if !exists('g:colors_name') || g:colors_name != 'github' | colorscheme github | endif
call setqflist([])
let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Geotexan/src/Geotex-INN
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +163 ~/.vimrc
badd +1 formularios/auditviewer.py
badd +13 ~/.vim/plugin/ack.vim
badd +249 formularios/consulta_existenciasBolsas.py
badd +1 formularios/dynconsulta.py
badd +1 framework/pclases.py
badd +168 formularios/gestor_mensajes.py
badd +181 formularios/menu.py
badd +85 formularios/autenticacion.py
badd +1 formularios/dynconsulta.glade
badd +179 formularios/consulta_facturas_sin_doc_pago.py
badd +73 formularios/utils_almacen.py
badd +1 ginn/formularios/dynconsulta.glade
badd +279 ginn/formularios/dynconsulta.py
badd +77 ginn/framework/pclases.py
badd +201 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +706 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1390 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +1798 ginn/formularios/partes_de_fabricacion_balas.py
badd +580 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1776 ginn/formularios/partes_de_fabricacion_rollos.py
badd +312 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +93 ginn/formularios/launcher.py
badd +625 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +760 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +9542 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2332 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +750 ginn/formularios/ventana.py
badd +992 ginn/formularios/pedidos_de_venta.py
badd +1559 db/tablas.sql
badd +799 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +2642 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +1527 ginn/formularios/facturas_compra.py
badd +138 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +394 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +218 ginn/formularios/gtkexcepthook.py
badd +402 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +134 ginn/framework/pclases/facturaventa.py
badd +694 ginn/formularios/consulta_mensual_nominas.py
badd +88 ginn/informes/treeview2pdf.py
badd +163 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +82 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +140 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +289 ginn/formularios/consumo_balas_partida.py
badd +324 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +397 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +1020 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +542 ginn/formularios/postomatic.py
badd +18 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +39 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +434 ginn/formularios/consulta_productividad.py
badd +171 ginn/formularios/mail_sender.py
badd +1143 ginn/formularios/abonos_venta.py
badd +306 ginn/formularios/ventana_progreso.py
badd +993 ginn/formularios/control_personal.py
badd +195 ginn/formularios/listado_rollos.py
badd +74 ginn/formularios/consulta_existenciasRollos.py
badd +91 ginn/formularios/listado_rollos_defectuosos.py
badd +3498 ginn/formularios/consulta_global.py
badd +168 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
badd +1 ginn/informes/presupuesto.py
badd +112 ginn/formularios/consulta_libro_iva.py
badd +298 ginn/formularios/consulta_ofertas.py
badd +24 extra/patches/create_ventana_consultas.py
badd +203 ginn/lib/ezodf/ezodf/const.py
badd +61 ginn/lib/ezodf/ezodf/xmlns.py
badd +21 ginn/lib/simple_odspy/simpleodspy/sodsods.py
badd +17 ginn/lib/simple_odspy/simpleodspy/sodsspreadsheet.py
badd +41 ginn/lib/simple_odspy/simpleodspy/sodstable.py
badd +66 ginn/lib/odfpy/contrib/odscell/odscell
badd +127 ginn/lib/odfpy/contrib/odscell/odscell.py
badd +76 ginn/formularios/consulta_ofertas_pendientes_validar.py
badd +392 ginn/formularios/consulta_ofertas_estudio.py
badd +1075 ginn/formularios/confirmings.py
badd +177 ginn/formularios/transferencias.py
badd +66 ginn/formularios/cuentas_destino.py
badd +509 ginn/formularios/facturacion_por_cliente_y_fechas.py
badd +1 ginn/formularios/presupuestos.glade
badd +24 ginn/lib/simple_odspy/simpleodspy/sodsxls.py
badd +1 ginn/formularios/ofer
badd +1 ginn/formularios/usuarios.glade
badd +251 ginn/formularios/usuarios.py
badd +7 ginn/lib/xlutils/xlutils/copy.py
badd +108 ginn/lib/xlutils/xlutils/filter.py
badd +10 ginn/lib/xlutils/xlutils/display.py
badd +8 ginn/lib/xlutils/xlutils/margins.py
badd +1 ginn/lib/xlutils/xlutils/filter.pyç
badd +381 ginn/lib/xlrd/xlrd/__init__.py
badd +9 ginn/lib/xlwt/xlwt/__init__.py
badd +659 ginn/lib/xlwt/xlwt/Workbook.py
badd +123 ginn/formularios/gestor_mensajes.py
badd +450 ginn/formularios/prefacturas.py
badd +1 presupuestos
badd +1 ginn/formularios/consulta_albaranesPorFacturar.glade
badd +393 ginn/formularios/consulta_albaranesPorFacturar.py
badd +1 ginn/formularios/checklist_window.py
badd +637 ginn/formularios/pedidos_de_compra.py
badd +92 ginn/formularios/utils_almacen.py
badd +178 ginn/formularios/consumo_fibra_por_partida_gtx.py
badd +138 ginn/lib/charting.py
args formularios/auditviewer.py
set lines=45 columns=101
edit ginn/framework/pclases/__init__.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
5wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 20 + 50) / 101)
exe '2resize ' . ((&lines * 21 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 50) / 101)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 50) / 101)
exe '4resize ' . ((&lines * 13 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 50) / 101)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 50) / 101)
argglobal
enew
file __Tag_List__
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=9999
setlocal fml=0
setlocal fdn=20
setlocal fen
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
270
normal! zo
361
normal! zo
370
normal! zo
375
normal! zo
390
normal! zo
644
normal! zo
683
normal! zo
780
normal! zo
1105
normal! zo
1197
normal! zo
1206
normal! zo
1248
normal! zo
1254
normal! zo
1254
normal! zo
1254
normal! zo
1281
normal! zo
1287
normal! zo
1287
normal! zo
1287
normal! zo
1306
normal! zo
1315
normal! zo
1415
normal! zo
1424
normal! zo
1524
normal! zo
1533
normal! zo
1633
normal! zo
1754
normal! zo
2455
normal! zo
2834
normal! zo
3043
normal! zo
3532
normal! zo
3844
normal! zo
3878
normal! zo
3880
normal! zo
3936
normal! zo
3943
normal! zo
3944
normal! zo
3944
normal! zo
3944
normal! zo
3944
normal! zo
3944
normal! zo
3944
normal! zo
3968
normal! zo
4018
normal! zo
4021
normal! zo
4026
normal! zo
4027
normal! zo
4027
normal! zo
4027
normal! zo
4031
normal! zo
4031
normal! zo
4031
normal! zo
4031
normal! zo
4031
normal! zo
4031
normal! zo
4034
normal! zo
4034
normal! zo
4040
normal! zo
4042
normal! zo
4047
normal! zo
4050
normal! zo
4052
normal! zo
4057
normal! zo
4058
normal! zo
4068
normal! zo
4076
normal! zo
4077
normal! zo
4077
normal! zo
4077
normal! zo
4077
normal! zo
4081
normal! zo
4084
normal! zo
4085
normal! zo
4085
normal! zo
4085
normal! zo
4085
normal! zo
4085
normal! zo
4099
normal! zo
4122
normal! zo
4166
normal! zo
4579
normal! zo
4590
normal! zo
4724
normal! zo
4809
normal! zo
4848
normal! zo
4860
normal! zo
4861
normal! zo
4861
normal! zo
4861
normal! zo
5138
normal! zo
5162
normal! zo
5173
normal! zo
5173
normal! zo
5173
normal! zo
5225
normal! zo
5231
normal! zo
5231
normal! zo
5231
normal! zo
5231
normal! zo
5247
normal! zo
5247
normal! zo
5247
normal! zo
5247
normal! zo
5247
normal! zo
5343
normal! zo
5349
normal! zo
5373
normal! zo
5400
normal! zo
5490
normal! zo
5502
normal! zo
5503
normal! zo
5504
normal! zo
5504
normal! zo
5504
normal! zo
5504
normal! zo
5506
normal! zo
5506
normal! zo
5506
normal! zo
5506
normal! zo
5506
normal! zo
5557
normal! zo
5557
normal! zo
5557
normal! zo
5557
normal! zo
5557
normal! zo
5585
normal! zo
5588
normal! zo
5607
normal! zo
5608
normal! zo
5609
normal! zo
5619
normal! zo
5671
normal! zo
5672
normal! zo
5792
normal! zo
5847
normal! zo
5859
normal! zo
5924
normal! zo
5968
normal! zo
5976
normal! zo
6002
normal! zo
6015
normal! zo
6019
normal! zo
6025
normal! zo
6158
normal! zo
6284
normal! zo
7540
normal! zo
7569
normal! zo
7569
normal! zo
7569
normal! zo
7569
normal! zo
7569
normal! zo
7593
normal! zo
7662
normal! zo
7681
normal! zo
7684
normal! zo
7685
normal! zo
7685
normal! zo
7685
normal! zo
7698
normal! zo
7699
normal! zo
7700
normal! zo
7705
normal! zo
7711
normal! zo
7717
normal! zo
7717
normal! zo
7717
normal! zo
7717
normal! zo
7717
normal! zo
7717
normal! zo
7719
normal! zo
7758
normal! zo
7768
normal! zo
7769
normal! zo
7777
normal! zo
7778
normal! zo
7781
normal! zo
7786
normal! zo
7787
normal! zo
7788
normal! zo
7789
normal! zo
7789
normal! zo
7789
normal! zo
7789
normal! zo
7789
normal! zo
7789
normal! zo
7793
normal! zo
7799
normal! zo
7802
normal! zo
7802
normal! zo
7802
normal! zo
7802
normal! zo
7802
normal! zo
7811
normal! zo
7812
normal! zo
7813
normal! zo
7821
normal! zo
7828
normal! zo
7828
normal! zo
7828
normal! zo
7828
normal! zo
7828
normal! zo
7828
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7830
normal! zo
7833
normal! zo
7833
normal! zo
7833
normal! zo
7833
normal! zo
7833
normal! zo
7833
normal! zo
7834
normal! zo
7834
normal! zo
7834
normal! zo
7834
normal! zo
7836
normal! zo
7837
normal! zo
7846
normal! zo
7853
normal! zo
7853
normal! zo
7853
normal! zo
7853
normal! zo
7853
normal! zo
7853
normal! zo
7855
normal! zo
7858
normal! zo
7858
normal! zo
7858
normal! zo
7858
normal! zo
7858
normal! zo
7858
normal! zo
7859
normal! zo
7859
normal! zo
7859
normal! zo
7859
normal! zo
7861
normal! zo
7862
normal! zo
7865
normal! zo
7870
normal! zo
7870
normal! zo
7870
normal! zo
7870
normal! zo
7870
normal! zo
7870
normal! zo
7870
normal! zo
7918
normal! zo
7923
normal! zo
7925
normal! zo
7926
normal! zo
7926
normal! zo
7926
normal! zo
7926
normal! zo
7926
normal! zo
7926
normal! zo
7929
normal! zo
7935
normal! zo
7938
normal! zo
7947
normal! zo
7949
normal! zo
7950
normal! zo
7957
normal! zo
7958
normal! zo
7959
normal! zo
7964
normal! zo
7968
normal! zo
7976
normal! zo
7977
normal! zo
7979
normal! zo
7979
normal! zo
7986
normal! zo
7987
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7988
normal! zo
7991
normal! zo
7991
normal! zo
7991
normal! zo
7998
normal! zo
8000
normal! zo
8283
normal! zo
8294
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8295
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8298
normal! zo
8302
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8309
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8312
normal! zo
8747
normal! zo
8751
normal! zo
8782
normal! zo
8831
normal! zo
8838
normal! zo
9006
normal! zo
9017
normal! zo
9030
normal! zo
9031
normal! zo
9044
normal! zo
9049
normal! zo
9054
normal! zo
9059
normal! zo
9070
normal! zo
9093
normal! zo
9116
normal! zo
9117
normal! zo
9117
normal! zo
9117
normal! zo
9117
normal! zo
9117
normal! zo
9117
normal! zo
9128
normal! zo
9143
normal! zo
9266
normal! zo
9296
normal! zo
9303
normal! zo
9306
normal! zo
9321
normal! zo
9369
normal! zo
9410
normal! zo
9672
normal! zo
9698
normal! zo
9737
normal! zo
9748
normal! zo
9749
normal! zo
9762
normal! zo
9777
normal! zo
9793
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9810
normal! zo
9817
normal! zo
9831
normal! zo
9832
normal! zo
9832
normal! zo
9834
normal! zo
9835
normal! zo
9835
normal! zo
9837
normal! zo
9838
normal! zo
9838
normal! zo
9840
normal! zo
9841
normal! zo
9841
normal! zo
9843
normal! zo
9846
normal! zo
9848
normal! zo
9848
normal! zo
9848
normal! zo
9857
normal! zo
9870
normal! zo
9873
normal! zo
9874
normal! zo
9874
normal! zo
9877
normal! zo
9877
normal! zo
9877
normal! zo
9880
normal! zo
9880
normal! zo
9880
normal! zo
9880
normal! zo
9886
normal! zo
9889
normal! zo
9893
normal! zo
9900
normal! zo
9902
normal! zo
9949
normal! zo
9963
normal! zo
9964
normal! zo
9966
normal! zo
10001
normal! zo
10008
normal! zo
10013
normal! zo
10014
normal! zo
10019
normal! zo
10019
normal! zo
10019
normal! zo
10019
normal! zo
10019
normal! zo
10022
normal! zo
10022
normal! zo
10022
normal! zo
10048
normal! zo
10057
normal! zo
10062
normal! zo
10064
normal! zo
10069
normal! zo
10075
normal! zo
10083
normal! zo
10084
normal! zo
10084
normal! zo
10084
normal! zo
10084
normal! zo
10093
normal! zo
10094
normal! zo
10099
normal! zo
10148
normal! zo
10153
normal! zo
10266
normal! zo
10293
normal! zo
10298
normal! zo
10304
normal! zo
10390
normal! zo
10397
normal! zo
10398
normal! zo
10446
normal! zo
10446
normal! zo
10446
normal! zo
10446
normal! zo
10446
normal! zo
10449
normal! zo
10457
normal! zo
10458
normal! zo
10503
normal! zo
10523
normal! zo
10524
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10525
normal! zo
10542
normal! zo
10548
normal! zo
10558
normal! zo
10573
normal! zo
10576
normal! zo
10579
normal! zo
10579
normal! zo
10579
normal! zo
10582
normal! zo
10582
normal! zo
10582
normal! zo
10582
normal! zo
10587
normal! zo
10587
normal! zo
10587
normal! zo
10595
normal! zo
10602
normal! zo
10609
normal! zo
10612
normal! zo
10614
normal! zo
10617
normal! zo
10620
normal! zo
10625
normal! zo
10636
normal! zo
10643
normal! zo
10647
normal! zo
10648
normal! zo
10648
normal! zo
10650
normal! zo
10651
normal! zo
10651
normal! zo
10653
normal! zo
10654
normal! zo
10654
normal! zo
10656
normal! zo
10657
normal! zo
10657
normal! zo
10659
normal! zo
10660
normal! zo
10660
normal! zo
10662
normal! zo
10663
normal! zo
10663
normal! zo
10665
normal! zo
10666
normal! zo
10666
normal! zo
10668
normal! zo
10671
normal! zo
10673
normal! zo
10673
normal! zo
10673
normal! zo
10679
normal! zo
10680
normal! zo
10680
normal! zo
10682
normal! zo
10683
normal! zo
10683
normal! zo
10707
normal! zo
10711
normal! zo
10714
normal! zo
10715
normal! zo
10715
normal! zo
10715
normal! zo
10715
normal! zo
10715
normal! zo
10715
normal! zo
10720
normal! zo
10721
normal! zo
10721
normal! zo
10721
normal! zo
10724
normal! zo
10836
normal! zo
10912
normal! zo
10920
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10927
normal! zo
10938
normal! zo
10942
normal! zo
10943
normal! zo
10943
normal! zo
10943
normal! zo
10953
normal! zo
10956
normal! zo
10963
normal! zo
10972
normal! zo
10981
normal! zo
11091
normal! zo
11105
normal! zo
11105
normal! zo
11105
normal! zo
11105
normal! zo
11117
normal! zo
11130
normal! zo
11143
normal! zo
11150
normal! zo
11152
normal! zo
11152
normal! zo
11152
normal! zo
11152
normal! zo
11152
normal! zo
11152
normal! zo
11177
normal! zo
11205
normal! zo
11217
normal! zo
11218
normal! zo
11218
normal! zo
11218
normal! zo
11218
normal! zo
11389
normal! zo
11397
normal! zo
11397
normal! zo
11397
normal! zo
11397
normal! zo
11411
normal! zo
11422
normal! zo
11439
normal! zo
11439
normal! zo
11443
normal! zo
11448
normal! zo
11448
normal! zo
11450
normal! zo
11451
normal! zo
11451
normal! zo
11456
normal! zo
11456
normal! zo
11456
normal! zo
11456
normal! zo
11456
normal! zo
11469
normal! zo
11472
normal! zo
11472
normal! zo
11472
normal! zo
11472
normal! zo
11478
normal! zo
11478
normal! zo
11478
normal! zo
11478
normal! zo
11478
normal! zo
11506
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11604
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11625
normal! zo
11666
normal! zo
11667
normal! zo
11689
normal! zo
11994
normal! zo
11994
normal! zo
11994
normal! zo
12008
normal! zo
12045
normal! zo
12056
normal! zo
12061
normal! zo
12079
normal! zo
12079
normal! zo
12079
normal! zo
12079
normal! zo
12080
normal! zo
12085
normal! zo
12101
normal! zo
12101
normal! zo
12101
normal! zo
12101
normal! zo
13297
normal! zo
13431
normal! zo
13431
normal! zo
13431
normal! zo
13441
normal! zo
13446
normal! zo
13447
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13448
normal! zo
13454
normal! zo
13455
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13456
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13458
normal! zo
13460
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13461
normal! zo
13464
normal! zo
13466
normal! zo
13466
normal! zo
13471
normal! zo
13471
normal! zo
13481
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13482
normal! zo
13601
normal! zo
13601
normal! zo
13601
normal! zo
13622
normal! zo
13627
normal! zo
13628
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13635
normal! zo
13636
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13641
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13645
normal! zo
13647
normal! zo
13652
normal! zo
13661
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13662
normal! zo
13732
normal! zo
13732
normal! zo
13732
normal! zo
13743
normal! zo
13748
normal! zo
13749
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13750
normal! zo
13756
normal! zo
13757
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13758
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13760
normal! zo
13762
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13763
normal! zo
13766
normal! zo
13768
normal! zo
13773
normal! zo
13782
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13783
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13890
normal! zo
13900
normal! zo
13900
normal! zo
13900
normal! zo
13900
normal! zo
13900
normal! zo
13900
normal! zo
13902
normal! zo
13903
normal! zo
13903
normal! zo
13903
normal! zo
14098
normal! zo
14098
normal! zo
14098
normal! zo
14098
normal! zo
14114
normal! zo
14119
normal! zo
14120
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14121
normal! zo
14127
normal! zo
14128
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14129
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14131
normal! zo
14133
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14134
normal! zo
14137
normal! zo
14139
normal! zo
14139
normal! zo
14144
normal! zo
14144
normal! zo
14154
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14155
normal! zo
14215
normal! zo
14215
normal! zo
14215
normal! zo
14215
normal! zo
14227
normal! zo
14232
normal! zo
14233
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14234
normal! zo
14240
normal! zo
14241
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14242
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14244
normal! zo
14246
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14247
normal! zo
14250
normal! zo
14252
normal! zo
14252
normal! zo
14257
normal! zo
14257
normal! zo
14267
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14268
normal! zo
14336
normal! zo
14348
normal! zo
14351
normal! zo
14352
normal! zo
14353
normal! zo
14353
normal! zo
14353
normal! zo
14355
normal! zo
14356
normal! zo
14356
normal! zo
14356
normal! zo
14372
normal! zo
14383
normal! zo
14392
normal! zo
14402
normal! zo
14429
normal! zo
14434
normal! zo
14440
normal! zo
14451
normal! zo
14464
normal! zo
14488
normal! zo
14490
normal! zo
14493
normal! zo
14496
normal! zo
14497
normal! zo
14501
normal! zo
14502
normal! zo
14516
normal! zo
14516
normal! zo
14516
normal! zo
14516
normal! zo
14538
normal! zo
14539
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14540
normal! zo
14549
normal! zo
14550
normal! zo
14556
normal! zo
14560
normal! zo
14561
normal! zo
14570
normal! zo
14571
normal! zo
14579
normal! zo
14580
normal! zo
14586
normal! zo
14601
normal! zo
14609
normal! zo
14615
normal! zo
14621
normal! zo
14626
normal! zo
14630
normal! zo
14636
normal! zo
14641
normal! zo
14642
normal! zo
14647
normal! zo
14658
normal! zo
14676
normal! zo
14718
normal! zo
14724
normal! zo
14730
normal! zo
14737
normal! zo
14746
normal! zo
14748
normal! zo
14755
normal! zo
14755
normal! zo
14755
normal! zo
14755
normal! zo
14755
normal! zo
14755
normal! zo
14772
normal! zo
14784
normal! zo
14795
normal! zo
14796
normal! zo
14812
normal! zo
14829
normal! zo
14833
normal! zo
14834
normal! zo
14835
normal! zo
14835
normal! zo
14837
normal! zo
14840
normal! zo
14853
normal! zo
14863
normal! zo
14865
normal! zo
14869
normal! zo
14870
normal! zo
14870
normal! zo
14870
normal! zo
14870
normal! zo
14870
normal! zo
14870
normal! zo
14883
normal! zo
14904
normal! zo
14905
normal! zo
14912
normal! zo
14945
normal! zo
14946
normal! zo
14946
normal! zo
14962
normal! zo
14968
normal! zo
14971
normal! zo
14971
normal! zo
14971
normal! zo
14977
normal! zo
14977
normal! zo
14997
normal! zo
15002
normal! zo
15007
normal! zo
15015
normal! zo
15034
normal! zo
15068
normal! zo
15076
normal! zo
15085
normal! zo
15104
normal! zo
15106
normal! zo
15110
normal! zo
15127
normal! zo
15133
normal! zo
15137
normal! zo
15469
normal! zo
15500
normal! zo
15524
normal! zo
15534
normal! zo
15534
normal! zo
15534
normal! zo
15534
normal! zo
15534
normal! zo
15722
normal! zo
15741
normal! zo
15763
normal! zo
15768
normal! zo
15769
normal! zo
15769
normal! zo
15772
normal! zo
15773
normal! zo
15773
normal! zo
15773
normal! zo
15776
normal! zo
15776
normal! zo
15776
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
15780
normal! zo
16311
normal! zo
16347
normal! zo
16362
normal! zo
16368
normal! zo
16371
normal! zo
16379
normal! zo
16380
normal! zo
16380
normal! zo
16380
normal! zo
16380
normal! zo
16380
normal! zo
16384
normal! zo
16392
normal! zo
16395
normal! zo
16401
normal! zo
16407
normal! zo
16410
normal! zo
16416
normal! zo
16430
normal! zo
16436
normal! zo
16441
normal! zo
16444
normal! zo
16444
normal! zo
16444
normal! zo
16454
normal! zo
16469
normal! zo
16480
normal! zo
16480
normal! zo
16491
normal! zo
16506
normal! zo
16516
normal! zo
16527
normal! zo
16536
normal! zo
16543
normal! zo
16581
normal! zo
16586
normal! zo
16586
normal! zo
16586
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16599
normal! zo
16611
normal! zo
16632
normal! zo
16651
normal! zo
16659
normal! zo
16660
normal! zo
16661
normal! zo
16665
normal! zo
16669
normal! zo
16685
normal! zo
16700
normal! zo
16705
normal! zo
16710
normal! zo
16720
normal! zo
16721
normal! zo
16721
normal! zo
16721
normal! zo
16723
normal! zo
16723
normal! zo
16723
normal! zo
16723
normal! zo
16723
normal! zo
16723
normal! zo
16723
normal! zo
16723
normal! zo
16723
normal! zo
16723
normal! zo
16728
normal! zo
16729
normal! zo
16735
normal! zo
16736
normal! zo
16756
normal! zo
16781
normal! zo
16785
normal! zo
16802
normal! zo
16813
normal! zo
16813
normal! zo
16813
normal! zo
16813
normal! zo
16815
normal! zo
16816
normal! zo
16817
normal! zo
16818
normal! zo
16819
normal! zo
16823
normal! zo
16824
normal! zo
16825
normal! zo
16825
normal! zo
16825
normal! zo
16825
normal! zo
16825
normal! zo
16825
normal! zo
16825
normal! zo
16827
normal! zo
16829
normal! zo
16834
normal! zo
16834
normal! zo
16834
normal! zo
16834
normal! zo
16840
normal! zo
16844
normal! zo
16852
normal! zo
16852
normal! zo
16852
normal! zo
16852
normal! zo
16860
normal! zo
16868
normal! zo
16869
normal! zo
16872
normal! zo
16877
normal! zo
16885
normal! zo
16890
normal! zo
16898
normal! zo
16903
normal! zo
16912
normal! zo
16913
normal! zo
16913
normal! zo
16923
normal! zo
16938
normal! zo
16939
normal! zo
16955
normal! zo
16975
normal! zo
16976
normal! zo
16976
normal! zo
16976
normal! zo
16976
normal! zo
16976
normal! zo
16977
normal! zo
16982
normal! zo
16992
normal! zo
17006
normal! zo
17008
normal! zo
17009
normal! zo
17010
normal! zo
17011
normal! zo
17011
normal! zo
17011
normal! zo
17011
normal! zo
17011
normal! zo
17028
normal! zo
17035
normal! zo
17036
normal! zo
17043
normal! zo
17050
normal! zo
17051
normal! zo
17052
normal! zo
17054
normal! zo
17057
normal! zo
17064
normal! zo
17069
normal! zo
17082
normal! zo
17083
normal! zo
17083
normal! zo
17083
normal! zo
17088
normal! zo
17101
normal! zo
17108
normal! zo
17109
normal! zo
17124
normal! zo
17131
normal! zo
17145
normal! zo
17152
normal! zo
17153
normal! zo
17158
normal! zo
17167
normal! zo
17181
normal! zo
17203
normal! zo
17224
normal! zo
17237
normal! zo
17237
normal! zo
17237
normal! zo
17237
normal! zo
17237
normal! zo
17237
normal! zo
17247
normal! zo
17260
normal! zo
17284
normal! zo
17289
normal! zo
17291
normal! zo
17294
normal! zo
17301
normal! zo
17313
normal! zo
17323
normal! zo
17323
normal! zo
17323
normal! zo
17323
normal! zo
17323
normal! zo
17323
normal! zo
17331
normal! zo
17341
normal! zo
17341
normal! zo
17341
normal! zo
17341
normal! zo
17341
normal! zo
17341
normal! zo
17349
normal! zo
17350
normal! zo
17361
normal! zo
17366
normal! zo
17377
normal! zo
17385
normal! zo
17398
normal! zo
17402
normal! zo
17402
normal! zo
17402
normal! zo
17402
normal! zo
17402
normal! zo
17404
normal! zo
17416
normal! zo
17416
normal! zo
17416
normal! zo
17416
normal! zo
17416
normal! zo
17416
normal! zo
17416
normal! zo
17420
normal! zo
17420
normal! zo
17420
normal! zo
17420
normal! zo
17420
normal! zo
17420
normal! zo
17426
normal! zo
17426
normal! zo
17426
normal! zo
17426
normal! zo
17429
normal! zo
17430
normal! zo
17431
normal! zo
17437
normal! zo
17438
normal! zo
17438
normal! zo
17438
normal! zo
17560
normal! zo
17648
normal! zo
17705
normal! zo
17720
normal! zo
17727
normal! zo
17728
normal! zo
17744
normal! zo
17754
normal! zo
17768
normal! zo
17771
normal! zo
17772
normal! zo
17772
normal! zo
17794
normal! zo
17814
normal! zo
17826
normal! zo
17826
normal! zo
17826
normal! zo
17826
normal! zo
17826
normal! zo
17829
normal! zo
17836
normal! zo
17839
normal! zo
17850
normal! zo
17856
normal! zo
17861
normal! zo
17867
normal! zo
17868
normal! zo
17869
normal! zo
17872
normal! zo
17891
normal! zo
17906
normal! zo
17934
normal! zo
17959
normal! zo
17980
normal! zo
18015
normal! zo
18024
normal! zo
18025
normal! zo
18026
normal! zo
18028
normal! zo
18028
normal! zo
18028
normal! zo
18031
normal! zo
18033
normal! zo
18033
normal! zo
18033
normal! zo
18036
normal! zo
18037
normal! zo
18037
normal! zo
18037
normal! zo
18037
normal! zo
18037
normal! zo
18563
normal! zo
18580
normal! zo
18590
normal! zo
18593
normal! zo
18594
normal! zo
18594
normal! zo
18600
normal! zo
18607
normal! zo
18608
normal! zo
18609
normal! zo
18609
normal! zo
18609
normal! zo
18609
normal! zo
18613
normal! zo
18614
normal! zo
18614
normal! zo
18614
normal! zo
18614
normal! zo
18630
normal! zo
18931
normal! zo
19848
normal! zo
19872
normal! zo
19878
normal! zo
19884
normal! zo
19902
normal! zo
19912
normal! zo
19915
normal! zo
19922
normal! zo
19922
normal! zo
19922
normal! zo
19922
normal! zo
19927
normal! zo
20207
normal! zo
20213
normal! zo
20213
normal! zo
20222
normal! zo
20229
normal! zo
20236
normal! zo
20243
normal! zo
20250
normal! zo
20257
normal! zo
20264
normal! zo
20270
normal! zo
20271
normal! zo
20280
normal! zo
20289
normal! zo
20452
normal! zo
20462
normal! zo
20473
normal! zo
20484
normal! zo
20485
normal! zo
20490
normal! zo
20491
normal! zo
20491
normal! zo
20501
normal! zo
20501
normal! zo
20501
normal! zo
20501
normal! zo
20501
normal! zo
20501
normal! zo
20501
normal! zo
20501
normal! zo
20501
normal! zo
20512
normal! zo
20513
normal! zo
20521
normal! zo
20521
normal! zo
20521
normal! zo
20521
normal! zo
20521
normal! zo
20521
normal! zo
20521
normal! zo
20521
normal! zo
20532
normal! zo
20533
normal! zo
20589
normal! zo
20610
normal! zo
20615
normal! zo
20627
normal! zo
20627
normal! zo
20627
normal! zo
20627
normal! zo
20627
normal! zo
20627
normal! zo
20627
normal! zo
20645
normal! zo
let s:l = 17014 - ((14 * winheight(0) + 10) / 21)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
17014
normal! 09|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/lib/xlutils/xlutils/copy.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
10
normal! zo
let s:l = 21 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
21
normal! 025|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_global.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
82
normal! zo
83
normal! zo
166
normal! zo
218
normal! zo
248
normal! zo
277
normal! zo
369
normal! zo
399
normal! zo
437
normal! zo
437
normal! zo
510
normal! zo
579
normal! zo
707
normal! zo
732
normal! zo
759
normal! zo
793
normal! zo
887
normal! zo
894
normal! zo
916
normal! zo
923
normal! zo
938
normal! zo
943
normal! zo
977
normal! zo
987
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
989
normal! zo
998
normal! zo
1008
normal! zo
1012
normal! zo
1186
normal! zo
1303
normal! zo
1613
normal! zo
1629
normal! zo
1639
normal! zo
1686
normal! zo
1686
normal! zo
1706
normal! zo
1722
normal! zo
1723
normal! zo
1724
normal! zo
1730
normal! zo
1767
normal! zo
1767
normal! zo
1950
normal! zo
1952
normal! zo
2411
normal! zo
2418
normal! zo
2438
normal! zo
2630
normal! zo
2687
normal! zo
2736
normal! zo
2976
normal! zo
2994
normal! zo
3123
normal! zo
3489
normal! zo
3495
normal! zo
3519
normal! zo
let s:l = 1200 - ((7 * winheight(0) + 6) / 13)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1200
normal! 08|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_cobros.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
50
normal! zo
274
normal! zo
let s:l = 317 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
317
normal! 011|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/ventana.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
66
normal! zo
104
normal! zo
105
normal! zo
105
normal! zo
137
normal! zo
154
normal! zo
155
normal! zo
161
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
922
normal! zo
1068
normal! zo
let s:l = 926 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
926
normal! 020|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/configuracion.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
71
normal! zo
85
normal! zo
435
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
503
normal! zo
let s:l = 452 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
452
normal! 033|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 20 + 50) / 101)
exe '2resize ' . ((&lines * 21 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 50) / 101)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 50) / 101)
exe '4resize ' . ((&lines * 13 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 50) / 101)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 50) / 101)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
tabnext 1
2wincmd w

" vim: ft=vim ro nowrap smc=128
