" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 24 abril 2015 at 14:36:58.
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
badd +1 ginn/formularios/partes_de_visita.py
badd +902 ginn/formularios/productos_de_venta_rollos.py
badd +357 ginn/formularios/proveedores.py
badd +79 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/clientes.py
badd +1 ginn/formularios/ventana.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=45 columns=92
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
exe '1resize ' . ((&lines * 6 + 22) / 45)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe '5resize ' . ((&lines * 28 + 22) / 45)
exe '6resize ' . ((&lines * 1 + 22) / 45)
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
11243
normal! zo
11245
normal! zo
15992
normal! zo
16005
normal! zo
16015
normal! zo
let s:l = 11253 - ((1 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
11253
normal! 054|
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
let s:l = 3364 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3364
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/clientes.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/ventana.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
111
normal! zo
112
normal! zo
232
normal! zo
242
normal! zo
243
normal! zo
630
normal! zo
631
normal! zo
632
normal! zo
664
normal! zo
688
normal! zo
699
normal! zo
731
normal! zo
740
normal! zo
751
normal! zo
751
normal! zo
751
normal! zo
751
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
849
normal! zo
866
normal! zo
871
normal! zo
888
normal! zo
945
normal! zo
1022
normal! zo
1028
normal! zo
1031
normal! zo
1035
normal! zo
1042
normal! zo
1052
normal! zo
1052
normal! zo
1052
normal! zo
1052
normal! zo
1056
normal! zo
let s:l = 910 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
910
normal! 021|
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
69
normal! zo
69
normal! zo
69
normal! zo
78
normal! zo
78
normal! zo
78
normal! zo
78
normal! zo
78
normal! zo
80
normal! zo
80
normal! zo
80
normal! zo
80
normal! zo
80
normal! zo
82
normal! zo
82
normal! zo
82
normal! zo
82
normal! zo
82
normal! zo
94
normal! zo
95
normal! zo
101
normal! zo
102
normal! zo
103
normal! zo
108
normal! zo
109
normal! zo
115
normal! zo
142
normal! zo
148
normal! zo
172
normal! zo
180
normal! zo
181
normal! zo
181
normal! zo
181
normal! zo
181
normal! zo
181
normal! zo
181
normal! zo
181
normal! zo
181
normal! zo
185
normal! zo
194
normal! zo
195
normal! zo
195
normal! zo
195
normal! zo
195
normal! zo
196
normal! zo
199
normal! zo
200
normal! zo
200
normal! zo
200
normal! zo
200
normal! zo
201
normal! zo
215
normal! zo
219
normal! zo
223
normal! zo
224
normal! zo
230
normal! zo
230
normal! zo
230
normal! zo
241
normal! zo
248
normal! zo
248
normal! zo
262
normal! zo
290
normal! zo
291
normal! zo
294
normal! zo
294
normal! zo
294
normal! zo
294
normal! zo
299
normal! zo
313
normal! zo
324
normal! zo
334
normal! zo
354
normal! zo
363
normal! zo
366
normal! zo
381
normal! zo
388
normal! zo
393
normal! zo
398
normal! zo
407
normal! zo
408
normal! zo
418
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
440
normal! zo
453
normal! zo
459
normal! zo
459
normal! zo
459
normal! zo
459
normal! zo
459
normal! zo
463
normal! zo
466
normal! zo
466
normal! zo
let s:l = 279 - ((15 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
279
normal! 032|
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
let s:l = 4 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4
normal! 03|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
5wincmd w
exe '1resize ' . ((&lines * 6 + 22) / 45)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe '5resize ' . ((&lines * 28 + 22) / 45)
exe '6resize ' . ((&lines * 1 + 22) / 45)
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
5wincmd w

" vim: ft=vim ro nowrap smc=128
