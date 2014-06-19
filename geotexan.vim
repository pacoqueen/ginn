" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 19 junio 2014 at 15:05:05.
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
badd +47 ginn/formularios/consulta_productividad.py
badd +590 ginn/formularios/listado_rollos.py
badd +3049 ginn/informes/geninformes.py
badd +402 ginn/informes/norma2013.py
badd +1 ginn/formularios/consumo_balas_partida.py
badd +696 ginn/formularios/utils.py
badd +847 ginn/framework/pclases/cliente.py
badd +1094 ginn/formularios/consulta_global.py
badd +1 ginn/formularios/consulta_global.glade
badd +1 ginn/framework/pclases/__init__.py
badd +57 ginn/formularios/consumo_fibra_por_partida_gtx.py
badd +1 extra/scripts/clouseau.glade
badd +1 ginn/formularios/presupuestos.py
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
badd +1659 ginn/lib/cairoplot/cairoplot.py
badd +1 ginn/formularios/consulta_pedidos_clientes.py
badd +1439 ginn/formularios/pedidos_de_venta.py
badd +1230 ginn/formularios/clientes.py
badd +28 ginn/lib/cagraph/cagraph/ca_graph.py
badd +129 ginn/lib/cagraph/cagraph/ca_graph_file.py
badd +93 ginn/lib/cagraph/cagraph/axis/yaxis.py
badd +1 ginn/formularios/widgets.py
badd +135 ginn/formularios/custom_widgets/gtkcairoplot.py
badd +1 ginn/formularios/albaranes_de_salida.py
args formularios/auditviewer.py
set lines=48 columns=117
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
exe 'vert 1resize ' . ((&columns * 29 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 87 + 58) / 117)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 87 + 58) / 117)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 87 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 87 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 87 + 58) / 117)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 87 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 87 + 58) / 117)
exe '9resize ' . ((&lines * 26 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 87 + 58) / 117)
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 87 + 58) / 117)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 87 + 58) / 117)
exe '12resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 87 + 58) / 117)
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
let s:l = 69 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
69
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
2468
normal! zo
2568
normal! zo
6528
normal! zo
6551
normal! zo
6558
normal! zo
6629
normal! zo
6917
normal! zo
7292
normal! zo
7292
normal! zo
7292
normal! zo
7307
normal! zo
7376
normal! zo
7463
normal! zo
7697
normal! zo
7821
normal! zo
9988
normal! zo
10001
normal! zc
10145
normal! zo
10212
normal! zo
10232
normal! zo
10232
normal! zo
10232
normal! zo
10371
normal! zo
10387
normal! zo
10392
normal! zo
10476
normal! zo
14674
normal! zo
15195
normal! zo
16078
normal! zo
16130
normal! zo
16630
normal! zo
16737
normal! zo
18386
normal! zo
18419
normal! zo
18421
normal! zo
18451
normal! zo
18463
normal! zo
18465
normal! zo
19271
normal! zo
19299
normal! zo
let s:l = 138 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
138
normal! 09|
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
let s:l = 30 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
30
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
let s:l = 506 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
506
normal! 043|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consumo_balas_partida.py
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
150
normal! zo
let s:l = 160 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
160
normal! 031|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consumo_fibra_por_partida_gtx.py
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
72
normal! zo
72
normal! zo
160
normal! zo
169
normal! zo
170
normal! zo
231
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
239
normal! zo
246
normal! zo
252
normal! zo
259
normal! zo
260
normal! zo
277
normal! zo
311
normal! zo
312
normal! zo
312
normal! zo
332
normal! zo
338
normal! zo
341
normal! zo
349
normal! zo
352
normal! zo
360
normal! zo
363
normal! zo
373
normal! zo
382
normal! zo
414
normal! zo
445
normal! zo
449
normal! zo
456
normal! zo
let s:l = 520 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
520
normal! 035|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
enew
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
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
98
normal! zo
99
normal! zo
109
normal! zo
109
normal! zo
109
normal! zo
112
normal! zo
113
normal! zo
114
normal! zo
116
normal! zo
169
normal! zo
174
normal! zo
183
normal! zo
185
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
186
normal! zo
186
normal! zo
186
normal! zo
200
normal! zo
243
normal! zo
247
normal! zo
247
normal! zo
336
normal! zo
337
normal! zo
346
normal! zo
351
normal! zo
351
normal! zo
351
normal! zo
351
normal! zo
353
normal! zo
353
normal! zo
361
normal! zo
374
normal! zo
375
normal! zo
376
normal! zo
384
normal! zo
407
normal! zo
468
normal! zo
469
normal! zo
469
normal! zo
474
normal! zo
474
normal! zo
479
normal! zo
479
normal! zo
496
normal! zo
543
normal! zo
577
normal! zo
578
normal! zo
592
normal! zo
633
normal! zo
641
normal! zo
648
normal! zo
651
normal! zo
652
normal! zo
652
normal! zo
652
normal! zo
677
normal! zo
681
normal! zo
682
normal! zo
682
normal! zo
686
normal! zo
687
normal! zo
691
normal! zo
696
normal! zo
726
normal! zo
734
normal! zo
749
normal! zo
750
normal! zo
750
normal! zo
750
normal! zo
802
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
820
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
845
normal! zo
852
normal! zo
856
normal! zo
860
normal! zo
864
normal! zo
869
normal! zo
869
normal! zo
874
normal! zo
874
normal! zo
874
normal! zo
874
normal! zo
874
normal! zo
874
normal! zo
874
normal! zo
874
normal! zo
874
normal! zo
874
normal! zo
878
normal! zo
878
normal! zo
878
normal! zo
878
normal! zo
878
normal! zo
878
normal! zo
878
normal! zo
878
normal! zo
878
normal! zo
878
normal! zo
881
normal! zo
884
normal! zo
901
normal! zo
1082
normal! zo
1094
normal! zo
1111
normal! zo
1112
normal! zo
1116
normal! zo
1126
normal! zo
1147
normal! zo
1154
normal! zo
1170
normal! zo
1203
normal! zo
1213
normal! zo
1214
normal! zo
1242
normal! zo
1274
normal! zo
1275
normal! zo
1278
normal! zo
1285
normal! zo
1292
normal! zo
1292
normal! zo
1292
normal! zo
1292
normal! zo
1292
normal! zo
1292
normal! zo
1292
normal! zo
1292
normal! zo
1292
normal! zo
1292
normal! zo
1292
normal! zo
1352
normal! zo
1356
normal! zo
1363
normal! zo
1382
normal! zo
1411
normal! zo
1414
normal! zo
1419
normal! zo
1420
normal! zo
1421
normal! zo
1432
normal! zo
1586
normal! zo
1691
normal! zo
1734
normal! zo
1816
normal! zo
1827
normal! zo
1906
normal! zo
1917
normal! zo
1921
normal! zo
1932
normal! zo
1933
normal! zo
1933
normal! zo
1934
normal! zo
1974
normal! zo
2017
normal! zo
2017
normal! zo
2017
normal! zo
2017
normal! zo
2017
normal! zo
2017
normal! zo
2017
normal! zo
2017
normal! zo
2034
normal! zo
2061
normal! zo
2234
normal! zo
2243
normal! zo
2260
normal! zo
2261
normal! zo
2262
normal! zo
2263
normal! zo
2307
normal! zo
2327
normal! zo
2327
normal! zo
2329
normal! zo
2329
normal! zo
2332
normal! zo
2337
normal! zo
2337
normal! zo
2337
normal! zo
2337
normal! zo
2366
normal! zo
2377
normal! zo
2393
normal! zo
2394
normal! zo
2405
normal! zo
2543
normal! zo
2556
normal! zo
2559
normal! zo
2560
normal! zo
2570
normal! zo
2575
normal! zo
2575
normal! zo
2575
normal! zo
2575
normal! zo
2575
normal! zo
2575
normal! zo
2588
normal! zo
2589
normal! zo
2589
normal! zo
2590
normal! zo
2626
normal! zo
2632
normal! zo
2633
normal! zo
2634
normal! zo
2677
normal! zo
2686
normal! zo
2712
normal! zo
2721
normal! zo
2722
normal! zo
2726
normal! zo
2737
normal! zo
2741
normal! zo
2742
normal! zo
2753
normal! zo
2838
normal! zo
2845
normal! zo
2846
normal! zo
2852
normal! zo
2898
normal! zo
2903
normal! zo
2903
normal! zo
2903
normal! zo
2903
normal! zo
2903
normal! zo
2934
normal! zo
2936
normal! zo
2939
normal! zo
2968
normal! zo
2970
normal! zo
3006
normal! zo
3011
normal! zo
3021
normal! zo
3021
normal! zo
3021
normal! zo
3022
normal! zo
3051
normal! zo
3072
normal! zo
3180
normal! zo
3181
normal! zo
3181
normal! zo
3181
normal! zo
3181
normal! zo
3181
normal! zo
3185
normal! zo
3185
normal! zo
3185
normal! zo
3185
normal! zo
3194
normal! zo
3195
normal! zo
3195
normal! zo
3195
normal! zo
3195
normal! zo
3195
normal! zo
3195
normal! zo
3195
normal! zo
3195
normal! zo
3199
normal! zo
3200
normal! zo
3200
normal! zo
3200
normal! zo
3200
normal! zo
3204
normal! zo
3205
normal! zo
3205
normal! zo
3205
normal! zo
3205
normal! zo
3205
normal! zo
3210
normal! zo
3210
normal! zo
3210
normal! zo
3210
normal! zo
3224
normal! zo
3277
normal! zo
3292
normal! zo
3293
normal! zo
3293
normal! zo
3294
normal! zo
3297
normal! zo
3298
normal! zo
3298
normal! zo
3299
normal! zo
3345
normal! zo
3346
normal! zo
3346
normal! zo
3346
normal! zo
3346
normal! zo
3347
normal! zo
3352
normal! zo
3353
normal! zo
3353
normal! zo
3353
normal! zo
3353
normal! zo
3354
normal! zo
3371
normal! zo
3383
normal! zo
3384
normal! zo
3385
normal! zo
3402
normal! zo
3402
normal! zo
3430
normal! zo
3438
normal! zo
3438
normal! zo
3438
normal! zo
3438
normal! zo
3485
normal! zo
3487
normal! zo
3491
normal! zo
3491
normal! zo
3566
normal! zo
3569
normal! zo
3592
normal! zo
3597
normal! zo
3598
normal! zo
3627
normal! zo
3628
normal! zo
3634
normal! zo
3635
normal! zo
3635
normal! zo
3644
normal! zo
3646
normal! zo
3653
normal! zo
3654
normal! zo
3654
normal! zo
3654
normal! zo
3654
normal! zo
3660
normal! zo
3662
normal! zo
3663
normal! zo
3667
normal! zo
3668
normal! zo
3668
normal! zo
3668
normal! zo
3674
normal! zo
3678
normal! zo
3679
normal! zo
3679
normal! zo
3679
normal! zo
3685
normal! zo
3688
normal! zo
3689
normal! zo
3689
normal! zo
3689
normal! zo
3695
normal! zo
3698
normal! zo
3699
normal! zo
3699
normal! zo
3699
normal! zo
3705
normal! zo
3706
normal! zo
3706
normal! zo
3706
normal! zo
3706
normal! zo
3773
normal! zo
3774
normal! zo
3777
normal! zo
3778
normal! zo
3781
normal! zo
3792
normal! zo
3870
normal! zo
3871
normal! zo
3901
normal! zo
3912
normal! zo
3913
normal! zo
3913
normal! zo
3916
normal! zo
3916
normal! zo
3989
normal! zo
3997
normal! zo
4032
normal! zo
4035
normal! zo
4051
normal! zo
4054
normal! zo
4055
normal! zo
4055
normal! zo
4056
normal! zo
4096
normal! zo
4099
normal! zo
4100
normal! zo
4100
normal! zo
4101
normal! zo
4117
normal! zo
4122
normal! zo
4123
normal! zo
4138
normal! zo
4142
normal! zo
4152
normal! zo
4163
normal! zo
4165
normal! zo
4165
normal! zo
4165
normal! zo
4165
normal! zo
4165
normal! zo
4171
normal! zo
4205
normal! zo
4231
normal! zo
4234
normal! zo
4235
normal! zo
4235
normal! zo
4237
normal! zo
4237
normal! zo
4237
normal! zo
4237
normal! zo
4237
normal! zo
4237
normal! zo
4237
normal! zo
4239
normal! zo
4240
normal! zo
4240
normal! zo
4315
normal! zo
4317
normal! zo
4317
normal! zo
4317
normal! zo
4317
normal! zo
4319
normal! zo
4319
normal! zo
4319
normal! zo
4319
normal! zo
4323
normal! zo
4323
normal! zo
4323
normal! zo
4325
normal! zo
4325
normal! zo
4325
normal! zo
4338
normal! zo
4350
normal! zo
4358
normal! zo
4358
normal! zo
4358
normal! zo
4358
normal! zo
4358
normal! zo
4361
normal! zo
4361
normal! zo
4361
normal! zo
4370
normal! zo
4374
normal! zo
4374
normal! zo
4377
normal! zo
4381
normal! zo
4381
normal! zo
4384
normal! zo
4406
normal! zo
4407
normal! zo
4410
normal! zo
4411
normal! zo
4411
normal! zo
4411
normal! zo
4411
normal! zo
4411
normal! zo
4411
normal! zo
4413
normal! zo
4420
normal! zo
4434
normal! zo
4438
normal! zo
4439
normal! zo
4443
normal! zo
4444
normal! zo
4444
normal! zo
4456
normal! zo
4458
normal! zo
4459
normal! zo
4460
normal! zo
4461
normal! zo
4466
normal! zo
4473
normal! zo
4479
normal! zo
4480
normal! zo
4486
normal! zo
4487
normal! zo
4496
normal! zo
4497
normal! zo
4497
normal! zo
4498
normal! zo
4503
normal! zo
4510
normal! zo
4510
normal! zo
4518
normal! zo
4520
normal! zo
4521
normal! zo
4521
normal! zo
4521
normal! zo
4521
normal! zo
4521
normal! zo
4521
normal! zo
4521
normal! zo
4522
normal! zo
4531
normal! zo
4532
normal! zo
4533
normal! zo
4534
normal! zo
4536
normal! zo
4537
normal! zo
4537
normal! zo
4541
normal! zo
4541
normal! zo
4542
normal! zo
4553
normal! zo
4571
normal! zo
4579
normal! zo
4585
normal! zo
4588
normal! zo
4591
normal! zo
4592
normal! zo
4594
normal! zo
4779
normal! zo
4798
normal! zo
4800
normal! zo
4800
normal! zo
4800
normal! zo
4800
normal! zo
4810
normal! zo
4818
normal! zo
4818
normal! zo
4818
normal! zo
4823
normal! zo
4825
normal! zo
4825
normal! zo
4825
normal! zo
4825
normal! zo
4825
normal! zo
4825
normal! zo
4835
normal! zo
4854
normal! zo
4870
normal! zo
4937
normal! zo
4945
normal! zo
4997
normal! zo
5016
normal! zo
5017
normal! zo
5021
normal! zo
5036
normal! zo
5036
normal! zo
let s:l = 2954 - ((10 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2954
normal! 035|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_pedidos_clientes.py
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
62
normal! zo
175
normal! zo
189
normal! zo
195
normal! zo
227
normal! zo
235
normal! zo
288
normal! zo
300
normal! zo
300
normal! zo
300
normal! zo
300
normal! zo
let s:l = 233 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
233
normal! 036|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/widgets.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 94 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
94
normal! 07|
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
63
normal! zo
63
normal! zo
63
normal! zo
63
normal! zo
67
normal! zo
246
normal! zo
247
normal! zo
258
normal! zo
259
normal! zo
260
normal! zo
295
normal! zo
296
normal! zo
402
normal! zo
1272
normal! zo
1409
normal! zo
1775
normal! zo
1862
normal! zo
1864
normal! zo
1970
normal! zo
2121
normal! zo
2214
normal! zo
2214
normal! zo
2214
normal! zo
2214
normal! zo
2214
normal! zo
2214
normal! zo
2214
normal! zo
2277
normal! zo
2281
normal! zo
2595
normal! zo
2614
normal! zo
let s:l = 1397 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1397
normal! 019|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
9wincmd w
exe 'vert 1resize ' . ((&columns * 29 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 87 + 58) / 117)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 87 + 58) / 117)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 87 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 87 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 87 + 58) / 117)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 87 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 87 + 58) / 117)
exe '9resize ' . ((&lines * 26 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 87 + 58) / 117)
exe '10resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 87 + 58) / 117)
exe '11resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 11resize ' . ((&columns * 87 + 58) / 117)
exe '12resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 12resize ' . ((&columns * 87 + 58) / 117)
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
