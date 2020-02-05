#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

"""
Geotextiles C perdidos del packing list
=======================================

En el albarán X44732 salen 42 rollos de Geotextil clase C (PV364) pero en el
packing list no se ve ninguno. Como consecuencia, hay 42 rollos en almacén que
pesan entre todos 4.191,90 kg que en realidad no están.
Sabemos los códigos de los 470 rollos que había el 1 de febrero. El albarán es
del 22 de enero. Podemos saber también los rollos que había hasta esa fecha por
su fecha de fabricación, lo que nos dejará algunos menos.
Las combinaciones de m elementos tomados de n en n sin repetición y sin
importar el orden son:
    C_470,42 = 1.8210971934995877e+60
Casi _na_.

Después de algunas pruebas y sin intentar siquiera optimizar o meter heurística
estimo que tardaría en explorar todas las soluciones unas 3 sextillones de
veces la edad del universo: 4x10^46 años.
"""

from __future__ import print_function
from math import factorial
import sys
import os
import datetime
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
if DIRACTUAL != "ginn":
    PATH_TO_F = os.path.join("..", "..", "ginn")
    sys.path.append(PATH_TO_F)
# pylint: disable=wrong-import-position,import-error
from framework import pclases   # noqa
# from api import murano          # noqa
from lib.tqdm.tqdm import tqdm  # noqa
from itertools import combinations


TARGET = (42, 4191.9)


def cargar_articulos(codigos, fecha_tope=None):
    """
    Devuelve una lista de rollos y pesos cuya fecha de fabricación es anterior
    a la indicada en fecha_tope.
    """
    if not fecha_tope:
        fecha_tope = datetime.date(2020, 1, 22)
    res = []
    for codigo in tqdm(codigos):
        articulo = pclases.Articulo.get_articulo(codigo)
        try:
            if articulo.fecha_fabricacion <= fecha_tope:
                res.append((articulo.codigo, articulo.peso_neto))
        except AttributeError:
            print("{} no se encontró en la base de datos.".format(codigo))
            sys.exit(1)
    return res


def numero_combinaciones(m, n):
    """Calcula y devuelve el número de combinaciones
       posibles que se pueden hacer con m elementos
       tomando n elementos a la vez.
    """
    return factorial(m) // (factorial(n) * factorial(m - n))


def cumple(rollos, bultos, kg):
    """
    Comprueba si la lista de rollos recibida cumple con el número de bultos
    y peso neto total recibido.
    """
    cumple_bultos = len(rollos) == bultos
    res = cumple_bultos
    if res:
        cumple_peso = round(sum([r[1] for r in rollos]), 2) == round(kg, 2)
        res = res and cumple_peso
    return res


def find(bultos, kg, rollos):
    """
    Devuelve una lista de la forma
    ((codigo1, codigo2, ... codigon), peso_neto_total),
     (codigo1, codigo3, ... codigom), peso_neto_total),
     ...
    )
    que cumplen el criterio de número de códigos con peso total igual los
    parámetros recibidos:
    bultos: número de bultos que debe llevar la tupla
    kg: peso total de los rollos de la tupla
    rollos: lista de la forma ((codigo1, peso_neto1),... (codigon, peso_neton))
    """
    print("{} combinaciones.".format(numero_combinaciones(len(rollos),
                                                          bultos)))
    res = []
    # Datos de prueba
    for test in tqdm(combinations(rollos, bultos)):
        if cumple(test, bultos, kg):
            res.append(([t[0] for t in test], sum([t[1] for t in test])))
            break   # Me vale con la primera combinación que pudiera encontrar.
    return res


