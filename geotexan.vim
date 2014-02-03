" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 31 enero 2014 at 14:41:56.
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
badd +624 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1183 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +3989 ginn/formularios/partes_de_fabricacion_balas.py
badd +580 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +2250 ginn/formularios/partes_de_fabricacion_rollos.py
badd +446 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +93 ginn/formularios/launcher.py
badd +625 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +760 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1202 ginn/informes/geninformes.py
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
badd +3175 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +238 ginn/formularios/facturas_compra.py
badd +138 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
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
badd +704 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +134 ginn/framework/pclases/facturaventa.py
badd +694 ginn/formularios/consulta_mensual_nominas.py
badd +88 ginn/informes/treeview2pdf.py
badd +189 ginn/formularios/balas_cable.py
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
badd +93 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +1020 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +523 ginn/formularios/postomatic.py
badd +36 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +39 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +416 ginn/formularios/consulta_productividad.py
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
args formularios/auditviewer.py
set lines=45 columns=102
edit ginn/framework/pclases/cliente.py
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
wincmd _ | wincmd |
split
11wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 21 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
exe '9resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 9resize ' . ((&columns * 80 + 51) / 102)
exe '10resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 10resize ' . ((&columns * 80 + 51) / 102)
exe '11resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 11resize ' . ((&columns * 80 + 51) / 102)
exe '12resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 12resize ' . ((&columns * 80 + 51) / 102)
exe '13resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 13resize ' . ((&columns * 80 + 51) / 102)
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
53
normal! zo
let s:l = 499 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
499
normal! 033|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/pclases/__init__.py
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
16374
normal! zo
16382
normal! zo
16385
normal! zo
16391
normal! zo
16397
normal! zo
16400
normal! zo
16406
normal! zo
16420
normal! zo
16426
normal! zo
16431
normal! zo
16434
normal! zo
16434
normal! zo
16434
normal! zo
16444
normal! zo
16459
normal! zo
16470
normal! zo
16470
normal! zo
16481
normal! zo
16496
normal! zo
16506
normal! zo
16517
normal! zo
16522
normal! zo
16522
normal! zo
16522
normal! zo
16535
normal! zo
16561
normal! zo
16582
normal! zo
16601
normal! zo
16609
normal! zo
16610
normal! zo
16611
normal! zo
16615
normal! zo
16619
normal! zo
16635
normal! zo
16650
normal! zo
16655
normal! zo
16660
normal! zo
16670
normal! zo
16671
normal! zo
16671
normal! zo
16671
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16673
normal! zo
16678
normal! zo
16679
normal! zo
16685
normal! zo
16686
normal! zo
16706
normal! zo
16731
normal! zo
16735
normal! zo
16752
normal! zo
16763
normal! zo
16763
normal! zo
16763
normal! zo
16763
normal! zo
16765
normal! zo
16766
normal! zo
16767
normal! zo
16768
normal! zo
16769
normal! zo
16773
normal! zo
16774
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16775
normal! zo
16777
normal! zo
16779
normal! zo
16784
normal! zo
16784
normal! zo
16784
normal! zo
16784
normal! zo
16790
normal! zo
16794
normal! zo
16802
normal! zo
16802
normal! zo
16802
normal! zo
16802
normal! zo
16810
normal! zo
16818
normal! zo
16819
normal! zo
16822
normal! zo
16827
normal! zo
16835
normal! zo
16840
normal! zo
16848
normal! zo
16853
normal! zo
16862
normal! zo
16863
normal! zo
16863
normal! zo
16873
normal! zo
16888
normal! zo
16889
normal! zo
16905
normal! zo
16912
normal! zo
16917
normal! zo
16930
normal! zo
16931
normal! zo
16931
normal! zo
16931
normal! zo
16936
normal! zo
16949
normal! zo
16956
normal! zo
16957
normal! zo
16972
normal! zo
16979
normal! zo
16993
normal! zo
17000
normal! zo
17001
normal! zo
17006
normal! zo
17015
normal! zo
17029
normal! zo
17051
normal! zo
17072
normal! zo
17085
normal! zo
17085
normal! zo
17085
normal! zo
17085
normal! zo
17085
normal! zo
17085
normal! zo
17095
normal! zo
17108
normal! zo
17132
normal! zo
17137
normal! zo
17139
normal! zo
17142
normal! zo
17149
normal! zo
17161
normal! zo
17171
normal! zo
17171
normal! zo
17171
normal! zo
17171
normal! zo
17171
normal! zo
17171
normal! zo
17179
normal! zo
17189
normal! zo
17189
normal! zo
17189
normal! zo
17189
normal! zo
17189
normal! zo
17189
normal! zo
17197
normal! zo
17198
normal! zo
17209
normal! zo
17214
normal! zo
17225
normal! zo
17233
normal! zo
17246
normal! zo
17250
normal! zo
17250
normal! zo
17250
normal! zo
17250
normal! zo
17250
normal! zo
17252
normal! zo
17264
normal! zo
17264
normal! zo
17264
normal! zo
17264
normal! zo
17264
normal! zo
17264
normal! zo
17264
normal! zo
17268
normal! zo
17268
normal! zo
17268
normal! zo
17268
normal! zo
17268
normal! zo
17268
normal! zo
17274
normal! zo
17274
normal! zo
17274
normal! zo
17274
normal! zo
17277
normal! zo
17278
normal! zo
17279
normal! zo
17285
normal! zo
17286
normal! zo
17286
normal! zo
17286
normal! zo
17408
normal! zo
17496
normal! zo
17553
normal! zo
17568
normal! zo
17575
normal! zo
17576
normal! zo
17592
normal! zo
17602
normal! zo
17616
normal! zo
17619
normal! zo
17620
normal! zo
17620
normal! zo
17642
normal! zo
17662
normal! zo
17674
normal! zo
17674
normal! zo
17674
normal! zo
17674
normal! zo
17674
normal! zo
17677
normal! zo
17684
normal! zo
17687
normal! zo
17698
normal! zo
17704
normal! zo
17709
normal! zo
17715
normal! zo
17716
normal! zo
17717
normal! zo
17720
normal! zo
17739
normal! zo
17754
normal! zo
17782
normal! zo
17807
normal! zo
17828
normal! zo
17863
normal! zo
17872
normal! zo
17873
normal! zo
17874
normal! zo
17876
normal! zo
17876
normal! zo
17876
normal! zo
17879
normal! zo
17881
normal! zo
17881
normal! zo
17881
normal! zo
17884
normal! zo
17885
normal! zo
17885
normal! zo
17885
normal! zo
17885
normal! zo
17885
normal! zo
18411
normal! zo
18428
normal! zo
18438
normal! zo
18441
normal! zo
18442
normal! zo
18442
normal! zo
18448
normal! zo
18455
normal! zo
18456
normal! zo
18457
normal! zo
18457
normal! zo
18457
normal! zo
18457
normal! zo
18461
normal! zo
18462
normal! zo
18462
normal! zo
18462
normal! zo
18462
normal! zo
18478
normal! zo
19696
normal! zo
19720
normal! zo
19726
normal! zo
19732
normal! zo
19750
normal! zo
19760
normal! zo
19763
normal! zo
19770
normal! zo
19770
normal! zo
19770
normal! zo
19770
normal! zo
19775
normal! zo
20055
normal! zo
20061
normal! zo
20061
normal! zo
20070
normal! zo
20077
normal! zo
20084
normal! zo
20091
normal! zo
20098
normal! zo
20105
normal! zo
20112
normal! zo
20118
normal! zo
20119
normal! zo
20128
normal! zo
20137
normal! zo
20300
normal! zo
20310
normal! zo
20321
normal! zo
20332
normal! zo
20333
normal! zo
20338
normal! zo
20339
normal! zo
20339
normal! zo
20349
normal! zo
20349
normal! zo
20349
normal! zo
20349
normal! zo
20349
normal! zo
20349
normal! zo
20349
normal! zo
20349
normal! zo
20349
normal! zo
20360
normal! zo
20361
normal! zo
20369
normal! zo
20369
normal! zo
20369
normal! zo
20369
normal! zo
20369
normal! zo
20369
normal! zo
20369
normal! zo
20369
normal! zo
20380
normal! zo
20381
normal! zo
20437
normal! zo
20458
normal! zo
20463
normal! zo
20475
normal! zo
20475
normal! zo
20475
normal! zo
20475
normal! zo
20475
normal! zo
20475
normal! zo
20475
normal! zo
20493
normal! zo
let s:l = 16900 - ((14 * winheight(0) + 10) / 21)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16900
normal! 043|
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
let s:l = 20 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
20
normal! 09|
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
let s:l = 314 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
314
normal! 017|
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
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_balas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
108
normal! zo
3524
normal! zo
3536
normal! zo
3553
normal! zo
3562
normal! zo
let s:l = 3592 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3592
normal! 021|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/clientes.py
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
let s:l = 1741 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1741
normal! 05|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/facturas_compra.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
76
normal! zo
let s:l = 1753 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1753
normal! 05|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_producido.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
57
normal! zo
58
normal! zo
136
normal! zo
149
normal! zo
168
normal! zo
241
normal! zo
260
normal! zo
263
normal! zo
269
normal! zo
397
normal! zo
400
normal! zo
404
normal! zo
410
normal! zo
418
normal! zo
419
normal! zo
426
normal! zo
428
normal! zo
428
normal! zo
428
normal! zo
428
normal! zo
428
normal! zo
442
normal! zo
452
normal! zo
455
normal! zo
457
normal! zo
460
normal! zo
467
normal! zo
475
normal! zo
477
normal! zo
477
normal! zo
477
normal! zo
477
normal! zo
483
normal! zo
490
normal! zo
500
normal! zo
503
normal! zo
512
normal! zo
518
normal! zo
519
normal! zo
519
normal! zo
519
normal! zo
519
normal! zo
519
normal! zo
532
normal! zo
534
normal! zo
534
normal! zo
534
normal! zo
534
normal! zo
540
normal! zo
546
normal! zo
556
normal! zo
566
normal! zo
567
normal! zo
581
normal! zo
let s:l = 562 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
562
normal! 017|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_productividad.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
53
normal! zo
57
normal! zo
73
normal! zo
73
normal! zo
153
normal! zo
212
normal! zo
253
normal! zo
254
normal! zo
385
normal! zo
398
normal! zo
417
normal! zo
417
normal! zo
417
normal! zo
417
normal! zo
430
normal! zo
482
normal! zo
492
normal! zo
504
normal! zo
let s:l = 170 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
170
normal! 09|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/presupuestos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
68
normal! zo
69
normal! zo
77
normal! zo
77
normal! zo
77
normal! zo
77
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
224
normal! zo
230
normal! zo
271
normal! zo
288
normal! zo
384
normal! zo
405
normal! zo
414
normal! zo
460
normal! zo
471
normal! zo
480
normal! zo
1133
normal! zo
1140
normal! zo
1142
normal! zo
1200
normal! zo
1234
normal! zo
1573
normal! zo
1720
normal! zo
1729
normal! zo
1730
normal! zo
1768
normal! zo
1842
normal! zo
1848
normal! zo
1849
normal! zo
1897
normal! zo
1899
normal! zo
1905
normal! zo
1910
normal! zo
1915
normal! zo
1915
normal! zo
2105
normal! zo
2114
normal! zo
2114
normal! zo
2114
normal! zo
2114
normal! zo
2114
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2151
normal! zo
2227
normal! zo
2239
normal! zo
2240
normal! zo
2258
normal! zo
2259
normal! zo
2264
normal! zo
2264
normal! zo
2300
normal! zo
2312
normal! zo
2313
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2314
normal! zo
2392
normal! zo
2406
normal! zo
2406
normal! zo
2406
normal! zo
2406
normal! zo
2406
normal! zo
2406
normal! zo
2407
normal! zo
2411
normal! zo
2419
normal! zo
2430
normal! zo
2431
normal! zo
2431
normal! zo
2431
normal! zo
2431
normal! zo
2447
normal! zo
2447
normal! zo
2473
normal! zo
2474
normal! zo
2475
normal! zo
2487
normal! zo
2503
normal! zo
2505
normal! zo
2520
normal! zo
2552
normal! zo
2553
normal! zo
2553
normal! zo
2554
normal! zo
2560
normal! zo
3001
normal! zo
3003
normal! zo
3043
normal! zo
let s:l = 1208 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1208
normal! 033|
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
let s:l = 525 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
525
normal! 0
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 21 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
exe '9resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 9resize ' . ((&columns * 80 + 51) / 102)
exe '10resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 10resize ' . ((&columns * 80 + 51) / 102)
exe '11resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 11resize ' . ((&columns * 80 + 51) / 102)
exe '12resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 12resize ' . ((&columns * 80 + 51) / 102)
exe '13resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 13resize ' . ((&columns * 80 + 51) / 102)
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
3wincmd w

" vim: ft=vim ro nowrap smc=128
