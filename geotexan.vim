" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 20 enero 2021 at 11:39:26.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Menlo\ For\ Powerline
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'kalisi' | colorscheme kalisi | endif
call setqflist([])
let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Geotexan/src/Geotex-INN
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
argglobal
%argdel
$argadd geotexan.vim
edit ginn/formularios/pyconsole.py
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
wincmd _ | wincmd |
split
9wincmd k
wincmd w
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
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 29 + 61) / 123)
exe '2resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 2resize ' . ((&columns * 93 + 61) / 123)
exe '3resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 3resize ' . ((&columns * 93 + 61) / 123)
exe '4resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 4resize ' . ((&columns * 93 + 61) / 123)
exe '5resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 5resize ' . ((&columns * 93 + 61) / 123)
exe '6resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 6resize ' . ((&columns * 93 + 61) / 123)
exe '7resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 7resize ' . ((&columns * 93 + 61) / 123)
exe '8resize ' . ((&lines * 41 + 30) / 61)
exe 'vert 8resize ' . ((&columns * 93 + 61) / 123)
exe '9resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 9resize ' . ((&columns * 93 + 61) / 123)
exe '10resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 10resize ' . ((&columns * 93 + 61) / 123)
exe '11resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 11resize ' . ((&columns * 93 + 61) / 123)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 596 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
596
normal! 09|
wincmd w
argglobal
if bufexists("ginn/formularios/trazabilidad.py") | buffer ginn/formularios/trazabilidad.py | else | edit ginn/formularios/trazabilidad.py | endif
let s:l = 41 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
41
normal! 033|
wincmd w
argglobal
if bufexists("ginn/formularios/menu.py") | buffer ginn/formularios/menu.py | else | edit ginn/formularios/menu.py | endif
let s:l = 499 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
499
normal! 075|
wincmd w
argglobal
if bufexists("ginn/formularios/trazabilidad_articulos.py") | buffer ginn/formularios/trazabilidad_articulos.py | else | edit ginn/formularios/trazabilidad_articulos.py | endif
let s:l = 1092 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1092
normal! 013|
wincmd w
argglobal
if bufexists("ginn/api/tests/feynman.py") | buffer ginn/api/tests/feynman.py | else | edit ginn/api/tests/feynman.py | endif
let s:l = 166 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
166
normal! 0
wincmd w
argglobal
if bufexists("ginn/api/murano/connection.py") | buffer ginn/api/murano/connection.py | else | edit ginn/api/murano/connection.py | endif
let s:l = 192 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
192
normal! 033|
wincmd w
argglobal
if bufexists("ginn/formularios/consulta_producido.py") | buffer ginn/formularios/consulta_producido.py | else | edit ginn/formularios/consulta_producido.py | endif
let s:l = 439 - ((26 * winheight(0) + 20) / 41)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
439
normal! 056|
wincmd w
argglobal
if bufexists("ginn/api/murano/ops.py") | buffer ginn/api/murano/ops.py | else | edit ginn/api/murano/ops.py | endif
let s:l = 2041 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2041
normal! 0
wincmd w
argglobal
if bufexists("ginn/api/tests/sr_lobo.py") | buffer ginn/api/tests/sr_lobo.py | else | edit ginn/api/tests/sr_lobo.py | endif
let s:l = 696 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
696
normal! 046|
wincmd w
argglobal
if bufexists("ginn/api/tests/ramanujan.py") | buffer ginn/api/tests/ramanujan.py | else | edit ginn/api/tests/ramanujan.py | endif
let s:l = 1926 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1926
normal! 028|
wincmd w
8wincmd w
exe 'vert 1resize ' . ((&columns * 29 + 61) / 123)
exe '2resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 2resize ' . ((&columns * 93 + 61) / 123)
exe '3resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 3resize ' . ((&columns * 93 + 61) / 123)
exe '4resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 4resize ' . ((&columns * 93 + 61) / 123)
exe '5resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 5resize ' . ((&columns * 93 + 61) / 123)
exe '6resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 6resize ' . ((&columns * 93 + 61) / 123)
exe '7resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 7resize ' . ((&columns * 93 + 61) / 123)
exe '8resize ' . ((&lines * 41 + 30) / 61)
exe 'vert 8resize ' . ((&columns * 93 + 61) / 123)
exe '9resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 9resize ' . ((&columns * 93 + 61) / 123)
exe '10resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 10resize ' . ((&columns * 93 + 61) / 123)
exe '11resize ' . ((&lines * 1 + 30) / 61)
exe 'vert 11resize ' . ((&columns * 93 + 61) / 123)
tabnext 1
badd +1 ginn/formularios/pyconsole.py
badd +1 geotexan.vim
badd +192 ginn/formularios/trazabilidad.py
badd +501 ginn/formularios/menu.py
badd +1 ginn/formularios/trazabilidad_articulos.py
badd +1 ginn/api/tests/feynman.py
badd +1 ginn/api/murano/connection.py
badd +1223 ginn/formularios/partes_de_fabricacion_balas.py
badd +1 ginn/api/murano/ops.py
badd +0 ginn/api/tests/sr_lobo.py
badd +1759 ginn/api/tests/ramanujan.py
badd +46 ginn/formularios/custom_widgets/marquee_label.py
badd +309 ginn/formularios/gtkexcepthook.py
badd +110 ginn/formularios/launcher.py
badd +0 ginn/formularios/consulta_producido.py
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0
"   silent exe 'bwipe ' . s:wipebuf
endif
" unlet! s:wipebuf
set winheight=1 winwidth=1 shortmess=aoOc
set winminheight=1 winminwidth=1
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save

" Support for special windows like quick-fix and plug-in windows.
" Everything down here is generated by vim-session (not supported
" by :mksession out of the box).

8wincmd w
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
