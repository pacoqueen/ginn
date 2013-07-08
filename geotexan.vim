" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 08 julio 2013 at 15:13:18.
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
badd +1247 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +638 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +864 ginn/formularios/productos_de_venta_rollos.py
badd +507 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +578 ginn/formularios/productos_de_venta_especial.py
badd +1604 ginn/formularios/partes_de_fabricacion_balas.py
badd +399 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1583 ginn/formularios/partes_de_fabricacion_rollos.py
badd +550 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +109 ginn/formularios/launcher.py
badd +155 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +770 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +7583 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +1 ginn/formularios/facturas_venta.py
badd +468 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +678 ginn/formularios/ventana.py
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
badd +64 ginn/formularios/trazabilidad.py
badd +15873 ginn/framework/pclases/__init__.py
badd +398 ginn/framework/pclases/superfacturaventa.py
badd +4 ginn/framework/pclases/facturaventa.py
badd +647 ginn/formularios/consulta_mensual_nominas.py
badd +1 ginn/informes/treeview2pdf.py
badd +129 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +0 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
args formularios/auditviewer.py
set lines=58 columns=111
edit ginn/informes/norma2013.py
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
wincmd _ | wincmd |
split
11wincmd k
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
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 34 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 29) / 58)
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
exe '13resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 13resize ' . ((&columns * 80 + 55) / 111)
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
let s:l = 13 - ((9 * winheight(0) + 17) / 34)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
13
normal! 010|
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
1934
normal! zo
2124
normal! zo
2322
normal! zo
2499
normal! zo
2557
normal! zo
3084
normal! zo
3399
normal! zo
3399
normal! zo
3399
normal! zo
3399
normal! zo
3399
normal! zo
3399
normal! zo
3399
normal! zo
3412
normal! zo
3418
normal! zo
3422
normal! zo
3488
normal! zo
3488
normal! zo
3488
normal! zo
3488
normal! zo
3488
normal! zo
3488
normal! zo
3488
normal! zo
3488
normal! zo
3493
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
3515
normal! zo
3515
normal! zo
3515
normal! zo
3515
normal! zo
3515
normal! zo
3515
normal! zo
3515
normal! zo
3515
normal! zo
3515
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
3523
normal! zo
let s:l = 3488 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3488
normal! 032|
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
normal! zo
181
normal! zo
197
normal! zo
217
normal! zo
217
normal! zo
217
normal! zo
217
normal! zo
let s:l = 606 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
606
normal! 09|
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
normal! zo
64
normal! zo
72
normal! zo
72
normal! zo
let s:l = 682 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
682
normal! 05|
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
normal! zo
169
normal! zo
191
normal! zo
196
normal! zo
279
normal! zo
326
normal! zo
let s:l = 37 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
37
normal! 024|
wincmd w
argglobal
edit ginn/informes/treeview2pdf.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 265 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
265
normal! 05|
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
720
normal! zo
732
normal! zo
736
normal! zo
737
normal! zo
741
normal! zo
742
normal! zo
742
normal! zo
742
normal! zo
742
normal! zo
1605
normal! zo
1625
normal! zo
1828
normal! zo
1878
normal! zo
1967
normal! zo
1977
normal! zo
4055
normal! zo
4264
normal! zo
4294
normal! zo
4756
normal! zo
4933
normal! zo
4947
normal! zo
4953
normal! zo
4969
normal! zo
4980
normal! zo
6098
normal! zo
6224
normal! zo
6239
normal! zo
6246
normal! zo
6246
normal! zo
6246
normal! zo
6246
normal! zo
6246
normal! zo
6246
normal! zo
6246
normal! zo
6246
normal! zo
6249
normal! zo
6249
normal! zo
6249
normal! zo
6249
normal! zo
6249
normal! zo
6249
normal! zo
6249
normal! zo
6249
normal! zo
6249
normal! zo
6269
normal! zo
6393
normal! zo
6409
normal! zo
6440
normal! zo
6463
normal! zo
6470
normal! zo
6488
normal! zo
6495
normal! zo
6503
normal! zo
6530
normal! zo
6530
normal! zo
6530
normal! zo
6530
normal! zo
6530
normal! zo
6548
normal! zo
6554
normal! zo
6554
normal! zo
6573
normal! zo
6581
normal! zo
6581
normal! zo
6585
normal! zo
6589
normal! zo
6606
normal! zo
6607
normal! zo
6607
normal! zo
6613
normal! zo
6618
normal! zo
6639
normal! zo
6652
normal! zo
6671
normal! zo
6677
normal! zo
6681
normal! zo
6685
normal! zo
6700
normal! zo
6708
normal! zo
6720
normal! zo
6728
normal! zo
6734
normal! zo
6734
normal! zo
6734
normal! zo
6734
normal! zo
6734
normal! zo
6734
normal! zo
6734
normal! zo
6746
normal! zo
6752
normal! zo
6760
normal! zo
6773
normal! zo
6779
normal! zo
7533
normal! zo
8172
normal! zo
8172
normal! zo
8172
normal! zo
8172
normal! zo
8172
normal! zo
8172
normal! zo
8172
normal! zo
8200
normal! zo
8207
normal! zo
8214
normal! zo
10510
normal! zo
10692
normal! zo
10701
normal! zo
10720
normal! zo
10773
normal! zo
10788
normal! zo
10829
normal! zo
11412
normal! zo
11412
normal! zo
11412
normal! zo
11998
normal! zo
11998
normal! zo
11998
normal! zo
11998
normal! zo
11998
normal! zo
12034
normal! zo
12035
normal! zo
12036
normal! zo
12082
normal! zo
12083
normal! zo
12177
normal! zo
12178
normal! zo
12217
normal! zo
12218
normal! zo
12371
normal! zo
12371
normal! zo
12410
normal! zo
12411
normal! zo
12412
normal! zo
12472
normal! zo
12473
normal! zo
12533
normal! zo
12534
normal! zo
12594
normal! zo
12595
normal! zo
12735
normal! zo
12736
normal! zo
12737
normal! zo
12738
normal! zo
12738
normal! zo
12758
normal! zo
12759
normal! zo
12760
normal! zo
12760
normal! zo
12772
normal! zo
12773
normal! zo
12774
normal! zo
12774
normal! zo
12791
normal! zo
12792
normal! zo
12793
normal! zo
12794
normal! zo
12794
normal! zo
12815
normal! zo
12816
normal! zo
12817
normal! zo
12817
normal! zo
12829
normal! zo
12830
normal! zo
12831
normal! zo
12831
normal! zo
12907
normal! zo
12908
normal! zo
12909
normal! zo
12910
normal! zo
12910
normal! zo
12931
normal! zo
12932
normal! zo
12933
normal! zo
12933
normal! zo
12945
normal! zo
12946
normal! zo
12947
normal! zo
12947
normal! zo
12963
normal! zo
12964
normal! zo
12965
normal! zo
12966
normal! zo
12966
normal! zo
12987
normal! zo
12988
normal! zo
12989
normal! zo
12989
normal! zo
13001
normal! zo
13002
normal! zo
13003
normal! zo
13003
normal! zo
13087
normal! zo
13089
normal! zo
13090
normal! zo
13091
normal! zo
13091
normal! zo
13102
normal! zo
13103
normal! zo
13104
normal! zo
13104
normal! zo
13119
normal! zo
13120
normal! zo
13121
normal! zo
13122
normal! zo
13122
normal! zo
13133
normal! zo
13134
normal! zo
13135
normal! zo
13135
normal! zo
13756
normal! zo
13767
normal! zo
13778
normal! zo
13797
normal! zo
13848
normal! zo
13885
normal! zo
13886
normal! zo
14049
normal! zo
14091
normal! zo
14919
normal! zo
14923
normal! zo
14923
normal! zo
14923
normal! zo
14923
normal! zo
14923
normal! zo
14938
normal! zo
14957
normal! zo
14969
normal! zo
14972
normal! zo
14972
normal! zo
14972
normal! zo
14972
normal! zo
14980
normal! zo
15004
normal! zo
15012
normal! zo
15014
normal! zo
15027
normal! zo
15036
normal! zo
15047
normal! zo
15048
normal! zo
15057
normal! zo
15057
normal! zo
15064
normal! zo
15073
normal! zo
15077
normal! zo
15078
normal! zo
15090
normal! zo
15109
normal! zo
15131
normal! zo
15136
normal! zo
15137
normal! zo
15137
normal! zo
15140
normal! zo
15141
normal! zo
15141
normal! zo
15141
normal! zo
15144
normal! zo
15144
normal! zo
15144
normal! zo
15148
normal! zo
15148
normal! zo
15148
normal! zo
15148
normal! zo
15148
normal! zo
15148
normal! zo
15148
normal! zo
15148
normal! zo
15148
normal! zo
15153
normal! zo
15181
normal! zo
15201
normal! zo
15208
normal! zo
15211
normal! zo
15214
normal! zo
15233
normal! zo
15254
normal! zo
15272
normal! zo
15279
normal! zo
15293
normal! zo
15308
normal! zo
15327
normal! zo
15338
normal! zo
15350
normal! zo
15368
normal! zo
15378
normal! zo
15383
normal! zo
15383
normal! zo
15383
normal! zo
15383
normal! zo
15383
normal! zo
15383
normal! zo
15383
normal! zo
15383
normal! zo
15383
normal! zo
15383
normal! zo
15383
normal! zo
15385
normal! zo
15385
normal! zo
15385
normal! zo
15389
normal! zo
15390
normal! zo
15398
normal! zo
15412
normal! zo
15428
normal! zo
15437
normal! zo
15445
normal! zo
15448
normal! zo
15453
normal! zo
15467
normal! zo
15477
normal! zo
15481
normal! zo
15486
normal! zo
15492
normal! zo
15498
normal! zo
15498
normal! zo
15498
normal! zo
15500
normal! zo
15500
normal! zo
15500
normal! zo
15506
normal! zo
15510
normal! zo
15511
normal! zo
15511
normal! zo
15511
normal! zo
15511
normal! zo
15511
normal! zo
15511
normal! zo
15518
normal! zo
15519
normal! zo
15519
normal! zo
15531
normal! zo
15531
normal! zo
15531
normal! zo
15561
normal! zo
15562
normal! zo
15562
normal! zo
15562
normal! zo
15562
normal! zo
15562
normal! zo
15562
normal! zo
15564
normal! zo
15569
normal! zo
15575
normal! zo
15582
normal! zo
15583
normal! zo
15583
normal! zo
15586
normal! zo
15591
normal! zo
15597
normal! zo
15608
normal! zo
15625
normal! zo
15636
normal! zo
15637
normal! zo
15637
normal! zo
15639
normal! zo
15640
normal! zo
15640
normal! zo
15646
normal! zo
15647
normal! zo
15648
normal! zo
15649
normal! zo
15649
normal! zo
15649
normal! zo
15649
normal! zo
15655
normal! zo
15656
normal! zo
15657
normal! zo
15657
normal! zo
15657
normal! zo
15657
normal! zo
15664
normal! zo
15675
normal! zo
15682
normal! zo
18537
normal! zo
18695
normal! zo
18738
normal! zo
19107
normal! zo
19195
normal! zo
19213
normal! zo
19574
normal! zo
19732
normal! zo
let s:l = 19220 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19220
normal! 088|
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
let s:l = 3 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3
normal! 0
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
normal! zo
122
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
174
normal! zo
189
normal! zo
218
normal! zo
254
normal! zo
264
normal! zo
285
normal! zo
286
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
288
normal! zo
291
normal! zo
293
normal! zo
295
normal! zo
295
normal! zo
321
normal! zo
321
normal! zc
329
normal! zc
337
normal! zo
339
normal! zo
342
normal! zo
344
normal! zo
349
normal! zc
363
normal! zo
363
normal! zc
403
normal! zo
405
normal! zo
403
normal! zc
431
normal! zo
431
normal! zc
470
normal! zo
470
normal! zc
492
normal! zo
496
normal! zo
501
normal! zo
492
normal! zc
630
normal! zo
638
normal! zo
641
normal! zo
654
normal! zo
657
normal! zo
658
normal! zo
661
normal! zo
664
normal! zo
665
normal! zo
668
normal! zo
671
normal! zo
672
normal! zo
672
normal! zo
672
normal! zo
672
normal! zo
672
normal! zo
672
normal! zo
676
normal! zo
677
normal! zo
677
normal! zo
677
normal! zo
677
normal! zo
677
normal! zo
677
normal! zo
682
normal! zo
683
normal! zo
692
normal! zo
703
normal! zo
706
normal! zo
709
normal! zo
712
normal! zo
715
normal! zo
718
normal! zo
723
normal! zo
726
normal! zo
727
normal! zo
760
normal! zo
896
normal! zo
900
normal! zo
902
normal! zo
906
normal! zo
910
normal! zo
911
normal! zo
911
normal! zo
924
normal! zo
926
normal! zo
929
normal! zo
933
normal! zo
937
normal! zo
938
normal! zo
938
normal! zo
1124
normal! zo
1158
normal! zo
1176
normal! zo
1185
normal! zo
1186
normal! zo
1186
normal! zo
1186
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1194
normal! zo
1210
normal! zo
1337
normal! zo
1366
normal! zo
1386
normal! zo
1471
normal! zo
1842
normal! zo
1900
normal! zo
1915
normal! zo
1956
normal! zo
2004
normal! zo
2005
normal! zo
2008
normal! zo
2263
normal! zo
2266
normal! zo
2273
normal! zo
2516
normal! zo
2524
normal! zo
2525
normal! zo
2546
normal! zo
2559
normal! zo
2560
normal! zo
2582
normal! zo
2651
normal! zo
2651
normal! zo
2651
normal! zo
2651
normal! zo
2656
normal! zo
2785
normal! zo
2805
normal! zo
2806
normal! zo
2806
normal! zo
2806
normal! zo
let s:l = 2291 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2291
normal! 045|
wincmd w
argglobal
edit ginn/formularios/partes_de_fabricacion_balas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
108
normal! zo
109
normal! zo
121
normal! zo
121
normal! zo
let s:l = 1608 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1608
normal! 0
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
1570
normal! zo
1581
normal! zo
1582
normal! zo
1583
normal! zo
let s:l = 1591 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1591
normal! 030|
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
normal! zo
684
normal! zo
692
normal! zo
697
normal! zo
715
normal! zo
720
normal! zo
855
normal! zo
920
normal! zo
926
normal! zo
974
normal! zo
985
normal! zo
986
normal! zo
992
normal! zo
1894
normal! zo
1912
normal! zo
let s:l = 694 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
694
normal! 048|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 34 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 29) / 58)
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
exe '13resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 13resize ' . ((&columns * 80 + 55) / 111)
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
