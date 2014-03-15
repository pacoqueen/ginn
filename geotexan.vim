" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 15 marzo 2014 at 11:56:35.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 12
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'gruvbox' | colorscheme gruvbox | endif
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
badd +9 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1505 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +206 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +374 ginn/formularios/productos_de_venta_rollos.py
badd +315 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +337 ginn/formularios/productos_de_venta_especial.py
badd +2420 ginn/formularios/partes_de_fabricacion_balas.py
badd +737 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1899 ginn/formularios/partes_de_fabricacion_rollos.py
badd +312 ginn/formularios/proveedores.py
badd +547 ~/workspace/CICAN/src/formularios/menu.py
badd +93 ginn/formularios/launcher.py
badd +625 ginn/formularios/empleados.py
badd +38 ginn/formularios/resultados_geotextiles.py
badd +760 ginn/formularios/menu.py
badd +142 ginn/formularios/autenticacion.py
badd +1148 ginn/informes/geninformes.py
badd +233 ginn/informes/informe_certificado_calidad.py
badd +1518 informes/geninformes.py
badd +2349 ginn/formularios/facturas_venta.py
badd +144 ginn/framework/configuracion.py
badd +4 bin/ginn.sh
badd +10 ginn/main.py
badd +1149 ginn/formularios/ventana.py
badd +2094 ginn/formularios/pedidos_de_venta.py
badd +3879 db/tablas.sql
badd +2048 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +1 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +1527 ginn/formularios/facturas_compra.py
badd +123 ginn/formularios/utils.py
badd +648 ginn/formularios/resultados_fibra.py
badd +955 ginn/formularios/albaranes_de_entrada.py
badd +611 ginn/formularios/consulta_ventas.py
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
badd +21254 ginn/framework/pclases/__init__.py
badd +494 ginn/framework/pclases/superfacturaventa.py
badd +149 ginn/framework/pclases/facturaventa.py
badd +694 ginn/formularios/consulta_mensual_nominas.py
badd +309 ginn/informes/treeview2pdf.py
badd +82 ginn/formularios/balas_cable.py
badd +13 ginn/informes/nied.py
badd +82 ginn/informes/norma2013.py
badd +65 ginn/formularios/widgets.py
badd +1 ginn/informes/ekotex.py
badd +7 ~/.vim/ftplugin/python.vim
badd +140 ginn/formularios/listado_balas.py
badd +227 ginn/formularios/consulta_pendientes_servir.py
badd +130 ginn/formularios/facturas_no_bloqueadas.py
badd +611 ginn/formularios/consumo_balas_partida.py
badd +324 ginn/formularios/categorias_laborales.py
badd +411 ginn/formularios/nominas.py
badd +511 ginn/framework/pclases/cliente.py
badd +1 ginn/formularios/consulta_cobros.py
badd +638 ginn/formularios/pagares_cobros.py
badd +24 extra/patches/calcular_credito_disponible.sql
badd +301 ginn/formularios/pclase2tv.py
badd +94 ginn/formularios/consulta_control_horas.py
badd +533 ginn/formularios/horas_trabajadas.py
badd +550 ginn/formularios/horas_trabajadas_dia.py
badd +1 ginn/formularios/pedidos_de_compra.glade
badd +542 ginn/formularios/postomatic.py
badd +18 ginn/formularios/custom_widgets/cellrendererautocomplete.py
badd +47 ginn/formularios/custom_widgets/__init__.py
badd +549 ginn/informes/presupuesto2.py
badd +61 ginn/informes/albaran_multipag.py
badd +192 ginn/formularios/silos.py
badd +4 ginn/framework/__init__.py
badd +1 ginn/formularios/vencimientos_pendientes_por_cliente.glade
badd +93 ginn/formularios/consulta_productividad.py
badd +171 ginn/formularios/mail_sender.py
badd +1143 ginn/formularios/abonos_venta.py
badd +306 ginn/formularios/ventana_progreso.py
badd +993 ginn/formularios/control_personal.py
badd +594 ginn/formularios/listado_rollos.py
badd +74 ginn/formularios/consulta_existenciasRollos.py
badd +64 ginn/formularios/listado_rollos_defectuosos.py
badd +500 ginn/formularios/consulta_global.py
badd +91 ginn/formularios/rollos_c.py
badd +56 extra/scripts/enviar_exitencias_geotextiles_a_comerciales.py
badd +1 ginn/informes/presupuesto.py
badd +112 ginn/formularios/consulta_libro_iva.py
badd +531 ginn/formularios/consulta_ofertas.py
badd +24 extra/patches/create_ventana_consultas.py
badd +203 ginn/lib/ezodf/ezodf/const.py
badd +61 ginn/lib/ezodf/ezodf/xmlns.py
badd +21 ginn/lib/simple_odspy/simpleodspy/sodsods.py
badd +17 ginn/lib/simple_odspy/simpleodspy/sodsspreadsheet.py
badd +41 ginn/lib/simple_odspy/simpleodspy/sodstable.py
badd +66 ginn/lib/odfpy/contrib/odscell/odscell
badd +127 ginn/lib/odfpy/contrib/odscell/odscell.py
badd +280 ginn/formularios/consulta_ofertas_pendientes_validar.py
badd +538 ginn/formularios/consulta_ofertas_estudio.py
badd +1075 ginn/formularios/confirmings.py
badd +213 ginn/formularios/transferencias.py
badd +66 ginn/formularios/cuentas_destino.py
badd +509 ginn/formularios/facturacion_por_cliente_y_fechas.py
badd +1 ginn/formularios/presupuestos.glade
badd +24 ginn/lib/simple_odspy/simpleodspy/sodsxls.py
badd +1 ginn/formularios/ofer
badd +1 ginn/formularios/usuarios.glade
badd +251 ginn/formularios/usuarios.py
badd +22 ginn/lib/xlutils/xlutils/copy.py
badd +108 ginn/lib/xlutils/xlutils/filter.py
badd +10 ginn/lib/xlutils/xlutils/display.py
badd +8 ginn/lib/xlutils/xlutils/margins.py
badd +1 ginn/lib/xlutils/xlutils/filter.pyç
badd +381 ginn/lib/xlrd/xlrd/__init__.py
badd +9 ginn/lib/xlwt/xlwt/__init__.py
badd +659 ginn/lib/xlwt/xlwt/Workbook.py
badd +123 ginn/formularios/gestor_mensajes.py
badd +2290 ginn/formularios/prefacturas.py
badd +1 presupuestos
badd +1 ginn/formularios/consulta_albaranesPorFacturar.glade
badd +393 ginn/formularios/consulta_albaranesPorFacturar.py
badd +1 ginn/formularios/checklist_window.py
badd +506 ginn/formularios/pedidos_de_compra.py
badd +92 ginn/formularios/utils_almacen.py
badd +121 ginn/formularios/consumo_fibra_por_partida_gtx.py
badd +138 ginn/lib/charting.py
badd +66 ginn/formularios/consulta_existenciasBalas.py
badd +338 ginn/formularios/consulta_consumo.py
badd +182 ginn/formularios/consulta_existencias_por_tipo.py
badd +82 ginn/formularios/consulta_existencias.py
badd +1 ginn/formularios/consulta_producido.glade
badd +1 ginn/formularios/consumo_balas_partida.pyç
badd +28 db/restore_snapshot.sh
badd +1 extra/scripts/clouseau.py
badd +86 ginn/informes/treeview2csv.py
badd +287 ginn/formularios/consulta_ventas_por_producto.py
badd +1 tests/stock_performance.py
badd +1 (clewn)_console
badd +1 ginn/formularios/consulta_productividad.glade
args formularios/auditviewer.py
set lines=62 columns=114
edit (clewn)_console
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
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
exe '1resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 1resize ' . ((&columns * 33 + 57) / 114)
exe '2resize ' . ((&lines * 58 + 31) / 62)
exe 'vert 2resize ' . ((&columns * 33 + 57) / 114)
exe '3resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 114)
exe '4resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 114)
exe '5resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 114)
exe '6resize ' . ((&lines * 42 + 31) / 62)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 114)
exe '7resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 114)
exe '8resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 114)
exe '9resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 114)
exe '10resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 114)
exe '11resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 11resize ' . ((&columns * 80 + 57) / 114)
exe '12resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 12resize ' . ((&columns * 80 + 57) / 114)
argglobal
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
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
enew
file ~/Geotexan/src/Geotex-INN/__Tag_List__
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
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/albaranes_de_salida.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
98
normal! zo
99
normal! zo
111
normal! zo
111
normal! zo
111
normal! zo
1173
normal! zo
2019
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2032
normal! zo
2041
normal! zo
2047
normal! zo
2048
normal! zo
2048
normal! zo
2049
normal! zo
2052
normal! zo
2069
normal! zo
2074
normal! zo
2074
normal! zo
2200
normal! zo
2834
normal! zo
2843
normal! zo
3066
normal! zo
3264
normal! zo
3276
normal! zo
3277
normal! zo
3278
normal! zo
3295
normal! zo
3295
normal! zo
4218
normal! zo
4248
normal! zo
let s:l = 4813 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4813
normal! 020|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/framework/pclases/__init__.py
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
361
normal! zo
370
normal! zo
375
normal! zo
390
normal! zo
461
normal! zo
593
normal! zo
599
normal! zo
600
normal! zo
610
normal! zo
647
normal! zo
686
normal! zo
750
normal! zo
760
normal! zo
766
normal! zo
793
normal! zo
1118
normal! zo
1210
normal! zo
1219
normal! zo
1261
normal! zo
1267
normal! zo
1267
normal! zo
1267
normal! zo
1294
normal! zo
1300
normal! zo
1300
normal! zo
1300
normal! zo
1319
normal! zo
1328
normal! zo
1403
normal! zo
1428
normal! zo
1437
normal! zo
1512
normal! zo
1537
normal! zo
1546
normal! zo
1621
normal! zo
1646
normal! zo
1767
normal! zo
1809
normal! zo
1850
normal! zo
1850
normal! zo
1850
normal! zo
2468
normal! zo
2599
normal! zo
2640
normal! zo
2645
normal! zo
2654
normal! zo
2660
normal! zo
2662
normal! zo
2669
normal! zo
2804
normal! zo
2854
normal! zo
3063
normal! zo
3212
normal! zo
3363
normal! zo
3552
normal! zo
3864
normal! zo
3898
normal! zo
3900
normal! zo
3956
normal! zo
3963
normal! zo
3964
normal! zo
3964
normal! zo
3964
normal! zo
3964
normal! zo
3964
normal! zo
3964
normal! zo
3988
normal! zo
4038
normal! zo
4041
normal! zo
4046
normal! zo
4047
normal! zo
4047
normal! zo
4047
normal! zo
4051
normal! zo
4051
normal! zo
4051
normal! zo
4051
normal! zo
4051
normal! zo
4051
normal! zo
4054
normal! zo
4054
normal! zo
4060
normal! zo
4062
normal! zo
4067
normal! zo
4070
normal! zo
4072
normal! zo
4077
normal! zo
4078
normal! zo
4088
normal! zo
4096
normal! zo
4097
normal! zo
4097
normal! zo
4097
normal! zo
4097
normal! zo
4101
normal! zo
4104
normal! zo
4105
normal! zo
4105
normal! zo
4105
normal! zo
4105
normal! zo
4105
normal! zo
4119
normal! zo
4142
normal! zo
4186
normal! zo
4599
normal! zo
4610
normal! zo
4744
normal! zo
4784
normal! zo
4797
normal! zo
4808
normal! zo
4829
normal! zo
4868
normal! zo
4880
normal! zo
4881
normal! zo
4881
normal! zo
4881
normal! zo
5158
normal! zo
5182
normal! zo
5193
normal! zo
5193
normal! zo
5193
normal! zo
5202
normal! zo
5222
normal! zo
5231
normal! zo
5232
normal! zo
5245
normal! zo
5251
normal! zo
5251
normal! zo
5251
normal! zo
5251
normal! zo
5267
normal! zo
5267
normal! zo
5267
normal! zo
5267
normal! zo
5267
normal! zo
5363
normal! zo
5369
normal! zo
5393
normal! zo
5420
normal! zo
5510
normal! zo
5522
normal! zo
5523
normal! zo
5524
normal! zo
5524
normal! zo
5524
normal! zo
5524
normal! zo
5526
normal! zo
5526
normal! zo
5526
normal! zo
5526
normal! zo
5526
normal! zo
5577
normal! zo
5577
normal! zo
5577
normal! zo
5577
normal! zo
5577
normal! zo
5605
normal! zo
5608
normal! zo
5627
normal! zo
5628
normal! zo
5629
normal! zo
5639
normal! zo
5691
normal! zo
5692
normal! zo
5812
normal! zo
5867
normal! zo
5879
normal! zo
5944
normal! zo
5988
normal! zo
5996
normal! zo
6023
normal! zo
6036
normal! zo
6040
normal! zo
6046
normal! zo
6179
normal! zo
6305
normal! zo
6350
normal! zo
6899
normal! zo
7149
normal! zo
7156
normal! zo
7174
normal! zo
7185
normal! zo
7185
normal! zo
7185
normal! zo
7188
normal! zo
7188
normal! zo
7191
normal! zo
7191
normal! zo
7194
normal! zo
7194
normal! zo
7198
normal! zo
7202
normal! zo
7210
normal! zo
7228
normal! zo
7229
normal! zo
7238
normal! zo
7239
normal! zo
7626
normal! zo
7655
normal! zo
7655
normal! zo
7655
normal! zo
7655
normal! zo
7655
normal! zo
7679
normal! zo
7748
normal! zo
7767
normal! zo
7770
normal! zo
7771
normal! zo
7771
normal! zo
7771
normal! zo
7784
normal! zo
7785
normal! zo
7786
normal! zo
7791
normal! zo
7797
normal! zo
7803
normal! zo
7803
normal! zo
7803
normal! zo
7803
normal! zo
7803
normal! zo
7803
normal! zo
7805
normal! zo
7844
normal! zo
7854
normal! zo
7855
normal! zo
7863
normal! zo
7864
normal! zo
7867
normal! zo
7872
normal! zo
7873
normal! zo
7874
normal! zo
7875
normal! zo
7875
normal! zo
7875
normal! zo
7875
normal! zo
7875
normal! zo
7875
normal! zo
7879
normal! zo
7885
normal! zo
7888
normal! zo
7888
normal! zo
7888
normal! zo
7888
normal! zo
7888
normal! zo
7897
normal! zo
7898
normal! zo
7899
normal! zo
7907
normal! zo
7914
normal! zo
7914
normal! zo
7914
normal! zo
7914
normal! zo
7914
normal! zo
7914
normal! zo
7916
normal! zo
7916
normal! zo
7916
normal! zo
7916
normal! zo
7916
normal! zo
7916
normal! zo
7916
normal! zo
7919
normal! zo
7919
normal! zo
7919
normal! zo
7919
normal! zo
7919
normal! zo
7919
normal! zo
7920
normal! zo
7920
normal! zo
7920
normal! zo
7920
normal! zo
7922
normal! zo
7923
normal! zo
7932
normal! zo
7939
normal! zo
7939
normal! zo
7939
normal! zo
7939
normal! zo
7939
normal! zo
7939
normal! zo
7941
normal! zo
7944
normal! zo
7944
normal! zo
7944
normal! zo
7944
normal! zo
7944
normal! zo
7944
normal! zo
7945
normal! zo
7945
normal! zo
7945
normal! zo
7945
normal! zo
7947
normal! zo
7948
normal! zo
7951
normal! zo
7956
normal! zo
7956
normal! zo
7956
normal! zo
7956
normal! zo
7956
normal! zo
7956
normal! zo
7956
normal! zo
8004
normal! zo
8009
normal! zo
8011
normal! zo
8012
normal! zo
8012
normal! zo
8012
normal! zo
8012
normal! zo
8012
normal! zo
8012
normal! zo
8015
normal! zo
8021
normal! zo
8024
normal! zo
8033
normal! zo
8035
normal! zo
8036
normal! zo
8043
normal! zo
8044
normal! zo
8045
normal! zo
8050
normal! zo
8054
normal! zo
8062
normal! zo
8063
normal! zo
8065
normal! zo
8065
normal! zo
8072
normal! zo
8073
normal! zo
8074
normal! zo
8074
normal! zo
8074
normal! zo
8074
normal! zo
8074
normal! zo
8074
normal! zo
8074
normal! zo
8074
normal! zo
8077
normal! zo
8077
normal! zo
8077
normal! zo
8084
normal! zo
8086
normal! zo
8369
normal! zo
8380
normal! zo
8381
normal! zo
8381
normal! zo
8381
normal! zo
8381
normal! zo
8381
normal! zo
8381
normal! zo
8381
normal! zo
8384
normal! zo
8384
normal! zo
8384
normal! zo
8384
normal! zo
8384
normal! zo
8384
normal! zo
8384
normal! zo
8388
normal! zo
8395
normal! zo
8395
normal! zo
8395
normal! zo
8395
normal! zo
8395
normal! zo
8395
normal! zo
8395
normal! zo
8395
normal! zo
8398
normal! zo
8398
normal! zo
8398
normal! zo
8398
normal! zo
8398
normal! zo
8398
normal! zo
8398
normal! zo
8398
normal! zo
8833
normal! zo
8837
normal! zo
8868
normal! zo
8917
normal! zo
8924
normal! zo
9092
normal! zo
9103
normal! zo
9116
normal! zo
9117
normal! zo
9130
normal! zo
9135
normal! zo
9140
normal! zo
9145
normal! zo
9156
normal! zo
9179
normal! zo
9202
normal! zo
9203
normal! zo
9203
normal! zo
9203
normal! zo
9203
normal! zo
9203
normal! zo
9203
normal! zo
9214
normal! zo
9229
normal! zo
9264
normal! zo
9352
normal! zo
9384
normal! zo
9391
normal! zo
9395
normal! zo
9400
normal! zo
9415
normal! zo
9463
normal! zo
9504
normal! zo
9525
normal! zo
9766
normal! zo
9792
normal! zo
9831
normal! zo
9842
normal! zo
9843
normal! zo
9856
normal! zo
9872
normal! zo
9888
normal! zo
9892
normal! zo
9892
normal! zo
9894
normal! zo
9900
normal! zo
9911
normal! zo
9927
normal! zo
9944
normal! zo
9944
normal! zo
9944
normal! zo
9944
normal! zo
9944
normal! zo
9944
normal! zo
9944
normal! zo
9944
normal! zo
9944
normal! zo
9951
normal! zo
9965
normal! zo
9966
normal! zo
9966
normal! zo
9968
normal! zo
9969
normal! zo
9969
normal! zo
9971
normal! zo
9972
normal! zo
9972
normal! zo
9974
normal! zo
9975
normal! zo
9975
normal! zo
9977
normal! zo
9980
normal! zo
9982
normal! zo
9982
normal! zo
9982
normal! zo
9991
normal! zo
10004
normal! zo
10007
normal! zo
10008
normal! zo
10008
normal! zo
10011
normal! zo
10011
normal! zo
10011
normal! zo
10014
normal! zo
10014
normal! zo
10014
normal! zo
10014
normal! zo
10020
normal! zo
10023
normal! zo
10027
normal! zo
10034
normal! zo
10036
normal! zo
10083
normal! zo
10097
normal! zo
10098
normal! zo
10100
normal! zo
10135
normal! zo
10142
normal! zo
10147
normal! zo
10148
normal! zo
10153
normal! zo
10153
normal! zo
10153
normal! zo
10153
normal! zo
10153
normal! zo
10156
normal! zo
10156
normal! zo
10156
normal! zo
10182
normal! zo
10191
normal! zo
10196
normal! zo
10198
normal! zo
10203
normal! zo
10209
normal! zo
10217
normal! zo
10218
normal! zo
10218
normal! zo
10218
normal! zo
10218
normal! zo
10227
normal! zo
10228
normal! zo
10233
normal! zo
10282
normal! zo
10287
normal! zo
10400
normal! zo
10427
normal! zo
10432
normal! zo
10438
normal! zo
10524
normal! zo
10531
normal! zo
10532
normal! zo
10580
normal! zo
10580
normal! zo
10580
normal! zo
10580
normal! zo
10580
normal! zo
10583
normal! zo
10591
normal! zo
10592
normal! zo
10637
normal! zo
10657
normal! zo
10658
normal! zo
10659
normal! zo
10659
normal! zo
10659
normal! zo
10659
normal! zo
10659
normal! zo
10659
normal! zo
10659
normal! zo
10659
normal! zo
10659
normal! zo
10676
normal! zo
10682
normal! zo
10692
normal! zo
10707
normal! zo
10710
normal! zo
10713
normal! zo
10713
normal! zo
10713
normal! zo
10716
normal! zo
10716
normal! zo
10716
normal! zo
10716
normal! zo
10721
normal! zo
10721
normal! zo
10721
normal! zo
10729
normal! zo
10736
normal! zo
10743
normal! zo
10746
normal! zo
10748
normal! zo
10751
normal! zo
10754
normal! zo
10759
normal! zo
10770
normal! zo
10777
normal! zo
10781
normal! zo
10782
normal! zo
10782
normal! zo
10784
normal! zo
10785
normal! zo
10785
normal! zo
10787
normal! zo
10788
normal! zo
10788
normal! zo
10790
normal! zo
10791
normal! zo
10791
normal! zo
10793
normal! zo
10794
normal! zo
10794
normal! zo
10796
normal! zo
10797
normal! zo
10797
normal! zo
10799
normal! zo
10800
normal! zo
10800
normal! zo
10802
normal! zo
10805
normal! zo
10807
normal! zo
10807
normal! zo
10807
normal! zo
10813
normal! zo
10814
normal! zo
10814
normal! zo
10816
normal! zo
10817
normal! zo
10817
normal! zo
10841
normal! zo
10845
normal! zo
10848
normal! zo
10849
normal! zo
10849
normal! zo
10849
normal! zo
10849
normal! zo
10849
normal! zo
10849
normal! zo
10854
normal! zo
10855
normal! zo
10855
normal! zo
10855
normal! zo
10858
normal! zo
10970
normal! zo
11046
normal! zo
11054
normal! zo
11061
normal! zo
11061
normal! zo
11061
normal! zo
11061
normal! zo
11061
normal! zo
11061
normal! zo
11061
normal! zo
11072
normal! zo
11076
normal! zo
11077
normal! zo
11077
normal! zo
11077
normal! zo
11087
normal! zo
11090
normal! zo
11097
normal! zo
11106
normal! zo
11115
normal! zo
11225
normal! zo
11226
normal! zc
11239
normal! zo
11239
normal! zo
11239
normal! zo
11239
normal! zo
11248
normal! zc
11251
normal! zo
11264
normal! zo
11277
normal! zo
11284
normal! zo
11286
normal! zo
11286
normal! zo
11286
normal! zo
11286
normal! zo
11286
normal! zo
11286
normal! zo
11294
normal! zc
11311
normal! zo
11339
normal! zo
11351
normal! zo
11352
normal! zo
11352
normal! zo
11352
normal! zo
11352
normal! zo
11311
normal! zc
11357
normal! zo
11357
normal! zc
11408
normal! zo
11408
normal! zc
11523
normal! zo
11531
normal! zo
11531
normal! zo
11531
normal! zo
11531
normal! zo
11523
normal! zc
11539
normal! zc
11545
normal! zo
11545
normal! zc
11556
normal! zo
11556
normal! zc
11573
normal! zo
11573
normal! zo
11577
normal! zo
11582
normal! zo
11582
normal! zo
11584
normal! zo
11585
normal! zo
11585
normal! zo
11590
normal! zo
11590
normal! zo
11590
normal! zo
11590
normal! zo
11590
normal! zo
11590
normal! zc
11603
normal! zo
11606
normal! zo
11606
normal! zo
11606
normal! zo
11606
normal! zo
11612
normal! zo
11612
normal! zo
11612
normal! zo
11612
normal! zo
11612
normal! zo
11612
normal! zc
11640
normal! zo
11678
normal! zc
11685
normal! zc
11693
normal! zo
11693
normal! zc
11701
normal! zc
11709
normal! zc
11723
normal! zo
11723
normal! zc
11741
normal! zo
11741
normal! zo
11741
normal! zo
11741
normal! zo
11741
normal! zo
11741
normal! zo
11741
normal! zo
11741
normal! zo
11741
normal! zo
11741
normal! zo
11741
normal! zc
11762
normal! zo
11762
normal! zo
11762
normal! zo
11762
normal! zo
11762
normal! zo
11762
normal! zo
11803
normal! zo
11804
normal! zo
11826
normal! zo
11826
normal! zc
11933
normal! zo
11933
normal! zc
11982
normal! zo
11982
normal! zo
11984
normal! zo
11994
normal! zo
11982
normal! zc
12077
normal! zo
12077
normal! zc
12131
normal! zo
12131
normal! zo
12131
normal! zo
12131
normal! zc
12131
normal! zc
12145
normal! zo
12182
normal! zo
12193
normal! zo
12198
normal! zo
12216
normal! zo
12216
normal! zo
12216
normal! zo
12216
normal! zo
12217
normal! zo
12222
normal! zo
12238
normal! zo
12238
normal! zo
12238
normal! zo
12238
normal! zo
12247
normal! zo
12247
normal! zo
12247
normal! zo
12247
normal! zo
12247
normal! zo
12271
normal! zo
12295
normal! zo
12295
normal! zc
12336
normal! zo
12336
normal! zo
12336
normal! zo
12336
normal! zo
12398
normal! zo
12414
normal! zo
12414
normal! zc
12438
normal! zo
12438
normal! zo
12438
normal! zo
12438
normal! zc
12463
normal! zo
12463
normal! zo
12463
normal! zo
12463
normal! zc
12538
normal! zo
12538
normal! zo
12538
normal! zo
12538
normal! zo
12538
normal! zo
12538
normal! zo
12538
normal! zo
12538
normal! zo
12538
normal! zc
12554
normal! zo
12554
normal! zc
12576
normal! zo
12576
normal! zc
12597
normal! zo
12597
normal! zo
12597
normal! zo
12597
normal! zo
12597
normal! zo
12597
normal! zo
12597
normal! zo
12597
normal! zc
12597
normal! zc
12717
normal! zo
12717
normal! zo
12717
normal! zo
12717
normal! zo
12717
normal! zo
12717
normal! zc
12985
normal! zo
12985
normal! zc
13015
normal! zo
13015
normal! zo
13015
normal! zo
13015
normal! zo
13015
normal! zo
13015
normal! zo
13015
normal! zo
13015
normal! zo
13030
normal! zo
13045
normal! zo
13047
normal! zo
13069
normal! zo
13077
normal! zo
13077
normal! zc
13093
normal! zo
13093
normal! zo
13132
normal! zo
13194
normal! zo
13195
normal! zo
13213
normal! zo
13255
normal! zo
13256
normal! zo
13284
normal! zo
13316
normal! zo
13317
normal! zo
13345
normal! zo
13381
normal! zo
13382
normal! zo
13400
normal! zo
13427
normal! zc
13437
normal! zo
13437
normal! zc
13457
normal! zo
13458
normal! zo
13459
normal! zo
13457
normal! zc
13513
normal! zo
13513
normal! zc
13571
normal! zo
13571
normal! zo
13571
normal! zo
13581
normal! zo
13586
normal! zo
13587
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13588
normal! zo
13594
normal! zo
13595
normal! zo
13596
normal! zo
13596
normal! zo
13596
normal! zo
13596
normal! zo
13596
normal! zo
13596
normal! zo
13596
normal! zo
13598
normal! zo
13598
normal! zo
13598
normal! zo
13598
normal! zo
13598
normal! zo
13598
normal! zo
13598
normal! zo
13598
normal! zo
13600
normal! zo
13601
normal! zo
13601
normal! zo
13601
normal! zo
13601
normal! zo
13601
normal! zo
13601
normal! zo
13601
normal! zo
13601
normal! zo
13601
normal! zo
13604
normal! zo
13606
normal! zo
13606
normal! zo
13611
normal! zo
13611
normal! zo
13621
normal! zo
13622
normal! zo
13622
normal! zo
13622
normal! zo
13622
normal! zo
13622
normal! zo
13622
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13635
normal! zo
13636
normal! zo
13645
normal! zo
13646
normal! zo
13646
normal! zo
13646
normal! zo
13646
normal! zo
13650
normal! zo
13650
normal! zo
13650
normal! zo
13658
normal! zo
13659
normal! zo
13661
normal! zo
13669
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13674
normal! zo
13674
normal! zo
13674
normal! zo
13681
normal! zo
13681
normal! zo
13681
normal! zo
13681
normal! zo
13681
normal! zo
13684
normal! zo
13685
normal! zo
13686
normal! zo
13687
normal! zo
13687
normal! zo
13688
normal! zo
13700
normal! zo
13701
normal! zo
13701
normal! zo
13701
normal! zo
13708
normal! zo
13709
normal! zo
13710
normal! zo
13710
normal! zo
13711
normal! zo
13722
normal! zo
13723
normal! zo
13724
normal! zo
13724
normal! zo
13725
normal! zo
13740
normal! zo
13741
normal! zo
13742
normal! zo
13743
normal! zo
13743
normal! zo
13744
normal! zo
13756
normal! zo
13757
normal! zo
13757
normal! zo
13757
normal! zo
13758
normal! zo
13764
normal! zo
13765
normal! zo
13766
normal! zo
13766
normal! zo
13767
normal! zo
13778
normal! zo
13779
normal! zo
13780
normal! zo
13780
normal! zo
13781
normal! zo
13796
normal! zo
13796
normal! zo
13796
normal! zo
13817
normal! zo
13822
normal! zo
13823
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13824
normal! zo
13830
normal! zo
13831
normal! zo
13832
normal! zo
13832
normal! zo
13832
normal! zo
13832
normal! zo
13832
normal! zo
13832
normal! zo
13832
normal! zo
13834
normal! zo
13834
normal! zo
13834
normal! zo
13834
normal! zo
13834
normal! zo
13834
normal! zo
13834
normal! zo
13834
normal! zo
13836
normal! zo
13837
normal! zo
13837
normal! zo
13837
normal! zo
13837
normal! zo
13837
normal! zo
13837
normal! zo
13837
normal! zo
13837
normal! zo
13837
normal! zo
13840
normal! zo
13842
normal! zo
13847
normal! zo
13856
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13857
normal! zo
13864
normal! zo
13866
normal! zo
13867
normal! zo
13868
normal! zo
13868
normal! zo
13869
normal! zo
13879
normal! zo
13880
normal! zo
13881
normal! zo
13881
normal! zo
13882
normal! zo
13896
normal! zo
13897
normal! zo
13898
normal! zo
13899
normal! zo
13899
normal! zo
13900
normal! zo
13910
normal! zo
13911
normal! zo
13912
normal! zo
13912
normal! zo
13913
normal! zo
13927
normal! zo
13927
normal! zo
13927
normal! zo
13938
normal! zo
13943
normal! zo
13944
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13945
normal! zo
13951
normal! zo
13952
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13953
normal! zo
13955
normal! zo
13955
normal! zo
13955
normal! zo
13955
normal! zo
13955
normal! zo
13955
normal! zo
13955
normal! zo
13955
normal! zo
13957
normal! zo
13958
normal! zo
13958
normal! zo
13958
normal! zo
13958
normal! zo
13958
normal! zo
13958
normal! zo
13958
normal! zo
13958
normal! zo
13958
normal! zo
13961
normal! zo
13963
normal! zo
13968
normal! zo
13977
normal! zo
13978
normal! zo
13978
normal! zo
13978
normal! zo
13978
normal! zo
13978
normal! zo
13978
normal! zo
13978
normal! zo
13985
normal! zo
13990
normal! zo
13991
normal! zo
13992
normal! zo
13999
normal! zo
14000
normal! zo
14001
normal! zo
14007
normal! zo
14008
normal! zo
14009
normal! zo
14014
normal! zo
14015
normal! zo
14016
normal! zo
14016
normal! zo
14026
normal! zo
14027
normal! zo
14028
normal! zo
14028
normal! zo
14028
normal! zo
14028
normal! zo
14028
normal! zo
14028
normal! zo
14035
normal! zo
14036
normal! zo
14036
normal! zo
14036
normal! zo
14036
normal! zo
14036
normal! zo
14036
normal! zo
14036
normal! zo
14043
normal! zo
14044
normal! zo
14044
normal! zo
14044
normal! zo
14044
normal! zo
14044
normal! zo
14044
normal! zo
14044
normal! zo
14050
normal! zo
14051
normal! zo
14051
normal! zo
14051
normal! zo
14051
normal! zo
14051
normal! zo
14051
normal! zo
14051
normal! zo
14061
normal! zo
14067
normal! zo
14067
normal! zo
14073
normal! zo
14079
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14085
normal! zo
14095
normal! zo
14095
normal! zo
14095
normal! zo
14095
normal! zo
14095
normal! zo
14095
normal! zo
14097
normal! zo
14098
normal! zo
14098
normal! zo
14098
normal! zo
14104
normal! zo
14104
normal! zo
14104
normal! zo
14104
normal! zo
14104
normal! zo
14104
normal! zo
14104
normal! zo
14104
normal! zo
14104
normal! zo
14115
normal! zo
14115
normal! zo
14115
normal! zo
14115
normal! zo
14115
normal! zo
14115
normal! zo
14117
normal! zo
14118
normal! zo
14118
normal! zo
14118
normal! zo
14124
normal! zo
14124
normal! zo
14124
normal! zo
14124
normal! zo
14132
normal! zo
14137
normal! zo
14140
normal! zo
14145
normal! zo
14146
normal! zo
14147
normal! zo
14147
normal! zo
14147
normal! zo
14147
normal! zo
14147
normal! zo
14147
normal! zo
14147
normal! zo
14147
normal! zo
14147
normal! zo
14147
normal! zo
14153
normal! zo
14154
normal! zo
14157
normal! zo
14158
normal! zo
14158
normal! zo
14158
normal! zo
14158
normal! zo
14158
normal! zo
14158
normal! zo
14158
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14160
normal! zo
14162
normal! zo
14163
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14166
normal! zo
14169
normal! zo
14170
normal! zo
14174
normal! zo
14174
normal! zo
14179
normal! zo
14179
normal! zo
14184
normal! zo
14185
normal! zo
14192
normal! zo
14193
normal! zo
14196
normal! zo
14196
normal! zo
14196
normal! zo
14196
normal! zo
14196
normal! zo
14196
normal! zo
14203
normal! zo
14204
normal! zo
14205
normal! zo
14206
normal! zo
14212
normal! zo
14213
normal! zo
14214
normal! zo
14220
normal! zo
14221
normal! zo
14221
normal! zo
14222
normal! zo
14227
normal! zo
14228
normal! zo
14228
normal! zo
14229
normal! zo
14238
normal! zo
14239
normal! zo
14240
normal! zo
14240
normal! zo
14240
normal! zo
14240
normal! zo
14240
normal! zo
14240
normal! zo
14247
normal! zo
14248
normal! zo
14249
normal! zo
14255
normal! zo
14256
normal! zo
14256
normal! zo
14256
normal! zo
14256
normal! zo
14256
normal! zo
14256
normal! zo
14256
normal! zo
14262
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14263
normal! zo
14274
normal! zo
14275
normal! zo
14275
normal! zo
14281
normal! zo
14287
normal! zo
14287
normal! zo
14293
normal! zo
14293
normal! zo
14293
normal! zo
14293
normal! zo
14309
normal! zo
14314
normal! zo
14315
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14316
normal! zo
14322
normal! zo
14323
normal! zo
14324
normal! zo
14324
normal! zo
14324
normal! zo
14324
normal! zo
14324
normal! zo
14324
normal! zo
14324
normal! zo
14326
normal! zo
14326
normal! zo
14326
normal! zo
14326
normal! zo
14326
normal! zo
14326
normal! zo
14326
normal! zo
14326
normal! zo
14326
normal! zo
14328
normal! zo
14329
normal! zo
14329
normal! zo
14329
normal! zo
14329
normal! zo
14329
normal! zo
14329
normal! zo
14329
normal! zo
14329
normal! zo
14329
normal! zo
14332
normal! zo
14334
normal! zo
14334
normal! zo
14339
normal! zo
14339
normal! zo
14349
normal! zo
14350
normal! zo
14350
normal! zo
14350
normal! zo
14350
normal! zo
14350
normal! zo
14350
normal! zo
14357
normal! zo
14358
normal! zo
14359
normal! zo
14360
normal! zo
14365
normal! zo
14366
normal! zo
14367
normal! zo
14377
normal! zo
14378
normal! zo
14379
normal! zo
14379
normal! zo
14379
normal! zo
14379
normal! zo
14379
normal! zo
14379
normal! zo
14384
normal! zo
14385
normal! zo
14385
normal! zo
14385
normal! zo
14386
normal! zo
14396
normal! zo
14397
normal! zo
14397
normal! zo
14403
normal! zo
14404
normal! zo
14404
normal! zo
14410
normal! zo
14410
normal! zo
14410
normal! zo
14410
normal! zo
14422
normal! zo
14427
normal! zo
14428
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14429
normal! zo
14435
normal! zo
14436
normal! zo
14437
normal! zo
14437
normal! zo
14437
normal! zo
14437
normal! zo
14437
normal! zo
14437
normal! zo
14437
normal! zo
14439
normal! zo
14439
normal! zo
14439
normal! zo
14439
normal! zo
14439
normal! zo
14439
normal! zo
14439
normal! zo
14439
normal! zo
14439
normal! zo
14441
normal! zo
14442
normal! zo
14442
normal! zo
14442
normal! zo
14442
normal! zo
14442
normal! zo
14442
normal! zo
14442
normal! zo
14442
normal! zo
14442
normal! zo
14445
normal! zo
14447
normal! zo
14447
normal! zo
14452
normal! zo
14452
normal! zo
14462
normal! zo
14463
normal! zo
14463
normal! zo
14463
normal! zo
14463
normal! zo
14463
normal! zo
14463
normal! zo
14470
normal! zo
14477
normal! zo
14478
normal! zo
14480
normal! zo
14480
normal! zo
14480
normal! zo
14486
normal! zo
14488
normal! zo
14490
normal! zo
14496
normal! zo
14498
normal! zo
14500
normal! zo
14511
normal! zo
14531
normal! zo
14543
normal! zo
14544
normal! zo
14545
normal! zo
14547
normal! zo
14548
normal! zo
14549
normal! zo
14549
normal! zo
14549
normal! zo
14551
normal! zo
14552
normal! zo
14552
normal! zo
14552
normal! zo
14568
normal! zo
14579
normal! zo
14588
normal! zo
14598
normal! zo
14625
normal! zo
14630
normal! zo
14636
normal! zo
14647
normal! zo
14660
normal! zo
14684
normal! zo
14686
normal! zo
14689
normal! zo
14692
normal! zo
14693
normal! zo
14697
normal! zo
14698
normal! zo
14712
normal! zo
14712
normal! zo
14712
normal! zo
14712
normal! zo
14734
normal! zo
14735
normal! zo
14736
normal! zo
14736
normal! zo
14736
normal! zo
14736
normal! zo
14736
normal! zo
14736
normal! zo
14736
normal! zo
14736
normal! zo
14736
normal! zo
14736
normal! zo
14745
normal! zo
14746
normal! zo
14752
normal! zo
14756
normal! zo
14757
normal! zo
14766
normal! zo
14767
normal! zo
14775
normal! zo
14776
normal! zo
14782
normal! zo
14797
normal! zo
14805
normal! zo
14811
normal! zo
14817
normal! zo
14822
normal! zo
14826
normal! zo
14832
normal! zo
14837
normal! zo
14838
normal! zo
14843
normal! zo
14854
normal! zo
14872
normal! zo
14914
normal! zo
14920
normal! zo
14926
normal! zo
14933
normal! zo
14942
normal! zo
14944
normal! zo
14951
normal! zo
14951
normal! zo
14951
normal! zo
14951
normal! zo
14951
normal! zo
14951
normal! zo
14968
normal! zo
14980
normal! zo
14991
normal! zo
14992
normal! zo
15008
normal! zo
15025
normal! zo
15029
normal! zo
15030
normal! zo
15031
normal! zo
15031
normal! zo
15033
normal! zo
15036
normal! zo
15049
normal! zo
15059
normal! zo
15061
normal! zo
15065
normal! zo
15066
normal! zo
15066
normal! zo
15066
normal! zo
15066
normal! zo
15066
normal! zo
15066
normal! zo
15079
normal! zo
15100
normal! zo
15101
normal! zo
15108
normal! zo
15141
normal! zo
15142
normal! zo
15142
normal! zo
15158
normal! zo
15164
normal! zo
15167
normal! zo
15167
normal! zo
15167
normal! zo
15173
normal! zo
15173
normal! zo
15193
normal! zo
15198
normal! zo
15203
normal! zo
15211
normal! zo
15230
normal! zo
15264
normal! zo
15272
normal! zo
15281
normal! zo
15300
normal! zo
15302
normal! zo
15306
normal! zo
15323
normal! zo
15329
normal! zo
15333
normal! zo
15372
normal! zo
15476
normal! zo
15476
normal! zo
15552
normal! zo
15552
normal! zo
15552
normal! zo
15665
normal! zo
15696
normal! zo
15720
normal! zo
15730
normal! zo
15730
normal! zo
15730
normal! zo
15730
normal! zo
15730
normal! zo
15918
normal! zo
15937
normal! zo
15959
normal! zo
15964
normal! zo
15965
normal! zo
15965
normal! zo
15968
normal! zo
15969
normal! zo
15969
normal! zo
15969
normal! zo
15972
normal! zo
15972
normal! zo
15972
normal! zo
15976
normal! zo
15976
normal! zo
15976
normal! zo
15976
normal! zo
15976
normal! zo
15976
normal! zo
15976
normal! zo
15976
normal! zo
15976
normal! zo
16281
normal! zo
16439
normal! zo
16507
normal! zo
16543
normal! zo
16558
normal! zo
16564
normal! zo
16567
normal! zo
16575
normal! zo
16576
normal! zo
16576
normal! zo
16576
normal! zo
16576
normal! zo
16576
normal! zo
16580
normal! zo
16588
normal! zo
16591
normal! zo
16597
normal! zo
16603
normal! zo
16606
normal! zo
16612
normal! zo
16626
normal! zo
16632
normal! zo
16637
normal! zo
16640
normal! zo
16640
normal! zo
16640
normal! zo
16650
normal! zo
16665
normal! zo
16676
normal! zo
16676
normal! zo
16687
normal! zo
16702
normal! zo
16712
normal! zo
16723
normal! zo
16731
normal! zo
16736
normal! zo
16752
normal! zo
16790
normal! zo
16818
normal! zo
16819
normal! zo
16819
normal! zo
16819
normal! zo
16819
normal! zo
16819
normal! zo
16819
normal! zo
16819
normal! zo
16819
normal! zo
16819
normal! zo
16819
normal! zo
16819
normal! zo
16831
normal! zo
16839
normal! zo
16840
normal! zo
16843
normal! zo
16844
normal! zo
16850
normal! zo
16871
normal! zo
16890
normal! zo
16898
normal! zo
16899
normal! zo
16908
normal! zo
16924
normal! zo
16944
normal! zo
16949
normal! zo
16962
normal! zo
16962
normal! zo
16962
normal! zo
16962
normal! zo
16962
normal! zo
16962
normal! zo
16962
normal! zo
16962
normal! zo
16962
normal! zo
16962
normal! zo
17041
normal! zo
17054
normal! zo
17055
normal! zo
17056
normal! zo
17062
normal! zo
17066
normal! zo
17068
normal! zo
17083
normal! zo
17099
normal! zo
17107
normal! zo
17111
normal! zo
17116
normal! zo
17124
normal! zo
17129
normal! zo
17137
normal! zo
17142
normal! zo
17162
normal! zo
17177
normal! zo
17178
normal! zo
17194
normal! zo
17231
normal! zo
17245
normal! zo
17248
normal! zo
17252
normal! zo
17253
normal! zo
17272
normal! zo
17287
normal! zo
17294
normal! zo
17295
normal! zo
17301
normal! zo
17308
normal! zo
17313
normal! zo
17341
normal! zo
17361
normal! zo
17362
normal! zo
17384
normal! zo
17398
normal! zo
17405
normal! zo
17406
normal! zo
17420
normal! zo
17456
normal! zo
17477
normal! zo
17500
normal! zo
17513
normal! zo
17537
normal! zo
17542
normal! zo
17566
normal! zo
17584
normal! zo
17602
normal! zo
17603
normal! zo
17614
normal! zo
17638
normal! zo
17651
normal! zo
17655
normal! zo
17655
normal! zo
17655
normal! zo
17655
normal! zo
17655
normal! zo
17669
normal! zo
17669
normal! zo
17669
normal! zo
17669
normal! zo
17669
normal! zo
17669
normal! zo
17669
normal! zo
17783
normal! zo
17791
normal! zo
17813
normal! zo
17836
normal! zo
17901
normal! zo
17958
normal! zo
17973
normal! zo
18007
normal! zo
18021
normal! zo
18047
normal! zo
18067
normal! zo
18079
normal! zo
18079
normal! zo
18079
normal! zo
18079
normal! zo
18079
normal! zo
18082
normal! zo
18089
normal! zo
18092
normal! zo
18103
normal! zo
18109
normal! zo
18114
normal! zo
18125
normal! zo
18144
normal! zo
18187
normal! zo
18212
normal! zo
18268
normal! zo
18277
normal! zo
18722
normal! zo
18794
normal! zo
18800
normal! zo
18803
normal! zo
18816
normal! zo
18833
normal! zo
18843
normal! zo
18846
normal! zo
18847
normal! zo
18847
normal! zo
18853
normal! zo
18860
normal! zo
19112
normal! zo
19158
normal! zo
19168
normal! zo
19169
normal! zo
19169
normal! zo
19169
normal! zo
19169
normal! zo
19169
normal! zo
19449
normal! zo
20059
normal! zo
20067
normal! zo
20101
normal! zo
20113
normal! zo
20118
normal! zo
20125
normal! zo
20137
normal! zo
20155
normal! zo
20165
normal! zo
20202
normal! zo
20321
normal! zo
20339
normal! zo
20347
normal! zo
20376
normal! zo
20447
normal! zo
20448
normal! zo
20460
normal! zo
20475
normal! zo
20482
normal! zo
20489
normal! zo
20496
normal! zo
20503
normal! zo
20510
normal! zo
20517
normal! zo
20523
normal! zo
20642
normal! zo
20660
normal! zo
20689
normal! zo
20705
normal! zo
20715
normal! zo
20726
normal! zo
20737
normal! zo
20754
normal! zo
20754
normal! zo
20754
normal! zo
20754
normal! zo
20754
normal! zo
20754
normal! zo
20754
normal! zo
20754
normal! zo
20754
normal! zo
20774
normal! zo
20774
normal! zo
20774
normal! zo
20774
normal! zo
20774
normal! zo
20774
normal! zo
20774
normal! zo
20774
normal! zo
20794
normal! zo
20842
normal! zo
20854
normal! zo
20855
normal! zo
20863
normal! zo
20880
normal! zo
20880
normal! zo
20880
normal! zo
20880
normal! zo
20880
normal! zo
20880
normal! zo
20880
normal! zo
21027
normal! zo
21034
normal! zo
21036
normal! zo
21040
normal! zo
let s:l = 10756 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10756
normal! 024|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_productividad.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
46
normal! zo
50
normal! zo
51
normal! zo
178
normal! zo
199
normal! zo
217
normal! zo
217
normal! zo
247
normal! zo
299
normal! zo
300
normal! zo
381
normal! zo
382
normal! zo
396
normal! zo
398
normal! zo
406
normal! zo
406
normal! zo
431
normal! zo
450
normal! zo
454
normal! zo
454
normal! zo
454
normal! zo
464
normal! zo
475
normal! zo
476
normal! zo
487
normal! zo
487
normal! zo
487
normal! zo
487
normal! zo
500
normal! zo
567
normal! zo
579
normal! zo
607
normal! zo
609
normal! zo
679
normal! zo
680
normal! zo
let s:l = 133 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
133
normal! 013|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_ventas_por_producto.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
47
normal! zo
48
normal! zo
50
normal! zo
50
normal! zo
50
normal! zo
52
normal! zo
52
normal! zo
141
normal! zo
163
normal! zo
168
normal! zo
184
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
185
normal! zo
195
normal! zo
199
normal! zo
205
normal! zo
219
normal! zo
219
normal! zo
219
normal! zo
219
normal! zo
219
normal! zo
219
normal! zo
231
normal! zo
232
normal! zo
232
normal! zo
232
normal! zo
232
normal! zo
232
normal! zo
242
normal! zo
249
normal! zo
250
normal! zo
250
normal! zo
250
normal! zo
250
normal! zo
272
normal! zo
286
normal! zo
290
normal! zo
291
normal! zo
292
normal! zo
296
normal! zo
318
normal! zo
323
normal! zo
356
normal! zo
362
normal! zo
362
normal! zo
362
normal! zo
362
normal! zo
362
normal! zo
364
normal! zo
364
normal! zo
364
normal! zo
364
normal! zo
364
normal! zo
365
normal! zo
398
normal! zo
408
normal! zo
409
normal! zo
415
normal! zo
421
normal! zo
426
normal! zo
439
normal! zo
445
normal! zo
let s:l = 173 - ((19 * winheight(0) + 21) / 42)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
173
normal! 09|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/facturas_venta.py
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
114
normal! zo
114
normal! zo
114
normal! zo
308
normal! zo
312
normal! zo
338
normal! zo
483
normal! zo
1754
normal! zo
1764
normal! zo
1768
normal! zo
1862
normal! zo
1866
normal! zo
2676
normal! zo
2957
normal! zo
2980
normal! zo
2993
normal! zo
2993
normal! zo
2993
normal! zo
let s:l = 86 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
86
normal! 045|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_producido.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
59
normal! zo
60
normal! zo
73
normal! zo
73
normal! zo
73
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
85
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
98
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
100
normal! zo
112
normal! zo
116
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
117
normal! zo
122
normal! zo
143
normal! zo
150
normal! zo
162
normal! zo
187
normal! zo
225
normal! zo
238
normal! zo
249
normal! zo
273
normal! zo
286
normal! zo
303
normal! zo
303
normal! zo
303
normal! zo
303
normal! zo
307
normal! zo
308
normal! zo
308
normal! zo
331
normal! zo
332
normal! zo
332
normal! zo
350
normal! zo
351
normal! zo
356
normal! zo
357
normal! zo
362
normal! zo
371
normal! zo
374
normal! zo
375
normal! zo
375
normal! zo
375
normal! zo
375
normal! zo
375
normal! zo
375
normal! zo
425
normal! zo
426
normal! zo
427
normal! zo
427
normal! zo
430
normal! zo
431
normal! zo
431
normal! zo
431
normal! zo
431
normal! zo
444
normal! zo
445
normal! zo
446
normal! zo
446
normal! zo
449
normal! zo
450
normal! zo
450
normal! zo
450
normal! zo
450
normal! zo
454
normal! zo
459
normal! zo
459
normal! zo
459
normal! zo
459
normal! zo
462
normal! zo
463
normal! zo
467
normal! zo
484
normal! zo
484
normal! zo
484
normal! zo
484
normal! zo
493
normal! zo
494
normal! zo
494
normal! zo
494
normal! zo
494
normal! zo
503
normal! zo
508
normal! zo
508
normal! zo
508
normal! zo
508
normal! zo
511
normal! zo
511
normal! zo
511
normal! zo
511
normal! zo
516
normal! zo
517
normal! zo
520
normal! zo
552
normal! zo
561
normal! zo
561
normal! zo
561
normal! zo
561
normal! zo
567
normal! zo
568
normal! zo
571
normal! zo
620
normal! zo
621
normal! zo
643
normal! zo
644
normal! zo
670
normal! zo
728
normal! zo
734
normal! zo
734
normal! zo
734
normal! zo
734
normal! zo
734
normal! zo
746
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
763
normal! zo
763
normal! zo
784
normal! zo
799
normal! zo
800
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
801
normal! zo
805
normal! zo
805
normal! zo
805
normal! zo
815
normal! zo
823
normal! zo
833
normal! zo
847
normal! zo
848
normal! zo
854
normal! zo
885
normal! zo
905
normal! zo
905
normal! zo
905
normal! zo
905
normal! zo
905
normal! zo
916
normal! zo
998
normal! zo
1005
normal! zo
1012
normal! zo
1051
normal! zo
1060
normal! zo
1066
normal! zo
1067
normal! zo
1068
normal! zo
1093
normal! zo
1113
normal! zo
1124
normal! zo
1124
normal! zo
1124
normal! zo
1124
normal! zo
1124
normal! zo
1124
normal! zo
1124
normal! zo
1153
normal! zo
let s:l = 665 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
665
normal! 036|
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/extra/scripts/clouseau.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
16
normal! zo
47
normal! zo
69
normal! zo
77
normal! zo
87
normal! zo
91
normal! zo
110
normal! zo
115
normal! zo
152
normal! zo
163
normal! zo
176
normal! zo
185
normal! zo
195
normal! zo
203
normal! zo
203
normal! zo
203
normal! zo
203
normal! zo
203
normal! zo
231
normal! zo
241
normal! zo
245
normal! zo
254
normal! zo
264
normal! zo
279
normal! zo
279
normal! zo
288
normal! zo
288
normal! zo
297
normal! zo
297
normal! zo
297
normal! zo
297
normal! zo
297
normal! zo
297
normal! zo
314
normal! zo
315
normal! zo
let s:l = 53 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
53
normal! 0
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/db/tablas.sql
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
122
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
173
normal! zo
367
normal! zo
let s:l = 173 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
173
normal! 037|
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
50
normal! zo
55
normal! zo
63
normal! zo
63
normal! zo
274
normal! zo
let s:l = 254 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
254
normal! 025|
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
169
normal! zo
170
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
576
normal! zo
580
normal! zo
922
normal! zo
1068
normal! zo
1124
normal! zo
1140
normal! zo
1145
normal! zo
1146
normal! zo
1146
normal! zo
1146
normal! zo
1148
normal! zo
let s:l = 1140 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1140
normal! 012|
wincmd w
6wincmd w
exe '1resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 1resize ' . ((&columns * 33 + 57) / 114)
exe '2resize ' . ((&lines * 58 + 31) / 62)
exe 'vert 2resize ' . ((&columns * 33 + 57) / 114)
exe '3resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 114)
exe '4resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 114)
exe '5resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 114)
exe '6resize ' . ((&lines * 42 + 31) / 62)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 114)
exe '7resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 114)
exe '8resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 114)
exe '9resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 114)
exe '10resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 114)
exe '11resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 11resize ' . ((&columns * 80 + 57) / 114)
exe '12resize ' . ((&lines * 1 + 31) / 62)
exe 'vert 12resize ' . ((&columns * 80 + 57) / 114)
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
6wincmd w

" vim: ft=vim ro nowrap smc=128
