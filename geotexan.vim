" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 19 abril 2018 at 18:41:20.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Menlo\ For\ Powerline
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'light'
	set background=light
endif
if !exists('g:colors_name') || g:colors_name != 'solarized' | colorscheme solarized | endif
call setqflist([])
let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Geotexan/src/Geotex-INN/ginn
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +39 api/murano/ops.py
badd +1 api/tests/sr_lobo.py
badd +1 api/tests/ramanujan.py
badd +1 ~/Geotexan/src/Geotex-INN/geotexan.vim
badd +9845 informes/geninformes.py
badd +1 api/murano/connection.py
badd +1423 formularios/partes_de_fabricacion_rollos.py
badd +178 formularios/ventana.py
badd +112 formularios/partes_de_fabricacion_bolsas.py
badd +1 formularios/productos_de_venta_rollos.py
badd +1 formularios/productos_de_venta_balas.py
badd +1 framework/pclases/__init__.py
badd +47 ~/Geotexan/src/fixes/20180206_cambio_a_C.py
badd +1 ~/Geotexan/src/fixes/20180206_cambio_a_c.py
badd +1 ~/Geotexan/src/Geotex-INN/extra/scripts/20180206_cambio_a_C.py
argglobal
silent! argdel *
$argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit framework/pclases/__init__.py
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
wincmd _ | wincmd |
split
8wincmd k
wincmd w
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
set winminheight=1 winheight=1 winminwidth=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 32 + 67) / 134)
exe '2resize ' . ((&lines * 20 + 28) / 56)
exe 'vert 2resize ' . ((&columns * 101 + 67) / 134)
exe '3resize ' . ((&lines * 19 + 28) / 56)
exe 'vert 3resize ' . ((&columns * 101 + 67) / 134)
exe '4resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 4resize ' . ((&columns * 101 + 67) / 134)
exe '5resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 5resize ' . ((&columns * 101 + 67) / 134)
exe '6resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 6resize ' . ((&columns * 101 + 67) / 134)
exe '7resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 7resize ' . ((&columns * 101 + 67) / 134)
exe '8resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 8resize ' . ((&columns * 101 + 67) / 134)
exe '9resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 9resize ' . ((&columns * 101 + 67) / 134)
exe '10resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 10resize ' . ((&columns * 101 + 67) / 134)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 9909 - ((1 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9909
normal! 09|
wincmd w
argglobal
if bufexists('formularios/partes_de_fabricacion_rollos.py') | buffer formularios/partes_de_fabricacion_rollos.py | else | edit formularios/partes_de_fabricacion_rollos.py | endif
let s:l = 3109 - ((9 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3109
normal! 09|
wincmd w
argglobal
if bufexists('api/murano/connection.py') | buffer api/murano/connection.py | else | edit api/murano/connection.py | endif
let s:l = 148 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
148
normal! 027|
wincmd w
argglobal
if bufexists('api/tests/ramanujan.py') | buffer api/tests/ramanujan.py | else | edit api/tests/ramanujan.py | endif
let s:l = 372 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
372
normal! 034|
wincmd w
argglobal
if bufexists('formularios/productos_de_venta_balas.py') | buffer formularios/productos_de_venta_balas.py | else | edit formularios/productos_de_venta_balas.py | endif
let s:l = 559 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
559
normal! 05|
wincmd w
argglobal
if bufexists('formularios/productos_de_venta_rollos.py') | buffer formularios/productos_de_venta_rollos.py | else | edit formularios/productos_de_venta_rollos.py | endif
let s:l = 880 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
880
normal! 023|
wincmd w
argglobal
if bufexists('api/tests/sr_lobo.py') | buffer api/tests/sr_lobo.py | else | edit api/tests/sr_lobo.py | endif
let s:l = 359 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
359
normal! 05|
wincmd w
argglobal
if bufexists('~/Geotexan/src/Geotex-INN/extra/scripts/20180206_cambio_a_C.py') | buffer ~/Geotexan/src/Geotex-INN/extra/scripts/20180206_cambio_a_C.py | else | edit ~/Geotexan/src/Geotex-INN/extra/scripts/20180206_cambio_a_C.py | endif
let s:l = 111 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
111
normal! 065|
wincmd w
argglobal
if bufexists('api/murano/ops.py') | buffer api/murano/ops.py | else | edit api/murano/ops.py | endif
let s:l = 1945 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1945
normal! 037|
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 32 + 67) / 134)
exe '2resize ' . ((&lines * 20 + 28) / 56)
exe 'vert 2resize ' . ((&columns * 101 + 67) / 134)
exe '3resize ' . ((&lines * 19 + 28) / 56)
exe 'vert 3resize ' . ((&columns * 101 + 67) / 134)
exe '4resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 4resize ' . ((&columns * 101 + 67) / 134)
exe '5resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 5resize ' . ((&columns * 101 + 67) / 134)
exe '6resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 6resize ' . ((&columns * 101 + 67) / 134)
exe '7resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 7resize ' . ((&columns * 101 + 67) / 134)
exe '8resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 8resize ' . ((&columns * 101 + 67) / 134)
exe '9resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 9resize ' . ((&columns * 101 + 67) / 134)
exe '10resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 10resize ' . ((&columns * 101 + 67) / 134)
tabnext 1
if exists('s:wipebuf')
"   silent exe 'bwipe ' . s:wipebuf
endif
" unlet! s:wipebuf
set winheight=1 winwidth=1 shortmess=aoOc
set winminheight=1 winminwidth=1
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save

" Support for special windows like quick-fix and plug-in windows.
" Everything down here is generated by vim-session (not supported
" by :mksession out of the box).

3wincmd w
tabnext 1
if exists('s:wipebuf')
  if empty(bufname(s:wipebuf))
if !getbufvar(s:wipebuf, '&modified')
  let s:wipebuflines = getbufline(s:wipebuf, 1, '$')
  if len(s:wipebuflines) <= 1 && empty(get(s:wipebuflines, 0, ''))
    silent execute 'bwipeout' s:wipebuf
  endif
endif
  endif
endif
doautoall SessionLoadPost
unlet SessionLoad
" vim: ft=vim ro nowrap smc=128
