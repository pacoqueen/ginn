" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 31 octubre 2013 at 07:27:09.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 13
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
badd +127 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +39 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +603 ginn/formularios/productos_de_venta_rollos.py
badd +382 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +417 ginn/formularios/productos_de_venta_especial.py
badd +1 ginn/formularios/partes_de_fabricacion_balas.py
badd +901 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +749 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +117 ginn/formularios/launcher.py
badd +464 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +230 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1115 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1627 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +292 ginn/formularios/ventana.py
badd +1899 ginn/formularios/pedidos_de_venta.py
badd +1 db/tablas.sql
badd +1732 ginn/formularios/albaranes_de_salida.py
badd +170 ginn/formularios/presupuesto.py
badd +2236 ginn/formularios/presupuestos.py
badd +1 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +693 ginn/formularios/facturas_compra.py
badd +4379 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +751 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +218 ginn/formularios/gtkexcepthook.py
badd +407 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +1 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +61 ginn/framework/pclases/facturaventa.py
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
badd +510 ginn/framework/pclases/cliente.py
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
badd +322 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +1 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +416 ginn/formularios/consulta_productividad.py
badd +212 ginn/formularios/mail_sender.py
badd +1143 ginn/formularios/abonos_venta.py
badd +131 ginn/formularios/ventana_progreso.py
badd +1047 ginn/formularios/control_personal.py
badd +195 ginn/formularios/listado_rollos.py
badd +68 ginn/formularios/consulta_existenciasRollos.py
badd +91 ginn/formularios/listado_rollos_defectuosos.py
badd +3498 ginn/formularios/consulta_global.py
badd +195 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
args formularios/auditviewer.py
set lines=54 columns=110
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
exe 'vert 1resize ' . ((&columns * 29 + 55) / 110)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 110)
exe '3resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 110)
exe '4resize ' . ((&lines * 30 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 110)
exe '5resize ' . ((&lines * 9 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 110)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 110)
exe '7resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 110)
exe '8resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 110)
exe '9resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 110)
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
1016
normal! zo
1408
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3759
normal! zo
3774
normal! zo
let s:l = 59 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
59
normal! 02|
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
270
normal! zo
461
normal! zo
480
normal! zo
499
normal! zo
667
normal! zo
674
normal! zo
683
normal! zo
742
normal! zo
775
normal! zo
778
normal! zo
778
normal! zo
778
normal! zo
778
normal! zo
778
normal! zo
778
normal! zo
780
normal! zo
780
normal! zo
780
normal! zo
780
normal! zo
780
normal! zo
780
normal! zo
1192
normal! zo
1201
normal! zo
1301
normal! zo
1310
normal! zo
1410
normal! zo
1419
normal! zo
1519
normal! zo
1528
normal! zo
2072
normal! zo
2248
normal! zo
2269
normal! zo
2450
normal! zo
2460
normal! zo
2460
normal! zo
3185
normal! zo
3336
normal! zo
4088
normal! zo
4417
normal! zo
4456
normal! zo
4456
normal! zo
4456
normal! zo
4456
normal! zo
4749
normal! zo
4762
normal! zo
4773
normal! zo
4794
normal! zo
7253
normal! zo
7258
normal! zo
7258
normal! zo
9051
normal! zo
9124
normal! zo
9391
normal! zo
9746
normal! zo
10094
normal! zo
10099
normal! zo
10107
normal! zo
10212
normal! zo
10981
normal! zo
10995
normal! zo
10995
normal! zo
10995
normal! zo
10995
normal! zo
14269
normal! zo
14457
normal! zo
14492
normal! zo
14497
normal! zo
14498
normal! zo
15032
normal! zo
15037
normal! zo
15037
normal! zo
15037
normal! zo
15037
normal! zo
15281
normal! zo
15294
normal! zo
15304
normal! zo
15407
normal! zo
15411
normal! zo
15411
normal! zo
15411
normal! zo
15411
normal! zo
15411
normal! zo
15415
normal! zo
15415
normal! zo
15415
normal! zo
15415
normal! zo
15457
normal! zo
15460
normal! zo
15460
normal! zo
15460
normal! zo
15460
normal! zo
16199
normal! zo
16587
normal! zo
16598
normal! zo
16598
normal! zo
16598
normal! zo
16598
normal! zo
16629
normal! zo
16637
normal! zo
16637
normal! zo
16637
normal! zo
16637
normal! zo
16952
normal! zo
17148
normal! zo
18003
normal! zo
18013
normal! zo
18102
normal! zo
18112
normal! zo
18235
normal! zo
18302
normal! zo
18313
normal! zo
18363
normal! zo
18420
normal! zo
18430
normal! zo
18478
normal! zo
18531
normal! zo
18772
normal! zo
18794
normal! zo
18853
normal! zo
19051
normal! zo
19520
normal! zo
19759
normal! zo
19932
normal! zo
19936
normal! zo
19936
normal! zo
20025
normal! zo
20088
normal! zo
20410
normal! zo
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
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
45
normal! zo
49
normal! zo
54
normal! zo
54
normal! zo
54
normal! zo
68
normal! zo
85
normal! zo
98
normal! zo
117
normal! zo
127
normal! zo
137
normal! zo
139
normal! zo
140
normal! zo
140
normal! zo
140
normal! zo
140
normal! zo
140
normal! zo
140
normal! zo
143
normal! zo
143
normal! zo
143
normal! zo
147
normal! zo
152
normal! zo
153
normal! zo
153
normal! zo
153
normal! zo
153
normal! zo
153
normal! zo
153
normal! zo
160
normal! zo
178
normal! zo
190
normal! zo
309
normal! zo
312
normal! zo
317
normal! zo
317
normal! zo
317
normal! zo
321
normal! zo
324
normal! zo
324
normal! zo
324
normal! zo
let s:l = 186 - ((16 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
186
normal! 010|
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
normal! zo
105
normal! zo
143
normal! zo
let s:l = 145 - ((1 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
145
normal! 031|
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
61
normal! zo
62
normal! zo
70
normal! zo
70
normal! zo
70
normal! zo
70
normal! zo
107
normal! zo
107
normal! zo
107
normal! zo
107
normal! zo
107
normal! zo
110
normal! zo
110
normal! zo
110
normal! zo
110
normal! zo
110
normal! zo
154
normal! zo
154
normal! zo
154
normal! zo
161
normal! zo
162
normal! zo
165
normal! zo
166
normal! zo
199
normal! zo
211
normal! zo
217
normal! zo
219
normal! zo
222
normal! zo
224
normal! zo
229
normal! zo
230
normal! zo
234
normal! zo
235
normal! zo
246
normal! zo
247
normal! zo
248
normal! zo
264
normal! zo
265
normal! zo
276
normal! zo
278
normal! zo
287
normal! zo
287
normal! zo
287
normal! zo
287
normal! zo
287
normal! zo
287
normal! zo
319
normal! zo
320
normal! zo
321
normal! zo
330
normal! zo
346
normal! zo
347
normal! zo
347
normal! zo
348
normal! zo
353
normal! zo
356
normal! zo
362
normal! zo
373
normal! zo
394
normal! zo
399
normal! zo
410
normal! zo
410
normal! zo
419
normal! zo
419
normal! zo
419
normal! zo
419
normal! zo
419
normal! zo
419
normal! zo
430
normal! zo
441
normal! zo
450
normal! zo
468
normal! zo
468
normal! zo
476
normal! zo
478
normal! zo
479
normal! zo
480
normal! zo
481
normal! zo
491
normal! zo
493
normal! zo
494
normal! zo
511
normal! zo
524
normal! zo
525
normal! zo
536
normal! zo
548
normal! zo
548
normal! zo
556
normal! zo
557
normal! zo
564
normal! zo
574
normal! zo
574
normal! zo
582
normal! zo
582
normal! zo
583
normal! zo
591
normal! zo
591
normal! zo
599
normal! zo
604
normal! zo
604
normal! zo
604
normal! zo
604
normal! zo
604
normal! zo
608
normal! zo
610
normal! zo
613
normal! zo
626
normal! zo
645
normal! zo
653
normal! zo
664
normal! zo
675
normal! zo
679
normal! zo
680
normal! zo
690
normal! zo
696
normal! zo
699
normal! zo
730
normal! zo
749
normal! zo
751
normal! zo
751
normal! zo
751
normal! zo
751
normal! zo
751
normal! zo
757
normal! zo
771
normal! zo
778
normal! zo
778
normal! zo
779
normal! zo
782
normal! zo
786
normal! zo
787
normal! zo
794
normal! zo
802
normal! zo
809
normal! zo
820
normal! zo
822
normal! zo
844
normal! zo
877
normal! zo
892
normal! zo
902
normal! zo
921
normal! zo
961
normal! zo
970
normal! zo
977
normal! zo
977
normal! zo
982
normal! zo
983
normal! zo
988
normal! zo
990
normal! zo
1005
normal! zo
1043
normal! zo
1059
normal! zo
1075
normal! zo
1075
normal! zo
1075
normal! zo
1075
normal! zo
1075
normal! zo
1075
normal! zo
1086
normal! zo
1102
normal! zo
1109
normal! zo
1111
normal! zo
1113
normal! zo
1114
normal! zo
1114
normal! zo
1114
normal! zo
1114
normal! zo
1114
normal! zo
1114
normal! zo
1114
normal! zo
1121
normal! zo
1133
normal! zo
1146
normal! zo
1154
normal! zo
1252
normal! zo
1263
normal! zo
1264
normal! zo
1268
normal! zo
1301
normal! zo
1303
normal! zo
1305
normal! zo
1338
normal! zo
1359
normal! zo
1363
normal! zo
1366
normal! zo
1383
normal! zo
1386
normal! zo
1392
normal! zo
1400
normal! zo
1438
normal! zo
1449
normal! zo
1452
normal! zo
1511
normal! zo
1519
normal! zo
1529
normal! zo
1529
normal! zo
1529
normal! zo
1529
normal! zo
1529
normal! zo
1534
normal! zo
1534
normal! zo
1537
normal! zo
1540
normal! zo
1555
normal! zo
1559
normal! zo
1563
normal! zo
1572
normal! zo
1638
normal! zo
1645
normal! zo
1646
normal! zo
1647
normal! zo
1658
normal! zo
1667
normal! zo
1668
normal! zo
1682
normal! zo
1684
normal! zo
1706
normal! zo
1717
normal! zo
1724
normal! zo
1761
normal! zo
1761
normal! zo
1761
normal! zo
1761
normal! zo
1777
normal! zo
1790
normal! zo
1801
normal! zo
1826
normal! zo
1829
normal! zo
1831
normal! zo
1845
normal! zo
1876
normal! zo
1885
normal! zo
1885
normal! zo
1928
normal! zo
1928
normal! zo
1928
normal! zo
1928
normal! zo
1931
normal! zo
1938
normal! zo
1938
normal! zo
1938
normal! zo
1938
normal! zo
1938
normal! zo
1938
normal! zo
1938
normal! zo
1956
normal! zo
1990
normal! zo
2003
normal! zo
2007
normal! zo
2009
normal! zo
2017
normal! zo
2017
normal! zo
2026
normal! zo
2029
normal! zo
2036
normal! zo
2055
normal! zo
2056
normal! zo
2057
normal! zo
2062
normal! zo
2062
normal! zo
2065
normal! zo
2067
normal! zo
2067
normal! zo
2069
normal! zo
2070
normal! zo
2070
normal! zo
2093
normal! zo
2114
normal! zo
2141
normal! zo
2158
normal! zo
2169
normal! zo
2180
normal! zo
2185
normal! zo
2199
normal! zo
2211
normal! zo
2212
normal! zo
2219
normal! zo
2225
normal! zo
2245
normal! zo
2291
normal! zo
2310
normal! zo
2386
normal! zo
2400
normal! zo
2402
normal! zo
2460
normal! zo
2465
normal! zo
2469
normal! zo
2475
normal! zo
2476
normal! zo
2476
normal! zo
2488
normal! zo
2488
normal! zo
2494
normal! zo
2494
normal! zo
2502
normal! zo
2515
normal! zo
2515
normal! zo
2516
normal! zo
2527
normal! zo
2536
normal! zo
2543
normal! zo
2554
normal! zo
2581
normal! zo
2652
normal! zo
2674
normal! zo
2677
normal! zo
2678
normal! zo
2678
normal! zo
2683
normal! zo
2684
normal! zo
2685
normal! zo
2685
normal! zo
2693
normal! zo
2698
normal! zo
2700
normal! zo
2700
normal! zo
2727
normal! zo
2730
normal! zo
2731
normal! zo
2807
normal! zo
2811
normal! zo
2812
normal! zo
2812
normal! zo
2814
normal! zo
2815
normal! zo
let s:l = 699 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
699
normal! 028|
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
let s:l = 317 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
317
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
66
normal! zo
70
normal! zo
97
normal! zo
108
normal! zo
let s:l = 77 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
77
normal! 030|
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 29 + 55) / 110)
exe '2resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 110)
exe '3resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 110)
exe '4resize ' . ((&lines * 30 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 110)
exe '5resize ' . ((&lines * 9 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 110)
exe '6resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 110)
exe '7resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 110)
exe '8resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 110)
exe '9resize ' . ((&lines * 1 + 27) / 54)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 110)
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
4wincmd w

" vim: ft=vim ro nowrap smc=128
