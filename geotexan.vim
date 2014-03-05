" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 05 marzo 2014 at 23:20:31.
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
badd +809 ginn/formularios/consulta_producido.py
badd +1 ginn/__init__.py
badd +1505 ginn/formularios/clientes.py
badd +991 ginn/formularios/productos_compra.py
badd +206 ginn/formularios/productos_de_venta_balas.py
badd +525 ginn/formularios/recibos.py
badd +374 ginn/formularios/productos_de_venta_rollos.py
badd +315 ginn/formularios/productos_de_venta_rollos_geocompuestos.py
badd +337 ginn/formularios/productos_de_venta_especial.py
badd +1868 ginn/formularios/partes_de_fabricacion_balas.py
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
badd +1 ginn/formularios/albaranes_de_salida.py
badd +93 ginn/formularios/presupuesto.py
badd +1884 ginn/formularios/presupuestos.py
badd +97 ginn/informes/carta_compromiso.py
badd +367 ginn/formularios/tarifas_de_precios.py
badd +88 ginn/formularios/logviewer.py
badd +1527 ginn/formularios/facturas_compra.py
badd +2785 ginn/formularios/utils.py
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
badd +44 ginn/informes/treeview2pdf.py
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
badd +1020 ginn/formularios/pagares_cobros.py
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
badd +193 ginn/formularios/consulta_productividad.py
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
badd +450 ginn/formularios/prefacturas.py
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
badd +92 ginn/informes/treeview2csv.py
badd +287 ginn/formularios/consulta_ventas_por_producto.py
badd +1 tests/stock_performance.py
badd +1 (clewn)_console
badd +1 ginn/formularios/consulta_productividad.glade
args formularios/auditviewer.py
set lines=63 columns=107
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
exe '1resize ' . ((&lines * 6 + 31) / 63)
exe 'vert 1resize ' . ((&columns * 26 + 53) / 107)
exe '2resize ' . ((&lines * 54 + 31) / 63)
exe 'vert 2resize ' . ((&columns * 26 + 53) / 107)
exe '3resize ' . ((&lines * 7 + 31) / 63)
exe 'vert 3resize ' . ((&columns * 80 + 53) / 107)
exe '4resize ' . ((&lines * 18 + 31) / 63)
exe 'vert 4resize ' . ((&columns * 80 + 53) / 107)
exe '5resize ' . ((&lines * 13 + 31) / 63)
exe 'vert 5resize ' . ((&columns * 80 + 53) / 107)
exe '6resize ' . ((&lines * 10 + 31) / 63)
exe 'vert 6resize ' . ((&columns * 80 + 53) / 107)
exe '7resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 7resize ' . ((&columns * 80 + 53) / 107)
exe '8resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 8resize ' . ((&columns * 80 + 53) / 107)
exe '9resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 9resize ' . ((&columns * 80 + 53) / 107)
exe '10resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 10resize ' . ((&columns * 80 + 53) / 107)
exe '11resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 11resize ' . ((&columns * 80 + 53) / 107)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 3) / 6)
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
2021
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2034
normal! zo
2043
normal! zo
2065
normal! zo
2070
normal! zo
2070
normal! zo
2196
normal! zo
2830
normal! zo
2839
normal! zo
3062
normal! zo
3260
normal! zo
3272
normal! zo
3273
normal! zo
3274
normal! zo
4209
normal! zo
4239
normal! zo
let s:l = 4794 - ((0 * winheight(0) + 3) / 7)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
4794
normal! 0
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
644
normal! zo
683
normal! zo
747
normal! zo
757
normal! zo
763
normal! zo
790
normal! zo
1115
normal! zo
1207
normal! zo
1216
normal! zo
1258
normal! zo
1264
normal! zo
1264
normal! zo
1264
normal! zo
1291
normal! zo
1297
normal! zo
1297
normal! zo
1297
normal! zo
1316
normal! zo
1325
normal! zo
1400
normal! zo
1425
normal! zo
1434
normal! zo
1509
normal! zo
1534
normal! zo
1543
normal! zo
1618
normal! zo
1643
normal! zo
1764
normal! zo
1806
normal! zo
1847
normal! zo
1847
normal! zo
1847
normal! zo
2465
normal! zo
2844
normal! zo
3053
normal! zo
3542
normal! zo
3854
normal! zo
3888
normal! zo
3890
normal! zo
3946
normal! zo
3953
normal! zo
3954
normal! zo
3954
normal! zo
3954
normal! zo
3954
normal! zo
3954
normal! zo
3954
normal! zo
3978
normal! zo
4028
normal! zo
4031
normal! zo
4036
normal! zo
4037
normal! zo
4037
normal! zo
4037
normal! zo
4041
normal! zo
4041
normal! zo
4041
normal! zo
4041
normal! zo
4041
normal! zo
4041
normal! zo
4044
normal! zo
4044
normal! zo
4050
normal! zo
4052
normal! zo
4057
normal! zo
4060
normal! zo
4062
normal! zo
4067
normal! zo
4068
normal! zo
4078
normal! zo
4086
normal! zo
4087
normal! zo
4087
normal! zo
4087
normal! zo
4087
normal! zo
4091
normal! zo
4094
normal! zo
4095
normal! zo
4095
normal! zo
4095
normal! zo
4095
normal! zo
4095
normal! zo
4109
normal! zo
4132
normal! zo
4176
normal! zo
4589
normal! zo
4600
normal! zo
4734
normal! zo
4819
normal! zo
4858
normal! zo
4870
normal! zo
4871
normal! zo
4871
normal! zo
4871
normal! zo
5148
normal! zo
5172
normal! zo
5183
normal! zo
5183
normal! zo
5183
normal! zo
5192
normal! zo
5212
normal! zo
5221
normal! zo
5222
normal! zo
5235
normal! zo
5241
normal! zo
5241
normal! zo
5241
normal! zo
5241
normal! zo
5257
normal! zo
5257
normal! zo
5257
normal! zo
5257
normal! zo
5257
normal! zo
5353
normal! zo
5359
normal! zo
5383
normal! zo
5410
normal! zo
5500
normal! zo
5512
normal! zo
5513
normal! zo
5514
normal! zo
5514
normal! zo
5514
normal! zo
5514
normal! zo
5516
normal! zo
5516
normal! zo
5516
normal! zo
5516
normal! zo
5516
normal! zo
5567
normal! zo
5567
normal! zo
5567
normal! zo
5567
normal! zo
5567
normal! zo
5595
normal! zo
5598
normal! zo
5617
normal! zo
5618
normal! zo
5619
normal! zo
5629
normal! zo
5681
normal! zo
5682
normal! zo
5802
normal! zo
5857
normal! zo
5869
normal! zo
5934
normal! zo
5978
normal! zo
5986
normal! zo
6013
normal! zo
6026
normal! zo
6030
normal! zo
6036
normal! zo
6169
normal! zo
6295
normal! zo
6889
normal! zo
7139
normal! zo
7146
normal! zo
7546
normal! zo
7575
normal! zo
7575
normal! zo
7575
normal! zo
7575
normal! zo
7575
normal! zo
7599
normal! zo
7668
normal! zo
7687
normal! zo
7690
normal! zo
7691
normal! zo
7691
normal! zo
7691
normal! zo
7704
normal! zo
7705
normal! zo
7706
normal! zo
7711
normal! zo
7717
normal! zo
7723
normal! zo
7723
normal! zo
7723
normal! zo
7723
normal! zo
7723
normal! zo
7723
normal! zo
7725
normal! zo
7764
normal! zo
7774
normal! zo
7775
normal! zo
7783
normal! zo
7784
normal! zo
7787
normal! zo
7792
normal! zo
7793
normal! zo
7794
normal! zo
7795
normal! zo
7795
normal! zo
7795
normal! zo
7795
normal! zo
7795
normal! zo
7795
normal! zo
7799
normal! zo
7805
normal! zo
7808
normal! zo
7808
normal! zo
7808
normal! zo
7808
normal! zo
7808
normal! zo
7817
normal! zo
7818
normal! zo
7819
normal! zo
7827
normal! zo
7834
normal! zo
7834
normal! zo
7834
normal! zo
7834
normal! zo
7834
normal! zo
7834
normal! zo
7836
normal! zo
7836
normal! zo
7836
normal! zo
7836
normal! zo
7836
normal! zo
7836
normal! zo
7836
normal! zo
7839
normal! zo
7839
normal! zo
7839
normal! zo
7839
normal! zo
7839
normal! zo
7839
normal! zo
7840
normal! zo
7840
normal! zo
7840
normal! zo
7840
normal! zo
7842
normal! zo
7843
normal! zo
7852
normal! zo
7859
normal! zo
7859
normal! zo
7859
normal! zo
7859
normal! zo
7859
normal! zo
7859
normal! zo
7861
normal! zo
7864
normal! zo
7864
normal! zo
7864
normal! zo
7864
normal! zo
7864
normal! zo
7864
normal! zo
7865
normal! zo
7865
normal! zo
7865
normal! zo
7865
normal! zo
7867
normal! zo
7868
normal! zo
7871
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7876
normal! zo
7924
normal! zo
7929
normal! zo
7931
normal! zo
7932
normal! zo
7932
normal! zo
7932
normal! zo
7932
normal! zo
7932
normal! zo
7932
normal! zo
7935
normal! zo
7941
normal! zo
7944
normal! zo
7953
normal! zo
7955
normal! zo
7956
normal! zo
7963
normal! zo
7964
normal! zo
7965
normal! zo
7970
normal! zo
7974
normal! zo
7982
normal! zo
7983
normal! zo
7985
normal! zo
7985
normal! zo
7992
normal! zo
7993
normal! zo
7994
normal! zo
7994
normal! zo
7994
normal! zo
7994
normal! zo
7994
normal! zo
7994
normal! zo
7994
normal! zo
7994
normal! zo
7997
normal! zo
7997
normal! zo
7997
normal! zo
8004
normal! zo
8006
normal! zo
8289
normal! zo
8300
normal! zo
8301
normal! zo
8301
normal! zo
8301
normal! zo
8301
normal! zo
8301
normal! zo
8301
normal! zo
8301
normal! zo
8304
normal! zo
8304
normal! zo
8304
normal! zo
8304
normal! zo
8304
normal! zo
8304
normal! zo
8304
normal! zo
8308
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8315
normal! zo
8318
normal! zo
8318
normal! zo
8318
normal! zo
8318
normal! zo
8318
normal! zo
8318
normal! zo
8318
normal! zo
8318
normal! zo
8753
normal! zo
8757
normal! zo
8788
normal! zo
8837
normal! zo
8844
normal! zo
9012
normal! zo
9023
normal! zo
9036
normal! zo
9037
normal! zo
9050
normal! zo
9055
normal! zo
9060
normal! zo
9065
normal! zo
9076
normal! zo
9099
normal! zo
9122
normal! zo
9123
normal! zo
9123
normal! zo
9123
normal! zo
9123
normal! zo
9123
normal! zo
9123
normal! zo
9134
normal! zo
9149
normal! zo
9184
normal! zo
9272
normal! zo
9303
normal! zo
9310
normal! zo
9314
normal! zo
9319
normal! zo
9334
normal! zo
9382
normal! zo
9423
normal! zo
9685
normal! zo
9711
normal! zo
9750
normal! zo
9761
normal! zo
9762
normal! zo
9775
normal! zo
9787
normal! zo
9801
normal! zo
9817
normal! zo
9834
normal! zo
9834
normal! zo
9834
normal! zo
9834
normal! zo
9834
normal! zo
9834
normal! zo
9834
normal! zo
9834
normal! zo
9834
normal! zo
9841
normal! zo
9855
normal! zo
9856
normal! zo
9856
normal! zo
9858
normal! zo
9859
normal! zo
9859
normal! zo
9861
normal! zo
9862
normal! zo
9862
normal! zo
9864
normal! zo
9865
normal! zo
9865
normal! zo
9867
normal! zo
9870
normal! zo
9872
normal! zo
9872
normal! zo
9872
normal! zo
9881
normal! zo
9894
normal! zo
9897
normal! zo
9898
normal! zo
9898
normal! zo
9901
normal! zo
9901
normal! zo
9901
normal! zo
9904
normal! zo
9904
normal! zo
9904
normal! zo
9904
normal! zo
9910
normal! zo
9913
normal! zo
9917
normal! zo
9924
normal! zo
9926
normal! zo
9973
normal! zo
9987
normal! zo
9988
normal! zo
9990
normal! zo
10025
normal! zo
10032
normal! zo
10037
normal! zo
10038
normal! zo
10043
normal! zo
10043
normal! zo
10043
normal! zo
10043
normal! zo
10043
normal! zo
10046
normal! zo
10046
normal! zo
10046
normal! zo
10072
normal! zo
10081
normal! zo
10086
normal! zo
10088
normal! zo
10093
normal! zo
10099
normal! zo
10107
normal! zo
10108
normal! zo
10108
normal! zo
10108
normal! zo
10108
normal! zo
10117
normal! zo
10118
normal! zo
10123
normal! zo
10172
normal! zo
10177
normal! zo
10290
normal! zo
10317
normal! zo
10322
normal! zo
10328
normal! zo
10414
normal! zo
10421
normal! zo
10422
normal! zo
10470
normal! zo
10470
normal! zo
10470
normal! zo
10470
normal! zo
10470
normal! zo
10473
normal! zo
10481
normal! zo
10482
normal! zo
10527
normal! zo
10547
normal! zo
10548
normal! zo
10549
normal! zo
10549
normal! zo
10549
normal! zo
10549
normal! zo
10549
normal! zo
10549
normal! zo
10549
normal! zo
10549
normal! zo
10549
normal! zo
10566
normal! zo
10572
normal! zo
10582
normal! zo
10597
normal! zo
10600
normal! zo
10603
normal! zo
10603
normal! zo
10603
normal! zo
10606
normal! zo
10606
normal! zo
10606
normal! zo
10606
normal! zo
10611
normal! zo
10611
normal! zo
10611
normal! zo
10619
normal! zo
10626
normal! zo
10633
normal! zo
10636
normal! zo
10638
normal! zo
10641
normal! zo
10644
normal! zo
10649
normal! zo
10660
normal! zo
10667
normal! zo
10671
normal! zo
10672
normal! zo
10672
normal! zo
10674
normal! zo
10675
normal! zo
10675
normal! zo
10677
normal! zo
10678
normal! zo
10678
normal! zo
10680
normal! zo
10681
normal! zo
10681
normal! zo
10683
normal! zo
10684
normal! zo
10684
normal! zo
10686
normal! zo
10687
normal! zo
10687
normal! zo
10689
normal! zo
10690
normal! zo
10690
normal! zo
10692
normal! zo
10695
normal! zo
10697
normal! zo
10697
normal! zo
10697
normal! zo
10703
normal! zo
10704
normal! zo
10704
normal! zo
10706
normal! zo
10707
normal! zo
10707
normal! zo
10731
normal! zo
10735
normal! zo
10738
normal! zo
10739
normal! zo
10739
normal! zo
10739
normal! zo
10739
normal! zo
10739
normal! zo
10739
normal! zo
10744
normal! zo
10745
normal! zo
10745
normal! zo
10745
normal! zo
10748
normal! zo
10860
normal! zo
10936
normal! zo
10944
normal! zo
10951
normal! zo
10951
normal! zo
10951
normal! zo
10951
normal! zo
10951
normal! zo
10951
normal! zo
10951
normal! zo
10962
normal! zo
10966
normal! zo
10967
normal! zo
10967
normal! zo
10967
normal! zo
10977
normal! zo
10980
normal! zo
10987
normal! zo
10996
normal! zo
11005
normal! zo
11115
normal! zo
11116
normal! zc
11129
normal! zo
11129
normal! zo
11129
normal! zo
11129
normal! zo
11138
normal! zc
11141
normal! zo
11154
normal! zo
11167
normal! zo
11174
normal! zo
11176
normal! zo
11176
normal! zo
11176
normal! zo
11176
normal! zo
11176
normal! zo
11176
normal! zo
11184
normal! zc
11201
normal! zo
11229
normal! zo
11241
normal! zo
11242
normal! zo
11242
normal! zo
11242
normal! zo
11242
normal! zo
11201
normal! zc
11247
normal! zo
11247
normal! zc
11298
normal! zo
11298
normal! zc
11413
normal! zo
11421
normal! zo
11421
normal! zo
11421
normal! zo
11421
normal! zo
11413
normal! zc
11429
normal! zc
11435
normal! zo
11435
normal! zc
11446
normal! zo
11446
normal! zc
11463
normal! zo
11463
normal! zo
11467
normal! zo
11472
normal! zo
11472
normal! zo
11474
normal! zo
11475
normal! zo
11475
normal! zo
11480
normal! zo
11480
normal! zo
11480
normal! zo
11480
normal! zo
11480
normal! zo
11480
normal! zc
11493
normal! zo
11496
normal! zo
11496
normal! zo
11496
normal! zo
11496
normal! zo
11502
normal! zo
11502
normal! zo
11502
normal! zo
11502
normal! zo
11502
normal! zo
11502
normal! zc
11530
normal! zo
11568
normal! zc
11575
normal! zc
11583
normal! zo
11583
normal! zc
11591
normal! zc
11599
normal! zc
11613
normal! zo
11613
normal! zc
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
11652
normal! zo
11652
normal! zo
11652
normal! zo
11652
normal! zo
11652
normal! zo
11652
normal! zo
11693
normal! zo
11694
normal! zo
11716
normal! zo
11716
normal! zc
11823
normal! zo
11823
normal! zc
11872
normal! zo
11872
normal! zo
11874
normal! zo
11884
normal! zo
11872
normal! zc
11967
normal! zo
11967
normal! zc
12021
normal! zo
12021
normal! zo
12021
normal! zo
12021
normal! zc
12021
normal! zc
12035
normal! zo
12072
normal! zo
12083
normal! zo
12088
normal! zo
12106
normal! zo
12106
normal! zo
12106
normal! zo
12106
normal! zo
12107
normal! zo
12112
normal! zo
12128
normal! zo
12128
normal! zo
12128
normal! zo
12128
normal! zo
12137
normal! zo
12137
normal! zo
12137
normal! zo
12137
normal! zo
12137
normal! zo
12161
normal! zo
12185
normal! zo
12185
normal! zc
12226
normal! zo
12226
normal! zo
12226
normal! zo
12226
normal! zo
12288
normal! zo
12304
normal! zo
12304
normal! zc
12328
normal! zo
12328
normal! zo
12328
normal! zo
12328
normal! zc
12353
normal! zo
12353
normal! zo
12353
normal! zo
12353
normal! zc
12428
normal! zo
12428
normal! zo
12428
normal! zo
12428
normal! zo
12428
normal! zo
12428
normal! zo
12428
normal! zo
12428
normal! zo
12428
normal! zc
12444
normal! zo
12444
normal! zc
12466
normal! zo
12466
normal! zc
12487
normal! zo
12487
normal! zo
12487
normal! zo
12487
normal! zo
12487
normal! zo
12487
normal! zo
12487
normal! zo
12487
normal! zc
12487
normal! zc
12607
normal! zo
12607
normal! zo
12607
normal! zo
12607
normal! zo
12607
normal! zo
12607
normal! zc
12875
normal! zo
12875
normal! zc
12905
normal! zo
12905
normal! zo
12905
normal! zo
12905
normal! zo
12905
normal! zo
12905
normal! zo
12905
normal! zo
12905
normal! zo
12920
normal! zo
12935
normal! zo
12937
normal! zo
12959
normal! zo
12967
normal! zo
12967
normal! zc
12983
normal! zo
12983
normal! zo
13022
normal! zo
13084
normal! zo
13085
normal! zo
13103
normal! zo
13145
normal! zo
13146
normal! zo
13174
normal! zo
13206
normal! zo
13207
normal! zo
13235
normal! zo
13271
normal! zo
13272
normal! zo
13290
normal! zo
13317
normal! zc
13327
normal! zo
13327
normal! zc
13347
normal! zo
13348
normal! zo
13349
normal! zo
13347
normal! zc
13403
normal! zo
13403
normal! zc
13461
normal! zo
13461
normal! zo
13461
normal! zo
13471
normal! zo
13476
normal! zo
13477
normal! zo
13478
normal! zo
13478
normal! zo
13478
normal! zo
13478
normal! zo
13478
normal! zo
13478
normal! zo
13478
normal! zo
13478
normal! zo
13478
normal! zo
13478
normal! zo
13484
normal! zo
13485
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13486
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13488
normal! zo
13490
normal! zo
13491
normal! zo
13491
normal! zo
13491
normal! zo
13491
normal! zo
13491
normal! zo
13491
normal! zo
13491
normal! zo
13491
normal! zo
13491
normal! zo
13494
normal! zo
13496
normal! zo
13496
normal! zo
13501
normal! zo
13501
normal! zo
13511
normal! zo
13512
normal! zo
13512
normal! zo
13512
normal! zo
13512
normal! zo
13512
normal! zo
13512
normal! zo
13519
normal! zo
13519
normal! zo
13519
normal! zo
13525
normal! zo
13526
normal! zo
13535
normal! zo
13536
normal! zo
13536
normal! zo
13536
normal! zo
13536
normal! zo
13540
normal! zo
13540
normal! zo
13540
normal! zo
13548
normal! zo
13549
normal! zo
13551
normal! zo
13559
normal! zo
13560
normal! zo
13560
normal! zo
13560
normal! zo
13560
normal! zo
13564
normal! zo
13564
normal! zo
13564
normal! zo
13571
normal! zo
13571
normal! zo
13571
normal! zo
13571
normal! zo
13571
normal! zo
13574
normal! zo
13575
normal! zo
13576
normal! zo
13577
normal! zo
13577
normal! zo
13578
normal! zo
13590
normal! zo
13591
normal! zo
13591
normal! zo
13591
normal! zo
13598
normal! zo
13599
normal! zo
13600
normal! zo
13600
normal! zo
13601
normal! zo
13612
normal! zo
13613
normal! zo
13614
normal! zo
13614
normal! zo
13615
normal! zo
13630
normal! zo
13631
normal! zo
13632
normal! zo
13633
normal! zo
13633
normal! zo
13634
normal! zo
13646
normal! zo
13647
normal! zo
13647
normal! zo
13647
normal! zo
13648
normal! zo
13654
normal! zo
13655
normal! zo
13656
normal! zo
13656
normal! zo
13657
normal! zo
13668
normal! zo
13669
normal! zo
13670
normal! zo
13670
normal! zo
13671
normal! zo
13686
normal! zo
13686
normal! zo
13686
normal! zo
13707
normal! zo
13712
normal! zo
13713
normal! zo
13714
normal! zo
13714
normal! zo
13714
normal! zo
13714
normal! zo
13714
normal! zo
13714
normal! zo
13714
normal! zo
13714
normal! zo
13714
normal! zo
13714
normal! zo
13720
normal! zo
13721
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
13722
normal! zo
13722
normal! zo
13724
normal! zo
13724
normal! zo
13724
normal! zo
13724
normal! zo
13724
normal! zo
13724
normal! zo
13724
normal! zo
13724
normal! zo
13726
normal! zo
13727
normal! zo
13727
normal! zo
13727
normal! zo
13727
normal! zo
13727
normal! zo
13727
normal! zo
13727
normal! zo
13727
normal! zo
13727
normal! zo
13730
normal! zo
13732
normal! zo
13737
normal! zo
13746
normal! zo
13747
normal! zo
13747
normal! zo
13747
normal! zo
13747
normal! zo
13747
normal! zo
13747
normal! zo
13747
normal! zo
13754
normal! zo
13756
normal! zo
13757
normal! zo
13758
normal! zo
13758
normal! zo
13759
normal! zo
13769
normal! zo
13770
normal! zo
13771
normal! zo
13771
normal! zo
13772
normal! zo
13786
normal! zo
13787
normal! zo
13788
normal! zo
13789
normal! zo
13789
normal! zo
13790
normal! zo
13800
normal! zo
13801
normal! zo
13802
normal! zo
13802
normal! zo
13803
normal! zo
13817
normal! zo
13817
normal! zo
13817
normal! zo
13828
normal! zo
13833
normal! zo
13834
normal! zo
13835
normal! zo
13835
normal! zo
13835
normal! zo
13835
normal! zo
13835
normal! zo
13835
normal! zo
13835
normal! zo
13835
normal! zo
13835
normal! zo
13835
normal! zo
13841
normal! zo
13842
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13843
normal! zo
13845
normal! zo
13845
normal! zo
13845
normal! zo
13845
normal! zo
13845
normal! zo
13845
normal! zo
13845
normal! zo
13845
normal! zo
13847
normal! zo
13848
normal! zo
13848
normal! zo
13848
normal! zo
13848
normal! zo
13848
normal! zo
13848
normal! zo
13848
normal! zo
13848
normal! zo
13848
normal! zo
13851
normal! zo
13853
normal! zo
13858
normal! zo
13867
normal! zo
13868
normal! zo
13868
normal! zo
13868
normal! zo
13868
normal! zo
13868
normal! zo
13868
normal! zo
13868
normal! zo
13875
normal! zo
13880
normal! zo
13881
normal! zo
13882
normal! zo
13889
normal! zo
13890
normal! zo
13891
normal! zo
13897
normal! zo
13898
normal! zo
13899
normal! zo
13904
normal! zo
13905
normal! zo
13906
normal! zo
13906
normal! zo
13916
normal! zo
13917
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13918
normal! zo
13925
normal! zo
13926
normal! zo
13926
normal! zo
13926
normal! zo
13926
normal! zo
13926
normal! zo
13926
normal! zo
13926
normal! zo
13933
normal! zo
13934
normal! zo
13934
normal! zo
13934
normal! zo
13934
normal! zo
13934
normal! zo
13934
normal! zo
13934
normal! zo
13940
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13941
normal! zo
13951
normal! zo
13957
normal! zo
13957
normal! zo
13963
normal! zo
13969
normal! zo
13975
normal! zo
13975
normal! zo
13975
normal! zo
13975
normal! zo
13975
normal! zo
13975
normal! zo
13975
normal! zo
13975
normal! zo
13975
normal! zo
13985
normal! zo
13985
normal! zo
13985
normal! zo
13985
normal! zo
13985
normal! zo
13985
normal! zo
13987
normal! zo
13988
normal! zo
13988
normal! zo
13988
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
13994
normal! zo
13994
normal! zo
14005
normal! zo
14005
normal! zo
14005
normal! zo
14005
normal! zo
14005
normal! zo
14005
normal! zo
14007
normal! zo
14008
normal! zo
14008
normal! zo
14008
normal! zo
14014
normal! zo
14014
normal! zo
14014
normal! zo
14014
normal! zo
14022
normal! zo
14027
normal! zo
14030
normal! zo
14035
normal! zo
14036
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14037
normal! zo
14043
normal! zo
14044
normal! zo
14047
normal! zo
14048
normal! zo
14048
normal! zo
14048
normal! zo
14048
normal! zo
14048
normal! zo
14048
normal! zo
14048
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14050
normal! zo
14052
normal! zo
14053
normal! zo
14056
normal! zo
14056
normal! zo
14056
normal! zo
14056
normal! zo
14056
normal! zo
14056
normal! zo
14056
normal! zo
14056
normal! zo
14056
normal! zo
14059
normal! zo
14060
normal! zo
14064
normal! zo
14064
normal! zo
14069
normal! zo
14069
normal! zo
14074
normal! zo
14075
normal! zo
14082
normal! zo
14083
normal! zo
14086
normal! zo
14086
normal! zo
14086
normal! zo
14086
normal! zo
14086
normal! zo
14086
normal! zo
14093
normal! zo
14094
normal! zo
14095
normal! zo
14096
normal! zo
14102
normal! zo
14103
normal! zo
14104
normal! zo
14110
normal! zo
14111
normal! zo
14111
normal! zo
14112
normal! zo
14117
normal! zo
14118
normal! zo
14118
normal! zo
14119
normal! zo
14128
normal! zo
14129
normal! zo
14130
normal! zo
14130
normal! zo
14130
normal! zo
14130
normal! zo
14130
normal! zo
14130
normal! zo
14137
normal! zo
14138
normal! zo
14139
normal! zo
14145
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14146
normal! zo
14152
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14153
normal! zo
14164
normal! zo
14165
normal! zo
14165
normal! zo
14171
normal! zo
14177
normal! zo
14177
normal! zo
14183
normal! zo
14183
normal! zo
14183
normal! zo
14183
normal! zo
14199
normal! zo
14204
normal! zo
14205
normal! zo
14206
normal! zo
14206
normal! zo
14206
normal! zo
14206
normal! zo
14206
normal! zo
14206
normal! zo
14206
normal! zo
14206
normal! zo
14206
normal! zo
14206
normal! zo
14212
normal! zo
14213
normal! zo
14214
normal! zo
14214
normal! zo
14214
normal! zo
14214
normal! zo
14214
normal! zo
14214
normal! zo
14214
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14216
normal! zo
14218
normal! zo
14219
normal! zo
14219
normal! zo
14219
normal! zo
14219
normal! zo
14219
normal! zo
14219
normal! zo
14219
normal! zo
14219
normal! zo
14219
normal! zo
14222
normal! zo
14224
normal! zo
14224
normal! zo
14229
normal! zo
14229
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
14250
normal! zo
14255
normal! zo
14256
normal! zo
14257
normal! zo
14267
normal! zo
14268
normal! zo
14269
normal! zo
14269
normal! zo
14269
normal! zo
14269
normal! zo
14269
normal! zo
14269
normal! zo
14274
normal! zo
14275
normal! zo
14275
normal! zo
14275
normal! zo
14276
normal! zo
14286
normal! zo
14287
normal! zo
14287
normal! zo
14293
normal! zo
14294
normal! zo
14294
normal! zo
14300
normal! zo
14300
normal! zo
14300
normal! zo
14300
normal! zo
14312
normal! zo
14317
normal! zo
14318
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14319
normal! zo
14325
normal! zo
14326
normal! zo
14327
normal! zo
14327
normal! zo
14327
normal! zo
14327
normal! zo
14327
normal! zo
14327
normal! zo
14327
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
14331
normal! zo
14332
normal! zo
14332
normal! zo
14332
normal! zo
14332
normal! zo
14332
normal! zo
14332
normal! zo
14332
normal! zo
14332
normal! zo
14332
normal! zo
14335
normal! zo
14337
normal! zo
14337
normal! zo
14342
normal! zo
14342
normal! zo
14352
normal! zo
14353
normal! zo
14353
normal! zo
14353
normal! zo
14353
normal! zo
14353
normal! zo
14353
normal! zo
14360
normal! zo
14367
normal! zo
14368
normal! zo
14370
normal! zo
14370
normal! zo
14370
normal! zo
14376
normal! zo
14378
normal! zo
14380
normal! zo
14386
normal! zo
14388
normal! zo
14390
normal! zo
14401
normal! zo
14421
normal! zo
14433
normal! zo
14436
normal! zo
14437
normal! zo
14438
normal! zo
14438
normal! zo
14438
normal! zo
14440
normal! zo
14441
normal! zo
14441
normal! zo
14441
normal! zo
14457
normal! zo
14468
normal! zo
14477
normal! zo
14487
normal! zo
14514
normal! zo
14519
normal! zo
14525
normal! zo
14536
normal! zo
14549
normal! zo
14573
normal! zo
14575
normal! zo
14578
normal! zo
14581
normal! zo
14582
normal! zo
14586
normal! zo
14587
normal! zo
14601
normal! zo
14601
normal! zo
14601
normal! zo
14601
normal! zo
14623
normal! zo
14624
normal! zo
14625
normal! zo
14625
normal! zo
14625
normal! zo
14625
normal! zo
14625
normal! zo
14625
normal! zo
14625
normal! zo
14625
normal! zo
14625
normal! zo
14625
normal! zo
14634
normal! zo
14635
normal! zo
14641
normal! zo
14645
normal! zo
14646
normal! zo
14655
normal! zo
14656
normal! zo
14664
normal! zo
14665
normal! zo
14671
normal! zo
14686
normal! zo
14694
normal! zo
14700
normal! zo
14706
normal! zo
14711
normal! zo
14715
normal! zo
14721
normal! zo
14726
normal! zo
14727
normal! zo
14732
normal! zo
14743
normal! zo
14761
normal! zo
14803
normal! zo
14809
normal! zo
14815
normal! zo
14822
normal! zo
14831
normal! zo
14833
normal! zo
14840
normal! zo
14840
normal! zo
14840
normal! zo
14840
normal! zo
14840
normal! zo
14840
normal! zo
14857
normal! zo
14869
normal! zo
14880
normal! zo
14881
normal! zo
14897
normal! zo
14914
normal! zo
14918
normal! zo
14919
normal! zo
14920
normal! zo
14920
normal! zo
14922
normal! zo
14925
normal! zo
14938
normal! zo
14948
normal! zo
14950
normal! zo
14954
normal! zo
14955
normal! zo
14955
normal! zo
14955
normal! zo
14955
normal! zo
14955
normal! zo
14955
normal! zo
14968
normal! zo
14989
normal! zo
14990
normal! zo
14997
normal! zo
15030
normal! zo
15031
normal! zo
15031
normal! zo
15047
normal! zo
15053
normal! zo
15056
normal! zo
15056
normal! zo
15056
normal! zo
15062
normal! zo
15062
normal! zo
15082
normal! zo
15087
normal! zo
15092
normal! zo
15100
normal! zo
15119
normal! zo
15153
normal! zo
15161
normal! zo
15170
normal! zo
15189
normal! zo
15191
normal! zo
15195
normal! zo
15212
normal! zo
15218
normal! zo
15222
normal! zo
15261
normal! zo
15365
normal! zo
15365
normal! zo
15441
normal! zo
15441
normal! zo
15441
normal! zo
15554
normal! zo
15585
normal! zo
15609
normal! zo
15619
normal! zo
15619
normal! zo
15619
normal! zo
15619
normal! zo
15619
normal! zo
15807
normal! zo
15826
normal! zo
15848
normal! zo
15853
normal! zo
15854
normal! zo
15854
normal! zo
15857
normal! zo
15858
normal! zo
15858
normal! zo
15858
normal! zo
15861
normal! zo
15861
normal! zo
15861
normal! zo
15865
normal! zo
15865
normal! zo
15865
normal! zo
15865
normal! zo
15865
normal! zo
15865
normal! zo
15865
normal! zo
15865
normal! zo
15865
normal! zo
16396
normal! zo
16432
normal! zo
16447
normal! zo
16453
normal! zo
16456
normal! zo
16464
normal! zo
16465
normal! zo
16465
normal! zo
16465
normal! zo
16465
normal! zo
16465
normal! zo
16469
normal! zo
16477
normal! zo
16480
normal! zo
16486
normal! zo
16492
normal! zo
16495
normal! zo
16501
normal! zo
16515
normal! zo
16521
normal! zo
16526
normal! zo
16529
normal! zo
16529
normal! zo
16529
normal! zo
16539
normal! zo
16554
normal! zo
16565
normal! zo
16565
normal! zo
16576
normal! zo
16591
normal! zo
16601
normal! zo
16612
normal! zo
16621
normal! zo
16628
normal! zo
16666
normal! zo
16671
normal! zo
16671
normal! zo
16671
normal! zo
16684
normal! zo
16684
normal! zo
16684
normal! zo
16684
normal! zo
16684
normal! zo
16684
normal! zo
16684
normal! zo
16684
normal! zo
16684
normal! zo
16684
normal! zo
16684
normal! zo
16696
normal! zo
16717
normal! zo
16736
normal! zo
16744
normal! zo
16745
normal! zo
16746
normal! zo
16750
normal! zo
16754
normal! zo
16770
normal! zo
16785
normal! zo
16790
normal! zo
16795
normal! zo
16805
normal! zo
16806
normal! zo
16806
normal! zo
16806
normal! zo
16808
normal! zo
16808
normal! zo
16808
normal! zo
16808
normal! zo
16808
normal! zo
16808
normal! zo
16808
normal! zo
16808
normal! zo
16808
normal! zo
16808
normal! zo
16813
normal! zo
16814
normal! zo
16820
normal! zo
16821
normal! zo
16841
normal! zo
16866
normal! zo
16870
normal! zo
16887
normal! zo
16898
normal! zo
16898
normal! zo
16898
normal! zo
16898
normal! zo
16900
normal! zo
16901
normal! zo
16902
normal! zo
16903
normal! zo
16904
normal! zo
16908
normal! zo
16909
normal! zo
16910
normal! zo
16910
normal! zo
16910
normal! zo
16910
normal! zo
16910
normal! zo
16910
normal! zo
16910
normal! zo
16912
normal! zo
16914
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16919
normal! zo
16925
normal! zo
16929
normal! zo
16937
normal! zo
16937
normal! zo
16937
normal! zo
16937
normal! zo
16945
normal! zo
16953
normal! zo
16954
normal! zo
16957
normal! zo
16962
normal! zo
16970
normal! zo
16975
normal! zo
16983
normal! zo
16988
normal! zo
16997
normal! zo
16998
normal! zo
16998
normal! zo
17008
normal! zo
17023
normal! zo
17024
normal! zo
17040
normal! zo
17060
normal! zo
17061
normal! zo
17061
normal! zo
17061
normal! zo
17061
normal! zo
17061
normal! zo
17067
normal! zo
17077
normal! zo
17091
normal! zo
17094
normal! zo
17098
normal! zo
17099
normal! zo
17100
normal! zo
17100
normal! zo
17100
normal! zo
17100
normal! zo
17100
normal! zo
17118
normal! zo
17125
normal! zo
17126
normal! zo
17133
normal! zo
17140
normal! zo
17141
normal! zo
17142
normal! zo
17147
normal! zo
17154
normal! zo
17159
normal! zo
17172
normal! zo
17173
normal! zo
17173
normal! zo
17173
normal! zo
17178
normal! zo
17191
normal! zo
17198
normal! zo
17199
normal! zo
17214
normal! zo
17221
normal! zo
17235
normal! zo
17242
normal! zo
17243
normal! zo
17248
normal! zo
17257
normal! zo
17271
normal! zo
17293
normal! zo
17314
normal! zo
17327
normal! zo
17327
normal! zo
17327
normal! zo
17327
normal! zo
17327
normal! zo
17327
normal! zo
17337
normal! zo
17350
normal! zo
17374
normal! zo
17379
normal! zo
17381
normal! zo
17384
normal! zo
17391
normal! zo
17403
normal! zo
17413
normal! zo
17413
normal! zo
17413
normal! zo
17413
normal! zo
17413
normal! zo
17413
normal! zo
17421
normal! zo
17431
normal! zo
17431
normal! zo
17431
normal! zo
17431
normal! zo
17431
normal! zo
17431
normal! zo
17439
normal! zo
17440
normal! zo
17451
normal! zo
17456
normal! zo
17467
normal! zo
17475
normal! zo
17488
normal! zo
17492
normal! zo
17492
normal! zo
17492
normal! zo
17492
normal! zo
17492
normal! zo
17494
normal! zo
17506
normal! zo
17506
normal! zo
17506
normal! zo
17506
normal! zo
17506
normal! zo
17506
normal! zo
17506
normal! zo
17510
normal! zo
17510
normal! zo
17510
normal! zo
17510
normal! zo
17510
normal! zo
17510
normal! zo
17516
normal! zo
17516
normal! zo
17516
normal! zo
17516
normal! zo
17519
normal! zo
17520
normal! zo
17521
normal! zo
17527
normal! zo
17528
normal! zo
17528
normal! zo
17528
normal! zo
17650
normal! zo
17705
normal! zo
17738
normal! zo
17795
normal! zo
17810
normal! zo
17817
normal! zo
17818
normal! zo
17834
normal! zo
17844
normal! zo
17858
normal! zo
17861
normal! zo
17862
normal! zo
17862
normal! zo
17884
normal! zo
17904
normal! zo
17916
normal! zo
17916
normal! zo
17916
normal! zo
17916
normal! zo
17916
normal! zo
17919
normal! zo
17926
normal! zo
17929
normal! zo
17940
normal! zo
17946
normal! zo
17951
normal! zo
17957
normal! zo
17958
normal! zo
17959
normal! zo
17962
normal! zo
17981
normal! zo
17996
normal! zo
18024
normal! zo
18049
normal! zo
18070
normal! zo
18105
normal! zo
18114
normal! zo
18115
normal! zo
18116
normal! zo
18118
normal! zo
18118
normal! zo
18118
normal! zo
18121
normal! zo
18123
normal! zo
18123
normal! zo
18123
normal! zo
18126
normal! zo
18127
normal! zo
18127
normal! zo
18127
normal! zo
18127
normal! zo
18127
normal! zo
18653
normal! zo
18670
normal! zo
18680
normal! zo
18683
normal! zo
18684
normal! zo
18684
normal! zo
18690
normal! zo
18697
normal! zo
18698
normal! zo
18699
normal! zo
18699
normal! zo
18699
normal! zo
18699
normal! zo
18703
normal! zo
18704
normal! zo
18704
normal! zo
18704
normal! zo
18704
normal! zo
18720
normal! zo
19021
normal! zo
19938
normal! zo
19962
normal! zo
19968
normal! zo
19974
normal! zo
19992
normal! zo
20002
normal! zo
20005
normal! zo
20012
normal! zo
20012
normal! zo
20012
normal! zo
20012
normal! zo
20017
normal! zo
20297
normal! zo
20303
normal! zo
20303
normal! zo
20312
normal! zo
20319
normal! zo
20326
normal! zo
20333
normal! zo
20340
normal! zo
20347
normal! zo
20354
normal! zo
20360
normal! zo
20361
normal! zo
20370
normal! zo
20379
normal! zo
20542
normal! zo
20552
normal! zo
20563
normal! zo
20574
normal! zo
20575
normal! zo
20580
normal! zo
20581
normal! zo
20581
normal! zo
20591
normal! zo
20591
normal! zo
20591
normal! zo
20591
normal! zo
20591
normal! zo
20591
normal! zo
20591
normal! zo
20591
normal! zo
20591
normal! zo
20602
normal! zo
20603
normal! zo
20611
normal! zo
20611
normal! zo
20611
normal! zo
20611
normal! zo
20611
normal! zo
20611
normal! zo
20611
normal! zo
20611
normal! zo
20622
normal! zo
20623
normal! zo
20631
normal! zo
20646
normal! zo
20679
normal! zo
20700
normal! zo
20705
normal! zo
20717
normal! zo
20717
normal! zo
20717
normal! zo
20717
normal! zo
20717
normal! zo
20717
normal! zo
20717
normal! zo
20735
normal! zo
20742
normal! zo
21232
normal! zo
let s:l = 16611 - ((2 * winheight(0) + 9) / 18)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16611
normal! 09|
lcd ~/Geotexan/src/Geotex-INN
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
58
normal! zo
59
normal! zo
110
normal! zo
335
normal! zo
364
normal! zo
369
normal! zo
373
normal! zo
395
normal! zo
405
normal! zo
414
normal! zo
424
normal! zo
432
normal! zo
433
normal! zo
457
normal! zo
458
normal! zo
458
normal! zo
458
normal! zo
458
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
467
normal! zo
472
normal! zo
472
normal! zo
472
normal! zo
472
normal! zo
475
normal! zo
475
normal! zo
475
normal! zo
475
normal! zo
480
normal! zo
481
normal! zo
504
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
516
normal! zo
521
normal! zo
521
normal! zo
521
normal! zo
521
normal! zo
525
normal! zo
525
normal! zo
525
normal! zo
525
normal! zo
531
normal! zo
532
normal! zo
556
normal! zo
557
normal! zo
557
normal! zo
557
normal! zo
557
normal! zo
561
normal! zo
561
normal! zo
561
normal! zo
561
normal! zo
568
normal! zo
573
normal! zo
573
normal! zo
573
normal! zo
573
normal! zo
578
normal! zo
578
normal! zo
578
normal! zo
578
normal! zo
633
normal! zo
639
normal! zo
640
normal! zo
641
normal! zo
642
normal! zo
688
normal! zo
694
normal! zo
694
normal! zo
694
normal! zo
694
normal! zo
694
normal! zo
794
normal! zo
794
normal! zo
794
normal! zo
794
normal! zo
794
normal! zo
805
normal! zo
809
normal! zo
813
normal! zo
846
normal! zo
846
normal! zo
846
normal! zo
846
normal! zo
846
normal! zo
854
normal! zo
859
normal! zo
let s:l = 268 - ((0 * winheight(0) + 6) / 13)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
268
normal! 065|
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
56
normal! zo
56
normal! zo
63
normal! zo
139
normal! zo
161
normal! zo
176
normal! zo
177
normal! zo
177
normal! zo
177
normal! zo
177
normal! zo
177
normal! zo
187
normal! zo
191
normal! zo
197
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
211
normal! zo
223
normal! zo
224
normal! zo
224
normal! zo
224
normal! zo
224
normal! zo
224
normal! zo
234
normal! zo
240
normal! zo
241
normal! zo
241
normal! zo
241
normal! zo
241
normal! zo
263
normal! zo
278
normal! zo
307
normal! zo
312
normal! zo
345
normal! zo
351
normal! zo
351
normal! zo
351
normal! zo
351
normal! zo
351
normal! zo
353
normal! zo
353
normal! zo
353
normal! zo
353
normal! zo
353
normal! zo
354
normal! zo
387
normal! zo
404
normal! zo
410
normal! zo
415
normal! zo
428
normal! zo
434
normal! zo
let s:l = 192 - ((4 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
192
normal! 021|
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
let s:l = 43 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
43
normal! 029|
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
367
normal! zo
let s:l = 173 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
173
normal! 032|
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
normal! 023|
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
let s:l = 1137 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1137
normal! 043|
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
58
normal! zo
59
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
84
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
95
normal! zo
106
normal! zo
110
normal! zo
115
normal! zo
132
normal! zo
145
normal! zo
170
normal! zo
205
normal! zo
218
normal! zo
227
normal! zo
248
normal! zo
261
normal! zo
269
normal! zo
269
normal! zo
269
normal! zo
269
normal! zo
276
normal! zo
276
normal! zo
276
normal! zo
276
normal! zo
280
normal! zo
281
normal! zo
281
normal! zo
304
normal! zo
305
normal! zo
305
normal! zo
329
normal! zo
330
normal! zo
335
normal! zo
344
normal! zo
345
normal! zo
345
normal! zo
345
normal! zo
347
normal! zo
348
normal! zo
348
normal! zo
348
normal! zo
348
normal! zo
348
normal! zo
348
normal! zo
364
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
367
normal! zo
369
normal! zo
373
normal! zo
381
normal! zo
382
normal! zo
382
normal! zo
383
normal! zo
387
normal! zo
389
normal! zo
391
normal! zo
395
normal! zo
400
normal! zo
401
normal! zo
401
normal! zo
401
normal! zo
401
normal! zo
405
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
411
normal! zo
414
normal! zo
419
normal! zo
420
normal! zo
420
normal! zo
420
normal! zo
420
normal! zo
424
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
429
normal! zo
432
normal! zo
433
normal! zo
450
normal! zo
450
normal! zo
450
normal! zo
450
normal! zo
452
normal! zo
452
normal! zo
452
normal! zo
452
normal! zo
457
normal! zo
458
normal! zo
458
normal! zo
458
normal! zo
458
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
461
normal! zo
467
normal! zo
472
normal! zo
472
normal! zo
472
normal! zo
472
normal! zo
475
normal! zo
475
normal! zo
475
normal! zo
475
normal! zo
480
normal! zo
481
normal! zo
484
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
497
normal! zo
499
normal! zo
499
normal! zo
499
normal! zo
499
normal! zo
504
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
505
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
509
normal! zo
516
normal! zo
521
normal! zo
521
normal! zo
521
normal! zo
521
normal! zo
525
normal! zo
525
normal! zo
525
normal! zo
525
normal! zo
531
normal! zo
532
normal! zo
535
normal! zo
549
normal! zo
549
normal! zo
549
normal! zo
549
normal! zo
551
normal! zo
551
normal! zo
551
normal! zo
551
normal! zo
556
normal! zo
557
normal! zo
557
normal! zo
557
normal! zo
557
normal! zo
561
normal! zo
561
normal! zo
561
normal! zo
561
normal! zo
568
normal! zo
573
normal! zo
573
normal! zo
573
normal! zo
573
normal! zo
578
normal! zo
578
normal! zo
578
normal! zo
578
normal! zo
584
normal! zo
585
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
587
normal! zo
607
normal! zo
627
normal! zo
633
normal! zo
639
normal! zo
640
normal! zo
649
normal! zo
654
normal! zo
659
normal! zo
659
normal! zo
663
normal! zo
665
normal! zo
665
normal! zo
665
normal! zo
675
normal! zo
676
normal! zo
677
normal! zo
683
normal! zo
684
normal! zo
688
normal! zo
694
normal! zo
694
normal! zo
694
normal! zo
694
normal! zo
694
normal! zo
706
normal! zo
709
normal! zo
709
normal! zo
709
normal! zo
709
normal! zo
715
normal! zo
726
normal! zo
740
normal! zo
741
normal! zo
751
normal! zo
753
normal! zo
759
normal! zo
763
normal! zo
763
normal! zo
775
normal! zo
779
normal! zo
779
normal! zo
794
normal! zo
794
normal! zo
794
normal! zo
794
normal! zo
794
normal! zo
813
normal! zo
814
normal! zo
814
normal! zo
832
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
833
normal! zo
846
normal! zo
846
normal! zo
846
normal! zo
846
normal! zo
846
normal! zo
866
normal! zo
let s:l = 1 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
6wincmd w
exe '1resize ' . ((&lines * 6 + 31) / 63)
exe 'vert 1resize ' . ((&columns * 26 + 53) / 107)
exe '2resize ' . ((&lines * 54 + 31) / 63)
exe 'vert 2resize ' . ((&columns * 26 + 53) / 107)
exe '3resize ' . ((&lines * 7 + 31) / 63)
exe 'vert 3resize ' . ((&columns * 80 + 53) / 107)
exe '4resize ' . ((&lines * 18 + 31) / 63)
exe 'vert 4resize ' . ((&columns * 80 + 53) / 107)
exe '5resize ' . ((&lines * 13 + 31) / 63)
exe 'vert 5resize ' . ((&columns * 80 + 53) / 107)
exe '6resize ' . ((&lines * 10 + 31) / 63)
exe 'vert 6resize ' . ((&columns * 80 + 53) / 107)
exe '7resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 7resize ' . ((&columns * 80 + 53) / 107)
exe '8resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 8resize ' . ((&columns * 80 + 53) / 107)
exe '9resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 9resize ' . ((&columns * 80 + 53) / 107)
exe '10resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 10resize ' . ((&columns * 80 + 53) / 107)
exe '11resize ' . ((&lines * 1 + 31) / 63)
exe 'vert 11resize ' . ((&columns * 80 + 53) / 107)
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
