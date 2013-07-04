" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 04 julio 2013 at 15:24:55.
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
badd +1910 ginn/formularios/clientes.py
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
badd +166 ginn/formularios/menu.py
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
badd +64 ginn/formularios/trazabilidad.py
badd +15873 ginn/framework/pclases/__init__.py
badd +398 ginn/framework/pclases/superfacturaventa.py
badd +4 ginn/framework/pclases/facturaventa.py
badd +647 ginn/formularios/consulta_mensual_nominas.py
badd +0 ginn/informes/treeview2pdf.py
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
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 29) / 58)
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
exe '10resize ' . ((&lines * 38 + 29) / 58)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
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
let s:l = 606 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
606
normal! 08l
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
let s:l = 682 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
682
normal! 04l
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
let s:l = 37 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
37
normal! 023l
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
normal! 04l
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
silent! normal zo
732
silent! normal zo
736
silent! normal zo
737
silent! normal zo
741
silent! normal zo
742
silent! normal zo
742
silent! normal zo
742
silent! normal zo
742
silent! normal zo
1605
silent! normal zo
1625
silent! normal zo
1828
silent! normal zo
1878
silent! normal zo
1967
silent! normal zo
1977
silent! normal zo
4055
silent! normal zo
4264
silent! normal zo
4294
silent! normal zo
4756
silent! normal zo
4933
silent! normal zo
4947
silent! normal zo
4953
silent! normal zo
4969
silent! normal zo
4980
silent! normal zo
6098
silent! normal zo
6224
silent! normal zo
6239
silent! normal zo
6246
silent! normal zo
6246
silent! normal zo
6246
silent! normal zo
6246
silent! normal zo
6246
silent! normal zo
6246
silent! normal zo
6246
silent! normal zo
6246
silent! normal zo
6249
silent! normal zo
6249
silent! normal zo
6249
silent! normal zo
6249
silent! normal zo
6249
silent! normal zo
6249
silent! normal zo
6249
silent! normal zo
6249
silent! normal zo
6249
silent! normal zo
6269
silent! normal zo
6393
silent! normal zo
6409
silent! normal zo
6440
silent! normal zo
6463
silent! normal zo
6470
silent! normal zo
6488
silent! normal zo
6495
silent! normal zo
6503
silent! normal zo
6530
silent! normal zo
6530
silent! normal zo
6530
silent! normal zo
6530
silent! normal zo
6530
silent! normal zo
6548
silent! normal zo
6554
silent! normal zo
6554
silent! normal zo
6573
silent! normal zo
6581
silent! normal zo
6581
silent! normal zo
6585
silent! normal zo
6589
silent! normal zo
6606
silent! normal zo
6607
silent! normal zo
6607
silent! normal zo
6613
silent! normal zo
6618
silent! normal zo
6639
silent! normal zo
6652
silent! normal zo
6671
silent! normal zo
6677
silent! normal zo
6681
silent! normal zo
6685
silent! normal zo
6700
silent! normal zo
6708
silent! normal zo
6720
silent! normal zo
6728
silent! normal zo
6734
silent! normal zo
6734
silent! normal zo
6734
silent! normal zo
6734
silent! normal zo
6734
silent! normal zo
6734
silent! normal zo
6734
silent! normal zo
6746
silent! normal zo
6752
silent! normal zo
6760
silent! normal zo
6773
silent! normal zo
6779
silent! normal zo
7533
silent! normal zo
8172
silent! normal zo
8200
silent! normal zo
8207
silent! normal zo
8214
silent! normal zo
10510
silent! normal zo
10692
silent! normal zo
10701
silent! normal zo
10720
silent! normal zo
10773
silent! normal zo
10788
silent! normal zo
10829
silent! normal zo
11412
silent! normal zo
11998
silent! normal zo
12034
silent! normal zo
12035
silent! normal zo
12036
silent! normal zo
12082
silent! normal zo
12083
silent! normal zo
12177
silent! normal zo
12178
silent! normal zo
12217
silent! normal zo
12218
silent! normal zo
12371
silent! normal zo
12410
silent! normal zo
12411
silent! normal zo
12412
silent! normal zo
12472
silent! normal zo
12473
silent! normal zo
12533
silent! normal zo
12534
silent! normal zo
12594
silent! normal zo
12595
silent! normal zo
12735
silent! normal zo
12736
silent! normal zo
12737
silent! normal zo
12738
silent! normal zo
12738
silent! normal zo
12758
silent! normal zo
12759
silent! normal zo
12760
silent! normal zo
12760
silent! normal zo
12772
silent! normal zo
12773
silent! normal zo
12774
silent! normal zo
12774
silent! normal zo
12791
silent! normal zo
12792
silent! normal zo
12793
silent! normal zo
12794
silent! normal zo
12794
silent! normal zo
12815
silent! normal zo
12816
silent! normal zo
12817
silent! normal zo
12817
silent! normal zo
12829
silent! normal zo
12830
silent! normal zo
12831
silent! normal zo
12831
silent! normal zo
12907
silent! normal zo
12908
silent! normal zo
12909
silent! normal zo
12910
silent! normal zo
12910
silent! normal zo
12931
silent! normal zo
12932
silent! normal zo
12933
silent! normal zo
12933
silent! normal zo
12945
silent! normal zo
12946
silent! normal zo
12947
silent! normal zo
12947
silent! normal zo
12963
silent! normal zo
12964
silent! normal zo
12965
silent! normal zo
12966
silent! normal zo
12966
silent! normal zo
12987
silent! normal zo
12988
silent! normal zo
12989
silent! normal zo
12989
silent! normal zo
13001
silent! normal zo
13002
silent! normal zo
13003
silent! normal zo
13003
silent! normal zo
13087
silent! normal zo
13089
silent! normal zo
13090
silent! normal zo
13091
silent! normal zo
13091
silent! normal zo
13102
silent! normal zo
13103
silent! normal zo
13104
silent! normal zo
13104
silent! normal zo
13119
silent! normal zo
13120
silent! normal zo
13121
silent! normal zo
13122
silent! normal zo
13133
silent! normal zo
13134
silent! normal zo
13135
silent! normal zo
13135
silent! normal zo
13756
silent! normal zo
13767
silent! normal zo
13778
silent! normal zo
13797
silent! normal zo
13848
silent! normal zo
13885
silent! normal zo
13886
silent! normal zo
14049
silent! normal zo
14091
silent! normal zo
14919
silent! normal zo
14923
silent! normal zo
14923
silent! normal zo
14923
silent! normal zo
14923
silent! normal zo
14923
silent! normal zo
14938
silent! normal zo
14957
silent! normal zo
15484
silent! normal zo
15491
silent! normal zo
15502
silent! normal zo
15504
silent! normal zo
15513
silent! normal zo
15515
silent! normal zo
15524
silent! normal zo
15529
silent! normal zo
15538
silent! normal zo
15540
silent! normal zo
14969
silent! normal zo
14972
silent! normal zo
14972
silent! normal zo
14972
silent! normal zo
14972
silent! normal zo
14980
silent! normal zo
15004
silent! normal zo
15012
silent! normal zo
15014
silent! normal zo
15027
silent! normal zo
15036
silent! normal zo
15047
silent! normal zo
15048
silent! normal zo
15057
silent! normal zo
15057
silent! normal zo
15064
silent! normal zo
15073
silent! normal zo
15077
silent! normal zo
15078
silent! normal zo
15090
silent! normal zo
15109
silent! normal zo
15131
silent! normal zo
15136
silent! normal zo
15137
silent! normal zo
15137
silent! normal zo
15140
silent! normal zo
15141
silent! normal zo
15141
silent! normal zo
15141
silent! normal zo
15144
silent! normal zo
15144
silent! normal zo
15144
silent! normal zo
15148
silent! normal zo
15148
silent! normal zo
15148
silent! normal zo
15148
silent! normal zo
15148
silent! normal zo
15148
silent! normal zo
15148
silent! normal zo
15148
silent! normal zo
15148
silent! normal zo
15153
silent! normal zo
15181
silent! normal zo
15201
silent! normal zo
15208
silent! normal zo
15211
silent! normal zo
15214
silent! normal zo
15233
silent! normal zo
15254
silent! normal zo
15272
silent! normal zo
15279
silent! normal zo
15293
silent! normal zo
15308
silent! normal zo
15327
silent! normal zo
15338
silent! normal zo
15350
silent! normal zo
15368
silent! normal zo
15378
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15383
silent! normal zo
15385
silent! normal zo
15385
silent! normal zo
15385
silent! normal zo
15389
silent! normal zo
15390
silent! normal zo
15398
silent! normal zo
15412
silent! normal zo
15428
silent! normal zo
15437
silent! normal zo
15445
silent! normal zo
15448
silent! normal zo
15453
silent! normal zo
15467
silent! normal zo
15477
silent! normal zo
15481
silent! normal zo
15486
silent! normal zo
15492
silent! normal zo
15498
silent! normal zo
15498
silent! normal zo
15498
silent! normal zo
15500
silent! normal zo
15500
silent! normal zo
15500
silent! normal zo
15506
silent! normal zo
15510
silent! normal zo
15511
silent! normal zo
15511
silent! normal zo
15511
silent! normal zo
15511
silent! normal zo
15511
silent! normal zo
15511
silent! normal zo
15518
silent! normal zo
15519
silent! normal zo
15519
silent! normal zo
15531
silent! normal zo
15531
silent! normal zo
15531
silent! normal zo
15561
silent! normal zo
15562
silent! normal zo
15562
silent! normal zo
15562
silent! normal zo
15562
silent! normal zo
15562
silent! normal zo
15562
silent! normal zo
15564
silent! normal zo
15569
silent! normal zo
15575
silent! normal zo
15582
silent! normal zo
15583
silent! normal zo
15583
silent! normal zo
15586
silent! normal zo
15591
silent! normal zo
15597
silent! normal zo
15608
silent! normal zo
15625
silent! normal zo
15636
silent! normal zo
15637
silent! normal zo
15637
silent! normal zo
15639
silent! normal zo
15640
silent! normal zo
15640
silent! normal zo
15646
silent! normal zo
15647
silent! normal zo
15648
silent! normal zo
15649
silent! normal zo
15649
silent! normal zo
15649
silent! normal zo
15649
silent! normal zo
15655
silent! normal zo
15656
silent! normal zo
15657
silent! normal zo
15657
silent! normal zo
15657
silent! normal zo
15657
silent! normal zo
15664
silent! normal zo
15675
silent! normal zo
15682
silent! normal zo
18537
silent! normal zo
18695
silent! normal zo
18738
silent! normal zo
19107
silent! normal zo
19195
silent! normal zo
19213
silent! normal zo
19574
silent! normal zo
19732
silent! normal zo
20336
silent! normal zo
20473
silent! normal zo
let s:l = 19220 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19220
normal! 087l
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
let s:l = 1583 - ((17 * winheight(0) + 19) / 38)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1583
normal! 026l
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
10wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 29) / 58)
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
exe '10resize ' . ((&lines * 38 + 29) / 58)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
exe '11resize ' . ((&lines * 1 + 29) / 58)
exe 'vert 11resize ' . ((&columns * 80 + 55) / 111)
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
10wincmd w

" vim: ft=vim ro nowrap smc=128
