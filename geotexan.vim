" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 07 junio 2016 at 07:16:24.
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
badd +1 ginn/api/tests/murano_tests.py
badd +1 ginn/api/tests/dump_existencias.py
badd +53 ginn/api/murano/extra.py
badd +1 ginn/api/murano/__init__.py
argglobal
silent! argdel *
edit ginn/api/murano/__init__.py
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
exe 'vert 1resize ' . ((&columns * 23 + 61) / 123)
exe '2resize ' . ((&lines * 7 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 99 + 61) / 123)
exe '3resize ' . ((&lines * 5 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 99 + 61) / 123)
exe '4resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 99 + 61) / 123)
exe '5resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 99 + 61) / 123)
exe '6resize ' . ((&lines * 8 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 99 + 61) / 123)
exe '7resize ' . ((&lines * 12 + 26) / 52)
exe 'vert 7resize ' . ((&columns * 99 + 61) / 123)
exe '8resize ' . ((&lines * 10 + 26) / 52)
exe 'vert 8resize ' . ((&columns * 99 + 61) / 123)
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
let s:l = 36 - ((1 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
36
normal! 05|
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
let s:l = 77 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
77
normal! 038|
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
normal! 040|
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
let s:l = 1341 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1341
normal! 038|
wincmd w
argglobal
edit ginn/api/tests/murano_tests.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 82 - ((0 * winheight(0) + 4) / 8)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
82
normal! 012|
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
let s:l = 1633 - ((8 * winheight(0) + 6) / 12)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1633
normal! 072|
wincmd w
argglobal
enew
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
wincmd w
7wincmd w
exe 'vert 1resize ' . ((&columns * 23 + 61) / 123)
exe '2resize ' . ((&lines * 7 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 99 + 61) / 123)
exe '3resize ' . ((&lines * 5 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 99 + 61) / 123)
exe '4resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 99 + 61) / 123)
exe '5resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 99 + 61) / 123)
exe '6resize ' . ((&lines * 8 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 99 + 61) / 123)
exe '7resize ' . ((&lines * 12 + 26) / 52)
exe 'vert 7resize ' . ((&columns * 99 + 61) / 123)
exe '8resize ' . ((&lines * 10 + 26) / 52)
exe 'vert 8resize ' . ((&columns * 99 + 61) / 123)
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

8wincmd w
tabnext 1
let s:bufnr_save = bufnr("%")
let s:cwd_save = getcwd()
cwindow
if !getbufvar(s:bufnr_save, '&modified')
  let s:wipebuflines = getbufline(s:bufnr_save, 1, '$')
  if len(s:wipebuflines) <= 1 && empty(get(s:wipebuflines, 0, ''))
    silent execute 'bwipeout' s:bufnr_save
  endif
endif
execute "cd" fnameescape(s:cwd_save)
1resize 50|vert 1resize 23|2resize 7|vert 2resize 99|3resize 5|vert 3resize 99|4resize 1|vert 4resize 99|5resize 1|vert 5resize 99|6resize 8|vert 6resize 99|7resize 12|vert 7resize 99|8resize 10|vert 8resize 99|
7wincmd w
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
