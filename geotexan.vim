" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 24 enero 2014 at 20:57:39.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 13
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
badd +353 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +266 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +3989 ginn/formularios/partes_de_fabricacion_balas.py
badd +580 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1131 ginn/formularios/partes_de_fabricacion_rollos.py
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
badd +1260 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +750 ginn/formularios/ventana.py
badd +2578 ginn/formularios/pedidos_de_venta.py
badd +725 db/tablas.sql
badd +4754 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +2052 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +238 ginn/formularios/facturas_compra.py
badd +4386 ginn/formularios/utils.py
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
args formularios/auditviewer.py
set lines=57 columns=100
edit ginn/formularios/presupuestos.py
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
10wincmd k
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
exe 'vert 1resize ' . ((&columns * 21 + 50) / 100)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 78 + 50) / 100)
exe '3resize ' . ((&lines * 10 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 78 + 50) / 100)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 78 + 50) / 100)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 78 + 50) / 100)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 78 + 50) / 100)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 78 + 50) / 100)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 78 + 50) / 100)
exe '9resize ' . ((&lines * 26 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 78 + 50) / 100)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 78 + 50) / 100)
exe '11resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 11resize ' . ((&columns * 78 + 50) / 100)
exe '12resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 12resize ' . ((&columns * 78 + 50) / 100)
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
let s:l = 3175 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3175
normal! 07|
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
3840
normal! zo
3932
normal! zo
3939
normal! zo
3940
normal! zo
3940
normal! zo
3940
normal! zo
3940
normal! zo
3940
normal! zo
3940
normal! zo
3964
normal! zo
4095
normal! zo
4162
normal! zo
4571
normal! zo
4801
normal! zo
5130
normal! zo
5335
normal! zo
5341
normal! zo
5847
normal! zo
6013
normal! zo
7528
normal! zo
7581
normal! zo
7650
normal! zo
7686
normal! zo
7687
normal! zo
7688
normal! zo
7693
normal! zo
7699
normal! zo
7705
normal! zo
7705
normal! zo
7705
normal! zo
7705
normal! zo
7705
normal! zo
7705
normal! zo
7799
normal! zo
7800
normal! zo
7801
normal! zo
7809
normal! zo
7824
normal! zo
7825
normal! zo
7834
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
7858
normal! zo
7906
normal! zo
7911
normal! zo
7913
normal! zo
7917
normal! zo
7935
normal! zo
7937
normal! zo
7945
normal! zo
7946
normal! zo
7952
normal! zo
7964
normal! zo
7965
normal! zo
7974
normal! zo
7986
normal! zo
7988
normal! zo
8271
normal! zo
9058
normal! zo
9753
normal! zo
9793
normal! zo
9846
normal! zo
9849
normal! zo
9853
normal! zo
9853
normal! zo
9853
normal! zo
9869
normal! zo
10002
normal! zo
10242
normal! zo
10269
normal! zo
10274
normal! zo
10280
normal! zo
10333
normal! zo
10366
normal! zo
10373
normal! zo
10374
normal! zo
10379
normal! zo
10386
normal! zo
10387
normal! zo
10400
normal! zo
10549
normal! zo
10552
normal! zo
10555
normal! zo
10555
normal! zo
10555
normal! zo
10571
normal! zo
10578
normal! zo
10593
normal! zo
10596
normal! zo
10612
normal! zo
10812
normal! zo
11067
normal! zo
11093
normal! zo
11153
normal! zo
11398
normal! zo
11432
normal! zo
11432
normal! zo
11432
normal! zo
11432
normal! zo
11432
normal! zo
11445
normal! zo
11454
normal! zo
11454
normal! zo
11454
normal! zo
11454
normal! zo
11454
normal! zo
11482
normal! zo
11970
normal! zo
11970
normal! zo
11970
normal! zo
13407
normal! zo
13407
normal! zo
13407
normal! zo
13422
normal! zo
13423
normal! zo
13577
normal! zo
13577
normal! zo
13577
normal! zo
13603
normal! zo
13604
normal! zo
13708
normal! zo
13708
normal! zo
13708
normal! zo
13724
normal! zo
13725
normal! zo
13842
normal! zo
13848
normal! zo
13848
normal! zo
14177
normal! zo
14178
normal! zo
14178
normal! zo
14355
normal! zo
14629
normal! zo
14671
normal! zo
15057
normal! zo
15059
normal! zo
15063
normal! zo
15090
normal! zo
15694
normal! zo
16296
normal! zo
16466
normal! zo
16499
normal! zo
16690
normal! zo
16701
normal! zo
16701
normal! zo
16701
normal! zo
16701
normal! zo
16703
normal! zo
16704
normal! zo
16705
normal! zo
16706
normal! zo
16707
normal! zo
16711
normal! zo
16712
normal! zo
16713
normal! zo
16713
normal! zo
16713
normal! zo
16713
normal! zo
16713
normal! zo
16713
normal! zo
16713
normal! zo
16715
normal! zo
16717
normal! zo
16722
normal! zo
16722
normal! zo
16722
normal! zo
16722
normal! zo
16728
normal! zo
17055
normal! zo
17079
normal! zo
17084
normal! zo
17086
normal! zo
17089
normal! zo
17096
normal! zo
17108
normal! zo
17118
normal! zo
17118
normal! zo
17118
normal! zo
17118
normal! zo
17118
normal! zo
17118
normal! zo
17443
normal! zo
17453
normal! zo
17473
normal! zo
17549
normal! zo
17589
normal! zo
17609
normal! zo
17624
normal! zo
17631
normal! zo
17634
normal! zo
18375
normal! zo
19643
normal! zo
19655
normal! zo
19660
normal! zo
20002
normal! zo
20008
normal! zo
20008
normal! zo
20031
normal! zo
20045
normal! zo
20052
normal! zo
20059
normal! zo
20065
normal! zo
20066
normal! zo
20075
normal! zo
20084
normal! zo
20247
normal! zo
20296
normal! zo
20296
normal! zo
20296
normal! zo
20296
normal! zo
20296
normal! zo
20296
normal! zo
20296
normal! zo
20296
normal! zo
20296
normal! zo
20307
normal! zo
20308
normal! zo
20316
normal! zo
20316
normal! zo
20316
normal! zo
20316
normal! zo
20316
normal! zo
20316
normal! zo
20316
normal! zo
20316
normal! zo
20327
normal! zo
20328
normal! zo
20351
normal! zo
20405
normal! zo
20410
normal! zo
20422
normal! zo
20422
normal! zo
20422
normal! zo
20422
normal! zo
20422
normal! zo
20422
normal! zo
20422
normal! zo
20440
normal! zo
let s:l = 10280 - ((6 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10280
normal! 013|
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
1084
normal! zo
1378
normal! zo
1526
normal! zo
1527
normal! zo
1527
normal! zo
1528
normal! zo
1528
normal! zo
let s:l = 1188 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1188
normal! 035|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/utils.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
403
normal! zo
403
normal! zo
403
normal! zo
403
normal! zo
let s:l = 407 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
407
normal! 034|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/albaranes_de_salida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
98
normal! zo
99
normal! zo
111
normal! zo
111
normal! zo
111
normal! zo
1172
normal! zo
1693
normal! zo
1719
normal! zo
2006
normal! zo
2019
normal! zo
2019
normal! zo
2019
normal! zo
2019
normal! zo
2019
normal! zo
2019
normal! zo
2019
normal! zo
2028
normal! zo
2097
normal! zo
2099
normal! zo
2104
normal! zo
2113
normal! zo
2114
normal! zo
2115
normal! zo
2115
normal! zo
2116
normal! zo
2116
normal! zo
2117
normal! zo
2122
normal! zo
2207
normal! zo
2207
normal! zo
2217
normal! zo
2218
normal! zo
2230
normal! zo
2230
normal! zo
2230
normal! zo
2230
normal! zo
2232
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2228
normal! zo
2249
normal! zo
2263
normal! zo
3042
normal! zo
3050
normal! zo
3240
normal! zo
3252
normal! zo
3253
normal! zo
3254
normal! zo
3638
normal! zo
3647
normal! zo
4582
normal! zo
4600
normal! zo
let s:l = 2202 - ((17 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2202
normal! 040|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/pedidos_de_venta.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
121
normal! zo
768
normal! zo
1393
normal! zo
1775
normal! zo
1785
normal! zo
1786
normal! zo
1787
normal! zo
1787
normal! zo
let s:l = 2845 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2845
normal! 05|
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
2227
normal! zo
2239
normal! zo
2258
normal! zo
2259
normal! zo
2264
normal! zo
2264
normal! zo
2267
normal! zo
2268
normal! zo
2392
normal! zo
2411
normal! zo
2419
normal! zo
2487
normal! zo
2503
normal! zo
2505
normal! zo
3001
normal! zo
3003
normal! zo
3043
normal! zo
let s:l = 3175 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3175
normal! 07|
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
let s:l = 523 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
523
normal! 022|
wincmd w
9wincmd w
exe 'vert 1resize ' . ((&columns * 21 + 50) / 100)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 78 + 50) / 100)
exe '3resize ' . ((&lines * 10 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 78 + 50) / 100)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 78 + 50) / 100)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 78 + 50) / 100)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 78 + 50) / 100)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 78 + 50) / 100)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 78 + 50) / 100)
exe '9resize ' . ((&lines * 26 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 78 + 50) / 100)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 78 + 50) / 100)
exe '11resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 11resize ' . ((&columns * 78 + 50) / 100)
exe '12resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 12resize ' . ((&columns * 78 + 50) / 100)
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
9wincmd w

" vim: ft=vim ro nowrap smc=128
