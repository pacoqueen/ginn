" ~/Geotexan/src/ginn/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 08 abril 2013 at 11:58:07.
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
badd +1 framework/pclases.py
badd +168 formularios/gestor_mensajes.py
badd +181 formularios/menu.py
badd +85 formularios/autenticacion.py
badd +1 formularios/dynconsulta.glade
badd +179 formularios/consulta_facturas_sin_doc_pago.py
badd +73 formularios/utils_almacen.py
args formularios/auditviewer.py
set lines=47 columns=80
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
exe '1resize ' . ((&lines * 21 + 23) / 47)
exe '2resize ' . ((&lines * 23 + 23) / 47)
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
816
silent! normal zo
825
silent! normal zo
825
silent! normal zo
816
silent! normal zo
2651
silent! normal zo
2662
silent! normal zo
2651
silent! normal zo
2727
silent! normal zo
2740
silent! normal zo
2727
silent! normal zo
3211
silent! normal zo
3350
silent! normal zo
3352
silent! normal zo
3352
silent! normal zo
3350
silent! normal zo
3211
silent! normal zo
3371
silent! normal zo
3380
silent! normal zo
3371
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
6313
silent! normal zo
6458
silent! normal zo
6479
silent! normal zo
6480
silent! normal zo
6480
silent! normal zo
6480
silent! normal zo
6480
silent! normal zo
6486
silent! normal zo
6487
silent! normal zo
6491
silent! normal zo
6492
silent! normal zo
6496
silent! normal zo
6491
silent! normal zo
6486
silent! normal zo
6479
silent! normal zo
6458
silent! normal zo
6313
silent! normal zo
6672
silent! normal zo
6738
silent! normal zo
6672
silent! normal zo
7374
silent! normal zo
7409
silent! normal zo
7409
silent! normal zo
7374
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
15509
silent! normal zo
15514
silent! normal zo
15514
silent! normal zo
15948
silent! normal zo
15953
silent! normal zo
15953
silent! normal zo
15953
silent! normal zo
15958
silent! normal zo
15958
silent! normal zo
15948
silent! normal zo
15509
silent! normal zo
16236
silent! normal zo
16262
silent! normal zo
16262
silent! normal zo
16236
silent! normal zo
18457
silent! normal zo
18513
silent! normal zo
18519
silent! normal zo
18520
silent! normal zo
18519
silent! normal zo
18513
silent! normal zo
18524
silent! normal zo
18524
silent! normal zo
18457
silent! normal zo
19296
silent! normal zo
19326
silent! normal zo
19326
silent! normal zo
19346
silent! normal zo
19296
silent! normal zo
20861
silent! normal zo
20870
silent! normal zo
20871
silent! normal zo
20871
silent! normal zo
20871
silent! normal zo
20870
silent! normal zo
20861
silent! normal zo
let s:l = 19294 - ((8 * winheight(0) + 10) / 21)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19294
normal! 0
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
let s:l = 294 - ((9 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
294
normal! 015l
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 21 + 23) / 47)
exe '2resize ' . ((&lines * 23 + 23) / 47)
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
