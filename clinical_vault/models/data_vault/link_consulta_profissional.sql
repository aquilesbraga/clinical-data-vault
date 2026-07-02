with source as (
    select
        md5(id_consulta || id_medico)       as hk_link_consulta_profissional,
        md5(id_consulta)                    as hk_consulta,
        md5(id_medico)                      as hk_profissional,
        dbt_loaded_at                       as load_date,
        fonte
    from {{ ref('stg_medico') }}
    where id_consulta is not null
      and id_medico is not null
)
select distinct * from source
