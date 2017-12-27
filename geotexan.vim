" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 22 diciembre 2017 at 15:38:42.
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
badd +127 formularios/partes_de_fabricacion_balas.py
badd +3094 formularios/partes_de_fabricacion_rollos.py
badd +178 formularios/ventana.py
badd +112 formularios/partes_de_fabricacion_bolsas.py
badd +244 formularios/consumo_balas_partida.py
badd +1 formularios/productos_de_venta_rollos.py
badd +1 formularios/productos_de_venta_balas.py
argglobal
silent! argdel *
$argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit api/murano/connection.py
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
set winminheight=1 winheight=1 winminwidth=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 10 + 67) / 135)
exe '2resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 2resize ' . ((&columns * 124 + 67) / 135)
exe '3resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 3resize ' . ((&columns * 124 + 67) / 135)
exe '4resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 4resize ' . ((&columns * 124 + 67) / 135)
exe '5resize ' . ((&lines * 26 + 28) / 56)
exe 'vert 5resize ' . ((&columns * 124 + 67) / 135)
exe '6resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 6resize ' . ((&columns * 124 + 67) / 135)
exe '7resize ' . ((&lines * 19 + 28) / 56)
exe 'vert 7resize ' . ((&columns * 124 + 67) / 135)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 122 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
122
normal! 024|
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
let s:l = 880 - ((9 * winheight(0) + 13) / 26)
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
if bufexists('api/murano/ops.py') | buffer api/murano/ops.py | else | edit api/murano/ops.py | endif
let s:l = 3213 - ((9 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3213
normal! 05|
wincmd w
5wincmd w
exe 'vert 1resize ' . ((&columns * 10 + 67) / 135)
exe '2resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 2resize ' . ((&columns * 124 + 67) / 135)
exe '3resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 3resize ' . ((&columns * 124 + 67) / 135)
exe '4resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 4resize ' . ((&columns * 124 + 67) / 135)
exe '5resize ' . ((&lines * 26 + 28) / 56)
exe 'vert 5resize ' . ((&columns * 124 + 67) / 135)
exe '6resize ' . ((&lines * 1 + 28) / 56)
exe 'vert 6resize ' . ((&columns * 124 + 67) / 135)
exe '7resize ' . ((&lines * 19 + 28) / 56)
exe 'vert 7resize ' . ((&columns * 124 + 67) / 135)
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

5wincmd w
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
