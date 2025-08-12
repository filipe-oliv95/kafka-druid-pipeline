# Automatic Data Ingestion

Este script insere dados fictícios em duas tabelas PostgreSQL — uma de cadastro imobiliário e outra de dados geoespaciais — utilizando Python, Faker e psycopg2. Ideal para simular dados em pipelines de dados ou ambientes de teste.

## 📌 Funcionalidade

A cada execução, o script:
1. Insere 5 registros na tabela `imobiliario.cadastro_mobiliario`
2. Insere 5 registros relacionados na tabela `geoespacial.lotes`
3. Gera logs de execução e erros no diretório `logs/`

## ⚙️ Estrutura de Banco Esperada

- **Banco:** `PostgreSQL`
- **Tabelas:**
  - `imobiliario.cadastro_mobiliario(inscricao_tecnica, matricula, area_construida, valor_iptu)`
  - `geoespacial.lotes(inscricao_tecnica, geometria, lat_centro, lng_centro, loteamentos)`

## 📦 Requisitos

- Python 3.7+
- PostgreSQL rodando com os bancos e schemas configurados
- Acesso aos bancos `ecidades` e `sigeo` com o mesmo host

## 🛠️ Instalação

```bash
# Clone o projeto ou copie os arquivos para o servidor
cd /home/deploy/kafka-druid-pipeline/automatic_data_ingestion
```

# Crie e ative o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
````

# Instale as dependências
```bash
pip install -r requirements.txt
````

## 🕒 Agendamento com cron (a cada 10 minutos)

Edite o crontab:

```bash
crontab -e
```

Adicione a linha:

```bash
*/10 * * * * /home/deploy/kafka-druid-pipeline/automatic_data_ingestion/venv/bin/python /home/deploy/kafka-druid-pipeline/automatic_data_ingestion/main.py >> /home/deploy/kafka-druid-pipeline/automatic_data_ingestion/logs/cron.log 2>&1
```

## 📂 Estrutura de Arquivos

```
automatic_data_ingestion/
├── main.py                # Script principal
├── requirements.txt       # Dependências
├── README                 # Instruções de uso
├── venv/                  # Ambiente virtual
└── logs/
    ├── error.log          # Log de erros
    └── execution.log      # Log de execuções
```