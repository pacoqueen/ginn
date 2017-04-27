" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 22 abril 2017 at 14:24:43.
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
badd +175 api/tests/clouseau.py
badd +421 api/tests/ramanujan.py
badd +1 api/murano/ops.py
badd +48 formularios/reports.py
badd +582 informes/norma2013.py
badd +1 api/murano/export.py
badd +159 formularios/listado_balas.py
badd +1 api/tests/sr_lobo.py
badd +0 ~/Geotexan/src/Geotex-INN/geotexan.vim
argglobal
silent! argdel *
argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit api/tests/sr_lobo.py
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
10wincmd k
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
exe 'vert 1resize ' . ((&columns * 24 + 57) / 115)
exe '2resize ' . ((&lines * 15 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 90 + 57) / 115)
exe '3resize ' . ((&lines * 5 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 90 + 57) / 115)
exe '4resize ' . ((&lines * 7 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 90 + 57) / 115)
exe '5resize ' . ((&lines * 4 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 90 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 6resize ' . ((&columns * 90 + 57) / 115)
exe '7resize ' . ((&lines * 4 + 32) / 64)
exe 'vert 7resize ' . ((&columns * 90 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 8resize ' . ((&columns * 90 + 57) / 115)
exe '9resize ' . ((&lines * 4 + 32) / 64)
exe 'vert 9resize ' . ((&columns * 90 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 10resize ' . ((&columns * 90 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 11resize ' . ((&columns * 90 + 57) / 115)
exe '12resize ' . ((&lines * 9 + 32) / 64)
exe 'vert 12resize ' . ((&columns * 90 + 57) / 115)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 714 - ((7 * winheight(0) + 7) / 15)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
714
normal! 030|
wincmd w
argglobal
edit informes/norma2013.py
let s:l = 678 - ((1 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
678
normal! 016|
wincmd w
argglobal
edit api/tests/clouseau.py
let s:l = 92 - ((5 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
92
normal! 047|
wincmd w
argglobal
enew
wincmd w
argglobal
edit api/murano/ops.py
let s:l = 1191 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1191
normal! 016|
wincmd w
argglobal
enew
wincmd w
argglobal
edit api/tests/ramanujan.py
let s:l = 1179 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1179
normal! 023|
wincmd w
argglobal
enew
wincmd w
argglobal
edit api/tests/sr_lobo.py
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit api/tests/sr_lobo.py
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit api/tests/sr_lobo.py
let s:l = 6 - ((3 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
6
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 24 + 57) / 115)
exe '2resize ' . ((&lines * 15 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 90 + 57) / 115)
exe '3resize ' . ((&lines * 5 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 90 + 57) / 115)
exe '4resize ' . ((&lines * 7 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 90 + 57) / 115)
exe '5resize ' . ((&lines * 4 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 90 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 6resize ' . ((&columns * 90 + 57) / 115)
exe '7resize ' . ((&lines * 4 + 32) / 64)
exe 'vert 7resize ' . ((&columns * 90 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 8resize ' . ((&columns * 90 + 57) / 115)
exe '9resize ' . ((&lines * 4 + 32) / 64)
exe 'vert 9resize ' . ((&columns * 90 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 10resize ' . ((&columns * 90 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 32) / 64)
exe 'vert 11resize ' . ((&columns * 90 + 57) / 115)
exe '12resize ' . ((&lines * 9 + 32) / 64)
exe 'vert 12resize ' . ((&columns * 90 + 57) / 115)
tabnext 1
if exists('s:wipebuf')
"   silent exe 'bwipe ' . s:wipebuf
endif
" unlet! s:wipebuf
set winheight=1 winwidth=1 shortmess=aoOc
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
7wincmd w
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
9wincmd w
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
1resize 62|vert 1resize 24|2resize 15|vert 2resize 90|3resize 5|vert 3resize 90|4resize 7|vert 4resize 90|5resize 4|vert 5resize 90|6resize 1|vert 6resize 90|7resize 4|vert 7resize 90|8resize 1|vert 8resize 90|9resize 4|vert 9resize 90|10resize 1|vert 10resize 90|11resize 1|vert 11resize 90|12resize 9|vert 12resize 90|
1wincmd w
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
