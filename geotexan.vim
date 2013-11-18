" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 18 noviembre 2013 at 17:24:50.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 9
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
badd +114 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +901 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1706 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +117 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +3063 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2951 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +908 ginn/formularios/ventana.py
badd +1899 ginn/formularios/pedidos_de_venta.py
badd +3876 db/tablas.sql
badd +2103 ginn/formularios/albaranes_de_salida.py
badd +227 ginn/formularios/presupuesto.py
badd +1 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +693 ginn/formularios/facturas_compra.py
badd +15 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +218 ginn/formularios/gtkexcepthook.py
badd +351 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +10622 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +61 ginn/framework/pclases/facturaventa.py
badd +689 ginn/formularios/consulta_mensual_nominas.py
badd +88 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +118 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +140 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +221 ginn/formularios/consumo_balas_partida.py
badd +553 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +488 ginn/framework/pclases/cliente.py
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
badd +404 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +416 ginn/formularios/consulta_productividad.py
badd +212 ginn/formularios/mail_sender.py
badd +1143 ginn/formularios/abonos_venta.py
badd +306 ginn/formularios/ventana_progreso.py
badd +1047 ginn/formularios/control_personal.py
badd +195 ginn/formularios/listado_rollos.py
badd +85 ginn/formularios/consulta_existenciasRollos.py
badd +91 ginn/formularios/listado_rollos_defectuosos.py
badd +3498 ginn/formularios/consulta_global.py
badd +195 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
badd +1 ginn/informes/presupuesto.py
badd +112 ginn/formularios/consulta_libro_iva.py
badd +929 ginn/formularios/consulta_ofertas.py
badd +24 extra/patches/create_ventana_consultas.py
badd +203 ginn/lib/ezodf/ezodf/const.py
badd +61 ginn/lib/ezodf/ezodf/xmlns.py
badd +307 ginn/lib/simple_odspy/simpleodspy/sodsods.py
badd +17 ginn/lib/simple_odspy/simpleodspy/sodsspreadsheet.py
badd +41 ginn/lib/simple_odspy/simpleodspy/sodstable.py
badd +66 ginn/lib/odfpy/contrib/odscell/odscell
badd +127 ginn/lib/odfpy/contrib/odscell/odscell.py
args formularios/auditviewer.py
set lines=51 columns=107
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
exe 'vert 1resize ' . ((&columns * 26 + 53) / 107)
exe '2resize ' . ((&lines * 39 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 80 + 53) / 107)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 53) / 107)
exe '4resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 53) / 107)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 53) / 107)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 53) / 107)
exe '7resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 53) / 107)
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
61
normal! zo
62
normal! zo
70
normal! zo
70
normal! zo
70
normal! zo
70
normal! zo
107
normal! zo
107
normal! zo
107
normal! zo
107
normal! zo
107
normal! zo
110
normal! zo
110
normal! zo
110
normal! zo
110
normal! zo
110
normal! zo
152
normal! zo
152
normal! zo
152
normal! zo
154
normal! zo
154
normal! zo
154
normal! zo
161
normal! zo
162
normal! zo
165
normal! zo
166
normal! zo
199
normal! zo
211
normal! zo
217
normal! zo
226
normal! zo
228
normal! zo
233
normal! zo
234
normal! zo
238
normal! zo
239
normal! zo
250
normal! zo
251
normal! zo
252
normal! zo
262
normal! zo
268
normal! zo
269
normal! zo
279
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
293
normal! zo
318
normal! zo
318
normal! zo
318
normal! zo
318
normal! zo
346
normal! zo
346
normal! zo
346
normal! zo
346
normal! zo
346
normal! zo
346
normal! zo
346
normal! zo
346
normal! zo
348
normal! zo
349
normal! zo
349
normal! zo
355
normal! zo
358
normal! zo
364
normal! zo
365
normal! zo
365
normal! zo
365
normal! zo
365
normal! zo
365
normal! zo
365
normal! zo
370
normal! zo
371
normal! zo
375
normal! zo
396
normal! zo
401
normal! zo
406
normal! zo
420
normal! zo
420
normal! zo
422
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
445
normal! zo
456
normal! zo
465
normal! zo
476
normal! zo
476
normal! zo
483
normal! zo
483
normal! zo
491
normal! zo
493
normal! zo
494
normal! zo
495
normal! zo
506
normal! zo
526
normal! zo
539
normal! zo
540
normal! zo
551
normal! zo
563
normal! zo
563
normal! zo
571
normal! zo
572
normal! zo
579
normal! zo
589
normal! zo
589
normal! zo
597
normal! zo
597
normal! zo
598
normal! zo
606
normal! zo
606
normal! zo
614
normal! zo
619
normal! zo
619
normal! zo
619
normal! zo
619
normal! zo
619
normal! zo
623
normal! zo
625
normal! zo
641
normal! zo
660
normal! zo
668
normal! zo
686
normal! zo
686
normal! zo
690
normal! zo
694
normal! zo
695
normal! zo
705
normal! zo
745
normal! zo
764
normal! zo
772
normal! zo
786
normal! zo
793
normal! zo
793
normal! zo
797
normal! zo
801
normal! zo
802
normal! zo
809
normal! zo
817
normal! zo
848
normal! zo
853
normal! zo
853
normal! zo
854
normal! zo
859
normal! zo
892
normal! zo
907
normal! zo
912
normal! zo
936
normal! zo
976
normal! zo
985
normal! zo
992
normal! zo
992
normal! zo
993
normal! zo
997
normal! zo
998
normal! zo
1010
normal! zo
1015
normal! zo
1016
normal! zo
1016
normal! zo
1016
normal! zo
1016
normal! zo
1016
normal! zo
1016
normal! zo
1016
normal! zo
1016
normal! zo
1016
normal! zo
1020
normal! zo
1033
normal! zo
1034
normal! zo
1038
normal! zo
1052
normal! zo
1068
normal! zo
1088
normal! zo
1089
normal! zo
1089
normal! zo
1090
normal! zo
1095
normal! zo
1111
normal! zo
1118
normal! zo
1120
normal! zo
1157
normal! zo
1161
normal! zo
1170
normal! zo
1178
normal! zo
1201
normal! zo
1201
normal! zo
1211
normal! zo
1263
normal! zo
1263
normal! zo
1278
normal! zo
1287
normal! zo
1288
normal! zo
1325
normal! zo
1336
normal! zo
1354
normal! zo
1362
normal! zo
1363
normal! zo
1368
normal! zo
1377
normal! zo
1383
normal! zo
1387
normal! zo
1390
normal! zo
1396
normal! zo
1396
normal! zo
1396
normal! zo
1396
normal! zo
1396
normal! zo
1396
normal! zo
1407
normal! zo
1410
normal! zo
1416
normal! zo
1424
normal! zo
1443
normal! zo
1459
normal! zo
1462
normal! zo
1469
normal! zo
1473
normal! zo
1476
normal! zo
1492
normal! zo
1503
normal! zo
1532
normal! zo
1532
normal! zo
1532
normal! zo
1535
normal! zo
1543
normal! zo
1558
normal! zo
1558
normal! zo
1561
normal! zo
1564
normal! zo
1573
normal! zo
1573
normal! zo
1573
normal! zo
1573
normal! zo
1573
normal! zo
1573
normal! zo
1579
normal! zo
1583
normal! zo
1587
normal! zo
1593
normal! zo
1594
normal! zo
1594
normal! zo
1594
normal! zo
1594
normal! zo
1594
normal! zo
1596
normal! zo
1608
normal! zo
1608
normal! zo
1608
normal! zo
1622
normal! zo
1624
normal! zo
1626
normal! zo
1626
normal! zo
1641
normal! zo
1662
normal! zo
1684
normal! zo
1693
normal! zo
1694
normal! zo
1732
normal! zo
1743
normal! zo
1787
normal! zo
1787
normal! zo
1787
normal! zo
1787
normal! zo
1803
normal! zo
1804
normal! zo
1808
normal! zo
1812
normal! zo
1812
normal! zo
1816
normal! zo
1819
normal! zo
1827
normal! zo
1871
normal! zo
1902
normal! zo
1903
normal! zo
1911
normal! zo
1911
normal! zo
1964
normal! zo
1964
normal! zo
1964
normal! zo
1964
normal! zo
1964
normal! zo
1964
normal! zo
1964
normal! zo
1982
normal! zo
1987
normal! zo
1997
normal! zo
2001
normal! zo
2005
normal! zo
2006
normal! zo
2007
normal! zo
2007
normal! zo
2007
normal! zo
2007
normal! zo
2016
normal! zo
2017
normal! zo
2017
normal! zo
2017
normal! zo
2017
normal! zo
2017
normal! zo
2029
normal! zo
2033
normal! zo
2035
normal! zo
2043
normal! zo
2043
normal! zo
2052
normal! zo
2062
normal! zo
2081
normal! zo
2082
normal! zo
2083
normal! zo
2085
normal! zo
2085
normal! zo
2085
normal! zo
2085
normal! zo
2088
normal! zo
2088
normal! zo
2089
normal! zo
2091
normal! zo
2119
normal! zo
2140
normal! zo
2167
normal! zo
2184
normal! zo
2206
normal! zo
2211
normal! zo
2225
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2233
normal! zo
2237
normal! zo
2245
normal! zo
2251
normal! zo
2257
normal! zo
2258
normal! zo
2262
normal! zo
2262
normal! zo
2271
normal! zo
2284
normal! zo
2317
normal! zo
2328
normal! zo
2328
normal! zo
2328
normal! zo
2328
normal! zo
2328
normal! zo
2328
normal! zo
2328
normal! zo
2331
normal! zo
2331
normal! zo
2331
normal! zo
2331
normal! zo
2331
normal! zo
2331
normal! zo
2332
normal! zo
2336
normal! zo
2344
normal! zo
2349
normal! zo
2352
normal! zo
2382
normal! zo
2382
normal! zo
2383
normal! zo
2412
normal! zo
2428
normal! zo
2430
normal! zo
2477
normal! zo
2478
normal! zo
2478
normal! zo
2488
normal! zo
2493
normal! zo
2497
normal! zo
2503
normal! zo
2516
normal! zo
2516
normal! zo
2522
normal! zo
2522
normal! zo
2530
normal! zo
2543
normal! zo
2543
normal! zo
2547
normal! zo
2547
normal! zo
2555
normal! zo
2564
normal! zo
2582
normal! zo
2585
normal! zo
2586
normal! zo
2586
normal! zo
2593
normal! zo
2609
normal! zo
2635
normal! zo
2645
normal! zo
2645
normal! zo
2645
normal! zo
2645
normal! zo
2650
normal! zo
2651
normal! zo
2651
normal! zo
2651
normal! zo
2655
normal! zo
2656
normal! zo
2656
normal! zo
2660
normal! zo
2661
normal! zo
2661
normal! zo
2667
normal! zo
2667
normal! zo
2667
normal! zo
2711
normal! zo
2712
normal! zo
2724
normal! zo
2725
normal! zo
2728
normal! zo
2728
normal! zo
2729
normal! zo
2746
normal! zo
2750
normal! zo
2751
normal! zo
2751
normal! zo
2751
normal! zo
2759
normal! zo
2764
normal! zo
2767
normal! zo
2768
normal! zo
2791
normal! zo
2802
normal! zo
2809
normal! zo
2818
normal! zo
2819
normal! zo
2819
normal! zo
2820
normal! zo
2820
normal! zo
2821
normal! zo
2822
normal! zo
2827
normal! zo
2831
normal! zo
2834
normal! zo
2835
normal! zo
2835
normal! zo
2836
normal! zo
2840
normal! zo
2841
normal! zo
2842
normal! zo
2842
normal! zo
2850
normal! zo
2855
normal! zo
2857
normal! zo
2857
normal! zo
2858
normal! zo
2858
normal! zo
2863
normal! zo
2864
normal! zo
2878
normal! zo
2880
normal! zo
2885
normal! zo
2888
normal! zo
2889
normal! zo
2908
normal! zo
2922
normal! zo
2950
normal! zo
2965
normal! zo
2969
normal! zo
3050
normal! zo
let s:l = 399 - ((10 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
399
normal! 0191|
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
461
normal! zo
480
normal! zo
499
normal! zo
644
normal! zo
667
normal! zo
674
normal! zo
683
normal! zo
742
normal! zo
775
normal! zo
778
normal! zo
778
normal! zo
778
normal! zo
778
normal! zo
778
normal! zo
778
normal! zo
780
normal! zo
780
normal! zo
780
normal! zo
780
normal! zo
780
normal! zo
780
normal! zo
1192
normal! zo
1201
normal! zo
1301
normal! zo
1310
normal! zo
1410
normal! zo
1419
normal! zo
1519
normal! zo
1528
normal! zo
2072
normal! zo
2248
normal! zo
2269
normal! zo
2450
normal! zo
2460
normal! zo
2460
normal! zo
3185
normal! zo
3336
normal! zo
4088
normal! zo
4417
normal! zo
4456
normal! zo
4456
normal! zo
4456
normal! zo
4456
normal! zo
4749
normal! zo
4762
normal! zo
4773
normal! zo
4794
normal! zo
7253
normal! zo
7258
normal! zo
7258
normal! zo
9051
normal! zo
9124
normal! zo
9391
normal! zo
9746
normal! zo
9786
normal! zo
9839
normal! zo
9842
normal! zo
9868
normal! zo
9870
normal! zo
10094
normal! zo
10099
normal! zo
10107
normal! zo
10212
normal! zo
10303
normal! zo
10312
normal! zo
10314
normal! zo
10493
normal! zo
10496
normal! zo
10528
normal! zo
10530
normal! zo
10536
normal! zo
10539
normal! zo
10544
normal! zo
10549
normal! zo
10555
normal! zo
10601
normal! zo
10602
normal! zo
10602
normal! zo
10606
normal! zo
10612
normal! zo
10613
normal! zo
10613
normal! zo
11010
normal! zo
11024
normal! zo
11024
normal! zo
11024
normal! zo
11024
normal! zo
11913
normal! zo
12245
normal! zo
14298
normal! zo
14325
normal! zo
14330
normal! zo
14412
normal! zo
14412
normal! zo
14412
normal! zo
14412
normal! zo
14434
normal! zo
14435
normal! zo
14445
normal! zo
14497
normal! zo
14532
normal! zo
14537
normal! zo
14538
normal! zo
15072
normal! zo
15077
normal! zo
15077
normal! zo
15077
normal! zo
15077
normal! zo
15321
normal! zo
15334
normal! zo
15344
normal! zo
15447
normal! zo
15451
normal! zo
15451
normal! zo
15451
normal! zo
15451
normal! zo
15451
normal! zo
15455
normal! zo
15455
normal! zo
15455
normal! zo
15455
normal! zo
15497
normal! zo
15500
normal! zo
15500
normal! zo
15500
normal! zo
15500
normal! zo
16239
normal! zo
16627
normal! zo
16638
normal! zo
16638
normal! zo
16638
normal! zo
16638
normal! zo
16669
normal! zo
16677
normal! zo
16677
normal! zo
16677
normal! zo
16677
normal! zo
16992
normal! zo
17188
normal! zo
18043
normal! zo
18053
normal! zo
18063
normal! zo
18152
normal! zo
18162
normal! zo
18197
normal! zo
18204
normal! zo
18211
normal! zo
18212
normal! zo
18212
normal! zo
18212
normal! zo
18214
normal! zo
18215
normal! zo
18215
normal! zo
18215
normal! zo
18291
normal! zo
18358
normal! zo
18369
normal! zo
18419
normal! zo
18476
normal! zo
18486
normal! zo
18534
normal! zo
18587
normal! zo
18828
normal! zo
18850
normal! zo
18909
normal! zo
19107
normal! zo
19576
normal! zo
19815
normal! zo
19988
normal! zo
19992
normal! zo
19992
normal! zo
20081
normal! zo
20144
normal! zo
20344
normal! zo
20448
normal! zo
20454
normal! zo
20455
normal! zo
20456
normal! zo
20456
normal! zo
20456
normal! zo
20456
normal! zo
20456
normal! zo
20456
normal! zo
20466
normal! zo
20677
normal! zo
20768
normal! zo
let s:l = 9872 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9872
normal! 024|
lcd ~/Geotexan/src/Geotex-INN
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
let s:l = 317 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
317
normal! 0264|
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
1068
normal! zo
let s:l = 137 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
137
normal! 049|
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
let s:l = 521 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
521
normal! 07|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/launcher.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
51
normal! zo
67
normal! zo
71
normal! zo
98
normal! zo
101
normal! zo
112
normal! zo
let s:l = 68 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
68
normal! 053|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 26 + 53) / 107)
exe '2resize ' . ((&lines * 39 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 80 + 53) / 107)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 53) / 107)
exe '4resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 53) / 107)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 53) / 107)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 53) / 107)
exe '7resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 53) / 107)
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
