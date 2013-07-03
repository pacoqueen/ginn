" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 02 julio 2013 at 15:07:25.
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
badd +279 ginn/formularios/dynconsulta.py
badd +77 ginn/framework/pclases.py
badd +201 ginn/formularios/historico_existencias_compra.py
badd +39 ginn/formularios/historico_existencias.py
badd +46 ginn/formularios/consulta_incidencias.py
badd +392 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +2031 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +638 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +864 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1604 ginn/formularios/partes_de_fabricacion_balas.py
badd +197 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +117 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +109 ginn/formularios/launcher.py
badd +155 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +178 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +7583 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1 ginn/formularios/facturas_venta.py
badd +468 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +89 ginn/formularios/ventana.py
badd +2286 ginn/formularios/pedidos_de_venta.py
badd +1 db/tablas.sql
badd +412 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +359 ginn/formularios/presupuestos.py
badd +412 ginn/informes/presupuesto2.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +1359 ginn/formularios/facturas_compra.py
badd +1923 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +1228 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +416 ginn/formularios/pagares_pagos.py
badd +509 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +47 ginn/formularios/gtkexcepthook.py
badd +512 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +49 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +1 ginn/formularios/consulta_vencimientos_pago.py
badd +1 ginn/formularios/trazabilidad.py
badd +0 ginn/framework/pclases/__init__.py
badd +0 ginn/framework/pclases/superfacturaventa.py
badd +0 ginn/framework/pclases/facturaventa.py
args formularios/auditviewer.py
set lines=58 columns=111
edit db/tablas.sql
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
10wincmd k
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
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 9 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 16 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 13 + 29) / 58)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
exe '12resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 12resize ' . ((&columns * 80 + 55) / 111)
argglobal
enew
file __Tag_List__
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=9999
setlocal fml=0
setlocal fdn=20
setlocal fen
wincmd w
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
1934
silent! normal zo
2124
silent! normal zo
2322
silent! normal zo
2499
silent! normal zo
2557
silent! normal zo
3084
silent! normal zo
3399
silent! normal zo
3399
silent! normal zo
3399
silent! normal zo
3399
silent! normal zo
3399
silent! normal zo
3399
silent! normal zo
3399
silent! normal zo
3412
silent! normal zo
3418
silent! normal zo
3422
silent! normal zo
3488
silent! normal zo
3488
silent! normal zo
3488
silent! normal zo
3488
silent! normal zo
3488
silent! normal zo
3488
silent! normal zo
3488
silent! normal zo
3488
silent! normal zo
3493
silent! normal zo
3500
silent! normal zo
3500
silent! normal zo
3500
silent! normal zo
3500
silent! normal zo
3500
silent! normal zo
3500
silent! normal zo
3500
silent! normal zo
3500
silent! normal zo
3515
silent! normal zo
3515
silent! normal zo
3515
silent! normal zo
3515
silent! normal zo
3515
silent! normal zo
3515
silent! normal zo
3515
silent! normal zo
3515
silent! normal zo
3515
silent! normal zo
3523
silent! normal zo
3523
silent! normal zo
3523
silent! normal zo
3523
silent! normal zo
3523
silent! normal zo
3523
silent! normal zo
3523
silent! normal zo
3523
silent! normal zo
3523
silent! normal zo
let s:l = 3515 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3515
normal! 046l
wincmd w
argglobal
edit ginn/framework/pclases/superfacturaventa.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
7
silent! normal zo
45
silent! normal zo
50
silent! normal zo
let s:l = 17 - ((6 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
17
normal! 09l
wincmd w
argglobal
edit ginn/framework/pclases/facturaventa.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
7
silent! normal zo
let s:l = 5 - ((4 * winheight(0) + 8) / 16)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
5
normal! 0
wincmd w
argglobal
edit ginn/framework/pclases/__init__.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
120
silent! normal zo
120
silent! normal zo
120
silent! normal zo
120
silent! normal zo
120
silent! normal zo
120
silent! normal zo
120
silent! normal zo
120
silent! normal zo
120
silent! normal zo
120
silent! normal zo
667
silent! normal zo
15879
silent! normal zo
18312
silent! normal zo
let s:l = 15876 - ((9 * winheight(0) + 6) / 13)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15876
normal! 033l
wincmd w
argglobal
edit ginn/formularios/consulta_vencimientos_pago.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
52
silent! normal zo
181
silent! normal zo
197
silent! normal zo
217
silent! normal zo
217
silent! normal zo
217
silent! normal zo
217
silent! normal zo
let s:l = 237 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
237
normal! 052l
wincmd w
argglobal
edit ginn/formularios/pagares_pagos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
63
silent! normal zo
64
silent! normal zo
72
silent! normal zo
72
silent! normal zo
let s:l = 664 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
664
normal! 069l
wincmd w
argglobal
edit ginn/formularios/gtkexcepthook.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
155
silent! normal zo
169
silent! normal zo
191
silent! normal zo
196
silent! normal zo
279
silent! normal zo
326
silent! normal zo
let s:l = 271 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
271
normal! 016l
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
66
silent! normal zo
75
silent! normal zo
82
silent! normal zo
88
silent! normal zo
let s:l = 79 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
79
normal! 035l
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
silent! normal zo
122
silent! normal zo
134
silent! normal zo
134
silent! normal zo
134
silent! normal zo
174
silent! normal zo
189
silent! normal zo
218
silent! normal zo
254
silent! normal zo
264
silent! normal zo
285
silent! normal zo
286
silent! normal zo
288
silent! normal zo
288
silent! normal zo
288
silent! normal zo
288
silent! normal zo
291
silent! normal zo
293
silent! normal zo
295
silent! normal zo
295
silent! normal zo
321
silent! normal zo
321
normal zc
329
normal zc
337
silent! normal zo
339
silent! normal zo
342
silent! normal zo
344
silent! normal zo
349
normal zc
363
silent! normal zo
363
normal zc
403
silent! normal zo
405
silent! normal zo
403
normal zc
431
silent! normal zo
431
normal zc
470
silent! normal zo
470
normal zc
492
silent! normal zo
496
silent! normal zo
501
silent! normal zo
492
normal zc
630
silent! normal zo
638
silent! normal zo
641
silent! normal zo
654
silent! normal zo
657
silent! normal zo
658
silent! normal zo
661
silent! normal zo
664
silent! normal zo
665
silent! normal zo
668
silent! normal zo
671
silent! normal zo
672
silent! normal zo
672
silent! normal zo
672
silent! normal zo
672
silent! normal zo
672
silent! normal zo
672
silent! normal zo
676
silent! normal zo
677
silent! normal zo
677
silent! normal zo
677
silent! normal zo
677
silent! normal zo
677
silent! normal zo
677
silent! normal zo
682
silent! normal zo
683
silent! normal zo
692
silent! normal zo
703
silent! normal zo
706
silent! normal zo
709
silent! normal zo
712
silent! normal zo
715
silent! normal zo
718
silent! normal zo
723
silent! normal zo
726
silent! normal zo
727
silent! normal zo
760
silent! normal zo
896
silent! normal zo
900
silent! normal zo
902
silent! normal zo
906
silent! normal zo
910
silent! normal zo
911
silent! normal zo
911
silent! normal zo
924
silent! normal zo
926
silent! normal zo
929
silent! normal zo
933
silent! normal zo
937
silent! normal zo
938
silent! normal zo
938
silent! normal zo
1124
silent! normal zo
1158
silent! normal zo
1176
silent! normal zo
1185
silent! normal zo
1186
silent! normal zo
1186
silent! normal zo
1186
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1194
silent! normal zo
1210
silent! normal zo
1337
silent! normal zo
1366
silent! normal zo
1386
silent! normal zo
1471
silent! normal zo
1842
silent! normal zo
1900
silent! normal zo
1915
silent! normal zo
1956
silent! normal zo
2004
silent! normal zo
2005
silent! normal zo
2008
silent! normal zo
2263
silent! normal zo
2266
silent! normal zo
2273
silent! normal zo
2516
silent! normal zo
2524
silent! normal zo
2525
silent! normal zo
2546
silent! normal zo
2559
silent! normal zo
2560
silent! normal zo
2582
silent! normal zo
2651
silent! normal zo
2651
silent! normal zo
2651
silent! normal zo
2651
silent! normal zo
2656
silent! normal zo
2785
silent! normal zo
2805
silent! normal zo
2806
silent! normal zo
2806
silent! normal zo
2806
silent! normal zo
let s:l = 2291 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2291
normal! 044l
wincmd w
argglobal
edit ginn/formularios/trazabilidad.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 50 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
50
normal! 08l
wincmd w
argglobal
edit ginn/formularios/facturas_compra.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
76
silent! normal zo
684
silent! normal zo
692
silent! normal zo
697
silent! normal zo
715
silent! normal zo
720
silent! normal zo
855
silent! normal zo
920
silent! normal zo
926
silent! normal zo
974
silent! normal zo
985
silent! normal zo
986
silent! normal zo
992
silent! normal zo
1894
silent! normal zo
1912
silent! normal zo
let s:l = 694 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
694
normal! 047l
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 9 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 16 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 13 + 29) / 58)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
exe '12resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 12resize ' . ((&columns * 80 + 55) / 111)
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
3wincmd w

" vim: ft=vim ro nowrap smc=128
