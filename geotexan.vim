" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 19 marzo 2019 at 15:00:02.
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
if !exists('g:colors_name') || g:colors_name != 'summerfruit256' | colorscheme summerfruit256 | endif
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
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 22 + 57) / 115)
exe '2resize ' . ((&lines * 3 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 92 + 57) / 115)
exe '3resize ' . ((&lines * 8 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 92 + 57) / 115)
exe '4resize ' . ((&lines * 35 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 92 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 92 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 92 + 57) / 115)
exe '7resize ' . ((&lines * 2 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 92 + 57) / 115)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 186 - ((1 * winheight(0) + 1) / 3)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
186
normal! 034|
wincmd w
argglobal
if bufexists("api/murano/ops.py") | buffer api/murano/ops.py | else | edit api/murano/ops.py | endif
let s:l = 3353 - ((6 * winheight(0) + 4) / 8)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3353
normal! 015|
wincmd w
argglobal
if bufexists("api/tests/sr_lobo.py") | buffer api/tests/sr_lobo.py | else | edit api/tests/sr_lobo.py | endif
let s:l = 954 - ((14 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
954
normal! 044|
wincmd w
argglobal
if bufexists("api/tests/ramanujan.py") | buffer api/tests/ramanujan.py | else | edit api/tests/ramanujan.py | endif
let s:l = 1423 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1423
normal! 075|
wincmd w
argglobal
if bufexists("api/tests/clouseau.py") | buffer api/tests/clouseau.py | else | edit api/tests/clouseau.py | endif
let s:l = 329 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
329
normal! 036|
wincmd w
argglobal
enew
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 22 + 57) / 115)
exe '2resize ' . ((&lines * 3 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 92 + 57) / 115)
exe '3resize ' . ((&lines * 8 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 92 + 57) / 115)
exe '4resize ' . ((&lines * 35 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 92 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 92 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 92 + 57) / 115)
exe '7resize ' . ((&lines * 2 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 92 + 57) / 115)
tabnext 1
badd +1 api/murano/connection.py
badd +1 ~/Geotexan/src/Geotex-INN/geotexan.vim
badd +0 api/murano/ops.py
badd +1 api/tests/sr_lobo.py
badd +1 api/tests/ramanujan.py
badd +1 api/tests/clouseau.py
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0
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
1resize 55|vert 1resize 22|2resize 3|vert 2resize 92|3resize 8|vert 3resize 92|4resize 35|vert 4resize 92|5resize 1|vert 5resize 92|6resize 1|vert 6resize 92|7resize 2|vert 7resize 92|
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
