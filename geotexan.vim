" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 05 mayo 2015 at 17:29:50.
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
set lines=48 columns=114
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
exe 'vert 1resize ' . ((&columns * 29 + 57) / 114)
exe '2resize ' . ((&lines * 8 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 84 + 57) / 114)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 84 + 57) / 114)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 84 + 57) / 114)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 84 + 57) / 114)
exe '6resize ' . ((&lines * 25 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 84 + 57) / 114)
exe '7resize ' . ((&lines * 2 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 84 + 57) / 114)
exe '8resize ' . ((&lines * 2 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 84 + 57) / 114)
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
let s:l = 20945 - ((4 * winheight(0) + 4) / 8)
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
let s:l = 4442 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4442
normal! 038|
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
54
normal! zo
58
normal! zo
81
normal! zo
81
normal! zo
111
normal! zo
122
normal! zo
125
normal! zo
125
normal! zo
125
normal! zo
125
normal! zo
125
normal! zo
125
normal! zo
125
normal! zo
125
normal! zo
125
normal! zo
125
normal! zo
131
normal! zo
146
normal! zo
147
normal! zo
147
normal! zo
158
normal! zo
159
normal! zo
159
normal! zo
165
normal! zo
165
normal! zo
165
normal! zo
165
normal! zo
165
normal! zo
165
normal! zo
165
normal! zo
182
normal! zo
182
normal! zo
200
normal! zo
225
normal! zo
228
normal! zo
234
normal! zo
246
normal! zo
246
normal! zo
246
normal! zo
246
normal! zo
let s:l = 163 - ((21 * winheight(0) + 12) / 25)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
163
normal! 032|
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
257
normal! zo
260
normal! zo
261
normal! zo
265
normal! zo
273
normal! zo
273
normal! zo
273
normal! zo
276
normal! zo
280
normal! zo
280
normal! zo
280
normal! zo
280
normal! zo
280
normal! zo
285
normal! zo
286
normal! zo
290
normal! zo
297
normal! zo
297
normal! zo
311
normal! zo
321
normal! zo
321
normal! zo
321
normal! zo
321
normal! zo
321
normal! zo
321
normal! zo
321
normal! zo
325
normal! zo
325
normal! zo
325
normal! zo
325
normal! zo
325
normal! zo
337
normal! zo
337
normal! zo
337
normal! zo
337
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
349
normal! zo
357
normal! zo
366
normal! zo
367
normal! zo
368
normal! zo
368
normal! zo
373
normal! zo
374
normal! zo
378
normal! zo
386
normal! zo
386
normal! zo
386
normal! zo
386
normal! zo
391
normal! zo
409
normal! zo
415
normal! zo
415
normal! zo
415
normal! zo
415
normal! zo
415
normal! zo
418
normal! zo
427
normal! zo
432
normal! zo
443
normal! zo
453
normal! zo
473
normal! zo
482
normal! zo
485
normal! zo
500
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
509
normal! zo
514
normal! zo
517
normal! zo
528
normal! zo
529
normal! zo
539
normal! zo
546
normal! zo
546
normal! zo
546
normal! zo
546
normal! zo
546
normal! zo
561
normal! zo
567
normal! zo
569
normal! zo
570
normal! zo
573
normal! zo
578
normal! zo
584
normal! zo
592
normal! zo
598
normal! zo
598
normal! zo
598
normal! zo
598
normal! zo
598
normal! zo
602
normal! zo
605
normal! zo
605
normal! zo
620
normal! zo
621
normal! zo
621
normal! zo
627
normal! zo
let s:l = 584 - ((1 * winheight(0) + 1) / 2)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
584
normal! 041|
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
6wincmd w
exe 'vert 1resize ' . ((&columns * 29 + 57) / 114)
exe '2resize ' . ((&lines * 8 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 84 + 57) / 114)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 84 + 57) / 114)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 84 + 57) / 114)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 84 + 57) / 114)
exe '6resize ' . ((&lines * 25 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 84 + 57) / 114)
exe '7resize ' . ((&lines * 2 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 84 + 57) / 114)
exe '8resize ' . ((&lines * 2 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 84 + 57) / 114)
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
