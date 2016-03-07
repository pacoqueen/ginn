" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 07 marzo 2016 at 20:07:36.
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
badd +636 ginn/formularios/pedidos_de_compra.py
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
badd +1 ginn/formularios/partes_de_fabricacion_bolsas.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=53 columns=115
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
exe 'vert 1resize ' . ((&columns * 30 + 57) / 115)
exe '2resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 2resize ' . ((&columns * 84 + 57) / 115)
exe '3resize ' . ((&lines * 39 + 26) / 53)
exe 'vert 3resize ' . ((&columns * 84 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 4resize ' . ((&columns * 84 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 5resize ' . ((&columns * 84 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 6resize ' . ((&columns * 84 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 7resize ' . ((&columns * 84 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 8resize ' . ((&columns * 84 + 57) / 115)
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
22
normal! zo
41
normal! zo
50
normal! zo
51
normal! zo
51
normal! zo
51
normal! zo
51
normal! zo
51
normal! zo
51
normal! zo
51
normal! zo
55
normal! zo
66
normal! zo
75
normal! zo
76
normal! zo
76
normal! zo
76
normal! zo
76
normal! zo
76
normal! zo
76
normal! zo
76
normal! zo
84
normal! zo
93
normal! zo
94
normal! zo
98
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
99
normal! zo
105
normal! zo
106
normal! zo
115
normal! zo
120
normal! zo
121
normal! zo
144
normal! zo
145
normal! zo
145
normal! zo
145
normal! zo
145
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
150
normal! zo
167
normal! zo
168
normal! zo
170
normal! zo
173
normal! zo
176
normal! zo
179
normal! zo
182
normal! zo
182
normal! zo
190
normal! zo
194
normal! zo
198
normal! zo
202
normal! zo
let s:l = 209 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
209
normal! 010|
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
34
normal! zo
34
normal! zo
119
normal! zo
119
normal! zo
119
normal! zo
149
normal! zo
164
normal! zo
182
normal! zo
193
normal! zo
194
normal! zo
204
normal! zo
211
normal! zo
212
normal! zo
222
normal! zo
235
normal! zo
238
normal! zo
240
normal! zo
241
normal! zo
249
normal! zo
250
normal! zo
250
normal! zo
251
normal! zo
251
normal! zo
251
normal! zo
251
normal! zo
251
normal! zo
251
normal! zo
259
normal! zo
267
normal! zo
272
normal! zo
272
normal! zo
273
normal! zo
274
normal! zo
274
normal! zo
274
normal! zo
274
normal! zo
274
normal! zo
274
normal! zo
274
normal! zo
274
normal! zo
274
normal! zo
279
normal! zo
280
normal! zo
280
normal! zo
280
normal! zo
280
normal! zo
281
normal! zo
285
normal! zo
301
normal! zo
301
normal! zo
306
normal! zo
315
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
322
normal! zo
333
normal! zo
334
normal! zo
334
normal! zo
334
normal! zo
337
normal! zo
347
normal! zo
347
normal! zo
354
normal! zo
364
normal! zo
365
normal! zo
365
normal! zo
365
normal! zo
371
normal! zo
383
normal! zo
384
normal! zo
384
normal! zo
384
normal! zo
384
normal! zo
385
normal! zo
389
normal! zo
397
normal! zo
406
normal! zo
407
normal! zo
415
normal! zo
418
normal! zo
422
normal! zo
423
normal! zo
423
normal! zo
423
normal! zo
427
normal! zo
438
normal! zo
451
normal! zo
466
normal! zo
475
normal! zo
481
normal! zo
488
normal! zo
492
normal! zo
498
normal! zo
505
normal! zo
512
normal! zo
512
normal! zo
515
normal! zo
515
normal! zo
515
normal! zo
515
normal! zo
515
normal! zo
515
normal! zo
525
normal! zo
539
normal! zo
544
normal! zo
545
normal! zo
545
normal! zo
545
normal! zo
545
normal! zo
545
normal! zo
545
normal! zo
551
normal! zo
595
normal! zo
600
normal! zo
627
normal! zo
628
normal! zo
631
normal! zo
631
normal! zo
631
normal! zo
634
normal! zo
649
normal! zo
649
normal! zo
652
normal! zo
655
normal! zo
655
normal! zo
655
normal! zo
655
normal! zo
669
normal! zo
669
normal! zo
669
normal! zo
669
normal! zo
669
normal! zo
669
normal! zo
682
normal! zo
693
normal! zo
693
normal! zo
696
normal! zo
699
normal! zo
699
normal! zo
699
normal! zo
699
normal! zo
713
normal! zo
713
normal! zo
713
normal! zo
713
normal! zo
713
normal! zo
713
normal! zo
726
normal! zo
740
normal! zo
740
normal! zo
743
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
746
normal! zo
760
normal! zo
760
normal! zo
760
normal! zo
760
normal! zo
760
normal! zo
760
normal! zo
774
normal! zo
785
normal! zo
785
normal! zo
788
normal! zo
791
normal! zo
791
normal! zo
791
normal! zo
791
normal! zo
805
normal! zo
805
normal! zo
805
normal! zo
805
normal! zo
805
normal! zo
805
normal! zo
819
normal! zo
834
normal! zo
856
normal! zo
877
normal! zo
887
normal! zo
901
normal! zo
910
normal! zo
913
normal! zo
916
normal! zo
917
normal! zo
933
normal! zo
944
normal! zo
957
normal! zo
969
normal! zo
1009
normal! zo
1009
normal! zo
1009
normal! zo
1009
normal! zo
1028
normal! zo
1036
normal! zo
1042
normal! zo
1050
normal! zo
1069
normal! zo
1069
normal! zo
1069
normal! zo
1069
normal! zo
1069
normal! zo
1069
normal! zo
let s:l = 300 - ((1 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
300
normal! 0
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
106
normal! zo
107
normal! zo
108
normal! zo
109
normal! zo
114
normal! zo
124
normal! zo
134
normal! zo
let s:l = 72 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
72
normal! 030|
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
let s:l = 52 - ((1 * winheight(0) + 0) / 1)
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
let s:l = 315 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
315
normal! 031|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_bolsas.py
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
90
normal! zo
126
normal! zo
126
normal! zo
493
normal! zo
1662
normal! zo
1670
normal! zo
1680
normal! zo
1691
normal! zo
1728
normal! zo
1737
normal! zo
1795
normal! zo
1807
normal! zo
1825
normal! zo
1834
normal! zo
let s:l = 652 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
652
normal! 09|
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
let s:l = 8974 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
8974
normal! 09|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 57) / 115)
exe '2resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 2resize ' . ((&columns * 84 + 57) / 115)
exe '3resize ' . ((&lines * 39 + 26) / 53)
exe 'vert 3resize ' . ((&columns * 84 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 4resize ' . ((&columns * 84 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 5resize ' . ((&columns * 84 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 6resize ' . ((&columns * 84 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 7resize ' . ((&columns * 84 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 8resize ' . ((&columns * 84 + 57) / 115)
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
