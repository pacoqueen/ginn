" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 14 mayo 2015 at 18:42:47.
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
badd +1 ginn/formularios/partes_de_ancho_multiple.py
badd +1 ginn/framework/pclases/__init__.py
badd +1406 ginn/formularios/partes_de_fabricacion_balas.py
badd +1 ginn/formularios/facturas_compra.py
badd +1 fugitive:///home/bogado/Geotexan/src/Geotex-INN/.git//0/ginn/formularios/utils.py
badd +9 ginn/lib/fuzzywuzzy/fuzzywuzzy/utils.py
badd +1 formularios/auditviewer.py
badd +1247 ginn/formularios/utils.py
badd +38 ginn/informes/treeview2pdf.py
badd +138 ginn/formularios/listado_rollos.py
badd +2 ginn/lib/fuzzywuzzy/fuzzywuzzy/__init__.py
badd +1 ginn/formularios/consulta_ventas.py
badd +185 ginn/formularios/consulta_partes_de_visita.py
badd +1 db/tablas.sql
badd +367 ginn/formularios/productos_compra.py
badd +630 ginn/formularios/partes_de_visita.py
badd +902 ginn/formularios/productos_de_venta_rollos.py
badd +357 ginn/formularios/proveedores.py
badd +79 ginn/framework/pclases/cliente.py
badd +6 ginn/formularios/clientes.py
badd +914 ginn/formularios/ventana.py
badd +17 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +1 ginn/formularios/consulta_saldo_proveedores.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=54 columns=116
edit ginn/framework/pclases/__init__.py
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
exe 'vert 1resize ' . ((&columns * 29 + 58) / 116)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 86 + 58) / 116)
exe '3resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 86 + 58) / 116)
exe '4resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 86 + 58) / 116)
exe '5resize ' . ((&lines * 19 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 86 + 58) / 116)
exe '6resize ' . ((&lines * 22 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 86 + 58) / 116)
exe '7resize ' . ((&lines * 3 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 86 + 58) / 116)
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
301
normal! zo
11235
normal! zo
11245
normal! zo
15992
normal! zo
16005
normal! zo
16015
normal! zo
20827
normal! zo
let s:l = 20945 - ((4 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
20945
normal! 05|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/db/tablas.sql
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
1380
normal! zo
1434
normal! zo
3320
normal! zo
3497
normal! zo
3530
normal! zo
3533
normal! zo
3543
normal! zo
3549
normal! zo
3549
normal! zo
3549
normal! zo
3549
normal! zo
3549
normal! zo
let s:l = 3380 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3380
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/utils.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
507
normal! zo
507
normal! zo
507
normal! zo
1196
normal! zo
1214
normal! zo
1257
normal! zo
1271
normal! zo
1282
normal! zo
1287
normal! zo
1509
normal! zo
1537
normal! zo
1545
normal! zo
1557
normal! zo
4388
normal! zo
4388
normal! zo
4388
normal! zo
4388
normal! zo
4428
normal! zo
4428
normal! zo
4428
normal! zo
4439
normal! zo
4444
normal! zo
4445
normal! zo
4447
normal! zo
4452
normal! zo
4459
normal! zo
4472
normal! zo
4480
normal! zo
4482
normal! zo
4486
normal! zo
4487
normal! zo
4487
normal! zo
4487
normal! zo
4487
normal! zo
4487
normal! zo
4496
normal! zo
4507
normal! zo
4507
normal! zo
4507
normal! zo
4507
normal! zo
4507
normal! zo
4507
normal! zo
4616
normal! zo
let s:l = 4387 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4387
normal! 023|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_visita.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
60
normal! zo
61
normal! zo
212
normal! zo
220
normal! zo
222
normal! zo
262
normal! zo
286
normal! zo
290
normal! zo
290
normal! zo
290
normal! zo
290
normal! zo
290
normal! zo
295
normal! zo
296
normal! zo
300
normal! zo
304
normal! zo
314
normal! zo
321
normal! zo
321
normal! zo
337
normal! zo
377
normal! zo
377
normal! zo
377
normal! zo
377
normal! zo
377
normal! zo
377
normal! zo
510
normal! zo
522
normal! zo
537
normal! zo
546
normal! zo
551
normal! zo
565
normal! zo
566
normal! zo
577
normal! zo
584
normal! zo
584
normal! zo
584
normal! zo
584
normal! zo
584
normal! zo
599
normal! zo
632
normal! zo
651
normal! zo
655
normal! zo
let s:l = 649 - ((4 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
649
normal! 011|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_partes_de_visita.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
56
normal! zo
61
normal! zo
83
normal! zo
84
normal! zo
88
normal! zo
96
normal! zo
96
normal! zo
96
normal! zo
96
normal! zo
101
normal! zo
107
normal! zo
109
normal! zo
109
normal! zo
140
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
150
normal! zo
156
normal! zo
172
normal! zo
173
normal! zo
173
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
188
normal! zo
188
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
196
normal! zo
205
normal! zo
207
normal! zo
210
normal! zo
218
normal! zo
224
normal! zo
224
normal! zo
229
normal! zo
242
normal! zo
270
normal! zo
273
normal! zo
279
normal! zo
291
normal! zo
291
normal! zo
291
normal! zo
291
normal! zo
let s:l = 59 - ((13 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
59
normal! 07|
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
let s:l = 4 - ((0 * winheight(0) + 1) / 3)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4
normal! 03|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 29 + 58) / 116)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 86 + 58) / 116)
exe '3resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 86 + 58) / 116)
exe '4resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 86 + 58) / 116)
exe '5resize ' . ((&lines * 19 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 86 + 58) / 116)
exe '6resize ' . ((&lines * 22 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 86 + 58) / 116)
exe '7resize ' . ((&lines * 3 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 86 + 58) / 116)
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
