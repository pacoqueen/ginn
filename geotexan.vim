" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 14 marzo 2016 at 19:43:42.
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
badd +10 ginn/api/murano/extra.py
badd +1 ginn/api/murano/__init__.py
badd +175 ginn/formularios/mail_sender.py
badd +42 ginn/informes/presupuesto2.py
badd +1 ginn/lib/xlutils/jenkins
badd +1 ginn/api/tests/murano_tests.py
badd +1 ginn/api/murano/ops.py
badd +102 ginn/formularios/utils_almacen.py
badd +1 ginn/api/murano/export.py
badd +1 ginn/api/murano/connection.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=52 columns=112
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
exe 'vert 1resize ' . ((&columns * 26 + 56) / 112)
exe '2resize ' . ((&lines * 6 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 85 + 56) / 112)
exe '3resize ' . ((&lines * 33 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 85 + 56) / 112)
exe '4resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 85 + 56) / 112)
exe '5resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 85 + 56) / 112)
exe '6resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 85 + 56) / 112)
exe '7resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 7resize ' . ((&columns * 85 + 56) / 112)
exe '8resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 8resize ' . ((&columns * 85 + 56) / 112)
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
let s:l = 296 - ((0 * winheight(0) + 3) / 6)
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
37
normal! zo
37
normal! zo
122
normal! zo
122
normal! zo
122
normal! zo
152
normal! zo
167
normal! zo
185
normal! zo
196
normal! zo
197
normal! zo
207
normal! zo
234
normal! zo
249
normal! zo
250
normal! zo
260
normal! zo
261
normal! zo
270
normal! zo
277
normal! zo
278
normal! zo
288
normal! zo
301
normal! zo
304
normal! zo
306
normal! zo
307
normal! zo
315
normal! zo
316
normal! zo
316
normal! zo
317
normal! zo
317
normal! zo
317
normal! zo
317
normal! zo
317
normal! zo
317
normal! zo
325
normal! zo
333
normal! zo
338
normal! zo
339
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
340
normal! zo
345
normal! zo
346
normal! zo
346
normal! zo
346
normal! zo
346
normal! zo
347
normal! zo
355
normal! zo
371
normal! zo
371
normal! zo
376
normal! zo
384
normal! zo
385
normal! zo
385
normal! zo
385
normal! zo
391
normal! zo
404
normal! zo
405
normal! zo
405
normal! zo
405
normal! zo
408
normal! zo
418
normal! zo
418
normal! zo
425
normal! zo
435
normal! zo
436
normal! zo
436
normal! zo
436
normal! zo
442
normal! zo
454
normal! zo
455
normal! zo
455
normal! zo
455
normal! zo
455
normal! zo
456
normal! zo
460
normal! zo
468
normal! zo
477
normal! zo
478
normal! zo
486
normal! zo
489
normal! zo
493
normal! zo
494
normal! zo
494
normal! zo
494
normal! zo
498
normal! zo
509
normal! zo
522
normal! zo
537
normal! zo
546
normal! zo
552
normal! zo
559
normal! zo
563
normal! zo
569
normal! zo
576
normal! zo
583
normal! zo
583
normal! zo
586
normal! zo
586
normal! zo
586
normal! zo
586
normal! zo
586
normal! zo
586
normal! zo
596
normal! zo
610
normal! zo
615
normal! zo
616
normal! zo
616
normal! zo
616
normal! zo
616
normal! zo
616
normal! zo
616
normal! zo
622
normal! zo
678
normal! zo
686
normal! zo
706
normal! zo
715
normal! zo
723
normal! zo
752
normal! zo
753
normal! zo
759
normal! zo
776
normal! zo
776
normal! zo
779
normal! zo
782
normal! zo
782
normal! zo
782
normal! zo
782
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
815
normal! zo
828
normal! zo
828
normal! zo
834
normal! zo
834
normal! zo
834
normal! zo
834
normal! zo
853
normal! zo
853
normal! zo
853
normal! zo
853
normal! zo
853
normal! zo
853
normal! zo
867
normal! zo
883
normal! zo
883
normal! zo
889
normal! zo
889
normal! zo
889
normal! zo
889
normal! zo
909
normal! zo
909
normal! zo
909
normal! zo
909
normal! zo
909
normal! zo
909
normal! zo
923
normal! zo
936
normal! zo
936
normal! zo
942
normal! zo
942
normal! zo
942
normal! zo
942
normal! zo
961
normal! zo
961
normal! zo
961
normal! zo
961
normal! zo
961
normal! zo
961
normal! zo
976
normal! zo
1000
normal! zo
1022
normal! zo
1043
normal! zo
1053
normal! zo
1067
normal! zo
1087
normal! zo
1099
normal! zo
1115
normal! zo
1128
normal! zo
1140
normal! zo
1184
normal! zo
1184
normal! zo
1184
normal! zo
1184
normal! zo
1203
normal! zo
1211
normal! zo
1225
normal! zo
1236
normal! zo
1236
normal! zo
1236
normal! zo
1236
normal! zo
1249
normal! zo
1249
normal! zo
1249
normal! zo
1249
normal! zo
1249
normal! zo
1249
normal! zo
1261
normal! zo
1262
normal! zo
1262
normal! zo
1271
normal! zo
let s:l = 702 - ((21 * winheight(0) + 16) / 33)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
702
normal! 044|
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
61
normal! zo
74
normal! zo
85
normal! zo
96
normal! zo
101
normal! zo
102
normal! zo
102
normal! zo
102
normal! zo
106
normal! zo
let s:l = 28 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
28
normal! 062|
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
let s:l = 697 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
697
normal! 017|
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
5592
normal! zo
5603
normal! zo
5659
normal! zo
5817
normal! zo
5861
normal! zo
5989
normal! zo
6139
normal! zo
6170
normal! zo
6187
normal! zo
6326
normal! zo
6452
normal! zo
6467
normal! zo
6497
normal! zo
6621
normal! zo
6637
normal! zo
6668
normal! zo
6939
normal! zo
6947
normal! zo
7057
normal! zo
7226
normal! zo
7237
normal! zo
7238
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
9403
normal! zo
9426
normal! zo
9488
normal! zo
9762
normal! zo
9797
normal! zo
9815
normal! zo
9833
normal! zo
10093
normal! zo
10109
normal! zo
10125
normal! zo
10146
normal! zo
10155
normal! zo
10155
normal! zo
10155
normal! zo
10155
normal! zo
10191
normal! zo
10221
normal! zo
10609
normal! zo
10638
normal! zo
10646
normal! zo
10714
normal! zo
10805
normal! zo
11337
normal! zo
11373
normal! zo
11628
normal! zo
12545
normal! zo
12545
normal! zo
12545
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
13189
normal! zo
13190
normal! zo
13190
normal! zo
13871
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
14043
normal! zo
14043
normal! zo
14043
normal! zo
14049
normal! zo
16560
normal! zo
16649
normal! zo
17001
normal! zo
17058
normal! zo
17767
normal! zo
17787
normal! zo
17788
normal! zo
17788
normal! zo
17788
normal! zo
17788
normal! zo
17788
normal! zo
17984
normal! zo
18524
normal! zo
18581
normal! zo
18668
normal! zo
18825
normal! zo
18856
normal! zo
18863
normal! zo
18863
normal! zo
18863
normal! zo
18863
normal! zo
18863
normal! zo
18872
normal! zo
19365
normal! zo
19379
normal! zo
21448
normal! zo
21517
normal! zo
21517
normal! zo
21517
normal! zo
21517
normal! zo
21517
normal! zo
21517
normal! zo
21517
normal! zo
21517
normal! zo
21770
normal! zo
21777
normal! zo
21779
normal! zo
let s:l = 10132 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10132
normal! 044|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 26 + 56) / 112)
exe '2resize ' . ((&lines * 6 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 85 + 56) / 112)
exe '3resize ' . ((&lines * 33 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 85 + 56) / 112)
exe '4resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 85 + 56) / 112)
exe '5resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 85 + 56) / 112)
exe '6resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 85 + 56) / 112)
exe '7resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 7resize ' . ((&columns * 85 + 56) / 112)
exe '8resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 8resize ' . ((&columns * 85 + 56) / 112)
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
