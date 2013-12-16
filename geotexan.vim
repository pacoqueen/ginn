" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 16 diciembre 2013 at 16:21:04.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'light'
	set background=light
endif
if !exists('g:colors_name') || g:colors_name != 'github' | colorscheme github | endif
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
badd +353 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +266 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +901 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1706 ginn/formularios/partes_de_fabricacion_rollos.py
badd +446 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +117 ginn/formularios/launcher.py
badd +625 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +3063 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2322 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +750 ginn/formularios/ventana.py
badd +1899 ginn/formularios/pedidos_de_venta.py
badd +3876 db/tablas.sql
badd +532 ginn/formularios/albaranes_de_salida.py
badd +227 ginn/formularios/presupuesto.py
badd +417 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +693 ginn/formularios/facturas_compra.py
badd +1950 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +218 ginn/formularios/gtkexcepthook.py
badd +402 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +61 ginn/framework/pclases/facturaventa.py
badd +694 ginn/formularios/consulta_mensual_nominas.py
badd +88 ginn/informes/treeview2pdf.py
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
badd +324 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +383 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +1020 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +523 ginn/formularios/postomatic.py
badd +36 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +449 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +416 ginn/formularios/consulta_productividad.py
badd +212 ginn/formularios/mail_sender.py
badd +1143 ginn/formularios/abonos_venta.py
badd +306 ginn/formularios/ventana_progreso.py
badd +993 ginn/formularios/control_personal.py
badd +195 ginn/formularios/listado_rollos.py
badd +85 ginn/formularios/consulta_existenciasRollos.py
badd +91 ginn/formularios/listado_rollos_defectuosos.py
badd +3498 ginn/formularios/consulta_global.py
badd +195 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
badd +1 ginn/informes/presupuesto.py
badd +112 ginn/formularios/consulta_libro_iva.py
badd +427 ginn/formularios/consulta_ofertas.py
badd +24 extra/patches/create_ventana_consultas.py
badd +203 ginn/lib/ezodf/ezodf/const.py
badd +61 ginn/lib/ezodf/ezodf/xmlns.py
badd +307 ginn/lib/simple_odspy/simpleodspy/sodsods.py
badd +17 ginn/lib/simple_odspy/simpleodspy/sodsspreadsheet.py
badd +41 ginn/lib/simple_odspy/simpleodspy/sodstable.py
badd +66 ginn/lib/odfpy/contrib/odscell/odscell
badd +127 ginn/lib/odfpy/contrib/odscell/odscell.py
badd +133 ginn/formularios/consulta_ofertas_pendientes_validar.py
badd +392 ginn/formularios/consulta_ofertas_estudio.py
badd +1075 ginn/formularios/confirmings.py
badd +177 ginn/formularios/transferencias.py
badd +66 ginn/formularios/cuentas_destino.py
badd +509 ginn/formularios/facturacion_por_cliente_y_fechas.py
args formularios/auditviewer.py
set lines=45 columns=102
edit ginn/framework/pclases/__init__.py
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
6wincmd k
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
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 5 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 27 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
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
lcd ~/Geotexan/src/Geotex-INN
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
270
normal! zo
3833
normal! zo
3925
normal! zo
3932
normal! zo
3933
normal! zo
3933
normal! zo
3933
normal! zo
3933
normal! zo
3933
normal! zo
3933
normal! zo
4088
normal! zo
4155
normal! zo
5840
normal! zo
6006
normal! zo
7521
normal! zo
7574
normal! zo
9051
normal! zo
9746
normal! zo
9786
normal! zo
9839
normal! zo
9842
normal! zo
9846
normal! zo
9846
normal! zo
9846
normal! zo
9862
normal! zo
10213
normal! zo
10345
normal! zo
10494
normal! zo
10497
normal! zo
10500
normal! zo
10500
normal! zo
10500
normal! zo
10520
normal! zo
10557
normal! zo
10757
normal! zo
11012
normal! zo
11098
normal! zo
11915
normal! zo
11915
normal! zo
11915
normal! zo
13352
normal! zo
13352
normal! zo
13352
normal! zo
13367
normal! zo
13368
normal! zo
13522
normal! zo
13522
normal! zo
13522
normal! zo
13548
normal! zo
13549
normal! zo
13653
normal! zo
13653
normal! zo
13653
normal! zo
13669
normal! zo
13670
normal! zo
14300
normal! zo
15639
normal! zo
16994
normal! zo
17018
normal! zo
17023
normal! zo
17028
normal! zo
17035
normal! zo
19582
normal! zo
19594
normal! zo
19599
normal! zo
let s:l = 10772 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10772
normal! 09|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/presupuestos.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
61
normal! zo
279
normal! zo
396
normal! zo
406
normal! zo
449
normal! zo
460
normal! zo
469
normal! zo
495
normal! zo
497
normal! zo
498
normal! zo
499
normal! zo
530
normal! zo
543
normal! zo
575
normal! zo
645
normal! zo
664
normal! zo
694
normal! zo
698
normal! zo
699
normal! zo
749
normal! zo
768
normal! zo
801
normal! zo
1539
normal! zo
1547
normal! zo
2411
normal! zo
2496
normal! zo
2502
normal! zo
2528
normal! zo
let s:l = 2511 - ((12 * winheight(0) + 13) / 27)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2511
normal! 061|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_ofertas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
53
normal! zo
54
normal! zo
62
normal! zo
62
normal! zo
70
normal! zo
70
normal! zo
83
normal! zo
169
normal! zo
169
normal! zo
188
normal! zo
188
normal! zo
211
normal! zo
224
normal! zo
225
normal! zo
232
normal! zo
238
normal! zo
239
normal! zo
250
normal! zo
256
normal! zo
257
normal! zo
280
normal! zo
327
normal! zo
334
normal! zo
424
normal! zo
500
normal! zo
515
normal! zo
580
normal! zo
600
normal! zo
606
normal! zo
659
normal! zo
694
normal! zo
752
normal! zo
784
normal! zo
790
normal! zo
805
normal! zo
806
normal! zo
841
normal! zo
872
normal! zo
878
normal! zo
972
normal! zo
984
normal! zo
1006
normal! zo
1045
normal! zo
1049
normal! zo
1049
normal! zo
1060
normal! zo
1064
normal! zo
1064
normal! zo
1072
normal! zo
1108
normal! zo
1108
normal! zo
1108
normal! zo
1108
normal! zo
1108
normal! zo
1108
normal! zo
1108
normal! zo
1111
normal! zo
1111
normal! zo
1111
normal! zo
1111
normal! zo
1111
normal! zo
1111
normal! zo
1117
normal! zo
1127
normal! zo
1130
normal! zo
1199
normal! zo
1203
normal! zo
1204
normal! zo
1205
normal! zo
1212
normal! zo
1218
normal! zo
1218
normal! zo
1219
normal! zo
1219
normal! zo
1219
normal! zo
1220
normal! zo
1220
normal! zo
1220
normal! zo
1220
normal! zo
1220
normal! zo
1224
normal! zo
1224
normal! zo
1224
normal! zo
1228
normal! zo
1228
normal! zo
1229
normal! zo
1229
normal! zo
1229
normal! zo
1233
normal! zo
1233
normal! zo
1233
normal! zo
1237
normal! zo
1237
normal! zo
1238
normal! zo
1238
normal! zo
1238
normal! zo
1242
normal! zo
1242
normal! zo
1242
normal! zo
1246
normal! zo
1246
normal! zo
1247
normal! zo
1247
normal! zo
1247
normal! zo
1251
normal! zo
1251
normal! zo
1251
normal! zo
let s:l = 1170 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1170
normal! 039|
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
let s:l = 316 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
316
normal! 044|
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
66
normal! zo
104
normal! zo
105
normal! zo
105
normal! zo
137
normal! zo
154
normal! zo
155
normal! zo
161
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
210
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
1068
normal! zo
let s:l = 137 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
137
normal! 029|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/configuracion.py
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
85
normal! zo
435
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
503
normal! zo
let s:l = 521 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
521
normal! 07|
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
51
normal! zo
67
normal! zo
71
normal! zo
98
normal! zo
101
normal! zo
112
normal! zo
let s:l = 68 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
68
normal! 053|
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 21 + 51) / 102)
exe '2resize ' . ((&lines * 5 + 22) / 45)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 102)
exe '3resize ' . ((&lines * 27 + 22) / 45)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 102)
exe '4resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 102)
exe '5resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 102)
exe '6resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 102)
exe '7resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 102)
exe '8resize ' . ((&lines * 1 + 22) / 45)
exe 'vert 8resize ' . ((&columns * 80 + 51) / 102)
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
