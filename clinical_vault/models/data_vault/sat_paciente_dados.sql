with source as (
    select
        md5(cpf_paciente)                   as hk_paciente,
        nome_paciente,
        data_nascimento,
        sexo,
        dbt_loaded_at                       as load_date,
        md5(nome_paciente || coalesce(cast(data_nascimento as text), '') || coalesce(sexo, '')) as hash_diff,
        fonte
    from {{ ref('stg_medico') }}
    where cpf_paciente is not null
)
select distinct * from source
