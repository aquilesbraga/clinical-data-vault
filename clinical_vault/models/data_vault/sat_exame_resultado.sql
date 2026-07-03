with source as (
    select
        md5(id_exame)                       as hk_exame,
        tipo_exame,
        resultado_valor,
        unidade,
        valor_referencia_min,
        valor_referencia_max,
        status_resultado,
        data_coleta,
        dbt_loaded_at                       as load_date,
        md5(tipo_exame || coalesce(cast(resultado_valor as text), '') || coalesce(status_resultado, '')) as hash_diff,
        fonte
    from {{ ref('stg_laboratorio') }}
    where id_exame is not null
)
select distinct * from source
