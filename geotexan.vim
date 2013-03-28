" ~/Geotexan/src/ginn/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 28 marzo 2013 at 20:29:48.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Droid\ Sans\ Mono\ Slashed\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'desert' | colorscheme desert | endif
call setqflist([])
let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Geotexan/src/ginn
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +181 formularios/auditviewer.py
badd +249 formularios/consulta_existenciasBolsas.py
badd +1403 formularios/dynconsulta.py
badd +19344 framework/pclases.py
badd +168 formularios/gestor_mensajes.py
badd +181 formularios/menu.py
badd +85 formularios/autenticacion.py
badd +1 formularios/dynconsulta.glade
args formularios/auditviewer.py
set lines=46 columns=80
edit framework/pclases.py
set splitbelow splitright
wincmd _ | wincmd |
split
1wincmd k
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 22 + 23) / 46)
exe '2resize ' . ((&lines * 21 + 23) / 46)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
210
silent! normal zo
356
silent! normal zo
365
silent! normal zo
368
silent! normal zo
368
silent! normal zo
365
silent! normal zo
356
silent! normal zo
376
silent! normal zo
379
silent! normal zo
380
silent! normal zo
379
silent! normal zo
384
silent! normal zo
392
silent! normal zo
376
silent! normal zo
210
silent! normal zo
818
silent! normal zo
827
silent! normal zo
827
silent! normal zo
818
silent! normal zo
2653
silent! normal zo
2664
silent! normal zo
2653
silent! normal zo
2729
silent! normal zo
2742
silent! normal zo
2729
silent! normal zo
3373
silent! normal zo
3382
silent! normal zo
3373
silent! normal zo
4661
silent! normal zo
4753
silent! normal zo
4753
silent! normal zo
4780
silent! normal zo
4780
silent! normal zo
4661
silent! normal zo
6314
silent! normal zo
6459
silent! normal zo
6480
silent! normal zo
6487
silent! normal zo
6492
silent! normal zo
6497
silent! normal zo
6492
silent! normal zo
6487
silent! normal zo
6480
silent! normal zo
6459
silent! normal zo
6314
silent! normal zo
6673
silent! normal zo
6739
silent! normal zo
6673
silent! normal zo
7375
silent! normal zo
7410
silent! normal zo
7410
silent! normal zo
7375
silent! normal zo
9983
silent! normal zo
9983
silent! normal zo
10181
silent! normal zo
10181
silent! normal zo
10238
silent! normal zo
10323
silent! normal zo
10323
silent! normal zo
10238
silent! normal zo
19303
silent! normal zo
19333
silent! normal zo
19346
silent! normal zo
19348
silent! normal zo
19346
silent! normal zo
19333
silent! normal zo
19303
silent! normal zo
20865
silent! normal zo
20874
silent! normal zo
20874
silent! normal zo
20865
silent! normal zo
let s:l = 19349 - ((16 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19349
normal! 023l
wincmd w
argglobal
edit formularios/dynconsulta.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 10) / 21)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 22 + 23) / 46)
exe '2resize ' . ((&lines * 21 + 23) / 46)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
tabnext 1
2wincmd w

" vim: ft=vim ro nowrap smc=128
