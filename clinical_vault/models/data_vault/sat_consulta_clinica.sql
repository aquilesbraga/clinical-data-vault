with source as (
    select
        md5(id_consulta)                    as hk_consulta,
        especialidade,
        cid_diagnostico,
        descricao_diagnostico,
        data_consulta,
        dbt_loaded_at                       as load_date,
        md5(especialidade || cid_diagnostico || coalesce(descricao_diagnostico, '')) as hash_diff,
        fonte
    from {{ ref('stg_medico') }}
    where id_consulta is not null
)
select distinct * from source
