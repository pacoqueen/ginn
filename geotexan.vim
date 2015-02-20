" ~/Geotexan/src/Geotex-INN/geotexan.vim: Vim session script.
" Created by session.vim 1.5 on 20 febrero 2015 at 15:57:00.
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
badd +1060 ginn/formularios/partes_de_fabricacion_balas.py
badd +1 ginn/formularios/facturas_compra.py
badd +1 fugitive:///home/bogado/Geotexan/src/Geotex-INN/.git//0/ginn/formularios/utils.py
badd +9 ginn/lib/fuzzywuzzy/fuzzywuzzy/utils.py
badd +1 formularios/auditviewer.py
badd +1260 ginn/formularios/utils.py
badd +2299 ginn/formularios/presupuestos.py
badd +38 ginn/informes/treeview2pdf.py
badd +138 ginn/formularios/listado_rollos.py
badd +2 ginn/lib/fuzzywuzzy/fuzzywuzzy/__init__.py
argglobal
silent! argdel *
argadd formularios/auditviewer.py
set lines=54 columns=103
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
4wincmd k
wincmd w
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 20 + 51) / 103)
exe '2resize ' . ((&lines * 10 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 82 + 51) / 103)
exe '3resize ' . ((&lines * 9 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 82 + 51) / 103)
exe '4resize ' . ((&lines * 10 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 82 + 51) / 103)
exe '5resize ' . ((&lines * 10 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 82 + 51) / 103)
exe '6resize ' . ((&lines * 9 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 82 + 51) / 103)
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
let s:l = 22 - ((0 * winheight(0) + 5) / 10)
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
1240
normal! zo
1252
normal! zo
1263
normal! zo
1921
normal! zo
1982
normal! zo
2555
normal! zo
2555
normal! zo
2555
normal! zo
let s:l = 1262 - ((6 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1262
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
16930
normal! zo
16930
normal! zo
16930
normal! zo
16931
normal! zo
17906
normal! zo
17915
normal! zo
17916
normal! zo
17916
normal! zo
17925
normal! zo
19176
normal! zo
19248
normal! zo
19254
normal! zo
19257
normal! zo
19258
normal! zo
19258
normal! zo
19258
normal! zo
19258
normal! zo
19268
normal! zo
19274
normal! zo
19277
normal! zo
19278
normal! zo
19278
normal! zo
19278
normal! zo
19278
normal! zo
19700
normal! zo
19789
normal! zo
let s:l = 19272 - ((4 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
19272
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
1405
normal! zo
1406
normal! zo
1407
normal! zo
1412
normal! zo
1413
normal! zo
1413
normal! zo
1413
normal! zo
1413
normal! zo
1413
normal! zo
1413
normal! zo
1416
normal! zo
1424
normal! zo
1433
normal! zo
1446
normal! zo
1447
normal! zo
1452
normal! zo
1456
normal! zo
1464
normal! zo
1471
normal! zo
1481
normal! zo
1483
normal! zo
1490
normal! zo
1492
normal! zo
1515
normal! zo
1533
normal! zo
1535
normal! zo
1542
normal! zo
1544
normal! zo
1545
normal! zo
1545
normal! zo
1545
normal! zo
1553
normal! zo
1554
normal! zo
1554
normal! zo
1554
normal! zo
1558
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
1582
normal! zo
1602
normal! zo
1606
normal! zo
1614
normal! zo
1615
normal! zo
1615
normal! zo
1615
normal! zo
1625
normal! zo
1644
normal! zo
1651
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1652
normal! zo
1661
normal! zo
1669
normal! zo
1670
normal! zo
1670
normal! zo
1670
normal! zo
1686
normal! zo
1693
normal! zo
1694
normal! zo
1704
normal! zo
1712
normal! zo
1713
normal! zo
1713
normal! zo
1713
normal! zo
1725
normal! zo
1735
normal! zo
1735
normal! zo
1735
normal! zo
1735
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1743
normal! zo
1759
normal! zo
1770
normal! zo
1771
normal! zo
1772
normal! zo
1774
normal! zo
1775
normal! zo
1775
normal! zo
1775
normal! zo
1775
normal! zo
1787
normal! zo
1798
normal! zo
1799
normal! zo
1799
normal! zo
1799
normal! zo
1804
normal! zo
1805
normal! zo
1819
normal! zo
1819
normal! zo
1820
normal! zo
1828
normal! zo
1829
normal! zo
1840
normal! zo
1846
normal! zo
1861
normal! zo
1873
normal! zo
1881
normal! zo
1881
normal! zo
1881
normal! zo
1881
normal! zo
1892
normal! zo
1903
normal! zo
1926
normal! zo
1948
normal! zo
1948
normal! zo
1948
normal! zo
1948
normal! zo
1960
normal! zo
1965
normal! zo
1981
normal! zo
1999
normal! zo
2019
normal! zo
2027
normal! zo
2030
normal! zo
2035
normal! zo
2044
normal! zo
2044
normal! zo
2053
normal! zo
2053
normal! zo
2054
normal! zo
2054
normal! zo
2054
normal! zo
2061
normal! zo
2062
normal! zo
2062
normal! zo
2062
normal! zo
2068
normal! zo
2076
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2083
normal! zo
2092
normal! zo
2103
normal! zo
2114
normal! zo
2115
normal! zo
2118
normal! zo
2119
normal! zo
2119
normal! zo
2119
normal! zo
2123
normal! zo
2123
normal! zo
2123
normal! zo
2123
normal! zo
2129
normal! zo
2130
normal! zo
2130
normal! zo
2130
normal! zo
2134
normal! zo
2142
normal! zo
2152
normal! zo
2157
normal! zo
2158
normal! zo
2158
normal! zo
2158
normal! zo
2163
normal! zo
2181
normal! zo
2182
normal! zo
2183
normal! zo
2184
normal! zo
2184
normal! zo
2184
normal! zo
2188
normal! zo
2189
normal! zo
2190
normal! zo
2192
normal! zo
2194
normal! zo
2195
normal! zo
2195
normal! zo
2195
normal! zo
2199
normal! zo
2200
normal! zo
2200
normal! zo
2200
normal! zo
2206
normal! zo
2217
normal! zo
2222
normal! zo
2227
normal! zo
2228
normal! zo
2228
normal! zo
2229
normal! zo
2235
normal! zo
2260
normal! zo
2281
normal! zo
2332
normal! zo
2337
normal! zo
2446
normal! zo
2496
normal! zo
2559
normal! zo
2567
normal! zo
2572
normal! zo
2578
normal! zo
2585
normal! zo
2586
normal! zo
2608
normal! zo
2715
normal! zo
2716
normal! zo
2716
normal! zo
2753
normal! zo
2757
normal! zo
2771
normal! zo
2841
normal! zo
2914
normal! zo
2918
normal! zo
2918
normal! zo
2918
normal! zo
2925
normal! zo
2929
normal! zo
2929
normal! zo
2929
normal! zo
3168
normal! zo
3224
normal! zo
3231
normal! zo
3253
normal! zo
3258
normal! zo
3258
normal! zo
3281
normal! zo
3308
normal! zo
3318
normal! zo
3319
normal! zo
3321
normal! zo
3327
normal! zo
3329
normal! zo
3331
normal! zo
3351
normal! zo
3364
normal! zo
3724
normal! zo
3732
normal! zo
3748
normal! zo
3760
normal! zo
3777
normal! zo
3786
normal! zo
3800
normal! zo
3800
normal! zo
3802
normal! zo
3802
normal! zo
3802
normal! zo
4218
normal! zo
let s:l = 1100 - ((3 * winheight(0) + 5) / 10)
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
let s:l = 789 - ((4 * winheight(0) + 4) / 9)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
789
normal! 011|
lcd ~/Geotexan/src/Geotex-INN
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 20 + 51) / 103)
exe '2resize ' . ((&lines * 10 + 27) / 54)
exe 'vert 2resize ' . ((&columns * 82 + 51) / 103)
exe '3resize ' . ((&lines * 9 + 27) / 54)
exe 'vert 3resize ' . ((&columns * 82 + 51) / 103)
exe '4resize ' . ((&lines * 10 + 27) / 54)
exe 'vert 4resize ' . ((&columns * 82 + 51) / 103)
exe '5resize ' . ((&lines * 10 + 27) / 54)
exe 'vert 5resize ' . ((&columns * 82 + 51) / 103)
exe '6resize ' . ((&lines * 9 + 27) / 54)
exe 'vert 6resize ' . ((&columns * 82 + 51) / 103)
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
4wincmd w

" vim: ft=vim ro nowrap smc=128
