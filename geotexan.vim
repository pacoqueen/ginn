" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 22 enero 2019 at 09:09:44.
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
call setqflist([{'lnum': 54, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'framework/metrics/core.py', 'text': 'E501: line too long (97 > 79 characters)'}, {'lnum': 80, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'framework/metrics/core.py', 'text': 'E501: line too long (97 > 79 characters)'}, {'lnum': 107, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'framework/metrics/core.py', 'text': 'E501: line too long (97 > 79 characters)'}, {'lnum': 133, 'col': 80, 'pattern': '', 'valid': 1, 'vcol': 0, 'nr': -1, 'type': 'E', 'module': '', 'filename': 'framework/metrics/core.py', 'text': 'E501: line too long (97 > 79 characters)'}])
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
badd +1 api/netdata/ginn.chart.py
badd +1 ~/Geotexan/src/Geotex-INN/geotexan.vim
badd +947 formularios/menu.py
badd +1 api/murano/ops.py
badd +1 api/tests/efcodd.py
badd +1 framework/metrics/__init__.py
badd +1 framework/metrics/core.py
badd +1 framework/metrics/tests.py
argglobal
silent! argdel *
$argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit api/tests/efcodd.py
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
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 1 + 52) / 105)
exe '2resize ' . ((&lines * 8 + 26) / 53)
exe 'vert 2resize ' . ((&columns * 103 + 52) / 105)
exe '3resize ' . ((&lines * 7 + 26) / 53)
exe 'vert 3resize ' . ((&columns * 103 + 52) / 105)
exe '4resize ' . ((&lines * 7 + 26) / 53)
exe 'vert 4resize ' . ((&columns * 103 + 52) / 105)
exe '5resize ' . ((&lines * 7 + 26) / 53)
exe 'vert 5resize ' . ((&columns * 103 + 52) / 105)
exe '6resize ' . ((&lines * 8 + 26) / 53)
exe 'vert 6resize ' . ((&columns * 103 + 52) / 105)
exe '7resize ' . ((&lines * 7 + 26) / 53)
exe 'vert 7resize ' . ((&columns * 103 + 52) / 105)
exe '8resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 8resize ' . ((&columns * 103 + 52) / 105)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 230 - ((3 * winheight(0) + 4) / 8)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
230
normal! 010|
wincmd w
argglobal
if bufexists('framework/metrics/tests.py') | buffer framework/metrics/tests.py | else | edit framework/metrics/tests.py | endif
let s:l = 47 - ((0 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
47
normal! 037|
wincmd w
argglobal
if bufexists('api/netdata/ginn.chart.py') | buffer api/netdata/ginn.chart.py | else | edit api/netdata/ginn.chart.py | endif
let s:l = 143 - ((0 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
143
normal! 057|
wincmd w
argglobal
if bufexists('framework/metrics/core.py') | buffer framework/metrics/core.py | else | edit framework/metrics/core.py | endif
let s:l = 31 - ((3 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 0
wincmd w
argglobal
if bufexists('framework/metrics/__init__.py') | buffer framework/metrics/__init__.py | else | edit framework/metrics/__init__.py | endif
let s:l = 22 - ((3 * winheight(0) + 4) / 8)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 0
wincmd w
argglobal
if bufexists('api/murano/ops.py') | buffer api/murano/ops.py | else | edit api/murano/ops.py | endif
let s:l = 1655 - ((1 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1655
normal! 013|
wincmd w
argglobal
enew
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 1 + 52) / 105)
exe '2resize ' . ((&lines * 8 + 26) / 53)
exe 'vert 2resize ' . ((&columns * 103 + 52) / 105)
exe '3resize ' . ((&lines * 7 + 26) / 53)
exe 'vert 3resize ' . ((&columns * 103 + 52) / 105)
exe '4resize ' . ((&lines * 7 + 26) / 53)
exe 'vert 4resize ' . ((&columns * 103 + 52) / 105)
exe '5resize ' . ((&lines * 7 + 26) / 53)
exe 'vert 5resize ' . ((&columns * 103 + 52) / 105)
exe '6resize ' . ((&lines * 8 + 26) / 53)
exe 'vert 6resize ' . ((&columns * 103 + 52) / 105)
exe '7resize ' . ((&lines * 7 + 26) / 53)
exe 'vert 7resize ' . ((&columns * 103 + 52) / 105)
exe '8resize ' . ((&lines * 1 + 26) / 53)
exe 'vert 8resize ' . ((&columns * 103 + 52) / 105)
tabnext 1
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
1resize 51|vert 1resize 1|2resize 8|vert 2resize 103|3resize 7|vert 3resize 103|4resize 7|vert 4resize 103|5resize 7|vert 5resize 103|6resize 8|vert 6resize 103|7resize 7|vert 7resize 103|8resize 1|vert 8resize 103|
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
