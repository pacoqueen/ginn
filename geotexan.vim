" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 06 marzo 2015 at 13:43:25.
" Open this file in Vim and run :source % to restore your session.

set guioptions=aegimrLtT
silent! set guifont=Monaco\ for\ Powerline\ 10
if exists('g:syntax_on') != 1 | syntax on | endif
if exists('g:did_load_filetypes') != 1 | filetype on | endif
if exists('g:did_load_ftplugin') != 1 | filetype plugin on | endif
if exists('g:did_indent_on') != 1 | filetype indent on | endif
if &background != 'dark'
	set background=dark
endif
if !exists('g:colors_name') || g:colors_name != 'vividchalk' | colorscheme vividchalk | endif
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
badd +1 ginn/formularios/partes_de_ancho_multiple.py
badd +10963 ginn/framework/pclases/__init__.py
badd +1406 ginn/formularios/partes_de_fabricacion_balas.py
badd +1 ginn/formularios/facturas_compra.py
badd +1 fugitive:///home/bogado/Geotexan/src/Geotex-INN/.git//0/ginn/formularios/utils.py
badd +9 ginn/lib/fuzzywuzzy/fuzzywuzzy/utils.py
badd +1 formularios/auditviewer.py
badd +1260 ginn/formularios/utils.py
badd +2299 ginn/formularios/presupuestos.py
badd +38 ginn/informes/treeview2pdf.py
badd +138 ginn/formularios/listado_rollos.py
badd +2 ginn/lib/fuzzywuzzy/fuzzywuzzy/__init__.py
badd +1 ginn/formularios/consulta_ventas.py
badd +136 ginn/formularios/consulta_saldo_proveedores.py
args formularios/auditviewer.py
set lines=43 columns=103
edit ginn/formularios/partes_de_ancho_multiple.py
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
exe 'vert 1resize ' . ((&columns * 20 + 51) / 103)
exe '2resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 2resize ' . ((&columns * 82 + 51) / 103)
exe '3resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 3resize ' . ((&columns * 82 + 51) / 103)
exe '4resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 4resize ' . ((&columns * 82 + 51) / 103)
exe '5resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 5resize ' . ((&columns * 82 + 51) / 103)
exe '6resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 6resize ' . ((&columns * 82 + 51) / 103)
exe '7resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 7resize ' . ((&columns * 82 + 51) / 103)
exe '8resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 8resize ' . ((&columns * 82 + 51) / 103)
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
lcd ~/Geotexan/src/Geotex-INN
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
let s:l = 22 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 011|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/utils.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
91
normal! zo
904
normal! zo
922
normal! zo
1196
normal! zo
1214
normal! zo
1227
normal! zo
1238
normal! zo
1248
normal! zo
1257
normal! zo
1271
normal! zo
1303
normal! zo
2379
normal! zo
let s:l = 1245 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1245
normal! 064|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_balas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1407 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1407
normal! 037|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/consulta_ventas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
55
normal! zo
60
normal! zo
147
normal! zo
147
normal! zo
147
normal! zo
155
normal! zo
155
normal! zo
155
normal! zo
159
normal! zo
159
normal! zo
159
normal! zo
350
normal! zo
367
normal! zo
386
normal! zo
387
normal! zo
398
normal! zo
452
normal! zo
591
normal! zo
618
normal! zo
619
normal! zo
619
normal! zo
619
normal! zo
619
normal! zo
619
normal! zo
720
normal! zo
858
normal! zo
998
normal! zo
1124
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1133
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1135
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1137
normal! zo
1263
normal! zo
1272
normal! zo
1273
normal! zo
1274
normal! zo
1279
normal! zo
1282
normal! zo
1282
normal! zo
1282
normal! zo
1284
normal! zo
1285
normal! zo
1290
normal! zo
1293
normal! zo
1294
normal! zo
1295
normal! zo
1300
normal! zo
1358
normal! zo
1358
normal! zo
1358
normal! zo
1358
normal! zo
1358
normal! zo
1358
normal! zo
1368
normal! zo
1369
normal! zo
1370
normal! zo
1375
normal! zo
1378
normal! zo
1379
normal! zo
1380
normal! zo
1385
normal! zo
1388
normal! zo
1389
normal! zo
1390
normal! zo
1395
normal! zo
1398
normal! zo
1399
normal! zo
1400
normal! zo
1405
normal! zo
1449
normal! zo
1449
normal! zo
1449
normal! zo
1449
normal! zo
1449
normal! zo
1449
normal! zo
1459
normal! zo
1460
normal! zo
1461
normal! zo
1466
normal! zo
1469
normal! zo
1470
normal! zo
1471
normal! zo
1476
normal! zo
1479
normal! zo
1480
normal! zo
1481
normal! zo
1486
normal! zo
1489
normal! zo
1490
normal! zo
1491
normal! zo
1496
normal! zo
1539
normal! zo
1539
normal! zo
1539
normal! zo
1539
normal! zo
1539
normal! zo
1539
normal! zo
1539
normal! zo
1551
normal! zo
1552
normal! zo
1553
normal! zo
1562
normal! zo
1563
normal! zo
1564
normal! zo
1575
normal! zo
1576
normal! zo
1576
normal! zo
1581
normal! zo
let s:l = 175 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
175
normal! 046|
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
693
normal! zo
970
normal! zo
1698
normal! zo
2150
normal! zo
2197
normal! zo
2197
normal! zo
2197
normal! zo
2197
normal! zo
2200
normal! zo
2224
normal! zo
2249
normal! zo
2250
normal! zo
2467
normal! zo
4937
normal! zo
7769
normal! zo
7775
normal! zo
10113
normal! zo
10153
normal! zo
10176
normal! zo
10179
normal! zo
10182
normal! zo
10184
normal! zo
10184
normal! zo
10184
normal! zo
10206
normal! zo
10222
normal! zo
10225
normal! zo
10606
normal! zo
10882
normal! zo
10888
normal! zo
10898
normal! zo
10913
normal! zo
10919
normal! zo
10929
normal! zo
10932
normal! zo
10951
normal! zo
10951
normal! zo
10951
normal! zo
11008
normal! zo
11013
normal! zo
11019
normal! zo
11048
normal! zo
11051
normal! zo
11068
normal! zo
16844
normal! zo
16860
normal! zo
16869
normal! zo
16886
normal! zo
16887
normal! zo
16894
normal! zo
16894
normal! zo
16901
normal! zo
16917
normal! zo
16918
normal! zo
16920
normal! zo
16920
normal! zo
16922
normal! zo
16940
normal! zo
16940
normal! zo
16940
normal! zo
16941
normal! zo
16946
normal! zo
17916
normal! zo
17925
normal! zo
17926
normal! zo
17926
normal! zo
17935
normal! zo
19186
normal! zo
19258
normal! zo
19264
normal! zo
19267
normal! zo
19268
normal! zo
19268
normal! zo
19268
normal! zo
19268
normal! zo
19278
normal! zo
19284
normal! zo
19287
normal! zo
19288
normal! zo
19288
normal! zo
19288
normal! zo
19288
normal! zo
19710
normal! zo
19799
normal! zo
let s:l = 16924 - ((3 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16924
normal! 051|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/partes_de_fabricacion_balas.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
111
normal! zo
112
normal! zo
126
normal! zo
126
normal! zo
312
normal! zo
388
normal! zo
388
normal! zo
413
normal! zo
467
normal! zo
468
normal! zo
468
normal! zo
468
normal! zo
503
normal! zo
508
normal! zo
510
normal! zo
522
normal! zo
530
normal! zo
532
normal! zo
533
normal! zo
536
normal! zo
549
normal! zo
549
normal! zo
549
normal! zo
565
normal! zo
570
normal! zo
577
normal! zo
578
normal! zo
578
normal! zo
582
normal! zo
589
normal! zo
589
normal! zo
595
normal! zo
607
normal! zo
608
normal! zo
608
normal! zo
608
normal! zo
611
normal! zo
619
normal! zo
620
normal! zo
620
normal! zo
620
normal! zo
626
normal! zo
645
normal! zo
658
normal! zo
665
normal! zo
666
normal! zo
674
normal! zo
675
normal! zo
675
normal! zo
675
normal! zo
675
normal! zo
689
normal! zo
689
normal! zo
689
normal! zo
689
normal! zo
689
normal! zo
695
normal! zo
695
normal! zo
695
normal! zo
695
normal! zo
695
normal! zo
695
normal! zo
707
normal! zo
707
normal! zo
707
normal! zo
707
normal! zo
711
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
720
normal! zo
728
normal! zo
733
normal! zo
745
normal! zo
751
normal! zo
751
normal! zo
751
normal! zo
754
normal! zo
754
normal! zo
754
normal! zo
764
normal! zo
768
normal! zo
768
normal! zo
777
normal! zo
778
normal! zo
787
normal! zo
787
normal! zo
787
normal! zo
787
normal! zo
787
normal! zo
798
normal! zo
809
normal! zo
812
normal! zo
813
normal! zo
813
normal! zo
822
normal! zo
823
normal! zo
823
normal! zo
823
normal! zo
823
normal! zo
824
normal! zo
841
normal! zo
864
normal! zo
884
normal! zo
904
normal! zo
925
normal! zo
930
normal! zo
939
normal! zo
950
normal! zo
959
normal! zo
960
normal! zo
960
normal! zo
960
normal! zo
965
normal! zo
965
normal! zo
968
normal! zo
968
normal! zo
980
normal! zo
982
normal! zo
985
normal! zo
998
normal! zo
1019
normal! zo
1019
normal! zo
1025
normal! zo
1042
normal! zo
1043
normal! zo
1064
normal! zo
1066
normal! zo
1070
normal! zo
1074
normal! zo
1090
normal! zo
1098
normal! zo
1099
normal! zo
1111
normal! zo
1117
normal! zo
1123
normal! zo
1129
normal! zo
1135
normal! zo
1141
normal! zo
1142
normal! zo
1146
normal! zo
1147
normal! zo
1147
normal! zo
1147
normal! zo
1153
normal! zo
1154
normal! zo
1163
normal! zo
1172
normal! zo
1175
normal! zo
1181
normal! zo
1187
normal! zo
1188
normal! zo
1188
normal! zo
1193
normal! zo
1201
normal! zo
1207
normal! zo
1236
normal! zo
1237
normal! zo
1239
normal! zo
1243
normal! zo
1244
normal! zo
1249
normal! zo
1258
normal! zo
1259
normal! zo
1263
normal! zo
1264
normal! zo
1275
normal! zo
1278
normal! zo
1295
normal! zo
1301
normal! zo
1313
normal! zo
1314
normal! zo
1314
normal! zo
1314
normal! zo
1314
normal! zo
1328
normal! zo
1359
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1362
normal! zo
1368
normal! zo
1373
normal! zo
1382
normal! zo
1389
normal! zo
1389
normal! zo
1395
normal! zo
1400
normal! zo
1407
normal! zo
1408
normal! zo
1408
normal! zo
1408
normal! zo
1412
normal! zo
1414
normal! zo
1415
normal! zo
1420
normal! zo
1421
normal! zo
1421
normal! zo
1421
normal! zo
1421
normal! zo
1421
normal! zo
1421
normal! zo
1424
normal! zo
1432
normal! zo
1441
normal! zo
1454
normal! zo
1455
normal! zo
1460
normal! zo
1464
normal! zo
1472
normal! zo
1479
normal! zo
1489
normal! zo
1491
normal! zo
1498
normal! zo
1500
normal! zo
1523
normal! zo
1541
normal! zo
1543
normal! zo
1550
normal! zo
1552
normal! zo
1553
normal! zo
1553
normal! zo
1553
normal! zo
1561
normal! zo
1562
normal! zo
1562
normal! zo
1562
normal! zo
1566
normal! zo
1575
normal! zo
1576
normal! zo
1576
normal! zo
1576
normal! zo
1580
normal! zo
1590
normal! zo
1610
normal! zo
1614
normal! zo
1622
normal! zo
1623
normal! zo
1623
normal! zo
1623
normal! zo
1633
normal! zo
1652
normal! zo
1659
normal! zo
1660
normal! zo
1660
normal! zo
1660
normal! zo
1660
normal! zo
1660
normal! zo
1660
normal! zo
1660
normal! zo
1660
normal! zo
1660
normal! zo
1660
normal! zo
1660
normal! zo
1669
normal! zo
1677
normal! zo
1678
normal! zo
1678
normal! zo
1678
normal! zo
1694
normal! zo
1701
normal! zo
1702
normal! zo
1712
normal! zo
1720
normal! zo
1721
normal! zo
1721
normal! zo
1721
normal! zo
1733
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1751
normal! zo
1751
normal! zo
1751
normal! zo
1751
normal! zo
1751
normal! zo
1751
normal! zo
1751
normal! zo
1751
normal! zo
1751
normal! zo
1751
normal! zo
1767
normal! zo
1778
normal! zo
1779
normal! zo
1780
normal! zo
1782
normal! zo
1783
normal! zo
1783
normal! zo
1783
normal! zo
1783
normal! zo
1795
normal! zo
1806
normal! zo
1807
normal! zo
1807
normal! zo
1807
normal! zo
1812
normal! zo
1813
normal! zo
1827
normal! zo
1827
normal! zo
1828
normal! zo
1836
normal! zo
1837
normal! zo
1848
normal! zo
1854
normal! zo
1869
normal! zo
1881
normal! zo
1889
normal! zo
1889
normal! zo
1889
normal! zo
1889
normal! zo
1900
normal! zo
1911
normal! zo
1934
normal! zo
1956
normal! zo
1956
normal! zo
1956
normal! zo
1956
normal! zo
1968
normal! zo
1973
normal! zo
1989
normal! zo
2007
normal! zo
2027
normal! zo
2035
normal! zo
2038
normal! zo
2043
normal! zo
2052
normal! zo
2052
normal! zo
2061
normal! zo
2061
normal! zo
2062
normal! zo
2062
normal! zo
2062
normal! zo
2069
normal! zo
2070
normal! zo
2070
normal! zo
2070
normal! zo
2076
normal! zo
2084
normal! zo
2091
normal! zo
2091
normal! zo
2091
normal! zo
2091
normal! zo
2091
normal! zo
2091
normal! zo
2091
normal! zo
2091
normal! zo
2100
normal! zo
2111
normal! zo
2122
normal! zo
2123
normal! zo
2126
normal! zo
2127
normal! zo
2127
normal! zo
2127
normal! zo
2131
normal! zo
2131
normal! zo
2131
normal! zo
2131
normal! zo
2137
normal! zo
2138
normal! zo
2138
normal! zo
2138
normal! zo
2142
normal! zo
2150
normal! zo
2160
normal! zo
2165
normal! zo
2166
normal! zo
2166
normal! zo
2166
normal! zo
2171
normal! zo
2189
normal! zo
2190
normal! zo
2191
normal! zo
2192
normal! zo
2192
normal! zo
2192
normal! zo
2196
normal! zo
2197
normal! zo
2198
normal! zo
2200
normal! zo
2202
normal! zo
2203
normal! zo
2203
normal! zo
2203
normal! zo
2207
normal! zo
2208
normal! zo
2208
normal! zo
2208
normal! zo
2214
normal! zo
2225
normal! zo
2230
normal! zo
2235
normal! zo
2236
normal! zo
2236
normal! zo
2237
normal! zo
2243
normal! zo
2268
normal! zo
2289
normal! zo
2340
normal! zo
2345
normal! zo
2454
normal! zo
2504
normal! zo
2567
normal! zo
2575
normal! zo
2580
normal! zo
2586
normal! zo
2593
normal! zo
2594
normal! zo
2616
normal! zo
2723
normal! zo
2724
normal! zo
2724
normal! zo
2761
normal! zo
2765
normal! zo
2779
normal! zo
2849
normal! zo
2922
normal! zo
2926
normal! zo
2926
normal! zo
2926
normal! zo
2933
normal! zo
2937
normal! zo
2937
normal! zo
2937
normal! zo
3176
normal! zo
3232
normal! zo
3239
normal! zo
3261
normal! zo
3266
normal! zo
3266
normal! zo
3289
normal! zo
3316
normal! zo
3326
normal! zo
3327
normal! zo
3329
normal! zo
3335
normal! zo
3337
normal! zo
3339
normal! zo
3359
normal! zo
3372
normal! zo
3732
normal! zo
3740
normal! zo
3756
normal! zo
3768
normal! zo
3785
normal! zo
3794
normal! zo
3808
normal! zo
3808
normal! zo
3810
normal! zo
3810
normal! zo
3810
normal! zo
4226
normal! zo
let s:l = 1100 - ((0 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1100
normal! 030|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
argglobal
edit ~/Geotexan/src/Geotex-INN/ginn/formularios/facturas_compra.py
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
79
normal! zo
585
normal! zo
605
normal! zo
649
normal! zo
717
normal! zo
725
normal! zo
730
normal! zo
731
normal! zo
731
normal! zo
731
normal! zo
731
normal! zo
731
normal! zo
753
normal! zo
773
normal! zo
896
normal! zo
962
normal! zo
968
normal! zo
1016
normal! zo
1027
normal! zo
1028
normal! zo
1034
normal! zo
1961
normal! zo
1979
normal! zo
let s:l = 788 - ((2 * winheight(0) + 2) / 5)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
788
normal! 050|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
6wincmd w
exe 'vert 1resize ' . ((&columns * 20 + 51) / 103)
exe '2resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 2resize ' . ((&columns * 82 + 51) / 103)
exe '3resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 3resize ' . ((&columns * 82 + 51) / 103)
exe '4resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 4resize ' . ((&columns * 82 + 51) / 103)
exe '5resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 5resize ' . ((&columns * 82 + 51) / 103)
exe '6resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 6resize ' . ((&columns * 82 + 51) / 103)
exe '7resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 7resize ' . ((&columns * 82 + 51) / 103)
exe '8resize ' . ((&lines * 5 + 21) / 43)
exe 'vert 8resize ' . ((&columns * 82 + 51) / 103)
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
