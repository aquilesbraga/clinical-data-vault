with source as (
    select * from public.raw_sistema_laboratorio
),

staged as (
    select
        id_exame,
        regexp_replace(numero_cpf, '[^0-9]', '', 'g')  as cpf_paciente,
        paciente_nome                                   as nome_paciente,
        cast(data_coleta as date)                       as data_coleta,
        tipo_exame,
        cast(resultado_valor as numeric)                as resultado_valor,
        unidade,
        cast(valor_referencia_min as numeric)           as valor_referencia_min,
        cast(valor_referencia_max as numeric)           as valor_referencia_max,
        status_resultado,
        id_laboratorio,
        nome_laboratorio,
        current_timestamp                               as dbt_loaded_at,
        'sistema_laboratorio'                           as fonte
    from source
)

select * from staged
