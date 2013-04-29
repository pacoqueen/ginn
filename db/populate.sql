--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.6
-- Dumped by pg_dump version 9.1.6
-- Started on 2012-11-05 14:59:00 CET

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- TOC entry 4607 (class 0 OID 0)
-- Dependencies: 363
-- Name: abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('abono_id_seq', 1, false);


--
-- TOC entry 4608 (class 0 OID 0)
-- Dependencies: 451
-- Name: alarma_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('alarma_id_seq', 1, false);


--
-- TOC entry 4609 (class 0 OID 0)
-- Dependencies: 367
-- Name: albaran_de_entrada_de_abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('albaran_de_entrada_de_abono_id_seq', 1, false);


--
-- TOC entry 4610 (class 0 OID 0)
-- Dependencies: 214
-- Name: albaran_entrada_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('albaran_entrada_id_seq', 1, false);


--
-- TOC entry 4611 (class 0 OID 0)
-- Dependencies: 282
-- Name: albaran_salida_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('albaran_salida_id_seq', 1, false);


--
-- TOC entry 4612 (class 0 OID 0)
-- Dependencies: 419
-- Name: alerta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('alerta_id_seq', 1, false);


--
-- TOC entry 4613 (class 0 OID 0)
-- Dependencies: 212
-- Name: almacen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('almacen_id_seq', 1, false);


--
-- TOC entry 4614 (class 0 OID 0)
-- Dependencies: 308
-- Name: articulo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('articulo_id_seq', 1, false);


--
-- TOC entry 4615 (class 0 OID 0)
-- Dependencies: 240
-- Name: ausencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('ausencia_id_seq', 1, false);


--
-- TOC entry 4616 (class 0 OID 0)
-- Dependencies: 242
-- Name: baja_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('baja_id_seq', 1, false);


--
-- TOC entry 4617 (class 0 OID 0)
-- Dependencies: 304
-- Name: bala_cable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('bala_cable_id_seq', 1, false);


--
-- TOC entry 4618 (class 0 OID 0)
-- Dependencies: 290
-- Name: bala_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('bala_id_seq', 1, false);


--
-- TOC entry 4619 (class 0 OID 0)
-- Dependencies: 294
-- Name: bigbag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('bigbag_id_seq', 1, false);


--
-- TOC entry 4620 (class 0 OID 0)
-- Dependencies: 298
-- Name: caja_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('caja_id_seq', 1, false);


--
-- TOC entry 4621 (class 0 OID 0)
-- Dependencies: 248
-- Name: calendario_laboral_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('calendario_laboral_id_seq', 1, false);


--
-- TOC entry 4622 (class 0 OID 0)
-- Dependencies: 183
-- Name: campos_especificos_bala_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('campos_especificos_bala_id_seq', 1, false);


--
-- TOC entry 4623 (class 0 OID 0)
-- Dependencies: 191
-- Name: campos_especificos_especial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('campos_especificos_especial_id_seq', 1, false);


--
-- TOC entry 4624 (class 0 OID 0)
-- Dependencies: 274
-- Name: campos_especificos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('campos_especificos_id_seq', 1, false);


--
-- TOC entry 4625 (class 0 OID 0)
-- Dependencies: 187
-- Name: campos_especificos_rollo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('campos_especificos_rollo_id_seq', 1, false);


--
-- TOC entry 4626 (class 0 OID 0)
-- Dependencies: 198
-- Name: carga_silo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('carga_silo_id_seq', 1, false);


--
-- TOC entry 4627 (class 0 OID 0)
-- Dependencies: 453
-- Name: categoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('categoria_id_seq', 1, false);


--
-- TOC entry 4628 (class 0 OID 0)
-- Dependencies: 210
-- Name: categoria_laboral_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('categoria_laboral_id_seq', 1, false);


--
-- TOC entry 4629 (class 0 OID 0)
-- Dependencies: 228
-- Name: centro_trabajo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('centro_trabajo_id_seq', 1, false);


--
-- TOC entry 4630 (class 0 OID 0)
-- Dependencies: 270
-- Name: cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('cliente_id_seq', 2, true);


--
-- TOC entry 4631 (class 0 OID 0)
-- Dependencies: 361
-- Name: cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('cobro_id_seq', 1, false);


--
-- TOC entry 4632 (class 0 OID 0)
-- Dependencies: 234
-- Name: comercial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('comercial_id_seq', 1, false);


--
-- TOC entry 4633 (class 0 OID 0)
-- Dependencies: 333
-- Name: comision_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('comision_id_seq', 1, false);


--
-- TOC entry 4634 (class 0 OID 0)
-- Dependencies: 355
-- Name: confirming_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('confirming_id_seq', 1, false);


--
-- TOC entry 4635 (class 0 OID 0)
-- Dependencies: 177
-- Name: consumo_adicional_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('consumo_adicional_id_seq', 1, false);


--
-- TOC entry 4636 (class 0 OID 0)
-- Dependencies: 206
-- Name: consumo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('consumo_id_seq', 1, false);


--
-- TOC entry 4637 (class 0 OID 0)
-- Dependencies: 443
-- Name: contacto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('contacto_id_seq', 1, false);


--
-- TOC entry 4638 (class 0 OID 0)
-- Dependencies: 266
-- Name: contador_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('contador_id_seq', 1, true);


--
-- TOC entry 4639 (class 0 OID 0)
-- Dependencies: 429
-- Name: control_horas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('control_horas_id_seq', 1, false);


--
-- TOC entry 4640 (class 0 OID 0)
-- Dependencies: 433
-- Name: control_horas_mantenimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('control_horas_mantenimiento_id_seq', 1, false);


--
-- TOC entry 4641 (class 0 OID 0)
-- Dependencies: 431
-- Name: control_horas_produccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('control_horas_produccion_id_seq', 1, false);


--
-- TOC entry 4642 (class 0 OID 0)
-- Dependencies: 272
-- Name: cuenta_bancaria_cliente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('cuenta_bancaria_cliente_id_seq', 1, false);


--
-- TOC entry 4643 (class 0 OID 0)
-- Dependencies: 343
-- Name: cuenta_destino_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('cuenta_destino_id_seq', 1, false);


--
-- TOC entry 4644 (class 0 OID 0)
-- Dependencies: 268
-- Name: cuenta_origen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('cuenta_origen_id_seq', 1, false);


--
-- TOC entry 4645 (class 0 OID 0)
-- Dependencies: 421
-- Name: datos_de_la_empresa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('datos_de_la_empresa_id_seq', 1, false);


--
-- TOC entry 4646 (class 0 OID 0)
-- Dependencies: 208
-- Name: descuento_de_material_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('descuento_de_material_id_seq', 1, false);


--
-- TOC entry 4647 (class 0 OID 0)
-- Dependencies: 167
-- Name: destino_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('destino_id_seq', 1, false);


--
-- TOC entry 4648 (class 0 OID 0)
-- Dependencies: 425
-- Name: documento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('documento_id_seq', 1, false);


--
-- TOC entry 4649 (class 0 OID 0)
-- Dependencies: 232
-- Name: empleado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('empleado_id_seq', 1, false);


--
-- TOC entry 4650 (class 0 OID 0)
-- Dependencies: 427
-- Name: estadistica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('estadistica_id_seq', 7, true);


--
-- TOC entry 4651 (class 0 OID 0)
-- Dependencies: 449
-- Name: estado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('estado_id_seq', 1, false);


--
-- TOC entry 4652 (class 0 OID 0)
-- Dependencies: 357
-- Name: estimacion_cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('estimacion_cobro_id_seq', 1, false);


--
-- TOC entry 4653 (class 0 OID 0)
-- Dependencies: 347
-- Name: estimacion_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('estimacion_pago_id_seq', 1, false);


--
-- TOC entry 4654 (class 0 OID 0)
-- Dependencies: 324
-- Name: factura_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('factura_compra_id_seq', 1, false);


--
-- TOC entry 4655 (class 0 OID 0)
-- Dependencies: 359
-- Name: factura_de_abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('factura_de_abono_id_seq', 1, false);


--
-- TOC entry 4656 (class 0 OID 0)
-- Dependencies: 312
-- Name: factura_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('factura_venta_id_seq', 1, false);


--
-- TOC entry 4657 (class 0 OID 0)
-- Dependencies: 252
-- Name: festivo_generico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('festivo_generico_id_seq', 1, false);


--
-- TOC entry 4658 (class 0 OID 0)
-- Dependencies: 250
-- Name: festivo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('festivo_id_seq', 1, false);


--
-- TOC entry 4659 (class 0 OID 0)
-- Dependencies: 175
-- Name: formulacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('formulacion_id_seq', 1, false);


--
-- TOC entry 4660 (class 0 OID 0)
-- Dependencies: 258
-- Name: grupo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('grupo_id_seq', 1, false);


--
-- TOC entry 4661 (class 0 OID 0)
-- Dependencies: 218
-- Name: historial_existencias_a_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('historial_existencias_a_id_seq', 1, false);


