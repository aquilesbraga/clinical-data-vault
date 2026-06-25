import uuid
import random
import hashlib
from datetime import date, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker("pt_BR")
random.seed(42)
np.random.seed(42)

# ─── CONFIGURAÇÕES ────────────────────────────────────────────
N_PACIENTES = 200
DATA_INICIO = date(2023, 1, 1)
DATA_FIM = date(2024, 12, 31)

MEDICOS = [(str(uuid.uuid4()), fake.name()) for _ in range(10)]
NUTRICIONISTAS = [(str(uuid.uuid4()), fake.name()) for _ in range(5)]
LABORATORIOS = [(str(uuid.uuid4()), "Lab " + fake.last_name()) for _ in range(3)]

# ─── HELPERS ──────────────────────────────────────────────────
def data_aleatoria(inicio, fim):
    delta = (fim - inicio).days
    return inicio + timedelta(days=random.randint(0, delta))

def calcular_imc(peso, altura_cm):
    altura_m = altura_cm / 100
    return round(peso / (altura_m ** 2), 1)

def classificar_imc(imc):
    if imc < 18.5:
        return "Magreza"
    elif imc < 25:
        return "Normal"
    elif imc < 30:
        return "Sobrepeso"
    elif imc < 35:
        return "Obesidade Grau I"
    elif imc < 40:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III"

def gerar_glicemia(imc):
    """Correlação clínica: IMC alto → glicemia tende a ser maior."""
    if imc >= 30:
        return round(np.random.normal(loc=130, scale=30), 1)
    elif imc >= 25:
        return round(np.random.normal(loc=105, scale=15), 1)
    else:
        return round(np.random.normal(loc=88, scale=10), 1)

def gerar_hba1c(glicemia):
    """HbA1c tem correlação direta com glicemia média."""
    return round((glicemia + 46.7) / 28.7, 1)

def gerar_triglicerideos(imc):
    if imc >= 30:
        return round(np.random.normal(loc=200, scale=50), 1)
    else:
        return round(np.random.normal(loc=130, scale=30), 1)

def status_resultado(valor, ref_min, ref_max):
    if valor < ref_min or valor > ref_max:
        return "Alterado" if abs(valor - ref_max) < 50 else "Crítico"
    return "Normal"

def definir_cid(imc, glicemia):
    """Correlação clínica: define diagnóstico com base em IMC e glicemia."""
    cids = []
    if imc >= 30:
        if random.random() < 0.85:
            cids.append(("E66", "Obesidade"))
    if glicemia >= 126:
        if random.random() < 0.80:
            cids.append(("E11", "Diabetes mellitus tipo 2"))
    elif glicemia >= 100:
        if random.random() < 0.50:
            cids.append(("R73", "Glicemia elevada / Pré-diabetes"))
    if not cids:
        cids.append(("Z00", "Consulta de rotina"))
    return random.choice(cids)

def cpf_sem_mascara(cpf):
    return cpf.replace(".", "").replace("-", "")

def cpf_com_mascara(cpf):
    digits = cpf_sem_mascara(cpf)
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"

# ─── GERAÇÃO DOS PACIENTES BASE ───────────────────────────────
pacientes = []
for _ in range(N_PACIENTES):
    sexo = random.choice(["M", "F"])
    if sexo == "M":
        peso = round(np.random.normal(loc=88, scale=18), 1)
        altura = random.randint(165, 190)
    else:
        peso = round(np.random.normal(loc=72, scale=15), 1)
        altura = random.randint(155, 175)

    peso = max(45, min(peso, 180))
    imc = calcular_imc(peso, altura)
    glicemia = gerar_glicemia(imc)

    pacientes.append({
        "cpf": fake.cpf(),
        "nome": fake.name_male() if sexo == "M" else fake.name_female(),
        "data_nascimento": fake.date_of_birth(minimum_age=25, maximum_age=75),
        "sexo": sexo,
        "peso_kg": peso,
        "altura_cm": altura,
        "imc": imc,
        "glicemia_base": glicemia,
    })

