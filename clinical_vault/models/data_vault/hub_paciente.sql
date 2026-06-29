with medico as (
    select cpf_paciente as bk_paciente, dbt_loaded_at as load_date, fonte
    from {{ ref('stg_medico') }}
),
laboratorio as (
    select cpf_paciente as bk_paciente, dbt_loaded_at as load_date, fonte
    from {{ ref('stg_laboratorio') }}
),
nutricional as (
    select cpf_paciente as bk_paciente, dbt_loaded_at as load_date, fonte
    from {{ ref('stg_nutricional') }}
),
todas_fontes as (
    select * from medico
    union
    select * from laboratorio
    union
    select * from nutricional
)
select distinct
    md5(bk_paciente)                                as hk_paciente,
    bk_paciente,
    min(load_date) over (partition by bk_paciente) as load_date,
    fonte
from todas_fontes
where bk_paciente is not null
