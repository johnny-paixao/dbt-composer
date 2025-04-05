with dados as (
  select 'Alice' as nome, 30 as idade
  union all
  select 'Bruno' as nome, 25 as idade
)
select * from dados
