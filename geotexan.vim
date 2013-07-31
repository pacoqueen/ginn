" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 31 julio 2013 at 19:37:36.
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
badd +3537 db/tablas.sql
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
set lines=69 columns=111
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
exe '2resize ' . ((&lines * 11 + 34) / 69)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 10 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 10 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 10 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 11 + 34) / 69)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 10 + 34) / 69)
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
551
normal! zo
564
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
587
normal! zo
621
normal! zo
1204
normal! zo
1217
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3414
normal! zo
3427
normal! zo
3433
normal! zo
3437
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3503
normal! zo
3530
normal! zo
3530
normal! zo
3530
normal! zo
3530
normal! zo
3530
normal! zo
3530
normal! zo
3530
normal! zo
3530
normal! zo
3530
normal! zo
let s:l = 589 - ((0 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
589
normal! 061|
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
104
normal! zo
105
normal! zo
105
normal! zo
let s:l = 140 - ((0 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
140
normal! 021|
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
436
normal! zo
447
normal! zo
722
normal! zo
734
normal! zo
738
normal! zo
739
normal! zo
743
normal! zo
744
normal! zo
744
normal! zo
744
normal! zo
744
normal! zo
1079
normal! zo
1607
normal! zo
1627
normal! zo
1830
normal! zo
1880
normal! zo
1969
normal! zo
1979
normal! zo
2808
normal! zo
3108
normal! zo
3117
normal! zo
3808
normal! zo
3998
normal! zo
3998
normal! zo
4021
normal! zo
4048
normal! zo
4063
normal! zo
4272
normal! zo
4302
normal! zo
4764
normal! zo
4941
normal! zo
4955
normal! zo
4961
normal! zo
4977
normal! zo
4988
normal! zo
5092
normal! zo
5179
normal! zo
5809
normal! zo
5965
normal! zo
5975
normal! zo
6108
normal! zo
6234
normal! zo
6249
normal! zo
6256
normal! zo
6256
normal! zo
6256
normal! zo
6256
normal! zo
6256
normal! zo
6256
normal! zo
6256
normal! zo
6256
normal! zo
6259
normal! zo
6259
normal! zo
6259
normal! zo
6259
normal! zo
6259
normal! zo
6259
normal! zo
6259
normal! zo
6259
normal! zo
6259
normal! zo
6279
normal! zo
6395
normal! zo
6403
normal! zo
6419
normal! zo
6450
normal! zo
6473
normal! zo
6480
normal! zo
6498
normal! zo
6505
normal! zo
6513
normal! zo
6540
normal! zo
6540
normal! zo
6540
normal! zo
6540
normal! zo
6540
normal! zo
6558
normal! zo
6564
normal! zo
6564
normal! zo
6583
normal! zo
6591
normal! zo
6591
normal! zo
6595
normal! zo
6599
normal! zo
6616
normal! zo
6617
normal! zo
6617
normal! zo
6623
normal! zo
6628
normal! zo
6649
normal! zo
6662
normal! zo
6681
normal! zo
6687
normal! zo
6691
normal! zo
6695
normal! zo
6710
normal! zo
6718
normal! zo
6730
normal! zo
6738
normal! zo
6744
normal! zo
6744
normal! zo
6744
normal! zo
6744
normal! zo
6744
normal! zo
6744
normal! zo
6744
normal! zo
6756
normal! zo
6762
normal! zo
6770
normal! zo
6783
normal! zo
6789
normal! zo
7543
normal! zo
8182
normal! zo
8182
normal! zo
8182
normal! zo
8182
normal! zo
8182
normal! zo
8182
normal! zo
8182
normal! zo
8210
normal! zo
8217
normal! zo
8224
normal! zo
9020
normal! zo
9381
normal! zo
10521
normal! zo
10703
normal! zo
10712
normal! zo
10731
normal! zo
10784
normal! zo
10799
normal! zo
10840
normal! zo
11423
normal! zo
11423
normal! zo
11423
normal! zo
11628
normal! zo
11628
normal! zo
11628
normal! zo
11628
normal! zo
11659
normal! zo
11662
normal! zo
11663
normal! zo
11671
normal! zo
11675
normal! zo
11676
normal! zo
12009
normal! zo
12009
normal! zo
12009
normal! zo
12009
normal! zo
12009
normal! zo
12045
normal! zo
12046
normal! zo
12047
normal! zo
12067
normal! zo
12093
normal! zo
12094
normal! zo
12188
normal! zo
12189
normal! zo
12228
normal! zo
12229
normal! zo
12307
normal! zo
12307
normal! zo
12307
normal! zo
12307
normal! zo
12307
normal! zo
12307
normal! zo
12307
normal! zo
12307
normal! zo
12319
normal! zo
12334
normal! zo
12336
normal! zo
12341
normal! zo
12346
normal! zo
12347
normal! zo
12347
normal! zo
12347
normal! zo
12382
normal! zo
12382
normal! zo
12421
normal! zo
12422
normal! zo
12423
normal! zo
12439
normal! zo
12483
normal! zo
12484
normal! zo
12544
normal! zo
12545
normal! zo
12605
normal! zo
12606
normal! zo
12746
normal! zo
12747
normal! zo
12748
normal! zo
12749
normal! zo
12749
normal! zo
12769
normal! zo
12770
normal! zo
12771
normal! zo
12771
normal! zo
12783
normal! zo
12784
normal! zo
12785
normal! zo
12785
normal! zo
12802
normal! zo
12803
normal! zo
12804
normal! zo
12805
normal! zo
12805
normal! zo
12826
normal! zo
12827
normal! zo
12828
normal! zo
12828
normal! zo
12840
normal! zo
12841
normal! zo
12842
normal! zo
12842
normal! zo
12918
normal! zo
12919
normal! zo
12920
normal! zo
12921
normal! zo
12921
normal! zo
12942
normal! zo
12943
normal! zo
12944
normal! zo
12944
normal! zo
12956
normal! zo
12957
normal! zo
12958
normal! zo
12958
normal! zo
12974
normal! zo
12975
normal! zo
12976
normal! zo
12977
normal! zo
12977
normal! zo
12998
normal! zo
12999
normal! zo
13000
normal! zo
13000
normal! zo
13012
normal! zo
13013
normal! zo
13014
normal! zo
13014
normal! zo
13098
normal! zo
13100
normal! zo
13101
normal! zo
13102
normal! zo
13102
normal! zo
13113
normal! zo
13114
normal! zo
13115
normal! zo
13115
normal! zo
13130
normal! zo
13131
normal! zo
13132
normal! zo
13133
normal! zo
13133
normal! zo
13144
normal! zo
13145
normal! zo
13146
normal! zo
13146
normal! zo
13767
normal! zo
13778
normal! zo
13789
normal! zo
13808
normal! zo
13859
normal! zo
13896
normal! zo
13897
normal! zo
14060
normal! zo
14102
normal! zo
14930
normal! zo
14934
normal! zo
14934
normal! zo
14934
normal! zo
14934
normal! zo
14934
normal! zo
14949
normal! zo
14968
normal! zo
14980
normal! zo
14983
normal! zo
14983
normal! zo
14983
normal! zo
14983
normal! zo
14991
normal! zo
15015
normal! zo
15023
normal! zo
15025
normal! zo
15038
normal! zo
15047
normal! zo
15058
normal! zo
15059
normal! zo
15068
normal! zo
15068
normal! zo
15075
normal! zo
15084
normal! zo
15088
normal! zo
15089
normal! zo
15101
normal! zo
15120
normal! zo
15142
normal! zo
15147
normal! zo
15148
normal! zo
15148
normal! zo
15151
normal! zo
15152
normal! zo
15152
normal! zo
15152
normal! zo
15155
normal! zo
15155
normal! zo
15155
normal! zo
15159
normal! zo
15159
normal! zo
15159
normal! zo
15159
normal! zo
15159
normal! zo
15159
normal! zo
15159
normal! zo
15159
normal! zo
15159
normal! zo
15164
normal! zo
15192
normal! zo
15212
normal! zo
15219
normal! zo
15222
normal! zo
15225
normal! zo
15244
normal! zo
15265
normal! zo
15283
normal! zo
15290
normal! zo
15304
normal! zo
15319
normal! zo
15338
normal! zo
15349
normal! zo
15361
normal! zo
15379
normal! zo
15389
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15394
normal! zo
15396
normal! zo
15396
normal! zo
15396
normal! zo
15400
normal! zo
15401
normal! zo
15409
normal! zo
15423
normal! zo
15439
normal! zo
15448
normal! zo
15456
normal! zo
15459
normal! zo
15464
normal! zo
15478
normal! zo
15488
normal! zo
15492
normal! zo
15497
normal! zo
15503
normal! zo
15509
normal! zo
15509
normal! zo
15509
normal! zo
15511
normal! zo
15511
normal! zo
15511
normal! zo
15517
normal! zo
15521
normal! zo
15522
normal! zo
15522
normal! zo
15522
normal! zo
15522
normal! zo
15522
normal! zo
15522
normal! zo
15529
normal! zo
15530
normal! zo
15530
normal! zo
15542
normal! zo
15542
normal! zo
15542
normal! zo
15572
normal! zo
15573
normal! zo
15573
normal! zo
15573
normal! zo
15573
normal! zo
15573
normal! zo
15573
normal! zo
15575
normal! zo
15580
normal! zo
15586
normal! zo
15593
normal! zo
15594
normal! zo
15594
normal! zo
15597
normal! zo
15602
normal! zo
15608
normal! zo
15619
normal! zo
15636
normal! zo
15647
normal! zo
15648
normal! zo
15648
normal! zo
15650
normal! zo
15651
normal! zo
15651
normal! zo
15657
normal! zo
15658
normal! zo
15659
normal! zo
15660
normal! zo
15660
normal! zo
15660
normal! zo
15660
normal! zo
15666
normal! zo
15667
normal! zo
15668
normal! zo
15668
normal! zo
15668
normal! zo
15668
normal! zo
15675
normal! zo
15686
normal! zo
15693
normal! zo
15740
normal! zo
15799
normal! zo
15837
normal! zo
15852
normal! zo
15863
normal! zo
15863
normal! zo
16493
normal! zo
16517
normal! zo
16522
normal! zo
16524
normal! zo
16530
normal! zo
17683
normal! zo
17690
normal! zo
17695
normal! zo
17695
normal! zo
17695
normal! zo
18384
normal! zo
18405
normal! zo
18567
normal! zo
18725
normal! zo
18768
normal! zo
19137
normal! zo
19225
normal! zo
19243
normal! zo
19359
normal! zo
19604
normal! zo
19762
normal! zo
let s:l = 16520 - ((3 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16520
normal! 018|
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
let s:l = 24 - ((0 * winheight(0) + 5) / 10)
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
normal! zo
51
normal! zo
66
normal! zo
89
normal! zo
100
normal! zo
let s:l = 82 - ((0 * winheight(0) + 5) / 11)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
82
normal! 020|
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
230
normal! zo
262
normal! zo
262
normal! zo
339
normal! zo
340
normal! zo
345
normal! zo
350
normal! zo
351
normal! zo
356
normal! zo
362
normal! zo
467
normal! zo
579
normal! zo
595
normal! zo
725
normal! zo
734
normal! zo
834
normal! zo
850
normal! zo
850
normal! zo
850
normal! zo
850
normal! zo
961
normal! zo
966
normal! zo
1531
normal! zo
1727
normal! zo
1728
normal! zo
1728
normal! zo
1728
normal! zo
1728
normal! zo
1739
normal! zo
1740
normal! zo
1744
normal! zo
1744
normal! zo
1745
normal! zo
1752
normal! zo
1753
normal! zo
1804
normal! zo
3253
normal! zo
3260
normal! zo
3265
normal! zo
3272
normal! zo
3276
normal! zo
3281
normal! zo
3282
normal! zo
3282
normal! zo
3282
normal! zo
3288
normal! zo
3293
normal! zo
3294
normal! zo
3299
normal! zo
let s:l = 1750 - ((0 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1750
normal! 061|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 11 + 34) / 69)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 10 + 34) / 69)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 10 + 34) / 69)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 10 + 34) / 69)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 11 + 34) / 69)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 10 + 34) / 69)
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
