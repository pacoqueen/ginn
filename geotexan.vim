" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 16 marzo 2016 at 18:34:31.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Monaco\ for\ Powerline\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'sierra' | colorscheme sierra | endif
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
badd +16 ginn/formularios/partes_de_ancho_multiple.py
badd +1 fugitive:///home/bogado/Geotexan/src/Geotex-INN/.git//0/ginn/formularios/utils.py
badd +9 ginn/lib/fuzzywuzzy/fuzzywuzzy/utils.py
badd +1 formularios/auditviewer.py
badd +38 ginn/informes/treeview2pdf.py
badd +138 ginn/formularios/listado_rollos.py
badd +2 ginn/lib/fuzzywuzzy/fuzzywuzzy/__init__.py
badd +706 ginn/formularios/consulta_ventas.py
badd +367 ginn/formularios/productos_compra.py
badd +902 ginn/formularios/productos_de_venta_rollos.py
badd +552 ginn/formularios/proveedores.py
badd +517 ginn/framework/pclases/cliente.py
badd +914 ginn/formularios/ventana.py
badd +17 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +1 ginn/formularios/consulta_saldo_proveedores.py
badd +123 ginn/lib/charting.py
badd +1868 ginn/formularios/partes_de_fabricacion_rollos.py
badd +72 ginn/formularios/consulta_existenciasRollos.py
badd +14 ginn/formularios/consulta_existenciasBalas.py
badd +467 db/tablas.sql
badd +1 ginn/framework/__init__.py
badd +3136 ginn/formularios/facturas_venta.py
badd +10 ginn/informes/alians_trade.py
badd +52 ginn/informes/barcode/EANBarCode.py
badd +63 ginn/informes/barcode/_barcode.py
badd +227 ginn/informes/barcode/common.py
badd +53 ginn/informes/presupuesto.py
badd +1072 ginn/formularios/abonos_venta.py
badd +2150 ginn/formularios/albaranes_de_salida.py
badd +19 ginn/formularios/consulta_ofertas.py
badd +1134 ginn/formularios/pagares_pagos.py
badd +1451 ginn/formularios/presupuestos.py
badd +1316 ginn/formularios/facturas_compra.py
badd +11628 ginn/framework/pclases/__init__.py
badd +37 ginn/api/murano/connection.py
badd +1 ginn/api/murano/__init__.py
badd +175 ginn/formularios/mail_sender.py
badd +42 ginn/informes/presupuesto2.py
badd +1 ginn/lib/xlutils/jenkins
badd +1 ginn/api/tests/murano_tests.py
badd +1 ginn/api/murano/ops.py
badd +102 ginn/formularios/utils_almacen.py
badd +1 ginn/api/murano/export.py
badd +668 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +0 ginn/api/murano/extra.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=48 columns=111
edit ginn/api/tests/murano_tests.py
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
exe 'vert 1resize ' . ((&columns * 23 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 87 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 87 + 55) / 111)
exe '4resize ' . ((&lines * 32 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 87 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 87 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 87 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 87 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 87 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 87 + 55) / 111)
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
29
normal! zo
39
normal! zo
42
normal! zo
43
normal! zo
47
normal! zo
48
normal! zo
48
normal! zo
48
normal! zo
48
normal! zo
48
normal! zo
48
normal! zo
48
normal! zo
52
normal! zo
58
normal! zo
61
normal! zo
70
normal! zo
73
normal! zo
74
normal! zo
74
normal! zo
74
normal! zo
74
normal! zo
74
normal! zo
74
normal! zo
74
normal! zo
78
normal! zo
89
normal! zo
98
normal! zo
101
normal! zo
102
normal! zo
102
normal! zo
102
normal! zo
102
normal! zo
102
normal! zo
102
normal! zo
102
normal! zo
110
normal! zo
119
normal! zo
122
normal! zo
123
normal! zo
127
normal! zo
128
normal! zo
128
normal! zo
128
normal! zo
128
normal! zo
128
normal! zo
128
normal! zo
128
normal! zo
134
normal! zo
135
normal! zo
144
normal! zo
145
normal! zo
149
normal! zo
155
normal! zo
156
normal! zo
158
normal! zo
163
normal! zo
167
normal! zo
171
normal! zo
175
normal! zo
179
normal! zo
183
normal! zo
188
normal! zo
189
normal! zo
189
normal! zo
189
normal! zo
189
normal! zo
192
normal! zo
193
normal! zo
193
normal! zo
193
normal! zo
193
normal! zo
193
normal! zo
193
normal! zo
193
normal! zo
193
normal! zo
193
normal! zo
193
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
200
normal! zo
201
normal! zo
201
normal! zo
201
normal! zo
201
normal! zo
201
normal! zo
201
normal! zo
201
normal! zo
201
normal! zo
201
normal! zo
201
normal! zo
206
normal! zo
207
normal! zo
208
normal! zo
208
normal! zo
208
normal! zo
208
normal! zo
208
normal! zo
208
normal! zo
208
normal! zo
208
normal! zo
208
normal! zo
208
normal! zo
213
normal! zo
214
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
215
normal! zo
215
normal! zo
220
normal! zo
221
normal! zo
222
normal! zo
222
normal! zo
222
normal! zo
222
normal! zo
222
normal! zo
222
normal! zo
222
normal! zo
222
normal! zo
222
normal! zo
222
normal! zo
230
normal! zo
240
normal! zo
241
normal! zo
247
normal! zo
248
normal! zo
250
normal! zo
253
normal! zo
256
normal! zo
259
normal! zo
262
normal! zo
262
normal! zo
266
normal! zo
266
normal! zo
274
normal! zo
278
normal! zo
282
normal! zo
286
normal! zo
290
normal! zo
295
normal! zo
302
normal! zo
313
normal! zo
314
normal! zo
let s:l = 37 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
37
normal! 032|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/api/murano/extra.py
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
let s:l = 56 - ((2 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
56
normal! 071|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/api/murano/ops.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
37
normal! zo
37
normal! zo
622
normal! zo
683
normal! zo
759
normal! zo
796
normal! zo
796
normal! zo
796
normal! zo
796
normal! zo
796
normal! zo
796
normal! zo
796
normal! zo
796
normal! zo
796
normal! zo
796
normal! zo
815
normal! zo
867
normal! zo
923
normal! zo
1140
normal! zo
1225
normal! zo
1271
normal! zo
1282
normal! zo
1282
normal! zo
1282
normal! zo
1283
normal! zo
let s:l = 182 - ((1 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
182
normal! 016|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/api/murano/connection.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
19
normal! zo
20
normal! zo
24
normal! zo
30
normal! zo
36
normal! zo
36
normal! zo
46
normal! zo
49
normal! zo
52
normal! zo
56
normal! zo
57
normal! zo
57
normal! zo
58
normal! zo
63
normal! zo
64
normal! zo
64
normal! zo
64
normal! zo
64
normal! zo
66
normal! zo
67
normal! zo
67
normal! zo
67
normal! zo
67
normal! zo
78
normal! zo
88
normal! zo
97
normal! zo
100
normal! zo
107
normal! zo
108
normal! zo
109
normal! zo
115
normal! zo
125
normal! zo
135
normal! zo
let s:l = 106 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
106
normal! 040|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/api/murano/__init__.py
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
let s:l = 52 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
52
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/api/murano/export.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
24
normal! zo
171
normal! zo
177
normal! zo
309
normal! zo
315
normal! zo
348
normal! zo
370
normal! zo
372
normal! zo
395
normal! zo
408
normal! zo
424
normal! zo
425
normal! zo
446
normal! zo
447
normal! zo
492
normal! zo
499
normal! zo
522
normal! zo
537
normal! zo
543
normal! zo
543
normal! zo
543
normal! zo
559
normal! zo
565
normal! zo
567
normal! zo
578
normal! zo
597
normal! zo
599
normal! zo
599
normal! zo
599
normal! zo
599
normal! zo
599
normal! zo
599
normal! zo
604
normal! zo
619
normal! zo
625
normal! zo
634
normal! zo
646
normal! zo
655
normal! zo
664
normal! zo
700
normal! zo
722
normal! zo
let s:l = 315 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
315
normal! 031|
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
733
normal! zo
802
normal! zo
2845
normal! zo
2869
normal! zo
2939
normal! zo
3117
normal! zo
3132
normal! zo
3133
normal! zo
3139
normal! zo
3140
normal! zo
5503
normal! zo
5989
normal! zo
6187
normal! zo
6326
normal! zo
6497
normal! zo
7784
normal! zo
7802
normal! zo
7807
normal! zo
7809
normal! zo
7810
normal! zo
7851
normal! zo
8663
normal! zo
8666
normal! zo
8903
normal! zo
8912
normal! zo
9380
normal! zo
10093
normal! zo
10109
normal! zo
10125
normal! zo
10191
normal! zo
10221
normal! zo
10237
normal! zo
10254
normal! zo
10254
normal! zo
10254
normal! zo
10254
normal! zo
10254
normal! zo
10254
normal! zo
10254
normal! zo
10254
normal! zo
10254
normal! zo
10261
normal! zo
10268
normal! zo
10272
normal! zo
10273
normal! zo
10273
normal! zo
10275
normal! zo
10276
normal! zo
10276
normal! zo
10278
normal! zo
10279
normal! zo
10279
normal! zo
10281
normal! zo
10282
normal! zo
10282
normal! zo
10284
normal! zo
10285
normal! zo
10285
normal! zo
10287
normal! zo
10290
normal! zo
10292
normal! zo
10292
normal! zo
10292
normal! zo
10314
normal! zo
10317
normal! zo
10318
normal! zo
10318
normal! zo
10321
normal! zo
10321
normal! zo
10321
normal! zo
10324
normal! zo
10324
normal! zo
10324
normal! zo
10324
normal! zo
10330
normal! zo
10333
normal! zo
10337
normal! zo
10344
normal! zo
10346
normal! zo
10378
normal! zo
10491
normal! zo
10500
normal! zo
10505
normal! zo
10507
normal! zo
10512
normal! zo
10518
normal! zo
10526
normal! zo
10527
normal! zo
10527
normal! zo
10527
normal! zo
10527
normal! zo
10541
normal! zo
10542
normal! zo
10547
normal! zo
10581
normal! zo
10588
normal! zo
10591
normal! zo
10596
normal! zo
10601
normal! zo
10714
normal! zo
10741
normal! zo
10746
normal! zo
10752
normal! zo
10782
normal! zo
10795
normal! zo
10894
normal! zo
10894
normal! zo
10894
normal! zo
10894
normal! zo
10894
normal! zo
11021
normal! zo
11027
normal! zo
11037
normal! zo
11040
normal! zo
11043
normal! zo
11043
normal! zo
11043
normal! zo
11046
normal! zo
11046
normal! zo
11046
normal! zo
11046
normal! zo
11051
normal! zo
11051
normal! zo
11051
normal! zo
11054
normal! zo
11054
normal! zo
11054
normal! zo
11059
normal! zo
11059
normal! zo
11059
normal! zo
11064
normal! zo
11077
normal! zo
11080
normal! zo
11083
normal! zo
11086
normal! zo
11093
normal! zo
11100
normal! zo
11103
normal! zo
11105
normal! zo
11108
normal! zo
11111
normal! zo
11127
normal! zo
11134
normal! zo
11138
normal! zo
11139
normal! zo
11139
normal! zo
11141
normal! zo
11142
normal! zo
11142
normal! zo
11144
normal! zo
11145
normal! zo
11145
normal! zo
11147
normal! zo
11148
normal! zo
11148
normal! zo
11150
normal! zo
11151
normal! zo
11151
normal! zo
11153
normal! zo
11154
normal! zo
11154
normal! zo
11156
normal! zo
11157
normal! zo
11157
normal! zo
11159
normal! zo
11162
normal! zo
11164
normal! zo
11164
normal! zo
11164
normal! zo
11170
normal! zo
11171
normal! zo
11171
normal! zo
11173
normal! zo
11174
normal! zo
11174
normal! zo
11176
normal! zo
11177
normal! zo
11177
normal! zo
11179
normal! zo
11180
normal! zo
11180
normal! zo
11182
normal! zo
11183
normal! zo
11183
normal! zo
11208
normal! zo
11212
normal! zo
11215
normal! zo
11216
normal! zo
11216
normal! zo
11216
normal! zo
11216
normal! zo
11216
normal! zo
11216
normal! zo
11221
normal! zo
11222
normal! zo
11222
normal! zo
11222
normal! zo
11225
normal! zo
11373
normal! zo
11449
normal! zo
11457
normal! zo
11464
normal! zo
11464
normal! zo
11464
normal! zo
11464
normal! zo
11464
normal! zo
11464
normal! zo
11464
normal! zo
11475
normal! zo
11479
normal! zo
11480
normal! zo
11480
normal! zo
11480
normal! zo
11490
normal! zo
11493
normal! zo
11500
normal! zo
11509
normal! zo
11518
normal! zo
11548
normal! zo
11555
normal! zo
11559
normal! zo
11562
normal! zo
11628
normal! zo
11642
normal! zo
11642
normal! zo
11642
normal! zo
11642
normal! zo
11654
normal! zo
11667
normal! zo
11680
normal! zo
11687
normal! zo
11689
normal! zo
11689
normal! zo
11689
normal! zo
11689
normal! zo
11689
normal! zo
11689
normal! zo
11714
normal! zo
11742
normal! zo
11754
normal! zo
11755
normal! zo
11755
normal! zo
11755
normal! zo
11755
normal! zo
11948
normal! zo
11959
normal! zo
11976
normal! zo
11976
normal! zo
11980
normal! zo
11985
normal! zo
11985
normal! zo
11987
normal! zo
11988
normal! zo
11988
normal! zo
12015
normal! zo
12015
normal! zo
12015
normal! zo
12015
normal! zo
12015
normal! zo
12043
normal! zo
12044
normal! zo
12045
normal! zo
12046
normal! zo
12052
normal! zo
12078
normal! zo
12078
normal! zo
12078
normal! zo
12078
normal! zo
12078
normal! zo
12126
normal! zo
12144
normal! zo
12144
normal! zo
12144
normal! zo
12144
normal! zo
12144
normal! zo
12144
normal! zo
12144
normal! zo
12144
normal! zo
12144
normal! zo
12144
normal! zo
12165
normal! zo
12165
normal! zo
12165
normal! zo
12165
normal! zo
12165
normal! zo
12165
normal! zo
12206
normal! zo
12207
normal! zo
12545
normal! zo
12545
normal! zo
12545
normal! zo
12548
normal! zo
12552
normal! zo
12559
normal! zo
12596
normal! zo
12612
normal! zo
12630
normal! zo
12630
normal! zo
12630
normal! zo
12630
normal! zo
12631
normal! zo
12636
normal! zo
12652
normal! zo
12652
normal! zo
12652
normal! zo
12652
normal! zo
12877
normal! zo
12877
normal! zo
12877
normal! zo
12946
normal! zo
12947
normal! zo
13011
normal! zo
13011
normal! zo
13011
normal! zo
13011
normal! zo
13011
normal! zo
13011
normal! zo
13011
normal! zo
13044
normal! zo
13045
normal! zo
13048
normal! zo
13049
normal! zo
13050
normal! zo
13051
normal! zo
13054
normal! zo
13055
normal! zo
13062
normal! zo
13063
normal! zo
13072
normal! zo
13073
normal! zo
13073
normal! zo
13073
normal! zo
13073
normal! zo
13078
normal! zo
13078
normal! zo
13078
normal! zo
13078
normal! zo
13078
normal! zo
13079
normal! zo
13082
normal! zo
13091
normal! zo
13092
normal! zo
13105
normal! zo
13106
normal! zo
13112
normal! zo
13113
normal! zo
13131
normal! zo
13131
normal! zo
13131
normal! zo
13131
normal! zo
13131
normal! zo
13167
normal! zo
13168
normal! zo
13169
normal! zo
13170
normal! zo
13172
normal! zo
13172
normal! zo
13189
normal! zo
13190
normal! zo
13190
normal! zo
13190
normal! zo
13190
normal! zo
13190
normal! zo
13190
normal! zo
13190
normal! zo
13195
normal! zo
13196
normal! zo
13197
normal! zo
13198
normal! zo
13206
normal! zo
13207
normal! zo
13208
normal! zo
13215
normal! zo
13216
normal! zo
13217
normal! zo
13219
normal! zo
13219
normal! zo
13225
normal! zo
13227
normal! zo
13236
normal! zo
13236
normal! zo
13236
normal! zo
13236
normal! zo
13236
normal! zo
13246
normal! zo
13246
normal! zo
13246
normal! zo
13252
normal! zo
13264
normal! zo
13265
normal! zo
13266
normal! zo
13268
normal! zo
13268
normal! zo
13274
normal! zo
13276
normal! zo
13285
normal! zo
13285
normal! zo
13285
normal! zo
13285
normal! zo
13285
normal! zo
13295
normal! zo
13295
normal! zo
13295
normal! zo
13301
normal! zo
13310
normal! zo
13311
normal! zo
13312
normal! zo
13313
normal! zo
13321
normal! zo
13328
normal! zo
13330
normal! zo
13331
normal! zo
13350
normal! zo
13351
normal! zo
13352
normal! zo
13353
normal! zo
13361
normal! zo
13368
normal! zo
13370
normal! zo
13371
normal! zo
13429
normal! zo
13429
normal! zo
13429
normal! zo
13429
normal! zo
13429
normal! zo
13429
normal! zo
13429
normal! zo
13429
normal! zo
13444
normal! zo
13459
normal! zo
13461
normal! zo
13466
normal! zo
13471
normal! zo
13472
normal! zo
13472
normal! zo
13472
normal! zo
13483
normal! zo
13507
normal! zo
13507
normal! zo
13518
normal! zo
13523
normal! zo
13523
normal! zo
13525
normal! zo
13525
normal! zo
13525
normal! zo
13525
normal! zo
13525
normal! zo
13525
normal! zo
13527
normal! zo
13529
normal! zo
13529
normal! zo
13530
normal! zo
13530
normal! zo
13546
normal! zo
13547
normal! zo
13548
normal! zo
13550
normal! zo
13551
normal! zo
13551
normal! zo
13560
normal! zo
13564
normal! zo
13565
normal! zo
13565
normal! zo
13565
normal! zo
13565
normal! zo
13571
normal! zo
13608
normal! zo
13609
normal! zo
13610
normal! zo
13611
normal! zo
13613
normal! zo
13613
normal! zo
13619
normal! zo
13621
normal! zo
13621
normal! zo
13627
normal! zo
13628
normal! zo
13628
normal! zo
13630
normal! zo
13630
normal! zo
13630
normal! zo
13630
normal! zo
13669
normal! zo
13670
normal! zo
13679
normal! zo
13680
normal! zo
13681
normal! zo
13689
normal! zo
13690
normal! zo
13698
normal! zo
13699
normal! zo
13699
normal! zo
13701
normal! zo
13701
normal! zo
13701
normal! zo
13701
normal! zo
13701
normal! zo
13730
normal! zo
13731
normal! zo
13740
normal! zo
13741
normal! zo
13742
normal! zo
13750
normal! zo
13751
normal! zo
13759
normal! zo
13760
normal! zo
13760
normal! zo
13762
normal! zo
13762
normal! zo
13762
normal! zo
13762
normal! zo
13762
normal! zo
13788
normal! zo
13795
normal! zo
13796
normal! zo
13797
normal! zo
13798
normal! zo
13800
normal! zo
13800
normal! zo
13806
normal! zo
13808
normal! zo
13808
normal! zo
13814
normal! zo
13815
normal! zo
13815
normal! zo
13817
normal! zo
13817
normal! zo
13817
normal! zo
13817
normal! zo
13827
normal! zo
13851
normal! zo
13871
normal! zo
13872
normal! zo
13873
normal! zo
13874
normal! zo
13874
normal! zo
13875
normal! zo
13886
normal! zo
13887
normal! zo
13887
normal! zo
13887
normal! zo
13888
normal! zo
13894
normal! zo
13895
normal! zo
13896
normal! zo
13896
normal! zo
13897
normal! zo
13908
normal! zo
13909
normal! zo
13910
normal! zo
13910
normal! zo
13911
normal! zo
14098
normal! zo
14099
normal! zo
14100
normal! zo
14101
normal! zo
14101
normal! zo
14102
normal! zo
14114
normal! zo
14115
normal! zo
14115
normal! zo
14115
normal! zo
14122
normal! zo
14123
normal! zo
14124
normal! zo
14124
normal! zo
14125
normal! zo
14136
normal! zo
14137
normal! zo
14138
normal! zo
14138
normal! zo
14139
normal! zo
14341
normal! zo
14341
normal! zo
14341
normal! zo
14352
normal! zo
14357
normal! zo
14358
normal! zo
14359
normal! zo
14359
normal! zo
14359
normal! zo
14359
normal! zo
14359
normal! zo
14359
normal! zo
14359
normal! zo
14359
normal! zo
14359
normal! zo
14359
normal! zo
14365
normal! zo
14366
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14369
normal! zo
14371
normal! zo
14372
normal! zo
14372
normal! zo
14372
normal! zo
14372
normal! zo
14372
normal! zo
14372
normal! zo
14372
normal! zo
14372
normal! zo
14372
normal! zo
14375
normal! zo
14377
normal! zo
14382
normal! zo
14391
normal! zo
14392
normal! zo
14392
normal! zo
14392
normal! zo
14392
normal! zo
14392
normal! zo
14392
normal! zo
14392
normal! zo
14499
normal! zo
14499
normal! zo
14499
normal! zo
14499
normal! zo
14499
normal! zo
14499
normal! zo
14499
normal! zo
14499
normal! zo
14499
normal! zo
14509
normal! zo
14509
normal! zo
14509
normal! zo
14509
normal! zo
14509
normal! zo
14509
normal! zo
14511
normal! zo
14512
normal! zo
14512
normal! zo
14512
normal! zo
14538
normal! zo
14538
normal! zo
14538
normal! zo
14538
normal! zo
14546
normal! zo
14551
normal! zo
14554
normal! zo
14559
normal! zo
14560
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14561
normal! zo
14567
normal! zo
14568
normal! zo
14571
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14572
normal! zo
14574
normal! zo
14574
normal! zo
14574
normal! zo
14574
normal! zo
14574
normal! zo
14574
normal! zo
14574
normal! zo
14574
normal! zo
14574
normal! zo
14576
normal! zo
14577
normal! zo
14580
normal! zo
14580
normal! zo
14580
normal! zo
14580
normal! zo
14580
normal! zo
14580
normal! zo
14580
normal! zo
14580
normal! zo
14580
normal! zo
14583
normal! zo
14584
normal! zo
14588
normal! zo
14588
normal! zo
14593
normal! zo
14593
normal! zo
14598
normal! zo
14599
normal! zo
14606
normal! zo
14607
normal! zo
14610
normal! zo
14610
normal! zo
14610
normal! zo
14610
normal! zo
14610
normal! zo
14610
normal! zo
14695
normal! zo
14701
normal! zo
14701
normal! zo
14707
normal! zo
14707
normal! zo
14707
normal! zo
14707
normal! zo
14723
normal! zo
14728
normal! zo
14729
normal! zo
14730
normal! zo
14730
normal! zo
14730
normal! zo
14730
normal! zo
14730
normal! zo
14730
normal! zo
14730
normal! zo
14730
normal! zo
14730
normal! zo
14730
normal! zo
14736
normal! zo
14737
normal! zo
14738
normal! zo
14738
normal! zo
14738
normal! zo
14738
normal! zo
14738
normal! zo
14738
normal! zo
14738
normal! zo
14740
normal! zo
14740
normal! zo
14740
normal! zo
14740
normal! zo
14740
normal! zo
14740
normal! zo
14740
normal! zo
14740
normal! zo
14740
normal! zo
14742
normal! zo
14743
normal! zo
14743
normal! zo
14743
normal! zo
14743
normal! zo
14743
normal! zo
14743
normal! zo
14743
normal! zo
14743
normal! zo
14743
normal! zo
14746
normal! zo
14748
normal! zo
14748
normal! zo
14753
normal! zo
14753
normal! zo
14763
normal! zo
14764
normal! zo
14764
normal! zo
14764
normal! zo
14764
normal! zo
14764
normal! zo
14764
normal! zo
14817
normal! zo
14818
normal! zo
14818
normal! zo
14824
normal! zo
14824
normal! zo
14824
normal! zo
14824
normal! zo
14836
normal! zo
14841
normal! zo
14842
normal! zo
14843
normal! zo
14843
normal! zo
14843
normal! zo
14843
normal! zo
14843
normal! zo
14843
normal! zo
14843
normal! zo
14843
normal! zo
14843
normal! zo
14843
normal! zo
14849
normal! zo
14850
normal! zo
14851
normal! zo
14851
normal! zo
14851
normal! zo
14851
normal! zo
14851
normal! zo
14851
normal! zo
14851
normal! zo
14853
normal! zo
14853
normal! zo
14853
normal! zo
14853
normal! zo
14853
normal! zo
14853
normal! zo
14853
normal! zo
14853
normal! zo
14853
normal! zo
14855
normal! zo
14856
normal! zo
14856
normal! zo
14856
normal! zo
14856
normal! zo
14856
normal! zo
14856
normal! zo
14856
normal! zo
14856
normal! zo
14856
normal! zo
14859
normal! zo
14861
normal! zo
14861
normal! zo
14866
normal! zo
14866
normal! zo
14876
normal! zo
14877
normal! zo
14877
normal! zo
14877
normal! zo
14877
normal! zo
14877
normal! zo
14877
normal! zo
14945
normal! zo
14957
normal! zo
14958
normal! zo
14959
normal! zo
14961
normal! zo
14962
normal! zo
14963
normal! zo
14963
normal! zo
14963
normal! zo
14965
normal! zo
14966
normal! zo
14966
normal! zo
14966
normal! zo
16560
normal! zo
16609
normal! zo
16621
normal! zo
16639
normal! zo
16649
normal! zo
16654
normal! zo
16654
normal! zo
16654
normal! zo
16654
normal! zo
16654
normal! zo
16654
normal! zo
16654
normal! zo
16654
normal! zo
16654
normal! zo
16654
normal! zo
16654
normal! zo
16656
normal! zo
16656
normal! zo
16656
normal! zo
16660
normal! zo
16661
normal! zo
16669
normal! zo
17001
normal! zo
17017
normal! zo
17023
normal! zo
17026
normal! zo
17033
normal! zo
17033
normal! zo
17033
normal! zo
17155
normal! zo
17161
normal! zo
17164
normal! zo
17209
normal! zo
17216
normal! zo
17217
normal! zo
17226
normal! zo
17237
normal! zo
17237
normal! zo
17237
normal! zo
17244
normal! zo
17244
normal! zo
17244
normal! zo
17359
normal! zo
17364
normal! zo
17364
normal! zo
17364
normal! zo
17387
normal! zo
17388
normal! zo
17388
normal! zo
17388
normal! zo
17388
normal! zo
17388
normal! zo
17388
normal! zo
17388
normal! zo
17388
normal! zo
17388
normal! zo
17388
normal! zo
17388
normal! zo
17493
normal! zo
17503
normal! zo
17506
normal! zo
17512
normal! zo
17517
normal! zo
17522
normal! zo
17532
normal! zo
17533
normal! zo
17533
normal! zo
17533
normal! zo
17535
normal! zo
17535
normal! zo
17535
normal! zo
17535
normal! zo
17535
normal! zo
17535
normal! zo
17535
normal! zo
17535
normal! zo
17535
normal! zo
17535
normal! zo
17540
normal! zo
17541
normal! zo
17547
normal! zo
17548
normal! zo
17593
normal! zo
17597
normal! zo
17614
normal! zo
17625
normal! zo
17625
normal! zo
17625
normal! zo
17625
normal! zo
17627
normal! zo
17628
normal! zo
17629
normal! zo
17630
normal! zo
17631
normal! zo
17635
normal! zo
17636
normal! zo
17637
normal! zo
17637
normal! zo
17637
normal! zo
17637
normal! zo
17637
normal! zo
17637
normal! zo
17637
normal! zo
17639
normal! zo
17641
normal! zo
17646
normal! zo
17646
normal! zo
17646
normal! zo
17646
normal! zo
17652
normal! zo
17715
normal! zo
17724
normal! zo
17725
normal! zo
17725
normal! zo
17735
normal! zo
17794
normal! zo
17804
normal! zo
17818
normal! zo
17821
normal! zo
17825
normal! zo
17826
normal! zo
17827
normal! zo
17827
normal! zo
17827
normal! zo
17827
normal! zo
17827
normal! zo
17860
normal! zo
17867
normal! zo
17868
normal! zo
17869
normal! zo
17957
normal! zo
17971
normal! zo
17978
normal! zo
17979
normal! zo
18029
normal! zo
18050
normal! zo
18063
normal! zo
18063
normal! zo
18063
normal! zo
18063
normal! zo
18063
normal! zo
18063
normal! zo
18524
normal! zo
18594
normal! zo
18601
normal! zo
18602
normal! zo
18668
normal! zo
18688
normal! zo
18700
normal! zo
18700
normal! zo
18700
normal! zo
18700
normal! zo
18700
normal! zo
18736
normal! zo
18742
normal! zo
18825
normal! zo
18915
normal! zo
18926
normal! zo
18930
normal! zo
18935
normal! zo
18944
normal! zo
18945
normal! zo
18946
normal! zo
18948
normal! zo
18948
normal! zo
18948
normal! zo
18951
normal! zo
18953
normal! zo
18953
normal! zo
18953
normal! zo
18956
normal! zo
18957
normal! zo
18957
normal! zo
18957
normal! zo
18957
normal! zo
18957
normal! zo
19355
normal! zo
21448
normal! zo
21497
normal! zo
21497
normal! zo
21497
normal! zo
21497
normal! zo
21497
normal! zo
21497
normal! zo
21497
normal! zo
21497
normal! zo
21497
normal! zo
21508
normal! zo
21509
normal! zo
21585
normal! zo
21597
normal! zo
21598
normal! zo
21623
normal! zo
21623
normal! zo
21623
normal! zo
21623
normal! zo
21623
normal! zo
21623
normal! zo
21623
normal! zo
21641
normal! zo
21770
normal! zo
21774
normal! zo
21893
normal! zo
21894
normal! zo
21898
normal! zo
21899
normal! zo
21903
normal! zo
21904
normal! zo
21908
normal! zo
21909
normal! zo
21913
normal! zo
21914
normal! zo
21918
normal! zo
let s:l = 12075 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
12075
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 23 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 87 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 87 + 55) / 111)
exe '4resize ' . ((&lines * 32 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 87 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 87 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 87 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 87 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 87 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 87 + 55) / 111)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=1 shortmess=aoO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
tabnext 1
4wincmd w

" vim: ft=vim ro nowrap smc=128
