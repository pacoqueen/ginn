" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
<<<<<<< HEAD
" Created by session.vim 1.5 on 29 julio 2013 at 14:51:06.
=======
" Created by session.vim 1.5 on 02 agosto 2013 at 19:15:50.
>>>>>>> blade-runner
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
badd +163 ~/.vimrc
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
badd +1247 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +310 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2258 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1608 ginn/formularios/partes_de_fabricacion_balas.py
badd +1957 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +121 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +105 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +11926 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +443 ginn/formularios/facturas_venta.py
badd +404 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +21 ginn/formularios/ventana.py
<<<<<<< HEAD
badd +663 ginn/formularios/pedidos_de_venta.py
badd +1294 db/tablas.sql
badd +2869 ginn/formularios/albaranes_de_salida.py
=======
badd +2310 ginn/formularios/pedidos_de_venta.py
badd +1 db/tablas.sql
badd +1958 ginn/formularios/albaranes_de_salida.py
>>>>>>> blade-runner
badd +1 ginn/formularios/presupuesto.py
badd +9 ginn/formularios/presupuestos.py
badd +382 ginn/informes/presupuesto2.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +724 ginn/formularios/facturas_compra.py
badd +4395 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +1134 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +46 ginn/formularios/gtkexcepthook.py
badd +512 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +19438 ginn/framework/pclases/__init__.py
badd +398 ginn/framework/pclases/superfacturaventa.py
badd +4 ginn/framework/pclases/facturaventa.py
badd +689 ginn/formularios/consulta_mensual_nominas.py
badd +269 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +249 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +921 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
<<<<<<< HEAD
badd +1 ginn/formularios/consumo_balas_partida.py
badd +27 ginn/informes/albaran_porte.py
args formularios/auditviewer.py
set lines=66 columns=111
edit ginn/informes/geninformes.py
=======
badd +221 ginn/formularios/consumo_balas_partida.py
badd +553 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +0 ginn/framework/pclases/cliente.py
args formularios/auditviewer.py
set lines=69 columns=111
edit ginn/framework/pclases/cliente.py
>>>>>>> blade-runner
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
<<<<<<< HEAD
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
8wincmd k
wincmd w
wincmd w
=======
6wincmd k
>>>>>>> blade-runner
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
<<<<<<< HEAD
exe '2resize ' . ((&lines * 48 + 33) / 66)
=======
exe '2resize ' . ((&lines * 31 + 34) / 69)
>>>>>>> blade-runner
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 25 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
<<<<<<< HEAD
exe '6resize ' . ((&lines * 1 + 33) / 66)
=======
exe '6resize ' . ((&lines * 1 + 34) / 69)
>>>>>>> blade-runner
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
<<<<<<< HEAD
exe '9resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
=======
>>>>>>> blade-runner
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
<<<<<<< HEAD
11273
normal! zo
11281
normal! zo
11429
normal! zo
11458
normal! zo
11460
normal! zo
let s:l = 11460 - ((45 * winheight(0) + 24) / 48)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
11460
normal! 067|
wincmd w
argglobal
edit ginn/formularios/consumo_balas_partida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
346
normal! zo
let s:l = 633 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
633
normal! 0
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_bolsas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
89
normal! zo
768
normal! zo
778
normal! zo
1789
normal! zo
1801
normal! zo
1819
normal! zo
1828
normal! zo
1853
normal! zo
1858
normal! zo
1861
normal! zo
1862
normal! zo
1862
=======
53
>>>>>>> blade-runner
normal! zo
429
normal! zo
491
normal! zo
let s:l = 448 - ((23 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
448
normal! 09|
wincmd w
argglobal
edit db/tablas.sql
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
551
normal! zo
564
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
621
normal! zo
1204
normal! zo
1217
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3427
normal! zo
3433
normal! zo
3437
normal! zo
3492
normal! zo
3492
normal! zo
3492
normal! zo
3492
normal! zo
3492
normal! zo
3492
normal! zo
3492
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3500
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3507
normal! zo
3514
normal! zo
3514
normal! zo
3514
normal! zo
3514
normal! zo
3514
normal! zo
3514
normal! zo
3514
normal! zo
3514
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3532
normal! zo
3550
normal! zo
3550
normal! zo
3550
normal! zo
3550
normal! zo
3550
normal! zo
3550
normal! zo
3550
normal! zo
3550
normal! zo
3550
normal! zo
3558
normal! zo
3562
normal! zo
3563
normal! zo
3563
normal! zo
3563
normal! zo
3563
normal! zo
3563
normal! zo
3563
normal! zo
3563
normal! zo
3563
normal! zo
3568
normal! zo
3568
normal! zo
3568
normal! zo
3568
normal! zo
3568
normal! zo
3568
normal! zo
3568
normal! zo
3568
normal! zo
3568
normal! zo
3582
normal! zo
3582
normal! zo
3582
normal! zo
3582
normal! zo
3582
normal! zo
3582
normal! zo
3582
normal! zo
3582
normal! zo
let s:l = 3545 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3545
normal! 0170|
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
normal! zo
75
normal! zo
82
normal! zo
88
normal! zo
104
normal! zo
105
normal! zo
105
normal! zo
let s:l = 140 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
140
normal! 021|
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
38
normal! zo
43
normal! zo
317
normal! zo
357
normal! zo
484
normal! zo
503
normal! zo
503
normal! zo
503
normal! zo
503
normal! zo
503
normal! zo
503
normal! zo
510
normal! zo
515
normal! zo
586
normal! zo
591
normal! zo
591
normal! zo
591
normal! zo
591
normal! zo
591
normal! zo
596
normal! zo
596
normal! zo
601
normal! zo
601
normal! zo
601
normal! zo
601
normal! zo
601
normal! zo
617
normal! zo
618
normal! zo
618
normal! zo
623
normal! zo
624
normal! zo
624
normal! zo
628
normal! zo
628
normal! zo
628
normal! zo
632
normal! zo
640
normal! zo
650
normal! zo
659
normal! zo
679
normal! zo
687
normal! zo
708
normal! zo
716
normal! zo
797
normal! zo
803
normal! zo
<<<<<<< HEAD
let s:l = 5209 - ((0 * winheight(0) + 0) / 1)
=======
let s:l = 607 - ((10 * winheight(0) + 12) / 25)
>>>>>>> blade-runner
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
607
normal! 09|
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
normal! zo
75
normal! zo
82
normal! zo
88
normal! zo
let s:l = 24 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
24
normal! 0
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
34
normal! zo
51
normal! zo
66
normal! zo
89
normal! zo
100
normal! zo
let s:l = 82 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
82
normal! 020|
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_rollos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
229
normal! zo
230
normal! zo
262
normal! zo
262
normal! zo
339
normal! zo
340
normal! zo
345
normal! zo
350
normal! zo
351
normal! zo
356
normal! zo
362
normal! zo
467
normal! zo
579
normal! zo
595
normal! zo
725
normal! zo
734
normal! zo
834
normal! zo
850
normal! zo
850
normal! zo
850
normal! zo
850
normal! zo
961
normal! zo
966
normal! zo
1531
normal! zo
1727
normal! zo
1728
normal! zo
1728
normal! zo
1728
normal! zo
1728
normal! zo
1739
normal! zo
1740
normal! zo
1744
normal! zo
1744
normal! zo
1745
normal! zo
1752
normal! zo
1753
normal! zo
1804
normal! zo
3253
normal! zo
3260
normal! zo
3265
normal! zo
3272
normal! zo
3276
normal! zo
3281
normal! zo
3282
normal! zo
3282
normal! zo
3282
normal! zo
3288
normal! zo
3293
normal! zo
3294
normal! zo
3299
normal! zo
let s:l = 1750 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1750
normal! 061|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
<<<<<<< HEAD
exe '2resize ' . ((&lines * 48 + 33) / 66)
=======
exe '2resize ' . ((&lines * 31 + 34) / 69)
>>>>>>> blade-runner
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 25 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
<<<<<<< HEAD
exe '6resize ' . ((&lines * 1 + 33) / 66)
=======
exe '6resize ' . ((&lines * 1 + 34) / 69)
>>>>>>> blade-runner
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 34) / 69)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
<<<<<<< HEAD
exe '9resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 33) / 66)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
=======
>>>>>>> blade-runner
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
