" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 23 septiembre 2014 at 17:10:31.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Source\ Code\ Pro\ 9
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
badd +126 ginn/formularios/consulta_consumo.py
badd +41 ginn/framework/memoize.py
badd +596 ginn/formularios/presupuesto.py
badd +44 ginn/formularios/listado_rollos.py
badd +89 ginn/informes/norma2013.py
badd +162 ginn/formularios/consulta_global.py
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
badd +335 ginn/formularios/custom_widgets/gtkcairoplot.py
badd +1 ginn/lib/cairoplot/__init__.py
badd +1 ginn/lib/cagraph/cagraph/series/__init__.py
badd +84 ginn/lib/cagraph/cagraph/series/dna.py
badd +562 ginn/formularios/facturas_venta.py
badd +1 ginn/formularios/facturas_compra.py
badd +111 ginn/formularios/prefacturas.py
badd +1020 ginn/formularios/pedidos_de_venta.py
badd +5 ginn/formularios/launcher.py
badd +20446 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/abonos_venta.glade
badd +513 ginn/formularios/crm_detalles_factura.py
badd +406 ginn/formularios/crm_seguimiento_impagos.py
badd +1 extra/scripts/clouseau-gtk.py
badd +1 ginn/formularios/partes_de_fabricacion_rollos.py
badd +1 ginn/formularios/consulta_producciones_estandar.py
badd +411 ginn/formularios/pagares_pagos.py
badd +606 ginn/formularios/consulta_pendientes_servir.py
badd +395 ginn/formularios/consulta_pagos_realizados.py
badd +21 ginn/lib/myprint.py
badd +926 ginn/formularios/consumo_balas_partida.py
badd +399 ginn/formularios/auditviewer.py
badd +1346 db/tablas.sql
badd +1 ginn/formularios/partes_de_fabricacion_bolsas.glade
badd +115 ginn/formularios/consulta_existenciasBolsas.py
badd +23 extra/scripts/bash_completion_ginn
badd +1 ginn/formularios/consulta_ventas.py
badd +631 ginn/formularios/pagares_cobros.py
args formularios/auditviewer.py
set lines=47 columns=115
edit ginn/formularios/consulta_ventas.py
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
exe 'vert 1resize ' . ((&columns * 30 + 57) / 115)
exe '2resize ' . ((&lines * 4 + 23) / 47)
exe 'vert 2resize ' . ((&columns * 84 + 57) / 115)
exe '3resize ' . ((&lines * 26 + 23) / 47)
exe 'vert 3resize ' . ((&columns * 84 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 4resize ' . ((&columns * 84 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 5resize ' . ((&columns * 84 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 6resize ' . ((&columns * 84 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 7resize ' . ((&columns * 84 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 8resize ' . ((&columns * 84 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 9resize ' . ((&columns * 84 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 10resize ' . ((&columns * 84 + 57) / 115)
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
55
normal! zo
60
normal! zo
77
normal! zo
77
normal! zo
114
normal! zo
114
normal! zo
164
normal! zo
164
normal! zo
184
normal! zo
184
normal! zo
556
normal! zo
579
normal! zo
580
normal! zo
580
normal! zo
580
normal! zo
580
normal! zo
580
normal! zo
681
normal! zo
707
normal! zo
708
normal! zo
708
normal! zo
708
normal! zo
708
normal! zo
708
normal! zo
815
normal! zo
837
normal! zo
838
normal! zo
838
normal! zo
838
normal! zo
838
normal! zo
838
normal! zo
951
normal! zo
956
normal! zo
957
normal! zo
957
normal! zo
957
normal! zo
957
normal! zo
957
normal! zo
1201
normal! zo
1228
normal! zo
1229
normal! zo
1229
normal! zo
1229
normal! zo
1229
normal! zo
1229
normal! zo
1277
normal! zo
1277
normal! zo
1277
normal! zo
1277
normal! zo
1277
normal! zo
1277
normal! zo
1317
normal! zo
1323
normal! zo
1323
normal! zo
1323
normal! zo
1323
normal! zo
1356
normal! zo
1356
normal! zo
1356
normal! zo
1356
normal! zo
1356
normal! zo
1356
normal! zo
1396
normal! zo
1401
normal! zo
1401
normal! zo
1401
normal! zo
1401
normal! zo
let s:l = 136 - ((0 * winheight(0) + 2) / 4)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
136
normal! 031|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/facturas_compra.py
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
423
normal! zo
700
normal! zo
708
normal! zo
715
normal! zo
733
normal! zo
738
normal! zo
882
normal! zo
947
normal! zo
953
normal! zo
1001
normal! zo
1012
normal! zo
1013
normal! zo
let s:l = 714 - ((12 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
714
normal! 078|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_ancho_multiple.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 27 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
27
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_global.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
1212
normal! zo
let s:l = 162 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
162
normal! 038|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_pagos_realizados.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
49
normal! zo
199
normal! zo
218
normal! zo
244
normal! zo
244
normal! zo
468
normal! zo
476
normal! zo
480
normal! zo
let s:l = 491 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
491
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/facturas_venta.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
107
normal! zo
209
normal! zo
264
normal! zo
264
normal! zo
2299
normal! zo
2327
normal! zo
2350
normal! zo
2354
normal! zo
2356
normal! zo
2359
normal! zo
2362
normal! zo
2364
normal! zo
2367
normal! zo
2370
normal! zo
2372
normal! zo
2609
normal! zo
2626
normal! zo
2630
normal! zo
2630
normal! zo
2630
normal! zo
2630
normal! zo
2630
normal! zo
2630
normal! zo
2630
normal! zo
let s:l = 2302 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2302
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
89
normal! zo
89
normal! zo
89
normal! zo
89
normal! zo
89
normal! zo
296
normal! zo
359
normal! zo
386
normal! zo
415
normal! zo
1675
normal! zo
1796
normal! zo
1838
normal! zo
1949
normal! zo
1982
normal! zo
1990
normal! zo
1992
normal! zo
1998
normal! zo
1998
normal! zo
1998
normal! zo
1998
normal! zo
2019
normal! zo
2030
normal! zo
2030
normal! zo
2125
normal! zo
2174
normal! zo
2860
normal! zo
3270
normal! zo
3304
normal! zo
3307
normal! zo
3421
normal! zo
3832
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3863
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3865
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3867
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3869
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3871
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3873
normal! zo
3876
normal! zo
3883
normal! zo
3884
normal! zo
3884
normal! zo
3884
normal! zo
3884
normal! zo
3884
normal! zo
3886
normal! zo
3887
normal! zo
3892
normal! zo
3893
normal! zo
3907
normal! zo
3912
normal! zo
3913
normal! zo
3913
normal! zo
3913
normal! zo
3918
normal! zo
3918
normal! zo
3918
normal! zo
3921
normal! zo
3927
normal! zo
3933
normal! zo
4188
normal! zo
4572
normal! zo
4598
normal! zo
4609
normal! zo
4617
normal! zo
4671
normal! zo
5951
normal! zo
6016
normal! zo
6025
normal! zo
6025
normal! zo
6025
normal! zo
6025
normal! zo
6025
normal! zo
6025
normal! zo
6027
normal! zo
6615
normal! zo
6716
normal! zo
6716
normal! zo
6716
normal! zo
6716
normal! zo
6716
normal! zo
7004
normal! zo
7349
normal! zo
7367
normal! zo
7463
normal! zo
7485
normal! zo
7784
normal! zo
7908
normal! zo
7908
normal! zo
7908
normal! zo
7908
normal! zo
7908
normal! zo
7908
normal! zo
7977
normal! zo
7984
normal! zo
7990
normal! zo
8474
normal! zo
9277
normal! zo
10075
normal! zo
10115
normal! zo
10168
normal! zo
10171
normal! zo
10568
normal! zo
10875
normal! zo
10878
normal! zo
10914
normal! zo
10922
normal! zo
11009
normal! zo
11013
normal! zo
11016
normal! zo
11393
normal! zo
11780
normal! zo
11780
normal! zo
11780
normal! zo
11780
normal! zo
11780
normal! zo
11994
normal! zo
12153
normal! zo
12153
normal! zo
12310
normal! zo
12310
normal! zo
12310
normal! zo
12324
normal! zo
12426
normal! zo
12426
normal! zo
12426
normal! zo
12426
normal! zo
12426
normal! zo
12776
normal! zo
12776
normal! zo
12776
normal! zo
12776
normal! zo
12776
normal! zo
12776
normal! zo
12776
normal! zo
12809
normal! zo
12810
normal! zo
12813
normal! zo
12827
normal! zo
14777
normal! zo
15269
normal! zo
15298
normal! zo
15940
normal! zo
15989
normal! zo
15995
normal! zo
15996
normal! zo
15999
normal! zo
16312
normal! zo
16451
normal! zo
16460
normal! zo
16468
normal! zo
16469
normal! zo
16470
normal! zo
16491
normal! zo
16555
normal! zo
16555
normal! zo
16555
normal! zo
16753
normal! zo
16822
normal! zo
16836
normal! zo
16842
normal! zo
16845
normal! zo
16846
normal! zo
16861
normal! zo
16868
normal! zo
16869
normal! zo
16878
normal! zo
16889
normal! zo
16889
normal! zo
16889
normal! zo
16896
normal! zo
16896
normal! zo
16896
normal! zo
16944
normal! zo
16952
normal! zo
16957
normal! zo
17071
normal! zo
17092
normal! zo
17111
normal! zo
17119
normal! zo
17120
normal! zo
17129
normal! zo
17145
normal! zo
17155
normal! zo
17158
normal! zo
17367
normal! zo
17456
normal! zo
17470
normal! zo
17473
normal! zo
17477
normal! zo
17478
normal! zo
17738
normal! zo
17762
normal! zo
17767
normal! zo
17938
normal! zo
18232
normal! zo
19058
normal! zo
19108
normal! zo
21503
normal! zo
21513
normal! zo
21562
normal! zo
21563
normal! zo
21563
normal! zo
let s:l = 3341 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3341
normal! 029|
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
1815
normal! zo
1827
normal! zo
1830
normal! zo
1831
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
let s:l = 1835 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1835
normal! 034|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/custom_widgets/gtkcairoplot.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
72
normal! zo
76
normal! zo
97
normal! zo
97
normal! zo
97
normal! zo
180
normal! zo
191
normal! zo
205
normal! zo
212
normal! zo
224
normal! zo
232
normal! zo
244
normal! zo
277
normal! zo
286
normal! zo
326
normal! zo
330
normal! zo
333
normal! zo
346
normal! zo
360
normal! zo
361
normal! zo
362
normal! zo
363
normal! zo
363
normal! zo
381
normal! zo
397
normal! zo
402
normal! zo
421
normal! zo
425
normal! zo
425
normal! zo
447
normal! zo
let s:l = 198 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
198
normal! 057|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 57) / 115)
exe '2resize ' . ((&lines * 4 + 23) / 47)
exe 'vert 2resize ' . ((&columns * 84 + 57) / 115)
exe '3resize ' . ((&lines * 26 + 23) / 47)
exe 'vert 3resize ' . ((&columns * 84 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 4resize ' . ((&columns * 84 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 5resize ' . ((&columns * 84 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 6resize ' . ((&columns * 84 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 7resize ' . ((&columns * 84 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 8resize ' . ((&columns * 84 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 9resize ' . ((&columns * 84 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 10resize ' . ((&columns * 84 + 57) / 115)
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
