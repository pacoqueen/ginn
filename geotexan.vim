" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 11 noviembre 2013 at 18:00:05.
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
badd +114 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +901 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +749 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +117 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +6230 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1627 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +908 ginn/formularios/ventana.py
badd +1899 ginn/formularios/pedidos_de_venta.py
badd +61 db/tablas.sql
badd +2103 ginn/formularios/albaranes_de_salida.py
badd +227 ginn/formularios/presupuesto.py
badd +1160 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +693 ginn/formularios/facturas_compra.py
badd +4380 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +218 ginn/formularios/gtkexcepthook.py
badd +415 ginn/framework/seeker.py
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
badd +131 ginn/formularios/ventana_progreso.py
badd +1047 ginn/formularios/control_personal.py
badd +195 ginn/formularios/listado_rollos.py
badd +85 ginn/formularios/consulta_existenciasRollos.py
badd +91 ginn/formularios/listado_rollos_defectuosos.py
badd +3498 ginn/formularios/consulta_global.py
badd +195 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
badd +1 ginn/informes/presupuesto.py
badd +112 ginn/formularios/consulta_libro_iva.py
badd +360 ginn/formularios/consulta_ofertas.py
badd +24 extra/patches/create_ventana_consultas.py
args formularios/auditviewer.py
set lines=55 columns=108
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
exe 'vert 1resize ' . ((&columns * 28 + 54) / 108)
exe '2resize ' . ((&lines * 8 + 27) / 55)
exe 'vert 2resize ' . ((&columns * 79 + 54) / 108)
exe '3resize ' . ((&lines * 8 + 27) / 55)
exe 'vert 3resize ' . ((&columns * 79 + 54) / 108)
exe '4resize ' . ((&lines * 7 + 27) / 55)
exe 'vert 4resize ' . ((&columns * 79 + 54) / 108)
exe '5resize ' . ((&lines * 22 + 27) / 55)
exe 'vert 5resize ' . ((&columns * 79 + 54) / 108)
exe '6resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 6resize ' . ((&columns * 79 + 54) / 108)
exe '7resize ' . ((&lines * 2 + 27) / 55)
exe 'vert 7resize ' . ((&columns * 79 + 54) / 108)
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
351
normal! zo
352
normal! zo
352
normal! zo
358
normal! zo
361
normal! zo
367
normal! zo
368
normal! zo
368
normal! zo
368
normal! zo
368
normal! zo
368
normal! zo
368
normal! zo
373
normal! zo
374
normal! zo
378
normal! zo
399
normal! zo
404
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
436
normal! zo
447
normal! zo
456
normal! zo
467
normal! zo
467
normal! zo
474
normal! zo
474
normal! zo
482
normal! zo
484
normal! zo
485
normal! zo
486
normal! zo
517
normal! zo
530
normal! zo
531
normal! zo
542
normal! zo
554
normal! zo
554
normal! zo
562
normal! zo
563
normal! zo
570
normal! zo
580
normal! zo
580
normal! zo
588
normal! zo
588
normal! zo
589
normal! zo
597
normal! zo
597
normal! zo
605
normal! zo
610
normal! zo
610
normal! zo
610
normal! zo
610
normal! zo
610
normal! zo
614
normal! zo
632
normal! zo
651
normal! zo
659
normal! zo
677
normal! zo
677
normal! zo
681
normal! zo
685
normal! zo
686
normal! zo
696
normal! zo
736
normal! zo
755
normal! zo
763
normal! zo
777
normal! zo
784
normal! zo
784
normal! zo
788
normal! zo
792
normal! zo
793
normal! zo
800
normal! zo
808
normal! zo
839
normal! zo
844
normal! zo
844
normal! zo
845
normal! zo
850
normal! zo
883
normal! zo
898
normal! zo
903
normal! zo
927
normal! zo
976
normal! zo
983
normal! zo
983
normal! zo
984
normal! zo
988
normal! zo
989
normal! zo
1001
normal! zo
1006
normal! zo
1007
normal! zo
1007
normal! zo
1007
normal! zo
1007
normal! zo
1007
normal! zo
1007
normal! zo
1007
normal! zo
1007
normal! zo
1007
normal! zo
1011
normal! zo
1024
normal! zo
1025
normal! zo
1029
normal! zo
1043
normal! zo
1059
normal! zo
1079
normal! zo
1080
normal! zo
1080
normal! zo
1081
normal! zo
1086
normal! zo
1102
normal! zo
1109
normal! zo
1111
normal! zo
1148
normal! zo
1152
normal! zo
1161
normal! zo
1169
normal! zo
1192
normal! zo
1192
normal! zo
1202
normal! zo
1254
normal! zo
1254
normal! zo
1269
normal! zo
1278
normal! zo
1279
normal! zo
1316
normal! zo
1327
normal! zo
1345
normal! zo
1353
normal! zo
1354
normal! zo
1359
normal! zo
1368
normal! zo
1374
normal! zo
1378
normal! zo
1381
normal! zo
1387
normal! zo
1387
normal! zo
1387
normal! zo
1387
normal! zo
1387
normal! zo
1387
normal! zo
1398
normal! zo
1401
normal! zo
1407
normal! zo
1415
normal! zo
1434
normal! zo
1453
normal! zo
1460
normal! zo
1464
normal! zo
1467
normal! zo
1483
normal! zo
1494
normal! zo
1526
normal! zo
1534
normal! zo
1549
normal! zo
1549
normal! zo
1552
normal! zo
1555
normal! zo
1564
normal! zo
1564
normal! zo
1564
normal! zo
1564
normal! zo
1564
normal! zo
1564
normal! zo
1570
normal! zo
1574
normal! zo
1578
normal! zo
1584
normal! zo
1585
normal! zo
1585
normal! zo
1585
normal! zo
1585
normal! zo
1585
normal! zo
1613
normal! zo
1615
normal! zo
1617
normal! zo
1617
normal! zo
1632
normal! zo
1653
normal! zo
1675
normal! zo
1684
normal! zo
1685
normal! zo
1723
normal! zo
1734
normal! zo
1778
normal! zo
1778
normal! zo
1778
normal! zo
1778
normal! zo
1794
normal! zo
1795
normal! zo
1799
normal! zo
1803
normal! zo
1803
normal! zo
1807
normal! zo
1810
normal! zo
1818
normal! zo
1862
normal! zo
1893
normal! zo
1894
normal! zo
1902
normal! zo
1902
normal! zo
1955
normal! zo
1955
normal! zo
1955
normal! zo
1955
normal! zo
1955
normal! zo
1955
normal! zo
1955
normal! zo
1973
normal! zo
1978
normal! zo
1988
normal! zo
1992
normal! zo
1996
normal! zo
1997
normal! zo
1998
normal! zo
1998
normal! zo
1998
normal! zo
1998
normal! zo
2007
normal! zo
2008
normal! zo
2008
normal! zo
2008
normal! zo
2008
normal! zo
2008
normal! zo
2020
normal! zo
2024
normal! zo
2026
normal! zo
2043
normal! zo
2053
normal! zo
2072
normal! zo
2073
normal! zo
2074
normal! zo
2076
normal! zo
2076
normal! zo
2076
normal! zo
2076
normal! zo
2079
normal! zo
2079
normal! zo
2080
normal! zo
2082
normal! zo
2110
normal! zo
2131
normal! zo
2158
normal! zo
2175
normal! zo
2197
normal! zo
2202
normal! zo
2216
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2224
normal! zo
2228
normal! zo
2236
normal! zo
2242
normal! zo
2248
normal! zo
2249
normal! zo
2253
normal! zo
2253
normal! zo
2262
normal! zo
2275
normal! zo
2308
normal! zo
2319
normal! zo
2319
normal! zo
2319
normal! zo
2319
normal! zo
2319
normal! zo
2319
normal! zo
2319
normal! zo
2322
normal! zo
2322
normal! zo
2322
normal! zo
2322
normal! zo
2322
normal! zo
2322
normal! zo
2323
normal! zo
2327
normal! zo
2335
normal! zo
2340
normal! zo
2343
normal! zo
2403
normal! zo
2417
normal! zo
2419
normal! zo
2466
normal! zo
2467
normal! zo
2467
normal! zo
2477
normal! zo
2482
normal! zo
2486
normal! zo
2492
normal! zo
2505
normal! zo
2505
normal! zo
2511
normal! zo
2511
normal! zo
2519
normal! zo
2532
normal! zo
2532
normal! zo
2536
normal! zo
2536
normal! zo
2544
normal! zo
2553
normal! zo
2571
normal! zo
2574
normal! zo
2575
normal! zo
2575
normal! zo
2582
normal! zo
2624
normal! zo
2627
normal! zo
2628
normal! zo
2651
normal! zo
2662
normal! zo
2669
normal! zo
2678
normal! zo
2679
normal! zo
2679
normal! zo
2680
normal! zo
2680
normal! zo
2681
normal! zo
2682
normal! zo
2687
normal! zo
2691
normal! zo
2694
normal! zo
2695
normal! zo
2695
normal! zo
2696
normal! zo
2700
normal! zo
2701
normal! zo
2710
normal! zo
2715
normal! zo
2717
normal! zo
2717
normal! zo
2718
normal! zo
2718
normal! zo
2723
normal! zo
2724
normal! zo
2738
normal! zo
2740
normal! zo
2745
normal! zo
2748
normal! zo
2749
normal! zo
2810
normal! zo
2825
normal! zo
2829
normal! zo
let s:l = 1660 - ((3 * winheight(0) + 4) / 8)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1660
normal! 09|
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
let s:l = 20447 - ((4 * winheight(0) + 4) / 8)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
20447
normal! 05|
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
let s:l = 317 - ((0 * winheight(0) + 3) / 7)
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
67
normal! zo
105
normal! zo
106
normal! zo
106
normal! zo
159
normal! zo
211
normal! zo
293
normal! zo
377
normal! zo
442
normal! zo
485
normal! zo
663
normal! zo
749
normal! zo
749
normal! zo
749
normal! zo
749
normal! zo
1066
normal! zo
1074
normal! zo
1074
normal! zo
1074
normal! zo
1152
normal! zo
let s:l = 130 - ((2 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
130
normal! 011|
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
let s:l = 68 - ((1 * winheight(0) + 1) / 2)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
68
normal! 053|
wincmd w
5wincmd w
exe 'vert 1resize ' . ((&columns * 28 + 54) / 108)
exe '2resize ' . ((&lines * 8 + 27) / 55)
exe 'vert 2resize ' . ((&columns * 79 + 54) / 108)
exe '3resize ' . ((&lines * 8 + 27) / 55)
exe 'vert 3resize ' . ((&columns * 79 + 54) / 108)
exe '4resize ' . ((&lines * 7 + 27) / 55)
exe 'vert 4resize ' . ((&columns * 79 + 54) / 108)
exe '5resize ' . ((&lines * 22 + 27) / 55)
exe 'vert 5resize ' . ((&columns * 79 + 54) / 108)
exe '6resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 6resize ' . ((&columns * 79 + 54) / 108)
exe '7resize ' . ((&lines * 2 + 27) / 55)
exe 'vert 7resize ' . ((&columns * 79 + 54) / 108)
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
