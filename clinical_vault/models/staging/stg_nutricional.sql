with source as (
    select * from public.raw_sistema_nutricional
),

staged as (
    select
        id_atendimento,
        regexp_replace(documento_paciente, '[^0-9]', '', 'g') as cpf_paciente,
        nome_completo                                          as nome_paciente,
        cast(data_atendimento as date)                        as data_atendimento,
        cast(peso_kg as numeric)                              as peso_kg,
        cast(altura_cm as numeric)                            as altura_cm,
        cast(imc as numeric)                                  as imc,
        classificacao_imc,
        cast(circunferencia_abdominal_cm as numeric)          as circunferencia_abdominal_cm,
        plano_alimentar,
        cast(meta_calorica as integer)                        as meta_calorica,
        id_nutricionista,
        nome_nutricionista,
        current_timestamp                                     as dbt_loaded_at,
        'sistema_nutricional'                                 as fonte
    from source
)

select * from staged
