" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 25 marzo 2014 at 18:06:04.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Inconsolata\ 9
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
badd +1038 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1505 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +206 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +435 ginn/formularios/productos_de_venta_rollos.py
badd +315 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +337 ginn/formularios/productos_de_venta_especial.py
badd +3624 ginn/formularios/partes_de_fabricacion_balas.py
badd +1687 ginn/formularios/partes_de_fabricacion_bolsas.py
badd +1210 ginn/formularios/partes_de_fabricacion_rollos.py
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
badd +1037 ginn/formularios/facturas_venta.py
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
badd +136 ginn/formularios/utils.py
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
badd +433 ginn/formularios/consumo_balas_partida.py
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
badd +511 ginn/formularios/consulta_productividad.py
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
badd +75 ginn/formularios/consumo_fibra_por_partida_gtx.py
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
badd +1 extra/scripts/balas_basura_reembaladas.py
badd +1 extra/scripts/reset_existencias_BC.py
badd +1 ginn/formularios/consulta_producido
args formularios/auditviewer.py
set lines=51 columns=115
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
exe '1resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 1resize ' . ((&columns * 34 + 57) / 115)
exe '2resize ' . ((&lines * 47 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 34 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 115)
exe '7resize ' . ((&lines * 33 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 11resize ' . ((&columns * 80 + 57) / 115)
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
edit ~/Geotexan/src/Geotex-INN/db/tablas.sql
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
3504
normal! zo
3509
normal! zo
3511
normal! zo
let s:l = 1518 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1518
normal! 015|
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
4698
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
9907
normal! zo
9908
normal! zo
9917
normal! zo
9917
normal! zo
9917
normal! zo
9917
normal! zo
9929
normal! zo
9930
normal! zo
9931
normal! zo
9952
normal! zo
9968
normal! zo
9985
normal! zo
9985
normal! zo
9985
normal! zo
9985
normal! zo
9985
normal! zo
9985
normal! zo
9985
normal! zo
9985
normal! zo
9985
normal! zo
9992
normal! zo
10006
normal! zo
10007
normal! zo
10007
normal! zo
10009
normal! zo
10010
normal! zo
10010
normal! zo
10012
normal! zo
10013
normal! zo
10013
normal! zo
10015
normal! zo
10016
normal! zo
10016
normal! zo
10018
normal! zo
10021
normal! zo
10023
normal! zo
10023
normal! zo
10023
normal! zo
10032
normal! zo
10045
normal! zo
10048
normal! zo
10049
normal! zo
10049
normal! zo
10052
normal! zo
10052
normal! zo
10052
normal! zo
10055
normal! zo
10055
normal! zo
10055
normal! zo
10055
normal! zo
10061
normal! zo
10064
normal! zo
10068
normal! zo
10075
normal! zo
10077
normal! zo
10124
normal! zo
10138
normal! zo
10139
normal! zo
10141
normal! zo
10176
normal! zo
10183
normal! zo
10188
normal! zo
10189
normal! zo
10194
normal! zo
10194
normal! zo
10194
normal! zo
10194
normal! zo
10194
normal! zo
10197
normal! zo
10197
normal! zo
10197
normal! zo
10223
normal! zo
10232
normal! zo
10237
normal! zo
10239
normal! zo
10244
normal! zo
10250
normal! zo
10258
normal! zo
10259
normal! zo
10259
normal! zo
10259
normal! zo
10259
normal! zo
10268
normal! zo
10269
normal! zo
10274
normal! zo
10323
normal! zo
10328
normal! zo
10441
normal! zo
10468
normal! zo
10473
normal! zo
10479
normal! zo
10565
normal! zo
10572
normal! zo
10573
normal! zo
10621
normal! zo
10621
normal! zo
10621
normal! zo
10621
normal! zo
10621
normal! zo
10624
normal! zo
10632
normal! zo
10633
normal! zo
10678
normal! zo
10698
normal! zo
10699
normal! zo
10700
normal! zo
10700
normal! zo
10700
normal! zo
10700
normal! zo
10700
normal! zo
10700
normal! zo
10700
normal! zo
10700
normal! zo
10700
normal! zo
10717
normal! zo
10723
normal! zo
10733
normal! zo
10748
normal! zo
10751
normal! zo
10754
normal! zo
10754
normal! zo
10754
normal! zo
10757
normal! zo
10757
normal! zo
10757
normal! zo
10757
normal! zo
10762
normal! zo
10762
normal! zo
10762
normal! zo
10770
normal! zo
10777
normal! zo
10784
normal! zo
10787
normal! zo
10789
normal! zo
10792
normal! zo
10795
normal! zo
10800
normal! zo
10811
normal! zo
10818
normal! zo
10822
normal! zo
10823
normal! zo
10823
normal! zo
10825
normal! zo
10826
normal! zo
10826
normal! zo
10828
normal! zo
10829
normal! zo
10829
normal! zo
10831
normal! zo
10832
normal! zo
10832
normal! zo
10834
normal! zo
10835
normal! zo
10835
normal! zo
10837
normal! zo
10838
normal! zo
10838
normal! zo
10840
normal! zo
10841
normal! zo
10841
normal! zo
10843
normal! zo
10846
normal! zo
10848
normal! zo
10848
normal! zo
10848
normal! zo
10854
normal! zo
10855
normal! zo
10855
normal! zo
10857
normal! zo
10858
normal! zo
10858
normal! zo
10882
normal! zo
10886
normal! zo
10889
normal! zo
10890
normal! zo
10890
normal! zo
10890
normal! zo
10890
normal! zo
10890
normal! zo
10890
normal! zo
10895
normal! zo
10896
normal! zo
10896
normal! zo
10896
normal! zo
10899
normal! zo
11011
normal! zo
11087
normal! zo
11095
normal! zo
11102
normal! zo
11102
normal! zo
11102
normal! zo
11102
normal! zo
11102
normal! zo
11102
normal! zo
11102
normal! zo
11113
normal! zo
11117
normal! zo
11118
normal! zo
11118
normal! zo
11118
normal! zo
11128
normal! zo
11131
normal! zo
11138
normal! zo
11147
normal! zo
11156
normal! zo
11266
normal! zo
11267
normal! zc
11280
normal! zo
11280
normal! zo
11280
normal! zo
11280
normal! zo
11289
normal! zc
11292
normal! zo
11305
normal! zo
11318
normal! zo
11325
normal! zo
11327
normal! zo
11327
normal! zo
11327
normal! zo
11327
normal! zo
11327
normal! zo
11327
normal! zo
11335
normal! zc
11352
normal! zo
11380
normal! zo
11392
normal! zo
11393
normal! zo
11393
normal! zo
11393
normal! zo
11393
normal! zo
11352
normal! zc
11398
normal! zo
11398
normal! zc
11449
normal! zo
11449
normal! zc
11564
normal! zo
11572
normal! zo
11572
normal! zo
11572
normal! zo
11572
normal! zo
11564
normal! zc
11580
normal! zc
11586
normal! zo
11586
normal! zc
11597
normal! zo
11597
normal! zc
11614
normal! zo
11614
normal! zo
11618
normal! zo
11623
normal! zo
11623
normal! zo
11625
normal! zo
11626
normal! zo
11626
normal! zo
11631
normal! zo
11631
normal! zo
11631
normal! zo
11631
normal! zo
11631
normal! zo
11631
normal! zc
11644
normal! zo
11647
normal! zo
11647
normal! zo
11647
normal! zo
11647
normal! zo
11653
normal! zo
11653
normal! zo
11653
normal! zo
11653
normal! zo
11653
normal! zo
11653
normal! zc
11681
normal! zo
11719
normal! zc
11726
normal! zc
11734
normal! zo
11734
normal! zc
11742
normal! zc
11750
normal! zc
11764
normal! zo
11764
normal! zc
11782
normal! zo
11782
normal! zo
11782
normal! zo
11782
normal! zo
11782
normal! zo
11782
normal! zo
11782
normal! zo
11782
normal! zo
11782
normal! zo
11782
normal! zo
11782
normal! zc
11803
normal! zo
11803
normal! zo
11803
normal! zo
11803
normal! zo
11803
normal! zo
11803
normal! zo
11844
normal! zo
11845
normal! zo
11867
normal! zo
11867
normal! zc
11974
normal! zo
11974
normal! zc
12023
normal! zo
12023
normal! zo
12025
normal! zo
12035
normal! zo
12023
normal! zc
12118
normal! zo
12118
normal! zc
12172
normal! zo
12172
normal! zo
12172
normal! zo
12172
normal! zc
12172
normal! zc
12186
normal! zo
12223
normal! zo
12234
normal! zo
12239
normal! zo
12257
normal! zo
12257
normal! zo
12257
normal! zo
12257
normal! zo
12258
normal! zo
12263
normal! zo
12279
normal! zo
12279
normal! zo
12279
normal! zo
12279
normal! zo
12288
normal! zo
12288
normal! zo
12288
normal! zo
12288
normal! zo
12288
normal! zo
12312
normal! zo
12336
normal! zo
12336
normal! zc
12377
normal! zo
12377
normal! zo
12377
normal! zo
12377
normal! zo
12439
normal! zo
12455
normal! zo
12455
normal! zc
12479
normal! zo
12479
normal! zo
12479
normal! zo
12479
normal! zc
12504
normal! zo
12504
normal! zo
12504
normal! zo
12504
normal! zc
12579
normal! zo
12579
normal! zo
12579
normal! zo
12579
normal! zo
12579
normal! zo
12579
normal! zo
12579
normal! zo
12579
normal! zo
12579
normal! zc
12595
normal! zo
12595
normal! zc
12617
normal! zo
12617
normal! zc
12638
normal! zo
12638
normal! zo
12638
normal! zo
12638
normal! zo
12638
normal! zo
12638
normal! zo
12638
normal! zo
12638
normal! zc
12638
normal! zc
12758
normal! zo
12758
normal! zo
12758
normal! zo
12758
normal! zo
12758
normal! zo
12758
normal! zc
13026
normal! zo
13026
normal! zc
13056
normal! zo
13056
normal! zo
13056
normal! zo
13056
normal! zo
13056
normal! zo
13056
normal! zo
13056
normal! zo
13056
normal! zo
13071
normal! zo
13086
normal! zo
13088
normal! zo
13110
normal! zo
13118
normal! zo
13118
normal! zc
13134
normal! zo
13134
normal! zo
13173
normal! zo
13235
normal! zo
13236
normal! zo
13254
normal! zo
13296
normal! zo
13297
normal! zo
13325
normal! zo
13357
normal! zo
13358
normal! zo
13386
normal! zo
13422
normal! zo
13423
normal! zo
13441
normal! zo
13468
normal! zc
13478
normal! zo
13478
normal! zc
13498
normal! zo
13499
normal! zo
13500
normal! zo
13498
normal! zc
13554
normal! zo
13554
normal! zc
13612
normal! zo
13612
normal! zo
13612
normal! zo
13622
normal! zo
13627
normal! zo
13628
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
normal! zo
13629
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
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13637
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13639
normal! zo
13641
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13642
normal! zo
13645
normal! zo
13647
normal! zo
13647
normal! zo
13652
normal! zo
13652
normal! zo
13662
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13663
normal! zo
13670
normal! zo
13670
normal! zo
13670
normal! zo
13676
normal! zo
13677
normal! zo
13686
normal! zo
13687
normal! zo
13687
normal! zo
13687
normal! zo
13687
normal! zo
13691
normal! zo
13691
normal! zo
13691
normal! zo
13699
normal! zo
13700
normal! zo
13702
normal! zo
13710
normal! zo
13711
normal! zo
13711
normal! zo
13711
normal! zo
13711
normal! zo
13715
normal! zo
13715
normal! zo
13715
normal! zo
13722
normal! zo
13722
normal! zo
13722
normal! zo
13722
normal! zo
13722
normal! zo
13725
normal! zo
13726
normal! zo
13727
normal! zo
13728
normal! zo
13728
normal! zo
13729
normal! zo
13741
normal! zo
13742
normal! zo
13742
normal! zo
13742
normal! zo
13749
normal! zo
13750
normal! zo
13751
normal! zo
13751
normal! zo
13752
normal! zo
13763
normal! zo
13764
normal! zo
13765
normal! zo
13765
normal! zo
13766
normal! zo
13781
normal! zo
13782
normal! zo
13783
normal! zo
13784
normal! zo
13784
normal! zo
13785
normal! zo
13797
normal! zo
13798
normal! zo
13798
normal! zo
13798
normal! zo
13799
normal! zo
13805
normal! zo
13806
normal! zo
13807
normal! zo
13807
normal! zo
13808
normal! zo
13819
normal! zo
13820
normal! zo
13821
normal! zo
13821
normal! zo
13822
normal! zo
13837
normal! zo
13837
normal! zo
13837
normal! zo
13858
normal! zo
13863
normal! zo
13864
normal! zo
13865
normal! zo
13865
normal! zo
13865
normal! zo
13865
normal! zo
13865
normal! zo
13865
normal! zo
13865
normal! zo
13865
normal! zo
13865
normal! zo
13865
normal! zo
13871
normal! zo
13872
normal! zo
13873
normal! zo
13873
normal! zo
13873
normal! zo
13873
normal! zo
13873
normal! zo
13873
normal! zo
13873
normal! zo
13875
normal! zo
13875
normal! zo
13875
normal! zo
13875
normal! zo
13875
normal! zo
13875
normal! zo
13875
normal! zo
13875
normal! zo
13877
normal! zo
13878
normal! zo
13878
normal! zo
13878
normal! zo
13878
normal! zo
13878
normal! zo
13878
normal! zo
13878
normal! zo
13878
normal! zo
13878
normal! zo
13881
normal! zo
13883
normal! zo
13888
normal! zo
13897
normal! zo
13898
normal! zo
13898
normal! zo
13898
normal! zo
13898
normal! zo
13898
normal! zo
13898
normal! zo
13898
normal! zo
13905
normal! zo
13907
normal! zo
13908
normal! zo
13909
normal! zo
13909
normal! zo
13910
normal! zo
13920
normal! zo
13921
normal! zo
13922
normal! zo
13922
normal! zo
13923
normal! zo
13937
normal! zo
13938
normal! zo
13939
normal! zo
13940
normal! zo
13940
normal! zo
13941
normal! zo
13951
normal! zo
13952
normal! zo
13953
normal! zo
13953
normal! zo
13954
normal! zo
13968
normal! zo
13968
normal! zo
13968
normal! zo
13979
normal! zo
13984
normal! zo
13985
normal! zo
13986
normal! zo
13986
normal! zo
13986
normal! zo
13986
normal! zo
13986
normal! zo
13986
normal! zo
13986
normal! zo
13986
normal! zo
13986
normal! zo
13986
normal! zo
13992
normal! zo
13993
normal! zo
13994
normal! zo
13994
normal! zo
13994
normal! zo
13994
normal! zo
13994
normal! zo
13994
normal! zo
13994
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13996
normal! zo
13998
normal! zo
13999
normal! zo
13999
normal! zo
13999
normal! zo
13999
normal! zo
13999
normal! zo
13999
normal! zo
13999
normal! zo
13999
normal! zo
13999
normal! zo
14002
normal! zo
14004
normal! zo
14009
normal! zo
14018
normal! zo
14019
normal! zo
14019
normal! zo
14019
normal! zo
14019
normal! zo
14019
normal! zo
14019
normal! zo
14019
normal! zo
14026
normal! zo
14031
normal! zo
14032
normal! zo
14033
normal! zo
14040
normal! zo
14041
normal! zo
14042
normal! zo
14048
normal! zo
14049
normal! zo
14050
normal! zo
14055
normal! zo
14056
normal! zo
14057
normal! zo
14057
normal! zo
14067
normal! zo
14068
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14069
normal! zo
14076
normal! zo
14077
normal! zo
14077
normal! zo
14077
normal! zo
14077
normal! zo
14077
normal! zo
14077
normal! zo
14077
normal! zo
14084
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
14091
normal! zo
14092
normal! zo
14092
normal! zo
14092
normal! zo
14092
normal! zo
14092
normal! zo
14092
normal! zo
14092
normal! zo
14102
normal! zo
14108
normal! zo
14108
normal! zo
14114
normal! zo
14120
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14126
normal! zo
14136
normal! zo
14136
normal! zo
14136
normal! zo
14136
normal! zo
14136
normal! zo
14136
normal! zo
14138
normal! zo
14139
normal! zo
14139
normal! zo
14139
normal! zo
14145
normal! zo
14145
normal! zo
14145
normal! zo
14145
normal! zo
14145
normal! zo
14145
normal! zo
14145
normal! zo
14145
normal! zo
14145
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14156
normal! zo
14158
normal! zo
14159
normal! zo
14159
normal! zo
14159
normal! zo
14165
normal! zo
14165
normal! zo
14165
normal! zo
14165
normal! zo
14173
normal! zo
14178
normal! zo
14181
normal! zo
14186
normal! zo
14187
normal! zo
14188
normal! zo
14188
normal! zo
14188
normal! zo
14188
normal! zo
14188
normal! zo
14188
normal! zo
14188
normal! zo
14188
normal! zo
14188
normal! zo
14188
normal! zo
14194
normal! zo
14195
normal! zo
14198
normal! zo
14199
normal! zo
14199
normal! zo
14199
normal! zo
14199
normal! zo
14199
normal! zo
14199
normal! zo
14199
normal! zo
14201
normal! zo
14201
normal! zo
14201
normal! zo
14201
normal! zo
14201
normal! zo
14201
normal! zo
14201
normal! zo
14201
normal! zo
14201
normal! zo
14203
normal! zo
14204
normal! zo
14207
normal! zo
14207
normal! zo
14207
normal! zo
14207
normal! zo
14207
normal! zo
14207
normal! zo
14207
normal! zo
14207
normal! zo
14207
normal! zo
14210
normal! zo
14211
normal! zo
14215
normal! zo
14215
normal! zo
14220
normal! zo
14220
normal! zo
14225
normal! zo
14226
normal! zo
14233
normal! zo
14234
normal! zo
14237
normal! zo
14237
normal! zo
14237
normal! zo
14237
normal! zo
14237
normal! zo
14237
normal! zo
14244
normal! zo
14245
normal! zo
14246
normal! zo
14247
normal! zo
14253
normal! zo
14254
normal! zo
14255
normal! zo
14261
normal! zo
14262
normal! zo
14262
normal! zo
14263
normal! zo
14268
normal! zo
14269
normal! zo
14269
normal! zo
14270
normal! zo
14279
normal! zo
14280
normal! zo
14281
normal! zo
14281
normal! zo
14281
normal! zo
14281
normal! zo
14281
normal! zo
14281
normal! zo
14288
normal! zo
14289
normal! zo
14290
normal! zo
14296
normal! zo
14297
normal! zo
14297
normal! zo
14297
normal! zo
14297
normal! zo
14297
normal! zo
14297
normal! zo
14297
normal! zo
14303
normal! zo
14304
normal! zo
14304
normal! zo
14304
normal! zo
14304
normal! zo
14304
normal! zo
14304
normal! zo
14304
normal! zo
14315
normal! zo
14316
normal! zo
14316
normal! zo
14322
normal! zo
14328
normal! zo
14328
normal! zo
14334
normal! zo
14334
normal! zo
14334
normal! zo
14334
normal! zo
14350
normal! zo
14355
normal! zo
14356
normal! zo
14357
normal! zo
14357
normal! zo
14357
normal! zo
14357
normal! zo
14357
normal! zo
14357
normal! zo
14357
normal! zo
14357
normal! zo
14357
normal! zo
14357
normal! zo
14363
normal! zo
14364
normal! zo
14365
normal! zo
14365
normal! zo
14365
normal! zo
14365
normal! zo
14365
normal! zo
14365
normal! zo
14365
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14367
normal! zo
14369
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14373
normal! zo
14375
normal! zo
14375
normal! zo
14380
normal! zo
14380
normal! zo
14390
normal! zo
14391
normal! zo
14391
normal! zo
14391
normal! zo
14391
normal! zo
14391
normal! zo
14391
normal! zo
14398
normal! zo
14399
normal! zo
14400
normal! zo
14401
normal! zo
14406
normal! zo
14407
normal! zo
14408
normal! zo
14418
normal! zo
14419
normal! zo
14420
normal! zo
14420
normal! zo
14420
normal! zo
14420
normal! zo
14420
normal! zo
14420
normal! zo
14425
normal! zo
14426
normal! zo
14426
normal! zo
14426
normal! zo
14427
normal! zo
14437
normal! zo
14438
normal! zo
14438
normal! zo
14444
normal! zo
14445
normal! zo
14445
normal! zo
14451
normal! zo
14451
normal! zo
14451
normal! zo
14451
normal! zo
14463
normal! zo
14468
normal! zo
14469
normal! zo
14470
normal! zo
14470
normal! zo
14470
normal! zo
14470
normal! zo
14470
normal! zo
14470
normal! zo
14470
normal! zo
14470
normal! zo
14470
normal! zo
14470
normal! zo
14476
normal! zo
14477
normal! zo
14478
normal! zo
14478
normal! zo
14478
normal! zo
14478
normal! zo
14478
normal! zo
14478
normal! zo
14478
normal! zo
14480
normal! zo
14480
normal! zo
14480
normal! zo
14480
normal! zo
14480
normal! zo
14480
normal! zo
14480
normal! zo
14480
normal! zo
14480
normal! zo
14482
normal! zo
14483
normal! zo
14483
normal! zo
14483
normal! zo
14483
normal! zo
14483
normal! zo
14483
normal! zo
14483
normal! zo
14483
normal! zo
14483
normal! zo
14486
normal! zo
14488
normal! zo
14488
normal! zo
14493
normal! zo
14493
normal! zo
14503
normal! zo
14504
normal! zo
14504
normal! zo
14504
normal! zo
14504
normal! zo
14504
normal! zo
14504
normal! zo
14511
normal! zo
14518
normal! zo
14519
normal! zo
14521
normal! zo
14521
normal! zo
14521
normal! zo
14527
normal! zo
14529
normal! zo
14531
normal! zo
14537
normal! zo
14539
normal! zo
14541
normal! zo
14552
normal! zo
14572
normal! zo
14584
normal! zo
14585
normal! zo
14586
normal! zo
14588
normal! zo
14589
normal! zo
14590
normal! zo
14590
normal! zo
14590
normal! zo
14592
normal! zo
14593
normal! zo
14593
normal! zo
14593
normal! zo
14609
normal! zo
14620
normal! zo
14629
normal! zo
14639
normal! zo
14666
normal! zo
14671
normal! zo
14677
normal! zo
14688
normal! zo
14701
normal! zo
14725
normal! zo
14727
normal! zo
14730
normal! zo
14733
normal! zo
14734
normal! zo
14738
normal! zo
14739
normal! zo
14753
normal! zo
14753
normal! zo
14753
normal! zo
14753
normal! zo
14775
normal! zo
14776
normal! zo
14777
normal! zo
14777
normal! zo
14777
normal! zo
14777
normal! zo
14777
normal! zo
14777
normal! zo
14777
normal! zo
14777
normal! zo
14777
normal! zo
14777
normal! zo
14786
normal! zo
14787
normal! zo
14793
normal! zo
14797
normal! zo
14798
normal! zo
14807
normal! zo
14808
normal! zo
14816
normal! zo
14817
normal! zo
14823
normal! zo
14838
normal! zo
14846
normal! zo
14852
normal! zo
14858
normal! zo
14863
normal! zo
14867
normal! zo
14873
normal! zo
14878
normal! zo
14879
normal! zo
14884
normal! zo
14895
normal! zo
14913
normal! zo
14955
normal! zo
14961
normal! zo
14972
normal! zo
14981
normal! zo
14985
normal! zo
14994
normal! zo
14996
normal! zo
15003
normal! zo
15003
normal! zo
15003
normal! zo
15003
normal! zo
15003
normal! zo
15003
normal! zo
15020
normal! zo
15032
normal! zo
15043
normal! zo
15044
normal! zo
15060
normal! zo
15077
normal! zo
15081
normal! zo
15082
normal! zo
15083
normal! zo
15083
normal! zo
15085
normal! zo
15088
normal! zo
15101
normal! zo
15111
normal! zo
15113
normal! zo
15117
normal! zo
15118
normal! zo
15118
normal! zo
15118
normal! zo
15118
normal! zo
15118
normal! zo
15118
normal! zo
15131
normal! zo
15152
normal! zo
15153
normal! zo
15160
normal! zo
15193
normal! zo
15194
normal! zo
15194
normal! zo
15210
normal! zo
15216
normal! zo
15219
normal! zo
15219
normal! zo
15219
normal! zo
15225
normal! zo
15225
normal! zo
15245
normal! zo
15250
normal! zo
15255
normal! zo
15263
normal! zo
15282
normal! zo
15316
normal! zo
15324
normal! zo
15333
normal! zo
15352
normal! zo
15354
normal! zo
15358
normal! zo
15375
normal! zo
15381
normal! zo
15385
normal! zo
15424
normal! zo
15528
normal! zo
15528
normal! zo
15604
normal! zo
15604
normal! zo
15604
normal! zo
15717
normal! zo
15748
normal! zo
15772
normal! zo
15782
normal! zo
15782
normal! zo
15782
normal! zo
15782
normal! zo
15782
normal! zo
15970
normal! zo
15989
normal! zo
16011
normal! zo
16016
normal! zo
16017
normal! zo
16017
normal! zo
16020
normal! zo
16021
normal! zo
16021
normal! zo
16021
normal! zo
16024
normal! zo
16024
normal! zo
16024
normal! zo
16028
normal! zo
16028
normal! zo
16028
normal! zo
16028
normal! zo
16028
normal! zo
16028
normal! zo
16028
normal! zo
16028
normal! zo
16028
normal! zo
16333
normal! zo
16491
normal! zo
16559
normal! zo
16595
normal! zo
16610
normal! zo
16616
normal! zo
16619
normal! zo
16627
normal! zo
16628
normal! zo
16628
normal! zo
16628
normal! zo
16628
normal! zo
16628
normal! zo
16632
normal! zo
16640
normal! zo
16643
normal! zo
16649
normal! zo
16655
normal! zo
16658
normal! zo
16664
normal! zo
16678
normal! zo
16684
normal! zo
16689
normal! zo
16692
normal! zo
16692
normal! zo
16692
normal! zo
16702
normal! zo
16717
normal! zo
16728
normal! zo
16728
normal! zo
16739
normal! zo
16754
normal! zo
16764
normal! zo
16775
normal! zo
16783
normal! zo
16788
normal! zo
16804
normal! zo
16842
normal! zo
16870
normal! zo
16871
normal! zo
16871
normal! zo
16871
normal! zo
16871
normal! zo
16871
normal! zo
16871
normal! zo
16871
normal! zo
16871
normal! zo
16871
normal! zo
16871
normal! zo
16871
normal! zo
16883
normal! zo
16891
normal! zo
16892
normal! zo
16895
normal! zo
16896
normal! zo
16902
normal! zo
16923
normal! zo
16942
normal! zo
16950
normal! zo
16951
normal! zo
16960
normal! zo
16976
normal! zo
16996
normal! zo
17001
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17014
normal! zo
17093
normal! zo
17106
normal! zo
17107
normal! zo
17108
normal! zo
17114
normal! zo
17118
normal! zo
17120
normal! zo
17135
normal! zo
17151
normal! zo
17159
normal! zo
17163
normal! zo
17168
normal! zo
17176
normal! zo
17181
normal! zo
17189
normal! zo
17194
normal! zo
17214
normal! zo
17229
normal! zo
17230
normal! zo
17246
normal! zo
17283
normal! zo
17297
normal! zo
17300
normal! zo
17304
normal! zo
17305
normal! zo
17324
normal! zo
17339
normal! zo
17346
normal! zo
17347
normal! zo
17353
normal! zo
17360
normal! zo
17365
normal! zo
17393
normal! zo
17413
normal! zo
17414
normal! zo
17436
normal! zo
17450
normal! zo
17457
normal! zo
17458
normal! zo
17472
normal! zo
17508
normal! zo
17529
normal! zo
17552
normal! zo
17565
normal! zo
17589
normal! zo
17594
normal! zo
17618
normal! zo
17636
normal! zo
17654
normal! zo
17655
normal! zo
17666
normal! zo
17690
normal! zo
17703
normal! zo
17707
normal! zo
17707
normal! zo
17707
normal! zo
17707
normal! zo
17707
normal! zo
17721
normal! zo
17721
normal! zo
17721
normal! zo
17721
normal! zo
17721
normal! zo
17721
normal! zo
17721
normal! zo
17835
normal! zo
17843
normal! zo
17865
normal! zo
17888
normal! zo
17953
normal! zo
18010
normal! zo
18025
normal! zo
18059
normal! zo
18073
normal! zo
18099
normal! zo
18119
normal! zo
18131
normal! zo
18131
normal! zo
18131
normal! zo
18131
normal! zo
18131
normal! zo
18134
normal! zo
18141
normal! zo
18144
normal! zo
18155
normal! zo
18161
normal! zo
18166
normal! zo
18177
normal! zo
18196
normal! zo
18239
normal! zo
18264
normal! zo
18320
normal! zo
18329
normal! zo
18774
normal! zo
18846
normal! zo
18852
normal! zo
18855
normal! zo
18868
normal! zo
18885
normal! zo
18895
normal! zo
18898
normal! zo
18899
normal! zo
18899
normal! zo
18905
normal! zo
18912
normal! zo
19164
normal! zo
19210
normal! zo
19220
normal! zo
19221
normal! zo
19221
normal! zo
19221
normal! zo
19221
normal! zo
19221
normal! zo
19501
normal! zo
20111
normal! zo
20119
normal! zo
20153
normal! zo
20165
normal! zo
20170
normal! zo
20177
normal! zo
20189
normal! zo
20207
normal! zo
20217
normal! zo
20254
normal! zo
20373
normal! zo
20391
normal! zo
20399
normal! zo
20428
normal! zo
20499
normal! zo
20500
normal! zo
20512
normal! zo
20527
normal! zo
20534
normal! zo
20541
normal! zo
20548
normal! zo
20555
normal! zo
20562
normal! zo
20569
normal! zo
20575
normal! zo
20694
normal! zo
20712
normal! zo
20741
normal! zo
20757
normal! zo
20767
normal! zo
20778
normal! zo
20789
normal! zo
20806
normal! zo
20806
normal! zo
20806
normal! zo
20806
normal! zo
20806
normal! zo
20806
normal! zo
20806
normal! zo
20806
normal! zo
20806
normal! zo
20826
normal! zo
20826
normal! zo
20826
normal! zo
20826
normal! zo
20826
normal! zo
20826
normal! zo
20826
normal! zo
20826
normal! zo
20846
normal! zo
20894
normal! zo
20906
normal! zo
20907
normal! zo
20915
normal! zo
20932
normal! zo
20932
normal! zo
20932
normal! zo
20932
normal! zo
20932
normal! zo
20932
normal! zo
20932
normal! zo
21079
normal! zo
21086
normal! zo
21088
normal! zo
21092
normal! zo
let s:l = 9933 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9933
normal! 021|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/extra/scripts/balas_basura_reembaladas.py
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
52
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
60
normal! zo
65
normal! zo
68
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
80
normal! zo
102
normal! zo
103
normal! zo
106
normal! zo
107
normal! zo
110
normal! zo
111
normal! zo
118
normal! zo
127
normal! zo
132
normal! zo
134
normal! zo
134
normal! zo
134
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
136
normal! zo
142
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
173
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
186
normal! zo
196
normal! zo
206
normal! zo
209
normal! zo
217
normal! zo
224
normal! zo
225
normal! zo
225
normal! zo
225
normal! zo
225
normal! zo
225
normal! zo
240
normal! zo
249
normal! zo
252
normal! zo
258
normal! zo
263
normal! zo
268
normal! zo
298
normal! zo
299
normal! zo
let s:l = 72 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
72
normal! 030|
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
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
71
normal! zo
91
normal! zo
99
normal! zo
126
normal! zo
148
normal! zo
153
normal! zo
169
normal! zo
170
normal! zo
170
normal! zo
170
normal! zo
170
normal! zo
170
normal! zo
180
normal! zo
184
normal! zo
190
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
204
normal! zo
216
normal! zo
217
normal! zo
217
normal! zo
217
normal! zo
217
normal! zo
217
normal! zo
227
normal! zo
234
normal! zo
235
normal! zo
235
normal! zo
235
normal! zo
235
normal! zo
257
normal! zo
271
normal! zo
275
normal! zo
276
normal! zo
277
normal! zo
281
normal! zo
303
normal! zo
308
normal! zo
341
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
347
normal! zo
349
normal! zo
349
normal! zo
349
normal! zo
349
normal! zo
349
normal! zo
350
normal! zo
383
normal! zo
393
normal! zo
394
normal! zo
400
normal! zo
406
normal! zo
411
normal! zo
424
normal! zo
430
normal! zo
let s:l = 121 - ((12 * winheight(0) + 16) / 33)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
121
normal! 0
lcd ~/Geotexan/src/Geotex-INN
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
normal! 029|
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
7wincmd w
exe '1resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 1resize ' . ((&columns * 34 + 57) / 115)
exe '2resize ' . ((&lines * 47 + 25) / 51)
exe 'vert 2resize ' . ((&columns * 34 + 57) / 115)
exe '3resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 3resize ' . ((&columns * 80 + 57) / 115)
exe '4resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 4resize ' . ((&columns * 80 + 57) / 115)
exe '5resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 5resize ' . ((&columns * 80 + 57) / 115)
exe '6resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 6resize ' . ((&columns * 80 + 57) / 115)
exe '7resize ' . ((&lines * 33 + 25) / 51)
exe 'vert 7resize ' . ((&columns * 80 + 57) / 115)
exe '8resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 8resize ' . ((&columns * 80 + 57) / 115)
exe '9resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 9resize ' . ((&columns * 80 + 57) / 115)
exe '10resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 10resize ' . ((&columns * 80 + 57) / 115)
exe '11resize ' . ((&lines * 1 + 25) / 51)
exe 'vert 11resize ' . ((&columns * 80 + 57) / 115)
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
