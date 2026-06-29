with source as (
    select
        id_exame                                        as bk_exame,
        tipo_exame,
        dbt_loaded_at                                   as load_date,
        fonte
    from {{ ref('stg_laboratorio') }}
)
select distinct
    md5(bk_exame)                                       as hk_exame,
    bk_exame,
    tipo_exame,
    min(load_date) over (partition by bk_exame)        as load_date,
    fonte
from source
where bk_exame is not null
