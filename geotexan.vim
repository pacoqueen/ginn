" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 13 mayo 2013 at 16:56:00.
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
cd ~/Geotexan/src/Geotex-INN
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 formularios/auditviewer.py
badd +249 formularios/consulta_existenciasBolsas.py
badd +1 formularios/dynconsulta.py
badd +1 framework/pclases.py
badd +168 formularios/gestor_mensajes.py
badd +181 formularios/menu.py
badd +85 formularios/autenticacion.py
badd +1 formularios/dynconsulta.glade
badd +179 formularios/consulta_facturas_sin_doc_pago.py
badd +73 formularios/utils_almacen.py
badd +1 ginn/formularios/dynconsulta.glade
badd +10 ginn/formularios/dynconsulta.py
badd +9 ginn/framework/pclases.py
badd +43 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +39 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1 ginn/formularios/clientes.py
badd +1 ginn/formularios/productos_compra.py
badd +1 ginn/formularios/productos_de_venta_balas.py
badd +1 ginn/formularios/recibos.py
badd +483 ginn/formularios/productos_de_venta_rollos.py
badd +624 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +319 ginn/formularios/productos_de_venta_especial.py
args formularios/auditviewer.py
set lines=47 columns=80
edit ginn/formularios/recibos.py
set splitbelow splitright
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
3wincmd k
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 39 + 23) / 47)
exe '2resize ' . ((&lines * 1 + 23) / 47)
exe '3resize ' . ((&lines * 1 + 23) / 47)
exe '4resize ' . ((&lines * 1 + 23) / 47)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
53
silent! normal zo
99
silent! normal zo
100
silent! normal zo
102
silent! normal zo
102
silent! normal zo
100
silent! normal zo
99
silent! normal zo
53
silent! normal zo
let s:l = 607 - ((13 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
607
normal! 04l
wincmd w
argglobal
edit ginn/formularios/productos_de_venta_balas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit ginn/formularios/productos_compra.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
edit ginn/formularios/clientes.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
66
silent! normal zo
67
silent! normal zo
76
silent! normal zo
76
silent! normal zo
76
silent! normal zo
76
silent! normal zo
76
silent! normal zo
76
silent! normal zo
67
silent! normal zo
145
silent! normal zo
146
silent! normal zo
160
silent! normal zo
146
silent! normal zo
145
silent! normal zo
1260
silent! normal zo
1260
silent! normal zo
1626
silent! normal zo
1639
silent! normal zo
1639
silent! normal zo
1626
silent! normal zo
1687
silent! normal zo
1698
silent! normal zo
1698
silent! normal zo
1687
silent! normal zo
66
silent! normal zo
let s:l = 1363 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1363
normal! 019l
wincmd w
exe '1resize ' . ((&lines * 39 + 23) / 47)
exe '2resize ' . ((&lines * 1 + 23) / 47)
exe '3resize ' . ((&lines * 1 + 23) / 47)
exe '4resize ' . ((&lines * 1 + 23) / 47)
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
1wincmd w

" vim: ft=vim ro nowrap smc=128