--
-- TOC entry 4662 (class 0 OID 0)
-- Dependencies: 220
-- Name: historial_existencias_b_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('historial_existencias_b_id_seq', 1, false);


--
-- TOC entry 4663 (class 0 OID 0)
-- Dependencies: 222
-- Name: historial_existencias_c_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('historial_existencias_c_id_seq', 1, false);


--
-- TOC entry 4664 (class 0 OID 0)
-- Dependencies: 224
-- Name: historial_existencias_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('historial_existencias_compra_id_seq', 1, false);


--
-- TOC entry 4665 (class 0 OID 0)
-- Dependencies: 216
-- Name: historial_existencias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('historial_existencias_id_seq', 1, false);


--
-- TOC entry 4666 (class 0 OID 0)
-- Dependencies: 439
-- Name: id_reciente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('id_reciente_id_seq', 1, false);


--
-- TOC entry 4667 (class 0 OID 0)
-- Dependencies: 264
-- Name: incidencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('incidencia_id_seq', 1, false);


--
-- TOC entry 4668 (class 0 OID 0)
-- Dependencies: 260
-- Name: laborable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('laborable_id_seq', 1, false);


--
-- TOC entry 4669 (class 0 OID 0)
-- Dependencies: 365
-- Name: linea_de_abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('linea_de_abono_id_seq', 1, false);


--
-- TOC entry 4670 (class 0 OID 0)
-- Dependencies: 326
-- Name: linea_de_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('linea_de_compra_id_seq', 1, false);


--
-- TOC entry 4671 (class 0 OID 0)
-- Dependencies: 369
-- Name: linea_de_devolucion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('linea_de_devolucion_id_seq', 1, false);


--
-- TOC entry 4672 (class 0 OID 0)
-- Dependencies: 310
-- Name: linea_de_movimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('linea_de_movimiento_id_seq', 1, false);


--
-- TOC entry 4673 (class 0 OID 0)
-- Dependencies: 328
-- Name: linea_de_pedido_de_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('linea_de_pedido_de_compra_id_seq', 1, false);


--
-- TOC entry 4674 (class 0 OID 0)
-- Dependencies: 320
-- Name: linea_de_pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('linea_de_pedido_id_seq', 1, false);


--
-- TOC entry 4675 (class 0 OID 0)
-- Dependencies: 179
-- Name: linea_de_produccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('linea_de_produccion_id_seq', 1, false);


--
-- TOC entry 4676 (class 0 OID 0)
-- Dependencies: 318
-- Name: linea_de_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('linea_de_venta_id_seq', 1, false);


--
-- TOC entry 4677 (class 0 OID 0)
-- Dependencies: 437
-- Name: lista_objetos_recientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('lista_objetos_recientes_id_seq', 1, false);


--
-- TOC entry 4678 (class 0 OID 0)
-- Dependencies: 339
-- Name: logic_movimientos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('logic_movimientos_id_seq', 1, false);


--
-- TOC entry 4679 (class 0 OID 0)
-- Dependencies: 292
-- Name: lote_cem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('lote_cem_id_seq', 1, false);


--
-- TOC entry 4680 (class 0 OID 0)
-- Dependencies: 284
-- Name: lote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('lote_id_seq', 1, false);


--
-- TOC entry 4681 (class 0 OID 0)
-- Dependencies: 189
-- Name: marcado_ce_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('marcado_ce_id_seq', 1, false);


--
-- TOC entry 4682 (class 0 OID 0)
-- Dependencies: 185
-- Name: modelo_etiqueta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('modelo_etiqueta_id_seq', 1, false);


--
-- TOC entry 4683 (class 0 OID 0)
-- Dependencies: 413
-- Name: modulo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('modulo_id_seq', 1, false);


--
-- TOC entry 4684 (class 0 OID 0)
-- Dependencies: 238
-- Name: motivo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('motivo_id_seq', 1, false);


--
-- TOC entry 4685 (class 0 OID 0)
-- Dependencies: 411
-- Name: muestra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('muestra_id_seq', 1, false);


--
-- TOC entry 4686 (class 0 OID 0)
-- Dependencies: 236
-- Name: nomina_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('nomina_id_seq', 1, false);


--
-- TOC entry 4687 (class 0 OID 0)
-- Dependencies: 447
-- Name: nota_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('nota_id_seq', 1, false);


--
-- TOC entry 4688 (class 0 OID 0)
-- Dependencies: 276
-- Name: obra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('obra_id_seq', 1, false);


--
-- TOC entry 4689 (class 0 OID 0)
-- Dependencies: 423
-- Name: observaciones_nominas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('observaciones_nominas_id_seq', 1, false);


--
-- TOC entry 4690 (class 0 OID 0)
-- Dependencies: 435
-- Name: orden_empleados_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('orden_empleados_id_seq', 1, false);


--
-- TOC entry 4691 (class 0 OID 0)
-- Dependencies: 353
-- Name: pagare_cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('pagare_cobro_id_seq', 1, false);


--
-- TOC entry 4692 (class 0 OID 0)
-- Dependencies: 341
-- Name: pagare_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('pagare_pago_id_seq', 1, false);


--
-- TOC entry 4693 (class 0 OID 0)
-- Dependencies: 371
-- Name: pago_de_abono_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('pago_de_abono_id_seq', 1, false);


--
-- TOC entry 4694 (class 0 OID 0)
-- Dependencies: 345
-- Name: pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('pago_id_seq', 1, false);


--
-- TOC entry 4695 (class 0 OID 0)
-- Dependencies: 296
-- Name: pale_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('pale_id_seq', 1, false);


--
-- TOC entry 4696 (class 0 OID 0)
-- Dependencies: 244
-- Name: parte_de_produccion_empleado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('parte_de_produccion_empleado_id_seq', 1, false);


--
-- TOC entry 4697 (class 0 OID 0)
-- Dependencies: 204
-- Name: parte_de_produccion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('parte_de_produccion_id_seq', 1, false);


--
-- TOC entry 4698 (class 0 OID 0)
-- Dependencies: 246
-- Name: parte_de_trabajo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('parte_de_trabajo_id_seq', 1, false);


--
-- TOC entry 4699 (class 0 OID 0)
-- Dependencies: 286
-- Name: partida_carga_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('partida_carga_id_seq', 1, false);


--
-- TOC entry 4700 (class 0 OID 0)
-- Dependencies: 202
-- Name: partida_cem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('partida_cem_id_seq', 1, false);


--
-- TOC entry 4701 (class 0 OID 0)
-- Dependencies: 288
-- Name: partida_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('partida_id_seq', 1, false);


--
-- TOC entry 4702 (class 0 OID 0)
-- Dependencies: 169
-- Name: pedido_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('pedido_compra_id_seq', 1, false);


--
-- TOC entry 4703 (class 0 OID 0)
-- Dependencies: 278
-- Name: pedido_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('pedido_venta_id_seq', 1, false);


--
-- TOC entry 4704 (class 0 OID 0)
-- Dependencies: 417
-- Name: permiso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('permiso_id_seq', 122, true);


--
-- TOC entry 4705 (class 0 OID 0)
-- Dependencies: 200
-- Name: precio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('precio_id_seq', 1, false);


--
-- TOC entry 4706 (class 0 OID 0)
-- Dependencies: 314
-- Name: prefactura_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prefactura_id_seq', 1, false);


--
-- TOC entry 4707 (class 0 OID 0)
-- Dependencies: 280
-- Name: presupuesto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('presupuesto_id_seq', 1, false);


--
-- TOC entry 4708 (class 0 OID 0)
-- Dependencies: 173
-- Name: producto_compra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('producto_compra_id_seq', 1, false);


--
-- TOC entry 4709 (class 0 OID 0)
-- Dependencies: 193
-- Name: producto_venta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('producto_venta_id_seq', 1, false);


--
-- TOC entry 4710 (class 0 OID 0)
-- Dependencies: 163
-- Name: proveedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('proveedor_id_seq', 2, true);


--
-- TOC entry 4711 (class 0 OID 0)
-- Dependencies: 391
-- Name: prueba_alargamiento_longitudinal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_alargamiento_longitudinal_id_seq', 1, false);


--
-- TOC entry 4712 (class 0 OID 0)
-- Dependencies: 395
-- Name: prueba_alargamiento_transversal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_alargamiento_transversal_id_seq', 1, false);


--
-- TOC entry 4713 (class 0 OID 0)
-- Dependencies: 397
-- Name: prueba_compresion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_compresion_id_seq', 1, false);


--
-- TOC entry 4714 (class 0 OID 0)
-- Dependencies: 375
-- Name: prueba_elongacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_elongacion_id_seq', 1, false);


--
-- TOC entry 4715 (class 0 OID 0)
-- Dependencies: 379
-- Name: prueba_encogimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_encogimiento_id_seq', 1, false);


--
-- TOC entry 4716 (class 0 OID 0)
-- Dependencies: 401
-- Name: prueba_espesor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_espesor_id_seq', 1, false);


