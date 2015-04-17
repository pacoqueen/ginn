" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 17 abril 2015 at 14:40:06.
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
badd +10963 ginn/framework/pclases/__init__.py
badd +1406 ginn/formularios/partes_de_fabricacion_balas.py
badd +1 ginn/formularios/facturas_compra.py
badd +1 fugitive:///home/bogado/Geotexan/src/Geotex-INN/.git//0/ginn/formularios/utils.py
badd +9 ginn/lib/fuzzywuzzy/fuzzywuzzy/utils.py
badd +1 formularios/auditviewer.py
badd +1 ginn/formularios/utils.py
badd +2299 ginn/formularios/presupuestos.py
badd +38 ginn/informes/treeview2pdf.py
badd +138 ginn/formularios/listado_rollos.py
badd +2 ginn/lib/fuzzywuzzy/fuzzywuzzy/__init__.py
badd +1 ginn/formularios/consulta_ventas.py
badd +108 ginn/formularios/consulta_saldo_proveedores.py
badd +1 db/tablas.sql
badd +367 ginn/formularios/productos_compra.py
badd +0 ginn/formularios/partes_de_visita.py
badd +0 ginn/formularios/productos_de_venta_rollos.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=45 columns=92
edit ginn/formularios/utils.py
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
exe '1resize ' . ((&lines * 1 + 22) / 45)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe '4resize ' . ((&lines * 17 + 22) / 45)
exe '5resize ' . ((&lines * 17 + 22) / 45)
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
91
normal! zo
904
normal! zo
922
normal! zo
1196
normal! zo
1214
normal! zo
1227
normal! zo
1238
normal! zo
1248
normal! zo
1257
normal! zo
1271
normal! zo
2374
normal! zo
let s:l = 1245 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1245
normal! 064|
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
let s:l = 3382 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3382
normal! 02|
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
7650
normal! zo
7682
normal! zo
7696
normal! zo
7784
normal! zo
7813
normal! zo
7813
normal! zo
7813
normal! zo
7813
normal! zo
7813
normal! zo
7837
normal! zo
7906
normal! zo
7915
normal! zo
7923
normal! zo
7930
normal! zo
7931
normal! zo
7931
normal! zo
7931
normal! zo
7931
normal! zo
7942
normal! zo
7961
normal! zo
7964
normal! zo
7978
normal! zo
7979
normal! zo
7980
normal! zo
7985
normal! zo
7991
normal! zo
7997
normal! zo
7997
normal! zo
7997
normal! zo
7997
normal! zo
7997
normal! zo
7997
normal! zo
8031
normal! zo
8032
normal! zo
8033
normal! zo
8033
normal! zo
8033
normal! zo
8033
normal! zo
8033
normal! zo
8033
normal! zo
8033
normal! zo
8033
normal! zo
8033
normal! zo
8033
normal! zo
8035
normal! zo
8036
normal! zo
8036
normal! zo
8036
normal! zo
8036
normal! zo
8036
normal! zo
8036
normal! zo
8036
normal! zo
8036
normal! zo
8036
normal! zo
8036
normal! zo
8036
normal! zo
8038
normal! zo
8048
normal! zo
8049
normal! zo
8053
normal! zo
8057
normal! zo
8061
normal! zo
8066
normal! zo
8067
normal! zo
8068
normal! zo
8069
normal! zo
8069
normal! zo
8069
normal! zo
8069
normal! zo
8069
normal! zo
8069
normal! zo
8073
normal! zo
8079
normal! zo
8082
normal! zo
8082
normal! zo
8082
normal! zo
8082
normal! zo
8082
normal! zo
8091
normal! zo
8092
normal! zo
8101
normal! zo
8108
normal! zo
8108
normal! zo
8108
normal! zo
8108
normal! zo
8108
normal! zo
8108
normal! zo
8116
normal! zo
8117
normal! zo
8118
normal! zo
8126
normal! zo
8133
normal! zo
8133
normal! zo
8133
normal! zo
8133
normal! zo
8133
normal! zo
8133
normal! zo
8135
normal! zo
8141
normal! zo
8145
normal! zo
8150
normal! zo
8150
normal! zo
8150
normal! zo
8150
normal! zo
8150
normal! zo
8150
normal! zo
8150
normal! zo
12452
normal! zo
12452
normal! zo
12452
normal! zo
12784
normal! zo
12784
normal! zo
12784
normal! zo
let s:l = 8049 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
8049
normal! 042|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/productos_de_venta_rollos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
57
normal! zo
212
normal! zo
305
normal! zo
398
normal! zo
542
normal! zo
840
normal! zo
887
normal! zo
898
normal! zo
898
normal! zo
898
normal! zo
898
normal! zo
898
normal! zo
898
normal! zo
898
normal! zo
898
normal! zo
898
normal! zo
908
normal! zo
908
normal! zo
908
normal! zo
908
normal! zo
908
normal! zo
908
normal! zo
908
normal! zo
992
normal! zo
let s:l = 898 - ((7 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
898
normal! 065|
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
let s:l = 50 - ((5 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
50
normal! 027|
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
4wincmd w
exe '1resize ' . ((&lines * 1 + 22) / 45)
exe '2resize ' . ((&lines * 1 + 22) / 45)
exe '3resize ' . ((&lines * 1 + 22) / 45)
exe '4resize ' . ((&lines * 17 + 22) / 45)
exe '5resize ' . ((&lines * 17 + 22) / 45)
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
4wincmd w

" vim: ft=vim ro nowrap smc=128
