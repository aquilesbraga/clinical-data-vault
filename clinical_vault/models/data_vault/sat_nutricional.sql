with source as (
    select
        md5(cpf_paciente)                   as hk_paciente,
        peso_kg,
        altura_cm,
        imc,
        classificacao_imc,
        circunferencia_abdominal_cm,
        plano_alimentar,
        meta_calorica,
        data_atendimento,
        dbt_loaded_at                       as load_date,
        md5(cast(peso_kg as text) || cast(imc as text) || coalesce(classificacao_imc, '')) as hash_diff,
        fonte
    from {{ ref('stg_nutricional') }}
    where cpf_paciente is not null
)
select distinct * from source
