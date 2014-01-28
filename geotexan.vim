" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 28 enero 2014 at 17:49:41.
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
badd +260 ginn/formularios/consulta_producido.py
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
badd +1260 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +750 ginn/formularios/ventana.py
badd +992 ginn/formularios/pedidos_de_venta.py
badd +1559 db/tablas.sql
badd +799 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +1 ginn/formularios/presupuestos.py
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
badd +65 ginn/formularios/consulta_albaranesPorFacturar.py
badd +1 ginn/formularios/checklist_window.py
args formularios/auditviewer.py
set lines=45 columns=102
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
9wincmd k
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
exe '3resize ' . ((&lines * 1 + 22) / 45)
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
exe '9resize ' . ((&lines * 25 + 22) / 45)
exe 'vert 9resize ' . ((&columns * 80 + 51) / 102)
exe '10resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 10resize ' . ((&columns * 80 + 51) / 102)
exe '11resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 11resize ' . ((&columns * 80 + 51) / 102)
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
let s:l = 3168 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3168
normal! 025|
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
4030
normal! zo
4030
normal! zo
4053
normal! zo
4080
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
5217
normal! zo
5239
normal! zo
5239
normal! zo
5239
normal! zo
5239
normal! zo
5239
normal! zo
5335
normal! zo
5341
normal! zo
5365
normal! zo
5450
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
9005
normal! zo
9058
normal! zo
9750
normal! zo
9765
normal! zo
9805
normal! zo
9858
normal! zo
9861
normal! zo
9865
normal! zo
9865
normal! zo
9865
normal! zo
9881
normal! zo
10014
normal! zo
10254
normal! zo
10378
normal! zo
10385
normal! zo
10386
normal! zo
10391
normal! zo
10398
normal! zo
10399
normal! zo
10412
normal! zo
10561
normal! zo
10564
normal! zo
10567
normal! zo
10567
normal! zo
10567
normal! zo
10590
normal! zo
10608
normal! zo
10624
normal! zo
10824
normal! zo
11079
normal! zo
11105
normal! zo
11165
normal! zo
11410
normal! zo
11444
normal! zo
11444
normal! zo
11444
normal! zo
11444
normal! zo
11444
normal! zo
11457
normal! zo
11466
normal! zo
11466
normal! zo
11466
normal! zo
11466
normal! zo
11466
normal! zo
11494
normal! zo
11982
normal! zo
11982
normal! zo
11982
normal! zo
13419
normal! zo
13419
normal! zo
13419
normal! zo
13434
normal! zo
13435
normal! zo
13589
normal! zo
13589
normal! zo
13589
normal! zo
13615
normal! zo
13616
normal! zo
13720
normal! zo
13720
normal! zo
13720
normal! zo
13736
normal! zo
13737
normal! zo
13854
normal! zo
13860
normal! zo
13860
normal! zo
14189
normal! zo
14190
normal! zo
14190
normal! zo
14326
normal! zo
14367
normal! zo
14641
normal! zo
14683
normal! zo
15069
normal! zo
15071
normal! zo
15075
normal! zo
15102
normal! zo
15434
normal! zo
15706
normal! zo
16308
normal! zo
16405
normal! zo
16420
normal! zo
16431
normal! zo
16431
normal! zo
16478
normal! zo
16511
normal! zo
16702
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
16716
normal! zo
16717
normal! zo
16718
normal! zo
16719
normal! zo
16723
normal! zo
16724
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16725
normal! zo
16727
normal! zo
16729
normal! zo
16734
normal! zo
16734
normal! zo
16734
normal! zo
16734
normal! zo
16740
normal! zo
17067
normal! zo
17091
normal! zo
17096
normal! zo
17098
normal! zo
17101
normal! zo
17108
normal! zo
17120
normal! zo
17130
normal! zo
17130
normal! zo
17130
normal! zo
17130
normal! zo
17130
normal! zo
17130
normal! zo
17455
normal! zo
17465
normal! zo
17485
normal! zo
17561
normal! zo
17601
normal! zo
17621
normal! zo
17636
normal! zo
17643
normal! zo
17646
normal! zo
18387
normal! zo
19655
normal! zo
19667
normal! zo
19672
normal! zo
20014
normal! zo
20020
normal! zo
20020
normal! zo
20043
normal! zo
20057
normal! zo
20064
normal! zo
20071
normal! zo
20077
normal! zo
20078
normal! zo
20087
normal! zo
20096
normal! zo
20259
normal! zo
20308
normal! zo
20308
normal! zo
20308
normal! zo
20308
normal! zo
20308
normal! zo
20308
normal! zo
20308
normal! zo
20308
normal! zo
20308
normal! zo
20319
normal! zo
20320
normal! zo
20328
normal! zo
20328
normal! zo
20328
normal! zo
20328
normal! zo
20328
normal! zo
20328
normal! zo
20328
normal! zo
20328
normal! zo
20339
normal! zo
20340
normal! zo
20363
normal! zo
20417
normal! zo
20422
normal! zo
20434
normal! zo
20434
normal! zo
20434
normal! zo
20434
normal! zo
20434
normal! zo
20434
normal! zo
20434
normal! zo
20452
normal! zo
let s:l = 5986 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5986
normal! 05|
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
let s:l = 3586 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3586
normal! 021|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_albaranesPorFacturar.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
52
normal! zo
57
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
178
normal! zo
193
normal! zo
204
normal! zo
213
normal! zo
214
normal! zo
325
normal! zo
336
normal! zo
339
normal! zo
340
normal! zo
343
normal! zo
343
normal! zo
344
normal! zo
344
normal! zo
347
normal! zo
348
normal! zo
348
normal! zo
349
normal! zo
349
normal! zo
352
normal! zo
352
normal! zo
353
normal! zo
353
normal! zo
358
normal! zo
360
normal! zo
361
normal! zo
365
normal! zo
366
normal! zo
369
normal! zo
372
normal! zo
373
normal! zo
374
normal! zo
377
normal! zo
378
normal! zo
382
normal! zo
385
normal! zo
385
normal! zo
385
normal! zo
385
normal! zo
389
normal! zo
392
normal! zo
392
normal! zo
392
normal! zo
392
normal! zo
403
normal! zo
409
normal! zo
410
normal! zo
412
normal! zo
413
normal! zo
let s:l = 394 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
394
normal! 034|
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
56
normal! zo
57
normal! zo
70
normal! zo
70
normal! zo
90
normal! zo
127
normal! zo
136
normal! zo
141
normal! zo
143
normal! zo
143
normal! zo
143
normal! zo
143
normal! zo
143
normal! zo
150
normal! zo
156
normal! zo
156
normal! zo
156
normal! zo
204
normal! zo
212
normal! zo
223
normal! zo
226
normal! zo
246
normal! zo
254
normal! zo
254
normal! zo
254
normal! zo
254
normal! zo
270
normal! zo
278
normal! zo
278
normal! zo
278
normal! zo
278
normal! zo
291
normal! zo
291
normal! zo
294
normal! zo
302
normal! zo
302
normal! zo
302
normal! zo
302
normal! zo
340
normal! zo
341
normal! zo
345
normal! zo
346
normal! zo
346
normal! zo
346
normal! zo
351
normal! zo
357
normal! zo
358
normal! zo
362
normal! zo
363
normal! zo
363
normal! zo
363
normal! zo
363
normal! zo
363
normal! zo
377
normal! zo
378
normal! zo
380
normal! zo
382
normal! zo
387
normal! zo
393
normal! zo
394
normal! zo
394
normal! zo
394
normal! zo
394
normal! zo
400
normal! zo
407
normal! zo
416
normal! zo
417
normal! zo
434
normal! zo
435
normal! zo
435
normal! zo
435
normal! zo
435
normal! zo
441
normal! zo
475
normal! zo
498
normal! zo
504
normal! zo
513
normal! zo
513
normal! zo
620
normal! zo
let s:l = 153 - ((12 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
153
normal! 0155|
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
let s:l = 1236 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1236
normal! 037|
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
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 1 + 22) / 45)
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
exe '9resize ' . ((&lines * 25 + 22) / 45)
exe 'vert 9resize ' . ((&columns * 80 + 51) / 102)
exe '10resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 10resize ' . ((&columns * 80 + 51) / 102)
exe '11resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 11resize ' . ((&columns * 80 + 51) / 102)
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