--
-- TOC entry 4717 (class 0 OID 0)
-- Dependencies: 387
-- Name: prueba_gramaje_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_gramaje_id_seq', 1, false);


--
-- TOC entry 4718 (class 0 OID 0)
-- Dependencies: 409
-- Name: prueba_granza_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_granza_id_seq', 1, false);


--
-- TOC entry 4719 (class 0 OID 0)
-- Dependencies: 381
-- Name: prueba_grasa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_grasa_id_seq', 1, false);


--
-- TOC entry 4720 (class 0 OID 0)
-- Dependencies: 385
-- Name: prueba_humedad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_humedad_id_seq', 1, false);


--
-- TOC entry 4721 (class 0 OID 0)
-- Dependencies: 389
-- Name: prueba_longitudinal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_longitudinal_id_seq', 1, false);


--
-- TOC entry 4722 (class 0 OID 0)
-- Dependencies: 399
-- Name: prueba_perforacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_perforacion_id_seq', 1, false);


--
-- TOC entry 4723 (class 0 OID 0)
-- Dependencies: 403
-- Name: prueba_permeabilidad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_permeabilidad_id_seq', 1, false);


--
-- TOC entry 4724 (class 0 OID 0)
-- Dependencies: 407
-- Name: prueba_piramidal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_piramidal_id_seq', 1, false);


--
-- TOC entry 4725 (class 0 OID 0)
-- Dependencies: 405
-- Name: prueba_poros_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_poros_id_seq', 1, false);


--
-- TOC entry 4726 (class 0 OID 0)
-- Dependencies: 377
-- Name: prueba_rizo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_rizo_id_seq', 1, false);


--
-- TOC entry 4727 (class 0 OID 0)
-- Dependencies: 373
-- Name: prueba_tenacidad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_tenacidad_id_seq', 1, false);


--
-- TOC entry 4728 (class 0 OID 0)
-- Dependencies: 383
-- Name: prueba_titulo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_titulo_id_seq', 1, false);


--
-- TOC entry 4729 (class 0 OID 0)
-- Dependencies: 393
-- Name: prueba_transversal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('prueba_transversal_id_seq', 1, false);


--
-- TOC entry 4730 (class 0 OID 0)
-- Dependencies: 349
-- Name: recibo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('recibo_id_seq', 1, false);


--
-- TOC entry 4731 (class 0 OID 0)
-- Dependencies: 306
-- Name: rollo_c_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('rollo_c_id_seq', 1, false);


--
-- TOC entry 4732 (class 0 OID 0)
-- Dependencies: 302
-- Name: rollo_defectuoso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('rollo_defectuoso_id_seq', 1, false);


--
-- TOC entry 4733 (class 0 OID 0)
-- Dependencies: 300
-- Name: rollo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('rollo_id_seq', 1, false);


--
-- TOC entry 4734 (class 0 OID 0)
-- Dependencies: 322
-- Name: servicio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('servicio_id_seq', 1, false);


--
-- TOC entry 4735 (class 0 OID 0)
-- Dependencies: 335
-- Name: servicio_tomado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('servicio_tomado_id_seq', 1, false);


--
-- TOC entry 4736 (class 0 OID 0)
-- Dependencies: 196
-- Name: silo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('silo_id_seq', 1, false);


--
-- TOC entry 4737 (class 0 OID 0)
-- Dependencies: 226
-- Name: stock_almacen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('stock_almacen_id_seq', 1, false);


--
-- TOC entry 4738 (class 0 OID 0)
-- Dependencies: 441
-- Name: stock_especial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('stock_especial_id_seq', 1, false);


--
-- TOC entry 4739 (class 0 OID 0)
-- Dependencies: 455
-- Name: tarea_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('tarea_id_seq', 1, false);


--
-- TOC entry 4740 (class 0 OID 0)
-- Dependencies: 161
-- Name: tarifa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('tarifa_id_seq', 1, false);


--
-- TOC entry 4741 (class 0 OID 0)
-- Dependencies: 316
-- Name: ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('ticket_id_seq', 1, false);


--
-- TOC entry 4742 (class 0 OID 0)
-- Dependencies: 262
-- Name: tipo_de_incidencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('tipo_de_incidencia_id_seq', 1, false);


--
-- TOC entry 4743 (class 0 OID 0)
-- Dependencies: 171
-- Name: tipo_de_material_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('tipo_de_material_id_seq', 1, false);


--
-- TOC entry 4744 (class 0 OID 0)
-- Dependencies: 181
-- Name: tipo_material_bala_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('tipo_material_bala_id_seq', 1, false);


--
-- TOC entry 4745 (class 0 OID 0)
-- Dependencies: 331
-- Name: transporte_a_cuenta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('transporte_a_cuenta_id_seq', 1, false);


--
-- TOC entry 4746 (class 0 OID 0)
-- Dependencies: 165
-- Name: transportista_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('transportista_id_seq', 1, false);


--
-- TOC entry 4747 (class 0 OID 0)
-- Dependencies: 256
-- Name: turno_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('turno_id_seq', 1, false);


--
-- TOC entry 4748 (class 0 OID 0)
-- Dependencies: 230
-- Name: usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('usuario_id_seq', 1, false);


--
-- TOC entry 4749 (class 0 OID 0)
-- Dependencies: 254
-- Name: vacaciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('vacaciones_id_seq', 1, false);


--
-- TOC entry 4750 (class 0 OID 0)
-- Dependencies: 351
-- Name: vencimiento_cobro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('vencimiento_cobro_id_seq', 1, false);


--
-- TOC entry 4751 (class 0 OID 0)
-- Dependencies: 337
-- Name: vencimiento_pago_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('vencimiento_pago_id_seq', 1, false);


--
-- TOC entry 4752 (class 0 OID 0)
-- Dependencies: 415
-- Name: ventana_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uginn
--

SELECT pg_catalog.setval('ventana_id_seq', 1, false);


--
-- TOC entry 4479 (class 0 OID 46435)
-- Dependencies: 213 4603
-- Data for Name: almacen; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4506 (class 0 OID 46996)
-- Dependencies: 267 4603
-- Data for Name: contador; Type: TABLE DATA; Schema: public; Owner: uginn
--

INSERT INTO contador (id, prefijo, sufijo, contador) VALUES (1, '', '', 1);


--
-- TOC entry 4507 (class 0 OID 47009)
-- Dependencies: 269 4603
-- Data for Name: cuenta_origen; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4454 (class 0 OID 45846)
-- Dependencies: 164 4603
-- Data for Name: proveedor; Type: TABLE DATA; Schema: public; Owner: uginn
--

INSERT INTO proveedor (id, nombre, cif, direccion, pais, ciudad, provincia, cp, telefono, fax, contacto, observaciones, direccionfacturacion, paisfacturacion, ciudadfacturacion, provinciafacturacion, cpfacturacion, email, formadepago, documentodepago, vencimiento, diadepago, correoe, web, banco, swif, iban, cuenta, inhabilitado, motivo, iva, nombre_banco) VALUES (1, 'Empre, S. A.', 'A12345678', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '90 D.F.F.', 'Pagaré', '90 D.F.F.', '25', '', '', '', '', '', '', false, '', 0.209999999999999992, '');
INSERT INTO proveedor (id, nombre, cif, direccion, pais, ciudad, provincia, cp, telefono, fax, contacto, observaciones, direccionfacturacion, paisfacturacion, ciudadfacturacion, provinciafacturacion, cpfacturacion, email, formadepago, documentodepago, vencimiento, diadepago, correoe, web, banco, swif, iban, cuenta, inhabilitado, motivo, iva, nombre_banco) VALUES (2, 'Proveedor de prueba', 'PENDIENTE', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '120 D.F.F.', 'Pagaré', '120 D.F.F.', '25', '', '', '', '', '', '', false, '', 0.209999999999999992, '');


--
-- TOC entry 4453 (class 0 OID 45834)
-- Dependencies: 162 4603
-- Data for Name: tarifa; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4508 (class 0 OID 47027)
-- Dependencies: 271 4507 4454 4506 4453 4603
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: uginn
--

