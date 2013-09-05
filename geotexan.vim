" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 04 septiembre 2013 at 17:40:16.
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
badd +3614 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2958 ginn/formularios/facturas_venta.py
badd +479 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +250 ginn/formularios/ventana.py
badd +1851 ginn/formularios/pedidos_de_venta.py
badd +2895 db/tablas.sql
badd +4267 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +9 ginn/formularios/presupuestos.py
badd +382 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +724 ginn/formularios/facturas_compra.py
badd +1897 ginn/formularios/utils.py
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
badd +36 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +467 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
args formularios/auditviewer.py
set lines=44 columns=111
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
exe '2resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 26 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
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
silent! normal zo
641
silent! normal zo
722
silent! normal zo
1608
silent! normal zo
2052
silent! normal zo
2160
silent! normal zo
2160
silent! normal zo
2160
silent! normal zo
2160
silent! normal zo
2430
silent! normal zo
4765
silent! normal zo
4804
silent! normal zo
4816
silent! normal zo
4817
silent! normal zo
4817
silent! normal zo
4817
silent! normal zo
6452
silent! normal zo
6732
silent! normal zo
6758
silent! normal zo
6830
silent! normal zo
6943
silent! normal zo
7224
silent! normal zo
7545
silent! normal zo
8512
silent! normal zo
8525
silent! normal zo
8526
silent! normal zo
8527
silent! normal zo
9717
silent! normal zo
9757
silent! normal zo
9764
silent! normal zo
9797
silent! normal zo
9810
silent! normal zo
9813
silent! normal zo
9826
silent! normal zo
9829
silent! normal zo
9839
silent! normal zo
9841
silent! normal zo
9873
silent! normal zo
10067
silent! normal zo
10074
silent! normal zo
10083
silent! normal zo
10088
silent! normal zo
10096
silent! normal zo
10104
silent! normal zo
10115
silent! normal zo
10129
silent! normal zo
10148
silent! normal zo
10160
silent! normal zo
10166
silent! normal zo
10170
silent! normal zo
10176
silent! normal zo
10200
silent! normal zo
10208
silent! normal zo
10209
silent! normal zo
10217
silent! normal zo
10232
silent! normal zo
10241
silent! normal zo
10241
silent! normal zo
10241
silent! normal zo
10253
silent! normal zo
10273
silent! normal zo
10274
silent! normal zo
10275
silent! normal zo
10275
silent! normal zo
10275
silent! normal zo
10275
silent! normal zo
10275
silent! normal zo
10275
silent! normal zo
10275
silent! normal zo
10275
silent! normal zo
10275
silent! normal zo
10292
silent! normal zo
10298
silent! normal zo
10308
silent! normal zo
10314
silent! normal zo
10317
silent! normal zo
10320
silent! normal zo
10320
silent! normal zo
10320
silent! normal zo
10323
silent! normal zo
10323
silent! normal zo
10323
silent! normal zo
10323
silent! normal zo
10335
silent! normal zo
10341
silent! normal zo
10344
silent! normal zo
10346
silent! normal zo
10349
silent! normal zo
10352
silent! normal zo
10357
silent! normal zo
10364
silent! normal zo
10368
silent! normal zo
10369
silent! normal zo
10369
silent! normal zo
10371
silent! normal zo
10372
silent! normal zo
10372
silent! normal zo
10374
silent! normal zo
10375
silent! normal zo
10375
silent! normal zo
10377
silent! normal zo
10378
silent! normal zo
10378
silent! normal zo
10380
silent! normal zo
10381
silent! normal zo
10381
silent! normal zo
10383
silent! normal zo
10384
silent! normal zo
10384
silent! normal zo
10386
silent! normal zo
10387
silent! normal zo
10387
silent! normal zo
10389
silent! normal zo
10392
silent! normal zo
10394
silent! normal zo
10394
silent! normal zo
10394
silent! normal zo
10407
normal zc
10411
silent! normal zo
10415
silent! normal zo
10418
silent! normal zo
10419
silent! normal zo
10419
silent! normal zo
10419
silent! normal zo
10419
silent! normal zo
10419
silent! normal zo
10419
silent! normal zo
10424
silent! normal zo
10425
silent! normal zo
10425
silent! normal zo
10425
silent! normal zo
10428
silent! normal zo
10437
silent! normal zo
10447
silent! normal zo
10453
silent! normal zo
14033
silent! normal zo
14052
silent! normal zo
14440
silent! normal zo
15174
silent! normal zo
15193
silent! normal zo
15436
silent! normal zo
15488
silent! normal zo
15548
silent! normal zo
15722
silent! normal zo
15948
silent! normal zo
16933
silent! normal zo
17788
silent! normal zo
17928
silent! normal zo
17993
silent! normal zo
17994
silent! normal zo
18000
silent! normal zo
18003
silent! normal zo
18004
silent! normal zo
18004
silent! normal zo
18004
silent! normal zo
18004
silent! normal zo
18124
silent! normal zo
18384
silent! normal zo
19624
silent! normal zo
19869
silent! normal zo
19918
silent! normal zo
19929
silent! normal zo
19930
silent! normal zo
19938
silent! normal zo
19949
silent! normal zo
19950
silent! normal zo
let s:l = 308 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
308
normal! 04l
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
silent! normal zo
61
silent! normal zo
65
silent! normal zo
65
silent! normal zo
65
silent! normal zo
65
silent! normal zo
65
silent! normal zo
72
silent! normal zo
83
silent! normal zo
88
silent! normal zo
92
silent! normal zo
93
silent! normal zo
93
silent! normal zo
105
silent! normal zo
110
silent! normal zo
110
silent! normal zo
112
silent! normal zo
112
silent! normal zo
112
silent! normal zo
158
silent! normal zo
171
silent! normal zo
184
silent! normal zo
203
silent! normal zo
213
silent! normal zo
240
silent! normal zo
262
silent! normal zo
262
silent! normal zo
262
silent! normal zo
262
silent! normal zo
262
silent! normal zo
312
silent! normal zo
348
silent! normal zo
376
silent! normal zo
376
silent! normal zo
376
silent! normal zo
379
silent! normal zo
382
silent! normal zo
383
silent! normal zo
383
silent! normal zo
389
silent! normal zo
389
silent! normal zo
389
silent! normal zo
390
silent! normal zo
390
silent! normal zo
390
silent! normal zo
390
silent! normal zo
396
silent! normal zo
396
silent! normal zo
396
silent! normal zo
396
silent! normal zo
396
silent! normal zo
402
silent! normal zo
404
silent! normal zo
404
silent! normal zo
404
silent! normal zo
404
silent! normal zo
406
silent! normal zo
406
silent! normal zo
406
silent! normal zo
406
silent! normal zo
417
silent! normal zo
420
silent! normal zo
431
silent! normal zo
448
silent! normal zo
454
silent! normal zo
457
silent! normal zo
458
silent! normal zo
463
silent! normal zo
463
silent! normal zo
463
silent! normal zo
463
silent! normal zo
466
silent! normal zo
468
silent! normal zo
470
silent! normal zo
473
silent! normal zo
485
silent! normal zo
510
silent! normal zo
527
silent! normal zo
528
silent! normal zo
528
silent! normal zo
528
silent! normal zo
567
silent! normal zo
570
silent! normal zo
let s:l = 430 - ((12 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
430
normal! 040l
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
silent! normal zo
150
silent! normal zo
170
silent! normal zo
185
silent! normal zo
190
silent! normal zo
279
silent! normal zo
282
silent! normal zo
282
silent! normal zo
293
silent! normal zo
293
silent! normal zo
293
silent! normal zo
293
silent! normal zo
293
silent! normal zo
311
silent! normal zo
314
silent! normal zo
let s:l = 346 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
346
normal! 022l
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
silent! normal zo
60
silent! normal zo
68
silent! normal zo
68
silent! normal zo
68
silent! normal zo
87
silent! normal zo
87
silent! normal zo
87
silent! normal zo
89
silent! normal zo
89
silent! normal zo
89
silent! normal zo
96
silent! normal zo
97
silent! normal zo
100
silent! normal zo
101
silent! normal zo
125
silent! normal zo
134
silent! normal zo
135
silent! normal zo
135
silent! normal zo
135
silent! normal zo
135
silent! normal zo
135
silent! normal zo
137
silent! normal zo
137
silent! normal zo
137
silent! normal zo
138
silent! normal zo
143
silent! normal zo
153
silent! normal zo
153
silent! normal zo
160
silent! normal zo
160
silent! normal zo
168
silent! normal zo
170
silent! normal zo
171
silent! normal zo
172
silent! normal zo
173
silent! normal zo
191
silent! normal zo
192
silent! normal zo
203
silent! normal zo
215
silent! normal zo
215
silent! normal zo
223
silent! normal zo
224
silent! normal zo
231
silent! normal zo
241
silent! normal zo
241
silent! normal zo
249
silent! normal zo
249
silent! normal zo
250
silent! normal zo
258
silent! normal zo
258
silent! normal zo
275
silent! normal zo
290
silent! normal zo
292
silent! normal zo
292
silent! normal zo
292
silent! normal zo
292
silent! normal zo
292
silent! normal zo
298
silent! normal zo
309
silent! normal zo
316
silent! normal zo
316
silent! normal zo
317
silent! normal zo
320
silent! normal zo
324
silent! normal zo
325
silent! normal zo
329
silent! normal zo
330
silent! normal zo
335
silent! normal zo
340
silent! normal zo
344
silent! normal zo
354
silent! normal zo
355
silent! normal zo
355
silent! normal zo
355
silent! normal zo
355
silent! normal zo
355
silent! normal zo
355
silent! normal zo
370
silent! normal zo
375
silent! normal zo
375
silent! normal zo
376
silent! normal zo
381
silent! normal zo
414
silent! normal zo
419
silent! normal zo
420
silent! normal zo
420
silent! normal zo
421
silent! normal zo
421
silent! normal zo
422
silent! normal zo
423
silent! normal zo
428
silent! normal zo
432
silent! normal zo
435
silent! normal zo
436
silent! normal zo
436
silent! normal zo
437
silent! normal zo
441
silent! normal zo
442
silent! normal zo
443
silent! normal zo
450
silent! normal zo
451
silent! normal zo
452
silent! normal zo
465
silent! normal zo
465
silent! normal zo
465
silent! normal zo
465
silent! normal zo
465
silent! normal zo
467
silent! normal zo
468
silent! normal zo
469
silent! normal zo
478
silent! normal zo
478
silent! normal zo
478
silent! normal zo
478
silent! normal zo
478
silent! normal zo
482
silent! normal zo
482
silent! normal zo
482
silent! normal zo
482
silent! normal zo
482
silent! normal zo
482
silent! normal zo
498
silent! normal zo
499
silent! normal zo
502
silent! normal zo
503
silent! normal zo
511
silent! normal zo
512
silent! normal zo
521
silent! normal zo
525
silent! normal zo
540
silent! normal zo
545
silent! normal zo
568
silent! normal zo
599
silent! normal zo
599
silent! normal zo
599
silent! normal zo
599
silent! normal zo
599
silent! normal zo
599
silent! normal zo
599
silent! normal zo
608
silent! normal zo
618
silent! normal zo
625
silent! normal zo
625
silent! normal zo
626
silent! normal zo
630
silent! normal zo
631
silent! normal zo
636
silent! normal zo
638
silent! normal zo
643
silent! normal zo
644
silent! normal zo
645
silent! normal zo
645
silent! normal zo
648
silent! normal zo
649
silent! normal zo
649
silent! normal zo
649
silent! normal zo
649
silent! normal zo
649
silent! normal zo
649
silent! normal zo
649
silent! normal zo
649
silent! normal zo
649
silent! normal zo
663
silent! normal zo
677
silent! normal zo
678
silent! normal zo
686
silent! normal zo
692
silent! normal zo
696
silent! normal zo
703
silent! normal zo
705
silent! normal zo
707
silent! normal zo
708
silent! normal zo
708
silent! normal zo
708
silent! normal zo
708
silent! normal zo
708
silent! normal zo
708
silent! normal zo
708
silent! normal zo
713
silent! normal zo
735
silent! normal zo
752
silent! normal zo
752
silent! normal zo
762
silent! normal zo
768
silent! normal zo
768
silent! normal zo
768
silent! normal zo
768
silent! normal zo
768
silent! normal zo
768
silent! normal zo
768
silent! normal zo
768
silent! normal zo
768
silent! normal zo
768
silent! normal zo
768
silent! normal zo
796
silent! normal zo
796
silent! normal zo
796
silent! normal zo
796
silent! normal zo
796
silent! normal zo
805
silent! normal zo
805
silent! normal zo
805
silent! normal zo
805
silent! normal zo
805
silent! normal zo
805
silent! normal zo
812
silent! normal zo
815
silent! normal zo
821
silent! normal zo
822
silent! normal zo
831
silent! normal zo
839
silent! normal zo
850
silent! normal zo
854
silent! normal zo
868
silent! normal zo
875
silent! normal zo
879
silent! normal zo
882
silent! normal zo
898
silent! normal zo
905
silent! normal zo
909
silent! normal zo
913
silent! normal zo
916
silent! normal zo
918
silent! normal zo
918
silent! normal zo
919
silent! normal zo
919
silent! normal zo
921
silent! normal zo
923
silent! normal zo
923
silent! normal zo
923
silent! normal zo
925
silent! normal zo
925
silent! normal zo
925
silent! normal zo
927
silent! normal zo
927
silent! normal zo
927
silent! normal zo
939
silent! normal zo
947
silent! normal zo
956
silent! normal zo
956
silent! normal zo
959
silent! normal zo
962
silent! normal zo
963
silent! normal zo
963
silent! normal zo
963
silent! normal zo
969
silent! normal zo
969
silent! normal zo
969
silent! normal zo
969
silent! normal zo
969
silent! normal zo
969
silent! normal zo
989
silent! normal zo
990
silent! normal zo
992
silent! normal zo
992
silent! normal zo
997
silent! normal zo
1009
silent! normal zo
1018
silent! normal zo
1019
silent! normal zo
1024
silent! normal zo
1032
silent! normal zo
1037
silent! normal zo
1037
silent! normal zo
1037
silent! normal zo
1037
silent! normal zo
1037
silent! normal zo
1039
silent! normal zo
1039
silent! normal zo
1054
silent! normal zo
1062
silent! normal zo
1062
silent! normal zo
1076
silent! normal zo
1076
silent! normal zo
1076
silent! normal zo
1076
silent! normal zo
1081
silent! normal zo
1089
silent! normal zo
1098
silent! normal zo
1104
silent! normal zo
1107
silent! normal zo
1119
silent! normal zo
1122
silent! normal zo
1129
silent! normal zo
1146
silent! normal zo
1147
silent! normal zo
1148
silent! normal zo
1150
silent! normal zo
1150
silent! normal zo
1150
silent! normal zo
1150
silent! normal zo
1153
silent! normal zo
1153
silent! normal zo
1154
silent! normal zo
1156
silent! normal zo
1158
silent! normal zo
1158
silent! normal zo
1160
silent! normal zo
1161
silent! normal zo
1161
silent! normal zo
1184
silent! normal zo
1188
silent! normal zo
1189
silent! normal zo
1189
silent! normal zo
1189
silent! normal zo
1189
silent! normal zo
1189
silent! normal zo
1189
silent! normal zo
1204
silent! normal zo
1206
silent! normal zo
1209
silent! normal zo
1211
silent! normal zo
1228
silent! normal zo
1231
silent! normal zo
1246
silent! normal zo
1252
silent! normal zo
1255
silent! normal zo
1255
silent! normal zo
1264
silent! normal zo
1277
silent! normal zo
1279
silent! normal zo
1301
silent! normal zo
1301
silent! normal zo
1301
silent! normal zo
1310
silent! normal zo
1321
silent! normal zo
1321
silent! normal zo
1321
silent! normal zo
1321
silent! normal zo
1321
silent! normal zo
1321
silent! normal zo
1321
silent! normal zo
1324
silent! normal zo
1324
silent! normal zo
1324
silent! normal zo
1324
silent! normal zo
1324
silent! normal zo
1324
silent! normal zo
1325
silent! normal zo
1329
silent! normal zo
1337
silent! normal zo
1345
silent! normal zo
1348
silent! normal zo
1349
silent! normal zo
1349
silent! normal zo
1349
silent! normal zo
1349
silent! normal zo
1351
silent! normal zo
1351
silent! normal zo
1351
silent! normal zo
1351
silent! normal zo
1351
silent! normal zo
1351
silent! normal zo
1353
silent! normal zo
1357
silent! normal zo
1363
silent! normal zo
1363
silent! normal zo
1384
silent! normal zo
1396
silent! normal zo
1410
silent! normal zo
1412
silent! normal zo
1414
silent! normal zo
1427
silent! normal zo
1464
silent! normal zo
1469
silent! normal zo
1485
silent! normal zo
1485
silent! normal zo
1486
silent! normal zo
1489
silent! normal zo
1489
silent! normal zo
1497
silent! normal zo
1506
silent! normal zo
1513
silent! normal zo
1524
silent! normal zo
1527
silent! normal zo
1528
silent! normal zo
1528
silent! normal zo
1529
silent! normal zo
1529
silent! normal zo
1529
silent! normal zo
1529
silent! normal zo
1529
silent! normal zo
1529
silent! normal zo
1529
silent! normal zo
1535
silent! normal zo
1537
silent! normal zo
1540
silent! normal zo
1540
silent! normal zo
1540
silent! normal zo
1540
silent! normal zo
1574
silent! normal zo
1577
silent! normal zo
1580
silent! normal zo
1581
silent! normal zo
1591
silent! normal zo
let s:l = 1030 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1030
normal! 033l
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
silent! normal zo
274
silent! normal zo
299
silent! normal zo
301
silent! normal zo
302
silent! normal zo
302
silent! normal zo
302
silent! normal zo
302
silent! normal zo
302
silent! normal zo
306
silent! normal zo
308
silent! normal zo
309
silent! normal zo
309
silent! normal zo
309
silent! normal zo
309
silent! normal zo
309
silent! normal zo
322
silent! normal zo
327
silent! normal zo
335
silent! normal zo
336
silent! normal zo
336
silent! normal zo
let s:l = 318 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
318
normal! 017l
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
let s:l = 4 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4
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
silent! normal zo
418
silent! normal zo
418
silent! normal zo
418
silent! normal zo
418
silent! normal zo
418
silent! normal zo
418
silent! normal zo
418
silent! normal zo
418
silent! normal zo
let s:l = 422 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
422
normal! 074l
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
silent! normal zo
51
silent! normal zo
66
silent! normal zo
70
silent! normal zo
let s:l = 111 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
111
normal! 06l
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
silent! normal zo
230
silent! normal zo
262
silent! normal zo
262
silent! normal zo
339
silent! normal zo
340
silent! normal zo
345
silent! normal zo
350
silent! normal zo
351
silent! normal zo
356
silent! normal zo
362
silent! normal zo
467
silent! normal zo
579
silent! normal zo
595
silent! normal zo
725
silent! normal zo
734
silent! normal zo
834
silent! normal zo
850
silent! normal zo
850
silent! normal zo
850
silent! normal zo
850
silent! normal zo
961
silent! normal zo
966
silent! normal zo
1531
silent! normal zo
1727
silent! normal zo
1728
silent! normal zo
1728
silent! normal zo
1728
silent! normal zo
1728
silent! normal zo
1739
silent! normal zo
1740
silent! normal zo
1744
silent! normal zo
1744
silent! normal zo
1745
silent! normal zo
1752
silent! normal zo
1753
silent! normal zo
1804
silent! normal zo
3253
silent! normal zo
3260
silent! normal zo
3265
silent! normal zo
3272
silent! normal zo
3276
silent! normal zo
3281
silent! normal zo
3282
silent! normal zo
3282
silent! normal zo
3282
silent! normal zo
3288
silent! normal zo
3293
silent! normal zo
3294
silent! normal zo
3299
silent! normal zo
let s:l = 1753 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1753
normal! 036l
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 26 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
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
3wincmd w

" vim: ft=vim ro nowrap smc=128
