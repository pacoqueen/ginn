" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 27 septiembre 2013 at 14:36:25.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata
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
badd +1187 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +310 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +325 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +1931 ginn/formularios/partes_de_fabricacion_bolsas.py
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
badd +535 ginn/formularios/pedidos_de_venta.py
badd +3664 db/tablas.sql
badd +2956 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +1283 ginn/formularios/presupuestos.py
badd +1 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +1007 ginn/formularios/facturas_compra.py
badd +4363 ginn/formularios/utils.py
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
badd +164 ginn/formularios/mail_sender.py
badd +1239 ginn/formularios/abonos_venta.py
args formularios/auditviewer.py
set lines=44 columns=111
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
exe '2resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 22 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
exe '12resize ' . ((&lines * 1 + 22) / 44)
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
270
silent! normal zo
2056
silent! normal zo
2227
silent! normal zo
2227
silent! normal zo
2227
silent! normal zo
2227
silent! normal zo
2227
silent! normal zo
2227
silent! normal zo
2232
silent! normal zo
2249
silent! normal zo
2253
silent! normal zo
2269
silent! normal zo
2813
silent! normal zo
3022
silent! normal zo
3034
silent! normal zo
3035
silent! normal zo
3073
silent! normal zo
4733
silent! normal zo
4746
silent! normal zo
4773
silent! normal zo
7553
silent! normal zo
7830
silent! normal zo
7830
silent! normal zo
7830
silent! normal zo
7830
silent! normal zo
7830
silent! normal zo
7830
silent! normal zo
7830
silent! normal zo
7972
silent! normal zo
7972
silent! normal zo
7972
silent! normal zo
7972
silent! normal zo
7972
silent! normal zo
7972
silent! normal zo
7972
silent! normal zo
7972
silent! normal zo
7972
silent! normal zo
7972
silent! normal zo
9725
silent! normal zo
10075
silent! normal zo
10137
silent! normal zo
10180
silent! normal zo
10192
silent! normal zo
10207
silent! normal zo
10212
silent! normal zo
10226
silent! normal zo
10232
silent! normal zo
10248
silent! normal zo
10254
silent! normal zo
10255
silent! normal zo
10271
silent! normal zo
10421
silent! normal zo
10452
silent! normal zo
10553
silent! normal zo
10566
silent! normal zo
10579
silent! normal zo
10604
silent! normal zo
10605
silent! normal zo
10606
silent! normal zo
10606
silent! normal zo
10606
silent! normal zo
10620
silent! normal zo
10621
silent! normal zo
10622
silent! normal zo
10622
silent! normal zo
10622
silent! normal zo
14225
silent! normal zo
14613
silent! normal zo
14654
silent! normal zo
14977
silent! normal zo
15081
silent! normal zo
15081
silent! normal zo
15172
silent! normal zo
15172
silent! normal zo
15172
silent! normal zo
15172
silent! normal zo
15172
silent! normal zo
15172
silent! normal zo
15172
silent! normal zo
15226
silent! normal zo
15877
silent! normal zo
17943
silent! normal zo
17958
silent! normal zo
19456
silent! normal zo
19557
silent! normal zo
19566
silent! normal zo
19579
silent! normal zo
19604
silent! normal zo
19779
silent! normal zo
19861
silent! normal zo
19868
silent! normal zo
19913
silent! normal zo
19961
silent! normal zo
19979
silent! normal zo
let s:l = 10631 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10631
normal! 0
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
60
silent! normal zo
150
silent! normal zo
170
silent! normal zo
185
silent! normal zo
190
silent! normal zo
279
silent! normal zo
282
silent! normal zo
282
silent! normal zo
293
silent! normal zo
293
silent! normal zo
293
silent! normal zo
293
silent! normal zo
293
silent! normal zo
311
silent! normal zo
314
silent! normal zo
let s:l = 352 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
352
normal! 017l
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
104
silent! normal zo
733
silent! normal zo
733
silent! normal zo
733
silent! normal zo
733
silent! normal zo
let s:l = 814 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
814
normal! 034l
wincmd w
argglobal
edit ginn/formularios/utils.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
2419
silent! normal zo
2419
silent! normal zo
2419
silent! normal zo
2506
silent! normal zo
4351
silent! normal zo
4358
silent! normal zo
4366
silent! normal zo
4367
silent! normal zo
4367
silent! normal zo
4367
silent! normal zo
4375
silent! normal zo
let s:l = 4414 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4414
normal! 019l
wincmd w
argglobal
edit ginn/formularios/mail_sender.py
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
54
silent! normal zo
67
silent! normal zo
168
silent! normal zo
207
silent! normal zo
209
silent! normal zo
209
silent! normal zo
209
silent! normal zo
209
silent! normal zo
209
silent! normal zo
209
silent! normal zo
209
silent! normal zo
let s:l = 52 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
52
normal! 016l
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
59
silent! normal zo
60
silent! normal zo
68
silent! normal zo
68
silent! normal zo
68
silent! normal zo
90
silent! normal zo
90
silent! normal zo
90
silent! normal zo
129
silent! normal zo
130
silent! normal zo
131
silent! normal zo
131
silent! normal zo
141
silent! normal zo
142
silent! normal zo
143
silent! normal zo
144
silent! normal zo
159
silent! normal zo
160
silent! normal zo
170
silent! normal zo
171
silent! normal zo
176
silent! normal zo
177
silent! normal zo
181
silent! normal zo
184
silent! normal zo
190
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
191
silent! normal zo
196
silent! normal zo
197
silent! normal zo
198
silent! normal zo
198
silent! normal zo
198
silent! normal zo
198
silent! normal zo
198
silent! normal zo
198
silent! normal zo
201
silent! normal zo
222
silent! normal zo
231
silent! normal zo
240
silent! normal zo
267
silent! normal zo
269
silent! normal zo
270
silent! normal zo
271
silent! normal zo
293
silent! normal zo
325
silent! normal zo
377
silent! normal zo
392
silent! normal zo
394
silent! normal zo
394
silent! normal zo
394
silent! normal zo
394
silent! normal zo
394
silent! normal zo
400
silent! normal zo
411
silent! normal zo
422
silent! normal zo
426
silent! normal zo
427
silent! normal zo
431
silent! normal zo
559
silent! normal zo
661
silent! normal zo
681
silent! normal zo
697
silent! normal zo
713
silent! normal zo
713
silent! normal zo
713
silent! normal zo
713
silent! normal zo
713
silent! normal zo
713
silent! normal zo
717
silent! normal zo
718
silent! normal zo
718
silent! normal zo
719
silent! normal zo
724
silent! normal zo
729
silent! normal zo
730
silent! normal zo
730
silent! normal zo
731
silent! normal zo
782
silent! normal zo
913
silent! normal zo
971
silent! normal zo
975
silent! normal zo
1012
silent! normal zo
1050
silent! normal zo
1057
silent! normal zo
1080
silent! normal zo
1087
silent! normal zo
1091
silent! normal zo
1123
silent! normal zo
1131
silent! normal zo
1164
silent! normal zo
1168
silent! normal zo
1207
silent! normal zo
1209
silent! normal zo
1295
silent! normal zo
1306
silent! normal zo
1306
silent! normal zo
1306
silent! normal zo
1340
silent! normal zo
1340
silent! normal zo
1340
silent! normal zo
1340
silent! normal zo
1361
silent! normal zo
1369
silent! normal zo
1380
silent! normal zo
1406
silent! normal zo
1489
silent! normal zo
1489
silent! normal zo
1489
silent! normal zo
1489
silent! normal zo
1491
silent! normal zo
1498
silent! normal zo
1498
silent! normal zo
1498
silent! normal zo
1498
silent! normal zo
1498
silent! normal zo
1498
silent! normal zo
1498
silent! normal zo
1513
silent! normal zo
1518
silent! normal zo
1528
silent! normal zo
1536
silent! normal zo
1537
silent! normal zo
1538
silent! normal zo
1538
silent! normal zo
1538
silent! normal zo
1538
silent! normal zo
1542
silent! normal zo
1543
silent! normal zo
1543
silent! normal zo
1543
silent! normal zo
1543
silent! normal zo
1552
silent! normal zo
1552
silent! normal zo
1552
silent! normal zo
1552
silent! normal zo
1552
silent! normal zo
1552
silent! normal zo
1552
silent! normal zo
1552
silent! normal zo
1552
silent! normal zo
1560
silent! normal zo
1572
silent! normal zo
1686
silent! normal zo
1725
silent! normal zo
1730
silent! normal zo
1744
silent! normal zo
1790
silent! normal zo
1836
silent! normal zo
1850
silent! normal zo
1850
silent! normal zo
1850
silent! normal zo
1850
silent! normal zo
1850
silent! normal zo
1850
silent! normal zo
1855
silent! normal zo
1868
silent! normal zo
1871
silent! normal zo
1872
silent! normal zo
1872
silent! normal zo
1872
silent! normal zo
1872
silent! normal zo
1931
silent! normal zo
2005
silent! normal zo
2010
silent! normal zo
2014
silent! normal zo
2028
silent! normal zo
2028
silent! normal zo
2032
silent! normal zo
2032
silent! normal zo
2040
silent! normal zo
2049
silent! normal zo
2067
silent! normal zo
2070
silent! normal zo
2071
silent! normal zo
2071
silent! normal zo
2078
silent! normal zo
2094
silent! normal zo
2120
silent! normal zo
2123
silent! normal zo
2124
silent! normal zo
2158
silent! normal zo
2165
silent! normal zo
2183
silent! normal zo
2187
silent! normal zo
2190
silent! normal zo
2191
silent! normal zo
2191
silent! normal zo
2196
silent! normal zo
2205
silent! normal zo
2210
silent! normal zo
2212
silent! normal zo
2212
silent! normal zo
2213
silent! normal zo
2217
silent! normal zo
2218
silent! normal zo
2225
silent! normal zo
2261
silent! normal zo
2275
silent! normal zo
2303
silent! normal zo
2318
silent! normal zo
2322
silent! normal zo
2323
silent! normal zo
2323
silent! normal zo
2325
silent! normal zo
2326
silent! normal zo
let s:l = 1554 - ((10 * winheight(0) + 11) / 22)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1554
normal! 010l
wincmd w
argglobal
edit ginn/formularios/consulta_cobros.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
50
silent! normal zo
274
silent! normal zo
299
silent! normal zo
301
silent! normal zo
302
silent! normal zo
302
silent! normal zo
302
silent! normal zo
302
silent! normal zo
302
silent! normal zo
306
silent! normal zo
308
silent! normal zo
309
silent! normal zo
309
silent! normal zo
309
silent! normal zo
309
silent! normal zo
309
silent! normal zo
322
silent! normal zo
327
silent! normal zo
335
silent! normal zo
336
silent! normal zo
336
silent! normal zo
let s:l = 320 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
320
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
104
silent! normal zo
277
silent! normal zo
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
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
silent! normal zo
let s:l = 621 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
621
normal! 027l
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
silent! normal zo
51
silent! normal zo
66
silent! normal zo
70
silent! normal zo
let s:l = 97 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
97
normal! 06l
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
578
silent! normal zo
593
silent! normal zo
593
silent! normal zo
593
silent! normal zo
593
silent! normal zo
593
silent! normal zo
593
silent! normal zo
624
silent! normal zo
635
silent! normal zo
643
silent! normal zo
651
silent! normal zo
659
silent! normal zo
659
silent! normal zo
659
silent! normal zo
659
silent! normal zo
668
silent! normal zo
673
silent! normal zo
687
silent! normal zo
let s:l = 126 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
126
normal! 010l
wincmd w
7wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 22 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
exe '12resize ' . ((&lines * 1 + 22) / 44)
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
7wincmd w

" vim: ft=vim ro nowrap smc=128
