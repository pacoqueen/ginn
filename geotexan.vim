" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 01 octubre 2014 at 14:18:37.
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
badd +126 ginn/formularios/consulta_consumo.py
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
badd +335 ginn/formularios/custom_widgets/gtkcairoplot.py
badd +1 ginn/lib/cairoplot/__init__.py
badd +1 ginn/lib/cagraph/cagraph/series/__init__.py
badd +84 ginn/lib/cagraph/cagraph/series/dna.py
badd +562 ginn/formularios/facturas_venta.py
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
badd +504 ginn/formularios/consulta_pagos_realizados.py
badd +21 ginn/lib/myprint.py
badd +926 ginn/formularios/consumo_balas_partida.py
badd +399 ginn/formularios/auditviewer.py
badd +1 ginn/formularios/partes_de_fabricacion_bolsas.glade
badd +115 ginn/formularios/consulta_existenciasBolsas.py
badd +23 extra/scripts/bash_completion_ginn
badd +1200 ginn/formularios/consulta_ventas.py
badd +631 ginn/formularios/pagares_cobros.py
badd +1 ginn/framework/pclases/superfacturaventa.py
badd +1 ginn/informes/geninformes.py
badd +1 ginn/formularios/utils.py
badd +1 ginn/formularios/fixedpoint.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=64 columns=126
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
exe 'vert 1resize ' . ((&columns * 32 + 63) / 126)
exe '2resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 93 + 63) / 126)
exe '3resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 93 + 63) / 126)
exe '4resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 93 + 63) / 126)
exe '5resize ' . ((&lines * 46 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 93 + 63) / 126)
exe '6resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 6resize ' . ((&columns * 93 + 63) / 126)
exe '7resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 7resize ' . ((&columns * 93 + 63) / 126)
exe '8resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 8resize ' . ((&columns * 93 + 63) / 126)
exe '9resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 9resize ' . ((&columns * 93 + 63) / 126)
exe '10resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 10resize ' . ((&columns * 93 + 63) / 126)
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
let s:l = 27 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
27
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/fixedpoint.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 223 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
223
normal! 041|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/utils.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
2115
normal! zo
2122
normal! zo
2153
normal! zo
2162
normal! zo
2174
normal! zo
2182
normal! zo
let s:l = 2192 - ((15 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2192
normal! 029|
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
1380
normal! zo
1380
normal! zo
1803
normal! zo
1804
normal! zo
1804
normal! zo
1804
normal! zo
1804
normal! zo
1816
normal! zo
1816
normal! zo
1816
normal! zo
1816
normal! zo
2297
normal! zo
2297
normal! zo
2297
normal! zo
2297
normal! zo
2311
normal! zo
2476
normal! zo
2476
normal! zo
2476
normal! zo
2476
normal! zo
2490
normal! zo
2490
normal! zo
2490
normal! zo
2903
normal! zo
2903
normal! zo
2903
normal! zo
2903
normal! zo
2914
normal! zo
2951
normal! zo
2951
normal! zo
3005
normal! zo
3071
normal! zo
3078
normal! zo
3079
normal! zo
3092
normal! zo
3093
normal! zo
3093
normal! zo
3093
normal! zo
3099
normal! zo
3100
normal! zo
3101
normal! zo
3101
normal! zo
3101
normal! zo
3101
normal! zo
3101
normal! zo
3101
normal! zo
3115
normal! zo
3146
normal! zo
3154
normal! zo
3158
normal! zo
3158
normal! zo
3158
normal! zo
3177
normal! zo
3177
normal! zo
3177
normal! zo
3365
normal! zo
3428
normal! zo
3428
normal! zo
3428
normal! zo
3428
normal! zo
3442
normal! zo
3443
normal! zo
3514
normal! zo
3517
normal! zo
3564
normal! zo
3567
normal! zo
3567
normal! zo
3567
normal! zo
3570
normal! zo
3592
normal! zo
4440
normal! zo
4522
normal! zo
4788
normal! zo
4789
normal! zo
4845
normal! zo
4845
normal! zo
4845
normal! zo
4845
normal! zo
let s:l = 3434 - ((24 * winheight(0) + 23) / 46)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3434
normal! 09|
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
224
normal! zo
224
normal! zo
264
normal! zo
264
normal! zo
324
normal! zo
488
normal! zo
497
normal! zo
498
normal! zo
498
normal! zo
498
normal! zo
498
normal! zo
562
normal! zo
600
normal! zo
601
normal! zo
601
normal! zo
601
normal! zo
601
normal! zo
601
normal! zo
601
normal! zo
634
normal! zo
2300
normal! zo
2328
normal! zo
2351
normal! zo
2355
normal! zo
2357
normal! zo
2360
normal! zo
2363
normal! zo
2365
normal! zo
2368
normal! zo
2371
normal! zo
2373
normal! zo
2610
normal! zo
2627
normal! zo
2627
normal! zo
2627
normal! zo
2627
normal! zo
2627
normal! zo
2627
normal! zo
2631
normal! zo
2631
normal! zo
2631
normal! zo
2631
normal! zo
2631
normal! zo
2631
normal! zo
2631
normal! zo
2778
normal! zo
2915
normal! zo
2920
normal! zo
2949
normal! zo
2950
normal! zo
2950
normal! zo
2954
normal! zo
3051
normal! zo
let s:l = 571 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
571
normal! 013|
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
58
normal! zo
151
normal! zo
160
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
168
normal! zo
169
normal! zo
175
normal! zo
176
normal! zo
176
normal! zo
182
normal! zo
183
normal! zo
576
normal! zo
586
normal! zo
595
normal! zo
595
normal! zo
595
normal! zo
595
normal! zo
595
normal! zo
595
normal! zo
607
normal! zo
948
normal! zo
967
normal! zo
968
normal! zo
971
normal! zo
let s:l = 209 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
209
normal! 044|
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
6906
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
18008
normal! zo
18232
normal! zo
19058
normal! zo
19108
normal! zo
19287
normal! zo
19314
normal! zo
19324
normal! zo
19325
normal! zo
19325
normal! zo
19325
normal! zo
19325
normal! zo
19325
normal! zo
19325
normal! zo
19342
normal! zo
19388
normal! zo
19398
normal! zo
19399
normal! zo
19399
normal! zo
19399
normal! zo
19399
normal! zo
19399
normal! zo
19399
normal! zo
19864
normal! zo
20937
normal! zo
21507
normal! zo
21517
normal! zo
21566
normal! zo
21567
normal! zo
21567
normal! zo
let s:l = 15197 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15197
normal! 05|
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
let s:l = 217 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
217
normal! 025|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
5wincmd w
exe 'vert 1resize ' . ((&columns * 32 + 63) / 126)
exe '2resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 93 + 63) / 126)
exe '3resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 93 + 63) / 126)
exe '4resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 93 + 63) / 126)
exe '5resize ' . ((&lines * 46 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 93 + 63) / 126)
exe '6resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 6resize ' . ((&columns * 93 + 63) / 126)
exe '7resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 7resize ' . ((&columns * 93 + 63) / 126)
exe '8resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 8resize ' . ((&columns * 93 + 63) / 126)
exe '9resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 9resize ' . ((&columns * 93 + 63) / 126)
exe '10resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 10resize ' . ((&columns * 93 + 63) / 126)
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
