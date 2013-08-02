" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 01 agosto 2013 at 14:59:07.
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
badd +2310 ginn/formularios/pedidos_de_venta.py
badd +1 db/tablas.sql
badd +1958 ginn/formularios/albaranes_de_salida.py
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
badd +9324 ginn/framework/pclases/__init__.py
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
badd +221 ginn/formularios/consumo_balas_partida.py
badd +553 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
args formularios/auditviewer.py
set lines=57 columns=111
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
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 45 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
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
736
silent! normal zo
813
silent! normal zo
837
silent! normal zo
837
silent! normal zo
837
silent! normal zo
837
silent! normal zo
837
silent! normal zo
837
silent! normal zo
2015
silent! normal zo
3414
silent! normal zo
3427
silent! normal zo
3433
silent! normal zo
3437
silent! normal zo
3492
silent! normal zo
3492
silent! normal zo
3492
silent! normal zo
3492
silent! normal zo
3492
silent! normal zo
3492
silent! normal zo
3492
silent! normal zo
3492
silent! normal zo
3509
silent! normal zo
3509
silent! normal zo
3509
silent! normal zo
3509
silent! normal zo
3509
silent! normal zo
3509
silent! normal zo
3509
silent! normal zo
3509
silent! normal zo
3509
silent! normal zo
3509
silent! normal zo
3516
silent! normal zo
let s:l = 3508 - ((27 * winheight(0) + 22) / 45)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3508
normal! 06l
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
104
silent! normal zo
105
silent! normal zo
105
silent! normal zo
let s:l = 140 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
140
normal! 020l
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
silent! normal zo
436
silent! normal zo
447
silent! normal zo
722
silent! normal zo
734
silent! normal zo
738
silent! normal zo
739
silent! normal zo
743
silent! normal zo
744
silent! normal zo
744
silent! normal zo
744
silent! normal zo
744
silent! normal zo
1079
silent! normal zo
1607
silent! normal zo
1627
silent! normal zo
1830
silent! normal zo
1880
silent! normal zo
1969
silent! normal zo
1979
silent! normal zo
2808
silent! normal zo
3108
silent! normal zo
3117
silent! normal zo
3808
silent! normal zo
3998
silent! normal zo
3998
silent! normal zo
4021
silent! normal zo
4048
silent! normal zo
4063
silent! normal zo
4272
silent! normal zo
4302
silent! normal zo
4764
silent! normal zo
4941
silent! normal zo
4955
silent! normal zo
4961
silent! normal zo
4977
silent! normal zo
4988
silent! normal zo
5092
silent! normal zo
5179
silent! normal zo
5809
silent! normal zo
5965
silent! normal zo
5975
silent! normal zo
6108
silent! normal zo
6234
silent! normal zo
6249
silent! normal zo
6256
silent! normal zo
6256
silent! normal zo
6256
silent! normal zo
6256
silent! normal zo
6256
silent! normal zo
6256
silent! normal zo
6256
silent! normal zo
6256
silent! normal zo
6259
silent! normal zo
6259
silent! normal zo
6259
silent! normal zo
6259
silent! normal zo
6259
silent! normal zo
6259
silent! normal zo
6259
silent! normal zo
6259
silent! normal zo
6259
silent! normal zo
6279
silent! normal zo
6395
silent! normal zo
6403
silent! normal zo
6419
silent! normal zo
6450
silent! normal zo
6473
silent! normal zo
6480
silent! normal zo
6498
silent! normal zo
6505
silent! normal zo
6513
silent! normal zo
6540
silent! normal zo
6540
silent! normal zo
6540
silent! normal zo
6540
silent! normal zo
6540
silent! normal zo
6558
silent! normal zo
6564
silent! normal zo
6564
silent! normal zo
6583
silent! normal zo
6591
silent! normal zo
6591
silent! normal zo
6595
silent! normal zo
6599
silent! normal zo
6616
silent! normal zo
6617
silent! normal zo
6617
silent! normal zo
6623
silent! normal zo
6628
silent! normal zo
6649
silent! normal zo
6662
silent! normal zo
6681
silent! normal zo
6687
silent! normal zo
6691
silent! normal zo
6695
silent! normal zo
6710
silent! normal zo
6718
silent! normal zo
6730
silent! normal zo
6738
silent! normal zo
6744
silent! normal zo
6744
silent! normal zo
6744
silent! normal zo
6744
silent! normal zo
6744
silent! normal zo
6744
silent! normal zo
6744
silent! normal zo
6756
silent! normal zo
6762
silent! normal zo
6770
silent! normal zo
6783
silent! normal zo
6789
silent! normal zo
7543
silent! normal zo
8182
silent! normal zo
8182
silent! normal zo
8182
silent! normal zo
8182
silent! normal zo
8182
silent! normal zo
8182
silent! normal zo
8182
silent! normal zo
8210
silent! normal zo
8217
silent! normal zo
8224
silent! normal zo
9020
silent! normal zo
9381
silent! normal zo
10521
silent! normal zo
10703
silent! normal zo
10712
silent! normal zo
10731
silent! normal zo
10784
silent! normal zo
10799
silent! normal zo
10840
silent! normal zo
11423
silent! normal zo
11423
silent! normal zo
11423
silent! normal zo
11628
silent! normal zo
11628
silent! normal zo
11628
silent! normal zo
11628
silent! normal zo
11659
silent! normal zo
11662
silent! normal zo
11663
silent! normal zo
11671
silent! normal zo
11675
silent! normal zo
11676
silent! normal zo
12009
silent! normal zo
12009
silent! normal zo
12009
silent! normal zo
12009
silent! normal zo
12009
silent! normal zo
12045
silent! normal zo
12046
silent! normal zo
12047
silent! normal zo
12067
silent! normal zo
12093
silent! normal zo
12094
silent! normal zo
12188
silent! normal zo
12189
silent! normal zo
12228
silent! normal zo
12229
silent! normal zo
12307
silent! normal zo
12307
silent! normal zo
12307
silent! normal zo
12307
silent! normal zo
12307
silent! normal zo
12307
silent! normal zo
12307
silent! normal zo
12307
silent! normal zo
12319
silent! normal zo
12334
silent! normal zo
12336
silent! normal zo
12341
silent! normal zo
12346
silent! normal zo
12347
silent! normal zo
12347
silent! normal zo
12347
silent! normal zo
12382
silent! normal zo
12382
silent! normal zo
12421
silent! normal zo
12422
silent! normal zo
12423
silent! normal zo
12439
silent! normal zo
12483
silent! normal zo
12484
silent! normal zo
12544
silent! normal zo
12545
silent! normal zo
12605
silent! normal zo
12606
silent! normal zo
12746
silent! normal zo
12747
silent! normal zo
12748
silent! normal zo
12749
silent! normal zo
12749
silent! normal zo
12769
silent! normal zo
12770
silent! normal zo
12771
silent! normal zo
12771
silent! normal zo
12783
silent! normal zo
12784
silent! normal zo
12785
silent! normal zo
12785
silent! normal zo
12802
silent! normal zo
12803
silent! normal zo
12804
silent! normal zo
12805
silent! normal zo
12805
silent! normal zo
12826
silent! normal zo
12827
silent! normal zo
12828
silent! normal zo
12828
silent! normal zo
12840
silent! normal zo
12841
silent! normal zo
12842
silent! normal zo
12842
silent! normal zo
12918
silent! normal zo
12919
silent! normal zo
12920
silent! normal zo
12921
silent! normal zo
12921
silent! normal zo
12942
silent! normal zo
12943
silent! normal zo
12944
silent! normal zo
12944
silent! normal zo
12956
silent! normal zo
12957
silent! normal zo
12958
silent! normal zo
12958
silent! normal zo
12974
silent! normal zo
12975
silent! normal zo
12976
silent! normal zo
12977
silent! normal zo
12977
silent! normal zo
12998
silent! normal zo
12999
silent! normal zo
13000
silent! normal zo
13000
silent! normal zo
13012
silent! normal zo
13013
silent! normal zo
13014
silent! normal zo
13014
silent! normal zo
13098
silent! normal zo
13100
silent! normal zo
13101
silent! normal zo
13102
silent! normal zo
13102
silent! normal zo
13113
silent! normal zo
13114
silent! normal zo
13115
silent! normal zo
13115
silent! normal zo
13130
silent! normal zo
13131
silent! normal zo
13132
silent! normal zo
13133
silent! normal zo
13133
silent! normal zo
13144
silent! normal zo
13145
silent! normal zo
13146
silent! normal zo
13146
silent! normal zo
13767
silent! normal zo
13778
silent! normal zo
13789
silent! normal zo
13808
silent! normal zo
13859
silent! normal zo
13896
silent! normal zo
13897
silent! normal zo
14060
silent! normal zo
14102
silent! normal zo
14930
silent! normal zo
14934
silent! normal zo
14934
silent! normal zo
14934
silent! normal zo
14934
silent! normal zo
14934
silent! normal zo
14949
silent! normal zo
14968
silent! normal zo
14980
silent! normal zo
14983
silent! normal zo
14983
silent! normal zo
14983
silent! normal zo
14983
silent! normal zo
14991
silent! normal zo
15015
silent! normal zo
15023
silent! normal zo
15025
silent! normal zo
15038
silent! normal zo
15047
silent! normal zo
15058
silent! normal zo
15059
silent! normal zo
15068
silent! normal zo
15068
silent! normal zo
15075
silent! normal zo
15084
silent! normal zo
15088
silent! normal zo
15089
silent! normal zo
15101
silent! normal zo
15120
silent! normal zo
15142
silent! normal zo
15147
silent! normal zo
15148
silent! normal zo
15148
silent! normal zo
15151
silent! normal zo
15152
silent! normal zo
15152
silent! normal zo
15152
silent! normal zo
15155
silent! normal zo
15155
silent! normal zo
15155
silent! normal zo
15159
silent! normal zo
15159
silent! normal zo
15159
silent! normal zo
15159
silent! normal zo
15159
silent! normal zo
15159
silent! normal zo
15159
silent! normal zo
15159
silent! normal zo
15159
silent! normal zo
15164
silent! normal zo
15192
silent! normal zo
15212
silent! normal zo
15219
silent! normal zo
15222
silent! normal zo
15225
silent! normal zo
15244
silent! normal zo
15265
silent! normal zo
15283
silent! normal zo
15290
silent! normal zo
15304
silent! normal zo
15319
silent! normal zo
15338
silent! normal zo
15349
silent! normal zo
15361
silent! normal zo
15379
silent! normal zo
15389
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15394
silent! normal zo
15396
silent! normal zo
15396
silent! normal zo
15396
silent! normal zo
15400
silent! normal zo
15401
silent! normal zo
15409
silent! normal zo
15423
silent! normal zo
15439
silent! normal zo
15448
silent! normal zo
15456
silent! normal zo
15459
silent! normal zo
15464
silent! normal zo
15478
silent! normal zo
15488
silent! normal zo
15492
silent! normal zo
15497
silent! normal zo
15503
silent! normal zo
15509
silent! normal zo
15509
silent! normal zo
15509
silent! normal zo
15511
silent! normal zo
15511
silent! normal zo
15511
silent! normal zo
15517
silent! normal zo
15521
silent! normal zo
15522
silent! normal zo
15522
silent! normal zo
15522
silent! normal zo
15522
silent! normal zo
15522
silent! normal zo
15522
silent! normal zo
15529
silent! normal zo
15530
silent! normal zo
15530
silent! normal zo
15542
silent! normal zo
15542
silent! normal zo
15542
silent! normal zo
15572
silent! normal zo
15573
silent! normal zo
15573
silent! normal zo
15573
silent! normal zo
15573
silent! normal zo
15573
silent! normal zo
15573
silent! normal zo
15575
silent! normal zo
15580
silent! normal zo
15586
silent! normal zo
15593
silent! normal zo
15594
silent! normal zo
15594
silent! normal zo
15597
silent! normal zo
15602
silent! normal zo
15608
silent! normal zo
15619
silent! normal zo
15636
silent! normal zo
15647
silent! normal zo
15648
silent! normal zo
15648
silent! normal zo
15650
silent! normal zo
15651
silent! normal zo
15651
silent! normal zo
15657
silent! normal zo
15658
silent! normal zo
15659
silent! normal zo
15660
silent! normal zo
15660
silent! normal zo
15660
silent! normal zo
15660
silent! normal zo
15666
silent! normal zo
15667
silent! normal zo
15668
silent! normal zo
15668
silent! normal zo
15668
silent! normal zo
15668
silent! normal zo
15675
silent! normal zo
15686
silent! normal zo
15693
silent! normal zo
15740
silent! normal zo
15799
silent! normal zo
15837
silent! normal zo
15852
silent! normal zo
15863
silent! normal zo
15863
silent! normal zo
16493
silent! normal zo
16517
silent! normal zo
16522
silent! normal zo
16524
silent! normal zo
16530
silent! normal zo
17683
silent! normal zo
17690
silent! normal zo
17695
silent! normal zo
17695
silent! normal zo
17695
silent! normal zo
18384
silent! normal zo
18405
silent! normal zo
18567
silent! normal zo
18725
silent! normal zo
18768
silent! normal zo
19137
silent! normal zo
19225
silent! normal zo
19243
silent! normal zo
19359
silent! normal zo
19604
silent! normal zo
19762
silent! normal zo
let s:l = 16520 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16520
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
66
silent! normal zo
75
silent! normal zo
82
silent! normal zo
88
silent! normal zo
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
silent! normal zo
51
silent! normal zo
66
silent! normal zo
89
silent! normal zo
100
silent! normal zo
let s:l = 82 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
82
normal! 019l
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
let s:l = 1750 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1750
normal! 060l
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 45 + 28) / 57)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 28) / 57)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
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
