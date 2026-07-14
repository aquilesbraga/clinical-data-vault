# Clinical Data Vault 

Pipeline de dados clínicos end-to-end com arquitetura **Data Vault 2.0**, simulando a integração de fontes heterogêneas de uma rede de saúde diagnóstica.

## Dashboard

[Monitoramento Clínico — Tableau Public](https://public.tableau.com/app/profile/aquiles.braga/viz/ClinicalDataVaultMonitoramentoClnico/MonitoramentoClnicoClinicalDataVault)

## Problema

Clínicas e redes de saúde operam com sistemas isolados por especialidade. O sistema médico não conversa com o laboratorial, que não conversa com o nutricional. Isso compromete a visão integrada do paciente e inviabiliza análises de prevenção.

Exemplo real: pacientes com obesidade documentada que desenvolvem diabetes tipo 2 — uma janela de prevenção perdida por falta de integração de dados.

## Arquitetura

Fontes (3 sistemas) → Raw Layer → Staging → Data Vault 2.0 → Data Mart → Tableau

### Camadas

| Camada | Descricao |
|---|---|
| Raw | Espelho fiel das fontes originais — todos os campos como TEXT |
| Staging | Limpeza, padronizacao de CPF e conversao de tipos |
| Data Vault | Hubs, Links e Satellites — integracao auditavel e historica |
| Data Mart | Modelo dimensional para consumo analitico |

### Data Vault 2.0

Hubs: hub_paciente · hub_profissional · hub_exame · hub_consulta

Links: link_paciente_consulta · link_consulta_profissional · link_paciente_exame

Satellites: sat_paciente_dados · sat_consulta_clinica · sat_exame_resultado · sat_nutricional

## Estrutura do Projeto

clinical-data-vault/
├── data/
│   └── raw/              <- CSVs gerados (ignorados pelo git)
├── src/
│   ├── generate_data.py  <- geracao de dados sinteticos
│   └── load_raw.py       <- carga no PostgreSQL
├── clinical_vault/       <- projeto dbt
│   └── models/
│       ├── staging/      <- limpeza e padronizacao
│       ├── data_vault/   <- Hubs, Links, Satellites
│       └── marts/        <- Data Mart final
├── dashboard/            <- CSV exportado para o Tableau
└── requirements.txt

## Fontes de Dados Simuladas

Tres sistemas com schemas intencionalmente heterogeneos:

| Sistema | Registros | Campo CPF | Formato CPF |
|---|---|---|---|
| Prontuario Medico | 505 | cpf_paciente | sem mascara |
| Laboratorio | 616 | numero_cpf | sem mascara |
| Nutricional | 729 | documento_paciente | com mascara |

### Correlacoes Clinicas Implementadas

- IMC >= 30 → 85% de chance de diagnostico E66 (Obesidade)
- Glicemia >= 126 → 80% de chance de diagnostico E11 (Diabetes tipo 2)
- Glicemia 100-125 → 50% de chance de R73 (Pre-diabetes)
- Evolucao de peso progressiva ao longo dos atendimentos nutricionais

## Stack Tecnologica

| Ferramenta | Uso |
|---|---|
| Python + Faker | Geracao de dados sinteticos |
| PostgreSQL 16 | Armazenamento Raw e Data Vault |
| dbt | Transformacoes e modelagem |
| Tableau Public | Dashboard de KPIs |
| GitHub | Versionamento |

## Como Executar

Pre-requisitos: Python 3.11+, PostgreSQL 16, conda

### Instalacao

1. Clonar o repositorio
git clone https://github.com/aquilesbraga/clinical-data-vault.git
cd clinical-data-vault

2. Criar ambiente
conda create -n clinical-data-vault python=3.11 -y
conda activate clinical-data-vault
pip install -r requirements.txt

3. Criar banco de dados
createdb clinical_vault

4. Gerar dados sinteticos
python src/generate_data.py

5. Carregar no PostgreSQL
python src/load_raw.py

6. Rodar transformacoes dbt
cd clinical_vault
dbt run

## KPIs do Dashboard

- Distribuicao de Diagnosticos: frequencia por CID (E11, E66, R73, Z00)
- Classificacao IMC: distribuicao de pacientes por faixa de IMC
- Evolucao de Exames: media mensal de Glicemia, HbA1c, Colesterol e Triglicerideos
- Diagnosticos por Faixa Etaria: distribuicao por Adulto Jovem, Adulto e Idoso

## Autor

Aquiles Braga
- LinkedIn: linkedin.com/in/aquilesbraga
- GitHub: github.com/aquilesbraga
