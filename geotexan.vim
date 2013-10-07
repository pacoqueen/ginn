" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 07 octubre 2013 at 12:18:36.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 13
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'solarized' | colorscheme solarized | endif
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
badd +127 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +310 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +325 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +901 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +3390 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +117 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +4852 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2733 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +292 ginn/formularios/ventana.py
badd +855 ginn/formularios/pedidos_de_venta.py
badd +1 db/tablas.sql
badd +700 ginn/formularios/albaranes_de_salida.py
badd +170 ginn/formularios/presupuesto.py
badd +2236 ginn/formularios/presupuestos.py
badd +1 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +1007 ginn/formularios/facturas_compra.py
badd +54 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +46 ginn/formularios/gtkexcepthook.py
badd +476 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +803 ginn/framework/pclases/superfacturaventa.py
badd +47 ginn/framework/pclases/facturaventa.py
badd +689 ginn/formularios/consulta_mensual_nominas.py
badd +269 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +118 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +140 ginn/formularios/listado_balas.py
badd +254 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +221 ginn/formularios/consumo_balas_partida.py
badd +553 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +535 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +628 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +523 ginn/formularios/postomatic.py
badd +36 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +394 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +416 ginn/formularios/consulta_productividad.py
badd +212 ginn/formularios/mail_sender.py
badd +1239 ginn/formularios/abonos_venta.py
badd +131 ginn/formularios/ventana_progreso.py
args formularios/auditviewer.py
set lines=55 columns=108
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
9wincmd k
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
exe 'vert 1resize ' . ((&columns * 28 + 54) / 108)
exe '2resize ' . ((&lines * 18 + 27) / 55)
exe 'vert 2resize ' . ((&columns * 79 + 54) / 108)
exe '3resize ' . ((&lines * 2 + 27) / 55)
exe 'vert 3resize ' . ((&columns * 79 + 54) / 108)
exe '4resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 4resize ' . ((&columns * 79 + 54) / 108)
exe '5resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 5resize ' . ((&columns * 79 + 54) / 108)
exe '6resize ' . ((&lines * 17 + 27) / 55)
exe 'vert 6resize ' . ((&columns * 79 + 54) / 108)
exe '7resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 7resize ' . ((&columns * 79 + 54) / 108)
exe '8resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 8resize ' . ((&columns * 79 + 54) / 108)
exe '9resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 9resize ' . ((&columns * 79 + 54) / 108)
exe '10resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 10resize ' . ((&columns * 79 + 54) / 108)
exe '11resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 11resize ' . ((&columns * 79 + 54) / 108)
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
let s:l = 2609 - ((8 * winheight(0) + 9) / 18)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2609
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
let s:l = 10292 - ((0 * winheight(0) + 1) / 2)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10292
normal! 09|
wincmd w
argglobal
edit ginn/informes/carta_compromiso.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 352 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
352
normal! 012|
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
let s:l = 815 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
815
normal! 013|
wincmd w
argglobal
edit ginn/formularios/presupuestos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
60
normal! zo
61
normal! zo
69
normal! zo
69
normal! zo
69
normal! zo
91
normal! zo
91
normal! zo
91
normal! zo
134
normal! zo
136
normal! zo
141
normal! zo
142
normal! zo
146
normal! zo
147
normal! zo
158
normal! zo
159
normal! zo
160
normal! zo
176
normal! zo
177
normal! zo
198
normal! zo
201
normal! zo
207
normal! zo
218
normal! zo
239
normal! zo
284
normal! zo
286
normal! zo
287
normal! zo
288
normal! zo
342
normal! zo
343
normal! zo
350
normal! zo
394
normal! zo
409
normal! zo
417
normal! zo
439
normal! zo
443
normal! zo
444
normal! zo
459
normal! zo
576
normal! zo
616
normal! zo
625
normal! zo
632
normal! zo
632
normal! zo
637
normal! zo
638
normal! zo
698
normal! zo
714
normal! zo
741
normal! zo
757
normal! zo
764
normal! zo
766
normal! zo
799
normal! zo
908
normal! zo
909
normal! zo
913
normal! zo
946
normal! zo
948
normal! zo
981
normal! zo
1026
normal! zo
1029
normal! zo
1035
normal! zo
1081
normal! zo
1092
normal! zo
1095
normal! zo
1154
normal! zo
1278
normal! zo
1287
normal! zo
1288
normal! zo
1302
normal! zo
1304
normal! zo
1326
normal! zo
1400
normal! zo
1437
normal! zo
1468
normal! zo
1477
normal! zo
1477
normal! zo
1520
normal! zo
1520
normal! zo
1520
normal! zo
1520
normal! zo
1530
normal! zo
1530
normal! zo
1530
normal! zo
1530
normal! zo
1530
normal! zo
1530
normal! zo
1530
normal! zo
1548
normal! zo
1595
normal! zo
1599
normal! zo
1601
normal! zo
1609
normal! zo
1609
normal! zo
1618
normal! zo
1621
normal! zo
1628
normal! zo
1647
normal! zo
1648
normal! zo
1649
normal! zo
1657
normal! zo
1659
normal! zo
1659
normal! zo
1661
normal! zo
1662
normal! zo
1662
normal! zo
1685
normal! zo
1705
normal! zo
1732
normal! zo
1749
normal! zo
1771
normal! zo
1776
normal! zo
1790
normal! zo
1802
normal! zo
1803
normal! zo
1810
normal! zo
1816
normal! zo
1882
normal! zo
1901
normal! zo
1977
normal! zo
1991
normal! zo
1993
normal! zo
2051
normal! zo
2056
normal! zo
2060
normal! zo
2211
normal! zo
2233
normal! zo
2236
normal! zo
2237
normal! zo
2237
normal! zo
2242
normal! zo
2243
normal! zo
2244
normal! zo
2244
normal! zo
2252
normal! zo
2257
normal! zo
2259
normal! zo
2259
normal! zo
2286
normal! zo
2289
normal! zo
2290
normal! zo
let s:l = 2269 - ((0 * winheight(0) + 8) / 17)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2269
normal! 045|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_cobros.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 320 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
320
normal! 0
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/ventana.py
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
edit ~/Geotexan/src/Geotex-INN/ginn/framework/pclases/superfacturaventa.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 621 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
621
normal! 025|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/launcher.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 97 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
97
normal! 09|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 8 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
8
normal! 0
lcd ~/Geotexan/src/Geotex-INN
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 28 + 54) / 108)
exe '2resize ' . ((&lines * 18 + 27) / 55)
exe 'vert 2resize ' . ((&columns * 79 + 54) / 108)
exe '3resize ' . ((&lines * 2 + 27) / 55)
exe 'vert 3resize ' . ((&columns * 79 + 54) / 108)
exe '4resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 4resize ' . ((&columns * 79 + 54) / 108)
exe '5resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 5resize ' . ((&columns * 79 + 54) / 108)
exe '6resize ' . ((&lines * 17 + 27) / 55)
exe 'vert 6resize ' . ((&columns * 79 + 54) / 108)
exe '7resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 7resize ' . ((&columns * 79 + 54) / 108)
exe '8resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 8resize ' . ((&columns * 79 + 54) / 108)
exe '9resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 9resize ' . ((&columns * 79 + 54) / 108)
exe '10resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 10resize ' . ((&columns * 79 + 54) / 108)
exe '11resize ' . ((&lines * 1 + 27) / 55)
exe 'vert 11resize ' . ((&columns * 79 + 54) / 108)
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
11wincmd w
let s:bufnr = bufnr("%")
edit ~/Geotexan/src/Geotex-INN/ginn/formularios
execute "bwipeout" s:bufnr
1resize 53|vert 1resize 28|2resize 18|vert 2resize 79|3resize 2|vert 3resize 79|4resize 1|vert 4resize 79|5resize 1|vert 5resize 79|6resize 17|vert 6resize 79|7resize 1|vert 7resize 79|8resize 1|vert 8resize 79|9resize 1|vert 9resize 79|10resize 1|vert 10resize 79|11resize 1|vert 11resize 79|
tabnext 1
6wincmd w

" vim: ft=vim ro nowrap smc=128
