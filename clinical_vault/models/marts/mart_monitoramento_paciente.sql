{{ config(materialized='table') }}

with pacientes as (
    select hk_paciente, bk_paciente
    from {{ ref('hub_paciente') }}
),

dados_paciente as (
    select hk_paciente, nome_paciente, sexo, data_nascimento
    from {{ ref('sat_paciente_dados') }}
),

consultas as (
    select hk_paciente, hk_consulta
    from {{ ref('link_paciente_consulta') }}
),

clinica as (
    select hk_consulta, especialidade, cid_diagnostico,
           descricao_diagnostico, data_consulta
    from {{ ref('sat_consulta_clinica') }}
),

nutricional as (
    select hk_paciente, peso_kg, imc, classificacao_imc,
           circunferencia_abdominal_cm, plano_alimentar,
           meta_calorica, data_atendimento
    from {{ ref('sat_nutricional') }}
),

exames as (
    select hk_paciente, hk_exame
    from {{ ref('link_paciente_exame') }}
),

resultados as (
    select hk_exame, tipo_exame, resultado_valor,
           unidade, valor_referencia_min, valor_referencia_max,
           status_resultado, data_coleta
    from {{ ref('sat_exame_resultado') }}
)

select
    p.bk_paciente                                           as cpf_paciente,
    dp.nome_paciente,
    dp.sexo,
    dp.data_nascimento,
    date_part('year', age(dp.data_nascimento::date))        as idade,
    c.especialidade,
    c.cid_diagnostico,
    c.descricao_diagnostico,
    c.data_consulta,
    n.peso_kg,
    n.imc,
    n.classificacao_imc,
    n.circunferencia_abdominal_cm,
    n.plano_alimentar,
    n.meta_calorica,
    n.data_atendimento,
    r.tipo_exame,
    r.resultado_valor,
    r.unidade,
    r.valor_referencia_min,
    r.valor_referencia_max,
    r.status_resultado,
    r.data_coleta

from pacientes p
left join dados_paciente dp on p.hk_paciente = dp.hk_paciente
left join consultas c_link  on p.hk_paciente = c_link.hk_paciente
left join clinica c         on c_link.hk_consulta = c.hk_consulta
left join nutricional n     on p.hk_paciente = n.hk_paciente
left join exames e_link     on p.hk_paciente = e_link.hk_paciente
left join resultados r      on e_link.hk_exame = r.hk_exame
