" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 11 octubre 2013 at 09:29:54.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 11
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
badd +1680 ginn/formularios/pedidos_de_venta.py
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
badd +828 ginn/framework/pclases/superfacturaventa.py
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
set lines=42 columns=107
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
exe 'vert 1resize ' . ((&columns * 26 + 53) / 107)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 80 + 53) / 107)
exe '3resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 80 + 53) / 107)
exe '4resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 80 + 53) / 107)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 80 + 53) / 107)
exe '6resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 80 + 53) / 107)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 80 + 53) / 107)
exe '8resize ' . ((&lines * 20 + 21) / 42)
exe 'vert 8resize ' . ((&columns * 80 + 53) / 107)
exe '9resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 9resize ' . ((&columns * 80 + 53) / 107)
exe '10resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 10resize ' . ((&columns * 80 + 53) / 107)
exe '11resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 11resize ' . ((&columns * 80 + 53) / 107)
exe '12resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 12resize ' . ((&columns * 80 + 53) / 107)
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
1990
silent! normal zo
2266
silent! normal zo
2342
silent! normal zo
2443
silent! normal zo
2473
silent! normal zo
2555
silent! normal zo
2571
silent! normal zo
2596
silent! normal zo
2613
silent! normal zo
3456
silent! normal zo
3469
silent! normal zo
3475
silent! normal zo
3480
silent! normal zo
3537
silent! normal zo
3548
silent! normal zo
3599
silent! normal zo
3607
silent! normal zo
3619
silent! normal zo
3630
silent! normal zo
3641
silent! normal zo
3659
silent! normal zo
3671
silent! normal zo
3687
silent! normal zo
3702
silent! normal zo
3719
silent! normal zo
3748
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3757
silent! normal zo
3775
silent! normal zo
3779
silent! normal zo
3783
silent! normal zo
3788
silent! normal zo
3799
silent! normal zo
let s:l = 3756 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3756
normal! 0
wincmd w
argglobal
edit ginn/framework/pclases/cliente.py
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
429
silent! normal zo
487
silent! normal zo
499
silent! normal zo
504
silent! normal zo
512
silent! normal zo
525
silent! normal zo
530
silent! normal zo
let s:l = 504 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
504
normal! 020l
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
38
silent! normal zo
let s:l = 46 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
46
normal! 06l
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
2056
silent! normal zo
2232
silent! normal zo
2253
silent! normal zo
3169
silent! normal zo
3320
silent! normal zo
let s:l = 3663 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3663
normal! 014l
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
let s:l = 353 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
353
normal! 0
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
let s:l = 818 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
818
normal! 012l
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
silent! normal zo
61
silent! normal zo
69
silent! normal zo
69
silent! normal zo
69
silent! normal zo
91
silent! normal zo
91
silent! normal zo
91
silent! normal zo
134
silent! normal zo
136
silent! normal zo
141
silent! normal zo
142
silent! normal zo
146
silent! normal zo
147
silent! normal zo
158
silent! normal zo
159
silent! normal zo
160
silent! normal zo
176
silent! normal zo
177
silent! normal zo
198
silent! normal zo
201
silent! normal zo
207
silent! normal zo
218
silent! normal zo
239
silent! normal zo
284
silent! normal zo
286
silent! normal zo
287
silent! normal zo
288
silent! normal zo
342
silent! normal zo
343
silent! normal zo
350
silent! normal zo
394
silent! normal zo
409
silent! normal zo
417
silent! normal zo
439
silent! normal zo
443
silent! normal zo
444
silent! normal zo
459
silent! normal zo
576
silent! normal zo
616
silent! normal zo
625
silent! normal zo
632
silent! normal zo
632
silent! normal zo
637
silent! normal zo
638
silent! normal zo
698
silent! normal zo
714
silent! normal zo
741
silent! normal zo
757
silent! normal zo
764
silent! normal zo
766
silent! normal zo
799
silent! normal zo
908
silent! normal zo
909
silent! normal zo
913
silent! normal zo
946
silent! normal zo
948
silent! normal zo
981
silent! normal zo
1026
silent! normal zo
1029
silent! normal zo
1035
silent! normal zo
1081
silent! normal zo
1092
silent! normal zo
1095
silent! normal zo
1154
silent! normal zo
1278
silent! normal zo
1287
silent! normal zo
1288
silent! normal zo
1302
silent! normal zo
1304
silent! normal zo
1326
silent! normal zo
1400
silent! normal zo
1437
silent! normal zo
1468
silent! normal zo
1477
silent! normal zo
1477
silent! normal zo
1520
silent! normal zo
1520
silent! normal zo
1520
silent! normal zo
1520
silent! normal zo
1523
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1530
silent! normal zo
1548
silent! normal zo
1595
silent! normal zo
1599
silent! normal zo
1601
silent! normal zo
1609
silent! normal zo
1609
silent! normal zo
1618
silent! normal zo
1621
silent! normal zo
1628
silent! normal zo
1647
silent! normal zo
1648
silent! normal zo
1649
silent! normal zo
1657
silent! normal zo
1659
silent! normal zo
1659
silent! normal zo
1661
silent! normal zo
1662
silent! normal zo
1662
silent! normal zo
1685
silent! normal zo
1705
silent! normal zo
1732
silent! normal zo
1749
silent! normal zo
1771
silent! normal zo
1776
silent! normal zo
1790
silent! normal zo
1802
silent! normal zo
1803
silent! normal zo
1810
silent! normal zo
1816
silent! normal zo
1882
silent! normal zo
1901
silent! normal zo
1977
silent! normal zo
1991
silent! normal zo
1993
silent! normal zo
2051
silent! normal zo
2056
silent! normal zo
2060
silent! normal zo
2211
silent! normal zo
2233
silent! normal zo
2236
silent! normal zo
2237
silent! normal zo
2237
silent! normal zo
2242
silent! normal zo
2243
silent! normal zo
2244
silent! normal zo
2244
silent! normal zo
2252
silent! normal zo
2257
silent! normal zo
2259
silent! normal zo
2259
silent! normal zo
2286
silent! normal zo
2289
silent! normal zo
2290
silent! normal zo
let s:l = 1522 - ((9 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1522
normal! 037l
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
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/facturas_compra.py
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
1662
silent! normal zo
1678
silent! normal zo
1682
silent! normal zo
1683
silent! normal zo
1684
silent! normal zo
1684
silent! normal zo
1685
silent! normal zo
1685
silent! normal zo
let s:l = 1684 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1684
normal! 052l
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
normal! 08l
wincmd w
8wincmd w
exe 'vert 1resize ' . ((&columns * 26 + 53) / 107)
exe '2resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 2resize ' . ((&columns * 80 + 53) / 107)
exe '3resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 3resize ' . ((&columns * 80 + 53) / 107)
exe '4resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 4resize ' . ((&columns * 80 + 53) / 107)
exe '5resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 5resize ' . ((&columns * 80 + 53) / 107)
exe '6resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 6resize ' . ((&columns * 80 + 53) / 107)
exe '7resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 7resize ' . ((&columns * 80 + 53) / 107)
exe '8resize ' . ((&lines * 20 + 21) / 42)
exe 'vert 8resize ' . ((&columns * 80 + 53) / 107)
exe '9resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 9resize ' . ((&columns * 80 + 53) / 107)
exe '10resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 10resize ' . ((&columns * 80 + 53) / 107)
exe '11resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 11resize ' . ((&columns * 80 + 53) / 107)
exe '12resize ' . ((&lines * 1 + 21) / 42)
exe 'vert 12resize ' . ((&columns * 80 + 53) / 107)
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
8wincmd w

" vim: ft=vim ro nowrap smc=128
