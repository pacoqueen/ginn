" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 11 junio 2013 at 17:13:32.
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
badd +109 ginn/framework/pclases.py
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
badd +68 ginn/formularios/launcher.py
badd +492 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +977 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1502 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +371 ginn/formularios/facturas_venta.py
badd +468 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +570 ginn/formularios/ventana.py
badd +258 ginn/formularios/pedidos_de_venta.py
badd +867 db/tablas.sql
args formularios/auditviewer.py
set lines=44 columns=80
edit ginn/framework/pclases.py
set splitbelow splitright
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
exe '1resize ' . ((&lines * 14 + 22) / 44)
exe '2resize ' . ((&lines * 13 + 22) / 44)
exe '3resize ' . ((&lines * 13 + 22) / 44)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
263
silent! normal zo
6390
silent! normal zo
6650
silent! normal zo
6658
silent! normal zo
7430
silent! normal zo
7436
silent! normal zo
9643
silent! normal zo
9679
silent! normal zo
9687
silent! normal zo
9690
silent! normal zo
9694
silent! normal zo
9696
silent! normal zo
9728
silent! normal zo
19493
silent! normal zo
19579
silent! normal zo
21080
silent! normal zo
21102
silent! normal zo
21136
silent! normal zo
21168
silent! normal zo
let s:l = 9696 - ((12 * winheight(0) + 7) / 14)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9696
normal! 019l
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
silent! normal zo
67
silent! normal zo
68
silent! normal zo
68
silent! normal zo
275
silent! normal zo
340
silent! normal zo
383
silent! normal zo
561
silent! normal zo
569
silent! normal zo
595
silent! normal zo
612
silent! normal zo
640
silent! normal zo
640
silent! normal zo
640
silent! normal zo
640
silent! normal zo
678
silent! normal zo
679
silent! normal zo
807
silent! normal zo
818
silent! normal zo
879
silent! normal zo
908
silent! normal zo
914
silent! normal zo
1039
silent! normal zo
let s:l = 823 - ((8 * winheight(0) + 6) / 13)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
823
normal! 044l
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
95
silent! normal zo
102
silent! normal zo
102
silent! normal zo
121
silent! normal zo
122
silent! normal zo
135
silent! normal zo
135
silent! normal zo
135
silent! normal zo
145
silent! normal zo
174
silent! normal zo
189
silent! normal zo
191
silent! normal zo
191
silent! normal zo
191
silent! normal zo
191
silent! normal zo
191
silent! normal zo
197
silent! normal zo
209
silent! normal zo
209
silent! normal zo
210
silent! normal zo
213
silent! normal zo
235
silent! normal zo
242
silent! normal zo
242
silent! normal zo
242
silent! normal zo
242
silent! normal zo
242
silent! normal zo
245
silent! normal zo
247
silent! normal zo
257
silent! normal zo
260
silent! normal zo
280
silent! normal zo
296
silent! normal zo
298
silent! normal zo
315
silent! normal zo
322
silent! normal zo
355
silent! normal zo
357
silent! normal zo
444
silent! normal zo
448
silent! normal zo
453
silent! normal zo
465
silent! normal zo
473
silent! normal zo
592
silent! normal zo
654
silent! normal zo
675
silent! normal zo
710
silent! normal zo
710
silent! normal zo
743
silent! normal zo
743
silent! normal zo
789
silent! normal zo
789
silent! normal zo
973
silent! normal zo
981
silent! normal zo
984
silent! normal zo
986
silent! normal zo
993
silent! normal zo
994
silent! normal zo
1016
silent! normal zo
1050
silent! normal zo
1068
silent! normal zo
1077
silent! normal zo
1078
silent! normal zo
1078
silent! normal zo
1078
silent! normal zo
1085
silent! normal zo
1085
silent! normal zo
1085
silent! normal zo
1085
silent! normal zo
1085
silent! normal zo
1085
silent! normal zo
1085
silent! normal zo
1085
silent! normal zo
1100
silent! normal zo
1224
silent! normal zo
1273
silent! normal zo
1317
silent! normal zo
1318
silent! normal zo
1321
silent! normal zo
1338
silent! normal zo
1344
silent! normal zo
1358
silent! normal zo
1368
silent! normal zo
1412
silent! normal zo
1424
silent! normal zo
1729
silent! normal zo
1781
silent! normal zo
1781
silent! normal zo
1781
silent! normal zo
1787
silent! normal zo
1802
silent! normal zo
1817
silent! normal zo
1843
silent! normal zo
1855
silent! normal zo
1856
silent! normal zo
1856
silent! normal zo
1857
silent! normal zo
1878
silent! normal zo
1921
silent! normal zo
1924
silent! normal zo
2057
silent! normal zo
2070
silent! normal zo
2078
silent! normal zo
2122
silent! normal zo
2139
silent! normal zo
2149
silent! normal zo
2151
silent! normal zo
2152
silent! normal zo
2160
silent! normal zo
2392
silent! normal zo
2401
silent! normal zo
2406
silent! normal zo
2419
silent! normal zo
2438
silent! normal zo
2455
silent! normal zo
2524
silent! normal zo
2524
silent! normal zo
2524
silent! normal zo
2524
silent! normal zo
2525
silent! normal zo
2529
silent! normal zo
2556
silent! normal zo
2561
silent! normal zo
2563
silent! normal zo
2564
silent! normal zo
2596
silent! normal zo
2610
silent! normal zo
2610
silent! normal zo
2610
silent! normal zo
2610
silent! normal zo
2610
silent! normal zo
2610
silent! normal zo
2610
silent! normal zo
let s:l = 1760 - ((6 * winheight(0) + 6) / 13)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1760
normal! 025l
wincmd w
exe '1resize ' . ((&lines * 14 + 22) / 44)
exe '2resize ' . ((&lines * 13 + 22) / 44)
exe '3resize ' . ((&lines * 13 + 22) / 44)
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
