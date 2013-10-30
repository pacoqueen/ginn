ALTER TABLE presupuesto ADD COLUMN bloqueado BOOLEAN DEFAULT FALSE;
ALTER TABLE presupuesto ADD COLUMN rechazado BOOLEAN DEFAULT FALSE; 
ALTER TABLE presupuesto ADD COLUMN motivo TEXT DEFAULT ''; 
ALTER TABLE presupuesto ADD COLUMN cred_apertura BOOLEAN DEFAULT FALSE;
ALTER TABLE presupuesto ADD COLUMN cred_aumento BOOLEAN DEFAULT FALSE;
ALTER TABLE presupuesto ADD COLUMN cred_solicitud BOOLEAN DEFAULT FALSE;
ALTER TABLE presupuesto ADD COLUMN cred_ute TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_licitador TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_dirfiscal TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_cpfiscal TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_telefonofiscal TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_contactofiscal TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_poblacionfiscal TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_faxfiscal TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_provinciafiscal TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_emailfiscal TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_movilfiscal TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_telefonocontratos TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_emailcontratos TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_dircontratos TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_cpcontratos TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_provinciacontratos TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_contactocontratos TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_poblacioncontratos TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_movilcontratos TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_dirobra TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_cpobra TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_provinciaobra TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_contactoobra TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_poblacionobra TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_movilobra TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_entidad TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_oficina TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_digitocontrol TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_numcuenta TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_fdp TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_diapago1 TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_diapago2 TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_diapago3 TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_credsolicitado FLOAT DEFAULT NULL;
ALTER TABLE presupuesto ADD COLUMN cred_vb_nombrecomercial TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_vb_nombreadmon TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_asegurado FLOAT DEFAULT NULL;
ALTER TABLE presupuesto ADD COLUMN cred_fechaasegurado DATE DEFAULT NULL;
ALTER TABLE presupuesto ADD COLUMN cred_concedido FLOAT DEFAULT NULL;
ALTER TABLE presupuesto ADD COLUMN cred_fechaconcedido DATE DEFAULT NULL;
ALTER TABLE presupuesto ADD COLUMN cred_fecha DATE DEFAULT NULL;
ALTER TABLE presupuesto ADD COLUMN cred_entidades TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_observaciones TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_veces_solicitado INT DEFAULT 0;
ALTER TABLE presupuesto ADD COLUMN cred_motivo_rechazo TEXT DEFAULT '';
ALTER TABLE presupuesto ADD COLUMN cred_usuario_id INT REFERENCES usuario;
ALTER TABLE presupuesto ADD COLUMN cred_condiciones TEXT DEFAULT ''; 

CREATE TABLE zona(
    id SERIAL PRIMARY KEY, 
    nombre TEXT DEFAULT ''
);
CREATE TABLE area(
    id SERIAL PRIMARY KEY, 
    zona_id INT REFERENCES zona DEFAULT NULL, 
    nombre TEXT DEFAULT ''
);
ALTER TABLE comercial ADD COLUMN zona_id INT REFERENCES zona DEFAULT NULL; 
