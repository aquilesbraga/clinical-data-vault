with source as (
    select
        md5(cpf_paciente || id_consulta)    as hk_link_paciente_consulta,
        md5(cpf_paciente)                   as hk_paciente,
        md5(id_consulta)                    as hk_consulta,
        dbt_loaded_at                       as load_date,
        fonte
    from {{ ref('stg_medico') }}
    where cpf_paciente is not null
      and id_consulta is not null
)
select distinct * from source