INSERT INTO cliente (id, tarifa_id, contador_id, telefono, nombre, cif, direccion, pais, ciudad, provincia, cp, iva, direccionfacturacion, paisfacturacion, ciudadfacturacion, provinciafacturacion, cpfacturacion, nombref, email, contacto, observaciones, vencimientos, formadepago, documentodepago, diadepago, inhabilitado, motivo, cliente_id, porcentaje, enviar_correo_albaran, enviar_correo_factura, enviar_correo_packing, fax, proveedor_id, cuenta_origen_id, riesgo_asegurado, riesgo_concedido, packing_list_con_codigo, facturar_con_albaran, copias_factura) VALUES (1, NULL, NULL, '', 'Empre, S. A.', 'A12345678', '', '', '', '', '', 0.209999999999999992, '', '', '', '', '', 'Empre, S. A.', '', '', '', '', '', '', '', false, '', NULL, 0, false, false, false, '', NULL, NULL, -1, -1, false, true, 0);
INSERT INTO cliente (id, tarifa_id, contador_id, telefono, nombre, cif, direccion, pais, ciudad, provincia, cp, iva, direccionfacturacion, paisfacturacion, ciudadfacturacion, provinciafacturacion, cpfacturacion, nombref, email, contacto, observaciones, vencimientos, formadepago, documentodepago, diadepago, inhabilitado, motivo, cliente_id, porcentaje, enviar_correo_albaran, enviar_correo_factura, enviar_correo_packing, fax, proveedor_id, cuenta_origen_id, riesgo_asegurado, riesgo_concedido, packing_list_con_codigo, facturar_con_albaran, copias_factura) VALUES (2, NULL, 1, '', 'Cliente de prueba', 'PENDIENTE', '', '', '', '', '', 0.209999999999999992, '', '', '', '', '', '', '', '', '', '180 D.F.F.', '180 D.F.F.', 'PAGARÉ A LA ORDEN', '25', false, '', NULL, 0, false, false, false, '', NULL, NULL, -1, -1, false, true, 0);


--
-- TOC entry 4553 (class 0 OID 48297)
-- Dependencies: 360 4603
-- Data for Name: factura_de_abono; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4511 (class 0 OID 47135)
-- Dependencies: 277 4603
-- Data for Name: obra; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4555 (class 0 OID 48350)
-- Dependencies: 364 4511 4479 4553 4508 4603
-- Data for Name: abono; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4599 (class 0 OID 49275)
-- Dependencies: 450 4603
-- Data for Name: estado; Type: TABLE DATA; Schema: public; Owner: uginn
--

INSERT INTO estado (id, descripcion, pendiente, observaciones) VALUES (1, 'No leída', true, '');
INSERT INTO estado (id, descripcion, pendiente, observaciones) VALUES (2, 'En espera', true, '');
INSERT INTO estado (id, descripcion, pendiente, observaciones) VALUES (3, 'Cerrada', false, '');


--
-- TOC entry 4529 (class 0 OID 47643)
-- Dependencies: 313 4511 4508 4603
-- Data for Name: factura_venta; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4600 (class 0 OID 49287)
-- Dependencies: 452 4599 4529 4603
-- Data for Name: alarma; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4557 (class 0 OID 48413)
-- Dependencies: 368 4603
-- Data for Name: albaran_de_entrada_de_abono; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4455 (class 0 OID 45887)
-- Dependencies: 166 4603
-- Data for Name: transportista; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4480 (class 0 OID 46456)
-- Dependencies: 215 4455 4479 4454 4603
-- Data for Name: albaran_entrada; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4456 (class 0 OID 45902)
-- Dependencies: 168 4603
-- Data for Name: destino; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4514 (class 0 OID 47239)
-- Dependencies: 283 4479 4479 4456 4508 4455 4603
-- Data for Name: albaran_salida; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4488 (class 0 OID 46628)
-- Dependencies: 231 4603
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: uginn
--

INSERT INTO usuario (id, usuario, passwd, nombre, cuenta, cpass, nivel, email, smtpserver, smtpuser, smtppassword, firma_total, firma_comercial, firma_director, firma_tecnico, firma_usuario, observaciones) VALUES (1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'Cuenta de administrador', 'informatica@geotexan.com', '', 0, 'informatica@geotexan.com', 'smtp.googlemail.com', 'informatica@geotexan.com', '', true, true, true, true, true, '');


--
-- TOC entry 4583 (class 0 OID 48882)
-- Dependencies: 420 4488 4603
-- Data for Name: alerta; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4515 (class 0 OID 47288)
-- Dependencies: 285 4603
-- Data for Name: lote; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4516 (class 0 OID 47310)
-- Dependencies: 287 4603
-- Data for Name: partida_carga; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4518 (class 0 OID 47356)
-- Dependencies: 291 4516 4515 4603
-- Data for Name: bala; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4525 (class 0 OID 47523)
-- Dependencies: 305 4603
-- Data for Name: bala_cable; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4519 (class 0 OID 47385)
-- Dependencies: 293 4603
-- Data for Name: lote_cem; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4474 (class 0 OID 46314)
-- Dependencies: 203 4603
-- Data for Name: partida_cem; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4475 (class 0 OID 46329)
-- Dependencies: 205 4474 4603
-- Data for Name: parte_de_produccion; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4520 (class 0 OID 47402)
-- Dependencies: 295 4475 4519 4603
-- Data for Name: bigbag; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4521 (class 0 OID 47431)
-- Dependencies: 297 4474 4603
-- Data for Name: pale; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4522 (class 0 OID 47452)
-- Dependencies: 299 4521 4603
-- Data for Name: caja; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4463 (class 0 OID 46042)
-- Dependencies: 182 4603
-- Data for Name: tipo_material_bala; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4464 (class 0 OID 46053)
-- Dependencies: 184 4463 4603
-- Data for Name: campos_especificos_bala; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4468 (class 0 OID 46192)
-- Dependencies: 192 4603
-- Data for Name: campos_especificos_especial; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4465 (class 0 OID 46075)
-- Dependencies: 186 4603
-- Data for Name: modelo_etiqueta; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4466 (class 0 OID 46086)
-- Dependencies: 188 4465 4603
-- Data for Name: campos_especificos_rollo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4460 (class 0 OID 45993)
-- Dependencies: 176 4603
-- Data for Name: formulacion; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4462 (class 0 OID 46025)
-- Dependencies: 180 4460 4603
-- Data for Name: linea_de_produccion; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4517 (class 0 OID 47325)
-- Dependencies: 289 4516 4603
-- Data for Name: partida; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4469 (class 0 OID 46207)
-- Dependencies: 194 4468 4466 4464 4462 4603
-- Data for Name: producto_venta; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4523 (class 0 OID 47472)
-- Dependencies: 301 4517 4603
-- Data for Name: rollo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4526 (class 0 OID 47543)
-- Dependencies: 307 4603
-- Data for Name: rollo_c; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4524 (class 0 OID 47497)
-- Dependencies: 303 4517 4603
-- Data for Name: rollo_defectuoso; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4527 (class 0 OID 47561)
-- Dependencies: 309 4522 4479 4526 4525 4524 4520 4514 4469 4475 4523 4518 4603
-- Data for Name: articulo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4478 (class 0 OID 46406)
-- Dependencies: 211 4462 4603
-- Data for Name: categoria_laboral; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4487 (class 0 OID 46612)
-- Dependencies: 229 4479 4603
-- Data for Name: centro_trabajo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4489 (class 0 OID 46656)
-- Dependencies: 233 4488 4487 4478 4603
-- Data for Name: empleado; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4492 (class 0 OID 46736)
-- Dependencies: 239 4603
-- Data for Name: motivo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4493 (class 0 OID 46753)
-- Dependencies: 241 4492 4489 4603
-- Data for Name: ausencia; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4494 (class 0 OID 46776)
-- Dependencies: 243 4489 4603
-- Data for Name: baja; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4497 (class 0 OID 46838)
-- Dependencies: 249 4462 4603
-- Data for Name: calendario_laboral; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4510 (class 0 OID 47118)
-- Dependencies: 275 4469 4603
-- Data for Name: campos_especificos; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4458 (class 0 OID 45953)
-- Dependencies: 172 4603
-- Data for Name: tipo_de_material; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4459 (class 0 OID 45964)
-- Dependencies: 174 4454 4458 4603
-- Data for Name: producto_compra; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4471 (class 0 OID 46258)
-- Dependencies: 197 4603
-- Data for Name: silo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4472 (class 0 OID 46271)
-- Dependencies: 199 4471 4459 4603
-- Data for Name: carga_silo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4601 (class 0 OID 49312)
-- Dependencies: 454 4603
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4551 (class 0 OID 48257)
-- Dependencies: 356 4603
-- Data for Name: confirming; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4550 (class 0 OID 48241)
-- Dependencies: 354 4603
-- Data for Name: pagare_cobro; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4530 (class 0 OID 47671)
-- Dependencies: 315 4508 4603
-- Data for Name: prefactura; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4554 (class 0 OID 48306)
-- Dependencies: 362 4551 4553 4508 4550 4530 4529 4603
-- Data for Name: cobro; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4490 (class 0 OID 46687)
-- Dependencies: 235 4489 4603
-- Data for Name: comercial; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4540 (class 0 OID 47972)
-- Dependencies: 334 4514 4530 4529 4508 4603
-- Data for Name: comision; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4476 (class 0 OID 46355)
-- Dependencies: 207 4471 4475 4459 4603
-- Data for Name: consumo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4461 (class 0 OID 46004)
-- Dependencies: 178 4460 4459 4603
-- Data for Name: consumo_adicional; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4470 (class 0 OID 46243)
-- Dependencies: 195 4461 4469 4603
-- Data for Name: consumo_adicional__producto_venta; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4595 (class 0 OID 49211)
-- Dependencies: 444 4603
-- Data for Name: contacto; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4502 (class 0 OID 46906)
-- Dependencies: 259 4489 4489 4489 4603
-- Data for Name: grupo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4588 (class 0 OID 49066)
-- Dependencies: 430 4489 4502 4603
-- Data for Name: control_horas; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4590 (class 0 OID 49128)
-- Dependencies: 434 4588 4462 4603
-- Data for Name: control_horas_mantenimiento; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4589 (class 0 OID 49109)
-- Dependencies: 432 4588 4462 4603
-- Data for Name: control_horas_produccion; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4509 (class 0 OID 47097)
-- Dependencies: 273 4508 4603
-- Data for Name: cuenta_bancaria_cliente; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4545 (class 0 OID 48091)
-- Dependencies: 344 4454 4603
-- Data for Name: cuenta_destino; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4584 (class 0 OID 48901)
-- Dependencies: 422 4603
-- Data for Name: datos_de_la_empresa; Type: TABLE DATA; Schema: public; Owner: uginn
--

