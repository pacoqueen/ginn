" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 21 junio 2016 at 17:12:37.
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
if !exists('g:colors_name') || g:colors_name != 'sierra' | colorscheme sierra | endif
call setqflist([{'lnum': 17, 'col': 1, 'valid': 1, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'ginn/api/murano/export.py', 'text': 'E402 module level import not at top of file'}, {'lnum': 18, 'col': 1, 'valid': 1, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'ginn/api/murano/export.py', 'text': 'E402 module level import not at top of file'}, {'lnum': 641, 'col': 80, 'valid': 1, 'vcol': 0, 'nr': -1, 'type': '', 'pattern': '', 'filename': 'ginn/api/murano/export.py', 'text': 'E501 line too long (81 > 79 characters)'}])
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
badd +16 ginn/api/murano/export.py
badd +1409 ginn/api/murano/ops.py
badd +166 ginn/api/murano/connection.py
badd +362 ginn/api/tests/murano_tests.py
badd +1 ginn/api/tests/dump_existencias.py
badd +882 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +2067 ginn/framework/pclases/__init__.py
badd +0 ginn/formularios/partes_de_fabricacion_rollos.py
argglobal
silent! argdel *
edit ginn/formularios/partes_de_fabricacion_bolsas.py
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
exe 'vert 1resize ' . ((&columns * 16 + 54) / 108)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 91 + 54) / 108)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 91 + 54) / 108)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 91 + 54) / 108)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 91 + 54) / 108)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 91 + 54) / 108)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 91 + 54) / 108)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 91 + 54) / 108)
exe '9resize ' . ((&lines * 32 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 91 + 54) / 108)
argglobal
enew
file __Tagbar__
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal nofen
wincmd w
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1794 - ((2 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1794
normal! 039|
wincmd w
argglobal
edit ginn/framework/pclases/__init__.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 9803 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9803
normal! 013|
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_balas.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 4029 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4029
normal! 027|
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_rollos.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 3499 - ((4 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3499
normal! 026|
wincmd w
argglobal
edit ginn/api/murano/connection.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 130 - ((2 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
130
normal! 021|
wincmd w
argglobal
edit ginn/api/tests/dump_existencias.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 42 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
42
normal! 05|
wincmd w
argglobal
edit ginn/api/murano/export.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1347 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1347
normal! 0
wincmd w
argglobal
edit ginn/api/murano/ops.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 2029 - ((30 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2029
normal! 013|
wincmd w
9wincmd w
exe 'vert 1resize ' . ((&columns * 16 + 54) / 108)
exe '2resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 2resize ' . ((&columns * 91 + 54) / 108)
exe '3resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 3resize ' . ((&columns * 91 + 54) / 108)
exe '4resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 4resize ' . ((&columns * 91 + 54) / 108)
exe '5resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 5resize ' . ((&columns * 91 + 54) / 108)
exe '6resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 6resize ' . ((&columns * 91 + 54) / 108)
exe '7resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 7resize ' . ((&columns * 91 + 54) / 108)
exe '8resize ' . ((&lines * 1 + 24) / 48)
exe 'vert 8resize ' . ((&columns * 91 + 54) / 108)
exe '9resize ' . ((&lines * 32 + 24) / 48)
exe 'vert 9resize ' . ((&columns * 91 + 54) / 108)
tabnext 1
if exists('s:wipebuf')
"   silent exe 'bwipe ' . s:wipebuf
endif
" unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToOc
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save

" Support for special windows like quick-fix and plug-in windows.
" Everything down here is generated by vim-session (not supported
" by :mksession out of the box).

9wincmd w
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
