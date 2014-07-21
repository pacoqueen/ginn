" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 21 julio 2014 at 14:20:23.
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
badd +1 extra/scripts/balas_basura_reembaladas.py
badd +19 ginn/informes/nied.py
badd +129 ginn/informes/ekotex.py
badd +1 formularios/auditviewer.py
badd +248 ginn/formularios/gtkexcepthook.py
badd +133 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1 ginn/formularios/partes_de_fabricacion_gtx.py
badd +1 ginn/formularios/partes_de_ancho_multiple.py
badd +1119 ginn/formularios/consulta_producido.py
badd +126 ginn/formularios/consulta_consumo.py
badd +41 ginn/framework/memoize.py
badd +596 ginn/formularios/presupuesto.py
badd +44 ginn/formularios/listado_rollos.py
badd +89 ginn/informes/norma2013.py
badd +95 ginn/framework/pclases/cliente.py
badd +1094 ginn/formularios/consulta_global.py
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
badd +9974 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/pclase2tv.py
badd +1 ginn/formularios/abonos_venta.glade
badd +513 ginn/formularios/crm_detalles_factura.py
badd +406 ginn/formularios/crm_seguimiento_impagos.py
badd +1 extra/scripts/clouseau-gtk.py
badd +1 extra/scripts/clouseau.py
badd +1 ginn/framework/configuracion.py
badd +1 ginn/formularios/consulta_productividad.py
badd +1 ginn/formularios/partes_de_fabricacion_rollos.py
badd +1 ginn/formularios/consulta_producciones_estandar.py
badd +0 ginn/formularios/presupuestos.py
args formularios/auditviewer.py
set lines=48 columns=117
edit extra/scripts/clouseau.py
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
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
10wincmd k
wincmd w
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
exe 'vert 1resize ' . ((&columns * 28 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 88 + 58) / 117)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 88 + 58) / 117)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 88 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 88 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 88 + 58) / 117)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 88 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 88 + 58) / 117)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 88 + 58) / 117)
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 88 + 58) / 117)
exe '11resize ' . ((&lines * 26 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 88 + 58) / 117)
exe '12resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 88 + 58) / 117)
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
let s:l = 31 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 034|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/extra/scripts/balas_basura_reembaladas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
45
normal! zo
52
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
65
normal! zo
68
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
80
normal! zo
102
normal! zo
103
normal! zo
106
normal! zo
107
normal! zo
110
normal! zo
111
normal! zo
118
normal! zo
127
normal! zo
132
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
142
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
173
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
196
normal! zo
206
normal! zo
209
normal! zo
217
normal! zo
224
normal! zo
225
normal! zo
225
normal! zo
225
normal! zo
225
normal! zo
225
normal! zo
240
normal! zo
249
normal! zo
252
normal! zo
258
normal! zo
263
normal! zo
268
normal! zo
298
normal! zo
299
normal! zo
let s:l = 313 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
313
normal! 029|
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
let s:l = 28 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
28
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_gtx.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
84
normal! zo
84
normal! zc
157
normal! zo
157
normal! zc
205
normal! zo
206
normal! zo
218
normal! zo
218
normal! zo
218
normal! zo
320
normal! zo
779
normal! zo
805
normal! zo
811
normal! zo
815
normal! zo
824
normal! zo
872
normal! zo
874
normal! zo
877
normal! zo
912
normal! zo
1045
normal! zo
1269
normal! zo
1411
normal! zo
1697
normal! zo
2412
normal! zo
2419
normal! zo
3031
normal! zo
3047
normal! zo
3061
normal! zo
3064
normal! zo
3064
normal! zo
3070
normal! zo
3076
normal! zo
3086
normal! zo
3092
normal! zo
3145
normal! zo
3166
normal! zo
3168
normal! zo
3345
normal! zo
3357
normal! zo
3394
normal! zo
3402
normal! zo
3405
normal! zo
3422
normal! zo
3422
normal! zo
3422
normal! zo
3456
normal! zo
3463
normal! zo
3467
normal! zo
3474
normal! zo
3622
normal! zo
3630
normal! zo
3631
normal! zo
3641
normal! zo
3646
normal! zo
3709
normal! zo
3709
normal! zo
3709
normal! zo
3716
normal! zo
let s:l = 3727 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3727
normal! 024|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/pclase2tv.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
178
normal! zo
185
normal! zo
185
normal! zo
207
normal! zo
287
normal! zo
287
normal! zo
287
normal! zo
let s:l = 23 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
23
normal! 058|
lcd ~/Geotexan/src/Geotex-INN
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
60
normal! zo
70
normal! zo
let s:l = 63 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
63
normal! 07|
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
297
normal! zo
360
normal! zo
387
normal! zo
416
normal! zo
1676
normal! zo
1797
normal! zo
1839
normal! zo
1950
normal! zo
1983
normal! zo
1991
normal! zo
1993
normal! zo
1999
normal! zo
1999
normal! zo
1999
normal! zo
1999
normal! zo
2020
normal! zo
2031
normal! zo
2031
normal! zo
2126
normal! zo
2175
normal! zo
2861
normal! zo
3833
normal! zo
3864
normal! zo
3864
normal! zo
3864
normal! zo
3864
normal! zo
3864
normal! zo
3864
normal! zo
3864
normal! zo
3864
normal! zo
3864
normal! zo
3864
normal! zo
3864
normal! zo
3866
normal! zo
3866
normal! zo
3866
normal! zo
3866
normal! zo
3866
normal! zo
3866
normal! zo
3866
normal! zo
3866
normal! zo
3866
normal! zo
3866
normal! zo
3866
normal! zo
3868
normal! zo
3868
normal! zo
3868
normal! zo
3868
normal! zo
3868
normal! zo
3868
normal! zo
3868
normal! zo
3868
normal! zo
3868
normal! zo
3868
normal! zo
3868
normal! zo
3870
normal! zo
3870
normal! zo
3870
normal! zo
3870
normal! zo
3870
normal! zo
3870
normal! zo
3870
normal! zo
3870
normal! zo
3870
normal! zo
3870
normal! zo
3870
normal! zo
3872
normal! zo
3872
normal! zo
3872
normal! zo
3872
normal! zo
3872
normal! zo
3872
normal! zo
3872
normal! zo
3872
normal! zo
3872
normal! zo
3872
normal! zo
3872
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3874
normal! zo
3877
normal! zo
3884
normal! zo
3885
normal! zo
3885
normal! zo
3885
normal! zo
3885
normal! zo
3885
normal! zo
3887
normal! zo
3888
normal! zo
3893
normal! zo
3894
normal! zo
3908
normal! zo
3913
normal! zo
3914
normal! zo
3914
normal! zo
3914
normal! zo
3919
normal! zo
3919
normal! zo
3919
normal! zo
3922
normal! zo
3928
normal! zo
4669
normal! zo
5949
normal! zo
6014
normal! zo
6023
normal! zo
6023
normal! zo
6023
normal! zo
6023
normal! zo
6023
normal! zo
6023
normal! zo
6025
normal! zo
6613
normal! zo
6714
normal! zo
6714
normal! zo
6714
normal! zo
6714
normal! zo
6714
normal! zo
7002
normal! zo
7347
normal! zo
7365
normal! zo
7461
normal! zo
7483
normal! zo
7782
normal! zo
7906
normal! zo
7906
normal! zo
7906
normal! zo
7906
normal! zo
7906
normal! zo
7906
normal! zo
7975
normal! zo
7982
normal! zo
7988
normal! zo
8472
normal! zo
9275
normal! zo
11391
normal! zo
11778
normal! zo
11778
normal! zo
11778
normal! zo
11778
normal! zo
11778
normal! zo
11992
normal! zo
12151
normal! zo
12151
normal! zo
12308
normal! zo
12308
normal! zo
12308
normal! zo
12322
normal! zo
12424
normal! zo
12424
normal! zo
12424
normal! zo
12424
normal! zo
12424
normal! zo
12774
normal! zo
12774
normal! zo
12774
normal! zo
12774
normal! zo
12774
normal! zo
12774
normal! zo
12774
normal! zo
12807
normal! zo
12808
normal! zo
12811
normal! zo
12825
normal! zo
14775
normal! zo
15267
normal! zo
15296
normal! zo
16294
normal! zo
16433
normal! zo
16442
normal! zo
16450
normal! zo
16451
normal! zo
16452
normal! zo
16473
normal! zo
16537
normal! zo
16537
normal! zo
16537
normal! zo
16735
normal! zo
16921
normal! zo
16929
normal! zo
16934
normal! zo
17048
normal! zo
17069
normal! zo
17088
normal! zo
17122
normal! zo
17132
normal! zo
17135
normal! zo
17344
normal! zo
17433
normal! zo
17447
normal! zo
17450
normal! zo
17454
normal! zo
17455
normal! zo
17715
normal! zo
17739
normal! zo
17744
normal! zo
17915
normal! zo
18209
normal! zo
19035
normal! zo
19085
normal! zo
21480
normal! zo
21490
normal! zo
21539
normal! zo
21540
normal! zo
21540
normal! zo
let s:l = 16920 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16920
normal! 020|
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
112
normal! zo
127
normal! zo
129
normal! zo
131
normal! zo
131
normal! zo
131
normal! zo
131
normal! zo
131
normal! zo
131
normal! zo
131
normal! zo
131
normal! zo
234
normal! zo
2945
normal! zo
2963
normal! zo
3026
normal! zo
3470
normal! zo
3470
normal! zo
3470
normal! zo
3504
normal! zo
3511
normal! zo
3515
normal! zo
3518
normal! zo
3522
normal! zo
3527
normal! zo
3528
normal! zo
3528
normal! zo
3532
normal! zo
let s:l = 3525 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3525
normal! 021|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_productividad.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
47
normal! zo
47
normal! zo
47
normal! zo
47
normal! zo
47
normal! zo
47
normal! zo
47
normal! zo
47
normal! zo
47
normal! zo
56
normal! zo
277
normal! zo
335
normal! zo
336
normal! zo
433
normal! zo
434
normal! zo
484
normal! zo
502
normal! zo
505
normal! zo
516
normal! zo
517
normal! zo
524
normal! zo
543
normal! zo
544
normal! zo
559
normal! zo
566
normal! zo
567
normal! zo
647
normal! zo
686
normal! zo
698
normal! zo
702
normal! zo
703
normal! zo
703
normal! zo
704
normal! zo
704
normal! zo
704
normal! zo
704
normal! zo
704
normal! zo
704
normal! zo
704
normal! zo
704
normal! zo
714
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
let s:l = 697 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
697
normal! 018|
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
68
normal! zo
69
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
291
normal! zo
296
normal! zo
300
normal! zo
301
normal! zo
301
normal! zo
302
normal! zo
302
normal! zo
747
normal! zo
let s:l = 812 - ((0 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
812
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
let s:l = 197 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
197
normal! 033|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
11wincmd w
exe 'vert 1resize ' . ((&columns * 28 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 88 + 58) / 117)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 88 + 58) / 117)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 88 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 88 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 88 + 58) / 117)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 88 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 88 + 58) / 117)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 88 + 58) / 117)
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 88 + 58) / 117)
exe '11resize ' . ((&lines * 26 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 88 + 58) / 117)
exe '12resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 88 + 58) / 117)
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
11wincmd w

" vim: ft=vim ro nowrap smc=128
