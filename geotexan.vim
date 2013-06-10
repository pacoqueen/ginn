" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 10 junio 2013 at 22:53:17.
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
badd +0 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +13 ginn/main.py
badd +0 ginn/formularios/ventana.py
badd +2545 ginn/formularios/pedidos_de_venta.py
badd +0 db/tablas.sql
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
exe '2resize ' . ((&lines * 21 + 29) / 59)
exe '3resize ' . ((&lines * 1 + 29) / 59)
exe '4resize ' . ((&lines * 1 + 29) / 59)
exe '5resize ' . ((&lines * 1 + 29) / 59)
exe '6resize ' . ((&lines * 17 + 29) / 59)
exe '7resize ' . ((&lines * 2 + 29) / 59)
exe '8resize ' . ((&lines * 6 + 29) / 59)
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
1373
normal! zo
let s:l = 293 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
293
normal! 0134|
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
6639
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
let s:l = 9671 - ((0 * winheight(0) + 10) / 21)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9671
normal! 05|
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
174
normal! zo
178
normal! zo
178
normal! zo
179
normal! zo
184
normal! zo
184
normal! zo
351
normal! zo
359
normal! zo
478
normal! zo
540
normal! zo
561
normal! zo
675
normal! zo
675
normal! zo
859
normal! zo
867
normal! zo
870
normal! zo
872
normal! zo
879
normal! zo
880
normal! zo
902
normal! zo
954
normal! zo
963
normal! zo
964
normal! zo
964
normal! zo
964
normal! zo
971
normal! zo
971
normal! zo
971
normal! zo
971
normal! zo
971
normal! zo
971
normal! zo
971
normal! zo
971
normal! zo
986
normal! zo
1103
normal! zo
1109
normal! zo
1115
normal! zo
1117
normal! zo
1120
normal! zo
1207
normal! zo
1208
normal! zo
1211
normal! zo
1228
normal! zo
1234
normal! zo
1248
normal! zo
1258
normal! zo
1302
normal! zo
1314
normal! zo
1619
normal! zo
1677
normal! zo
1692
normal! zo
1707
normal! zo
1733
normal! zo
2040
normal! zo
2272
normal! zo
2281
normal! zo
2286
normal! zo
2299
normal! zo
2318
normal! zo
2335
normal! zo
2404
normal! zo
2409
normal! zo
2436
normal! zo
2441
normal! zo
2443
normal! zo
2444
normal! zo
2476
normal! zo
2490
normal! zo
2490
normal! zo
2490
normal! zo
2490
normal! zo
2490
normal! zo
2490
normal! zo
2490
normal! zo
let s:l = 1113 - ((7 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1113
normal! 0336|
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
let s:l = 4 - ((0 * winheight(0) + 1) / 2)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4
normal! 027|
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
let s:l = 58 - ((2 * winheight(0) + 3) / 6)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
58
normal! 055|
wincmd w
6wincmd w
exe '1resize ' . ((&lines * 1 + 29) / 59)
exe '2resize ' . ((&lines * 21 + 29) / 59)
exe '3resize ' . ((&lines * 1 + 29) / 59)
exe '4resize ' . ((&lines * 1 + 29) / 59)
exe '5resize ' . ((&lines * 1 + 29) / 59)
exe '6resize ' . ((&lines * 17 + 29) / 59)
exe '7resize ' . ((&lines * 2 + 29) / 59)
exe '8resize ' . ((&lines * 6 + 29) / 59)
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
