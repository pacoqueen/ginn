" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 03 noviembre 2014 at 10:36:03.
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
badd +129 ginn/informes/ekotex.py
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
badd +11 ginn/formularios/pedidos_de_venta.py
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
badd +3229 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +2204 ginn/formularios/albaranes_de_salida.py
badd +3592 ginn/formularios/presupuestos.py
badd +174 ginn/formularios/mail_sender.py
badd +54 ginn/formularios/consulta_pedidos_clientes.py
badd +52 ginn/formularios/consulta_productividad.py
badd +1 ginn/formularios/mail_sender.glade
badd +141 ginn/formularios/facturas_compra.py
badd +39 ginn/informes/presupuesto2.py
badd +4498 ginn/formularios/utils.py
badd +59 ginn/framework/pclases/facturadeabono.py
args formularios/auditviewer.py
set lines=42 columns=101
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
7wincmd k
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
exe 'vert 1resize ' . ((&columns * 18 + 50) / 101)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 82 + 50) / 101)
exe '3resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 82 + 50) / 101)
exe '4resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 82 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 82 + 50) / 101)
exe '6resize ' . ((&lines * 25 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 82 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 82 + 50) / 101)
exe '8resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 8resize ' . ((&columns * 82 + 50) / 101)
exe '9resize ' . ((&lines * 2 + 21) / 42)
exe 'vert 9resize ' . ((&columns * 82 + 50) / 101)
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
let s:l = 544 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
544
normal! 034|
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
let s:l = 1466 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1466
normal! 032|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/informes/presupuesto2.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
323
normal! zo
324
normal! zo
324
normal! zo
324
normal! zo
324
normal! zo
324
normal! zo
324
normal! zo
348
normal! zo
349
normal! zo
337
normal! zo
338
normal! zo
338
normal! zo
338
normal! zo
338
normal! zo
338
normal! zo
338
normal! zo
344
normal! zo
368
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
387
normal! zo
415
normal! zo
415
normal! zo
415
normal! zo
418
normal! zo
425
normal! zo
426
normal! zo
426
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
440
normal! zo
506
normal! zo
541
normal! zo
541
normal! zo
541
normal! zo
541
normal! zo
544
normal! zo
546
normal! zo
548
normal! zo
598
normal! zo
599
normal! zo
600
normal! zo
600
normal! zo
602
normal! zo
603
normal! zo
603
normal! zo
607
normal! zo
607
normal! zo
607
normal! zo
607
normal! zo
607
normal! zo
609
normal! zo
616
normal! zo
617
normal! zo
619
normal! zo
621
normal! zo
623
normal! zo
627
normal! zo
628
normal! zo
628
normal! zo
628
normal! zo
646
normal! zo
646
normal! zo
646
normal! zo
670
normal! zo
673
normal! zo
674
normal! zo
674
normal! zo
674
normal! zo
674
normal! zo
677
normal! zo
677
normal! zo
677
normal! zo
681
normal! zo
681
normal! zo
681
normal! zo
685
normal! zo
689
normal! zo
689
normal! zo
let s:l = 359 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
359
normal! 037|
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
75
normal! zo
76
normal! zo
168
normal! zo
168
normal! zo
168
normal! zo
175
normal! zo
176
normal! zo
179
normal! zo
180
normal! zo
204
normal! zo
207
normal! zo
213
normal! zo
213
normal! zo
213
normal! zo
213
normal! zo
213
normal! zo
213
normal! zo
213
normal! zo
213
normal! zo
261
normal! zo
362
normal! zo
367
normal! zo
376
normal! zo
376
normal! zo
376
normal! zo
376
normal! zo
376
normal! zo
376
normal! zo
401
normal! zo
401
normal! zo
401
normal! zo
401
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
663
normal! zo
665
normal! zo
666
normal! zo
667
normal! zo
668
normal! zo
678
normal! zo
680
normal! zo
681
normal! zo
827
normal! zo
832
normal! zo
832
normal! zo
832
normal! zo
832
normal! zo
832
normal! zo
958
normal! zo
977
normal! zo
979
normal! zo
979
normal! zo
979
normal! zo
979
normal! zo
979
normal! zo
985
normal! zo
999
normal! zo
1006
normal! zo
1006
normal! zo
1007
normal! zo
1010
normal! zo
1014
normal! zo
1015
normal! zo
1022
normal! zo
1030
normal! zo
1037
normal! zo
1048
normal! zo
1050
normal! zo
1252
normal! zo
1270
normal! zo
1285
normal! zo
1417
normal! zo
1441
normal! zo
1441
normal! zo
1489
normal! zo
1489
normal! zo
1489
normal! zo
1489
normal! zo
1489
normal! zo
2120
normal! zo
2132
normal! zo
2870
normal! zo
3591
normal! zo
3596
normal! zo
3602
normal! zo
3602
normal! zo
3602
normal! zo
3602
normal! zo
3602
normal! zo
3602
normal! zo
3602
normal! zo
3602
normal! zo
3602
normal! zo
3602
normal! zo
3602
normal! zo
3669
normal! zo
3706
normal! zo
3706
normal! zo
3706
normal! zo
let s:l = 1838 - ((14 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1838
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
312
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
let s:l = 529 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
529
normal! 017|
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
300
normal! zo
318
normal! zo
325
normal! zo
326
normal! zo
1694
normal! zo
1816
normal! zo
1858
normal! zo
1892
normal! zo
1919
normal! zo
1929
normal! zo
1929
normal! zo
1929
normal! zo
1929
normal! zo
1929
normal! zo
3961
normal! zo
3995
normal! zo
3997
normal! zo
4216
normal! zo
4699
normal! zo
4710
normal! zo
5258
normal! zo
5345
normal! zo
5367
normal! zo
5367
normal! zo
5367
normal! zo
5367
normal! zo
5367
normal! zo
5430
normal! zo
5438
normal! zo
5439
normal! zo
5442
normal! zo
5444
normal! zo
5465
normal! zo
5471
normal! zo
6474
normal! zo
6645
normal! zo
6668
normal! zo
9307
normal! zo
12352
normal! zo
12352
normal! zo
12352
normal! zo
13314
normal! zo
13314
normal! zo
13353
normal! zo
13354
normal! zo
13355
normal! zo
13357
normal! zo
14819
normal! zo
15093
normal! zo
15135
normal! zo
15535
normal! zo
16795
normal! zo
16820
normal! zo
16836
normal! zo
16841
normal! zo
16841
normal! zo
16841
normal! zo
16842
normal! zo
16847
normal! zo
16910
normal! zo
16949
normal! zo
16956
normal! zo
16957
normal! zo
17005
normal! zo
17015
normal! zo
17099
normal! zo
17180
normal! zo
17199
normal! zo
17354
normal! zo
17367
normal! zo
17368
normal! zo
17369
normal! zo
17370
normal! zo
17375
normal! zo
17379
normal! zo
17381
normal! zo
17392
normal! zo
17455
normal! zo
17507
normal! zo
17614
normal! zo
17621
normal! zo
17626
normal! zo
17733
normal! zo
17790
normal! zo
17813
normal! zo
17822
normal! zo
17823
normal! zo
17823
normal! zo
17847
normal! zo
18047
normal! zo
18147
normal! zo
18235
normal! zo
18245
normal! zo
18265
normal! zo
18381
normal! zo
18602
normal! zo
18611
normal! zo
18612
normal! zo
18613
normal! zo
18615
normal! zo
18615
normal! zo
18615
normal! zo
18618
normal! zo
18620
normal! zo
18620
normal! zo
18620
normal! zo
18623
normal! zo
18624
normal! zo
18624
normal! zo
18624
normal! zo
18624
normal! zo
18624
normal! zo
let s:l = 338 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
338
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
let s:l = 1687 - ((0 * winheight(0) + 1) / 2)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1687
normal! 024|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 18 + 50) / 101)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 82 + 50) / 101)
exe '3resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 82 + 50) / 101)
exe '4resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 82 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 82 + 50) / 101)
exe '6resize ' . ((&lines * 25 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 82 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 82 + 50) / 101)
exe '8resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 8resize ' . ((&columns * 82 + 50) / 101)
exe '9resize ' . ((&lines * 2 + 21) / 42)
exe 'vert 9resize ' . ((&columns * 82 + 50) / 101)
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
