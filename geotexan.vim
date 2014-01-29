" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 29 enero 2014 at 17:37:43.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 11
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
badd +869 ginn/formularios/partes_de_fabricacion_bolsas.py
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
badd +366 ginn/formularios/horas_trabajadas.py
badd +533 ginn/formularios/horas_trabajadas_dia.py
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
badd +1088 ginn/formularios/abonos_venta.py
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
set lines=57 columns=102
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
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 8 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
exe '9resize ' . ((&lines * 10 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 80 + 51) / 102)
exe '10resize ' . ((&lines * 19 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 80 + 51) / 102)
exe '11resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 11resize ' . ((&columns * 80 + 51) / 102)
exe '12resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 12resize ' . ((&columns * 80 + 51) / 102)
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
3754
normal! zo
3792
normal! zo
3844
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
4034
normal! zo
4034
normal! zo
4057
normal! zo
4084
normal! zo
4099
normal! zo
4166
normal! zo
4483
normal! zo
4509
normal! zo
4579
normal! zo
4809
normal! zo
5138
normal! zo
5225
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
5309
normal! zo
5343
normal! zo
5349
normal! zo
5373
normal! zo
5462
normal! zo
5859
normal! zo
6025
normal! zo
6158
normal! zo
6329
normal! zo
6500
normal! zo
6878
normal! zo
7406
normal! zo
7540
normal! zo
7593
normal! zo
7662
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
7811
normal! zo
7812
normal! zo
7813
normal! zo
7821
normal! zo
7836
normal! zo
7837
normal! zo
7846
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
7929
normal! zo
7947
normal! zo
7949
normal! zo
7957
normal! zo
7958
normal! zo
7964
normal! zo
7976
normal! zo
7977
normal! zo
7986
normal! zo
7998
normal! zo
8000
normal! zo
8283
normal! zo
9017
normal! zo
9070
normal! zo
9762
normal! zo
9777
normal! zo
9817
normal! zo
9870
normal! zo
9873
normal! zo
9877
normal! zo
9877
normal! zo
9877
normal! zo
9893
normal! zo
10026
normal! zo
10266
normal! zo
10390
normal! zo
10397
normal! zo
10398
normal! zo
10403
normal! zo
10410
normal! zo
10411
normal! zo
10424
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
10602
normal! zo
10620
normal! zo
10636
normal! zo
10836
normal! zo
11091
normal! zo
11117
normal! zo
11177
normal! zo
11422
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
11994
normal! zo
11994
normal! zo
11994
normal! zo
13431
normal! zo
13431
normal! zo
13431
normal! zo
13446
normal! zo
13447
normal! zo
13601
normal! zo
13601
normal! zo
13601
normal! zo
13627
normal! zo
13628
normal! zo
13732
normal! zo
13732
normal! zo
13732
normal! zo
13748
normal! zo
13749
normal! zo
13866
normal! zo
13872
normal! zo
13872
normal! zo
14201
normal! zo
14202
normal! zo
14202
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
14361
normal! zo
14383
normal! zo
14402
normal! zo
14676
normal! zo
14718
normal! zo
15104
normal! zo
15106
normal! zo
15110
normal! zo
15137
normal! zo
15469
normal! zo
15741
normal! zo
15907
normal! zo
16347
normal! zo
16444
normal! zo
16459
normal! zo
16470
normal! zo
16470
normal! zo
16517
normal! zo
16550
normal! zo
16741
normal! zo
16752
normal! zo
16752
normal! zo
16752
normal! zo
16752
normal! zo
16754
normal! zo
16755
normal! zo
16756
normal! zo
16757
normal! zo
16758
normal! zo
16762
normal! zo
16763
normal! zo
16764
normal! zo
16764
normal! zo
16764
normal! zo
16764
normal! zo
16764
normal! zo
16764
normal! zo
16764
normal! zo
16766
normal! zo
16768
normal! zo
16773
normal! zo
16773
normal! zo
16773
normal! zo
16773
normal! zo
16779
normal! zo
17106
normal! zo
17130
normal! zo
17135
normal! zo
17137
normal! zo
17140
normal! zo
17147
normal! zo
17159
normal! zo
17169
normal! zo
17169
normal! zo
17169
normal! zo
17169
normal! zo
17169
normal! zo
17169
normal! zo
17494
normal! zo
17504
normal! zo
17524
normal! zo
17600
normal! zo
17640
normal! zo
17660
normal! zo
17675
normal! zo
17682
normal! zo
17685
normal! zo
18426
normal! zo
19694
normal! zo
19706
normal! zo
19711
normal! zo
20053
normal! zo
20059
normal! zo
20059
normal! zo
20082
normal! zo
20096
normal! zo
20103
normal! zo
20110
normal! zo
20116
normal! zo
20117
normal! zo
20126
normal! zo
20135
normal! zo
20298
normal! zo
20347
normal! zo
20347
normal! zo
20347
normal! zo
20347
normal! zo
20347
normal! zo
20347
normal! zo
20347
normal! zo
20347
normal! zo
20347
normal! zo
20358
normal! zo
20359
normal! zo
20367
normal! zo
20367
normal! zo
20367
normal! zo
20367
normal! zo
20367
normal! zo
20367
normal! zo
20367
normal! zo
20367
normal! zo
20378
normal! zo
20379
normal! zo
20402
normal! zo
20456
normal! zo
20461
normal! zo
20473
normal! zo
20473
normal! zo
20473
normal! zo
20473
normal! zo
20473
normal! zo
20473
normal! zo
20473
normal! zo
20491
normal! zo
let s:l = 9766 - ((1 * winheight(0) + 4) / 8)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9766
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
edit ~/Geotexan/src/Geotex-INN/ginn/informes/geninformes.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
9527
normal! zo
9534
normal! zo
let s:l = 9539 - ((7 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9539
normal! 071|
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
71
normal! zo
71
normal! zo
91
normal! zo
104
normal! zo
132
normal! zo
145
normal! zo
152
normal! zo
154
normal! zo
154
normal! zo
154
normal! zo
154
normal! zo
154
normal! zo
161
normal! zo
166
normal! zo
173
normal! zo
174
normal! zo
179
normal! zo
179
normal! zo
179
normal! zo
228
normal! zo
236
normal! zo
247
normal! zo
250
normal! zo
256
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
315
normal! zo
315
normal! zo
318
normal! zo
319
normal! zo
319
normal! zo
319
normal! zo
319
normal! zo
326
normal! zo
326
normal! zo
326
normal! zo
326
normal! zo
339
normal! zo
339
normal! zo
361
normal! zo
361
normal! zo
362
normal! zo
364
normal! zo
371
normal! zo
372
normal! zo
376
normal! zo
377
normal! zo
377
normal! zo
377
normal! zo
382
normal! zo
390
normal! zo
391
normal! zo
397
normal! zo
399
normal! zo
399
normal! zo
399
normal! zo
399
normal! zo
399
normal! zo
414
normal! zo
415
normal! zo
417
normal! zo
420
normal! zo
427
normal! zo
433
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
449
normal! zo
450
normal! zo
459
normal! zo
465
normal! zo
466
normal! zo
466
normal! zo
466
normal! zo
466
normal! zo
466
normal! zo
478
normal! zo
480
normal! zo
480
normal! zo
480
normal! zo
480
normal! zo
486
normal! zo
492
normal! zo
502
normal! zo
503
normal! zo
504
normal! zo
504
normal! zo
504
normal! zo
504
normal! zo
506
normal! zo
508
normal! zo
522
normal! zo
523
normal! zo
523
normal! zo
532
normal! zo
555
normal! zo
561
normal! zo
563
normal! zo
569
normal! zo
573
normal! zo
573
normal! zo
579
normal! zo
593
normal! zo
600
normal! zo
648
normal! zo
655
normal! zo
656
normal! zo
656
normal! zo
661
normal! zo
665
normal! zo
665
normal! zo
670
normal! zo
674
normal! zo
674
normal! zo
686
normal! zo
687
normal! zo
687
normal! zo
693
normal! zo
let s:l = 673 - ((14 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
673
normal! 055|
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
let s:l = 525 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
525
normal! 0
wincmd w
10wincmd w
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 8 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
exe '9resize ' . ((&lines * 10 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 80 + 51) / 102)
exe '10resize ' . ((&lines * 19 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 80 + 51) / 102)
exe '11resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 11resize ' . ((&columns * 80 + 51) / 102)
exe '12resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 12resize ' . ((&columns * 80 + 51) / 102)
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
10wincmd w

" vim: ft=vim ro nowrap smc=128
