" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 08 enero 2015 at 17:33:51.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Monaco\ for\ Powerline\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'molokayo' | colorscheme molokayo | endif
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
badd +19 ginn/informes/nied.py
badd +1 formularios/auditviewer.py
badd +248 ginn/formularios/gtkexcepthook.py
badd +893 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1 ginn/formularios/partes_de_ancho_multiple.py
badd +427 ginn/formularios/consulta_producido.py
badd +302 ginn/formularios/consulta_consumo.py
badd +41 ginn/framework/memoize.py
badd +596 ginn/formularios/presupuesto.py
badd +44 ginn/formularios/listado_rollos.py
badd +89 ginn/informes/norma2013.py
badd +2711 ginn/formularios/consulta_global.py
badd +1 ginn/formularios/consulta_global.glade
badd +528 ginn/formularios/consumo_fibra_por_partida_gtx.py
badd +1 extra/scripts/clouseau.glade
badd +27 ginn/lib/pygal/pygal/__init__.py
badd +25 ginn/lib/pygal/pygal/config.py
badd +25 ginn/lib/pygal/pygal/style.py
badd +25 ginn/lib/pygal/pygal/adapters.py
badd +42 ginn/lib/pygal/pygal/ghost.py
badd +25 ginn/lib/pygal/pygal/graph/line.py
badd +28 ginn/lib/pygal/pygal/graph/graph.py
badd +29 ginn/lib/pygal/pygal/graph/base.py
badd +98 ginn/lib/pygal/pygal/svg.py
badd +90 ginn/formularios/custom_widgets/mapamundi.py
badd +329 ginn/lib/pygal/pygal/util.py
badd +25 ginn/lib/pygal/pygal/graph/stackedline.py
badd +26 ginn/lib/pygal/pygal/graph/xy.py
badd +26 ginn/lib/pygal/pygal/graph/bar.py
badd +24 ginn/lib/pygal/pygal/graph/horizontalbar.py
badd +1 ginn/lib/pygal/pygal/graph/horizontal.p
badd +24 ginn/lib/pygal/pygal/graph/horizontal.py
badd +27 ginn/lib/pygal/pygal/graph/stackedbar.py
badd +24 ginn/lib/pygal/pygal/graph/horizontalstackedbar.py
badd +27 ginn/lib/pygal/pygal/graph/pie.py
badd +28 ginn/lib/pygal/pygal/graph/radar.py
badd +1 ginn/lib/pygal/pygal/graph/funel.py
badd +27 ginn/lib/pygal/pygal/graph/funnel.py
badd +25 ginn/lib/pygal/pygal/graph/pyramid.py
badd +26 ginn/lib/pygal/pygal/graph/verticalpyramid.py
badd +27 ginn/lib/pygal/pygal/graph/dot.py
badd +27 ginn/lib/pygal/pygal/graph/gauge.py
badd +42 ginn/lib/pygal/pygal/graph/datey.py
badd +28 ginn/lib/pygal/pygal/graph/worldmap.py
badd +28 ginn/lib/pygal/pygal/graph/supranationalworldmap.py
badd +26 ginn/lib/pygal/pygal/graph/histogram.py
badd +26 ginn/lib/pygal/pygal/graph/box.py
badd +36 ginn/formularios/custom_widgets/cairoplot.py
badd +1 ginn/lib/cairoplot/cairoplot.py
badd +151 ginn/lib/cagraph/cagraph/ca_graph_file.py
badd +93 ginn/lib/cagraph/cagraph/axis/yaxis.py
badd +111 ginn/formularios/widgets.py
badd +1 ginn/lib/cairoplot/__init__.py
badd +1 ginn/lib/cagraph/cagraph/series/__init__.py
badd +84 ginn/lib/cagraph/cagraph/series/dna.py
badd +111 ginn/formularios/prefacturas.py
badd +5 ginn/formularios/launcher.py
badd +1 ginn/formularios/abonos_venta.glade
badd +513 ginn/formularios/crm_detalles_factura.py
badd +406 ginn/formularios/crm_seguimiento_impagos.py
badd +1 extra/scripts/clouseau-gtk.py
badd +3931 ginn/formularios/partes_de_fabricacion_rollos.py
badd +1 ginn/formularios/consulta_producciones_estandar.py
badd +606 ginn/formularios/consulta_pendientes_servir.py
badd +504 ginn/formularios/consulta_pagos_realizados.py
badd +21 ginn/lib/myprint.py
badd +399 ginn/formularios/auditviewer.py
badd +1 ginn/formularios/partes_de_fabricacion_bolsas.glade
badd +115 ginn/formularios/consulta_existenciasBolsas.py
badd +23 extra/scripts/bash_completion_ginn
badd +1249 ginn/formularios/consulta_ventas.py
badd +631 ginn/formularios/pagares_cobros.py
badd +1061 ginn/formularios/ventana.py
badd +52 ginn/formularios/consulta_pagos.py
badd +153 ginn/formularios/facturas_venta.py
badd +149 ginn/framework/pclases/facturaventa.py
badd +86 ginn/formularios/consulta_existencias.py
badd +10963 ginn/framework/pclases/__init__.py
badd +1403 ginn/formularios/partes_de_fabricacion_balas.py
badd +174 ginn/formularios/mail_sender.py
badd +54 ginn/formularios/consulta_pedidos_clientes.py
badd +52 ginn/formularios/consulta_productividad.py
badd +1 ginn/formularios/mail_sender.glade
badd +59 ginn/framework/pclases/facturadeabono.py
badd +226 ginn/informes/presupuesto2.py
badd +210 ginn/formularios/partes_de_trabajo.py
badd +1174 ginn/formularios/clientes.py
badd +65 ginn/formularios/menu.py
badd +7246 ginn/informes/geninformes.py
badd +0 ginn/formularios/presupuestos.py
args formularios/auditviewer.py
set lines=43 columns=102
edit ginn/formularios/partes_de_ancho_multiple.py
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
4wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 16 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 2resize ' . ((&columns * 85 + 51) / 102)
exe '3resize ' . ((&lines * 16 + 21) / 43)
exe 'vert 3resize ' . ((&columns * 85 + 51) / 102)
exe '4resize ' . ((&lines * 15 + 21) / 43)
exe 'vert 4resize ' . ((&columns * 85 + 51) / 102)
exe '5resize ' . ((&lines * 4 + 21) / 43)
exe 'vert 5resize ' . ((&columns * 85 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 6resize ' . ((&columns * 85 + 51) / 102)
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
let s:l = 22 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 011|
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
693
normal! zo
970
normal! zo
1698
normal! zo
2150
normal! zo
2197
normal! zo
2197
normal! zo
2197
normal! zo
2197
normal! zo
2200
normal! zo
2224
normal! zo
2249
normal! zo
2250
normal! zo
2467
normal! zo
5989
normal! zo
6069
normal! zo
7769
normal! zo
7775
normal! zo
10113
normal! zo
10153
normal! zo
10176
normal! zo
10179
normal! zo
10182
normal! zo
10184
normal! zo
10184
normal! zo
10184
normal! zo
10206
normal! zo
10222
normal! zo
10225
normal! zo
10606
normal! zo
10882
normal! zo
10888
normal! zo
10898
normal! zo
10913
normal! zo
10919
normal! zo
10929
normal! zo
10932
normal! zo
10951
normal! zo
10951
normal! zo
10951
normal! zo
10969
normal! zo
10972
normal! zo
10975
normal! zo
11019
normal! zo
11048
normal! zo
11051
normal! zo
11054
normal! zo
11056
normal! zo
11056
normal! zo
11056
normal! zo
11071
normal! zo
11072
normal! zo
11072
normal! zo
11074
normal! zo
11075
normal! zo
11075
normal! zo
16844
normal! zo
16869
normal! zo
16876
normal! zo
16876
normal! zo
16876
normal! zo
16886
normal! zo
16887
normal! zo
16894
normal! zo
16894
normal! zo
16901
normal! zo
16916
normal! zo
16936
normal! zo
17906
normal! zo
17915
normal! zo
17925
normal! zo
17938
normal! zo
17939
normal! zo
17941
normal! zo
let s:l = 10924 - ((11 * winheight(0) + 8) / 16)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10924
normal! 026|
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
77
normal! zo
1416
normal! zo
1465
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1776
normal! zo
1874
normal! zo
1885
normal! zo
1888
normal! zo
1954
normal! zo
2041
normal! zo
2043
normal! zo
2045
normal! zo
2047
normal! zo
2154
normal! zo
2308
normal! zo
3106
normal! zo
3489
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
let s:l = 1814 - ((7 * winheight(0) + 7) / 15)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1814
normal! 09|
lcd ~/Geotexan/src/Geotex-INN
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
111
normal! zo
112
normal! zo
126
normal! zo
126
normal! zo
312
normal! zo
388
normal! zo
388
normal! zo
413
normal! zo
467
normal! zo
468
normal! zo
468
normal! zo
468
normal! zo
503
normal! zo
508
normal! zo
510
normal! zo
522
normal! zo
530
normal! zo
532
normal! zo
533
normal! zo
536
normal! zo
549
normal! zo
549
normal! zo
549
normal! zo
565
normal! zo
570
normal! zo
577
normal! zo
578
normal! zo
578
normal! zo
582
normal! zo
589
normal! zo
589
normal! zo
595
normal! zo
607
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
611
normal! zo
619
normal! zo
620
normal! zo
620
normal! zo
620
normal! zo
626
normal! zo
645
normal! zo
658
normal! zo
665
normal! zo
666
normal! zo
674
normal! zo
675
normal! zo
675
normal! zo
675
normal! zo
675
normal! zo
689
normal! zo
689
normal! zo
689
normal! zo
689
normal! zo
689
normal! zo
695
normal! zo
695
normal! zo
695
normal! zo
695
normal! zo
695
normal! zo
695
normal! zo
707
normal! zo
707
normal! zo
707
normal! zo
707
normal! zo
711
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
728
normal! zo
733
normal! zo
745
normal! zo
751
normal! zo
751
normal! zo
751
normal! zo
754
normal! zo
754
normal! zo
754
normal! zo
764
normal! zo
768
normal! zo
768
normal! zo
777
normal! zo
778
normal! zo
787
normal! zo
787
normal! zo
787
normal! zo
787
normal! zo
787
normal! zo
798
normal! zo
809
normal! zo
812
normal! zo
813
normal! zo
813
normal! zo
822
normal! zo
823
normal! zo
823
normal! zo
823
normal! zo
823
normal! zo
824
normal! zo
841
normal! zo
864
normal! zo
884
normal! zo
904
normal! zo
925
normal! zo
930
normal! zo
939
normal! zo
950
normal! zo
959
normal! zo
960
normal! zo
960
normal! zo
960
normal! zo
965
normal! zo
965
normal! zo
968
normal! zo
968
normal! zo
980
normal! zo
982
normal! zo
985
normal! zo
998
normal! zo
1019
normal! zo
1019
normal! zo
1025
normal! zo
1042
normal! zo
1043
normal! zo
1064
normal! zo
1066
normal! zo
1070
normal! zo
1074
normal! zo
1090
normal! zo
1098
normal! zo
1099
normal! zo
1111
normal! zo
1117
normal! zo
1123
normal! zo
1129
normal! zo
1135
normal! zo
1141
normal! zo
1142
normal! zo
1146
normal! zo
1147
normal! zo
1147
normal! zo
1147
normal! zo
1153
normal! zo
1154
normal! zo
1163
normal! zo
1172
normal! zo
1175
normal! zo
1181
normal! zo
1187
normal! zo
1188
normal! zo
1188
normal! zo
1193
normal! zo
1201
normal! zo
1207
normal! zo
1236
normal! zo
1237
normal! zo
1239
normal! zo
1243
normal! zo
1244
normal! zo
1249
normal! zo
1258
normal! zo
1259
normal! zo
1263
normal! zo
1264
normal! zo
1275
normal! zo
1278
normal! zo
1295
normal! zo
1301
normal! zo
1313
normal! zo
1314
normal! zo
1314
normal! zo
1314
normal! zo
1314
normal! zo
1328
normal! zo
1359
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1368
normal! zo
1373
normal! zo
1382
normal! zo
1389
normal! zo
1389
normal! zo
1395
normal! zo
1400
normal! zo
1405
normal! zo
1406
normal! zo
1407
normal! zo
1412
normal! zo
1413
normal! zo
1413
normal! zo
1413
normal! zo
1413
normal! zo
1413
normal! zo
1413
normal! zo
1416
normal! zo
1424
normal! zo
1433
normal! zo
1446
normal! zo
1447
normal! zo
1452
normal! zo
1456
normal! zo
1464
normal! zo
1471
normal! zo
1481
normal! zo
1483
normal! zo
1490
normal! zo
1492
normal! zo
1515
normal! zo
1533
normal! zo
1535
normal! zo
1542
normal! zo
1544
normal! zo
1545
normal! zo
1545
normal! zo
1545
normal! zo
1553
normal! zo
1554
normal! zo
1554
normal! zo
1554
normal! zo
1558
normal! zo
1567
normal! zo
1568
normal! zo
1568
normal! zo
1568
normal! zo
1572
normal! zo
1582
normal! zo
1602
normal! zo
1606
normal! zo
1614
normal! zo
1615
normal! zo
1615
normal! zo
1615
normal! zo
1625
normal! zo
1644
normal! zo
1651
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1661
normal! zo
1669
normal! zo
1670
normal! zo
1670
normal! zo
1670
normal! zo
1686
normal! zo
1693
normal! zo
1694
normal! zo
1704
normal! zo
1712
normal! zo
1713
normal! zo
1713
normal! zo
1713
normal! zo
1725
normal! zo
1735
normal! zo
1735
normal! zo
1735
normal! zo
1735
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1759
normal! zo
1770
normal! zo
1771
normal! zo
1772
normal! zo
1774
normal! zo
1775
normal! zo
1775
normal! zo
1775
normal! zo
1775
normal! zo
1787
normal! zo
1798
normal! zo
1799
normal! zo
1799
normal! zo
1799
normal! zo
1804
normal! zo
1805
normal! zo
1819
normal! zo
1819
normal! zo
1820
normal! zo
1828
normal! zo
1829
normal! zo
1840
normal! zo
1846
normal! zo
1861
normal! zo
1873
normal! zo
1881
normal! zo
1881
normal! zo
1881
normal! zo
1881
normal! zo
1892
normal! zo
1903
normal! zo
1926
normal! zo
1948
normal! zo
1948
normal! zo
1948
normal! zo
1948
normal! zo
1960
normal! zo
1965
normal! zo
1981
normal! zo
1999
normal! zo
2019
normal! zo
2027
normal! zo
2030
normal! zo
2035
normal! zo
2044
normal! zo
2044
normal! zo
2053
normal! zo
2053
normal! zo
2054
normal! zo
2054
normal! zo
2054
normal! zo
2061
normal! zo
2062
normal! zo
2062
normal! zo
2062
normal! zo
2068
normal! zo
2076
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2092
normal! zo
2103
normal! zo
2114
normal! zo
2115
normal! zo
2118
normal! zo
2119
normal! zo
2119
normal! zo
2119
normal! zo
2123
normal! zo
2123
normal! zo
2123
normal! zo
2123
normal! zo
2129
normal! zo
2130
normal! zo
2130
normal! zo
2130
normal! zo
2134
normal! zo
2142
normal! zo
2152
normal! zo
2157
normal! zo
2158
normal! zo
2158
normal! zo
2158
normal! zo
2163
normal! zo
2181
normal! zo
2182
normal! zo
2183
normal! zo
2184
normal! zo
2184
normal! zo
2184
normal! zo
2188
normal! zo
2189
normal! zo
2190
normal! zo
2192
normal! zo
2194
normal! zo
2195
normal! zo
2195
normal! zo
2195
normal! zo
2199
normal! zo
2200
normal! zo
2200
normal! zo
2200
normal! zo
2206
normal! zo
2217
normal! zo
2222
normal! zo
2227
normal! zo
2228
normal! zo
2228
normal! zo
2229
normal! zo
2235
normal! zo
2260
normal! zo
2281
normal! zo
2332
normal! zo
2337
normal! zo
2446
normal! zo
2496
normal! zo
2559
normal! zo
2567
normal! zo
2572
normal! zo
2578
normal! zo
2585
normal! zo
2586
normal! zo
2608
normal! zo
2715
normal! zo
2716
normal! zo
2716
normal! zo
2753
normal! zo
2757
normal! zo
2771
normal! zo
2841
normal! zo
2914
normal! zo
2918
normal! zo
2918
normal! zo
2918
normal! zo
2925
normal! zo
2929
normal! zo
2929
normal! zo
2929
normal! zo
3168
normal! zo
3224
normal! zo
3231
normal! zo
3253
normal! zo
3258
normal! zo
3258
normal! zo
3281
normal! zo
3308
normal! zo
3318
normal! zo
3319
normal! zo
3321
normal! zo
3327
normal! zo
3329
normal! zo
3331
normal! zo
3351
normal! zo
3364
normal! zo
3724
normal! zo
3732
normal! zo
3748
normal! zo
3760
normal! zo
3777
normal! zo
3786
normal! zo
3800
normal! zo
3800
normal! zo
3802
normal! zo
3802
normal! zo
3802
normal! zo
4218
normal! zo
let s:l = 1067 - ((0 * winheight(0) + 2) / 4)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1067
normal! 0135|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_rollos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
113
normal! zo
128
normal! zo
130
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
132
normal! zo
235
normal! zo
236
normal! zo
306
normal! zo
307
normal! zo
1075
normal! zo
1094
normal! zo
1114
normal! zo
1115
normal! zo
1115
normal! zo
1118
normal! zo
1119
normal! zo
1119
normal! zo
1122
normal! zo
1123
normal! zo
1123
normal! zo
1126
normal! zo
1127
normal! zo
1127
normal! zo
1657
normal! zo
1668
normal! zo
1682
normal! zo
1815
normal! zo
1827
normal! zo
1830
normal! zo
1831
normal! zo
2019
normal! zo
2064
normal! zo
2958
normal! zo
2976
normal! zo
3039
normal! zo
3092
normal! zo
3109
normal! zo
3114
normal! zo
3114
normal! zo
3114
normal! zo
3114
normal! zo
3114
normal! zo
3117
normal! zo
3117
normal! zo
3122
normal! zo
3123
normal! zo
3125
normal! zo
3125
normal! zo
3125
normal! zo
3125
normal! zo
3127
normal! zo
3130
normal! zo
3130
normal! zo
3136
normal! zo
3142
normal! zo
3147
normal! zo
3154
normal! zo
3160
normal! zo
3166
normal! zo
3175
normal! zo
3217
normal! zo
3238
normal! zo
3240
normal! zo
3282
normal! zo
3294
normal! zo
3310
normal! zo
3318
normal! zo
3417
normal! zo
3429
normal! zo
3466
normal! zo
3474
normal! zo
3475
normal! zo
3476
normal! zo
3481
normal! zo
3482
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3520
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3534
normal! zo
3538
normal! zo
3538
normal! zo
3538
normal! zo
3538
normal! zo
3538
normal! zo
3539
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3544
normal! zo
3545
normal! zo
3545
normal! zo
3545
normal! zo
3546
normal! zo
3549
normal! zo
3552
normal! zo
3556
normal! zo
3561
normal! zo
3562
normal! zo
3562
normal! zo
3566
normal! zo
3581
normal! zo
3638
normal! zo
3646
normal! zo
3648
normal! zo
3651
normal! zo
3653
normal! zo
3712
normal! zo
3720
normal! zo
3721
normal! zo
3731
normal! zo
3732
normal! zo
3736
normal! zo
3737
normal! zo
3754
normal! zo
3799
normal! zo
3799
normal! zo
3799
normal! zo
3806
normal! zo
3842
normal! zo
3864
normal! zo
3883
normal! zo
3884
normal! zo
3886
normal! zo
3891
normal! zo
3891
normal! zo
3891
normal! zo
3891
normal! zo
3891
normal! zo
3926
normal! zo
3951
normal! zo
3952
normal! zo
3956
normal! zo
3958
normal! zo
3958
normal! zo
3960
normal! zo
3960
normal! zo
3960
normal! zo
let s:l = 1716 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1716
normal! 013|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 16 + 51) / 102)
exe '2resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 2resize ' . ((&columns * 85 + 51) / 102)
exe '3resize ' . ((&lines * 16 + 21) / 43)
exe 'vert 3resize ' . ((&columns * 85 + 51) / 102)
exe '4resize ' . ((&lines * 15 + 21) / 43)
exe 'vert 4resize ' . ((&columns * 85 + 51) / 102)
exe '5resize ' . ((&lines * 4 + 21) / 43)
exe 'vert 5resize ' . ((&columns * 85 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 6resize ' . ((&columns * 85 + 51) / 102)
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