# ─── SISTEMA 1: PRONTUÁRIO MÉDICO ─────────────────────────────
registros_medicos = []
for p in pacientes:
    n_consultas = random.randint(1, 4)
    for _ in range(n_consultas):
        glicemia = gerar_glicemia(p["imc"])
        cid, descricao = definir_cid(p["imc"], glicemia)
        medico_id, medico_nome = random.choice(MEDICOS)
        especialidades = ["Clínica Geral", "Endocrinologia", "Cardiologia", "Nutrologia"]
        registros_medicos.append({
            "id_consulta": str(uuid.uuid4()),
            "cpf_paciente": cpf_sem_mascara(p["cpf"]),
            "nome_paciente": p["nome"],
            "data_nascimento": p["data_nascimento"],
            "sexo": p["sexo"],
            "data_consulta": data_aleatoria(DATA_INICIO, DATA_FIM),
            "especialidade": random.choice(especialidades),
            "cid_diagnostico": cid,
            "descricao_diagnostico": descricao,
            "id_medico": medico_id,
            "nome_medico": medico_nome,
        })

df_medico = pd.DataFrame(registros_medicos)

# ─── SISTEMA 2: LABORATÓRIO ───────────────────────────────────
registros_lab = []
for p in pacientes:
    n_exames = random.randint(1, 5)
    for _ in range(n_exames):
        glicemia = max(60, gerar_glicemia(p["imc"]))
        hba1c = max(4.0, gerar_hba1c(glicemia))
        trigli = max(50, gerar_triglicerideos(p["imc"]))
        lab_id, lab_nome = random.choice(LABORATORIOS)

        exames = [
            ("Glicemia de Jejum", glicemia, "mg/dL", 70, 99),
            ("HbA1c", hba1c, "%", 4.0, 5.6),
            ("Triglicerídeos", trigli, "mg/dL", 0, 150),
            ("Colesterol Total", round(np.random.normal(190, 35), 1), "mg/dL", 0, 200),
        ]

        tipo, valor, unidade, ref_min, ref_max = random.choice(exames)
        registros_lab.append({
            "id_exame": str(uuid.uuid4()),
            "numero_cpf": cpf_sem_mascara(p["cpf"]),
            "paciente_nome": p["nome"],
            "data_coleta": data_aleatoria(DATA_INICIO, DATA_FIM),
            "tipo_exame": tipo,
            "resultado_valor": valor,
            "unidade": unidade,
            "valor_referencia_min": ref_min,
            "valor_referencia_max": ref_max,
            "status_resultado": status_resultado(valor, ref_min, ref_max),
            "id_laboratorio": lab_id,
            "nome_laboratorio": lab_nome,
        })

df_lab = pd.DataFrame(registros_lab)

# ─── SISTEMA 3: NUTRICIONAL ───────────────────────────────────
registros_nutri = []
for p in pacientes:
    n_atendimentos = random.randint(1, 6)
    peso_atual = p["peso_kg"]
    for i in range(n_atendimentos):
        # Simula perda de peso progressiva ao longo dos atendimentos
        peso_atual = max(45, peso_atual - round(random.uniform(0, 1.5), 1))
        imc_atual = calcular_imc(peso_atual, p["altura_cm"])
        nutri_id, nutri_nome = random.choice(NUTRICIONISTAS)
        planos = [
            "Dieta hipocalórica com restrição de carboidratos simples",
            "Dieta mediterrânea com controle de gorduras saturadas",
            "Plano low carb com aumento de proteínas magras",
            "Dieta balanceada com fracionamento em 5 refeições",
        ]
        registros_nutri.append({
            "id_atendimento": str(uuid.uuid4()),
            "documento_paciente": cpf_com_mascara(p["cpf"]),
            "nome_completo": p["nome"],
            "data_atendimento": data_aleatoria(DATA_INICIO, DATA_FIM),
            "peso_kg": peso_atual,
            "altura_cm": p["altura_cm"],
            "imc": imc_atual,
            "classificacao_imc": classificar_imc(imc_atual),
            "circunferencia_abdominal_cm": round(np.random.normal(
                loc=95 if p["imc"] >= 30 else 82, scale=8), 1),
            "plano_alimentar": random.choice(planos),
            "meta_calorica": random.choice([1400, 1600, 1800, 2000, 2200]),
            "id_nutricionista": nutri_id,
            "nome_nutricionista": nutri_nome,
        })

df_nutri = pd.DataFrame(registros_nutri)

# ─── EXPORTAR CSVs ────────────────────────────────────────────
df_medico.to_csv("data/raw/sistema_medico.csv", index=False)
df_lab.to_csv("data/raw/sistema_laboratorio.csv", index=False)
df_nutri.to_csv("data/raw/sistema_nutricional.csv", index=False)

print("✅ Dados gerados com sucesso!")
print(f"   Sistema Médico:      {len(df_medico)} registros")
print(f"   Sistema Laboratório: {len(df_lab)} registros")
print(f"   Sistema Nutricional: {len(df_nutri)} registros")
print("\nArquivos salvos em data/raw/")