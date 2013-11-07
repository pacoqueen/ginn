" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 07 noviembre 2013 at 07:58:15.
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
badd +353 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +127 ginn/formularios/clientes.py
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
badd +1637 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1627 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +908 ginn/formularios/ventana.py
badd +1899 ginn/formularios/pedidos_de_venta.py
badd +1 db/tablas.sql
badd +3038 ginn/formularios/albaranes_de_salida.py
badd +227 ginn/formularios/presupuesto.py
badd +1160 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +693 ginn/formularios/facturas_compra.py
badd +4379 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +218 ginn/formularios/gtkexcepthook.py
badd +407 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +61 ginn/framework/pclases/facturaventa.py
badd +689 ginn/formularios/consulta_mensual_nominas.py
badd +115 ginn/informes/treeview2pdf.py
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
badd +510 ginn/framework/pclases/cliente.py
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
badd +150 ginn/informes/presupuesto2.py
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
badd +51 ginn/formularios/consulta_ofertas.py
badd +24 extra/patches/create_ventana_consultas.py
args formularios/auditviewer.py
set lines=42 columns=80
edit db/tablas.sql
set splitbelow splitright
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
exe '1resize ' . ((&lines * 1 + 21) / 42)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe '3resize ' . ((&lines * 1 + 21) / 42)
exe '4resize ' . ((&lines * 1 + 21) / 42)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe '6resize ' . ((&lines * 12 + 21) / 42)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe '8resize ' . ((&lines * 1 + 21) / 42)
exe '9resize ' . ((&lines * 1 + 21) / 42)
exe '10resize ' . ((&lines * 11 + 21) / 42)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
1016
normal! zo
1408
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3774
normal! zo
let s:l = 59 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
59
normal! 02|
wincmd w
argglobal
edit ginn/framework/pclases/__init__.py
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
10981
normal! zo
10995
normal! zo
10995
normal! zo
10995
normal! zo
10995
normal! zo
14269
normal! zo
14296
normal! zo
14301
normal! zo
14383
normal! zo
14405
normal! zo
14406
normal! zo
14416
normal! zo
14468
normal! zo
14503
normal! zo
14508
normal! zo
14509
normal! zo
15043
normal! zo
15048
normal! zo
15048
normal! zo
15048
normal! zo
15048
normal! zo
15292
normal! zo
15305
normal! zo
15315
normal! zo
15418
normal! zo
15422
normal! zo
15422
normal! zo
15422
normal! zo
15422
normal! zo
15422
normal! zo
15426
normal! zo
15426
normal! zo
15426
normal! zo
15426
normal! zo
15468
normal! zo
15471
normal! zo
15471
normal! zo
15471
normal! zo
15471
normal! zo
16210
normal! zo
16598
normal! zo
16609
normal! zo
16609
normal! zo
16609
normal! zo
16609
normal! zo
16640
normal! zo
16648
normal! zo
16648
normal! zo
16648
normal! zo
16648
normal! zo
16963
normal! zo
17159
normal! zo
18014
normal! zo
18024
normal! zo
18113
normal! zo
18123
normal! zo
18158
normal! zo
18165
normal! zo
18172
normal! zo
18173
normal! zo
18173
normal! zo
18173
normal! zo
18175
normal! zo
18176
normal! zo
18176
normal! zo
18176
normal! zo
18252
normal! zo
18319
normal! zo
18330
normal! zo
18380
normal! zo
18437
normal! zo
18447
normal! zo
18495
normal! zo
18548
normal! zo
18789
normal! zo
18811
normal! zo
18870
normal! zo
19068
normal! zo
19537
normal! zo
19776
normal! zo
19949
normal! zo
19953
normal! zo
19953
normal! zo
20042
normal! zo
20105
normal! zo
20427
normal! zo
let s:l = 15019 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15019
normal! 0
wincmd w
argglobal
edit ginn/framework/seeker.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
235
normal! zo
let s:l = 415 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
415
normal! 011|
lcd ~/Geotexan/src/Geotex-INN
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
1044
normal! zo
1060
normal! zo
1080
normal! zo
1081
normal! zo
1081
normal! zo
1082
normal! zo
1087
normal! zo
1103
normal! zo
1110
normal! zo
1112
normal! zo
1149
normal! zo
1153
normal! zo
1162
normal! zo
1170
normal! zo
1193
normal! zo
1193
normal! zo
1203
normal! zo
1255
normal! zo
1255
normal! zo
1270
normal! zo
1279
normal! zo
1280
normal! zo
1317
normal! zo
1328
normal! zo
1346
normal! zo
1354
normal! zo
1355
normal! zo
1360
normal! zo
1369
normal! zo
1375
normal! zo
1379
normal! zo
1382
normal! zo
1388
normal! zo
1399
normal! zo
1402
normal! zo
1408
normal! zo
1416
normal! zo
1435
normal! zo
1454
normal! zo
1461
normal! zo
1465
normal! zo
1468
normal! zo
1484
normal! zo
1495
normal! zo
1527
normal! zo
1535
normal! zo
1553
normal! zo
1556
normal! zo
1565
normal! zo
1565
normal! zo
1565
normal! zo
1565
normal! zo
1565
normal! zo
1565
normal! zo
1571
normal! zo
1575
normal! zo
1579
normal! zo
1585
normal! zo
1586
normal! zo
1586
normal! zo
1586
normal! zo
1586
normal! zo
1586
normal! zo
1614
normal! zo
1616
normal! zo
1618
normal! zo
1618
normal! zo
1633
normal! zo
1654
normal! zo
1674
normal! zo
1683
normal! zo
1684
normal! zo
1722
normal! zo
1733
normal! zo
1777
normal! zo
1793
normal! zo
1794
normal! zo
1798
normal! zo
1802
normal! zo
1802
normal! zo
1806
normal! zo
1809
normal! zo
1817
normal! zo
1861
normal! zo
1892
normal! zo
1893
normal! zo
1901
normal! zo
1901
normal! zo
1954
normal! zo
1972
normal! zo
1977
normal! zo
1987
normal! zo
1991
normal! zo
1995
normal! zo
1996
normal! zo
1997
normal! zo
1997
normal! zo
1997
normal! zo
1997
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
2007
normal! zo
2019
normal! zo
2023
normal! zo
2025
normal! zo
2042
normal! zo
2052
normal! zo
2071
normal! zo
2072
normal! zo
2073
normal! zo
2075
normal! zo
2075
normal! zo
2075
normal! zo
2075
normal! zo
2078
normal! zo
2078
normal! zo
2079
normal! zo
2081
normal! zo
2109
normal! zo
2130
normal! zo
2157
normal! zo
2174
normal! zo
2196
normal! zo
2201
normal! zo
2215
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2223
normal! zo
2227
normal! zo
2235
normal! zo
2241
normal! zo
2247
normal! zo
2248
normal! zo
2252
normal! zo
2252
normal! zo
2261
normal! zo
2307
normal! zo
2318
normal! zo
2318
normal! zo
2318
normal! zo
2318
normal! zo
2318
normal! zo
2318
normal! zo
2318
normal! zo
2321
normal! zo
2321
normal! zo
2321
normal! zo
2321
normal! zo
2321
normal! zo
2321
normal! zo
2322
normal! zo
2326
normal! zo
2334
normal! zo
2339
normal! zo
2342
normal! zo
2402
normal! zo
2416
normal! zo
2418
normal! zo
2465
normal! zo
2466
normal! zo
2466
normal! zo
2476
normal! zo
2481
normal! zo
2485
normal! zo
2491
normal! zo
2504
normal! zo
2504
normal! zo
2510
normal! zo
2510
normal! zo
2518
normal! zo
2531
normal! zo
2531
normal! zo
2535
normal! zo
2535
normal! zo
2543
normal! zo
2552
normal! zo
2570
normal! zo
2573
normal! zo
2574
normal! zo
2581
normal! zo
2623
normal! zo
2626
normal! zo
2627
normal! zo
2650
normal! zo
2661
normal! zo
2668
normal! zo
2677
normal! zo
2678
normal! zo
2678
normal! zo
2679
normal! zo
2679
normal! zo
2680
normal! zo
2681
normal! zo
2686
normal! zo
2690
normal! zo
2693
normal! zo
2694
normal! zo
2694
normal! zo
2695
normal! zo
2699
normal! zo
2700
normal! zo
2709
normal! zo
2714
normal! zo
2716
normal! zo
2716
normal! zo
2717
normal! zo
2717
normal! zo
2722
normal! zo
2723
normal! zo
2737
normal! zo
2739
normal! zo
2744
normal! zo
2747
normal! zo
2748
normal! zo
2809
normal! zo
2824
normal! zo
2828
normal! zo
let s:l = 2107 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2107
normal! 037|
lcd ~/Geotexan/src/Geotex-INN
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
286
normal! zo
476
normal! zo
476
normal! zo
476
normal! zo
476
normal! zo
496
normal! zo
675
normal! zo
675
normal! zo
675
normal! zo
675
normal! zo
693
normal! zo
739
normal! zo
757
normal! zo
757
normal! zo
757
normal! zo
757
normal! zo
769
normal! zo
813
normal! zo
835
normal! zo
835
normal! zo
835
normal! zo
835
normal! zo
847
normal! zo
882
normal! zo
882
normal! zo
882
normal! zo
882
normal! zo
2903
normal! zo
2940
normal! zo
3060
normal! zo
3435
normal! zo
3436
normal! zo
3570
normal! zo
3592
normal! zo
3601
normal! zo
3621
normal! zo
3818
normal! zo
3912
normal! zo
4315
normal! zo
4324
normal! zo
4440
normal! zo
4522
normal! zo
4872
normal! zo
5083
normal! zo
5096
normal! zo
5114
normal! zo
5123
normal! zo
5222
normal! zo
5240
normal! zo
5251
normal! zo
5264
normal! zo
5268
normal! zo
5709
normal! zo
5725
normal! zo
5824
normal! zo
5840
normal! zo
6228
normal! zo
6228
normal! zo
6434
normal! zo
6448
normal! zo
6482
normal! zo
6671
normal! zo
6704
normal! zo
6787
normal! zo
6799
normal! zo
6800
normal! zo
9527
normal! zo
9539
normal! zo
9539
normal! zo
9539
normal! zo
11697
normal! zo
let s:l = 6227 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
6227
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/informes/treeview2pdf.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
37
normal! zo
37
normal! zo
37
normal! zo
66
normal! zo
69
normal! zo
74
normal! zo
81
normal! zo
111
normal! zo
111
normal! zo
111
normal! zo
111
normal! zo
111
normal! zo
111
normal! zo
let s:l = 68 - ((4 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
68
normal! 0126|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_ofertas.py
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
52
normal! zo
60
normal! zo
60
normal! zo
86
normal! zo
86
normal! zo
87
normal! zo
87
normal! zo
89
normal! zo
89
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
107
normal! zo
107
normal! zo
154
normal! zo
155
normal! zo
160
normal! zo
178
normal! zo
202
normal! zo
203
normal! zo
215
normal! zo
216
normal! zo
222
normal! zo
223
normal! zo
229
normal! zo
261
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
262
normal! zo
262
normal! zo
262
normal! zo
262
normal! zo
264
normal! zo
265
normal! zo
265
normal! zo
265
normal! zo
265
normal! zo
265
normal! zo
265
normal! zo
265
normal! zo
265
normal! zo
265
normal! zo
270
normal! zo
272
normal! zo
273
normal! zo
274
normal! zo
310
normal! zo
320
normal! zo
324
normal! zo
324
normal! zo
330
normal! zo
330
normal! zo
352
normal! zo
356
normal! zo
356
normal! zo
358
normal! zo
378
normal! zo
389
normal! zo
390
normal! zo
395
normal! zo
402
normal! zo
428
normal! zo
435
normal! zo
438
normal! zo
438
normal! zo
438
normal! zo
438
normal! zo
438
normal! zo
438
normal! zo
438
normal! zo
452
normal! zo
463
normal! zo
469
normal! zo
481
normal! zo
482
normal! zo
487
normal! zo
518
normal! zo
550
normal! zo
556
normal! zo
568
normal! zo
569
normal! zo
574
normal! zo
581
normal! zo
588
normal! zo
588
normal! zo
604
normal! zo
607
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
612
normal! zo
635
normal! zo
641
normal! zo
648
normal! zo
653
normal! zo
654
normal! zo
655
normal! zo
655
normal! zo
655
normal! zo
655
normal! zo
655
normal! zo
655
normal! zo
655
normal! zo
655
normal! zo
655
normal! zo
659
normal! zo
660
normal! zo
673
normal! zo
673
normal! zo
683
normal! zo
685
normal! zo
695
normal! zo
732
normal! zo
744
normal! zo
764
normal! zo
770
normal! zo
774
normal! zo
774
normal! zo
786
normal! zo
790
normal! zo
790
normal! zo
803
normal! zo
807
normal! zo
807
normal! zo
818
normal! zo
822
normal! zo
822
normal! zo
830
normal! zo
834
normal! zo
834
normal! zo
856
normal! zo
856
normal! zo
856
normal! zo
856
normal! zo
856
normal! zo
856
normal! zo
861
normal! zo
861
normal! zo
861
normal! zo
861
normal! zo
861
normal! zo
861
normal! zo
861
normal! zo
864
normal! zo
864
normal! zo
864
normal! zo
864
normal! zo
864
normal! zo
864
normal! zo
let s:l = 163 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
163
normal! 072|
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
143
normal! zo
195
normal! zo
277
normal! zo
361
normal! zo
426
normal! zo
469
normal! zo
647
normal! zo
733
normal! zo
let s:l = 754 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
754
normal! 041|
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
66
normal! zo
70
normal! zo
97
normal! zo
108
normal! zo
let s:l = 28 - ((2 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
28
normal! 013|
wincmd w
6wincmd w
exe '1resize ' . ((&lines * 1 + 21) / 42)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe '3resize ' . ((&lines * 1 + 21) / 42)
exe '4resize ' . ((&lines * 1 + 21) / 42)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe '6resize ' . ((&lines * 12 + 21) / 42)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe '8resize ' . ((&lines * 1 + 21) / 42)
exe '9resize ' . ((&lines * 1 + 21) / 42)
exe '10resize ' . ((&lines * 11 + 21) / 42)
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
