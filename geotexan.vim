" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 11 junio 2013 at 07:30:40.
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
badd +175 ~/.vimrc
badd +1 formularios/auditviewer.py
badd +13 ~/.vim/plugin/ack.vim
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
badd +14313 ginn/framework/pclases.py
badd +43 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +39 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1542 ginn/formularios/clientes.py
badd +314 ginn/formularios/productos_compra.py
badd +323 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2147 ginn/formularios/productos_de_venta_rollos.py
badd +643 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +305 ginn/formularios/productos_de_venta_especial.py
badd +3998 ginn/formularios/partes_de_fabricacion_balas.py
badd +1927 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +961 ginn/formularios/partes_de_fabricacion_rollos.py
badd +669 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +1 ginn/formularios/launcher.py
badd +492 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +833 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1502 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +371 ginn/formularios/facturas_venta.py
badd +1 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +13 ginn/main.py
badd +1 ginn/formularios/ventana.py
badd +2545 ginn/formularios/pedidos_de_venta.py
badd +1 db/tablas.sql
args formularios/auditviewer.py
set lines=59 columns=80
edit db/tablas.sql
set splitbelow splitright
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
7wincmd k
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
exe '1resize ' . ((&lines * 1 + 29) / 59)
exe '2resize ' . ((&lines * 9 + 29) / 59)
exe '3resize ' . ((&lines * 1 + 29) / 59)
exe '4resize ' . ((&lines * 1 + 29) / 59)
exe '5resize ' . ((&lines * 1 + 29) / 59)
exe '6resize ' . ((&lines * 22 + 29) / 59)
exe '7resize ' . ((&lines * 1 + 29) / 59)
exe '8resize ' . ((&lines * 14 + 29) / 59)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
286
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
292
normal! zo
845
normal! zo
1322
normal! zo
1359
normal! zo
1359
normal! zo
1359
normal! zo
1359
normal! zo
1359
normal! zo
1359
normal! zo
1359
normal! zo
1376
normal! zo
1412
normal! zo
let s:l = 292 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
292
normal! 013|
wincmd w
argglobal
edit ginn/framework/pclases.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
6381
normal! zo
6641
normal! zo
6649
normal! zo
7421
normal! zo
7427
normal! zo
9634
normal! zo
9670
normal! zo
9678
normal! zo
9681
normal! zo
9685
normal! zo
9718
normal! zo
19483
normal! zo
let s:l = 19491 - ((7 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19491
normal! 046|
wincmd w
argglobal
edit ginn/framework/configuracion.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
71
normal! zo
408
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
417
normal! zo
434
normal! zo
434
normal! zo
434
normal! zo
446
normal! zo
461
normal! zo
480
normal! zo
let s:l = 464 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
464
normal! 05|
wincmd w
argglobal
edit ginn/main.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 10 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10
normal! 049|
wincmd w
argglobal
edit ginn/formularios/ventana.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
41
normal! zo
67
normal! zo
68
normal! zo
68
normal! zo
273
normal! zo
338
normal! zo
381
normal! zo
559
normal! zo
638
normal! zo
638
normal! zo
638
normal! zo
638
normal! zo
676
normal! zo
677
normal! zo
906
normal! zo
912
normal! zo
let s:l = 85 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
85
normal! 024|
wincmd w
argglobal
edit ginn/formularios/pedidos_de_venta.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
121
normal! zo
122
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
173
normal! zo
187
normal! zo
193
normal! zo
193
normal! zo
194
normal! zo
198
normal! zo
204
normal! zo
205
normal! zo
213
normal! zo
215
normal! zo
226
normal! zo
394
normal! zo
402
normal! zo
521
normal! zo
583
normal! zo
604
normal! zo
718
normal! zo
718
normal! zo
902
normal! zo
910
normal! zo
913
normal! zo
915
normal! zo
922
normal! zo
923
normal! zo
945
normal! zo
997
normal! zo
1006
normal! zo
1007
normal! zo
1007
normal! zo
1007
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1014
normal! zo
1029
normal! zo
1228
normal! zo
1229
normal! zo
1232
normal! zo
1249
normal! zo
1255
normal! zo
1269
normal! zo
1279
normal! zo
1323
normal! zo
1335
normal! zo
1640
normal! zo
1698
normal! zo
1713
normal! zo
1728
normal! zo
1754
normal! zo
2061
normal! zo
2293
normal! zo
2302
normal! zo
2307
normal! zo
2320
normal! zo
2339
normal! zo
2356
normal! zo
2425
normal! zo
2425
normal! zo
2425
normal! zo
2425
normal! zo
2430
normal! zo
2457
normal! zo
2462
normal! zo
2464
normal! zo
2465
normal! zo
2497
normal! zo
2511
normal! zo
2511
normal! zo
2511
normal! zo
2511
normal! zo
2511
normal! zo
2511
normal! zo
2511
normal! zo
let s:l = 185 - ((14 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
185
normal! 0124|
wincmd w
argglobal
edit ginn/main.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
4
normal! zo
let s:l = 5 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5
normal! 018|
wincmd w
argglobal
edit ginn/formularios/launcher.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
33
normal! zo
48
normal! zo
69
normal! zo
let s:l = 56 - ((1 * winheight(0) + 7) / 14)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
56
normal! 024|
wincmd w
6wincmd w
exe '1resize ' . ((&lines * 1 + 29) / 59)
exe '2resize ' . ((&lines * 9 + 29) / 59)
exe '3resize ' . ((&lines * 1 + 29) / 59)
exe '4resize ' . ((&lines * 1 + 29) / 59)
exe '5resize ' . ((&lines * 1 + 29) / 59)
exe '6resize ' . ((&lines * 22 + 29) / 59)
exe '7resize ' . ((&lines * 1 + 29) / 59)
exe '8resize ' . ((&lines * 14 + 29) / 59)
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
6wincmd w

" vim: ft=vim ro nowrap smc=128
