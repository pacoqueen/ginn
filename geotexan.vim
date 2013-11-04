" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 04 noviembre 2013 at 19:40:45.
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
badd +3041 ginn/formularios/albaranes_de_salida.py
badd +170 ginn/formularios/presupuesto.py
badd +2491 ginn/formularios/presupuestos.py
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
badd +269 ginn/informes/treeview2pdf.py
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
args formularios/auditviewer.py
set lines=55 columns=102
edit db/tablas.sql
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
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 14 + 27) / 55)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 17 + 27) / 55)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 7 + 27) / 55)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 6 + 27) / 55)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
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
let s:l = 14298 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
14298
normal! 018|
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
let s:l = 415 - ((10 * winheight(0) + 7) / 14)
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
219
normal! zo
222
normal! zo
224
normal! zo
229
normal! zo
230
normal! zo
234
normal! zo
235
normal! zo
246
normal! zo
247
normal! zo
248
normal! zo
264
normal! zo
265
normal! zo
266
normal! zo
268
normal! zo
268
normal! zo
275
normal! zo
279
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
313
normal! zo
313
normal! zo
313
normal! zo
313
normal! zo
320
normal! zo
321
normal! zo
322
normal! zo
331
normal! zo
347
normal! zo
348
normal! zo
348
normal! zo
349
normal! zo
354
normal! zo
357
normal! zo
363
normal! zo
374
normal! zo
395
normal! zo
400
normal! zo
411
normal! zo
411
normal! zo
412
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
432
normal! zo
443
normal! zo
446
normal! zo
446
normal! zo
446
normal! zo
447
normal! zo
452
normal! zo
470
normal! zo
470
normal! zo
478
normal! zo
480
normal! zo
481
normal! zo
482
normal! zo
483
normal! zo
493
normal! zo
495
normal! zo
496
normal! zo
513
normal! zo
526
normal! zo
527
normal! zo
538
normal! zo
550
normal! zo
550
normal! zo
558
normal! zo
559
normal! zo
566
normal! zo
576
normal! zo
576
normal! zo
584
normal! zo
584
normal! zo
585
normal! zo
593
normal! zo
593
normal! zo
601
normal! zo
606
normal! zo
606
normal! zo
606
normal! zo
606
normal! zo
606
normal! zo
610
normal! zo
612
normal! zo
615
normal! zo
628
normal! zo
647
normal! zo
655
normal! zo
666
normal! zo
677
normal! zo
681
normal! zo
682
normal! zo
692
normal! zo
698
normal! zo
701
normal! zo
732
normal! zo
751
normal! zo
753
normal! zo
753
normal! zo
753
normal! zo
753
normal! zo
753
normal! zo
759
normal! zo
773
normal! zo
780
normal! zo
780
normal! zo
781
normal! zo
784
normal! zo
788
normal! zo
789
normal! zo
796
normal! zo
804
normal! zo
811
normal! zo
822
normal! zo
824
normal! zo
846
normal! zo
879
normal! zo
894
normal! zo
904
normal! zo
923
normal! zo
963
normal! zo
972
normal! zo
979
normal! zo
979
normal! zo
984
normal! zo
985
normal! zo
990
normal! zo
992
normal! zo
1007
normal! zo
1025
normal! zo
1040
normal! zo
1056
normal! zo
1072
normal! zo
1072
normal! zo
1072
normal! zo
1072
normal! zo
1072
normal! zo
1072
normal! zo
1083
normal! zo
1088
normal! zo
1089
normal! zo
1089
normal! zo
1090
normal! zo
1099
normal! zo
1106
normal! zo
1108
normal! zo
1110
normal! zo
1111
normal! zo
1111
normal! zo
1111
normal! zo
1111
normal! zo
1111
normal! zo
1111
normal! zo
1111
normal! zo
1113
normal! zo
1119
normal! zo
1132
normal! zo
1136
normal! zo
1145
normal! zo
1149
normal! zo
1150
normal! zo
1150
normal! zo
1158
normal! zo
1163
normal! zo
1259
normal! zo
1166
normal! zo
1176
normal! zo
1176
normal! zo
1176
normal! zo
1176
normal! zo
1176
normal! zo
1176
normal! zo
1176
normal! zo
1176
normal! zo
1189
normal! zo
1189
normal! zo
1199
normal! zo
1205
normal! zo
1205
normal! zo
1205
normal! zo
1205
normal! zo
1205
normal! zo
1205
normal! zo
1205
normal! zo
1205
normal! zo
1205
normal! zo
1205
normal! zo
1205
normal! zo
1212
normal! zo
1235
normal! zo
1235
normal! zo
1235
normal! zo
1235
normal! zo
1235
normal! zo
1244
normal! zo
1244
normal! zo
1244
normal! zo
1244
normal! zo
1244
normal! zo
1244
normal! zo
1251
normal! zo
1251
normal! zo
1264
normal! zo
1266
normal! zo
1275
normal! zo
1276
normal! zo
1280
normal! zo
1313
normal! zo
1315
normal! zo
1317
normal! zo
1324
normal! zo
1328
normal! zo
1350
normal! zo
1351
normal! zo
1352
normal! zo
1356
normal! zo
1365
normal! zo
1371
normal! zo
1372
normal! zo
1373
normal! zo
1375
normal! zo
1378
normal! zo
1384
normal! zo
1395
normal! zo
1398
normal! zo
1404
normal! zo
1405
normal! zo
1412
normal! zo
1431
normal! zo
1435
normal! zo
1447
normal! zo
1450
normal! zo
1457
normal! zo
1458
normal! zo
1461
normal! zo
1464
normal! zo
1473
normal! zo
1473
normal! zo
1473
normal! zo
1523
normal! zo
1531
normal! zo
1533
normal! zo
1533
normal! zo
1533
normal! zo
1533
normal! zo
1541
normal! zo
1541
normal! zo
1541
normal! zo
1541
normal! zo
1541
normal! zo
1544
normal! zo
1547
normal! zo
1546
normal! zo
1546
normal! zo
1549
normal! zo
1552
normal! zo
1553
normal! zo
1553
normal! zo
1553
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
1565
normal! zo
1566
normal! zo
1570
normal! zo
1579
normal! zo
1567
normal! zo
1571
normal! zo
1575
normal! zo
1581
normal! zo
1582
normal! zo
1582
normal! zo
1582
normal! zo
1582
normal! zo
1582
normal! zo
1584
normal! zo
1586
normal! zo
1587
normal! zo
1598
normal! zo
1598
normal! zo
1598
normal! zo
1604
normal! zo
1604
normal! zo
1604
normal! zo
1604
normal! zo
1610
normal! zo
1612
normal! zo
1614
normal! zo
1614
normal! zo
1619
normal! zo
1629
normal! zo
1637
normal! zo
1654
normal! zo
1655
normal! zo
1657
normal! zo
1658
normal! zo
1659
normal! zo
1670
normal! zo
1679
normal! zo
1680
normal! zo
1685
normal! zo
1686
normal! zo
1694
normal! zo
1696
normal! zo
1718
normal! zo
1726
normal! zo
1731
normal! zo
1729
normal! zo
1736
normal! zo
1742
normal! zo
1742
normal! zo
1742
normal! zo
1762
normal! zo
1763
normal! zo
1769
normal! zo
1770
normal! zo
1778
normal! zo
1794
normal! zo
1798
normal! zo
1798
normal! zo
1802
normal! zo
1805
normal! zo
1806
normal! zo
1808
normal! zo
1809
normal! zo
1820
normal! zo
1821
normal! zo
1821
normal! zo
1821
normal! zo
1821
normal! zo
1838
normal! zo
1841
normal! zo
1843
normal! zo
1857
normal! zo
1885
normal! zo
1892
normal! zo
1892
normal! zo
1905
normal! zo
1906
normal! zo
1888
normal! zo
1889
normal! zo
1897
normal! zo
1897
normal! zo
1910
normal! zo
1911
normal! zo
1943
normal! zo
1950
normal! zo
1950
normal! zo
1950
normal! zo
1950
normal! zo
1950
normal! zo
1950
normal! zo
1950
normal! zo
1973
normal! zo
1975
normal! zo
1983
normal! zo
1987
normal! zo
1991
normal! zo
1992
normal! zo
1993
normal! zo
1993
normal! zo
1993
normal! zo
1993
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
2007
normal! zo
2007
normal! zo
2007
normal! zo
2015
normal! zo
2019
normal! zo
2025
normal! zo
2026
normal! zo
2029
normal! zo
2029
normal! zo
2038
normal! zo
2048
normal! zo
2062
normal! zo
2065
normal! zo
2065
normal! zo
2069
normal! zo
2069
normal! zo
2070
normal! zo
2072
normal! zo
2074
normal! zo
2074
normal! zo
2076
normal! zo
2077
normal! zo
2077
normal! zo
2067
normal! zo
2068
normal! zo
2069
normal! zo
2071
normal! zo
2071
normal! zo
2071
normal! zo
2071
normal! zo
2074
normal! zo
2074
normal! zo
2075
normal! zo
2077
normal! zo
2079
normal! zo
2079
normal! zo
2081
normal! zo
2082
normal! zo
2082
normal! zo
2094
normal! zo
2094
normal! zo
2094
normal! zo
2094
normal! zo
2094
normal! zo
2094
normal! zo
2094
normal! zo
2094
normal! zo
2105
normal! zo
2109
normal! zo
2110
normal! zo
2110
normal! zo
2110
normal! zo
2110
normal! zo
2110
normal! zo
2110
normal! zo
2126
normal! zo
2128
normal! zo
2150
normal! zo
2153
normal! zo
2170
normal! zo
2181
normal! zo
2192
normal! zo
2197
normal! zo
2211
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2219
normal! zo
2223
normal! zo
2224
normal! zo
2225
normal! zo
2225
normal! zo
2225
normal! zo
2225
normal! zo
2225
normal! zo
2225
normal! zo
2225
normal! zo
2225
normal! zo
2231
normal! zo
2237
normal! zo
2243
normal! zo
2244
normal! zo
2245
normal! zo
2248
normal! zo
2248
normal! zo
2257
normal! zo
2294
normal! zo
2294
normal! zo
2294
normal! zo
2303
normal! zo
2317
normal! zo
2317
normal! zo
2317
normal! zo
2317
normal! zo
2317
normal! zo
2317
normal! zo
2318
normal! zo
2353
normal! zo
2353
normal! zo
2322
normal! zo
2330
normal! zo
2335
normal! zo
2336
normal! zo
2336
normal! zo
2336
normal! zo
2336
normal! zo
2338
normal! zo
2339
normal! zo
2339
normal! zo
2339
normal! zo
2339
normal! zo
2341
normal! zo
2342
normal! zo
2342
normal! zo
2342
normal! zo
2342
normal! zo
2355
normal! zo
2355
normal! zo
2355
normal! zo
2355
normal! zo
2355
normal! zo
2355
normal! zo
2358
normal! zo
2358
normal! zo
2368
normal! zo
2368
normal! zo
2369
normal! zo
2384
normal! zo
2385
normal! zo
2386
normal! zo
2398
normal! zo
2412
normal! zo
2414
normal! zo
2429
normal! zo
2461
normal! zo
2462
normal! zo
2462
normal! zo
2463
normal! zo
2469
normal! zo
2472
normal! zo
2477
normal! zo
2481
normal! zo
2487
normal! zo
2488
normal! zo
2488
normal! zo
2495
normal! zo
2496
normal! zo
2500
normal! zo
2500
normal! zo
2506
normal! zo
2506
normal! zo
2514
normal! zo
2531
normal! zo
2531
normal! zo
2539
normal! zo
2548
normal! zo
2555
normal! zo
2557
normal! zo
2557
normal! zo
2557
normal! zo
2566
normal! zo
2567
normal! zo
2572
normal! zo
2577
normal! zo
2577
normal! zo
2577
normal! zo
2577
normal! zo
2569
normal! zo
2570
normal! zo
2570
normal! zo
2571
normal! zo
2571
normal! zo
2571
normal! zo
2571
normal! zo
2571
normal! zo
2571
normal! zo
2571
normal! zo
2577
normal! zo
2579
normal! zo
2582
normal! zo
2582
normal! zo
2582
normal! zo
2582
normal! zo
2593
normal! zo
2619
normal! zo
2622
normal! zo
2623
normal! zo
2624
normal! zo
2626
normal! zo
2627
normal! zo
2657
normal! zo
2681
normal! zo
2684
normal! zo
2685
normal! zo
2685
normal! zo
2690
normal! zo
2691
normal! zo
2692
normal! zo
2692
normal! zo
2700
normal! zo
2705
normal! zo
2707
normal! zo
2707
normal! zo
2708
normal! zo
2708
normal! zo
2664
normal! zo
2673
normal! zo
2674
normal! zo
2674
normal! zo
2675
normal! zo
2675
normal! zo
2676
normal! zo
2677
normal! zo
2682
normal! zo
2686
normal! zo
2689
normal! zo
2690
normal! zo
2690
normal! zo
2691
normal! zo
2695
normal! zo
2696
normal! zo
2697
normal! zo
2697
normal! zo
2705
normal! zo
2710
normal! zo
2712
normal! zo
2712
normal! zo
2713
normal! zo
2713
normal! zo
2718
normal! zo
2719
normal! zo
2726
normal! zo
2733
normal! zo
2735
normal! zo
2738
normal! zo
2739
normal! zo
2740
normal! zo
2743
normal! zo
2744
normal! zo
2753
normal! zo
2754
normal! zo
2820
normal! zo
2824
normal! zo
2825
normal! zo
2827
normal! zo
2828
normal! zo
let s:l = 1146 - ((13 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1146
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
normal! 0250|
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
let s:l = 1 - ((0 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
let s:l = 77 - ((0 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
77
normal! 030|
wincmd w
5wincmd w
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 14 + 27) / 55)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 17 + 27) / 55)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 7 + 27) / 55)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 6 + 27) / 55)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
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
