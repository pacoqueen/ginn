" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 04 julio 2014 at 14:47:29.
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
badd +247 ginn/formularios/consulta_consumo.py
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
badd +1 ginn/framework/pclases/__init__.py
badd +1 ginn/formularios/presupuestos.py
badd +3551 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/pclase2tv.py
badd +1 ginn/formularios/abonos_venta.glade
badd +428 ginn/formularios/clientes.py
badd +513 ginn/formularios/crm_detalles_factura.py
badd +406 ginn/formularios/crm_seguimiento_impagos.py
args formularios/auditviewer.py
set lines=48 columns=118
edit extra/scripts/balas_basura_reembaladas.py
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
exe 'vert 1resize ' . ((&columns * 28 + 59) / 118)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 89 + 59) / 118)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 89 + 59) / 118)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 89 + 59) / 118)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 89 + 59) / 118)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 89 + 59) / 118)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 89 + 59) / 118)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 89 + 59) / 118)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 89 + 59) / 118)
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 89 + 59) / 118)
exe '11resize ' . ((&lines * 8 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 89 + 59) / 118)
exe '12resize ' . ((&lines * 17 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 89 + 59) / 118)
exe '13resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 13resize ' . ((&columns * 89 + 59) / 118)
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
let s:l = 70 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
70
normal! 076|
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
let s:l = 882 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
882
normal! 050|
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
271
normal! zo
334
normal! zo
392
normal! zo
1652
normal! zo
1773
normal! zo
1815
normal! zo
1925
normal! zo
1992
normal! zo
2096
normal! zo
2145
normal! zo
2784
normal! zo
2808
normal! zo
2878
normal! zo
3142
normal! zo
3157
normal! zo
6860
normal! zo
6886
normal! zo
6892
normal! zo
7738
normal! zo
7862
normal! zo
7862
normal! zo
7862
normal! zo
7862
normal! zo
7862
normal! zo
7862
normal! zo
7931
normal! zo
7938
normal! zo
7944
normal! zo
8428
normal! zo
11347
normal! zo
11734
normal! zo
11734
normal! zo
11734
normal! zo
11734
normal! zo
11734
normal! zo
11948
normal! zo
11973
normal! zo
11977
normal! zo
11977
normal! zo
11978
normal! zo
11979
normal! zo
11979
normal! zo
12107
normal! zo
12107
normal! zo
12148
normal! zo
12148
normal! zo
12148
normal! zo
12148
normal! zo
12148
normal! zo
12152
normal! zo
12153
normal! zo
12153
normal! zo
12153
normal! zo
12153
normal! zo
12153
normal! zo
12153
normal! zo
12190
normal! zo
12192
normal! zo
12197
normal! zo
12264
normal! zo
12264
normal! zo
12264
normal! zo
12278
normal! zo
let s:l = 15894 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15894
normal! 0
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
let s:l = 914 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
914
normal! 09|
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
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
208
normal! zo
215
normal! zo
216
normal! zo
216
normal! zo
216
normal! zo
216
normal! zo
216
normal! zo
216
normal! zo
423
normal! zo
444
normal! zo
453
normal! zo
513
normal! zo
521
normal! zo
632
normal! zo
851
normal! zo
870
normal! zo
903
normal! zo
965
normal! zo
1003
normal! zo
1018
normal! zo
1028
normal! zo
1047
normal! zo
1096
normal! zo
1103
normal! zo
1103
normal! zo
1108
normal! zo
1109
normal! zo
1114
normal! zo
1116
normal! zo
1163
normal! zo
1179
normal! zo
1195
normal! zo
1195
normal! zo
1195
normal! zo
1195
normal! zo
1195
normal! zo
1195
normal! zo
1228
normal! zo
1235
normal! zo
1237
normal! zo
1265
normal! zo
1295
normal! zo
1620
normal! zo
1624
normal! zo
1627
normal! zo
1633
normal! zo
1633
normal! zo
1633
normal! zo
1633
normal! zo
1633
normal! zo
1633
normal! zo
1661
normal! zo
1750
normal! zo
1761
normal! zo
1798
normal! zo
1806
normal! zo
1824
normal! zo
1827
normal! zo
1871
normal! zo
1871
normal! zo
1871
normal! zo
1993
normal! zo
2146
normal! zo
2332
normal! zo
2338
normal! zo
2339
normal! zo
2549
normal! zo
2555
normal! zo
2561
normal! zo
2562
normal! zo
2563
normal! zo
2716
normal! zo
2819
normal! zo
2825
normal! zo
2852
normal! zo
2904
normal! zo
2907
normal! zo
2915
normal! zo
2931
normal! zo
3131
normal! zo
3248
normal! zo
3262
normal! zo
3291
normal! zo
3407
normal! zo
let s:l = 3384 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3384
normal! 05|
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
let s:l = 316 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
316
normal! 031|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/albaranes_de_salida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
100
normal! zo
101
normal! zo
123
normal! zo
123
normal! zo
123
normal! zo
1084
normal! zo
2900
normal! zo
3117
normal! zo
3433
normal! zo
3441
normal! zo
3441
normal! zo
3441
normal! zo
3441
normal! zo
3441
normal! zo
3441
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
3538
normal! zo
3538
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3541
normal! zo
3550
normal! zo
let s:l = 3555 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3555
normal! 014|
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
4625
normal! zo
5905
normal! zo
5970
normal! zo
5979
normal! zo
5979
normal! zo
5979
normal! zo
5979
normal! zo
5979
normal! zo
5979
normal! zo
5981
normal! zo
11347
normal! zo
14731
normal! zo
15252
normal! zo
16250
normal! zo
16690
normal! zo
17071
normal! zo
17081
normal! zo
17084
normal! zo
17664
normal! zo
17688
normal! zo
17693
normal! zo
17864
normal! zo
let s:l = 5982 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5982
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
61
normal! zo
62
normal! zo
75
normal! zo
75
normal! zo
75
normal! zo
116
normal! zo
120
normal! zo
126
normal! zo
166
normal! zo
191
normal! zo
307
normal! zo
478
normal! zo
479
normal! zo
483
normal! zo
let s:l = 1029 - ((0 * winheight(0) + 4) / 8)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1029
normal! 09|
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
77
normal! zo
77
normal! zo
77
normal! zo
77
normal! zo
161
normal! zo
161
normal! zo
161
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
198
normal! zo
208
normal! zo
215
normal! zo
216
normal! zo
216
normal! zo
216
normal! zo
216
normal! zo
216
normal! zo
216
normal! zo
327
normal! zo
341
normal! zo
341
normal! zo
341
normal! zo
341
normal! zo
341
normal! zo
341
normal! zo
632
normal! zo
677
normal! zo
678
normal! zo
685
normal! zo
1228
normal! zo
1235
normal! zo
1237
normal! zo
1945
normal! zo
1954
normal! zo
1955
normal! zo
1993
normal! zo
2068
normal! zo
2074
normal! zo
2075
normal! zo
2124
normal! zo
2575
normal! zo
2621
normal! zo
2640
normal! zo
2648
normal! zo
2716
normal! zo
2733
normal! zo
2735
normal! zo
2750
normal! zo
3131
normal! zo
3145
normal! zo
3150
normal! zo
3156
normal! zo
3169
normal! zo
3170
normal! zo
3291
normal! zo
3294
normal! zo
3295
normal! zo
let s:l = 199 - ((14 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
199
normal! 09|
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
12wincmd w
exe 'vert 1resize ' . ((&columns * 28 + 59) / 118)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 89 + 59) / 118)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 89 + 59) / 118)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 89 + 59) / 118)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 89 + 59) / 118)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 89 + 59) / 118)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 89 + 59) / 118)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 89 + 59) / 118)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 89 + 59) / 118)
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 89 + 59) / 118)
exe '11resize ' . ((&lines * 8 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 89 + 59) / 118)
exe '12resize ' . ((&lines * 17 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 89 + 59) / 118)
exe '13resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 13resize ' . ((&columns * 89 + 59) / 118)
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
12wincmd w

" vim: ft=vim ro nowrap smc=128
