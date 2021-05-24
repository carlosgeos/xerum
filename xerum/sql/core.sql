-- :name full_balance_by_account :many
select extract(year from date::date)::int as year,
       account,
       sum(amount) as balance
from transactions
group by account, year;

-- :name full_balance_for_account :many
select extract(year from date::date) as year,
       account,
       sum(amount) as balance
from transactions
where account = :account_id
group by account, year;

-- :name monthly_balance_by_account :many
select concat(extract(year from date::date), '-',
              lpad(extract(month from date::date)::text, 2, '0')) as month,
       account,
       sum(amount) as balance
from transactions
group by month, account;

-- :name monthly_balance_for_account :many
select concat(extract(year from date::date), '-',
              lpad(extract(month from date::date)::text, 2, '0')) as month,
       account,
       sum(amount) as balance
from transactions
where account = :account_id
group by month, account;

-- :name monthly_balance_for_month :many
with by_month as (
    select concat(extract(year from date::date), '-',
                  lpad(extract(month from date::date)::text, 2, '0')) as month,
           account,
           sum(amount) as balance
    from transactions
    group by month, account
)
select *
from by_month
where month = :month;

-- :name monthly_balance_for_month_and_account :one
with by_month as (
    select concat(extract(year from date::date), '-',
                  lpad(extract(month from date::date)::text, 2, '0')) as month,
           account,
           sum(amount) as balance
    from transactions
    group by month, account
)
select *
from by_month
where month = :month
and account = :account_id;

-- :name row_cnt :one
select count(*) as row_cnt from transactions;
