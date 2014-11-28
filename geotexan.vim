" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 28 noviembre 2014 at 10:25:50.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Source\ Code\ Pro\ 10
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
badd +1 ginn/formularios/partes_de_fabricacion_rollos.py
badd +1 ginn/formularios/consulta_producciones_estandar.py
badd +606 ginn/formularios/consulta_pendientes_servir.py
badd +504 ginn/formularios/consulta_pagos_realizados.py
badd +21 ginn/lib/myprint.py
badd +399 ginn/formularios/auditviewer.py
badd +1 ginn/formularios/partes_de_fabricacion_bolsas.glade
badd +115 ginn/formularios/consulta_existenciasBolsas.py
badd +23 extra/scripts/bash_completion_ginn
badd +16 ginn/formularios/consulta_ventas.py
badd +631 ginn/formularios/pagares_cobros.py
badd +916 ginn/framework/pclases/superfacturaventa.py
badd +1061 ginn/formularios/ventana.py
badd +52 ginn/formularios/consulta_pagos.py
badd +153 ginn/formularios/facturas_venta.py
badd +239 ginn/framework/pclases/facturaventa.py
badd +86 ginn/formularios/consulta_existencias.py
badd +10963 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +3592 ginn/formularios/presupuestos.py
badd +174 ginn/formularios/mail_sender.py
badd +54 ginn/formularios/consulta_pedidos_clientes.py
badd +52 ginn/formularios/consulta_productividad.py
badd +1 ginn/formularios/mail_sender.glade
badd +721 ginn/formularios/facturas_compra.py
badd +4498 ginn/formularios/utils.py
badd +59 ginn/framework/pclases/facturadeabono.py
badd +226 ginn/informes/presupuesto2.py
badd +210 ginn/formularios/partes_de_trabajo.py
badd +437 db/tablas.sql
badd +1174 ginn/formularios/clientes.py
badd +65 ginn/formularios/menu.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=42 columns=102
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
exe 'vert 1resize ' . ((&columns * 19 + 51) / 102)
exe '2resize ' . ((&lines * 7 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 82 + 51) / 102)
exe '3resize ' . ((&lines * 6 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 82 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 82 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 82 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 82 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 82 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 8resize ' . ((&columns * 82 + 51) / 102)
exe '9resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 9resize ' . ((&columns * 82 + 51) / 102)
exe '10resize ' . ((&lines * 13 + 21) / 42)
exe 'vert 10resize ' . ((&columns * 82 + 51) / 102)
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
let s:l = 22 - ((0 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 011|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/pclases/facturaventa.py
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
let s:l = 346 - ((0 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
346
normal! 027|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/pclases/superfacturaventa.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
53
normal! zo
531
normal! zo
537
normal! zo
538
normal! zo
542
normal! zo
543
normal! zo
let s:l = 150 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
150
normal! 022|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_ventas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
55
normal! zo
60
normal! zo
815
normal! zo
901
normal! zo
1061
normal! zo
1073
normal! zo
1167
normal! zo
1169
normal! zo
1177
normal! zo
1177
normal! zo
1177
normal! zo
1177
normal! zo
1177
normal! zo
1177
normal! zo
1181
normal! zo
1181
normal! zo
1181
normal! zo
1181
normal! zo
1181
normal! zo
1181
normal! zo
1181
normal! zo
1185
normal! zo
1185
normal! zo
1185
normal! zo
1185
normal! zo
1185
normal! zo
1185
normal! zo
1189
normal! zo
1189
normal! zo
1189
normal! zo
1189
normal! zo
1189
normal! zo
1189
normal! zo
1189
normal! zo
1193
normal! zo
1193
normal! zo
1193
normal! zo
1193
normal! zo
1193
normal! zo
1193
normal! zo
1193
normal! zo
1199
normal! zo
1206
normal! zo
1207
normal! zo
1212
normal! zo
1215
normal! zo
1215
normal! zo
1215
normal! zo
1217
normal! zo
1222
normal! zo
1285
normal! zo
1285
normal! zo
1285
normal! zo
1285
normal! zo
1285
normal! zo
1285
normal! zo
1320
normal! zo
1321
normal! zo
1326
normal! zo
1370
normal! zo
1370
normal! zo
1370
normal! zo
1370
normal! zo
1370
normal! zo
1370
normal! zo
1378
normal! zo
1379
normal! zo
1492
normal! zo
1512
normal! zo
1513
normal! zo
1513
normal! zo
1513
normal! zo
1513
normal! zo
let s:l = 1467 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1467
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
692
normal! zo
7764
normal! zo
7770
normal! zo
10108
normal! zo
10148
normal! zo
10171
normal! zo
10174
normal! zo
10177
normal! zo
10179
normal! zo
10179
normal! zo
10179
normal! zo
10201
normal! zo
10217
normal! zo
10220
normal! zo
10601
normal! zo
10877
normal! zo
10883
normal! zo
10893
normal! zo
10920
normal! zo
10923
normal! zo
10949
normal! zo
10949
normal! zo
10949
normal! zo
10960
normal! zo
10963
normal! zo
11010
normal! zo
11039
normal! zo
11042
normal! zo
11045
normal! zo
11047
normal! zo
11047
normal! zo
11047
normal! zo
11062
normal! zo
11063
normal! zo
11063
normal! zo
let s:l = 694 - ((5 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
694
normal! 09|
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
235
normal! zo
236
normal! zo
269
normal! zo
269
normal! zo
let s:l = 2323 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2323
normal! 023|
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
65
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
77
normal! zo
78
normal! zo
170
normal! zo
170
normal! zo
170
normal! zo
177
normal! zo
178
normal! zo
181
normal! zo
182
normal! zo
206
normal! zo
209
normal! zo
215
normal! zo
215
normal! zo
215
normal! zo
215
normal! zo
215
normal! zo
215
normal! zo
215
normal! zo
215
normal! zo
263
normal! zo
328
normal! zo
334
normal! zo
337
normal! zo
364
normal! zo
369
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
378
normal! zo
403
normal! zo
403
normal! zo
403
normal! zo
403
normal! zo
431
normal! zo
431
normal! zo
431
normal! zo
431
normal! zo
431
normal! zo
431
normal! zo
431
normal! zo
431
normal! zo
481
normal! zo
490
normal! zo
550
normal! zo
558
normal! zo
665
normal! zo
667
normal! zo
668
normal! zo
669
normal! zo
670
normal! zo
680
normal! zo
682
normal! zo
683
normal! zo
700
normal! zo
829
normal! zo
834
normal! zo
834
normal! zo
834
normal! zo
834
normal! zo
834
normal! zo
856
normal! zo
875
normal! zo
883
normal! zo
905
normal! zo
909
normal! zo
910
normal! zo
948
normal! zo
967
normal! zo
969
normal! zo
969
normal! zo
969
normal! zo
969
normal! zo
969
normal! zo
975
normal! zo
989
normal! zo
996
normal! zo
996
normal! zo
997
normal! zo
1000
normal! zo
1004
normal! zo
1005
normal! zo
1012
normal! zo
1020
normal! zo
1027
normal! zo
1038
normal! zo
1040
normal! zo
1062
normal! zo
1242
normal! zo
1260
normal! zo
1269
normal! zo
1275
normal! zo
1281
normal! zo
1281
normal! zo
1281
normal! zo
1281
normal! zo
1281
normal! zo
1281
normal! zo
1281
normal! zo
1281
normal! zo
1281
normal! zo
1281
normal! zo
1284
normal! zo
1300
normal! zo
1316
normal! zo
1316
normal! zo
1316
normal! zo
1316
normal! zo
1316
normal! zo
1316
normal! zo
1416
normal! zo
1440
normal! zo
1440
normal! zo
1450
normal! zo
1488
normal! zo
1488
normal! zo
1488
normal! zo
1488
normal! zo
1488
normal! zo
1553
normal! zo
1602
normal! zo
1635
normal! zo
1681
normal! zo
1711
normal! zo
1720
normal! zo
1735
normal! zo
1754
normal! zo
1760
normal! zo
1765
normal! zo
1772
normal! zo
1772
normal! zo
1772
normal! zo
1772
normal! zo
1772
normal! zo
1772
normal! zo
1811
normal! zo
1870
normal! zo
1881
normal! zo
1884
normal! zo
1893
normal! zo
1893
normal! zo
1893
normal! zo
1902
normal! zo
1913
normal! zo
1950
normal! zo
2037
normal! zo
2039
normal! zo
2041
normal! zo
2043
normal! zo
2150
normal! zo
2162
normal! zo
2423
normal! zo
2423
normal! zo
2423
normal! zo
2423
normal! zo
2423
normal! zo
2423
normal! zo
2423
normal! zo
2486
normal! zo
2490
normal! zo
2506
normal! zo
2509
normal! zo
2516
normal! zo
2522
normal! zo
2574
normal! zo
2623
normal! zo
2900
normal! zo
3017
normal! zo
3023
normal! zo
3063
normal! zo
3161
normal! zo
3368
normal! zo
3485
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3621
normal! zo
3626
normal! zo
3632
normal! zo
3632
normal! zo
3632
normal! zo
3632
normal! zo
3632
normal! zo
3632
normal! zo
3632
normal! zo
3632
normal! zo
3632
normal! zo
3632
normal! zo
3632
normal! zo
3699
normal! zo
3736
normal! zo
3736
normal! zo
3736
normal! zo
let s:l = 76 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
76
normal! 040|
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
312
normal! zo
546
normal! zo
551
normal! zo
667
normal! zo
667
normal! zo
667
normal! zo
667
normal! zo
667
normal! zo
1845
normal! zo
2526
normal! zo
2534
normal! zo
2539
normal! zo
2545
normal! zo
2552
normal! zo
2575
normal! zo
4176
normal! zo
let s:l = 556 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
556
normal! 099|
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
let s:l = 1716 - ((0 * winheight(0) + 6) / 13)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1716
normal! 035|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
10wincmd w
exe 'vert 1resize ' . ((&columns * 19 + 51) / 102)
exe '2resize ' . ((&lines * 7 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 82 + 51) / 102)
exe '3resize ' . ((&lines * 6 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 82 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 82 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 82 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 82 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 82 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 8resize ' . ((&columns * 82 + 51) / 102)
exe '9resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 9resize ' . ((&columns * 82 + 51) / 102)
exe '10resize ' . ((&lines * 13 + 21) / 42)
exe 'vert 10resize ' . ((&columns * 82 + 51) / 102)
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
