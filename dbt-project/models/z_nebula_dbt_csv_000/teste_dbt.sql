-- models/teste_dbt.sql

{{ config(materialized='table', schema='z_nebula_dbt_csv_000') }}

select 'Alice' as nome, 30 as idade
union all
select 'Bruno' as nome, 25 as idade