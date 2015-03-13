" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 13 marzo 2015 at 13:41:29.
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
badd +556 ginn/formularios/partes_de_fabricacion_balas.py
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
badd +75 ginn/formularios/consulta_saldo_proveedores.py
args formularios/auditviewer.py
set lines=43 columns=101
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
exe 'vert 1resize ' . ((&columns * 19 + 50) / 101)
exe '2resize ' . ((&lines * 6 + 21) / 43)
exe 'vert 2resize ' . ((&columns * 81 + 50) / 101)
exe '3resize ' . ((&lines * 26 + 21) / 43)
exe 'vert 3resize ' . ((&columns * 81 + 50) / 101)
exe '4resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 4resize ' . ((&columns * 81 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 5resize ' . ((&columns * 81 + 50) / 101)
exe '6resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 6resize ' . ((&columns * 81 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 7resize ' . ((&columns * 81 + 50) / 101)
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
let s:l = 22 - ((0 * winheight(0) + 3) / 6)
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
1282
normal! zo
1284
normal! zo
1287
normal! zo
1308
normal! zo
2384
normal! zo
let s:l = 1287 - ((16 * winheight(0) + 13) / 26)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1287
normal! 025|
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
let s:l = 180 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
180
normal! 028|
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
let s:l = 16884 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16884
normal! 035|
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
554
normal! zo
555
normal! zo
555
normal! zo
555
normal! zo
571
normal! zo
576
normal! zo
583
normal! zo
584
normal! zo
584
normal! zo
588
normal! zo
595
normal! zo
595
normal! zo
601
normal! zo
613
normal! zo
614
normal! zo
614
normal! zo
614
normal! zo
617
normal! zo
625
normal! zo
626
normal! zo
626
normal! zo
626
normal! zo
632
normal! zo
651
normal! zo
664
normal! zo
671
normal! zo
672
normal! zo
680
normal! zo
681
normal! zo
681
normal! zo
681
normal! zo
681
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
701
normal! zo
701
normal! zo
701
normal! zo
701
normal! zo
701
normal! zo
701
normal! zo
713
normal! zo
713
normal! zo
713
normal! zo
713
normal! zo
717
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
726
normal! zo
734
normal! zo
739
normal! zo
751
normal! zo
757
normal! zo
757
normal! zo
757
normal! zo
760
normal! zo
760
normal! zo
760
normal! zo
770
normal! zo
774
normal! zo
774
normal! zo
783
normal! zo
784
normal! zo
793
normal! zo
793
normal! zo
793
normal! zo
793
normal! zo
793
normal! zo
804
normal! zo
815
normal! zo
818
normal! zo
819
normal! zo
819
normal! zo
828
normal! zo
829
normal! zo
829
normal! zo
829
normal! zo
829
normal! zo
830
normal! zo
847
normal! zo
870
normal! zo
890
normal! zo
910
normal! zo
931
normal! zo
936
normal! zo
945
normal! zo
956
normal! zo
965
normal! zo
966
normal! zo
966
normal! zo
966
normal! zo
971
normal! zo
971
normal! zo
974
normal! zo
974
normal! zo
986
normal! zo
988
normal! zo
991
normal! zo
1004
normal! zo
1025
normal! zo
1025
normal! zo
1031
normal! zo
1048
normal! zo
1049
normal! zo
1070
normal! zo
1072
normal! zo
1076
normal! zo
1080
normal! zo
1096
normal! zo
1104
normal! zo
1105
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
1147
normal! zo
1148
normal! zo
1152
normal! zo
1153
normal! zo
1153
normal! zo
1153
normal! zo
1159
normal! zo
1160
normal! zo
1169
normal! zo
1178
normal! zo
1181
normal! zo
1187
normal! zo
1193
normal! zo
1194
normal! zo
1194
normal! zo
1199
normal! zo
1207
normal! zo
1213
normal! zo
1242
normal! zo
1243
normal! zo
1245
normal! zo
1249
normal! zo
1250
normal! zo
1255
normal! zo
1264
normal! zo
1265
normal! zo
1269
normal! zo
1270
normal! zo
1281
normal! zo
1284
normal! zo
1301
normal! zo
1307
normal! zo
1319
normal! zo
1320
normal! zo
1320
normal! zo
1320
normal! zo
1320
normal! zo
1334
normal! zo
1365
normal! zo
1368
normal! zo
1368
normal! zo
1368
normal! zo
1368
normal! zo
1368
normal! zo
1368
normal! zo
1368
normal! zo
1368
normal! zo
1374
normal! zo
1379
normal! zo
1388
normal! zo
1395
normal! zo
1395
normal! zo
1401
normal! zo
1406
normal! zo
1413
normal! zo
1414
normal! zo
1414
normal! zo
1414
normal! zo
1418
normal! zo
1420
normal! zo
1421
normal! zo
1426
normal! zo
1427
normal! zo
1427
normal! zo
1427
normal! zo
1427
normal! zo
1427
normal! zo
1427
normal! zo
1430
normal! zo
1438
normal! zo
1447
normal! zo
1460
normal! zo
1461
normal! zo
1466
normal! zo
1470
normal! zo
1478
normal! zo
1485
normal! zo
1495
normal! zo
1497
normal! zo
1504
normal! zo
1506
normal! zo
1529
normal! zo
1547
normal! zo
1549
normal! zo
1556
normal! zo
1558
normal! zo
1559
normal! zo
1559
normal! zo
1559
normal! zo
1567
normal! zo
1568
normal! zo
1568
normal! zo
1568
normal! zo
1572
normal! zo
1581
normal! zo
1582
normal! zo
1582
normal! zo
1582
normal! zo
1586
normal! zo
1596
normal! zo
1616
normal! zo
1620
normal! zo
1628
normal! zo
1629
normal! zo
1629
normal! zo
1629
normal! zo
1639
normal! zo
1658
normal! zo
1665
normal! zo
1666
normal! zo
1666
normal! zo
1666
normal! zo
1666
normal! zo
1666
normal! zo
1666
normal! zo
1666
normal! zo
1666
normal! zo
1666
normal! zo
1666
normal! zo
1666
normal! zo
1675
normal! zo
1683
normal! zo
1684
normal! zo
1684
normal! zo
1684
normal! zo
1700
normal! zo
1707
normal! zo
1708
normal! zo
1718
normal! zo
1726
normal! zo
1727
normal! zo
1727
normal! zo
1727
normal! zo
1739
normal! zo
1749
normal! zo
1749
normal! zo
1749
normal! zo
1749
normal! zo
1757
normal! zo
1757
normal! zo
1757
normal! zo
1757
normal! zo
1757
normal! zo
1757
normal! zo
1757
normal! zo
1757
normal! zo
1757
normal! zo
1757
normal! zo
1773
normal! zo
1784
normal! zo
1785
normal! zo
1786
normal! zo
1788
normal! zo
1789
normal! zo
1789
normal! zo
1789
normal! zo
1789
normal! zo
1801
normal! zo
1812
normal! zo
1813
normal! zo
1813
normal! zo
1813
normal! zo
1818
normal! zo
1819
normal! zo
1833
normal! zo
1833
normal! zo
1834
normal! zo
1842
normal! zo
1843
normal! zo
1854
normal! zo
1860
normal! zo
1875
normal! zo
1887
normal! zo
1895
normal! zo
1895
normal! zo
1895
normal! zo
1895
normal! zo
1906
normal! zo
1917
normal! zo
1940
normal! zo
1962
normal! zo
1962
normal! zo
1962
normal! zo
1962
normal! zo
1974
normal! zo
1979
normal! zo
1995
normal! zo
2013
normal! zo
2033
normal! zo
2041
normal! zo
2044
normal! zo
2049
normal! zo
2058
normal! zo
2058
normal! zo
2067
normal! zo
2067
normal! zo
2068
normal! zo
2068
normal! zo
2068
normal! zo
2075
normal! zo
2076
normal! zo
2076
normal! zo
2076
normal! zo
2082
normal! zo
2090
normal! zo
2097
normal! zo
2097
normal! zo
2097
normal! zo
2097
normal! zo
2097
normal! zo
2097
normal! zo
2097
normal! zo
2097
normal! zo
2106
normal! zo
2117
normal! zo
2128
normal! zo
2129
normal! zo
2132
normal! zo
2133
normal! zo
2133
normal! zo
2133
normal! zo
2137
normal! zo
2137
normal! zo
2137
normal! zo
2137
normal! zo
2143
normal! zo
2144
normal! zo
2144
normal! zo
2144
normal! zo
2148
normal! zo
2156
normal! zo
2166
normal! zo
2171
normal! zo
2172
normal! zo
2172
normal! zo
2172
normal! zo
2177
normal! zo
2195
normal! zo
2196
normal! zo
2197
normal! zo
2198
normal! zo
2198
normal! zo
2198
normal! zo
2202
normal! zo
2203
normal! zo
2204
normal! zo
2206
normal! zo
2208
normal! zo
2209
normal! zo
2209
normal! zo
2209
normal! zo
2213
normal! zo
2214
normal! zo
2214
normal! zo
2214
normal! zo
2220
normal! zo
2231
normal! zo
2236
normal! zo
2241
normal! zo
2242
normal! zo
2242
normal! zo
2243
normal! zo
2249
normal! zo
2274
normal! zo
2295
normal! zo
2346
normal! zo
2351
normal! zo
2460
normal! zo
2510
normal! zo
2573
normal! zo
2581
normal! zo
2586
normal! zo
2592
normal! zo
2599
normal! zo
2600
normal! zo
2622
normal! zo
2729
normal! zo
2730
normal! zo
2730
normal! zo
2767
normal! zo
2771
normal! zo
2785
normal! zo
2855
normal! zo
2928
normal! zo
2932
normal! zo
2932
normal! zo
2932
normal! zo
2939
normal! zo
2943
normal! zo
2943
normal! zo
2943
normal! zo
3182
normal! zo
3238
normal! zo
3245
normal! zo
3267
normal! zo
3272
normal! zo
3272
normal! zo
3295
normal! zo
3322
normal! zo
3332
normal! zo
3333
normal! zo
3335
normal! zo
3341
normal! zo
3343
normal! zo
3345
normal! zo
3365
normal! zo
3378
normal! zo
3738
normal! zo
3746
normal! zo
3762
normal! zo
3774
normal! zo
3791
normal! zo
3800
normal! zo
3814
normal! zo
3814
normal! zo
3816
normal! zo
3816
normal! zo
3816
normal! zo
4232
normal! zo
let s:l = 1106 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1106
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
let s:l = 788 - ((0 * winheight(0) + 0) / 1)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
788
normal! 050|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 19 + 50) / 101)
exe '2resize ' . ((&lines * 6 + 21) / 43)
exe 'vert 2resize ' . ((&columns * 81 + 50) / 101)
exe '3resize ' . ((&lines * 26 + 21) / 43)
exe 'vert 3resize ' . ((&columns * 81 + 50) / 101)
exe '4resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 4resize ' . ((&columns * 81 + 50) / 101)
exe '5resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 5resize ' . ((&columns * 81 + 50) / 101)
exe '6resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 6resize ' . ((&columns * 81 + 50) / 101)
exe '7resize ' . ((&lines * 1 + 21) / 43)
exe 'vert 7resize ' . ((&columns * 81 + 50) / 101)
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
3wincmd w

" vim: ft=vim ro nowrap smc=128
