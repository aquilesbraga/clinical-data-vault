import pandas as pd
from sqlalchemy import create_engine

# Conexão com o banco
engine = create_engine("postgresql+psycopg2://localhost/clinical_vault")

# Carregar CSVs
df_medico = pd.read_csv("data/raw/sistema_medico.csv", dtype=str)
df_lab = pd.read_csv("data/raw/sistema_laboratorio.csv", dtype=str)
df_nutri = pd.read_csv("data/raw/sistema_nutricional.csv", dtype=str)

# Inserir nas tabelas Raw
df_medico.to_sql("raw_sistema_medico", engine, if_exists="append", index=False)
df_lab.to_sql("raw_sistema_laboratorio", engine, if_exists="append", index=False)
df_nutri.to_sql("raw_sistema_nutricional", engine, if_exists="append", index=False)

print("Dados carregados com sucesso!")
print(f"   raw_sistema_medico:      {len(df_medico)} registros")
print(f"   raw_sistema_laboratorio: {len(df_lab)} registros")
print(f"   raw_sistema_nutricional: {len(df_nutri)} registros")
