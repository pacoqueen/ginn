" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 02 marzo 2016 at 18:30:48.
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
badd +4159 ginn/formularios/partes_de_fabricacion_balas.py
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
badd +0 ginn/formularios/partes_de_fabricacion_bolsas.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=54 columns=115
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
exe '2resize ' . ((&lines * 13 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 84 + 57) / 115)
exe '3resize ' . ((&lines * 28 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 84 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 84 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 84 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 84 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 84 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 27) / 54)
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
17
normal! zo
26
normal! zo
35
normal! zo
44
normal! zo
52
normal! zo
56
normal! zo
69
normal! zo
70
normal! zo
72
normal! zo
75
normal! zo
78
normal! zo
81
normal! zo
88
normal! zo
92
normal! zo
98
normal! zo
102
normal! zo
let s:l = 57 - ((5 * winheight(0) + 6) / 13)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
57
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
28
normal! zo
28
normal! zo
175
normal! zo
185
normal! zo
193
normal! zo
202
normal! zo
210
normal! zo
218
normal! zo
227
normal! zo
228
normal! zo
234
normal! zo
237
normal! zo
241
normal! zo
242
normal! zo
242
normal! zo
242
normal! zo
246
normal! zo
290
normal! zo
296
normal! zo
303
normal! zo
307
normal! zo
312
normal! zo
319
normal! zo
326
normal! zo
326
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
329
normal! zo
337
normal! zo
342
normal! zo
343
normal! zo
343
normal! zo
343
normal! zo
343
normal! zo
343
normal! zo
343
normal! zo
349
normal! zo
382
normal! zo
387
normal! zo
402
normal! zo
407
normal! zo
407
normal! zo
407
normal! zo
407
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
418
normal! zo
431
normal! zo
442
normal! zo
471
normal! zo
485
normal! zo
515
normal! zo
526
normal! zo
556
normal! zo
612
normal! zo
633
normal! zo
647
normal! zo
658
normal! zo
669
normal! zo
682
normal! zo
683
normal! zo
683
normal! zo
683
normal! zo
683
normal! zo
684
normal! zo
694
normal! zo
750
normal! zo
758
normal! zo
772
normal! zo
791
normal! zo
791
normal! zo
791
normal! zo
791
normal! zo
791
normal! zo
791
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
let s:l = 617 - ((19 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
617
normal! 0189|
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
17
normal! zo
18
normal! zo
22
normal! zo
28
normal! zo
34
normal! zo
34
normal! zo
44
normal! zo
47
normal! zo
50
normal! zo
54
normal! zo
55
normal! zo
55
normal! zo
56
normal! zo
61
normal! zo
62
normal! zo
62
normal! zo
62
normal! zo
62
normal! zo
64
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
65
normal! zo
76
normal! zo
86
normal! zo
95
normal! zo
98
normal! zo
104
normal! zo
105
normal! zo
106
normal! zo
107
normal! zo
112
normal! zo
122
normal! zo
132
normal! zo
let s:l = 140 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
140
normal! 017|
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
let s:l = 48 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
48
normal! 021|
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
467
normal! zo
474
normal! zo
497
normal! zo
512
normal! zo
518
normal! zo
518
normal! zo
518
normal! zo
534
normal! zo
540
normal! zo
542
normal! zo
553
normal! zo
572
normal! zo
574
normal! zo
574
normal! zo
574
normal! zo
574
normal! zo
574
normal! zo
574
normal! zo
579
normal! zo
594
normal! zo
600
normal! zo
609
normal! zo
621
normal! zo
630
normal! zo
639
normal! zo
675
normal! zo
697
normal! zo
let s:l = 566 - ((13 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
566
normal! 038|
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
let s:l = 652 - ((1 * winheight(0) + 0) / 1)
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
let s:l = 2889 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2889
normal! 018|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 57) / 115)
exe '2resize ' . ((&lines * 13 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 84 + 57) / 115)
exe '3resize ' . ((&lines * 28 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 84 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 84 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 84 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 84 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 84 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 27) / 54)
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