# pylint: disable=too-many-locals, too-many-statements
def main():
    """
    Rutina principal.
    """
    codigos = """Y5267
Y5269
Y5270
Y5271
Y5272
Y5273
Y5274
Y5275
Y5276
Y5277
Y5278
Y5279
Y5280
Y5281
Y5282
Y5283
Y5284
Y5285
Y5286
Y5287
Y5288
Y5289
Y5290
Y5291
Y5292
Y5293
Y5294
Y5295
Y5296
Y5297
Y5298
Y5299
Y5300
Y5301
Y5302
Y5303
Y5304
Y5305
Y5306
Y5307
Y5308
Y5309
Y5310
Y5312
Y5313
Y5314
Y5315
Y5316
Y5317
Y5318
Y5319
Y5320
Y5322
Y5324
Y5325
Y5326
Y5327
Y5335
Y5343
Y5346
Y5347
Y5348
Y5351
Y5352
Y5361
Y5363
Y5373
Y5375
Y5377
Y5378
Y5382
Y5385
Y5386
Y5391
Y5392
Y5393
Y5394
Y5396
Y5410
Y5411
Y5412
Y5413
Y5414
Y5423
Y5424
Y5425
Y5426
Y5427
Y5430
Y5431
Y5432
Y5433
Y5434
Y5436
Y5451
Y5453
Y5455
Y5456
Y5457
Y5472
Y5473
Y5488
Y5491
Y5492
Y5493
Y5495
Y5496
Y5497
Y5499
Y5502
Y5510
Y5511
Y5518
Y5522
Y5528
Y5531
Y5532
Y5534
Y5537
Y5540
Y5547
Y5550
Y5551
Y5564
Y5572
Y5574
Y5575
Y5580
Y5584
Y5588
Y5589
Y5591
Y5597
Y5600
Y5602
Y5604
Y5617
Y5623
Y5625
Y5627
Y5629
Y5633
Y5635
Y5645
Y5649
Y5654
Y5656
Y5658
Y5663
Y5667
Y5671
Y5675
Y5676
Y5679
Y5685
Y5709
Y5710
Y5720
Y5723
Y5726
Y5736
Y5737
Y5739
Y5750
Y5762
Y5765
Y5768
Y5769
Y5771
Y5776
Y5780
Y5786
Y5787
Y5788
Y5793
Y5806
Y5808
Y5834
Y5838
Y5839
Y5840
Y5842
Y5843
Y5845
Y5851
Y5853
Y5857
Y5858
Y5859
Y5862
Y5868
Y5871
Y5874
Y5875
Y5880
Y5883
Y5884
Y5885
Y5888
Y5893
Y5894
Y5896
Y5898
Y5900
Y5905
Y5906
Y5907
Y5919
Y5934
Y5943
Y5970
Y5972
Y5975
Y5978
Y5979
Y5982
Y5983
Y5984
Y5995
Y5996
Y5997
Y6000
Y6004
Y6007
Y6008
Y6009
Y6010
Y6011
Y6013
Y6014
Y6015
Y6016
Y6017
Y6018
Y6019
Y6020
Y6021
Y6022
Y6023
Y6024
Y6025
Y6026
Y6029
Y6031
Y6032
Y6033
Y6034
Y6035
Y6036
Y6037
Y6038
Y6039
Y6043
Y6044
Y6045
Y6046
Y6049
Y6050
Y6051
Y6052
Y6053
Y6054
Y6055
Y6056
Y6059
Y6060
Y6061
Y6062
Y6063
Y6064
Y6065
Y6066
Y6067
Y6068
Y6069
Y6070
Y6071
Y6072
Y6074
Y6075
Y6076
Y6077
Y6078
Y6079
Y6083
Y6084
Y6085
Y6087
Y6088
Y6090
Y6092
Y6093
Y6094
Y6095
Y6098
Y6099
Y6100
Y6101
Y6102
Y6103
Y6105
Y6106
Y6107
Y6108
Y6109
Y6110
Y6111
Y6112
Y6113
Y6114
Y6115
Y6116
Y6117
Y6118
Y6119
Y6120
Y6121
Y6122
Y6123
Y6124
Y6125
Y6126
Y6127
Y6128
Y6129
Y6130
Y6131
Y6132
Y6133
Y6134
Y6135
Y6136
Y6137
Y6138
Y6139
Y6142
Y6143
Y6144
Y6145
Y6146
Y6147
Y6148
Y6149
Y6150
Y6152
Y6153
Y6154
Y6155
Y6156
Y6160
Y6161
Y6162
Y6163
Y6165
Y6166
Y6169
Y6170
Y6171
Y6172
Y6173
Y6174
Y6175
Y6176
Y6177
Y6178
Y6179
Y6180
Y6181
Y6182
Y6183
Y6184
Y6185
Y6186
Y6187
Y6188
Y6189
Y6190
Y6191
Y6192
Y6193
Y6194
Y6195
Y6196
Y6197
Y6198
Y6199
Y6200
Y6201
Y6202
Y6203
Y6204
Y6205
Y6206
Y6207
Y6208
Y6209
Y6211
Y6212
Y6213
Y6214
Y6216
Y6217
Y6218
Y6219
Y6220
Y6221
Y6222
Y6224
Y6225
Y6226
Y6227
Y6228
Y6229
Y6230
Y6231
Y6232
Y6233
Y6234
Y6235
Y6236
Y6237
Y6238
Y6239
Y6240
Y6241
Y6242
Y6243
Y6244
Y6245
Y6246
Y6247
Y6248
Y6250
Y6251
Y6252
Y6255
Y6256
Y6257
Y6263
Y6264
Y6265
Y6266
Y6267
Y6268
Y6269
Y6270
Y6271
Y6272
Y6273
Y6274
Y6275
Y6276
Y6278
Y6282
Y6283
Y6284
Y6285
Y6286
Y6287
Y6288
Y6289
Y6290
Y6291
Y6292
Y6293
Y6295
Y6297
Y6298
Y6299
Y6300""".split()
    fout = open("X44732_PV364.txt", "w")
    rollos = cargar_articulos(codigos, datetime.date(2020, 1, 22))
    bultos, kg = TARGET
    candidatos = find(bultos, kg, rollos)
    for candidato in candidatos:
        codigos, peso = candidato
        fout.write("[{}]; {} bultos, {} kg\n".format(", ".join(codigos),
                                                     len(codigos), peso))
    fout.close()


if __name__ == "__main__":
    main()
