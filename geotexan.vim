" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 10 septiembre 2013 at 22:21:44.
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
badd +592 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +310 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2258 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1526 ginn/formularios/partes_de_fabricacion_balas.py
badd +1957 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1406 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +105 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +3614 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2958 ginn/formularios/facturas_venta.py
badd +417 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +292 ginn/formularios/ventana.py
badd +1858 ginn/formularios/pedidos_de_venta.py
badd +1431 db/tablas.sql
badd +810 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +1350 ginn/formularios/presupuestos.py
badd +1 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +724 ginn/formularios/facturas_compra.py
badd +4107 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +1329 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +46 ginn/formularios/gtkexcepthook.py
badd +476 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +611 ginn/framework/pclases/superfacturaventa.py
badd +47 ginn/framework/pclases/facturaventa.py
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
badd +511 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +628 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +523 ginn/formularios/postomatic.py
badd +36 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +431 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
args formularios/auditviewer.py
set lines=69 columns=111
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
8wincmd k
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
exe '2resize ' . ((&lines * 7 + 34) / 69)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 6 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 7 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 34 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
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
270
normal! zo
436
normal! zo
641
normal! zo
2053
normal! zo
2064
normal! zo
2064
normal! zo
2064
normal! zo
2064
normal! zo
2064
normal! zo
2064
normal! zo
2229
normal! zo
2250
normal! zo
2292
normal! zo
4726
normal! zo
4739
normal! zo
4745
normal! zo
9718
normal! zo
9734
normal! zo
10149
normal! zo
10199
normal! zo
10199
normal! zo
10199
normal! zo
10199
normal! zo
10199
normal! zo
10325
normal! zo
10328
normal! zo
10339
normal! zo
10339
normal! zo
10339
normal! zo
10348
normal! zo
10356
normal! zo
10372
normal! zo
15068
normal! zo
17890
normal! zo
19417
normal! zo
19439
normal! zo
19473
normal! zo
19505
normal! zo
19821
normal! zo
19839
normal! zo
19844
normal! zo
19844
normal! zo
19844
normal! zo
let s:l = 10146 - ((3 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10146
normal! 040|
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
let s:l = 352 - ((0 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
352
normal! 025|
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
60
normal! zo
61
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
72
normal! zo
83
normal! zo
88
normal! zo
92
normal! zo
93
normal! zo
93
normal! zo
105
normal! zo
110
normal! zo
110
normal! zo
112
normal! zo
112
normal! zo
112
normal! zo
158
normal! zo
171
normal! zo
184
normal! zo
203
normal! zo
213
normal! zo
240
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
312
normal! zo
348
normal! zo
376
normal! zo
376
normal! zo
376
normal! zo
379
normal! zo
382
normal! zo
383
normal! zo
383
normal! zo
389
normal! zo
389
normal! zo
389
normal! zo
390
normal! zo
390
normal! zo
390
normal! zo
390
normal! zo
396
normal! zo
396
normal! zo
396
normal! zo
396
normal! zo
396
normal! zo
402
normal! zo
404
normal! zo
404
normal! zo
404
normal! zo
404
normal! zo
406
normal! zo
406
normal! zo
406
normal! zo
406
normal! zo
417
normal! zo
420
normal! zo
433
normal! zo
449
normal! zo
458
normal! zo
459
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
464
normal! zo
467
normal! zo
469
normal! zo
471
normal! zo
474
normal! zo
486
normal! zo
511
normal! zo
528
normal! zo
529
normal! zo
529
normal! zo
529
normal! zo
568
normal! zo
571
normal! zo
let s:l = 112 - ((0 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
112
normal! 053|
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
58
normal! zo
59
normal! zo
67
normal! zo
67
normal! zo
67
normal! zo
89
normal! zo
89
normal! zo
89
normal! zo
138
normal! zo
147
normal! zo
156
normal! zo
181
normal! zo
183
normal! zo
184
normal! zo
185
normal! zo
204
normal! zo
236
normal! zo
288
normal! zo
303
normal! zo
311
normal! zo
333
normal! zo
394
normal! zo
426
normal! zo
431
normal! zo
432
normal! zo
432
normal! zo
444
normal! zo
447
normal! zo
448
normal! zo
448
normal! zo
453
normal! zo
454
normal! zo
462
normal! zo
465
normal! zo
472
normal! zo
505
normal! zo
507
normal! zo
513
normal! zo
519
normal! zo
523
normal! zo
523
normal! zo
523
normal! zo
523
normal! zo
523
normal! zo
523
normal! zo
546
normal! zo
560
normal! zo
564
normal! zo
565
normal! zo
565
normal! zo
566
normal! zo
566
normal! zo
567
normal! zo
568
normal! zo
581
normal! zo
581
normal! zo
581
normal! zo
581
normal! zo
581
normal! zo
585
normal! zo
600
normal! zo
605
normal! zo
677
normal! zo
684
normal! zo
689
normal! zo
690
normal! zo
695
normal! zo
697
normal! zo
755
normal! zo
762
normal! zo
764
normal! zo
766
normal! zo
767
normal! zo
767
normal! zo
767
normal! zo
767
normal! zo
767
normal! zo
767
normal! zo
767
normal! zo
783
normal! zo
794
normal! zo
800
normal! zo
800
normal! zo
800
normal! zo
800
normal! zo
800
normal! zo
800
normal! zo
800
normal! zo
800
normal! zo
813
normal! zo
813
normal! zo
874
normal! zo
877
normal! zo
899
normal! zo
905
normal! zo
906
normal! zo
911
normal! zo
920
normal! zo
926
normal! zo
928
normal! zo
935
normal! zo
935
normal! zo
935
normal! zo
935
normal! zo
935
normal! zo
935
normal! zo
1074
normal! zo
1082
normal! zo
1091
normal! zo
1091
normal! zo
1094
normal! zo
1097
normal! zo
1104
normal! zo
1104
normal! zo
1104
normal! zo
1104
normal! zo
1104
normal! zo
1112
normal! zo
1116
normal! zo
1120
normal! zo
1126
normal! zo
1127
normal! zo
1127
normal! zo
1127
normal! zo
1127
normal! zo
1127
normal! zo
1129
normal! zo
1131
normal! zo
1132
normal! zo
1141
normal! zo
1141
normal! zo
1141
normal! zo
1143
normal! zo
1143
normal! zo
1143
normal! zo
1149
normal! zo
1149
normal! zo
1149
normal! zo
1149
normal! zo
1155
normal! zo
1156
normal! zo
1158
normal! zo
1158
normal! zo
1162
normal! zo
1167
normal! zo
1174
normal! zo
1187
normal! zo
1210
normal! zo
1232
normal! zo
1240
normal! zo
1240
normal! zo
1254
normal! zo
1254
normal! zo
1254
normal! zo
1254
normal! zo
1276
normal! zo
1279
normal! zo
1282
normal! zo
1289
normal! zo
1290
normal! zo
1290
normal! zo
1290
normal! zo
1290
normal! zo
1303
normal! zo
1303
normal! zo
1303
normal! zo
1303
normal! zo
1306
normal! zo
1310
normal! zo
1311
normal! zo
1311
normal! zo
1312
normal! zo
1312
normal! zo
1312
normal! zo
1312
normal! zo
1312
normal! zo
1312
normal! zo
1312
normal! zo
1315
normal! zo
1317
normal! zo
1320
normal! zo
1320
normal! zo
1320
normal! zo
1320
normal! zo
1326
normal! zo
1327
normal! zo
1327
normal! zo
1340
normal! zo
1341
normal! zo
1364
normal! zo
1381
normal! zo
1382
normal! zo
1391
normal! zo
1439
normal! zo
1463
normal! zo
1466
normal! zo
1481
normal! zo
1487
normal! zo
1499
normal! zo
1545
normal! zo
1556
normal! zo
1556
normal! zo
1556
normal! zo
1556
normal! zo
1556
normal! zo
1556
normal! zo
1556
normal! zo
1559
normal! zo
1559
normal! zo
1559
normal! zo
1559
normal! zo
1559
normal! zo
1559
normal! zo
1560
normal! zo
1564
normal! zo
1572
normal! zo
1588
normal! zo
1608
normal! zo
1608
normal! zo
1609
normal! zo
1624
normal! zo
1625
normal! zo
1626
normal! zo
1638
normal! zo
1652
normal! zo
1654
normal! zo
1656
normal! zo
1708
normal! zo
1713
normal! zo
1741
normal! zo
1750
normal! zo
1757
normal! zo
1768
normal! zo
1771
normal! zo
1772
normal! zo
1772
normal! zo
1779
normal! zo
1784
normal! zo
1784
normal! zo
1784
normal! zo
1784
normal! zo
1818
normal! zo
1821
normal! zo
let s:l = 1346 - ((16 * winheight(0) + 17) / 34)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1346
normal! 011|
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
let s:l = 320 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
320
normal! 0
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
104
normal! zo
277
normal! zo
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit ginn/framework/pclases/superfacturaventa.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
38
normal! zo
let s:l = 621 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
621
normal! 028|
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
let s:l = 97 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
97
normal! 07|
wincmd w
argglobal
edit ginn/formularios/clientes.py
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
578
normal! zo
593
normal! zo
593
normal! zo
593
normal! zo
593
normal! zo
593
normal! zo
593
normal! zo
624
normal! zo
635
normal! zo
643
normal! zo
651
normal! zo
659
normal! zo
659
normal! zo
659
normal! zo
659
normal! zo
668
normal! zo
673
normal! zo
687
normal! zo
let s:l = 673 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
673
normal! 028|
wincmd w
5wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 7 + 34) / 69)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 6 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 7 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 34 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
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
5wincmd w

" vim: ft=vim ro nowrap smc=128
