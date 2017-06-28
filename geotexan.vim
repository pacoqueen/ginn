" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 28 junio 2017 at 10:26:07.
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
badd +25 api/tests/clouseau.py
badd +39 api/tests/ramanujan.py
badd +39 api/murano/ops.py
badd +17 api/tests/sr_lobo.py
badd +1 ~/Geotexan/src/Geotex-INN/geotexan.vim
badd +3045 formularios/partes_de_fabricacion_rollos.py
badd +169 api/murano/connection.py
badd +2671 formularios/partes_de_fabricacion_balas.py
badd +1725 formularios/partes_de_fabricacion_bolsas.py
badd +4024 framework/pclases/__init__.py
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
2wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 24 + 58) / 117)
exe '2resize ' . ((&lines * 20 + 32) / 65)
exe 'vert 2resize ' . ((&columns * 92 + 58) / 117)
exe '3resize ' . ((&lines * 37 + 32) / 65)
exe 'vert 3resize ' . ((&columns * 92 + 58) / 117)
exe '4resize ' . ((&lines * 4 + 32) / 65)
exe 'vert 4resize ' . ((&columns * 92 + 58) / 117)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 573 - ((13 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
573
normal! 029|
wincmd w
argglobal
edit api/murano/ops.py
let s:l = 2562 - ((18 * winheight(0) + 18) / 37)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2562
normal! 05|
wincmd w
argglobal
edit framework/pclases/__init__.py
let s:l = 4789 - ((1 * winheight(0) + 2) / 4)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4789
normal! 032|
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 24 + 58) / 117)
exe '2resize ' . ((&lines * 20 + 32) / 65)
exe 'vert 2resize ' . ((&columns * 92 + 58) / 117)
exe '3resize ' . ((&lines * 37 + 32) / 65)
exe 'vert 3resize ' . ((&columns * 92 + 58) / 117)
exe '4resize ' . ((&lines * 4 + 32) / 65)
exe 'vert 4resize ' . ((&columns * 92 + 58) / 117)
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

3wincmd w
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
