" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 28 agosto 2013 at 15:05:59.
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
badd +1175 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +310 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +2258 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +903 ginn/formularios/partes_de_fabricacion_balas.py
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
badd +479 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +280 ginn/formularios/ventana.py
badd +822 ginn/formularios/pedidos_de_venta.py
badd +1452 db/tablas.sql
badd +1958 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +9 ginn/formularios/presupuestos.py
badd +382 ginn/informes/presupuesto2.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +724 ginn/formularios/facturas_compra.py
badd +1126 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +812 ginn/formularios/albaranes_de_entrada.py
badd +1134 ginn/formularios/consulta_ventas.py
badd +37 ginn/formularios/__init__.py
badd +907 ginn/formularios/pagares_pagos.py
badd +331 ginn/formularios/ausencias.py
badd +67 ginn/formularios/partes_no_bloqueados.py
badd +46 ginn/formularios/gtkexcepthook.py
badd +664 ginn/framework/seeker.py
badd +13 ginn/formularios/crm_seguimiento_impagos.py
badd +203 ginn/formularios/productos.py
badd +1064 ginn/formularios/trazabilidad_articulos.py
badd +363 ginn/formularios/consulta_pagos.py
badd +13 ginn/formularios/consulta_vencimientos_pago.py
badd +500 ginn/formularios/trazabilidad.py
badd +9810 ginn/framework/pclases/__init__.py
badd +611 ginn/framework/pclases/superfacturaventa.py
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
badd +221 ginn/formularios/consumo_balas_partida.py
badd +553 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +753 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +628 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +523 ginn/formularios/postomatic.py
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
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 3 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 28 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
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
641
silent! normal zo
722
silent! normal zo
2052
silent! normal zo
2160
silent! normal zo
2160
silent! normal zo
2160
silent! normal zo
2160
silent! normal zo
2430
silent! normal zo
6451
silent! normal zo
6731
silent! normal zo
6757
silent! normal zo
6829
silent! normal zo
6942
silent! normal zo
7223
silent! normal zo
7544
silent! normal zo
8511
silent! normal zo
8524
silent! normal zo
8525
silent! normal zo
8526
silent! normal zo
9716
silent! normal zo
9756
silent! normal zo
9763
silent! normal zo
9796
silent! normal zo
9809
silent! normal zo
9812
silent! normal zo
9825
silent! normal zo
9828
silent! normal zo
9838
silent! normal zo
9840
silent! normal zo
9872
silent! normal zo
10066
silent! normal zo
10076
silent! normal zo
10082
silent! normal zo
10086
silent! normal zo
10113
silent! normal zo
10127
silent! normal zo
10142
silent! normal zo
10161
silent! normal zo
10181
silent! normal zo
10182
silent! normal zo
10183
silent! normal zo
10183
silent! normal zo
10183
silent! normal zo
10183
silent! normal zo
10183
silent! normal zo
10183
silent! normal zo
10183
silent! normal zo
10183
silent! normal zo
10183
silent! normal zo
10072
silent! normal zo
10073
silent! normal zo
10078
silent! normal zo
10084
silent! normal zo
10086
silent! normal zo
10094
silent! normal zo
10105
silent! normal zo
10119
silent! normal zo
10138
silent! normal zo
10150
silent! normal zo
10156
silent! normal zo
10160
silent! normal zo
10166
silent! normal zo
10190
silent! normal zo
10198
silent! normal zo
10207
silent! normal zo
10222
silent! normal zo
10231
silent! normal zo
10231
silent! normal zo
10231
silent! normal zo
10243
silent! normal zo
10263
silent! normal zo
10264
silent! normal zo
10265
silent! normal zo
10265
silent! normal zo
10265
silent! normal zo
10265
silent! normal zo
10265
silent! normal zo
10265
silent! normal zo
10265
silent! normal zo
10265
silent! normal zo
10265
silent! normal zo
10282
silent! normal zo
10285
silent! normal zo
10288
silent! normal zo
10288
silent! normal zo
10288
silent! normal zo
10291
silent! normal zo
10291
silent! normal zo
10291
silent! normal zo
10291
silent! normal zo
10301
silent! normal zo
10307
silent! normal zo
10311
silent! normal zo
10314
silent! normal zo
10320
silent! normal zo
10322
silent! normal zo
10325
silent! normal zo
10328
silent! normal zo
10333
silent! normal zo
10340
silent! normal zo
10344
silent! normal zo
10345
silent! normal zo
10345
silent! normal zo
10347
silent! normal zo
10348
silent! normal zo
10348
silent! normal zo
10350
silent! normal zo
10351
silent! normal zo
10351
silent! normal zo
10353
silent! normal zo
10354
silent! normal zo
10354
silent! normal zo
10356
silent! normal zo
10357
silent! normal zo
10357
silent! normal zo
10359
silent! normal zo
10360
silent! normal zo
10360
silent! normal zo
10362
silent! normal zo
10363
silent! normal zo
10363
silent! normal zo
10365
silent! normal zo
10368
silent! normal zo
10370
silent! normal zo
10370
silent! normal zo
10370
silent! normal zo
10377
silent! normal zo
10378
silent! normal zo
10387
silent! normal zo
10388
silent! normal zo
10397
silent! normal zo
13974
silent! normal zo
13993
silent! normal zo
14381
silent! normal zo
15377
silent! normal zo
15429
silent! normal zo
15489
silent! normal zo
15889
silent! normal zo
17729
silent! normal zo
18305
silent! normal zo
19545
silent! normal zo
let s:l = 10231 - ((2 * winheight(0) + 1) / 3)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10231
normal! 023l
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
194
silent! normal zo
286
silent! normal zo
292
silent! normal zo
292
silent! normal zo
292
silent! normal zo
292
silent! normal zo
292
silent! normal zo
292
silent! normal zo
1337
silent! normal zo
1391
silent! normal zo
1982
silent! normal zo
3528
silent! normal zo
3528
silent! normal zo
3517
silent! normal zo
3500
silent! normal zo
3528
silent! normal zo
3528
silent! normal zo
3528
silent! normal zo
3528
silent! normal zo
3534
silent! normal zo
3539
silent! normal zo
3545
silent! normal zo
3549
silent! normal zo
3565
silent! normal zo
3610
silent! normal zo
3610
silent! normal zo
3610
silent! normal zo
3610
silent! normal zo
3610
silent! normal zo
3610
silent! normal zo
3610
silent! normal zo
3650
silent! normal zo
3650
silent! normal zo
3650
silent! normal zo
3650
silent! normal zo
3650
silent! normal zo
3650
silent! normal zo
3650
silent! normal zo
3650
silent! normal zo
3650
silent! normal zo
3650
silent! normal zo
3656
silent! normal zo
3660
silent! normal zo
3660
silent! normal zo
3660
silent! normal zo
3660
silent! normal zo
3660
silent! normal zo
3662
silent! normal zo
3662
silent! normal zo
3662
silent! normal zo
3661
silent! normal zo
3672
silent! normal zo
3672
silent! normal zo
3672
silent! normal zo
3672
silent! normal zo
3672
silent! normal zo
3672
silent! normal zo
3672
silent! normal zo
3672
silent! normal zo
3672
silent! normal zo
3685
silent! normal zo
3690
silent! normal zo
3691
silent! normal zo
3691
silent! normal zo
3691
silent! normal zo
3691
silent! normal zo
3693
silent! normal zo
3693
silent! normal zo
3693
silent! normal zo
3699
silent! normal zo
3699
silent! normal zo
3699
silent! normal zo
3699
silent! normal zo
3699
silent! normal zo
3699
silent! normal zo
3699
silent! normal zo
3699
silent! normal zo
3699
silent! normal zo
3717
silent! normal zo
3717
silent! normal zo
3717
silent! normal zo
3717
silent! normal zo
3717
silent! normal zo
3717
silent! normal zo
3717
silent! normal zo
3717
silent! normal zo
3723
silent! normal zo
3726
silent! normal zo
3729
silent! normal zo
3728
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3737
silent! normal zo
3753
silent! normal zo
3757
silent! normal zo
3760
silent! normal zo
3845
silent! normal zo
3867
silent! normal zo
3867
silent! normal zo
let s:l = 1432 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1432
normal! 0
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
55
silent! normal zo
56
silent! normal zo
64
silent! normal zo
64
silent! normal zo
64
silent! normal zo
84
silent! normal zo
84
silent! normal zo
84
silent! normal zo
91
silent! normal zo
92
silent! normal zo
95
silent! normal zo
96
silent! normal zo
116
silent! normal zo
121
silent! normal zo
121
silent! normal zo
122
silent! normal zo
127
silent! normal zo
154
silent! normal zo
158
silent! normal zo
163
silent! normal zo
168
silent! normal zo
171
silent! normal zo
172
silent! normal zo
174
silent! normal zo
175
silent! normal zo
175
silent! normal zo
175
silent! normal zo
181
silent! normal zo
182
silent! normal zo
182
silent! normal zo
182
silent! normal zo
182
silent! normal zo
182
silent! normal zo
193
silent! normal zo
194
silent! normal zo
197
silent! normal zo
204
silent! normal zo
219
silent! normal zo
224
silent! normal zo
247
silent! normal zo
253
silent! normal zo
264
silent! normal zo
265
silent! normal zo
265
silent! normal zo
265
silent! normal zo
265
silent! normal zo
265
silent! normal zo
265
silent! normal zo
271
silent! normal zo
272
silent! normal zo
272
silent! normal zo
272
silent! normal zo
272
silent! normal zo
272
silent! normal zo
272
silent! normal zo
281
silent! normal zo
288
silent! normal zo
288
silent! normal zo
289
silent! normal zo
293
silent! normal zo
294
silent! normal zo
299
silent! normal zo
301
silent! normal zo
306
silent! normal zo
307
silent! normal zo
308
silent! normal zo
308
silent! normal zo
311
silent! normal zo
312
silent! normal zo
312
silent! normal zo
312
silent! normal zo
312
silent! normal zo
312
silent! normal zo
312
silent! normal zo
312
silent! normal zo
312
silent! normal zo
312
silent! normal zo
316
silent! normal zo
320
silent! normal zo
331
silent! normal zo
344
silent! normal zo
350
silent! normal zo
354
silent! normal zo
361
silent! normal zo
363
silent! normal zo
365
silent! normal zo
366
silent! normal zo
366
silent! normal zo
366
silent! normal zo
366
silent! normal zo
366
silent! normal zo
366
silent! normal zo
366
silent! normal zo
393
silent! normal zo
409
silent! normal zo
409
silent! normal zo
419
silent! normal zo
426
silent! normal zo
426
silent! normal zo
426
silent! normal zo
426
silent! normal zo
426
silent! normal zo
426
silent! normal zo
428
silent! normal zo
428
silent! normal zo
428
silent! normal zo
428
silent! normal zo
428
silent! normal zo
428
silent! normal zo
431
silent! normal zo
437
silent! normal zo
439
silent! normal zo
440
silent! normal zo
440
silent! normal zo
440
silent! normal zo
443
silent! normal zo
446
silent! normal zo
449
silent! normal zo
449
silent! normal zo
449
silent! normal zo
462
silent! normal zo
462
silent! normal zo
462
silent! normal zo
468
silent! normal zo
476
silent! normal zo
477
silent! normal zo
477
silent! normal zo
477
silent! normal zo
486
silent! normal zo
503
silent! normal zo
503
silent! normal zo
511
silent! normal zo
511
silent! normal zo
511
silent! normal zo
511
silent! normal zo
511
silent! normal zo
511
silent! normal zo
520
silent! normal zo
529
silent! normal zo
530
silent! normal zo
535
silent! normal zo
536
silent! normal zo
547
silent! normal zo
547
silent! normal zo
547
silent! normal zo
542
silent! normal zo
547
silent! normal zo
547
silent! normal zo
547
silent! normal zo
547
silent! normal zo
547
silent! normal zo
549
silent! normal zo
549
silent! normal zo
563
silent! normal zo
571
silent! normal zo
574
silent! normal zo
580
silent! normal zo
581
silent! normal zo
588
silent! normal zo
592
silent! normal zo
593
silent! normal zo
599
silent! normal zo
602
silent! normal zo
603
silent! normal zo
605
silent! normal zo
606
silent! normal zo
608
silent! normal zo
609
silent! normal zo
609
silent! normal zo
609
silent! normal zo
609
silent! normal zo
619
silent! normal zo
624
silent! normal zo
624
silent! normal zo
624
silent! normal zo
624
silent! normal zo
624
silent! normal zo
628
silent! normal zo
629
silent! normal zo
631
silent! normal zo
631
silent! normal zo
631
silent! normal zo
631
silent! normal zo
634
silent! normal zo
636
silent! normal zo
638
silent! normal zo
638
silent! normal zo
640
silent! normal zo
641
silent! normal zo
641
silent! normal zo
654
silent! normal zo
654
silent! normal zo
654
silent! normal zo
654
silent! normal zo
654
silent! normal zo
654
silent! normal zo
654
silent! normal zo
654
silent! normal zo
657
silent! normal zo
664
silent! normal zo
666
silent! normal zo
669
silent! normal zo
671
silent! normal zo
688
silent! normal zo
691
silent! normal zo
706
silent! normal zo
712
silent! normal zo
715
silent! normal zo
715
silent! normal zo
715
silent! normal zo
726
silent! normal zo
739
silent! normal zo
741
silent! normal zo
762
silent! normal zo
762
silent! normal zo
762
silent! normal zo
771
silent! normal zo
782
silent! normal zo
782
silent! normal zo
782
silent! normal zo
782
silent! normal zo
782
silent! normal zo
782
silent! normal zo
782
silent! normal zo
785
silent! normal zo
785
silent! normal zo
785
silent! normal zo
785
silent! normal zo
785
silent! normal zo
785
silent! normal zo
786
silent! normal zo
790
silent! normal zo
798
silent! normal zo
803
silent! normal zo
804
silent! normal zo
804
silent! normal zo
804
silent! normal zo
804
silent! normal zo
806
silent! normal zo
807
silent! normal zo
807
silent! normal zo
807
silent! normal zo
807
silent! normal zo
809
silent! normal zo
810
silent! normal zo
810
silent! normal zo
810
silent! normal zo
810
silent! normal zo
814
silent! normal zo
814
silent! normal zo
824
silent! normal zo
824
silent! normal zo
825
silent! normal zo
825
silent! normal zo
825
silent! normal zo
835
silent! normal zo
836
silent! normal zo
836
silent! normal zo
836
silent! normal zo
847
silent! normal zo
856
silent! normal zo
858
silent! normal zo
889
silent! normal zo
890
silent! normal zo
890
silent! normal zo
891
silent! normal zo
896
silent! normal zo
905
silent! normal zo
909
silent! normal zo
911
silent! normal zo
911
silent! normal zo
911
silent! normal zo
921
silent! normal zo
924
silent! normal zo
927
silent! normal zo
939
silent! normal zo
934
silent! normal zo
950
silent! normal zo
962
silent! normal zo
968
silent! normal zo
971
silent! normal zo
971
silent! normal zo
971
silent! normal zo
973
silent! normal zo
973
silent! normal zo
973
silent! normal zo
973
silent! normal zo
975
silent! normal zo
982
silent! normal zo
984
silent! normal zo
1006
silent! normal zo
1006
silent! normal zo
1006
silent! normal zo
1014
silent! normal zo
1022
silent! normal zo
1022
silent! normal zo
1022
silent! normal zo
1022
silent! normal zo
1022
silent! normal zo
1022
silent! normal zo
1023
silent! normal zo
1026
silent! normal zo
1031
silent! normal zo
1038
silent! normal zo
1038
silent! normal zo
1048
silent! normal zo
1048
silent! normal zo
1049
silent! normal zo
1049
silent! normal zo
1049
silent! normal zo
1059
silent! normal zo
1060
silent! normal zo
1060
silent! normal zo
1060
silent! normal zo
1070
silent! normal zo
1078
silent! normal zo
1080
silent! normal zo
1085
silent! normal zo
1086
silent! normal zo
1088
silent! normal zo
1089
silent! normal zo
1089
silent! normal zo
1090
silent! normal zo
1096
silent! normal zo
1097
silent! normal zo
1097
silent! normal zo
1097
silent! normal zo
1097
silent! normal zo
1097
silent! normal zo
1097
silent! normal zo
1099
silent! normal zo
1100
silent! normal zo
1100
silent! normal zo
1100
silent! normal zo
1100
silent! normal zo
1101
silent! normal zo
1114
silent! normal zo
1123
silent! normal zo
1127
silent! normal zo
1129
silent! normal zo
1129
silent! normal zo
1129
silent! normal zo
1137
silent! normal zo
1142
silent! normal zo
1142
silent! normal zo
1142
silent! normal zo
1142
silent! normal zo
1142
silent! normal zo
1142
silent! normal zo
1142
silent! normal zo
let s:l = 543 - ((11 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
543
normal! 043l
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
let s:l = 318 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
318
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
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
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
silent! normal zo
51
silent! normal zo
66
silent! normal zo
69
silent! normal zo
94
silent! normal zo
105
silent! normal zo
let s:l = 80 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
80
normal! 043l
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
silent! normal zo
230
silent! normal zo
262
silent! normal zo
262
silent! normal zo
339
silent! normal zo
340
silent! normal zo
345
silent! normal zo
350
silent! normal zo
351
silent! normal zo
356
silent! normal zo
362
silent! normal zo
467
silent! normal zo
579
silent! normal zo
595
silent! normal zo
725
silent! normal zo
734
silent! normal zo
834
silent! normal zo
850
silent! normal zo
850
silent! normal zo
850
silent! normal zo
850
silent! normal zo
961
silent! normal zo
966
silent! normal zo
1531
silent! normal zo
1727
silent! normal zo
1728
silent! normal zo
1728
silent! normal zo
1728
silent! normal zo
1728
silent! normal zo
1739
silent! normal zo
1740
silent! normal zo
1744
silent! normal zo
1744
silent! normal zo
1745
silent! normal zo
1752
silent! normal zo
1753
silent! normal zo
1804
silent! normal zo
3253
silent! normal zo
3260
silent! normal zo
3265
silent! normal zo
3272
silent! normal zo
3276
silent! normal zo
3281
silent! normal zo
3282
silent! normal zo
3282
silent! normal zo
3282
silent! normal zo
3288
silent! normal zo
3293
silent! normal zo
3294
silent! normal zo
3299
silent! normal zo
let s:l = 1753 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1753
normal! 036l
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 3 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 28 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
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
