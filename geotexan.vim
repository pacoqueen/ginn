" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 09 septiembre 2014 at 16:03:01.
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
badd +133 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1 ginn/formularios/partes_de_ancho_multiple.py
badd +1119 ginn/formularios/consulta_producido.py
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
badd +1867 ginn/formularios/facturas_compra.py
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
badd +1 ginn/formularios/consulta_cobros.py
badd +411 ginn/formularios/pagares_pagos.py
badd +606 ginn/formularios/consulta_pendientes_servir.py
badd +395 ginn/formularios/consulta_pagos_realizados.py
badd +21 ginn/lib/myprint.py
badd +926 ginn/formularios/consumo_balas_partida.py
badd +1 ginn/formularios/auditviewer.py
badd +1346 db/tablas.sql
badd +0 ginn/formularios/presupuestos.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=57 columns=115
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
exe 'vert 1resize ' . ((&columns * 29 + 57) / 115)
exe '2resize ' . ((&lines * 39 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 85 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 85 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 85 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 85 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 85 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 85 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 85 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 85 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 85 + 57) / 115)
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
58
normal! zo
59
normal! zo
74
normal! zo
75
normal! zo
83
normal! zo
83
normal! zo
83
normal! zo
83
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
214
normal! zo
222
normal! zo
229
normal! zo
232
normal! zo
238
normal! zo
239
normal! zo
239
normal! zo
240
normal! zo
240
normal! zo
245
normal! zo
312
normal! zo
465
normal! zo
474
normal! zo
534
normal! zo
542
normal! zo
594
normal! zo
601
normal! zo
683
normal! zo
696
normal! zo
742
normal! zo
839
normal! zo
858
normal! zo
866
normal! zo
1334
normal! zo
1341
normal! zo
1343
normal! zo
1904
normal! zo
1948
normal! zo
2104
normal! zo
2179
normal! zo
2185
normal! zo
2235
normal! zo
2249
normal! zo
2354
normal! zo
2373
normal! zo
2447
normal! zo
2736
normal! zo
2755
normal! zo
2831
normal! zo
2848
normal! zo
2850
normal! zo
2870
normal! zo
2874
normal! zo
2875
normal! zo
2877
normal! zo
2877
normal! zo
2948
normal! zo
2954
normal! zo
2994
normal! zo
3065
normal! zo
3068
normal! zo
3069
normal! zo
3069
normal! zo
3247
normal! zo
3250
normal! zo
3254
normal! zo
3255
normal! zo
3292
normal! zo
3306
normal! zo
3311
normal! zo
3317
normal! zo
3330
normal! zo
3331
normal! zo
3452
normal! zo
3453
normal! zo
3455
normal! zo
3455
normal! zo
3458
normal! zo
3461
normal! zo
let s:l = 60 - ((20 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
60
normal! 022|
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
let s:l = 27 - ((1 * winheight(0) + 0) / 1)
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
let s:l = 479 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
479
normal! 035|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/auditviewer.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
48
normal! zo
52
normal! zo
52
normal! zo
76
normal! zo
76
normal! zo
88
normal! zo
88
normal! zo
88
normal! zo
88
normal! zo
88
normal! zo
88
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
313
normal! zo
318
normal! zo
319
normal! zo
319
normal! zo
319
normal! zo
391
normal! zo
403
normal! zo
404
normal! zo
404
normal! zo
405
normal! zo
let s:l = 395 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
395
normal! 030|
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
50
normal! zo
55
normal! zo
274
normal! zo
345
normal! zo
357
normal! zo
360
normal! zo
363
normal! zo
394
normal! zo
let s:l = 475 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
475
normal! 05|
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
4668
normal! zo
5948
normal! zo
6013
normal! zo
6022
normal! zo
6022
normal! zo
6022
normal! zo
6022
normal! zo
6022
normal! zo
6022
normal! zo
6024
normal! zo
6612
normal! zo
6713
normal! zo
6713
normal! zo
6713
normal! zo
6713
normal! zo
6713
normal! zo
7001
normal! zo
7346
normal! zo
7364
normal! zo
7460
normal! zo
7482
normal! zo
7781
normal! zo
7905
normal! zo
7905
normal! zo
7905
normal! zo
7905
normal! zo
7905
normal! zo
7905
normal! zo
7974
normal! zo
7981
normal! zo
7987
normal! zo
8471
normal! zo
9274
normal! zo
10072
normal! zo
10112
normal! zo
10165
normal! zo
10168
normal! zo
10565
normal! zo
10872
normal! zo
10875
normal! zo
10911
normal! zo
10919
normal! zo
11006
normal! zo
11010
normal! zo
11013
normal! zo
11390
normal! zo
11777
normal! zo
11777
normal! zo
11777
normal! zo
11777
normal! zo
11777
normal! zo
11991
normal! zo
12150
normal! zo
12150
normal! zo
12307
normal! zo
12307
normal! zo
12307
normal! zo
12321
normal! zo
12423
normal! zo
12423
normal! zo
12423
normal! zo
12423
normal! zo
12423
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12773
normal! zo
12806
normal! zo
12807
normal! zo
12810
normal! zo
12824
normal! zo
14774
normal! zo
15266
normal! zo
15295
normal! zo
15984
normal! zo
15986
normal! zo
15992
normal! zo
15993
normal! zo
15996
normal! zo
15998
normal! zo
16000
normal! zo
16001
normal! zo
16309
normal! zo
16448
normal! zo
16457
normal! zo
16465
normal! zo
16466
normal! zo
16467
normal! zo
16488
normal! zo
16552
normal! zo
16552
normal! zo
16552
normal! zo
16750
normal! zo
16819
normal! zo
16833
normal! zo
16839
normal! zo
16842
normal! zo
16843
normal! zo
16858
normal! zo
16865
normal! zo
16866
normal! zo
16875
normal! zo
16886
normal! zo
16886
normal! zo
16886
normal! zo
16893
normal! zo
16893
normal! zo
16893
normal! zo
16941
normal! zo
16949
normal! zo
16954
normal! zo
17068
normal! zo
17089
normal! zo
17108
normal! zo
17116
normal! zo
17117
normal! zo
17126
normal! zo
17142
normal! zo
17152
normal! zo
17155
normal! zo
17364
normal! zo
17453
normal! zo
17467
normal! zo
17470
normal! zo
17474
normal! zo
17475
normal! zo
17735
normal! zo
17759
normal! zo
17764
normal! zo
17935
normal! zo
18229
normal! zo
19055
normal! zo
19105
normal! zo
21500
normal! zo
21510
normal! zo
21559
normal! zo
21560
normal! zo
21560
normal! zo
let s:l = 10920 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10920
normal! 040|
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
let s:l = 1828 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1828
normal! 036|
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
2wincmd w
exe 'vert 1resize ' . ((&columns * 29 + 57) / 115)
exe '2resize ' . ((&lines * 39 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 85 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 85 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 85 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 85 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 85 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 85 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 85 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 85 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 85 + 57) / 115)
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
