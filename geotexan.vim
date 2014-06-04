" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 04 junio 2014 at 09:19:42.
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
badd +104 extra/scripts/clouseau.py
badd +1 extra/scripts/balas_basura_reembaladas.py
badd +19 ginn/informes/nied.py
badd +129 ginn/informes/ekotex.py
badd +1 formularios/auditviewer.py
badd +248 ginn/formularios/gtkexcepthook.py
badd +20 extra/scripts/clouseau-gtk.py
badd +133 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1 ginn/formularios/partes_de_fabricacion_gtx.py
badd +1 ginn/formularios/partes_de_ancho_multiple.py
badd +1 ginn/formularios/consulta_producido.py
badd +247 ginn/formularios/consulta_consumo.py
badd +41 ginn/framework/memoize.py
badd +596 ginn/formularios/presupuesto.py
badd +47 ginn/formularios/consulta_productividad.py
badd +590 ginn/formularios/listado_rollos.py
badd +3049 ginn/informes/geninformes.py
badd +402 ginn/informes/norma2013.py
badd +99 ginn/formularios/consulta_ventas.py
badd +1 ginn/formularios/consumo_balas_partida.py
badd +696 ginn/formularios/utils.py
badd +847 ginn/framework/pclases/cliente.py
badd +851 ginn/formularios/consulta_global.py
badd +1 ginn/formularios/consulta_global.glade
badd +1 ginn/framework/pclases/__init__.py
badd +57 ginn/formularios/consumo_fibra_por_partida_gtx.py
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
exe 'vert 1resize ' . ((&columns * 31 + 59) / 118)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 86 + 59) / 118)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 86 + 59) / 118)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 86 + 59) / 118)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 86 + 59) / 118)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 86 + 59) / 118)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 86 + 59) / 118)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 86 + 59) / 118)
exe '9resize ' . ((&lines * 19 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 86 + 59) / 118)
exe '10resize ' . ((&lines * 12 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 86 + 59) / 118)
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
16629
normal! zo
16736
normal! zo
let s:l = 17294 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
17294
normal! 018|
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
let s:l = 159 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
159
normal! 059|
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
246
normal! zo
let s:l = 106 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
106
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
445
normal! zo
449
normal! zo
456
normal! zo
let s:l = 422 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
422
normal! 033|
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
83
normal! zo
88
normal! zo
93
normal! zo
93
normal! zo
93
normal! zo
95
normal! zo
95
normal! zo
122
normal! zo
129
normal! zo
129
normal! zo
129
normal! zo
129
normal! zo
129
normal! zo
129
normal! zo
129
normal! zo
155
normal! zo
164
normal! zo
166
normal! zo
167
normal! zo
167
normal! zo
174
normal! zo
221
normal! zo
221
normal! zo
221
normal! zo
221
normal! zo
228
normal! zo
228
normal! zo
228
normal! zo
228
normal! zo
258
normal! zo
287
normal! zo
373
normal! zo
379
normal! zo
409
normal! zo
412
normal! zo
413
normal! zo
414
normal! zo
428
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
432
normal! zo
437
normal! zo
439
normal! zo
441
normal! zo
442
normal! zo
443
normal! zo
444
normal! zo
444
normal! zo
444
normal! zo
444
normal! zo
450
normal! zo
451
normal! zo
452
normal! zo
453
normal! zo
453
normal! zo
457
normal! zo
457
normal! zo
457
normal! zo
457
normal! zo
486
normal! zo
494
normal! zo
497
normal! zo
500
normal! zo
510
normal! zo
520
normal! zo
523
normal! zo
525
normal! zo
532
normal! zo
538
normal! zo
539
normal! zo
542
normal! zo
544
normal! zo
554
normal! zo
597
normal! zo
597
normal! zo
597
normal! zo
597
normal! zo
606
normal! zo
607
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
625
normal! zo
668
normal! zo
676
normal! zo
677
normal! zo
678
normal! zo
678
normal! zo
678
normal! zo
678
normal! zo
678
normal! zo
678
normal! zo
678
normal! zo
754
normal! zo
765
normal! zo
769
normal! zo
771
normal! zo
773
normal! zo
782
normal! zo
790
normal! zo
791
normal! zo
795
normal! zo
797
normal! zo
799
normal! zo
812
normal! zo
853
normal! zo
856
normal! zo
862
normal! zo
869
normal! zo
869
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
881
normal! zo
881
normal! zo
881
normal! zo
881
normal! zo
881
normal! zo
881
normal! zo
881
normal! zo
883
normal! zo
883
normal! zo
883
normal! zo
883
normal! zo
883
normal! zo
883
normal! zo
883
normal! zo
883
normal! zo
888
normal! zo
894
normal! zo
901
normal! zo
901
normal! zo
916
normal! zo
921
normal! zo
929
normal! zo
936
normal! zo
936
normal! zo
936
normal! zo
936
normal! zo
936
normal! zo
955
normal! zo
971
normal! zo
980
normal! zo
996
normal! zo
1000
normal! zo
1062
normal! zo
1076
normal! zo
1076
normal! zo
1079
normal! zo
1084
normal! zo
1087
normal! zo
1092
normal! zo
1102
normal! zo
1107
normal! zo
1110
normal! zo
1114
normal! zo
1124
normal! zo
1147
normal! zo
1155
normal! zo
1160
normal! zo
1160
normal! zo
1160
normal! zo
1169
normal! zo
1180
normal! zo
1188
normal! zo
1194
normal! zo
1197
normal! zo
1208
normal! zo
1219
normal! zo
1226
normal! zo
1251
normal! zo
1258
normal! zo
1284
normal! zo
1294
normal! zo
1297
normal! zo
1297
normal! zo
1326
normal! zo
1330
normal! zo
1331
normal! zo
1331
normal! zo
1331
normal! zo
1331
normal! zo
1331
normal! zo
1331
normal! zo
1331
normal! zo
1335
normal! zo
1335
normal! zo
1335
normal! zo
1335
normal! zo
1336
normal! zo
1336
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1357
normal! zo
1361
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
1366
normal! zo
1367
normal! zo
1367
normal! zo
1367
normal! zo
1367
normal! zo
1367
normal! zo
1367
normal! zo
1377
normal! zo
1377
normal! zo
1377
normal! zo
1377
normal! zo
1377
normal! zo
1377
normal! zo
1377
normal! zo
1377
normal! zo
1377
normal! zo
1377
normal! zo
1399
normal! zo
1400
normal! zo
1400
normal! zo
1404
normal! zo
1404
normal! zo
1404
normal! zo
1404
normal! zo
1404
normal! zo
1404
normal! zo
1421
normal! zo
1422
normal! zo
1423
normal! zo
1429
normal! zo
1466
normal! zo
1466
normal! zo
1486
normal! zo
1496
normal! zo
1496
normal! zo
1496
normal! zo
1496
normal! zo
1496
normal! zo
1496
normal! zo
1518
normal! zo
1528
normal! zo
1528
normal! zo
1528
normal! zo
1528
normal! zo
1528
normal! zo
1528
normal! zo
1528
normal! zo
1549
normal! zo
1565
normal! zo
1565
normal! zo
1565
normal! zo
1565
normal! zo
1567
normal! zo
1567
normal! zo
1567
normal! zo
1567
normal! zo
1567
normal! zo
1567
normal! zo
1567
normal! zo
1571
normal! zo
1571
normal! zo
1571
normal! zo
1571
normal! zo
1571
normal! zo
1589
normal! zo
1591
normal! zo
1612
normal! zo
1644
normal! zo
1648
normal! zo
1650
normal! zo
1658
normal! zo
1661
normal! zo
1662
normal! zo
1662
normal! zo
1662
normal! zo
1662
normal! zo
1703
normal! zo
1761
normal! zo
1788
normal! zo
1799
normal! zo
1803
normal! zo
1807
normal! zo
1818
normal! zo
1820
normal! zo
1828
normal! zo
1848
normal! zo
1873
normal! zo
1897
normal! zo
1910
normal! zo
1911
normal! zo
1912
normal! zo
1912
normal! zo
1912
normal! zo
1917
normal! zo
1920
normal! zo
1924
normal! zo
1925
normal! zo
1926
normal! zo
1926
normal! zo
1926
normal! zo
1931
normal! zo
1933
normal! zo
1940
normal! zo
1986
normal! zo
1996
normal! zo
2026
normal! zo
2029
normal! zo
2041
normal! zo
2048
normal! zo
2066
normal! zo
2072
normal! zo
2091
normal! zo
2096
normal! zo
2109
normal! zo
2109
normal! zo
2109
normal! zo
2109
normal! zo
2109
normal! zo
2109
normal! zo
2124
normal! zo
2131
normal! zo
2134
normal! zo
2147
normal! zo
2147
normal! zo
2148
normal! zo
2180
normal! zo
2194
normal! zo
2198
normal! zo
2209
normal! zo
2213
normal! zo
2213
normal! zo
2213
normal! zo
2243
normal! zo
2246
normal! zo
2264
normal! zo
2271
normal! zo
2272
normal! zo
2273
normal! zo
2277
normal! zo
2298
normal! zo
2302
normal! zo
2302
normal! zo
2302
normal! zo
2302
normal! zo
2302
normal! zo
2302
normal! zo
2302
normal! zo
2302
normal! zo
2302
normal! zo
2302
normal! zo
2302
normal! zo
2305
normal! zo
2312
normal! zo
2312
normal! zo
2321
normal! zo
2356
normal! zo
2357
normal! zo
2366
normal! zo
2367
normal! zo
2375
normal! zo
2382
normal! zo
2382
normal! zo
2388
normal! zo
2395
normal! zo
2395
normal! zo
2400
normal! zo
2400
normal! zo
2400
normal! zo
2400
normal! zo
2400
normal! zo
2400
normal! zo
2400
normal! zo
2400
normal! zo
2400
normal! zo
2400
normal! zo
2402
normal! zo
2402
normal! zo
2402
normal! zo
2406
normal! zo
2412
normal! zo
2414
normal! zo
2416
normal! zo
2421
normal! zo
2421
normal! zo
2421
normal! zo
2444
normal! zo
2447
normal! zo
2447
normal! zo
2454
normal! zo
2457
normal! zo
2457
normal! zo
2474
normal! zo
2486
normal! zo
2489
normal! zo
2489
normal! zo
2492
normal! zo
2493
normal! zo
2493
normal! zo
2496
normal! zo
2497
normal! zo
2497
normal! zo
2500
normal! zo
2501
normal! zo
2501
normal! zo
2504
normal! zo
2505
normal! zo
2505
normal! zo
2548
normal! zo
2549
normal! zo
2549
normal! zo
2558
normal! zo
2560
normal! zo
2560
normal! zo
2560
normal! zo
2560
normal! zo
2567
normal! zo
2577
normal! zo
2599
normal! zo
2600
normal! zo
2600
normal! zo
2651
normal! zo
2662
normal! zo
2678
normal! zo
2679
normal! zo
2679
normal! zo
2691
normal! zo
2701
normal! zo
2717
normal! zo
2718
normal! zo
2718
normal! zo
2732
normal! zo
2732
normal! zo
2732
normal! zo
2732
normal! zo
2735
normal! zo
2736
normal! zo
2736
normal! zo
2736
normal! zo
2736
normal! zo
2736
normal! zo
2736
normal! zo
2744
normal! zo
2747
normal! zo
2764
normal! zo
2774
normal! zo
2778
normal! zo
2779
normal! zo
2779
normal! zo
2784
normal! zo
2789
normal! zo
2792
normal! zo
2797
normal! zo
2807
normal! zo
2823
normal! zo
2834
normal! zo
2842
normal! zo
2848
normal! zo
2851
normal! zo
2862
normal! zo
2868
normal! zo
2871
normal! zo
2881
normal! zo
2887
normal! zo
2891
normal! zo
2891
normal! zo
2895
normal! zo
2895
normal! zo
2895
normal! zo
2895
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2964
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2968
normal! zo
2973
normal! zo
2978
normal! zo
2982
normal! zo
2982
normal! zo
2986
normal! zo
2986
normal! zo
2986
normal! zo
2986
normal! zo
3040
normal! zo
3047
normal! zo
3047
normal! zo
3047
normal! zo
3047
normal! zo
3083
normal! zo
3090
normal! zo
3116
normal! zo
3121
normal! zo
3121
normal! zo
3121
normal! zo
3131
normal! zo
3131
normal! zo
3131
normal! zo
3131
normal! zo
3131
normal! zo
3131
normal! zo
3145
normal! zo
3146
normal! zo
3166
normal! zo
3176
normal! zo
3176
normal! zo
3176
normal! zo
3176
normal! zo
3176
normal! zo
3176
normal! zo
3176
normal! zo
3176
normal! zo
3176
normal! zo
3176
normal! zo
3176
normal! zo
3178
normal! zo
3178
normal! zo
3178
normal! zo
3178
normal! zo
3178
normal! zo
3178
normal! zo
3195
normal! zo
3196
normal! zo
3202
normal! zo
3203
normal! zo
3203
normal! zo
3203
normal! zo
3203
normal! zo
3203
normal! zo
3203
normal! zo
3213
normal! zo
3213
normal! zo
3213
normal! zo
3213
normal! zo
3216
normal! zo
3216
normal! zo
3216
normal! zo
3216
normal! zo
3216
normal! zo
3216
normal! zo
3216
normal! zo
3216
normal! zo
3216
normal! zo
3216
normal! zo
3232
normal! zo
3232
normal! zo
3232
normal! zo
3232
normal! zo
3232
normal! zo
3232
normal! zo
3232
normal! zo
3232
normal! zo
3232
normal! zo
3232
normal! zo
3232
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3235
normal! zo
3245
normal! zo
3245
normal! zo
3246
normal! zo
3246
normal! zo
3247
normal! zo
3251
normal! zo
3254
normal! zo
3254
normal! zo
3255
normal! zo
3264
normal! zo
3265
normal! zo
3265
normal! zo
3271
normal! zo
3301
normal! zo
3318
normal! zo
3328
normal! zo
3329
normal! zo
3333
normal! zo
3336
normal! zo
3343
normal! zo
3350
normal! zo
3354
normal! zo
3355
normal! zo
3355
normal! zo
3359
normal! zo
3366
normal! zo
3367
normal! zo
3367
normal! zo
3369
normal! zo
3381
normal! zo
3381
normal! zo
3381
normal! zo
3381
normal! zo
3381
normal! zo
3381
normal! zo
3381
normal! zo
3381
normal! zo
3381
normal! zo
3381
normal! zo
3381
normal! zo
3386
normal! zo
3387
normal! zo
3387
normal! zo
let s:l = 1078 - ((4 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1078
normal! 026|
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
1132
normal! zo
1384
normal! zo
1384
normal! zo
let s:l = 83 - ((7 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
83
normal! 048|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
9wincmd w
exe 'vert 1resize ' . ((&columns * 31 + 59) / 118)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 86 + 59) / 118)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 86 + 59) / 118)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 86 + 59) / 118)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 86 + 59) / 118)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 86 + 59) / 118)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 86 + 59) / 118)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 86 + 59) / 118)
exe '9resize ' . ((&lines * 19 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 86 + 59) / 118)
exe '10resize ' . ((&lines * 12 + 24) / 48)
exe 'vert 10resize ' . ((&columns * 86 + 59) / 118)
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
