" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 10 diciembre 2015 at 16:52:21.
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
if !exists('g:colors_name') || g:colors_name != 'vividchalk' | colorscheme vividchalk | endif
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
badd +4608 ginn/formularios/utils.py
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
badd +5011 ginn/informes/geninformes.py
badd +452 db/tablas.sql
badd +1 ginn/framework/__init__.py
badd +3136 ginn/formularios/facturas_venta.py
badd +10 ginn/informes/alians_trade.py
badd +52 ginn/informes/barcode/EANBarCode.py
badd +63 ginn/informes/barcode/_barcode.py
badd +227 ginn/informes/barcode/common.py
badd +53 ginn/informes/presupuesto.py
badd +1205 ginn/formularios/abonos_venta.py
badd +3507 ginn/formularios/albaranes_de_salida.py
badd +19 ginn/formularios/consulta_ofertas.py
badd +1134 ginn/formularios/pagares_pagos.py
badd +1272 ginn/formularios/pedidos_de_compra.py
badd +3667 ginn/formularios/presupuestos.py
badd +1316 ginn/formularios/facturas_compra.py
badd +20861 ginn/framework/pclases/__init__.py
badd +37 ginn/api/murano/connection.py
badd +1 ginn/api/murano/__init__.py
badd +1 ginn/api/murano/ops.py
badd +175 ginn/formularios/mail_sender.py
badd +42 ginn/informes/presupuesto2.py
badd +1 ginn/lib/xlutils/jenkins
badd +12 ginn/api/tests/murano_tests.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=48 columns=107
edit ginn/formularios/albaranes_de_salida.py
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
4wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 23 + 53) / 107)
exe '2resize ' . ((&lines * 19 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 83 + 53) / 107)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 83 + 53) / 107)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 83 + 53) / 107)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 83 + 53) / 107)
exe '6resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 83 + 53) / 107)
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
100
normal! zo
2064
normal! zo
2138
normal! zo
2155
normal! zo
2156
normal! zo
2157
normal! zo
2157
normal! zo
2158
normal! zo
2158
normal! zo
let s:l = 2139 - ((4 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2139
normal! 053|
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
23
normal! zo
23
normal! zo
108
normal! zo
108
normal! zo
108
normal! zo
170
normal! zo
180
normal! zo
188
normal! zo
197
normal! zo
205
normal! zo
211
normal! zo
213
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
221
normal! zo
227
normal! zo
234
normal! zo
243
normal! zo
254
normal! zo
269
normal! zo
278
normal! zo
284
normal! zo
291
normal! zo
295
normal! zo
300
normal! zo
307
normal! zo
312
normal! zo
313
normal! zo
313
normal! zo
313
normal! zo
313
normal! zo
313
normal! zo
313
normal! zo
319
normal! zo
349
normal! zo
354
normal! zo
369
normal! zo
374
normal! zo
374
normal! zo
374
normal! zo
374
normal! zo
385
normal! zo
385
normal! zo
385
normal! zo
385
normal! zo
385
normal! zo
385
normal! zo
398
normal! zo
409
normal! zo
414
normal! zo
414
normal! zo
414
normal! zo
414
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
425
normal! zo
438
normal! zo
452
normal! zo
457
normal! zo
457
normal! zo
457
normal! zo
457
normal! zo
468
normal! zo
468
normal! zo
468
normal! zo
468
normal! zo
468
normal! zo
468
normal! zo
482
normal! zo
493
normal! zo
498
normal! zo
498
normal! zo
498
normal! zo
498
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
523
normal! zo
536
normal! zo
558
normal! zo
591
normal! zo
600
normal! zo
619
normal! zo
620
normal! zo
620
normal! zo
620
normal! zo
630
normal! zo
667
normal! zo
667
normal! zo
667
normal! zo
667
normal! zo
685
normal! zo
693
normal! zo
699
normal! zo
702
normal! zo
703
normal! zo
703
normal! zo
703
normal! zo
707
normal! zo
712
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
718
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
let s:l = 218 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
218
normal! 012|
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
12
normal! zo
13
normal! zo
17
normal! zo
23
normal! zo
29
normal! zo
29
normal! zo
39
normal! zo
42
normal! zo
45
normal! zo
49
normal! zo
50
normal! zo
50
normal! zo
51
normal! zo
56
normal! zo
57
normal! zo
57
normal! zo
57
normal! zo
57
normal! zo
59
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
71
normal! zo
81
normal! zo
90
normal! zo
93
normal! zo
96
normal! zo
97
normal! zo
98
normal! zo
99
normal! zo
102
normal! zo
108
normal! zo
114
normal! zo
let s:l = 108 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
108
normal! 035|
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
let s:l = 46 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
46
normal! 071|
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
10684
normal! zo
10775
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
19336
normal! zo
19343
normal! zo
21582
normal! zo
21606
normal! zo
let s:l = 10726 - ((16 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10726
normal! 08|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 23 + 53) / 107)
exe '2resize ' . ((&lines * 19 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 83 + 53) / 107)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 83 + 53) / 107)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 83 + 53) / 107)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 83 + 53) / 107)
exe '6resize ' . ((&lines * 20 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 83 + 53) / 107)
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
6wincmd w

" vim: ft=vim ro nowrap smc=128
