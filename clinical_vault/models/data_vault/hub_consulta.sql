with source as (
    select
        id_consulta                                     as bk_consulta,
        especialidade,
        dbt_loaded_at                                   as load_date,
        fonte
    from {{ ref('stg_medico') }}
)
select distinct
    md5(bk_consulta)                                    as hk_consulta,
    bk_consulta,
    especialidade,
    min(load_date) over (partition by bk_consulta)     as load_date,
    fonte
from source
where bk_consulta is not null
