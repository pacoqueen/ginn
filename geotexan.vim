" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 11 marzo 2016 at 15:19:46.
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
badd +172 ginn/formularios/partes_de_fabricacion_rollos.py
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
badd +636 ginn/formularios/pedidos_de_compra.py
badd +1451 ginn/formularios/presupuestos.py
badd +1316 ginn/formularios/facturas_compra.py
badd +6003 ginn/framework/pclases/__init__.py
badd +37 ginn/api/murano/connection.py
badd +1 ginn/api/murano/__init__.py
badd +175 ginn/formularios/mail_sender.py
badd +42 ginn/informes/presupuesto2.py
badd +1 ginn/lib/xlutils/jenkins
badd +1 ginn/api/tests/murano_tests.py
badd +1 ginn/api/murano/ops.py
badd +102 ginn/formularios/utils_almacen.py
badd +1 ginn/api/murano/export.py
badd +0 ginn/formularios/partes_de_fabricacion_balas.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=47 columns=120
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
6wincmd k
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
exe 'vert 1resize ' . ((&columns * 26 + 60) / 120)
exe '2resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 2resize ' . ((&columns * 93 + 60) / 120)
exe '3resize ' . ((&lines * 33 + 23) / 47)
exe 'vert 3resize ' . ((&columns * 93 + 60) / 120)
exe '4resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 4resize ' . ((&columns * 93 + 60) / 120)
exe '5resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 5resize ' . ((&columns * 93 + 60) / 120)
exe '6resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 6resize ' . ((&columns * 93 + 60) / 120)
exe '7resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 7resize ' . ((&columns * 93 + 60) / 120)
exe '8resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 8resize ' . ((&columns * 93 + 60) / 120)
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
296
normal! zo
296
normal! zo
302
normal! zo
313
normal! zo
314
normal! zo
let s:l = 296 - ((2 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
296
normal! 027|
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
35
normal! zo
35
normal! zo
120
normal! zo
120
normal! zo
120
normal! zo
150
normal! zo
165
normal! zo
183
normal! zo
194
normal! zo
195
normal! zo
205
normal! zo
232
normal! zo
247
normal! zo
248
normal! zo
258
normal! zo
259
normal! zo
268
normal! zo
275
normal! zo
276
normal! zo
286
normal! zo
299
normal! zo
302
normal! zo
304
normal! zo
305
normal! zo
313
normal! zo
314
normal! zo
314
normal! zo
315
normal! zo
315
normal! zo
315
normal! zo
315
normal! zo
315
normal! zo
315
normal! zo
323
normal! zo
331
normal! zo
336
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
338
normal! zo
338
normal! zo
338
normal! zo
343
normal! zo
344
normal! zo
344
normal! zo
344
normal! zo
344
normal! zo
345
normal! zo
353
normal! zo
369
normal! zo
369
normal! zo
374
normal! zo
382
normal! zo
383
normal! zo
383
normal! zo
383
normal! zo
389
normal! zo
401
normal! zo
402
normal! zo
402
normal! zo
402
normal! zo
405
normal! zo
415
normal! zo
415
normal! zo
422
normal! zo
432
normal! zo
433
normal! zo
433
normal! zo
433
normal! zo
439
normal! zo
451
normal! zo
452
normal! zo
452
normal! zo
452
normal! zo
452
normal! zo
453
normal! zo
457
normal! zo
465
normal! zo
474
normal! zo
475
normal! zo
483
normal! zo
486
normal! zo
490
normal! zo
491
normal! zo
491
normal! zo
491
normal! zo
495
normal! zo
506
normal! zo
519
normal! zo
534
normal! zo
543
normal! zo
549
normal! zo
556
normal! zo
560
normal! zo
566
normal! zo
573
normal! zo
580
normal! zo
580
normal! zo
583
normal! zo
583
normal! zo
583
normal! zo
583
normal! zo
583
normal! zo
583
normal! zo
593
normal! zo
607
normal! zo
612
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
613
normal! zo
619
normal! zo
685
normal! zo
690
normal! zo
699
normal! zo
707
normal! zo
736
normal! zo
737
normal! zo
743
normal! zo
760
normal! zo
760
normal! zo
763
normal! zo
766
normal! zo
766
normal! zo
766
normal! zo
766
normal! zo
789
normal! zo
789
normal! zo
789
normal! zo
789
normal! zo
789
normal! zo
789
normal! zo
802
normal! zo
815
normal! zo
815
normal! zo
821
normal! zo
821
normal! zo
821
normal! zo
821
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
838
normal! zo
851
normal! zo
867
normal! zo
867
normal! zo
873
normal! zo
873
normal! zo
873
normal! zo
873
normal! zo
893
normal! zo
893
normal! zo
893
normal! zo
893
normal! zo
893
normal! zo
893
normal! zo
907
normal! zo
920
normal! zo
920
normal! zo
926
normal! zo
926
normal! zo
926
normal! zo
926
normal! zo
943
normal! zo
943
normal! zo
943
normal! zo
943
normal! zo
943
normal! zo
943
normal! zo
957
normal! zo
981
normal! zo
1003
normal! zo
1024
normal! zo
1034
normal! zo
1048
normal! zo
1068
normal! zo
1080
normal! zo
1096
normal! zo
1109
normal! zo
1121
normal! zo
1165
normal! zo
1165
normal! zo
1165
normal! zo
1165
normal! zo
1184
normal! zo
1192
normal! zo
1206
normal! zo
1217
normal! zo
1217
normal! zo
1217
normal! zo
1217
normal! zo
1230
normal! zo
1230
normal! zo
1230
normal! zo
1230
normal! zo
1230
normal! zo
1230
normal! zo
1242
normal! zo
1243
normal! zo
1243
normal! zo
let s:l = 663 - ((13 * winheight(0) + 16) / 33)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
663
normal! 0219|
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
let s:l = 113 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
113
normal! 045|
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
111
normal! zo
112
normal! zo
126
normal! zo
126
normal! zo
312
normal! zo
339
normal! zo
339
normal! zo
503
normal! zo
522
normal! zo
725
normal! zo
1131
normal! zo
1315
normal! zo
1327
normal! zo
1328
normal! zo
1328
normal! zo
1328
normal! zo
1328
normal! zo
1342
normal! zo
2164
normal! zo
2174
normal! zo
2179
normal! zo
2180
normal! zo
2180
normal! zo
2180
normal! zo
3373
normal! zo
3386
normal! zo
3911
normal! zo
3935
normal! zo
3945
normal! zo
3946
normal! zo
3946
normal! zo
3946
normal! zo
3949
normal! zo
3954
normal! zo
3963
normal! zo
4111
normal! zo
4135
normal! zo
4145
normal! zo
4158
normal! zo
let s:l = 4162 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4162
normal! 039|
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
3969
normal! zo
4224
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
9488
normal! zo
10093
normal! zo
10109
normal! zo
10125
normal! zo
10191
normal! zo
10684
normal! zo
10775
normal! zo
11343
normal! zo
11598
normal! zo
12515
normal! zo
12515
normal! zo
12515
normal! zo
13101
normal! zo
13101
normal! zo
13101
normal! zo
13101
normal! zo
13101
normal! zo
13137
normal! zo
13841
normal! zo
13878
normal! zo
13879
normal! zo
13880
normal! zo
13880
normal! zo
13881
normal! zo
14013
normal! zo
14013
normal! zo
14013
normal! zo
14019
normal! zo
16530
normal! zo
16619
normal! zo
16971
normal! zo
17028
normal! zo
17737
normal! zo
17757
normal! zo
17758
normal! zo
17758
normal! zo
17758
normal! zo
17758
normal! zo
17758
normal! zo
17954
normal! zo
18494
normal! zo
18551
normal! zo
18638
normal! zo
18795
normal! zo
18826
normal! zo
18833
normal! zo
18833
normal! zo
18833
normal! zo
18833
normal! zo
18833
normal! zo
18842
normal! zo
19335
normal! zo
19349
normal! zo
21418
normal! zo
21487
normal! zo
21487
normal! zo
21487
normal! zo
21487
normal! zo
21487
normal! zo
21487
normal! zo
21487
normal! zo
21487
normal! zo
21740
normal! zo
21747
normal! zo
21749
normal! zo
let s:l = 4584 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4584
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 26 + 60) / 120)
exe '2resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 2resize ' . ((&columns * 93 + 60) / 120)
exe '3resize ' . ((&lines * 33 + 23) / 47)
exe 'vert 3resize ' . ((&columns * 93 + 60) / 120)
exe '4resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 4resize ' . ((&columns * 93 + 60) / 120)
exe '5resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 5resize ' . ((&columns * 93 + 60) / 120)
exe '6resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 6resize ' . ((&columns * 93 + 60) / 120)
exe '7resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 7resize ' . ((&columns * 93 + 60) / 120)
exe '8resize ' . ((&lines * 1 + 23) / 47)
exe 'vert 8resize ' . ((&columns * 93 + 60) / 120)
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
3wincmd w

" vim: ft=vim ro nowrap smc=128
