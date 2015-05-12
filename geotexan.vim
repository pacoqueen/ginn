" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 12 mayo 2015 at 17:28:22.
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
badd +108 ginn/formularios/consulta_partes_de_visita.py
badd +1 db/tablas.sql
badd +367 ginn/formularios/productos_compra.py
badd +54 ginn/formularios/partes_de_visita.py
badd +902 ginn/formularios/productos_de_venta_rollos.py
badd +357 ginn/formularios/proveedores.py
badd +79 ginn/framework/pclases/cliente.py
badd +6 ginn/formularios/clientes.py
badd +914 ginn/formularios/ventana.py
badd +1 ginn/formularios/presupuestos.py
badd +17 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +1 ginn/formularios/consulta_saldo_proveedores.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=48 columns=116
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
exe 'vert 1resize ' . ((&columns * 29 + 58) / 116)
exe '2resize ' . ((&lines * 8 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 86 + 58) / 116)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 86 + 58) / 116)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 86 + 58) / 116)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 86 + 58) / 116)
exe '6resize ' . ((&lines * 3 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 86 + 58) / 116)
exe '7resize ' . ((&lines * 24 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 86 + 58) / 116)
exe '8resize ' . ((&lines * 2 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 86 + 58) / 116)
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
let s:l = 20945 - ((7 * winheight(0) + 4) / 8)
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
let s:l = 4442 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4442
normal! 0
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
60
normal! zo
82
normal! zo
83
normal! zo
87
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
100
normal! zo
106
normal! zo
108
normal! zo
108
normal! zo
139
normal! zo
149
normal! zo
149
normal! zo
149
normal! zo
149
normal! zo
149
normal! zo
149
normal! zo
149
normal! zo
149
normal! zo
149
normal! zo
149
normal! zo
149
normal! zo
155
normal! zo
171
normal! zo
172
normal! zo
172
normal! zo
184
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
187
normal! zo
187
normal! zo
195
normal! zo
195
normal! zo
195
normal! zo
195
normal! zo
195
normal! zo
195
normal! zo
195
normal! zo
204
normal! zo
206
normal! zo
209
normal! zo
217
normal! zo
223
normal! zo
223
normal! zo
228
normal! zo
241
normal! zo
269
normal! zo
272
normal! zo
278
normal! zo
290
normal! zo
290
normal! zo
290
normal! zo
290
normal! zo
let s:l = 144 - ((0 * winheight(0) + 1) / 3)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
144
normal! 09|
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
72
normal! zo
72
normal! zo
72
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
83
normal! zo
83
normal! zo
83
normal! zo
83
normal! zo
83
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
97
normal! zo
98
normal! zo
104
normal! zo
105
normal! zo
106
normal! zo
111
normal! zo
112
normal! zo
118
normal! zo
128
normal! zo
135
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
139
normal! zo
142
normal! zo
143
normal! zo
143
normal! zo
160
normal! zo
176
normal! zo
182
normal! zo
208
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
218
normal! zo
220
normal! zo
229
normal! zo
230
normal! zo
230
normal! zo
230
normal! zo
230
normal! zo
231
normal! zo
234
normal! zo
235
normal! zo
235
normal! zo
235
normal! zo
235
normal! zo
236
normal! zo
239
normal! zo
240
normal! zo
258
normal! zo
262
normal! zo
263
normal! zo
266
normal! zo
267
normal! zo
271
normal! zo
279
normal! zo
279
normal! zo
279
normal! zo
282
normal! zo
286
normal! zo
286
normal! zo
286
normal! zo
286
normal! zo
286
normal! zo
291
normal! zo
292
normal! zo
296
normal! zo
303
normal! zo
303
normal! zo
317
normal! zo
327
normal! zo
327
normal! zo
327
normal! zo
327
normal! zo
327
normal! zo
327
normal! zo
327
normal! zo
331
normal! zo
331
normal! zo
331
normal! zo
331
normal! zo
331
normal! zo
343
normal! zo
343
normal! zo
343
normal! zo
343
normal! zo
353
normal! zo
353
normal! zo
353
normal! zo
353
normal! zo
353
normal! zo
353
normal! zo
355
normal! zo
363
normal! zo
372
normal! zo
373
normal! zo
374
normal! zo
374
normal! zo
379
normal! zo
380
normal! zo
384
normal! zo
392
normal! zo
392
normal! zo
392
normal! zo
392
normal! zo
397
normal! zo
415
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
424
normal! zo
433
normal! zo
438
normal! zo
449
normal! zo
459
normal! zo
479
normal! zo
488
normal! zo
491
normal! zo
506
normal! zo
511
normal! zo
511
normal! zo
511
normal! zo
511
normal! zo
511
normal! zo
511
normal! zo
511
normal! zo
515
normal! zo
520
normal! zo
523
normal! zo
534
normal! zo
535
normal! zo
545
normal! zo
552
normal! zo
552
normal! zo
552
normal! zo
552
normal! zo
552
normal! zo
567
normal! zo
573
normal! zo
575
normal! zo
576
normal! zo
579
normal! zo
584
normal! zo
590
normal! zo
598
normal! zo
604
normal! zo
604
normal! zo
604
normal! zo
604
normal! zo
604
normal! zo
608
normal! zo
611
normal! zo
611
normal! zo
626
normal! zo
627
normal! zo
627
normal! zo
633
normal! zo
let s:l = 70 - ((4 * winheight(0) + 12) / 24)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
70
normal! 060|
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
exe 'vert 1resize ' . ((&columns * 29 + 58) / 116)
exe '2resize ' . ((&lines * 8 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 86 + 58) / 116)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 86 + 58) / 116)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 86 + 58) / 116)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 86 + 58) / 116)
exe '6resize ' . ((&lines * 3 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 86 + 58) / 116)
exe '7resize ' . ((&lines * 24 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 86 + 58) / 116)
exe '8resize ' . ((&lines * 2 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 86 + 58) / 116)
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
