" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 18 mayo 2016 at 19:56:18.
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
badd +1 ginn/api/murano/export.py
badd +1 ginn/api/murano/export.py
badd +744 ginn/api/murano/ops.py
badd +166 ginn/api/murano/connection.py
badd +1 ginn/api/tests/murano_tests.py
badd +0 ginn/api/murano/extra.py
argglobal
silent! argdel *
edit ginn/api/murano/export.py
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
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 21 + 61) / 122)
exe '2resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 2resize ' . ((&columns * 100 + 61) / 122)
exe '3resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 3resize ' . ((&columns * 100 + 61) / 122)
exe '4resize ' . ((&lines * 23 + 26) / 53)
exe 'vert 4resize ' . ((&columns * 100 + 61) / 122)
exe '5resize ' . ((&lines * 10 + 26) / 53)
exe 'vert 5resize ' . ((&columns * 100 + 61) / 122)
exe '6resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 6resize ' . ((&columns * 100 + 61) / 122)
exe '7resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 7resize ' . ((&columns * 100 + 61) / 122)
exe '8resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 8resize ' . ((&columns * 100 + 61) / 122)
exe '9resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 9resize ' . ((&columns * 100 + 61) / 122)
exe '10resize ' . ((&lines * 4 + 26) / 53)
exe 'vert 10resize ' . ((&columns * 100 + 61) / 122)
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
let s:l = 5 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5
normal! 044|
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
let s:l = 57 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
57
normal! 043|
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
let s:l = 721 - ((10 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
721
normal! 035|
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
let s:l = 33 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
33
normal! 012|
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
let s:l = 362 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
362
normal! 016|
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 021|
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
let s:l = 641 - ((2 * winheight(0) + 2) / 4)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
641
normal! 013|
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 21 + 61) / 122)
exe '2resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 2resize ' . ((&columns * 100 + 61) / 122)
exe '3resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 3resize ' . ((&columns * 100 + 61) / 122)
exe '4resize ' . ((&lines * 23 + 26) / 53)
exe 'vert 4resize ' . ((&columns * 100 + 61) / 122)
exe '5resize ' . ((&lines * 10 + 26) / 53)
exe 'vert 5resize ' . ((&columns * 100 + 61) / 122)
exe '6resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 6resize ' . ((&columns * 100 + 61) / 122)
exe '7resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 7resize ' . ((&columns * 100 + 61) / 122)
exe '8resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 8resize ' . ((&columns * 100 + 61) / 122)
exe '9resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 9resize ' . ((&columns * 100 + 61) / 122)
exe '10resize ' . ((&lines * 4 + 26) / 53)
exe 'vert 10resize ' . ((&columns * 100 + 61) / 122)
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

5wincmd w
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
1resize 51|vert 1resize 21|2resize 1|vert 2resize 100|3resize 1|vert 3resize 100|4resize 23|vert 4resize 100|5resize 10|vert 5resize 100|6resize 1|vert 6resize 100|7resize 1|vert 7resize 100|8resize 1|vert 8resize 100|9resize 1|vert 9resize 100|10resize 4|vert 10resize 100|
4wincmd w
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
