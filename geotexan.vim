" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 27 mayo 2016 at 19:49:53.
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
badd +744 ginn/api/murano/ops.py
badd +166 ginn/api/murano/connection.py
badd +1 dump_existencias.py
badd +1 ginn/api/murano/extra.py
badd +1 ginn/api/tests/murano_tests.py
badd +1 ginn/api/tests/dump_existencias.py
badd +0 ginn/framework/pclases/__init__.py
argglobal
silent! argdel *
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
12wincmd k
wincmd w
wincmd w
wincmd w
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
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 26 + 60) / 121)
exe '2resize ' . ((&lines * 26 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 94 + 60) / 121)
exe '3resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 94 + 60) / 121)
exe '4resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 94 + 60) / 121)
exe '5resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 94 + 60) / 121)
exe '6resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 94 + 60) / 121)
exe '7resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 7resize ' . ((&columns * 94 + 60) / 121)
exe '8resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 8resize ' . ((&columns * 94 + 60) / 121)
exe '9resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 9resize ' . ((&columns * 94 + 60) / 121)
exe '10resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 10resize ' . ((&columns * 94 + 60) / 121)
exe '11resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 11resize ' . ((&columns * 94 + 60) / 121)
exe '12resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 12resize ' . ((&columns * 94 + 60) / 121)
exe '13resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 13resize ' . ((&columns * 94 + 60) / 121)
exe '14resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 14resize ' . ((&columns * 94 + 60) / 121)
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
let s:l = 11576 - ((3 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
11576
normal! 030|
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
argglobal
edit ginn/api/murano/extra.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 29 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
29
normal! 054|
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
let s:l = 333 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
333
normal! 049|
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
let s:l = 129 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
129
normal! 05|
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
let s:l = 100 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
100
normal! 058|
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
let s:l = 26 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
26
normal! 024|
wincmd w
argglobal
edit ginn/api/murano/extra.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit ginn/api/murano/extra.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit ginn/api/murano/extra.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
2wincmd w
exe 'vert 1resize ' . ((&columns * 26 + 60) / 121)
exe '2resize ' . ((&lines * 26 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 94 + 60) / 121)
exe '3resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 94 + 60) / 121)
exe '4resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 94 + 60) / 121)
exe '5resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 94 + 60) / 121)
exe '6resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 94 + 60) / 121)
exe '7resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 7resize ' . ((&columns * 94 + 60) / 121)
exe '8resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 8resize ' . ((&columns * 94 + 60) / 121)
exe '9resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 9resize ' . ((&columns * 94 + 60) / 121)
exe '10resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 10resize ' . ((&columns * 94 + 60) / 121)
exe '11resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 11resize ' . ((&columns * 94 + 60) / 121)
exe '12resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 12resize ' . ((&columns * 94 + 60) / 121)
exe '13resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 13resize ' . ((&columns * 94 + 60) / 121)
exe '14resize ' . ((&lines * 1 + 26) / 52)
exe 'vert 14resize ' . ((&columns * 94 + 60) / 121)
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

3wincmd w
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
6wincmd w
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
14wincmd w
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
1resize 50|vert 1resize 26|2resize 26|vert 2resize 94|3resize 1|vert 3resize 94|4resize 1|vert 4resize 94|5resize 1|vert 5resize 94|6resize 1|vert 6resize 94|7resize 1|vert 7resize 94|8resize 1|vert 8resize 94|9resize 1|vert 9resize 94|10resize 1|vert 10resize 94|11resize 1|vert 11resize 94|12resize 1|vert 12resize 94|13resize 1|vert 13resize 94|14resize 1|vert 14resize 94|
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
