#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import time
import json
from datetime import datetime
from faker import Faker
import subprocess

# Caminhos
SCRIPT_DIR = '/home/deploy/kafka-druid-pipeline/automatic_data_ingestion'
LOG_DIR = os.path.join(SCRIPT_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

fake = Faker('pt_BR')

# Nome do container Docker
DOCKER_CONTAINER = "postgres"
DB_USER = "druid"

def log_info(message):
    _log('execution.log', message)

def log_error(message):
    _log('error.log', message)

def _log(filename, message):
    filepath = os.path.join(LOG_DIR, filename)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(filepath, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def generate_inscricao_tecnica():
    base = random.randint(100000000, 999999999)
    dv = random.randint(0, 9)
    return int(f"{base}{dv}")

def generate_matricula():
    return random.randint(100000000, 999999999)

def generate_geometria(lat, lng):
    offset = random.uniform(0.0001, 0.0005)
    return {
        "type": "Polygon",
        "coordinates": [[
            [lng, lat],
            [lng + offset, lat],
            [lng + offset, lat + offset],
            [lng, lat + offset],
            [lng, lat]
        ]]
    }

def run_psql_command(database, sql_command):
    try:
        command = [
            "docker", "exec", "-i", DOCKER_CONTAINER,
            "psql", "-U", DB_USER, "-d", database, "-c", sql_command
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(result.stderr)
        
        log_info(f"Comando executado com sucesso no banco {database}:\n{sql_command}")
    except Exception as e:
        log_error(f"Erro ao executar comando no banco {database}:\n{sql_command}\nErro: {str(e)}")

def insert_imobiliario_data():
    inscricao = generate_inscricao_tecnica()
    matricula = generate_matricula()
    area = round(random.uniform(50, 500), 2)
    valor_iptu = round(random.uniform(500, 5000), 2)

    sql_command = f"""
        INSERT INTO imobiliario.cadastro_mobiliario (
            inscricao_tecnica, matricula, area_construida, valor_iptu
        ) VALUES ({inscricao}, {matricula}, {area}, {valor_iptu});
    """
    run_psql_command("ecidades", sql_command)
    return inscricao

def insert_geoespacial_data(inscricao_tecnica):
    lat = random.uniform(-33.7, 5.3)
    lng = random.uniform(-73.9, -34.8)
    geometria = json.dumps(generate_geometria(lat, lng)).replace("'", "''")  # Escapar aspas simples
    loteamento = fake.last_name() + " " + random.choice(['Park', 'Village', 'Residencial', 'Centro'])

    sql_command = f"""
        INSERT INTO geoespacial.lotes (
            inscricao_tecnica, geometria, lat_centro, lng_centro, loteamentos
        ) VALUES ({inscricao_tecnica}, '{geometria}', {lat}, {lng}, '{loteamento}');
    """
    run_psql_command("sigeo", sql_command)

def main():
    start_time = time.time()
    log_info("Processo iniciado.")
    try:
        for i in range(5):
            log_info(f"Iteração {i+1}/5")
            inscricao = insert_imobiliario_data()
            inscricao_geo = inscricao + random.randint(1, 9)
            insert_geoespacial_data(inscricao_geo)

        log_info("Inserção completa: 5 registros gerados com sucesso.")

    except Exception as e:
        log_error(f"Erro no processo principal: {str(e)}")
    finally:
        duration = time.time() - start_time
        print(f"Processo concluído em {duration:.2f} segundos")
        log_info(f"Processo concluído em {duration:.2f} segundos")

if __name__ == "__main__":
    main()