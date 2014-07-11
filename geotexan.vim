" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 11 julio 2014 at 14:15:32.
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
badd +85 ginn/formularios/consulta_producido.py
badd +126 ginn/formularios/consulta_consumo.py
badd +41 ginn/framework/memoize.py
badd +596 ginn/formularios/presupuesto.py
badd +590 ginn/formularios/listado_rollos.py
badd +7346 ginn/informes/geninformes.py
badd +402 ginn/informes/norma2013.py
badd +696 ginn/formularios/utils.py
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
badd +1 ginn/framework/pclases/superfacturaventa.py
badd +1867 ginn/formularios/facturas_compra.py
badd +111 ginn/formularios/prefacturas.py
badd +1020 ginn/formularios/pedidos_de_venta.py
badd +5 ginn/formularios/launcher.py
badd +17415 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/pclase2tv.py
badd +1 ginn/formularios/abonos_venta.glade
badd +428 ginn/formularios/clientes.py
badd +513 ginn/formularios/crm_detalles_factura.py
badd +406 ginn/formularios/crm_seguimiento_impagos.py
badd +1 extra/scripts/clouseau-gtk.py
badd +1 extra/scripts/clouseau.py
badd +1 ginn/framework/configuracion.py
badd +1 ginn/formularios/menu.py
args formularios/auditviewer.py
set lines=39 columns=82
edit extra/scripts/clouseau.py
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
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
11wincmd k
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
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 1 + 19) / 39)
exe '2resize ' . ((&lines * 1 + 19) / 39)
exe '3resize ' . ((&lines * 1 + 19) / 39)
exe '4resize ' . ((&lines * 1 + 19) / 39)
exe '5resize ' . ((&lines * 1 + 19) / 39)
exe '6resize ' . ((&lines * 1 + 19) / 39)
exe '7resize ' . ((&lines * 1 + 19) / 39)
exe '8resize ' . ((&lines * 1 + 19) / 39)
exe '9resize ' . ((&lines * 15 + 19) / 39)
exe '10resize ' . ((&lines * 1 + 19) / 39)
exe '11resize ' . ((&lines * 1 + 19) / 39)
exe '12resize ' . ((&lines * 1 + 19) / 39)
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
74
normal! zo
508
normal! zo
518
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
527
normal! zo
539
normal! zo
869
normal! zo
880
normal! zo
899
normal! zo
900
normal! zo
903
normal! zo
905
normal! zo
913
normal! zo
937
normal! zo
951
normal! zo
996
normal! zo
1002
normal! zo
1009
normal! zo
let s:l = 41 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
41
normal! 012|
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
normal! 049|
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
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/menu.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
165
normal! zo
166
normal! zo
305
normal! zo
314
normal! zo
325
normal! zo
426
normal! zo
431
normal! zo
609
normal! zo
610
normal! zo
636
normal! zo
699
normal! zo
711
normal! zo
712
normal! zo
750
normal! zo
751
normal! zo
752
normal! zo
758
normal! zo
759
normal! zo
759
normal! zo
759
normal! zo
907
normal! zo
938
normal! zo
942
normal! zo
944
normal! zo
944
normal! zo
944
normal! zo
972
normal! zo
let s:l = 730 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
730
normal! 051|
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
17116
normal! zo
17126
normal! zo
17129
normal! zo
17427
normal! zo
17441
normal! zo
17444
normal! zo
17448
normal! zo
17449
normal! zo
17709
normal! zo
17733
normal! zo
17738
normal! zo
17909
normal! zo
19079
normal! zo
21474
normal! zo
21484
normal! zo
21533
normal! zo
21534
normal! zo
21534
normal! zo
let s:l = 143 - ((5 * winheight(0) + 7) / 15)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
143
normal! 04|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/clientes.py
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
1469
normal! zo
1627
normal! zo
1636
normal! zo
1684
normal! zo
1688
normal! zo
1692
normal! zo
1694
normal! zo
1695
normal! zo
1695
normal! zo
1698
normal! zo
1702
normal! zo
1703
normal! zo
1709
normal! zo
1715
normal! zo
1715
normal! zo
1717
normal! zo
1795
normal! zo
1808
normal! zo
1813
normal! zo
1813
normal! zo
1813
normal! zo
1813
normal! zo
1813
normal! zo
1813
normal! zo
1850
normal! zo
1850
normal! zo
1850
normal! zo
1850
normal! zo
1850
normal! zo
1909
normal! zo
1992
normal! zo
1993
normal! zo
1993
normal! zo
1993
normal! zo
2056
normal! zo
2061
normal! zo
2062
normal! zo
2062
normal! zo
2062
normal! zo
2069
normal! zo
2076
normal! zo
2077
normal! zo
2083
normal! zo
2102
normal! zo
2104
normal! zo
2119
normal! zo
2127
normal! zo
2127
normal! zo
2127
normal! zo
2127
normal! zo
2131
normal! zo
2131
normal! zo
2134
normal! zo
2134
normal! zo
2134
normal! zo
2134
normal! zo
2134
normal! zo
2136
normal! zo
2136
normal! zo
2139
normal! zo
2141
normal! zo
2151
normal! zo
2188
normal! zo
2189
normal! zo
let s:l = 2068 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2068
normal! 023|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_producido.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
62
normal! zo
63
normal! zo
76
normal! zo
76
normal! zo
76
normal! zo
117
normal! zo
121
normal! zo
127
normal! zo
167
normal! zo
192
normal! zo
308
normal! zo
308
normal! zo
308
normal! zo
308
normal! zo
479
normal! zo
480
normal! zo
484
normal! zo
660
normal! zo
681
normal! zo
let s:l = 56 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
56
normal! 054|
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
71
normal! zo
75
normal! zo
149
normal! zo
159
normal! zo
225
normal! zo
234
normal! zo
274
normal! zo
278
normal! zo
281
normal! zo
294
normal! zo
308
normal! zo
309
normal! zo
310
normal! zo
311
normal! zo
311
normal! zo
329
normal! zo
345
normal! zo
350
normal! zo
369
normal! zo
373
normal! zo
373
normal! zo
395
normal! zo
let s:l = 402 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
402
normal! 040|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
9wincmd w
exe '1resize ' . ((&lines * 1 + 19) / 39)
exe '2resize ' . ((&lines * 1 + 19) / 39)
exe '3resize ' . ((&lines * 1 + 19) / 39)
exe '4resize ' . ((&lines * 1 + 19) / 39)
exe '5resize ' . ((&lines * 1 + 19) / 39)
exe '6resize ' . ((&lines * 1 + 19) / 39)
exe '7resize ' . ((&lines * 1 + 19) / 39)
exe '8resize ' . ((&lines * 1 + 19) / 39)
exe '9resize ' . ((&lines * 15 + 19) / 39)
exe '10resize ' . ((&lines * 1 + 19) / 39)
exe '11resize ' . ((&lines * 1 + 19) / 39)
exe '12resize ' . ((&lines * 1 + 19) / 39)
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
9wincmd w

" vim: ft=vim ro nowrap smc=128
