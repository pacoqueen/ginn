" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 04 mayo 2015 at 12:46:16.
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
badd +1 ginn/formularios/presupuestos.py
badd +1 ginn/formularios/custom_widgets/cellrendererautocomplete.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=48 columns=117
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
exe 'vert 1resize ' . ((&columns * 30 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 86 + 58) / 117)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 86 + 58) / 117)
exe '4resize ' . ((&lines * 15 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 86 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 86 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 86 + 58) / 117)
exe '7resize ' . ((&lines * 19 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 86 + 58) / 117)
exe '8resize ' . ((&lines * 2 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 86 + 58) / 117)
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
let s:l = 11245 - ((0 * winheight(0) + 0) / 1)
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
let s:l = 4387 - ((0 * winheight(0) + 7) / 15)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4387
normal! 05|
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
2904
normal! zo
3021
normal! zo
3027
normal! zo
3067
normal! zo
let s:l = 3072 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3072
normal! 037|
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
38
normal! zo
let s:l = 31 - ((2 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 031|
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
122
normal! zo
129
normal! zo
130
normal! zo
130
normal! zo
130
normal! zo
133
normal! zo
136
normal! zo
137
normal! zo
137
normal! zo
154
normal! zo
170
normal! zo
176
normal! zo
202
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
212
normal! zo
214
normal! zo
223
normal! zo
224
normal! zo
224
normal! zo
224
normal! zo
224
normal! zo
225
normal! zo
228
normal! zo
229
normal! zo
229
normal! zo
229
normal! zo
229
normal! zo
230
normal! zo
233
normal! zo
234
normal! zo
252
normal! zo
256
normal! zo
260
normal! zo
261
normal! zo
268
normal! zo
268
normal! zo
268
normal! zo
271
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
280
normal! zo
281
normal! zo
285
normal! zo
292
normal! zo
292
normal! zo
306
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
316
normal! zo
316
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
332
normal! zo
332
normal! zo
332
normal! zo
332
normal! zo
342
normal! zo
342
normal! zo
342
normal! zo
342
normal! zo
342
normal! zo
342
normal! zo
344
normal! zo
357
normal! zo
358
normal! zo
359
normal! zo
359
normal! zo
364
normal! zo
365
normal! zo
369
normal! zo
377
normal! zo
377
normal! zo
377
normal! zo
377
normal! zo
382
normal! zo
400
normal! zo
406
normal! zo
406
normal! zo
406
normal! zo
406
normal! zo
406
normal! zo
409
normal! zo
417
normal! zo
422
normal! zo
433
normal! zo
443
normal! zo
463
normal! zo
472
normal! zo
475
normal! zo
490
normal! zo
495
normal! zo
495
normal! zo
495
normal! zo
495
normal! zo
495
normal! zo
495
normal! zo
495
normal! zo
499
normal! zo
504
normal! zo
507
normal! zo
518
normal! zo
519
normal! zo
529
normal! zo
536
normal! zo
536
normal! zo
536
normal! zo
536
normal! zo
536
normal! zo
551
normal! zo
557
normal! zo
559
normal! zo
560
normal! zo
563
normal! zo
573
normal! zo
579
normal! zo
579
normal! zo
579
normal! zo
579
normal! zo
579
normal! zo
583
normal! zo
586
normal! zo
586
normal! zo
601
normal! zo
602
normal! zo
602
normal! zo
608
normal! zo
let s:l = 413 - ((6 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
413
normal! 071|
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
exe 'vert 1resize ' . ((&columns * 30 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 86 + 58) / 117)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 86 + 58) / 117)
exe '4resize ' . ((&lines * 15 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 86 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 86 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 86 + 58) / 117)
exe '7resize ' . ((&lines * 19 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 86 + 58) / 117)
exe '8resize ' . ((&lines * 2 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 86 + 58) / 117)
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
