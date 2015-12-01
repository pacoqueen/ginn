" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 27 noviembre 2015 at 15:10:36.
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
badd +99 ginn/api/murano/ops.py
badd +175 ginn/formularios/mail_sender.py
badd +42 ginn/informes/presupuesto2.py
badd +1 ginn/lib/xlutils/jenkins
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=50 columns=108
edit ginn/api/murano/ops.py
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
3wincmd k
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 23 + 54) / 108)
exe '2resize ' . ((&lines * 12 + 25) / 50)
exe 'vert 2resize ' . ((&columns * 84 + 54) / 108)
exe '3resize ' . ((&lines * 11 + 25) / 50)
exe 'vert 3resize ' . ((&columns * 84 + 54) / 108)
exe '4resize ' . ((&lines * 11 + 25) / 50)
exe 'vert 4resize ' . ((&columns * 84 + 54) / 108)
exe '5resize ' . ((&lines * 11 + 25) / 50)
exe 'vert 5resize ' . ((&columns * 84 + 54) / 108)
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
17
normal! zo
102
normal! zo
102
normal! zo
102
normal! zo
164
normal! zo
170
normal! zo
170
normal! zo
170
normal! zo
170
normal! zo
176
normal! zo
183
normal! zo
195
normal! zo
199
normal! zo
212
normal! zo
218
normal! zo
232
normal! zo
261
normal! zo
261
normal! zo
261
normal! zo
261
normal! zo
272
normal! zo
272
normal! zo
272
normal! zo
272
normal! zo
272
normal! zo
272
normal! zo
351
normal! zo
362
normal! zo
362
normal! zo
362
normal! zo
362
normal! zo
373
normal! zo
373
normal! zo
373
normal! zo
373
normal! zo
let s:l = 372 - ((8 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
372
normal! 054|
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
10
normal! zo
11
normal! zo
16
normal! zo
22
normal! zo
28
normal! zo
28
normal! zo
39
normal! zo
43
normal! zo
44
normal! zo
44
normal! zo
45
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
52
normal! zo
52
normal! zo
52
normal! zo
52
normal! zo
53
normal! zo
54
normal! zo
54
normal! zo
54
normal! zo
54
normal! zo
71
normal! zo
79
normal! zo
82
normal! zo
85
normal! zo
86
normal! zo
92
normal! zo
83
normal! zo
83
normal! zo
83
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
85
normal! zo
86
normal! zo
92
normal! zo
let s:l = 70 - ((1 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
70
normal! 09|
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
let s:l = 42 - ((3 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
42
normal! 03|
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
19324
normal! zo
19331
normal! zo
let s:l = 1 - ((0 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 23 + 54) / 108)
exe '2resize ' . ((&lines * 12 + 25) / 50)
exe 'vert 2resize ' . ((&columns * 84 + 54) / 108)
exe '3resize ' . ((&lines * 11 + 25) / 50)
exe 'vert 3resize ' . ((&columns * 84 + 54) / 108)
exe '4resize ' . ((&lines * 11 + 25) / 50)
exe 'vert 4resize ' . ((&columns * 84 + 54) / 108)
exe '5resize ' . ((&lines * 11 + 25) / 50)
exe 'vert 5resize ' . ((&columns * 84 + 54) / 108)
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
2wincmd w

" vim: ft=vim ro nowrap smc=128
