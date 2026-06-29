with source as (
    select * from public.raw_sistema_medico
),

staged as (
    select
        id_consulta,
        -- Padroniza CPF: remove qualquer mascara e mantem so digitos
        regexp_replace(cpf_paciente, '[^0-9]', '', 'g') as cpf_paciente,
        nome_paciente,
        cast(data_nascimento as date)                   as data_nascimento,
        sexo,
        cast(data_consulta as date)                     as data_consulta,
        especialidade,
        cid_diagnostico,
        descricao_diagnostico,
        id_medico,
        nome_medico,
        -- Metadados de carga
        current_timestamp                               as dbt_loaded_at,
        'sistema_medico'                                as fonte
    from source
)

select * from staged
