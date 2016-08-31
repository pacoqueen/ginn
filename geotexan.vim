" ~/Geotexan/src/Geotex-INN/geotexan.vim:
" Vim session script.
" Created by session.vim 2.13.1 on 30 agosto 2016 at 20:44:55.
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
call setqflist([])
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
badd +1 ginn/api/murano/ops.py
badd +1 ginn/api/tests/sr_lobo.py
badd +1 ginn/api/murano/connection.py
badd +80 ginn/api/tests/dump_existencias.py
badd +45 ginn/api/tests/murano_exportar.py
badd +61 ginn/api/murano/export.py
badd +1 ginn/api/murano/extra.py
argglobal
silent! argdel *
edit ginn/api/murano/extra.py
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
exe 'vert 1resize ' . ((&columns * 22 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 94 + 58) / 117)
exe '3resize ' . ((&lines * 24 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 94 + 58) / 117)
exe '4resize ' . ((&lines * 10 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 94 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 94 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 94 + 58) / 117)
exe '7resize ' . ((&lines * 4 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 94 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 8resize ' . ((&columns * 94 + 58) / 117)
exe '9resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 9resize ' . ((&columns * 94 + 58) / 117)
exe '10resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 10resize ' . ((&columns * 94 + 58) / 117)
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
let s:l = 192 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
192
normal! 011|
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
let s:l = 2071 - ((21 * winheight(0) + 12) / 24)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2071
normal! 05|
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
let s:l = 14 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
14
normal! 0
wincmd w
argglobal
edit ginn/api/tests/sr_lobo.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 169 - ((1 * winheight(0) + 2) / 4)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
169
normal! 030|
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
let s:l = 12 - ((1 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
12
normal! 010|
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
3wincmd w
exe 'vert 1resize ' . ((&columns * 22 + 58) / 117)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 94 + 58) / 117)
exe '3resize ' . ((&lines * 24 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 94 + 58) / 117)
exe '4resize ' . ((&lines * 10 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 94 + 58) / 117)
exe '5resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 94 + 58) / 117)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 94 + 58) / 117)
exe '7resize ' . ((&lines * 4 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 94 + 58) / 117)
exe '8resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 8resize ' . ((&columns * 94 + 58) / 117)
exe '9resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 9resize ' . ((&columns * 94 + 58) / 117)
exe '10resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 10resize ' . ((&columns * 94 + 58) / 117)
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

4wincmd w
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
1resize 52|vert 1resize 22|2resize 1|vert 2resize 94|3resize 24|vert 3resize 94|4resize 10|vert 4resize 94|5resize 1|vert 5resize 94|6resize 1|vert 6resize 94|7resize 4|vert 7resize 94|8resize 1|vert 8resize 94|9resize 1|vert 9resize 94|10resize 1|vert 10resize 94|
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
