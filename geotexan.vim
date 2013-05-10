" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 10 mayo 2013 at 13:10:31.
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
badd +0 ginn/formularios/abonos_venta.py
badd +79 ginn/formularios/trazabilidad.py
badd +1244 ginn/formularios/clientes.py
args formularios/auditviewer.py
set lines=47 columns=80
edit ginn/framework/pclases.py
set splitbelow splitright
wincmd _ | wincmd |
split
1wincmd k
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 22 + 23) / 47)
exe '2resize ' . ((&lines * 22 + 23) / 47)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
19402
silent! normal zo
19415
silent! normal zo
19420
silent! normal zo
19421
silent! normal zo
19423
silent! normal zo
19425
silent! normal zo
19427
silent! normal zo
19429
silent! normal zo
19423
silent! normal zo
19430
silent! normal zo
19420
silent! normal zo
19432
silent! normal zo
19415
silent! normal zo
19402
silent! normal zo
let s:l = 19425 - ((13 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19425
normal! 041l
wincmd w
argglobal
edit ginn/formularios/abonos_venta.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
57
silent! normal zo
58
silent! normal zo
66
silent! normal zo
66
silent! normal zo
66
silent! normal zo
66
silent! normal zo
66
silent! normal zo
58
silent! normal zo
120
silent! normal zo
120
silent! normal zo
176
silent! normal zo
184
silent! normal zo
184
silent! normal zo
184
silent! normal zo
184
silent! normal zo
184
silent! normal zo
184
silent! normal zo
184
silent! normal zo
184
silent! normal zo
184
silent! normal zo
189
silent! normal zo
195
silent! normal zo
197
silent! normal zo
195
silent! normal zo
176
silent! normal zo
216
silent! normal zo
216
silent! normal zo
515
silent! normal zo
515
silent! normal zo
529
silent! normal zo
529
silent! normal zo
546
silent! normal zo
546
silent! normal zo
560
silent! normal zo
560
silent! normal zo
576
silent! normal zo
576
silent! normal zo
588
silent! normal zo
588
silent! normal zo
625
silent! normal zo
642
silent! normal zo
644
silent! normal zo
646
silent! normal zo
646
silent! normal zo
644
silent! normal zo
642
silent! normal zo
625
silent! normal zo
714
silent! normal zo
726
silent! normal zo
726
silent! normal zo
714
silent! normal zo
740
silent! normal zo
752
silent! normal zo
752
silent! normal zo
740
silent! normal zo
768
silent! normal zo
785
silent! normal zo
789
silent! normal zo
793
silent! normal zo
800
silent! normal zo
800
silent! normal zo
793
silent! normal zo
789
silent! normal zo
785
silent! normal zo
818
silent! normal zo
828
silent! normal zo
831
silent! normal zo
831
silent! normal zo
828
silent! normal zo
818
silent! normal zo
768
silent! normal zo
923
silent! normal zo
932
silent! normal zo
923
silent! normal zo
941
silent! normal zo
941
silent! normal zo
986
silent! normal zo
997
silent! normal zo
997
silent! normal zo
986
silent! normal zo
1052
silent! normal zo
1052
silent! normal zo
1396
silent! normal zo
1396
silent! normal zo
57
silent! normal zo
1444
silent! normal zo
let s:l = 194 - ((15 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
194
normal! 029l
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 22 + 23) / 47)
exe '2resize ' . ((&lines * 22 + 23) / 47)
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
