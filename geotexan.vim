" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 01 octubre 2013 at 17:20:31.
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
badd +855 ginn/formularios/pedidos_de_venta.py
badd +2026 db/tablas.sql
badd +1277 ginn/formularios/albaranes_de_salida.py
badd +1 ginn/formularios/presupuesto.py
badd +1283 ginn/formularios/presupuestos.py
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
badd +212 ginn/formularios/mail_sender.py
badd +1239 ginn/formularios/abonos_venta.py
badd +131 ginn/formularios/ventana_progreso.py
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
8wincmd k
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
exe '5resize ' . ((&lines * 26 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
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
10329
silent! normal zo
10337
silent! normal zo
10338
silent! normal zo
10422
silent! normal zo
10453
silent! normal zo
10554
silent! normal zo
10567
silent! normal zo
10580
silent! normal zo
10605
silent! normal zo
10606
silent! normal zo
10607
silent! normal zo
10607
silent! normal zo
10607
silent! normal zo
10621
silent! normal zo
10622
silent! normal zo
10623
silent! normal zo
10623
silent! normal zo
10623
silent! normal zo
14226
silent! normal zo
14614
silent! normal zo
14655
silent! normal zo
14978
silent! normal zo
15082
silent! normal zo
15082
silent! normal zo
15173
silent! normal zo
15173
silent! normal zo
15173
silent! normal zo
15173
silent! normal zo
15173
silent! normal zo
15173
silent! normal zo
15173
silent! normal zo
15227
silent! normal zo
15878
silent! normal zo
17944
silent! normal zo
17959
silent! normal zo
19457
silent! normal zo
19558
silent! normal zo
19567
silent! normal zo
19580
silent! normal zo
19605
silent! normal zo
19780
silent! normal zo
19862
silent! normal zo
19869
silent! normal zo
19914
silent! normal zo
19962
silent! normal zo
19980
silent! normal zo
let s:l = 10568 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10568
normal! 08l
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
let s:l = 815 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
815
normal! 015l
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
135
silent! normal zo
136
silent! normal zo
139
silent! normal zo
140
silent! normal zo
151
silent! normal zo
152
silent! normal zo
153
silent! normal zo
169
silent! normal zo
170
silent! normal zo
191
silent! normal zo
194
silent! normal zo
200
silent! normal zo
211
silent! normal zo
232
silent! normal zo
277
silent! normal zo
279
silent! normal zo
280
silent! normal zo
281
silent! normal zo
335
silent! normal zo
336
silent! normal zo
343
silent! normal zo
387
silent! normal zo
402
silent! normal zo
410
silent! normal zo
432
silent! normal zo
436
silent! normal zo
437
silent! normal zo
452
silent! normal zo
569
silent! normal zo
609
silent! normal zo
618
silent! normal zo
625
silent! normal zo
630
silent! normal zo
631
silent! normal zo
691
silent! normal zo
707
silent! normal zo
734
silent! normal zo
750
silent! normal zo
757
silent! normal zo
759
silent! normal zo
792
silent! normal zo
901
silent! normal zo
902
silent! normal zo
906
silent! normal zo
939
silent! normal zo
941
silent! normal zo
974
silent! normal zo
1019
silent! normal zo
1022
silent! normal zo
1028
silent! normal zo
1074
silent! normal zo
1085
silent! normal zo
1088
silent! normal zo
1147
silent! normal zo
1271
silent! normal zo
1280
silent! normal zo
1281
silent! normal zo
1295
silent! normal zo
1297
silent! normal zo
1319
silent! normal zo
1393
silent! normal zo
1430
silent! normal zo
1461
silent! normal zo
1470
silent! normal zo
1470
silent! normal zo
1513
silent! normal zo
1513
silent! normal zo
1523
silent! normal zo
1541
silent! normal zo
1588
silent! normal zo
1592
silent! normal zo
1594
silent! normal zo
1602
silent! normal zo
1611
silent! normal zo
1614
silent! normal zo
1621
silent! normal zo
1640
silent! normal zo
1641
silent! normal zo
1642
silent! normal zo
1650
silent! normal zo
1652
silent! normal zo
1652
silent! normal zo
1654
silent! normal zo
1655
silent! normal zo
1655
silent! normal zo
1678
silent! normal zo
1698
silent! normal zo
1725
silent! normal zo
1742
silent! normal zo
1764
silent! normal zo
1769
silent! normal zo
1783
silent! normal zo
1795
silent! normal zo
1796
silent! normal zo
1803
silent! normal zo
1809
silent! normal zo
1875
silent! normal zo
1894
silent! normal zo
1970
silent! normal zo
1984
silent! normal zo
1986
silent! normal zo
2044
silent! normal zo
2049
silent! normal zo
2053
silent! normal zo
2278
silent! normal zo
2281
silent! normal zo
2282
silent! normal zo
let s:l = 2282 - ((13 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2282
normal! 035l
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
normal! 046l
wincmd w
5wincmd w
exe 'vert 1resize ' . ((&columns * 30 + 55) / 111)
exe '2resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 2resize ' . ((&columns * 80 + 55) / 111)
exe '3resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 3resize ' . ((&columns * 80 + 55) / 111)
exe '4resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 4resize ' . ((&columns * 80 + 55) / 111)
exe '5resize ' . ((&lines * 26 + 22) / 44)
exe 'vert 5resize ' . ((&columns * 80 + 55) / 111)
exe '6resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 6resize ' . ((&columns * 80 + 55) / 111)
exe '7resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 7resize ' . ((&columns * 80 + 55) / 111)
exe '8resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 8resize ' . ((&columns * 80 + 55) / 111)
exe '9resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 9resize ' . ((&columns * 80 + 55) / 111)
exe '10resize ' . ((&lines * 1 + 22) / 44)
exe 'vert 10resize ' . ((&columns * 80 + 55) / 111)
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
5wincmd w

" vim: ft=vim ro nowrap smc=128
