" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 31 octubre 2013 at 17:22:39.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata
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
badd +1637 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1627 ginn/formularios/facturas_venta.py
badd +419 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +908 ginn/formularios/ventana.py
badd +1899 ginn/formularios/pedidos_de_venta.py
badd +1 db/tablas.sql
badd +1732 ginn/formularios/albaranes_de_salida.py
badd +170 ginn/formularios/presupuesto.py
badd +2236 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
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
badd +150 ginn/informes/presupuesto2.py
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
badd +85 ginn/formularios/consulta_existenciasRollos.py
badd +91 ginn/formularios/listado_rollos_defectuosos.py
badd +3498 ginn/formularios/consulta_global.py
badd +195 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
badd +1 ginn/informes/presupuesto.py
args formularios/auditviewer.py
set lines=43 columns=103
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
5wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 22 + 51) / 103)
exe '2resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 103)
exe '3resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 103)
exe '4resize ' . ((&lines * 31 + 21) / 43)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 103)
exe '5resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 103)
exe '6resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 103)
exe '7resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 103)
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
18147
normal! zo
18154
normal! zo
18161
normal! zo
18162
normal! zo
18162
normal! zo
18162
normal! zo
18164
normal! zo
18165
normal! zo
18165
normal! zo
18165
normal! zo
18241
normal! zo
18308
normal! zo
18319
normal! zo
18369
normal! zo
18426
normal! zo
18436
normal! zo
18484
normal! zo
18537
normal! zo
18778
normal! zo
18800
normal! zo
18859
normal! zo
19057
normal! zo
19526
normal! zo
19765
normal! zo
19938
normal! zo
19942
normal! zo
19942
normal! zo
20031
normal! zo
20094
normal! zo
20416
normal! zo
let s:l = 18165 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
18165
normal! 058|
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
266
normal! zo
268
normal! zo
268
normal! zo
277
normal! zo
279
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
313
normal! zo
320
normal! zo
321
normal! zo
322
normal! zo
331
normal! zo
347
normal! zo
348
normal! zo
348
normal! zo
349
normal! zo
354
normal! zo
357
normal! zo
363
normal! zo
374
normal! zo
395
normal! zo
400
normal! zo
411
normal! zo
411
normal! zo
412
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
421
normal! zo
432
normal! zo
443
normal! zo
446
normal! zo
446
normal! zo
446
normal! zo
447
normal! zo
452
normal! zo
470
normal! zo
470
normal! zo
478
normal! zo
480
normal! zo
481
normal! zo
482
normal! zo
483
normal! zo
493
normal! zo
495
normal! zo
496
normal! zo
513
normal! zo
526
normal! zo
527
normal! zo
538
normal! zo
550
normal! zo
550
normal! zo
558
normal! zo
559
normal! zo
566
normal! zo
576
normal! zo
576
normal! zo
584
normal! zo
584
normal! zo
585
normal! zo
593
normal! zo
593
normal! zo
601
normal! zo
606
normal! zo
606
normal! zo
606
normal! zo
606
normal! zo
606
normal! zo
610
normal! zo
612
normal! zo
615
normal! zo
628
normal! zo
647
normal! zo
655
normal! zo
666
normal! zo
677
normal! zo
681
normal! zo
682
normal! zo
692
normal! zo
698
normal! zo
701
normal! zo
732
normal! zo
751
normal! zo
753
normal! zo
753
normal! zo
753
normal! zo
753
normal! zo
753
normal! zo
759
normal! zo
773
normal! zo
780
normal! zo
780
normal! zo
781
normal! zo
784
normal! zo
788
normal! zo
789
normal! zo
796
normal! zo
804
normal! zo
811
normal! zo
822
normal! zo
824
normal! zo
846
normal! zo
879
normal! zo
894
normal! zo
904
normal! zo
923
normal! zo
963
normal! zo
972
normal! zo
979
normal! zo
979
normal! zo
984
normal! zo
985
normal! zo
990
normal! zo
992
normal! zo
1007
normal! zo
1040
normal! zo
1056
normal! zo
1072
normal! zo
1072
normal! zo
1072
normal! zo
1072
normal! zo
1072
normal! zo
1072
normal! zo
1083
normal! zo
1088
normal! zo
1089
normal! zo
1089
normal! zo
1090
normal! zo
1099
normal! zo
1106
normal! zo
1108
normal! zo
1110
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
1111
normal! zo
1118
normal! zo
1130
normal! zo
1141
normal! zo
1142
normal! zo
1142
normal! zo
1150
normal! zo
1158
normal! zo
1256
normal! zo
1267
normal! zo
1268
normal! zo
1272
normal! zo
1305
normal! zo
1307
normal! zo
1309
normal! zo
1316
normal! zo
1320
normal! zo
1342
normal! zo
1343
normal! zo
1348
normal! zo
1363
normal! zo
1367
normal! zo
1370
normal! zo
1387
normal! zo
1390
normal! zo
1396
normal! zo
1404
normal! zo
1442
normal! zo
1453
normal! zo
1456
normal! zo
1515
normal! zo
1523
normal! zo
1533
normal! zo
1533
normal! zo
1533
normal! zo
1533
normal! zo
1533
normal! zo
1538
normal! zo
1538
normal! zo
1541
normal! zo
1544
normal! zo
1559
normal! zo
1563
normal! zo
1567
normal! zo
1576
normal! zo
1642
normal! zo
1649
normal! zo
1650
normal! zo
1651
normal! zo
1662
normal! zo
1671
normal! zo
1672
normal! zo
1686
normal! zo
1688
normal! zo
1710
normal! zo
1721
normal! zo
1728
normal! zo
1765
normal! zo
1765
normal! zo
1765
normal! zo
1765
normal! zo
1781
normal! zo
1794
normal! zo
1805
normal! zo
1830
normal! zo
1833
normal! zo
1835
normal! zo
1849
normal! zo
1880
normal! zo
1889
normal! zo
1889
normal! zo
1902
normal! zo
1903
normal! zo
1932
normal! zo
1932
normal! zo
1932
normal! zo
1932
normal! zo
1935
normal! zo
1942
normal! zo
1942
normal! zo
1942
normal! zo
1942
normal! zo
1942
normal! zo
1942
normal! zo
1942
normal! zo
1960
normal! zo
1994
normal! zo
2007
normal! zo
2011
normal! zo
2013
normal! zo
2021
normal! zo
2021
normal! zo
2030
normal! zo
2033
normal! zo
2040
normal! zo
2059
normal! zo
2060
normal! zo
2061
normal! zo
2066
normal! zo
2066
normal! zo
2067
normal! zo
2069
normal! zo
2071
normal! zo
2071
normal! zo
2073
normal! zo
2074
normal! zo
2074
normal! zo
2097
normal! zo
2118
normal! zo
2145
normal! zo
2162
normal! zo
2173
normal! zo
2184
normal! zo
2189
normal! zo
2203
normal! zo
2215
normal! zo
2216
normal! zo
2223
normal! zo
2229
normal! zo
2249
normal! zo
2295
normal! zo
2314
normal! zo
2390
normal! zo
2404
normal! zo
2406
normal! zo
2464
normal! zo
2469
normal! zo
2473
normal! zo
2479
normal! zo
2480
normal! zo
2480
normal! zo
2492
normal! zo
2492
normal! zo
2498
normal! zo
2498
normal! zo
2506
normal! zo
2519
normal! zo
2519
normal! zo
2520
normal! zo
2531
normal! zo
2540
normal! zo
2547
normal! zo
2558
normal! zo
2585
normal! zo
2656
normal! zo
2678
normal! zo
2681
normal! zo
2682
normal! zo
2682
normal! zo
2687
normal! zo
2688
normal! zo
2689
normal! zo
2689
normal! zo
2697
normal! zo
2702
normal! zo
2704
normal! zo
2704
normal! zo
2705
normal! zo
2705
normal! zo
2732
normal! zo
2735
normal! zo
2736
normal! zo
2812
normal! zo
2816
normal! zo
2817
normal! zo
2817
normal! zo
2819
normal! zo
2820
normal! zo
let s:l = 2707 - ((18 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2707
normal! 061|
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
normal! 0250|
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
exe 'vert 1resize ' . ((&columns * 22 + 51) / 103)
exe '2resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 2resize ' . ((&columns * 80 + 51) / 103)
exe '3resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 3resize ' . ((&columns * 80 + 51) / 103)
exe '4resize ' . ((&lines * 31 + 21) / 43)
exe 'vert 4resize ' . ((&columns * 80 + 51) / 103)
exe '5resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 5resize ' . ((&columns * 80 + 51) / 103)
exe '6resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 6resize ' . ((&columns * 80 + 51) / 103)
exe '7resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 7resize ' . ((&columns * 80 + 51) / 103)
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
