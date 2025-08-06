-- Cria o usuário 'rangeradmin' se não existir
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'rangeradmin') THEN
      CREATE USER rangeradmin WITH CREATEDB LOGIN PASSWORD 'rangeradmin';
   END IF;
END
$$;

-- Cria o banco 'ranger' com dono 'rangeradmin' se não existir (fora do bloco DO)
CREATE DATABASE ranger OWNER rangeradmin;

-- Conecta ao banco ranger
\c ranger

-- Garante permissões no schema public
GRANT ALL PRIVILEGES ON SCHEMA public TO rangeradmin;

-- Garante permissões nas tabelas existentes
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rangeradmin;

-- Garante permissões nas sequências existentes
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO rangeradmin;

-- Garante que futuras tabelas e sequências também terão permissões
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO rangeradmin;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO rangeradmin;