with medicos as (
    select id_medico as bk_profissional, nome_medico as nome, 'Medico' as tipo, dbt_loaded_at as load_date, fonte
    from {{ ref('stg_medico') }}
),
nutricionistas as (
    select id_nutricionista as bk_profissional, nome_nutricionista as nome, 'Nutricionista' as tipo, dbt_loaded_at as load_date, fonte
    from {{ ref('stg_nutricional') }}
),
todas_fontes as (
    select * from medicos
    union
    select * from nutricionistas
)
select distinct
    md5(bk_profissional)                                    as hk_profissional,
    bk_profissional,
    nome,
    tipo,
    min(load_date) over (partition by bk_profissional)     as load_date,
    fonte
from todas_fontes
where bk_profissional is not null
