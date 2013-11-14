" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 13 noviembre 2013 at 17:24:28.
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
badd +61 db/tablas.sql
badd +2103 ginn/formularios/albaranes_de_salida.py
badd +227 ginn/formularios/presupuesto.py
badd +2908 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +693 ginn/formularios/facturas_compra.py
badd +2016 ginn/formularios/utils.py
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
badd +33 ginn/framework/pclases/cliente.py
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
badd +39 ginn/informes/presupuesto2.py
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
badd +133 ginn/lib/odfpy/contrib/odscell/odscell.py
args formularios/auditviewer.py
set lines=51 columns=108
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
6wincmd k
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
exe 'vert 1resize ' . ((&columns * 28 + 54) / 108)
exe '2resize ' . ((&lines * 22 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 79 + 54) / 108)
exe '3resize ' . ((&lines * 16 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 79 + 54) / 108)
exe '4resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 79 + 54) / 108)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 79 + 54) / 108)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 79 + 54) / 108)
exe '7resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 79 + 54) / 108)
exe '8resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 79 + 54) / 108)
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
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
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
400
normal! zo
405
normal! zo
419
normal! zo
419
normal! zo
430
normal! zo
430
normal! zo
430
normal! zo
430
normal! zo
430
normal! zo
430
normal! zo
443
normal! zo
454
normal! zo
463
normal! zo
474
normal! zo
474
normal! zo
481
normal! zo
481
normal! zo
489
normal! zo
491
normal! zo
492
normal! zo
493
normal! zo
524
normal! zo
537
normal! zo
538
normal! zo
549
normal! zo
561
normal! zo
561
normal! zo
569
normal! zo
570
normal! zo
577
normal! zo
587
normal! zo
587
normal! zo
595
normal! zo
595
normal! zo
596
normal! zo
604
normal! zo
604
normal! zo
612
normal! zo
617
normal! zo
617
normal! zo
617
normal! zo
617
normal! zo
617
normal! zo
621
normal! zo
639
normal! zo
658
normal! zo
666
normal! zo
684
normal! zo
684
normal! zo
688
normal! zo
692
normal! zo
693
normal! zo
703
normal! zo
743
normal! zo
762
normal! zo
770
normal! zo
784
normal! zo
791
normal! zo
791
normal! zo
795
normal! zo
799
normal! zo
800
normal! zo
807
normal! zo
815
normal! zo
846
normal! zo
851
normal! zo
851
normal! zo
852
normal! zo
857
normal! zo
890
normal! zo
905
normal! zo
910
normal! zo
934
normal! zo
974
normal! zo
983
normal! zo
990
normal! zo
990
normal! zo
991
normal! zo
995
normal! zo
996
normal! zo
1008
normal! zo
1013
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1018
normal! zo
1031
normal! zo
1032
normal! zo
1036
normal! zo
1050
normal! zo
1066
normal! zo
1086
normal! zo
1087
normal! zo
1087
normal! zo
1088
normal! zo
1093
normal! zo
1109
normal! zo
1116
normal! zo
1118
normal! zo
1155
normal! zo
1159
normal! zo
1168
normal! zo
1176
normal! zo
1199
normal! zo
1199
normal! zo
1209
normal! zo
1261
normal! zo
1261
normal! zo
1276
normal! zo
1285
normal! zo
1286
normal! zo
1323
normal! zo
1334
normal! zo
1352
normal! zo
1360
normal! zo
1361
normal! zo
1366
normal! zo
1375
normal! zo
1381
normal! zo
1385
normal! zo
1388
normal! zo
1394
normal! zo
1394
normal! zo
1394
normal! zo
1394
normal! zo
1394
normal! zo
1394
normal! zo
1405
normal! zo
1408
normal! zo
1414
normal! zo
1422
normal! zo
1441
normal! zo
1457
normal! zo
1460
normal! zo
1467
normal! zo
1471
normal! zo
1474
normal! zo
1490
normal! zo
1501
normal! zo
1530
normal! zo
1530
normal! zo
1530
normal! zo
1533
normal! zo
1541
normal! zo
1556
normal! zo
1556
normal! zo
1559
normal! zo
1562
normal! zo
1571
normal! zo
1571
normal! zo
1571
normal! zo
1571
normal! zo
1571
normal! zo
1571
normal! zo
1577
normal! zo
1581
normal! zo
1585
normal! zo
1591
normal! zo
1592
normal! zo
1592
normal! zo
1592
normal! zo
1592
normal! zo
1592
normal! zo
1620
normal! zo
1622
normal! zo
1624
normal! zo
1624
normal! zo
1639
normal! zo
1660
normal! zo
1682
normal! zo
1691
normal! zo
1692
normal! zo
1730
normal! zo
1741
normal! zo
1785
normal! zo
1785
normal! zo
1785
normal! zo
1785
normal! zo
1801
normal! zo
1802
normal! zo
1806
normal! zo
1810
normal! zo
1810
normal! zo
1814
normal! zo
1817
normal! zo
1825
normal! zo
1869
normal! zo
1900
normal! zo
1901
normal! zo
1909
normal! zo
1909
normal! zo
1962
normal! zo
1962
normal! zo
1962
normal! zo
1962
normal! zo
1962
normal! zo
1962
normal! zo
1962
normal! zo
1980
normal! zo
1985
normal! zo
1995
normal! zo
1999
normal! zo
2003
normal! zo
2004
normal! zo
2005
normal! zo
2005
normal! zo
2005
normal! zo
2005
normal! zo
2014
normal! zo
2015
normal! zo
2015
normal! zo
2015
normal! zo
2015
normal! zo
2015
normal! zo
2027
normal! zo
2031
normal! zo
2033
normal! zo
2041
normal! zo
2050
normal! zo
2060
normal! zo
2079
normal! zo
2080
normal! zo
2081
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2086
normal! zo
2086
normal! zo
2087
normal! zo
2089
normal! zo
2117
normal! zo
2138
normal! zo
2165
normal! zo
2182
normal! zo
2204
normal! zo
2209
normal! zo
2223
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2231
normal! zo
2235
normal! zo
2243
normal! zo
2249
normal! zo
2255
normal! zo
2256
normal! zo
2260
normal! zo
2260
normal! zo
2269
normal! zo
2282
normal! zo
2315
normal! zo
2326
normal! zo
2326
normal! zo
2326
normal! zo
2326
normal! zo
2326
normal! zo
2326
normal! zo
2326
normal! zo
2329
normal! zo
2329
normal! zo
2329
normal! zo
2329
normal! zo
2329
normal! zo
2329
normal! zo
2330
normal! zo
2334
normal! zo
2342
normal! zo
2347
normal! zo
2350
normal! zo
2380
normal! zo
2380
normal! zo
2381
normal! zo
2410
normal! zo
2424
normal! zo
2426
normal! zo
2473
normal! zo
2474
normal! zo
2474
normal! zo
2484
normal! zo
2489
normal! zo
2493
normal! zo
2499
normal! zo
2512
normal! zo
2512
normal! zo
2518
normal! zo
2518
normal! zo
2526
normal! zo
2539
normal! zo
2539
normal! zo
2543
normal! zo
2543
normal! zo
2551
normal! zo
2560
normal! zo
2578
normal! zo
2581
normal! zo
2582
normal! zo
2582
normal! zo
2589
normal! zo
2605
normal! zo
2630
normal! zo
2631
normal! zo
2641
normal! zo
2641
normal! zo
2641
normal! zo
2641
normal! zo
2646
normal! zo
2646
normal! zo
2646
normal! zo
2684
normal! zo
2685
normal! zo
2697
normal! zo
2698
normal! zo
2701
normal! zo
2701
normal! zo
2702
normal! zo
2715
normal! zo
2720
normal! zo
2720
normal! zo
2720
normal! zo
2720
normal! zo
2728
normal! zo
2733
normal! zo
2736
normal! zo
2737
normal! zo
2760
normal! zo
2771
normal! zo
2778
normal! zo
2787
normal! zo
2788
normal! zo
2788
normal! zo
2789
normal! zo
2789
normal! zo
2790
normal! zo
2791
normal! zo
2796
normal! zo
2800
normal! zo
2803
normal! zo
2804
normal! zo
2804
normal! zo
2805
normal! zo
2809
normal! zo
2810
normal! zo
2811
normal! zo
2811
normal! zo
2819
normal! zo
2824
normal! zo
2826
normal! zo
2826
normal! zo
2827
normal! zo
2827
normal! zo
2832
normal! zo
2833
normal! zo
2847
normal! zo
2849
normal! zo
2854
normal! zo
2857
normal! zo
2858
normal! zo
2877
normal! zo
2891
normal! zo
2919
normal! zo
2934
normal! zo
2938
normal! zo
let s:l = 2524 - ((5 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2524
normal! 04|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/lib/odfpy/contrib/odscell/odscell.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
67
normal! zo
67
normal! zo
67
normal! zo
89
normal! zo
105
normal! zo
let s:l = 95 - ((12 * winheight(0) + 8) / 16)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
95
normal! 036|
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
10094
normal! zo
10099
normal! zo
10107
normal! zo
10212
normal! zo
10588
normal! zo
10594
normal! zo
10595
normal! zo
10595
normal! zo
10992
normal! zo
11006
normal! zo
11006
normal! zo
11006
normal! zo
11006
normal! zo
14280
normal! zo
14307
normal! zo
14312
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14394
normal! zo
14416
normal! zo
14417
normal! zo
14427
normal! zo
14479
normal! zo
14514
normal! zo
14519
normal! zo
14520
normal! zo
15054
normal! zo
15059
normal! zo
15059
normal! zo
15059
normal! zo
15059
normal! zo
15303
normal! zo
15316
normal! zo
15326
normal! zo
15429
normal! zo
15433
normal! zo
15433
normal! zo
15433
normal! zo
15433
normal! zo
15433
normal! zo
15437
normal! zo
15437
normal! zo
15437
normal! zo
15437
normal! zo
15479
normal! zo
15482
normal! zo
15482
normal! zo
15482
normal! zo
15482
normal! zo
16221
normal! zo
16609
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16620
normal! zo
16651
normal! zo
16659
normal! zo
16659
normal! zo
16659
normal! zo
16659
normal! zo
16974
normal! zo
17170
normal! zo
18025
normal! zo
18035
normal! zo
18045
normal! zo
18134
normal! zo
18144
normal! zo
18179
normal! zo
18186
normal! zo
18193
normal! zo
18194
normal! zo
18194
normal! zo
18194
normal! zo
18196
normal! zo
18197
normal! zo
18197
normal! zo
18197
normal! zo
18273
normal! zo
18340
normal! zo
18351
normal! zo
18401
normal! zo
18458
normal! zo
18468
normal! zo
18516
normal! zo
18569
normal! zo
18810
normal! zo
18832
normal! zo
18891
normal! zo
19089
normal! zo
19558
normal! zo
19797
normal! zo
19970
normal! zo
19974
normal! zo
19974
normal! zo
20063
normal! zo
20126
normal! zo
20326
normal! zo
20430
normal! zo
20436
normal! zo
20437
normal! zo
20438
normal! zo
20438
normal! zo
20438
normal! zo
20438
normal! zo
20438
normal! zo
20438
normal! zo
20448
normal! zo
20659
normal! zo
20750
normal! zo
let s:l = 18197 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
18197
normal! 033|
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
let s:l = 520 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
520
normal! 05|
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
exe 'vert 1resize ' . ((&columns * 28 + 54) / 108)
exe '2resize ' . ((&lines * 22 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 79 + 54) / 108)
exe '3resize ' . ((&lines * 16 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 79 + 54) / 108)
exe '4resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 79 + 54) / 108)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 79 + 54) / 108)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 79 + 54) / 108)
exe '7resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 79 + 54) / 108)
exe '8resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 79 + 54) / 108)
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
