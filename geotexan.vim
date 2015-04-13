" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 13 abril 2015 at 12:30:04.
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
badd +1260 ginn/formularios/utils.py
badd +2299 ginn/formularios/presupuestos.py
badd +38 ginn/informes/treeview2pdf.py
badd +138 ginn/formularios/listado_rollos.py
badd +2 ginn/lib/fuzzywuzzy/fuzzywuzzy/__init__.py
badd +1 ginn/formularios/consulta_ventas.py
badd +1 ginn/formularios/consulta_saldo_proveedores.py
badd +1 db/tablas.sql
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=54 columns=103
edit ginn/formularios/partes_de_ancho_multiple.py
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
exe 'vert 1resize ' . ((&columns * 20 + 51) / 103)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 82 + 51) / 103)
exe '3resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 82 + 51) / 103)
exe '4resize ' . ((&lines * 38 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 82 + 51) / 103)
exe '5resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 82 + 51) / 103)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 82 + 51) / 103)
exe '7resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 82 + 51) / 103)
exe '8resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 8resize ' . ((&columns * 82 + 51) / 103)
exe '9resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 9resize ' . ((&columns * 82 + 51) / 103)
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
let s:l = 22 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 011|
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
let s:l = 3376 - ((25 * winheight(0) + 19) / 38)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3376
normal! 02|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_saldo_proveedores.py
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
77
normal! zo
77
normal! zo
81
normal! zo
115
normal! zo
122
normal! zo
124
normal! zo
124
normal! zo
124
normal! zo
124
normal! zo
124
normal! zo
124
normal! zo
124
normal! zo
124
normal! zo
124
normal! zo
126
normal! zo
134
normal! zo
147
normal! zo
148
normal! zo
148
normal! zo
159
normal! zo
160
normal! zo
160
normal! zo
169
normal! zo
169
normal! zo
169
normal! zo
169
normal! zo
169
normal! zo
169
normal! zo
177
normal! zo
179
normal! zo
181
normal! zo
183
normal! zo
202
normal! zo
227
normal! zo
230
normal! zo
236
normal! zo
248
normal! zo
248
normal! zo
248
normal! zo
248
normal! zo
let s:l = 82 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
82
normal! 023|
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 20 + 51) / 103)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 82 + 51) / 103)
exe '3resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 82 + 51) / 103)
exe '4resize ' . ((&lines * 38 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 82 + 51) / 103)
exe '5resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 82 + 51) / 103)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 82 + 51) / 103)
exe '7resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 82 + 51) / 103)
exe '8resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 8resize ' . ((&columns * 82 + 51) / 103)
exe '9resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 9resize ' . ((&columns * 82 + 51) / 103)
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
