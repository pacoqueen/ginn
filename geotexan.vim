" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 02 octubre 2017 at 12:19:16.
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
badd +1 informes/geninformes.py
badd +0 api/murano/connection.py
argglobal
silent! argdel *
$argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit informes/geninformes.py
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
set winminheight=1 winheight=1 winminwidth=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 17 + 57) / 115)
exe '2resize ' . ((&lines * 44 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 97 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 97 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 97 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 5resize ' . ((&columns * 97 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 6resize ' . ((&columns * 97 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 7resize ' . ((&columns * 97 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 8resize ' . ((&columns * 97 + 57) / 115)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 9828 - ((30 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9828
normal! 086|
wincmd w
argglobal
if bufexists('api/murano/connection.py') | buffer api/murano/connection.py | else | edit api/murano/connection.py | endif
let s:l = 77 - ((2 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
77
normal! 039|
wincmd w
argglobal
if bufexists('api/tests/ramanujan.py') | buffer api/tests/ramanujan.py | else | edit api/tests/ramanujan.py | endif
let s:l = 982 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
982
normal! 038|
wincmd w
argglobal
enew
wincmd w
argglobal
if bufexists('api/tests/sr_lobo.py') | buffer api/tests/sr_lobo.py | else | edit api/tests/sr_lobo.py | endif
let s:l = 395 - ((2 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
395
normal! 018|
wincmd w
argglobal
enew
wincmd w
argglobal
if bufexists('api/murano/ops.py') | buffer api/murano/ops.py | else | edit api/murano/ops.py | endif
let s:l = 1198 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1198
normal! 041|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 17 + 57) / 115)
exe '2resize ' . ((&lines * 44 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 97 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 97 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 97 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 5resize ' . ((&columns * 97 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 6resize ' . ((&columns * 97 + 57) / 115)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 7resize ' . ((&columns * 97 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 8resize ' . ((&columns * 97 + 57) / 115)
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
1resize 56|vert 1resize 17|2resize 44|vert 2resize 97|3resize 1|vert 3resize 97|4resize 1|vert 4resize 97|5resize 1|vert 5resize 97|6resize 1|vert 6resize 97|7resize 1|vert 7resize 97|8resize 1|vert 8resize 97|
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
