" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 28 abril 2015 at 17:45:12.
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
badd +108 ginn/formularios/consulta_saldo_proveedores.py
badd +1 db/tablas.sql
badd +367 ginn/formularios/productos_compra.py
badd +54 ginn/formularios/partes_de_visita.py
badd +902 ginn/formularios/productos_de_venta_rollos.py
badd +357 ginn/formularios/proveedores.py
badd +79 ginn/framework/pclases/cliente.py
badd +6 ginn/formularios/clientes.py
badd +914 ginn/formularios/ventana.py
badd +0 ginn/informes/norma2013.py
badd +0 ginn/formularios/presupuestos.py
badd +0 ginn/formularios/custom_widgets/cellrendererautocomplete.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=54 columns=92
edit ginn/framework/pclases/__init__.py
set splitbelow splitright
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
exe '1resize ' . ((&lines * 11 + 27) / 54)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe '3resize ' . ((&lines * 1 + 27) / 54)
exe '4resize ' . ((&lines * 1 + 27) / 54)
exe '5resize ' . ((&lines * 1 + 27) / 54)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe '7resize ' . ((&lines * 27 + 27) / 54)
exe '8resize ' . ((&lines * 2 + 27) / 54)
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
let s:l = 11245 - ((3 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
11245
normal! 011|
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
let s:l = 3379 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3379
normal! 02|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/custom_widgets/cellrendererautocomplete.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
9
normal! zo
24
normal! zo
32
normal! zo
32
normal! zo
32
normal! zo
32
normal! zo
32
normal! zo
32
normal! zo
32
normal! zo
38
normal! zo
let s:l = 21 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
21
normal! 020|
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
508
normal! zo
4389
normal! zo
4389
normal! zo
4389
normal! zo
4389
normal! zo
4422
normal! zo
4422
normal! zo
4422
normal! zo
4433
normal! zo
4438
normal! zo
4439
normal! zo
4441
normal! zo
4446
normal! zo
4453
normal! zo
4466
normal! zo
4486
normal! zo
4486
normal! zo
4486
normal! zo
4486
normal! zo
4486
normal! zo
4486
normal! zo
4595
normal! zo
let s:l = 4486 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4486
normal! 050|
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
79
normal! zo
149
normal! zo
150
normal! zo
187
normal! zo
243
normal! zo
269
normal! zo
301
normal! zo
let s:l = 150 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
150
normal! 013|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/presupuestos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
77
normal! zo
1416
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
1492
normal! zo
let s:l = 1815 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1815
normal! 0
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
59
normal! zo
60
normal! zo
68
normal! zo
68
normal! zo
68
normal! zo
77
normal! zo
77
normal! zo
77
normal! zo
77
normal! zo
77
normal! zo
79
normal! zo
79
normal! zo
79
normal! zo
79
normal! zo
79
normal! zo
81
normal! zo
81
normal! zo
81
normal! zo
81
normal! zo
81
normal! zo
93
normal! zo
94
normal! zo
100
normal! zo
101
normal! zo
102
normal! zo
107
normal! zo
108
normal! zo
114
normal! zo
141
normal! zo
147
normal! zo
171
normal! zo
179
normal! zo
180
normal! zo
180
normal! zo
180
normal! zo
180
normal! zo
180
normal! zo
180
normal! zo
180
normal! zo
180
normal! zo
184
normal! zo
193
normal! zo
194
normal! zo
194
normal! zo
194
normal! zo
194
normal! zo
195
normal! zo
198
normal! zo
199
normal! zo
199
normal! zo
199
normal! zo
199
normal! zo
200
normal! zo
217
normal! zo
221
normal! zo
225
normal! zo
226
normal! zo
233
normal! zo
233
normal! zo
233
normal! zo
244
normal! zo
251
normal! zo
251
normal! zo
265
normal! zo
275
normal! zo
275
normal! zo
275
normal! zo
275
normal! zo
275
normal! zo
275
normal! zo
275
normal! zo
279
normal! zo
279
normal! zo
279
normal! zo
279
normal! zo
279
normal! zo
290
normal! zo
290
normal! zo
290
normal! zo
290
normal! zo
300
normal! zo
300
normal! zo
300
normal! zo
300
normal! zo
300
normal! zo
300
normal! zo
302
normal! zo
317
normal! zo
318
normal! zo
321
normal! zo
321
normal! zo
321
normal! zo
321
normal! zo
326
normal! zo
341
normal! zo
352
normal! zo
362
normal! zo
382
normal! zo
391
normal! zo
394
normal! zo
409
normal! zo
416
normal! zo
421
normal! zo
424
normal! zo
435
normal! zo
436
normal! zo
446
normal! zo
453
normal! zo
453
normal! zo
453
normal! zo
453
normal! zo
453
normal! zo
468
normal! zo
474
normal! zo
476
normal! zo
477
normal! zo
480
normal! zo
490
normal! zo
496
normal! zo
496
normal! zo
496
normal! zo
496
normal! zo
496
normal! zo
500
normal! zo
503
normal! zo
503
normal! zo
519
normal! zo
let s:l = 338 - ((16 * winheight(0) + 13) / 27)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
338
normal! 036|
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
let s:l = 4 - ((0 * winheight(0) + 1) / 2)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4
normal! 03|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
7wincmd w
exe '1resize ' . ((&lines * 11 + 27) / 54)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe '3resize ' . ((&lines * 1 + 27) / 54)
exe '4resize ' . ((&lines * 1 + 27) / 54)
exe '5resize ' . ((&lines * 1 + 27) / 54)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe '7resize ' . ((&lines * 27 + 27) / 54)
exe '8resize ' . ((&lines * 2 + 27) / 54)
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
7wincmd w

" vim: ft=vim ro nowrap smc=128
