" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 09 febrero 2016 at 18:02:36.
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
badd +1 db/tablas.sql
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
badd +12 ginn/api/tests/murano_tests.py
badd +1 ginn/api/murano/ops.py
badd +102 ginn/formularios/utils_almacen.py
badd +1 ginn/informes/norma2013.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=46 columns=103
edit db/tablas.sql
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
5wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 22 + 51) / 103)
exe '2resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 103)
exe '3resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 103)
exe '4resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 103)
exe '5resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 103)
exe '6resize ' . ((&lines * 34 + 23) / 46)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 103)
exe '7resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 103)
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
444
normal! zo
let s:l = 450 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
450
normal! 05|
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
177
normal! zo
314
normal! zo
319
normal! zo
320
normal! zo
320
normal! zo
320
normal! zo
320
normal! zo
320
normal! zo
320
normal! zo
361
normal! zo
586
normal! zo
733
normal! zo
762
normal! zo
762
normal! zo
762
normal! zo
762
normal! zo
let s:l = 737 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
737
normal! 028|
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
let s:l = 36 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
36
normal! 029|
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
49
normal! zo
let s:l = 50 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
50
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
21416
normal! zo
21485
normal! zo
21496
normal! zo
21497
normal! zo
21520
normal! zo
21553
normal! zo
21616
normal! zo
21738
normal! zo
21745
normal! zo
21747
normal! zo
21751
normal! zo
21752
normal! zo
let s:l = 821 - ((33 * winheight(0) + 17) / 34)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
821
normal! 09|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/informes/norma2013.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
21
normal! zo
47
normal! zo
47
normal! zo
216
normal! zo
let s:l = 55 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
55
normal! 038|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 22 + 51) / 103)
exe '2resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 103)
exe '3resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 103)
exe '4resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 103)
exe '5resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 103)
exe '6resize ' . ((&lines * 34 + 23) / 46)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 103)
exe '7resize ' . ((&lines * 1 + 23) / 46)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 103)
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