INSERT INTO datos_de_la_empresa (id, nombre, cif, dirfacturacion, cpfacturacion, ciudadfacturacion, provinciafacturacion, direccion, cp, ciudad, provincia, telefono, fax, email, paisfacturacion, pais, telefonofacturacion, faxfacturacion, nombre_responsable_compras, telefono_responsable_compras, nombre_contacto, registro_mercantil, email_responsable_compras, logo, logo2, bvqi, nomalbaran2, diralbaran2, cpalbaran2, ciualbaran2, proalbaran2, telalbaran2, faxalbaran2, regalbaran2, irpf, es_sociedad, logoiso1, logoiso2, recargo_equivalencia, iva, ped_compra_texto_fijo, ped_compra_texto_editable, ped_compra_texto_editable_con_nivel1) VALUES (1, 'Empre, S. A.', 'A-12.345.678', 'P. E. Dirección De Facturación, n.º 1; 2-3', '99999', 'Ciudad', 'Provincia', 'C/ Calle, n.º 1', '99.999', 'Minas de Riotinto', 'Provincia', '900 123 456', '000 000 000', 'bogado@qinn.es', 'España', 'España', '034 999 999 999', '034 567 890 123', 'Nombre Responsable Compras', '600 666 999', 'Nombre Contacto', 'Inscrita en el Registro Mercantil de Sevilla, Tomo 3333 - Folio 101 - Hoja nº SE-55555 - C.I.F. A-12345678', 'informatica@geotexan.com', 'logo_nuevo.gif', 'logoComposan.gif', true, 'EMPRESA ASOCIADA, S. A.', 'Avda. Avenida n.º 1', '11111', 'Ciudad Albarán auxiliar', 'Provincia', '91 234 56 78', '99 999 99 99', 'CIF A-12345678 Reg. Mec. de Madrid, 11 de Julio de 1995. Tomo 8888, Sección 8º del Libro de Sociedades, Folio 00 Hoja M-111111, Insc. 1º', 0, true, 'iso9001_14001.jpg', 'iso9001_14001.jpg', false, 0.209999999999999992, 'ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.', 'ESTA MERCANCÍA SE DEBE ENTREGAR CON ALBARÁN Y ENVIARNOS COPIA DEL MISMO CON LA FIRMA Y SELLO DE RECIBIDO POR EL CLIENTE. ESTO ES CONDICIÓN IMPRESCINDIBLE PARA LA TRAMITACIÓN DE SU FACTURA.', 'PAGO A 120 DÍAS F.F. PAGO LOS 25.');


--
-- TOC entry 4477 (class 0 OID 46382)
-- Dependencies: 209 4475 4459 4603
-- Data for Name: descuento_de_material; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4535 (class 0 OID 47831)
-- Dependencies: 325 4454 4603
-- Data for Name: factura_compra; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4544 (class 0 OID 48075)
-- Dependencies: 342 4603
-- Data for Name: pagare_pago; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4457 (class 0 OID 45919)
-- Dependencies: 170 4454 4603
-- Data for Name: pedido_compra; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4512 (class 0 OID 47154)
-- Dependencies: 279 4511 4490 4453 4508 4603
-- Data for Name: pedido_venta; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4586 (class 0 OID 48967)
-- Dependencies: 426 4551 4454 4508 4489 4544 4535 4480 4457 4550 4530 4529 4514 4512 4603
-- Data for Name: documento; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4580 (class 0 OID 48832)
-- Dependencies: 414 4603
-- Data for Name: modulo; Type: TABLE DATA; Schema: public; Owner: uginn
--

INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (1, 'Administración', 'administracion.png', 'Administración');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (2, 'Comercial', 'comercial.png', 'Comercial');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (3, 'Almacén', 'almacen.png', 'Gestión de almacén');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (4, 'Laboratorio', 'laboratorio.png', 'Laboratorio');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (5, 'General', 'func_generales.png', 'Funciones generales');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (6, 'Consultas', 'costes.png', 'Costes e informes');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (7, 'Ayuda', 'doc_y_ayuda.png', 'Documentación y ayuda');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (8, 'Producción', 'produccion.png', 'Producción');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (9, 'DEBUG', 'debug.png', 'Utilidades de depuración para el administrador');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (10, 'RR.HH.', 'rrhh.png', 'Recursos humanos');
INSERT INTO modulo (id, nombre, icono, descripcion) VALUES (11, 'CRM', 'crm.png', 'Gestión de la relación con los clientes.');


--
-- TOC entry 4581 (class 0 OID 48843)
-- Dependencies: 416 4580 4603
-- Data for Name: ventana; Type: TABLE DATA; Schema: public; Owner: uginn
--

INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (1, 1, 'Facturas de compra', 'facturas_compra.py', 'FacturasDeEntrada', 'factura_compra.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (2, 1, 'Facturas de venta', 'facturas_venta.py', 'FacturasVenta', 'factura_venta.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (3, 1, 'Abonos sobre facturas de venta', 'abonos_venta.py', 'AbonosVenta', 'abonos_venta.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (4, 2, 'Pedidos de compra (a proveedores)', 'pedidos_de_compra.py', 'PedidosDeCompra', 'pedido.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (6, 2, 'Pedidos de venta (de clientes)', 'pedidos_de_venta.py', 'PedidosDeVenta', 'pedido.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (7, 2, 'Ver ventas sin pedido asignado', 'lineas_sin_pedido.py', 'LineasDeVentaSinPedido', 'sin_pedido.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (8, 3, 'Ver existencias de rollos en almacén', 'rollos_almacen.py', 'RollosAlmacen', 'rollos_en_almacen.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (9, 3, 'Listado de balas fabricadas', 'listado_balas.py', 'ListadoBalas', '');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (10, 3, 'Listado de rollos fabricados', 'listado_rollos.py', 'ListadoRollos', '');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (11, 3, 'Albaranes de entrada de material', 'albaranes_de_entrada.py', 'AlbaranesDeEntrada', 'albaran.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (12, 3, 'Albaranes de salida', 'albaranes_de_salida.py', 'AlbaranesDeSalida', 'albaran.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (53, 6, 'Consulta de albaranes de clientes', 'consulta_albaranes_clientes.py', 'ConsultaAlbaranesCliente', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (54, 6, 'Consulta de cobros', 'consulta_cobros.py', 'ConsultaCobros', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (22, 4, 'Asignar directamente resultados de laboratorio a lote de fibra. (No guarda histórico)', 'lab_resultados_lote.py', 'LabResultadosLote', '');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (23, 4, 'Buscar lotes con valores determinados', 'busca_lote.py', 'BuscaLote', 'buscar.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (56, 6, 'Consulta de pagos', 'consulta_pagos.py', 'ConsultaPagos', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (26, 5, 'Tipos de material de fibra', 'tipos_material_balas.py', 'TiposMaterialBala', 'tipos_de.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (27, 5, 'Gestión de usuarios', 'usuarios.py', 'Usuarios', 'usuarios.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (28, 5, 'Tipos de incidencia', 'tipos_incidencia.py', 'TiposIncidencia', 'tipos_de.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (29, 5, 'Proveedores', 'proveedores.py', 'Proveedores', 'proveedores.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (30, 5, 'Contadores para facturas de clientes', 'contadores.py', 'Contadores', 'contadores.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (32, 5, 'Catálogo de productos de venta (fibra)', 'productos_de_venta_balas.py', 'ProductosDeVentaBalas', 'catalogo.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (89, 6, 'Pedidos pendientes de servir', 'consulta_pendientes_servir.py', 'PendientesServir', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (35, 5, 'Productos de compra', 'productos_compra.py', 'ProductosCompra', 'catalogo.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (36, 5, 'Tipos de material de compra', 'tipos_material.py', 'TiposMaterial', 'tipos_de.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (37, 5, 'Catálogo de productos de venta (geotextiles)', 'productos_de_venta_rollos.py', 'ProductosDeVentaRollos', 'catalogo.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (38, 6, 'Existencias de materiales en almacén', 'consulta_existencias.py', 'ConsultaExistencias', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (39, 6, 'Listado de albaranes facturados', 'consulta_albaranesFacturados.py', 'ConsultaAlbaranesFacturados', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (40, 6, 'Ver productos bajo mínimos', 'consulta_bajoMinimos.py', 'ConsultaBajoMinimos', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (41, 6, 'Listado de albaranes pendientes de facturar', 'consulta_albaranesPorFacturar.py', 'ConsultaAlbaranesPorFacturar', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (42, 6, 'Listado de compras', 'consulta_compras.py', 'ConsultaCompras', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (43, 6, 'Listado de ventas', 'consulta_ventas.py', 'ConsultaVentas', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (44, 7, 'Acerca de...', 'acerca_de.py', 'acerca_de', 'acerca.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (90, 6, 'Pedidos pendientes de recibir', 'consulta_pendientes_recibir.py', 'PendientesRecibir', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (99, 4, 'Resultados fibra de cemento', 'resultados_cemento.py', 'ResultadosFibra', 'labo_fibra.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (49, 4, 'Muestras pendientes de analizar', 'muestras_pendientes.py', 'MuestrasPendientes', 'estrella.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (57, 6, 'Consulta de pedidos de clientes', 'consulta_pedidos_clientes.py', 'ConsultaPedidosCliente', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (5, 2, 'Tarifas de precios', 'tarifas_de_precios.py', 'TarifasDePrecios', 'tarifa.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (59, 6, 'Consulta de vencimientos de pago', 'consulta_vencimientos_pago.py', 'ConsultaVencimientosPagos', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (45, 7, 'Ayuda on-line (mensajería instantánea)', 'gajim.py', 'gajim', 'gajim.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (33, 5, 'Cartera de clientes', 'clientes.py', 'Clientes', 'clientes.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (50, 4, 'Buscar partidas por características', 'busca_partida.py', 'BuscaPartida', 'buscar.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (61, 5, 'Mis datos de usuario', 'ventana_usuario.py', 'Usuarios', 'usuarios.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (62, 4, 'Resultados fibra', 'resultados_fibra.py', 'ResultadosFibra', 'labo_fibra.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (63, 4, 'Resultados geotextiles', 'resultados_geotextiles.py', 'ResultadosGeotextiles', 'labo_rollos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (16, 4, 'Resultados de fluidez de granza (MFI)', 'resultados_fluidez.py', 'ResultadosFluidez', 'labo_mp.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (65, 8, 'Horas de trabajo por empleado', 'horas_trabajadas.py', 'HorasTrabajadas', 'reloj.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (64, 8, 'Partes pendientes de revisar', 'partes_no_bloqueados.py', 'PartesNoBloqueados', 'candado.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (91, 6, 'Consumos', 'consulta_consumo.py', 'ConsultaConsumo', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (58, 6, 'Consulta de vencimientos de cobro', 'consulta_vencimientos_cobro.py', 'ConsultaVencimientosCobros', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (87, 1, 'Cheques y pagarés de pago', 'pagares_pagos.py', 'PagaresPagos', 'money.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (69, 1, 'Efectos de cobro', 'pagares_cobros.py', 'PagaresCobros', 'money.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (47, 8, 'Ver productividad global', 'consulta_productividad.py', 'ConsultaProductividad', 'productividad.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (78, 6, 'Consulta partidas por producto', 'consulta_partidas_por_producto.py', 'ConsultaPartidasPorProducto', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (92, 6, 'Productos terminados', 'consulta_producido.py', 'ConsultaProducido', 'grafs.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (77, 6, 'Consulta lotes por producto', 'consulta_lotes_por_producto.py', 'ConsultaLotesPorProducto', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (34, 10, 'Empleados', 'empleados.py', 'Empleados', 'empleados.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (76, 6, 'Imprimir existencias de geotextiles', 'consulta_existenciasRollos.py', 'ConsultaExistencias', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (75, 6, 'Imprimir existencias de fibra', 'consulta_existenciasBalas.py', 'ConsultaExistencias', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (74, 3, 'Valoración de entradas en almacén', 'consulta_entradas_almacen.py', 'ConsultaEntradasAlmacen', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (70, 1, 'Ausencias', 'ausencias.py', 'Ausencias', 'ausencias.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (86, 1, 'Cálculo de primas y nóminas', 'nominas.py', 'Nominas', 'nominas.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (71, 8, 'Calendarios laborales', 'calendario_laboral.py', 'CalendarioLaboral', 'calendario.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (79, 8, 'Formulación fibra', 'formulacion_fibra.py', 'FormulacionFibra', 'formulacion.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (80, 8, 'Formulación geotextiles', 'formulacion_geotextiles.py', 'FormulacionGeotextiles', 'formulacion.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (83, 1, 'Importar datos de LOGIC', 'importar_logic.py', 'ImportarLogic', 'logic.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (84, 1, 'Mostrar datos de LOGIC existentes', 'mostrar_datos_logic.py', 'MostrarDatosLogic', 'logic.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (73, 5, 'Configuración de centros de trabajo', 'centros_de_trabajo.py', 'CentrosDeTrabajo', 'catcent.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (81, 5, 'Configuración de grupos de trabajo', 'grupos.py', 'Grupos', 'catcent.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (67, 8, 'Partes de trabajo (no producción)', 'partes_de_trabajo.py', 'PartesDeTrabajo', 'partestrabajo.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (88, 9, 'Trazabilidad interna (DEBUG) - Sólo para el administrador', 'trazabilidad.py', 'Trazabilidad', 'trazabilidad.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (66, 2, 'Trazabilidad de productos finales', 'trazabilidad_articulos.py', 'TrazabilidadArticulos', 'trazabilidad.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (82, 8, 'Horas trabajadas por día', 'horas_trabajadas_dia.py', 'HorasTrabajadasDia', 'reloj.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (85, 5, 'Configurar motivos de ausencia', 'motivos_ausencia.py', 'MotivosAusencia', 'motivos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (68, 1, 'Vencimientos pendientes por cliente', 'vencimientos_pendientes_por_cliente.py', 'VencimientosPendientesPorCliente', 'pendiente.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (20, NULL, '01.- Resultados de resistencia a alargamiento longitudinal', 'resultados_longitudinal.py', 'ResultadosLongitudinal', 'labo_rollos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (93, 8, 'Consumo de fibra por partida', 'consumo_balas_partida.py', 'ConsumoBalasPartida', '');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (13, NULL, '04.- Resultados de perforación (cono)', 'resultados_perforacion.py', 'ResultadosPerforacion', 'labo_rollos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (18, NULL, '06.- Resultados de permeabilidad', 'resultados_permeabilidad.py', 'ResultadosPermeabilidad', 'labo_rollos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (51, NULL, '07.- Resultados de apertura de poros', 'resultados_poros.py', 'ResultadosPoros', 'labo_rollos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (14, NULL, '02.- Resultados de resistencia a alargamiento transversal', 'resultados_transversal.py', 'ResultadosTransversal', 'labo_rollos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (52, NULL, '05.- Resultados de espesor', 'resultados_espesor.py', 'ResultadosEspesor', 'labo_rollos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (21, NULL, '03.- Resultados de compresión (CBR)', 'resultados_compresion.py', 'ResultadosCompresion', 'labo_rollos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (17, NULL, '09.- Resultados de tenacidad sobre fibra', 'resultados_tenacidad.py', 'ResultadosTenacidad', 'labo_fibra.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (15, NULL, '10.- Resultados de elongación sobre fibra', 'resultados_elongacion.py', 'ResultadosElongacion', 'labo_fibra.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (25, NULL, '11.- Resultados encogimiento sobre fibra', 'resultados_encogimiento.py', 'ResultadosEncogimiento', 'labo_fibra.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (19, NULL, '12.- Resultados de grasa sobre fibra', 'resultados_grasa.py', 'ResultadosGrasa', 'labo_fibra.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (24, NULL, '13.- Resultados de rizo sobre fibra', 'resultados_rizo.py', 'ResultadosRizo', 'labo_fibra.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (60, NULL, '08.- Resultados de título (DTEX)', 'resultados_titulo.py', 'ResultadosTitulo', 'labo_fibra.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (94, 1, 'Facturas pendientes de revisar e imprimir', 'facturas_no_bloqueadas.py', 'FacturasNoBloqueadas', 'facturas_no_bloqueadas.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (98, 3, 'Historial de productos de compra', 'historico_existencias_compra.py', 'HistoricoExistenciasCompra', 'globe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (97, 6, 'Consumo de fibra de la línea de geotextiles', 'consumo_fibra_por_partida_gtx.py', 'ConsumoFibraPorPartidaGtx', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (95, 3, 'Estado de silos', 'silos.py', 'Silos', 'silos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (96, 3, 'Histórico de existencias de productos de venta', 'historico_existencias.py', 'HistoricoExistencias', 'globe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (46, 8, 'Partes de fabricación de fibra', 'partes_de_fabricacion_balas.py', 'PartesDeFabricacionBalas', 'balas.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (48, 8, 'Partes de fabricación de geotextiles', 'partes_de_fabricacion_rollos.py', 'PartesDeFabricacionRollos', 'rollos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (100, 6, 'Resumen totales geotextiles por mes', 'consulta_totales_geotextiles.py', 'ConsultaTotalesGeotextiles', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (101, 6, 'Facturación por cliente y fecha', 'facturacion_por_cliente_y_fechas.py', 'FacturacionPorClienteYFechas', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (102, 9, 'Visor del log', 'logviewer.py', 'LogViewer', 'trazabilidad.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (55, 6, 'Consulta incidencias en líneas de producción', 'consulta_incidencias.py', 'ConsultaIncidencias', 'grafs.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (104, 1, 'Cuentas bancarias de proveedores', 'cuentas_destino.py', 'CuentasDestino', 'money.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (103, 1, 'Cuentas bancarias de la empresa', 'cuentas_origen.py', 'CuentasOrigen', 'money.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (105, 1, 'Pago por transferencia', 'transferencias.py', 'Transferencias', 'dollars.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (106, 1, 'Facturas de compra pendientes de aprobación', 'consulta_pendientes_vto_bueno.py', 'ConsultaPendientesVtoBueno', 'firma.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (107, 5, 'Productos de venta «especiales»', 'productos_de_venta_especial.py', 'ProductosDeVentaEspecial', 'catalogo.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (108, 2, 'Presupuestos a clientes', 'presupuestos.py', 'Presupuestos', 'presupuesto.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (109, 6, 'Informe de marcado CE', 'consulta_marcado_ce.py', 'ConsultaMarcadoCE', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (110, 6, 'Resumen global de producción, ventas y consumos', 'consulta_global.py', 'ConsultaGlobal', 'hojacalc.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (111, 8, 'Balas de fibra para reciclar', 'balas_cable.py', 'BalasCable', 'balascable.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (112, 6, 'Salidas de almacén agrupadas por producto', 'consulta_ventas_por_producto.py', 'ConsultaVentasPorProducto', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (113, 9, 'Pruebas de coherencia de datos', 'checklist_window.py', 'pruebas_periodicas', 'trazabilidad.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (114, 4, 'Búsqueda múltiple de rollos', 'rollos_procesados_por_lote.py', 'RollosProcesadosPorLote', '');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (115, 3, 'Albaranes de entrada de repuestos', 'albaranes_de_entrada_repuestos.py', 'AlbaranesDeEntradaRepuestos', 'albaran.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (116, 3, 'Albaranes de salida de repuestos', 'albaranes_de_salida_repuestos.py', 'AlbaranesDeSalidaRepuestos', 'albaran.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (117, 3, 'Listado de repuestos', 'consulta_repuestos.py', 'ConsultaRepuestos', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (118, 3, 'Listado de rollos defectuosos', 'listado_rollos_defectuosos.py', 'ListadoRollosDefectuosos', '');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (119, 1, 'IVA devengado y soportado', 'iva.py', 'IVA', 'aeat.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (120, 1, 'Datos declaración anual operaciones con terceras personas (347)', 'modelo_347.py', 'Modelo347', 'aeat.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (121, 8, 'Geotextiles C', 'rollos_c.py', 'RollosC', 'rollos_c.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (122, 10, 'Control diario de horas de personal', 'control_personal.py', 'ControlPersonal', '');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (123, 10, 'Resumen de horas por empleado y día', 'consulta_control_horas.py', 'ConsultaControlHoras', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (124, 10, 'Resumen horas y costes por línea y empleado', 'consulta_mensual_nominas.py', 'ConsultaMensualNominas', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (72, 10, 'Configuración de categorías laborales', 'categorias_laborales.py', 'CategoriasLaborales', 'catcent.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (125, 3, 'Existencias por almacén', 'consulta_existencias_por_almacen.py', 'ConsultaExistenciasPorAlmacen', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (126, 6, 'Facturas sin documento de pago', 'consulta_facturas_sin_doc_pago.py', 'ConsultaFacturasSinDocumentoDePago', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (127, 8, 'Partes de producción línea de envasado', 'partes_de_fabricacion_bolsas.py', 'PartesDeFabricacionBolsas', 'cemento.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (128, 11, 'Seguimiento de facturas sin documento de pago', 'crm_seguimiento_impagos.py', 'CRM_SeguimientoImpagos', 'impagos.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (129, 11, 'Detalles de factura de venta', 'crm_detalles_factura.py', 'CRM_DetallesFactura', 'lupa_detalles.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (130, 1, 'Confirming', 'confirmings.py', 'Confirmings', 'money_blue.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (131, 8, 'Formulacion línea de embolsado', 'formulacion_bolsas.py', 'FormulacionBolsaCemento', 'formulacion.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (133, 1, 'Libro de facturas', 'consulta_libro_iva.py', 'ConsultaLibroIVA', 'aeat.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (132, 4, 'Certificado de calidad por albarán', 'certificado_calidad.py', 'CertificadoCalidad', 'estrella.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (134, 6, 'Imprimir existencias de fibra embolsada', 'consulta_existenciasBolsas.py', 'ConsultaExistenciasBolsas', 'informe.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (31, 5, 'Catálogo de productos de venta (comercializados)', 'productos_de_venta_rollos_geocompuestos.py', 'ProductosDeVentaRollosGeocompuestos', 'catalogo.png');
INSERT INTO ventana (id, modulo_id, descripcion, fichero, clase, icono) VALUES (135, 6, 'Consulta de pagos realizados', 'consulta_pagos_realizados.py', 'ConsultaVencimientosPagados', 'informe.png');


--
-- TOC entry 4587 (class 0 OID 49046)
-- Dependencies: 428 4581 4488 4603
-- Data for Name: estadistica; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4552 (class 0 OID 48273)
-- Dependencies: 358 4530 4529 4603
-- Data for Name: estimacion_cobro; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4547 (class 0 OID 48159)
-- Dependencies: 348 4535 4603
-- Data for Name: estimacion_pago; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4498 (class 0 OID 46856)
-- Dependencies: 251 4497 4603
-- Data for Name: festivo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4499 (class 0 OID 46870)
-- Dependencies: 253 4603
-- Data for Name: festivo_generico; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4481 (class 0 OID 46485)
-- Dependencies: 217 4479 4469 4603
-- Data for Name: historial_existencias; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4482 (class 0 OID 46506)
-- Dependencies: 219 4479 4469 4603
-- Data for Name: historial_existencias_a; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4483 (class 0 OID 46527)
-- Dependencies: 221 4479 4469 4603
-- Data for Name: historial_existencias_b; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4484 (class 0 OID 46548)
-- Dependencies: 223 4479 4469 4603
-- Data for Name: historial_existencias_c; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4485 (class 0 OID 46569)
-- Dependencies: 225 4479 4459 4603
-- Data for Name: historial_existencias_compra; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4592 (class 0 OID 49161)
-- Dependencies: 438 4581 4488 4603
-- Data for Name: lista_objetos_recientes; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4593 (class 0 OID 49179)
-- Dependencies: 440 4592 4603
-- Data for Name: id_reciente; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4504 (class 0 OID 46961)
-- Dependencies: 263 4603
-- Data for Name: tipo_de_incidencia; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4505 (class 0 OID 46972)
-- Dependencies: 265 4475 4504 4603
-- Data for Name: incidencia; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4501 (class 0 OID 46892)
-- Dependencies: 257 4603
-- Data for Name: turno; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4503 (class 0 OID 46933)
-- Dependencies: 261 4502 4497 4501 4603
-- Data for Name: laborable; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4531 (class 0 OID 47694)
-- Dependencies: 317 4603
-- Data for Name: ticket; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4532 (class 0 OID 47703)
-- Dependencies: 319 4531 4459 4530 4529 4514 4512 4469 4603
-- Data for Name: linea_de_venta; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4513 (class 0 OID 47203)
-- Dependencies: 281 4490 4508 4603
-- Data for Name: presupuesto; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4534 (class 0 OID 47792)
-- Dependencies: 323 4513 4512 4514 4530 4529 4603
-- Data for Name: servicio; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4556 (class 0 OID 48384)
-- Dependencies: 366 4534 4555 4532 4603
-- Data for Name: linea_de_abono; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4536 (class 0 OID 47862)
-- Dependencies: 327 4472 4471 4459 4535 4480 4457 4603
-- Data for Name: linea_de_compra; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4558 (class 0 OID 48427)
-- Dependencies: 370 4514 4557 4527 4555 4603
-- Data for Name: linea_de_devolucion; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4528 (class 0 OID 47625)
-- Dependencies: 311 4527 4514 4603
-- Data for Name: linea_de_movimiento; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4533 (class 0 OID 47755)
-- Dependencies: 321 4513 4459 4512 4469 4603
-- Data for Name: linea_de_pedido; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4537 (class 0 OID 47907)
-- Dependencies: 329 4457 4459 4603
-- Data for Name: linea_de_pedido_de_compra; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4538 (class 0 OID 47932)
-- Dependencies: 330 4536 4537 4603
-- Data for Name: linea_de_pedido_de_compra__linea_de_compra; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4543 (class 0 OID 48059)
-- Dependencies: 340 4603
-- Data for Name: logic_movimientos; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4467 (class 0 OID 46144)
-- Dependencies: 190 4466 4603
-- Data for Name: marcado_ce; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4579 (class 0 OID 48802)
-- Dependencies: 412 4519 4517 4515 4603
-- Data for Name: muestra; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4491 (class 0 OID 46708)
-- Dependencies: 237 4489 4603
-- Data for Name: nomina; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4598 (class 0 OID 49256)
-- Dependencies: 448 4529 4603
-- Data for Name: nota; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4596 (class 0 OID 49228)
-- Dependencies: 445 4508 4511 4603
-- Data for Name: obra__cliente; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4597 (class 0 OID 49241)
-- Dependencies: 446 4595 4511 4603
-- Data for Name: obra__contacto; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4585 (class 0 OID 48954)
-- Dependencies: 424 4603
-- Data for Name: observaciones_nominas; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4591 (class 0 OID 49147)
-- Dependencies: 436 4489 4603
-- Data for Name: orden_empleados; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4546 (class 0 OID 48114)
-- Dependencies: 346 4545 4507 4454 4544 4543 4535 4603
-- Data for Name: pago; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4559 (class 0 OID 48460)
-- Dependencies: 372 4530 4529 4553 4603
-- Data for Name: pago_de_abono; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4495 (class 0 OID 46795)
-- Dependencies: 245 4475 4489 4603
-- Data for Name: parte_de_produccion_empleado; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4496 (class 0 OID 46814)
-- Dependencies: 247 4487 4489 4603
-- Data for Name: parte_de_trabajo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4582 (class 0 OID 48860)
-- Dependencies: 418 4581 4488 4603
-- Data for Name: permiso; Type: TABLE DATA; Schema: public; Owner: uginn
--

INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (22, 1, 6, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (54, 1, 30, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (23, 1, 7, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (24, 1, 5, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (55, 1, 32, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (25, 1, 66, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (75, 1, 43, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (26, 1, 108, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (56, 1, 35, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (41, 1, 22, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (42, 1, 23, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (57, 1, 36, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (43, 1, 99, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (76, 1, 90, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (44, 1, 49, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (58, 1, 37, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (45, 1, 50, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (46, 1, 62, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (59, 1, 33, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (47, 1, 63, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (48, 1, 16, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (60, 1, 61, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (49, 1, 114, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (77, 1, 57, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (50, 1, 132, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (61, 1, 73, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (62, 1, 81, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (63, 1, 85, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (64, 1, 107, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (78, 1, 59, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (27, 1, 8, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (65, 1, 31, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (28, 1, 9, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (29, 1, 10, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (30, 1, 11, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (31, 1, 12, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (32, 1, 74, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (2, 1, 1, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (3, 1, 2, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (33, 1, 98, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (4, 1, 3, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (5, 1, 87, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (34, 1, 95, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (6, 1, 69, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (7, 1, 70, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (35, 1, 96, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (8, 1, 86, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (79, 1, 91, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (9, 1, 83, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (36, 1, 115, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (10, 1, 84, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (11, 1, 68, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (37, 1, 116, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (12, 1, 94, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (120, 1, 72, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (13, 1, 104, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (38, 1, 117, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (14, 1, 103, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (15, 1, 105, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (39, 1, 118, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (16, 1, 106, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (17, 1, 119, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (40, 1, 125, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (18, 1, 120, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (19, 1, 130, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (20, 1, 133, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (80, 1, 58, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (81, 1, 78, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (82, 1, 92, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (83, 1, 77, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (21, 1, 4, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (84, 1, 76, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (85, 1, 75, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (113, 1, 88, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (86, 1, 97, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (114, 1, 102, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (87, 1, 100, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (98, 1, 65, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (88, 1, 101, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (99, 1, 64, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (89, 1, 55, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (115, 1, 113, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (90, 1, 109, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (100, 1, 47, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (91, 1, 110, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (121, 1, 128, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (92, 1, 112, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (101, 1, 71, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (93, 1, 126, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (51, 1, 26, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (1, 1, 27, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (52, 1, 28, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (53, 1, 29, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (122, 1, 129, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (94, 1, 134, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (102, 1, 79, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (95, 1, 135, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (103, 1, 80, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (104, 1, 67, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (105, 1, 82, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (96, 1, 44, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (106, 1, 93, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (97, 1, 45, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (66, 1, 53, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (67, 1, 54, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (68, 1, 56, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (69, 1, 89, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (70, 1, 38, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (71, 1, 39, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (72, 1, 40, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (73, 1, 41, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (74, 1, 42, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (116, 1, 34, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (107, 1, 46, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (108, 1, 48, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (117, 1, 122, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (109, 1, 111, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (110, 1, 121, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (118, 1, 123, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (111, 1, 127, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (112, 1, 131, true, true, true, true);
INSERT INTO permiso (id, usuario_id, ventana_id, permiso, lectura, escritura, nuevo) VALUES (119, 1, 124, true, true, true, true);


--
-- TOC entry 4473 (class 0 OID 46290)
-- Dependencies: 201 4459 4453 4469 4603
-- Data for Name: precio; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4569 (class 0 OID 48645)
-- Dependencies: 392 4517 4603
-- Data for Name: prueba_alargamiento_longitudinal; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4571 (class 0 OID 48675)
-- Dependencies: 396 4517 4603
-- Data for Name: prueba_alargamiento_transversal; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4572 (class 0 OID 48690)
-- Dependencies: 398 4517 4603
-- Data for Name: prueba_compresion; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4561 (class 0 OID 48505)
-- Dependencies: 376 4519 4515 4603
-- Data for Name: prueba_elongacion; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4563 (class 0 OID 48540)
-- Dependencies: 380 4519 4515 4603
-- Data for Name: prueba_encogimiento; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4574 (class 0 OID 48720)
-- Dependencies: 402 4517 4603
-- Data for Name: prueba_espesor; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4567 (class 0 OID 48615)
-- Dependencies: 388 4517 4603
-- Data for Name: prueba_gramaje; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4578 (class 0 OID 48780)
-- Dependencies: 410 4459 4603
-- Data for Name: prueba_granza; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4564 (class 0 OID 48560)
-- Dependencies: 382 4519 4515 4603
-- Data for Name: prueba_grasa; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4566 (class 0 OID 48600)
-- Dependencies: 386 4519 4603
-- Data for Name: prueba_humedad; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4568 (class 0 OID 48630)
-- Dependencies: 390 4517 4603
-- Data for Name: prueba_longitudinal; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4573 (class 0 OID 48705)
-- Dependencies: 400 4517 4603
-- Data for Name: prueba_perforacion; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4575 (class 0 OID 48735)
-- Dependencies: 404 4517 4603
-- Data for Name: prueba_permeabilidad; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4577 (class 0 OID 48765)
-- Dependencies: 408 4517 4603
-- Data for Name: prueba_piramidal; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4576 (class 0 OID 48750)
-- Dependencies: 406 4517 4603
-- Data for Name: prueba_poros; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4562 (class 0 OID 48525)
-- Dependencies: 378 4515 4603
-- Data for Name: prueba_rizo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4560 (class 0 OID 48485)
-- Dependencies: 374 4519 4515 4603
-- Data for Name: prueba_tenacidad; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4565 (class 0 OID 48580)
-- Dependencies: 384 4519 4515 4603
-- Data for Name: prueba_titulo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4570 (class 0 OID 48660)
-- Dependencies: 394 4517 4603
-- Data for Name: prueba_transversal; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4548 (class 0 OID 48178)
-- Dependencies: 350 4509 4507 4603
-- Data for Name: recibo; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4539 (class 0 OID 47947)
-- Dependencies: 332 4454 4514 4603
-- Data for Name: transporte_a_cuenta; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4541 (class 0 OID 48008)
-- Dependencies: 336 4539 4540 4535 4603
-- Data for Name: servicio_tomado; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4486 (class 0 OID 46593)
-- Dependencies: 227 4459 4479 4603
-- Data for Name: stock_almacen; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4594 (class 0 OID 49192)
-- Dependencies: 442 4468 4479 4603
-- Data for Name: stock_especial; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4602 (class 0 OID 49324)
-- Dependencies: 456 4601 4529 4603
-- Data for Name: tarea; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4500 (class 0 OID 46878)
-- Dependencies: 255 4497 4603
-- Data for Name: vacaciones; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4549 (class 0 OID 48207)
-- Dependencies: 352 4548 4507 4530 4529 4603
-- Data for Name: vencimiento_cobro; Type: TABLE DATA; Schema: public; Owner: uginn
--



--
-- TOC entry 4542 (class 0 OID 48039)
-- Dependencies: 338 4535 4603
-- Data for Name: vencimiento_pago; Type: TABLE DATA; Schema: public; Owner: uginn
--



-- Completed on 2012-11-05 14:59:01 CET

--
-- PostgreSQL database dump complete
--

