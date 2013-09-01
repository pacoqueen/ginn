" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 01 septiembre 2013 at 20:43:08.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Droid\ Sans\ Mono\ Slashed\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'desert' | colorscheme desert | endif
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
badd +392 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +2198 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +310 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2258 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +903 ginn/formularios/partes_de_fabricacion_balas.py
badd +1957 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +121 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +105 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +11926 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +443 ginn/formularios/facturas_venta.py
badd +479 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +280 ginn/formularios/ventana.py
badd +1851 ginn/formularios/pedidos_de_venta.py
badd +1452 db/tablas.sql
badd +1958 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +9 ginn/formularios/presupuestos.py
badd +382 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +724 ginn/formularios/facturas_compra.py
badd +2443 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +1329 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +46 ginn/formularios/gtkexcepthook.py
badd +664 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +611 ginn/framework/pclases/superfacturaventa.py
badd +4 ginn/framework/pclases/facturaventa.py
badd +689 ginn/formularios/consulta_mensual_nominas.py
badd +269 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +249 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +921 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +221 ginn/formularios/consumo_balas_partida.py
badd +553 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +753 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +628 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +523 ginn/formularios/postomatic.py
badd +20 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +1 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
args formularios/auditviewer.py
set lines=68 columns=111
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
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 26 + 34) / 68)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 5 + 34) / 68)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 6 + 34) / 68)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 5 + 34) / 68)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 6 + 34) / 68)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 5 + 34) / 68)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
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
641
normal! zo
722
normal! zo
2052
normal! zo
2160
normal! zo
2160
normal! zo
2160
normal! zo
2160
normal! zo
2430
normal! zo
6451
normal! zo
6731
normal! zo
6757
normal! zo
6829
normal! zo
6942
normal! zo
7223
normal! zo
7544
normal! zo
8511
normal! zo
8524
normal! zo
8525
normal! zo
8526
normal! zo
9716
normal! zo
9756
normal! zo
9763
normal! zo
9796
normal! zo
9809
normal! zo
9812
normal! zo
9825
normal! zo
9828
normal! zo
9838
normal! zo
9840
normal! zo
9872
normal! zo
10066
normal! zo
10073
normal! zo
10082
normal! zo
10087
normal! zo
10095
normal! zo
10103
normal! zo
10114
normal! zo
10128
normal! zo
10147
normal! zo
10159
normal! zo
10165
normal! zo
10169
normal! zo
10175
normal! zo
10199
normal! zo
10207
normal! zo
10216
normal! zo
10231
normal! zo
10240
normal! zo
10240
normal! zo
10240
normal! zo
10252
normal! zo
10272
normal! zo
10273
normal! zo
10274
normal! zo
10274
normal! zo
10274
normal! zo
10274
normal! zo
10274
normal! zo
10274
normal! zo
10274
normal! zo
10274
normal! zo
10274
normal! zo
10291
normal! zo
10294
normal! zo
10297
normal! zo
10297
normal! zo
10297
normal! zo
10300
normal! zo
10300
normal! zo
10300
normal! zo
10300
normal! zo
10310
normal! zo
10316
normal! zo
10320
normal! zo
10326
normal! zo
10329
normal! zo
10331
normal! zo
10334
normal! zo
10337
normal! zo
10342
normal! zo
10349
normal! zo
10353
normal! zo
10354
normal! zo
10354
normal! zo
10356
normal! zo
10357
normal! zo
10357
normal! zo
10359
normal! zo
10360
normal! zo
10360
normal! zo
10362
normal! zo
10363
normal! zo
10363
normal! zo
10365
normal! zo
10366
normal! zo
10366
normal! zo
10368
normal! zo
10369
normal! zo
10369
normal! zo
10371
normal! zo
10372
normal! zo
10372
normal! zo
10374
normal! zo
10377
normal! zo
10379
normal! zo
10379
normal! zo
10379
normal! zo
10396
normal! zo
10403
normal! zo
10404
normal! zo
10404
normal! zo
10404
normal! zo
10407
normal! zo
10416
normal! zo
10426
normal! zo
10431
normal! zo
10434
normal! zo
14012
normal! zo
14031
normal! zo
14419
normal! zo
15415
normal! zo
15467
normal! zo
15527
normal! zo
15701
normal! zo
15927
normal! zo
16912
normal! zo
17767
normal! zo
18083
normal! zo
18343
normal! zo
19583
normal! zo
let s:l = 10330 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10330
normal! 046|
wincmd w
argglobal
edit db/tablas.sql
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
1391
normal! zo
1619
normal! zo
1675
normal! zo
1726
normal! zo
1753
normal! zo
1789
normal! zo
1820
normal! zo
1983
normal! zo
let s:l = 1415 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1415
normal! 065|
wincmd w
argglobal
edit ginn/informes/presupuesto2.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
294
normal! zo
347
normal! zo
350
normal! zo
351
normal! zo
351
normal! zo
357
normal! zo
357
normal! zo
357
normal! zo
358
normal! zo
358
normal! zo
358
normal! zo
358
normal! zo
364
normal! zo
364
normal! zo
364
normal! zo
364
normal! zo
364
normal! zo
let s:l = 384 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
384
normal! 030|
wincmd w
argglobal
edit ginn/informes/carta_compromiso.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
60
normal! zo
150
normal! zo
170
normal! zo
185
normal! zo
190
normal! zo
279
normal! zo
282
normal! zo
282
normal! zo
293
normal! zo
293
normal! zo
293
normal! zo
293
normal! zo
293
normal! zo
311
normal! zo
314
normal! zo
let s:l = 66 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
66
normal! 0
wincmd w
argglobal
edit ginn/formularios/presupuestos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
59
normal! zo
60
normal! zo
68
normal! zo
68
normal! zo
68
normal! zo
88
normal! zo
88
normal! zo
88
normal! zo
95
normal! zo
96
normal! zo
99
normal! zo
100
normal! zo
104
normal! zo
104
normal! zo
104
normal! zo
104
normal! zo
124
normal! zo
133
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
137
normal! zo
148
normal! zo
152
normal! zo
152
normal! zo
159
normal! zo
159
normal! zo
167
normal! zo
169
normal! zo
170
normal! zo
171
normal! zo
172
normal! zo
190
normal! zo
191
normal! zo
201
normal! zo
212
normal! zo
212
normal! zo
220
normal! zo
221
normal! zo
228
normal! zo
238
normal! zo
238
normal! zo
245
normal! zo
245
normal! zo
245
normal! zo
245
normal! zo
246
normal! zo
246
normal! zo
247
normal! zo
255
normal! zo
255
normal! zo
272
normal! zo
287
normal! zo
289
normal! zo
289
normal! zo
289
normal! zo
289
normal! zo
289
normal! zo
295
normal! zo
304
normal! zo
311
normal! zo
311
normal! zo
312
normal! zo
315
normal! zo
319
normal! zo
320
normal! zo
322
normal! zo
327
normal! zo
329
normal! zo
339
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
341
normal! zo
341
normal! zo
341
normal! zo
341
normal! zo
341
normal! zo
341
normal! zo
355
normal! zo
360
normal! zo
360
normal! zo
361
normal! zo
366
normal! zo
397
normal! zo
402
normal! zo
403
normal! zo
403
normal! zo
404
normal! zo
404
normal! zo
405
normal! zo
406
normal! zo
411
normal! zo
415
normal! zo
418
normal! zo
419
normal! zo
419
normal! zo
420
normal! zo
424
normal! zo
425
normal! zo
426
normal! zo
433
normal! zo
434
normal! zo
435
normal! zo
447
normal! zo
447
normal! zo
447
normal! zo
447
normal! zo
447
normal! zo
449
normal! zo
450
normal! zo
451
normal! zo
460
normal! zo
460
normal! zo
460
normal! zo
460
normal! zo
460
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
477
normal! zo
478
normal! zo
481
normal! zo
482
normal! zo
490
normal! zo
491
normal! zo
500
normal! zo
504
normal! zo
519
normal! zo
524
normal! zo
547
normal! zo
578
normal! zo
578
normal! zo
578
normal! zo
578
normal! zo
578
normal! zo
578
normal! zo
578
normal! zo
587
normal! zo
596
normal! zo
603
normal! zo
603
normal! zo
604
normal! zo
608
normal! zo
609
normal! zo
614
normal! zo
616
normal! zo
621
normal! zo
622
normal! zo
623
normal! zo
623
normal! zo
626
normal! zo
627
normal! zo
627
normal! zo
627
normal! zo
627
normal! zo
627
normal! zo
627
normal! zo
627
normal! zo
627
normal! zo
627
normal! zo
641
normal! zo
645
normal! zo
651
normal! zo
651
normal! zo
651
normal! zo
651
normal! zo
651
normal! zo
651
normal! zo
651
normal! zo
651
normal! zo
651
normal! zo
655
normal! zo
656
normal! zo
664
normal! zo
670
normal! zo
674
normal! zo
681
normal! zo
683
normal! zo
685
normal! zo
686
normal! zo
686
normal! zo
686
normal! zo
686
normal! zo
686
normal! zo
686
normal! zo
686
normal! zo
691
normal! zo
713
normal! zo
730
normal! zo
730
normal! zo
740
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
774
normal! zo
774
normal! zo
774
normal! zo
774
normal! zo
774
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
783
normal! zo
790
normal! zo
793
normal! zo
799
normal! zo
800
normal! zo
809
normal! zo
817
normal! zo
828
normal! zo
832
normal! zo
845
normal! zo
856
normal! zo
866
normal! zo
877
normal! zo
881
normal! zo
884
normal! zo
886
normal! zo
886
normal! zo
887
normal! zo
887
normal! zo
889
normal! zo
891
normal! zo
891
normal! zo
891
normal! zo
893
normal! zo
893
normal! zo
893
normal! zo
895
normal! zo
895
normal! zo
895
normal! zo
907
normal! zo
924
normal! zo
924
normal! zo
949
normal! zo
951
normal! zo
951
normal! zo
955
normal! zo
966
normal! zo
975
normal! zo
976
normal! zo
981
normal! zo
988
normal! zo
993
normal! zo
993
normal! zo
993
normal! zo
993
normal! zo
993
normal! zo
995
normal! zo
995
normal! zo
1009
normal! zo
1017
normal! zo
1030
normal! zo
1030
normal! zo
1030
normal! zo
1030
normal! zo
1035
normal! zo
1042
normal! zo
1051
normal! zo
1057
normal! zo
1072
normal! zo
1075
normal! zo
1082
normal! zo
1094
normal! zo
1097
normal! zo
1097
normal! zo
1097
normal! zo
1099
normal! zo
1100
normal! zo
1101
normal! zo
1103
normal! zo
1103
normal! zo
1103
normal! zo
1103
normal! zo
1106
normal! zo
1106
normal! zo
1107
normal! zo
1109
normal! zo
1111
normal! zo
1111
normal! zo
1113
normal! zo
1114
normal! zo
1114
normal! zo
1148
normal! zo
1150
normal! zo
1153
normal! zo
1155
normal! zo
1172
normal! zo
1175
normal! zo
1190
normal! zo
1196
normal! zo
1199
normal! zo
1199
normal! zo
1208
normal! zo
1221
normal! zo
1245
normal! zo
1245
normal! zo
1245
normal! zo
1254
normal! zo
1265
normal! zo
1265
normal! zo
1265
normal! zo
1265
normal! zo
1265
normal! zo
1265
normal! zo
1265
normal! zo
1268
normal! zo
1268
normal! zo
1268
normal! zo
1268
normal! zo
1268
normal! zo
1268
normal! zo
1269
normal! zo
1273
normal! zo
1281
normal! zo
1289
normal! zo
1292
normal! zo
1293
normal! zo
1293
normal! zo
1293
normal! zo
1293
normal! zo
1295
normal! zo
1295
normal! zo
1295
normal! zo
1295
normal! zo
1295
normal! zo
1295
normal! zo
1297
normal! zo
1301
normal! zo
1307
normal! zo
1307
normal! zo
1328
normal! zo
1340
normal! zo
1352
normal! zo
1354
normal! zo
1356
normal! zo
1369
normal! zo
1372
normal! zo
1406
normal! zo
1411
normal! zo
1427
normal! zo
1427
normal! zo
1428
normal! zo
1431
normal! zo
1431
normal! zo
1439
normal! zo
1448
normal! zo
1455
normal! zo
1465
normal! zo
1466
normal! zo
1469
normal! zo
1470
normal! zo
1470
normal! zo
1471
normal! zo
1471
normal! zo
1471
normal! zo
1471
normal! zo
1471
normal! zo
1471
normal! zo
1471
normal! zo
1477
normal! zo
1479
normal! zo
1482
normal! zo
1482
normal! zo
1482
normal! zo
1482
normal! zo
1492
normal! zo
1493
normal! zo
1498
normal! zo
1498
normal! zo
1504
normal! zo
1513
normal! zo
1516
normal! zo
1519
normal! zo
1529
normal! zo
let s:l = 1413 - ((23 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1413
normal! 040|
wincmd w
argglobal
edit ginn/formularios/consulta_cobros.py
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
299
normal! zo
301
normal! zo
302
normal! zo
302
normal! zo
302
normal! zo
302
normal! zo
302
normal! zo
306
normal! zo
308
normal! zo
309
normal! zo
309
normal! zo
309
normal! zo
309
normal! zo
309
normal! zo
322
normal! zo
327
normal! zo
335
normal! zo
336
normal! zo
336
normal! zo
let s:l = 318 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
318
normal! 018|
wincmd w
argglobal
edit ginn/formularios/ventana.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit ginn/framework/configuracion.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
415
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
let s:l = 422 - ((3 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
422
normal! 075|
wincmd w
argglobal
edit ginn/formularios/launcher.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
34
normal! zo
51
normal! zo
66
normal! zo
70
normal! zo
95
normal! zo
106
normal! zo
let s:l = 111 - ((2 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
111
normal! 041|
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_rollos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
229
normal! zo
230
normal! zo
262
normal! zo
262
normal! zo
339
normal! zo
340
normal! zo
345
normal! zo
350
normal! zo
351
normal! zo
356
normal! zo
362
normal! zo
467
normal! zo
579
normal! zo
595
normal! zo
725
normal! zo
734
normal! zo
834
normal! zo
850
normal! zo
850
normal! zo
850
normal! zo
850
normal! zo
961
normal! zo
966
normal! zo
1531
normal! zo
1727
normal! zo
1728
normal! zo
1728
normal! zo
1728
normal! zo
1728
normal! zo
1739
normal! zo
1740
normal! zo
1744
normal! zo
1744
normal! zo
1745
normal! zo
1752
normal! zo
1753
normal! zo
1804
normal! zo
3253
normal! zo
3260
normal! zo
3265
normal! zo
3272
normal! zo
3276
normal! zo
3281
normal! zo
3282
normal! zo
3282
normal! zo
3282
normal! zo
3288
normal! zo
3293
normal! zo
3294
normal! zo
3299
normal! zo
let s:l = 1753 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1753
normal! 037|
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 34) / 68)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 26 + 34) / 68)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 5 + 34) / 68)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 6 + 34) / 68)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 5 + 34) / 68)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 6 + 34) / 68)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 5 + 34) / 68)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
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
6wincmd w

" vim: ft=vim ro nowrap smc=128
