with source as (
    select
        md5(cpf_paciente || id_exame)       as hk_link_paciente_exame,
        md5(cpf_paciente)                   as hk_paciente,
        md5(id_exame)                       as hk_exame,
        dbt_loaded_at                       as load_date,
        fonte
    from {{ ref('stg_laboratorio') }}
    where cpf_paciente is not null
      and id_exame is not null
)
select distinct * from source
