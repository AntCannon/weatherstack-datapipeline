\getenv airflow_password AIRFLOW_DB_PASSWORD


SELECT 'CREATE ROLE airflow LOGIN'
WHERE NOT EXISTS (
  SELECT 1 FROM pg_roles WHERE rolname = 'airflow'
)
\gexec


ALTER ROLE airflow
    WITH LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION
    NOBYPASSRLS
    PASSWORD :'airflow_password';


SELECT 'CREATE DATABASE airflowdb OWNER airflow'
WHERE NOT EXISTS (
    SELECT 1 FROM pg_database WHERE datname = 'airflowdb'
)
\gexec


ALTER DATABASE airflowdb OWNER TO airflow;
REVOKE ALL ON DATABASE airflowdb FROM PUBLIC;


\connect airflowdb

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE, CREATE ON SCHEMA public TO airflow;