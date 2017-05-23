" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 23 mayo 2017 at 13:36:17.
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
badd +1 api/tests/clouseau.py
badd +421 api/tests/ramanujan.py
badd +1 api/murano/ops.py
badd +679 informes/norma2013.py
badd +1 api/tests/sr_lobo.py
badd +1 ~/Geotexan/src/Geotex-INN/geotexan.vim
badd +740 formularios/consumo_balas_partida.py
badd +5500 framework/pclases/__init__.py
argglobal
silent! argdel *
argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit api/tests/clouseau.py
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
4wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 9 + 49) / 98)
exe '2resize ' . ((&lines * 10 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 88 + 49) / 98)
exe '3resize ' . ((&lines * 9 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 88 + 49) / 98)
exe '4resize ' . ((&lines * 9 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 88 + 49) / 98)
exe '5resize ' . ((&lines * 9 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 88 + 49) / 98)
exe '6resize ' . ((&lines * 9 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 88 + 49) / 98)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 141 - ((6 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
141
normal! 032|
wincmd w
argglobal
edit api/murano/ops.py
let s:l = 3 - ((2 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3
normal! 0
wincmd w
argglobal
enew
wincmd w
argglobal
edit api/tests/ramanujan.py
let s:l = 118 - ((0 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
118
normal! 05|
wincmd w
argglobal
edit api/tests/sr_lobo.py
let s:l = 15 - ((0 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15
normal! 022|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 9 + 49) / 98)
exe '2resize ' . ((&lines * 10 + 26) / 52)
exe 'vert 2resize ' . ((&columns * 88 + 49) / 98)
exe '3resize ' . ((&lines * 9 + 26) / 52)
exe 'vert 3resize ' . ((&columns * 88 + 49) / 98)
exe '4resize ' . ((&lines * 9 + 26) / 52)
exe 'vert 4resize ' . ((&columns * 88 + 49) / 98)
exe '5resize ' . ((&lines * 9 + 26) / 52)
exe 'vert 5resize ' . ((&columns * 88 + 49) / 98)
exe '6resize ' . ((&lines * 9 + 26) / 52)
exe 'vert 6resize ' . ((&columns * 88 + 49) / 98)
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
