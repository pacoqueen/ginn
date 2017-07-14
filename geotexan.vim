" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 14 julio 2017 at 18:33:30.
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
badd +1 formularios/partes_de_fabricacion_rollos.py
badd +169 api/murano/connection.py
badd +1 formularios/partes_de_fabricacion_bolsas.py
badd +861 informes/norma2013.py
badd +749 informes/sika.py
badd +0 ~/Geotexan/src/Geotex-INN/geotexan.vim
argglobal
silent! argdel *
argadd ~/Geotexan/src/Geotex-INN/geotexan.vim
edit formularios/partes_de_fabricacion_bolsas.py
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
exe 'vert 1resize ' . ((&columns * 20 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 96 + 58) / 117)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 96 + 58) / 117)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 96 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 96 + 58) / 117)
exe '6resize ' . ((&lines * 28 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 96 + 58) / 117)
exe '7resize ' . ((&lines * 4 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 96 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 96 + 58) / 117)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 96 + 58) / 117)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 96 + 58) / 117)
exe '11resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 11resize ' . ((&columns * 96 + 58) / 117)
exe '12resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 12resize ' . ((&columns * 96 + 58) / 117)
exe '13resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 13resize ' . ((&columns * 96 + 58) / 117)
exe '14resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 14resize ' . ((&columns * 96 + 58) / 117)
argglobal
enew
file __Tagbar__.1
wincmd w
argglobal
let s:l = 1696 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1696
normal! 042|
wincmd w
argglobal
enew
wincmd w
argglobal
edit formularios/partes_de_fabricacion_rollos.py
let s:l = 3106 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3106
normal! 050|
wincmd w
argglobal
enew
wincmd w
argglobal
edit api/tests/sr_lobo.py
let s:l = 105 - ((13 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
105
normal! 053|
wincmd w
argglobal
enew
wincmd w
argglobal
edit api/murano/ops.py
let s:l = 1826 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1826
normal! 026|
wincmd w
argglobal
enew
wincmd w
argglobal
edit formularios/partes_de_fabricacion_bolsas.py
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
enew
wincmd w
argglobal
edit formularios/partes_de_fabricacion_bolsas.py
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit formularios/partes_de_fabricacion_bolsas.py
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit formularios/partes_de_fabricacion_bolsas.py
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 20 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 96 + 58) / 117)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 96 + 58) / 117)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 96 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 96 + 58) / 117)
exe '6resize ' . ((&lines * 28 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 96 + 58) / 117)
exe '7resize ' . ((&lines * 4 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 96 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 8resize ' . ((&columns * 96 + 58) / 117)
exe '9resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 9resize ' . ((&columns * 96 + 58) / 117)
exe '10resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 10resize ' . ((&columns * 96 + 58) / 117)
exe '11resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 11resize ' . ((&columns * 96 + 58) / 117)
exe '12resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 12resize ' . ((&columns * 96 + 58) / 117)
exe '13resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 13resize ' . ((&columns * 96 + 58) / 117)
exe '14resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 14resize ' . ((&columns * 96 + 58) / 117)
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
11wincmd w
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
1resize 55|vert 1resize 20|2resize 1|vert 2resize 96|3resize 1|vert 3resize 96|4resize 1|vert 4resize 96|5resize 1|vert 5resize 96|6resize 28|vert 6resize 96|7resize 4|vert 7resize 96|8resize 1|vert 8resize 96|9resize 1|vert 9resize 96|10resize 1|vert 10resize 96|11resize 1|vert 11resize 96|12resize 1|vert 12resize 96|13resize 1|vert 13resize 96|14resize 1|vert 14resize 96|
6wincmd w
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
