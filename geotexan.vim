" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 08 septiembre 2020 at 14:39:24.
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
if !exists('g:colors_name') || g:colors_name != 'night-owl' | colorscheme night-owl | endif
call setqflist([])
let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Geotexan/src/Geotex-INN/ginn
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
argglobal
%argdel
$argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit ~/.vimrc
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
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 17 + 65) / 131)
exe '2resize ' . ((&lines * 17 + 30) / 60)
exe 'vert 2resize ' . ((&columns * 113 + 65) / 131)
exe '3resize ' . ((&lines * 14 + 30) / 60)
exe 'vert 3resize ' . ((&columns * 113 + 65) / 131)
exe '4resize ' . ((&lines * 1 + 30) / 60)
exe 'vert 4resize ' . ((&columns * 113 + 65) / 131)
exe '5resize ' . ((&lines * 1 + 30) / 60)
exe 'vert 5resize ' . ((&columns * 113 + 65) / 131)
exe '6resize ' . ((&lines * 1 + 30) / 60)
exe 'vert 6resize ' . ((&columns * 113 + 65) / 131)
exe '7resize ' . ((&lines * 1 + 30) / 60)
exe 'vert 7resize ' . ((&columns * 113 + 65) / 131)
exe '8resize ' . ((&lines * 4 + 30) / 60)
exe 'vert 8resize ' . ((&columns * 113 + 65) / 131)
exe '9resize ' . ((&lines * 6 + 30) / 60)
exe 'vert 9resize ' . ((&columns * 113 + 65) / 131)
exe '10resize ' . ((&lines * 5 + 30) / 60)
exe 'vert 10resize ' . ((&columns * 113 + 65) / 131)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 234 - ((12 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
234
normal! 044|
wincmd w
argglobal
if bufexists("formularios/trazabilidad.py") | buffer formularios/trazabilidad.py | else | edit formularios/trazabilidad.py | endif
let s:l = 534 - ((4 * winheight(0) + 7) / 14)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
534
normal! 013|
wincmd w
argglobal
if bufexists("api/tests/feynman.py") | buffer api/tests/feynman.py | else | edit api/tests/feynman.py | endif
let s:l = 166 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
166
normal! 0
wincmd w
argglobal
if bufexists("api/murano/connection.py") | buffer api/murano/connection.py | else | edit api/murano/connection.py | endif
let s:l = 192 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
192
normal! 033|
wincmd w
argglobal
if bufexists("formularios/partes_de_fabricacion_balas.py") | buffer formularios/partes_de_fabricacion_balas.py | else | edit formularios/partes_de_fabricacion_balas.py | endif
let s:l = 1881 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1881
normal! 09|
wincmd w
argglobal
if bufexists("api/murano/ops.py") | buffer api/murano/ops.py | else | edit api/murano/ops.py | endif
let s:l = 2041 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2041
normal! 0
wincmd w
argglobal
if bufexists("api/tests/sr_lobo.py") | buffer api/tests/sr_lobo.py | else | edit api/tests/sr_lobo.py | endif
let s:l = 505 - ((0 * winheight(0) + 2) / 4)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
505
normal! 025|
wincmd w
argglobal
if bufexists("api/tests/ramanujan.py") | buffer api/tests/ramanujan.py | else | edit api/tests/ramanujan.py | endif
let s:l = 1747 - ((0 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1747
normal! 020|
wincmd w
argglobal
if bufexists("~/.vimrc") | buffer ~/.vimrc | else | edit ~/.vimrc | endif
let s:l = 1 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 17 + 65) / 131)
exe '2resize ' . ((&lines * 17 + 30) / 60)
exe 'vert 2resize ' . ((&columns * 113 + 65) / 131)
exe '3resize ' . ((&lines * 14 + 30) / 60)
exe 'vert 3resize ' . ((&columns * 113 + 65) / 131)
exe '4resize ' . ((&lines * 1 + 30) / 60)
exe 'vert 4resize ' . ((&columns * 113 + 65) / 131)
exe '5resize ' . ((&lines * 1 + 30) / 60)
exe 'vert 5resize ' . ((&columns * 113 + 65) / 131)
exe '6resize ' . ((&lines * 1 + 30) / 60)
exe 'vert 6resize ' . ((&columns * 113 + 65) / 131)
exe '7resize ' . ((&lines * 1 + 30) / 60)
exe 'vert 7resize ' . ((&columns * 113 + 65) / 131)
exe '8resize ' . ((&lines * 4 + 30) / 60)
exe 'vert 8resize ' . ((&columns * 113 + 65) / 131)
exe '9resize ' . ((&lines * 6 + 30) / 60)
exe 'vert 9resize ' . ((&columns * 113 + 65) / 131)
exe '10resize ' . ((&lines * 5 + 30) / 60)
exe 'vert 10resize ' . ((&columns * 113 + 65) / 131)
tabnext 1
badd +1 ~/.vimrc
badd +1 ~/Geotexan/src/Geotex-INN/geotexan.vim
badd +1 formularios/trazabilidad.py
badd +1 api/tests/feynman.py
badd +1 api/murano/connection.py
badd +1 formularios/partes_de_fabricacion_balas.py
badd +1 api/murano/ops.py
badd +1 api/tests/sr_lobo.py
badd +1759 api/tests/ramanujan.py
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
nohlsearch

" Support for special windows like quick-fix and plug-in windows.
" Everything down here is generated by vim-session (not supported
" by :mksession out of the box).

2wincmd w
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
