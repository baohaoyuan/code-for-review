--case when in SQL


select to_char(avg(r.order_price), 'fm9999999.90'),to_char(avg(r.size_ord), 'fm9999999.90'),r.week_id,r.start_date ,
case when order_price>=25 and order_price<30 then '25-30'
when order_price>=30 and order_price<35 then '30-35'
when order_price>=35 and order_price<40 then '35-40'
when order_price>=40 then 'more than 40'
end as order_total_grp
from
(select sum(o.web_price) as order_price,sum(o.quantity_ordered) as size_ord,d.week_id as week_id,d.week_start_date as start_date from abc_data.xyz_FACT_ORDER_ITEMS o
INNER JOIN abc_data.xyz_FACT_SHIPPING s
on o.order_id=s.order_id
inner join abc_data.xyz_DIM_DAY d
ON s.DAY_SKEY = d.DAY_SKEY
inner join abc_data.xyz_DIM_ORDER_HEADER k
on o.order_id=k.order_id
where s.delivery_date BETWEEN  '28-SEP-2019' and '05-OCT-2019'
and k.fulfillment_type='xxx'
group by o.order_id,d.week_id,d.week_start_date
) r
group by r.week_id,r.start_date,case when order_price>=25 and order_price<30 then '25-30'
when order_price>=30 and order_price<35 then '30-35'
when order_price>=35 and order_price<40 then '35-40'
when order_price>=40 then 'more than 40' end
order by week_id

--sql to select only one type of response for the last 12 weeks


select distinct  O.SINGLE_PROFILE_ID,  postal_code
from aaa.abc_ORDER O
join aaa.abc_CUSTOMER_ADDRESS c
on c.order_record_id=o.record_id
where not exists
(select SINGLE_PROFILE_ID,pf_from
from aaa.abc_ORDER  s
where o.SINGLE_PROFILE_ID=s.SINGLE_PROFILE_ID
and (pf_from in ('A','G') or pf_from is null)
and TRUNC(ORDER_SUBMITTED_DATE) >sysdate-84)
and O.pf_from ='D1'
and TRUNC(ORDER_SUBMITTED_DATE) >sysdate-84
and postal_code in ('LL372JA','LL372JB');


--sql using cte to find out the percent of cancelled order but not due to authorization reasons

with al as 
(select distinct order_skey
from abc.DIM_ORDER
where created_date between '01-JUL-20' and '31-JUL-20')
,cc as
(select distinct order_skey
from abc.DIM_ORDER
where created_date between '01-JUL-20' and '31-JUL-20'
and order_status='CANCELLED'
and FULL_AUTHORIZATION_IND not in ('FAILURE','AUTHORIZATION_IGNORED'))

select  count(cc.order_skey) cc_cnt, count(al.order_skey) all_cnt, count(cc.order_skey)/count(al.order_skey) as percent_cancelled
from al 
left join cc
on al.order_skey=cc.order_skey;


--sql to get top 50 ranked items in each department

--first create cte for the top 50 items within each department
with cte_rk as ( select distinct DEPT_ID,sku_id
                                         from (select sku_id, DEPT_ID , DEPT_NAME ,total_ordered_qty,total_subst_qty,
                                          rank() over (partition by DEPT_ID order by total_subst_qty desc) as rk
                              from (select sku_id, DEPT_ID , DEPT_NAME ,
                                    sum(oi.quantity_ordered) as total_ordered_qty,
                                    sum(oi.subst_for_qty) as total_subst_qty
                                    from    abc_data.xyz_FACT_ORDER_ITEMS oi
                                    INNER JOIN abc_data.xyz_FACT_SHIPPING sh
                                    on oi.order_id=sh.order_id
                                    INNER JOIN  abc_data.xyz_DIM_PRODUCT  pr
                                    on oi.product_skey=pr.product_skey
                                    inner join abc_data.xyz_DIM_DAY dy
                                    ON sh.DAY_SKEY = dy.DAY_SKEY
                                    where oi.store_id in ('123','456')
                                    and sh.delivery_date  BETWEEN  '05-OCT-2019' and '19-OCT-2019'
                                GROUP BY sku_id, DEPT_ID , DEPT_NAME
                                        )
                                  where total_subst_qty>0
                                       )
                            where rk<=50
),


--2nd find min and max avg prices for a 52 week rolling period
  cte_od AS  (select od.*,
min(avg_unit_price ) over (order by store_id,sku_id,week_id ROWS BETWEEN 51 PRECEDING AND CURRENT ROW) as min_unit_price,
max(avg_unit_price ) over (order by store_id,sku_id,week_id ROWS BETWEEN 51 PRECEDING AND CURRENT ROW) as max_unit_price
from (select year, week_in_year, WEEK_START_DATE,WEEK_NAME,WEEK_ID,o.store_id,o.sku_id,p.product_name,p.DEPT_ID ,p.DEPT_NAME,
            sum(o.quantity_ordered) as total_ordered_qty,       
            sum(o.subst_for_qty) as total_subst_qty,
            to_char(avg(unit_price), 'fm9999999.90') as avg_unit_price
            from    abc_data.xyz_FACT_ORDER_ITEMS o 
            INNER JOIN abc_data.xyz_FACT_SHIPPING s
                on o.order_id=s.order_id
            INNER JOIN  abc_data.xyz_DIM_PRODUCT  p
                on o.product_skey=p.product_skey
            inner join abc_data.xyz_DIM_DAY d
                ON s.DAY_SKEY = d.DAY_SKEY                     
            where o.store_id in ('123','456')
            and s.delivery_date  BETWEEN  '05-OCT-2019' and '19-OCT-2019'
            GROUP BY year,week_in_year,WEEK_START_DATE,WEEK_NAME,WEEK_ID,o.store_id, o.sku_id,p.product_name, p.DEPT_ID,p.DEPT_NAME
            ) od)
--3rd find min and max discounted prices for a 52 week rolling period
, cte_dc as ( select year, week_in_year,WEEK_START_DATE,WEEK_NAME,WEEK_ID, store_id,sku_id,unit_discounted_price,
min(unit_discounted_price ) over (order by store_id,sku_id,week_id ROWS BETWEEN 51 PRECEDING AND CURRENT ROW) as min_price,
max(unit_discounted_price ) over (order by store_id,sku_id,week_id ROWS BETWEEN 51 PRECEDING AND CURRENT ROW) as max_price
from (select year,week_in_year ,WEEK_START_DATE,WEEK_NAME,WEEK_ID,i.store_id , i.sku_id ,
to_char(sum(WEB_PRICE)/sum(PICKED_QTY),'fm9999999.90')  as unit_discounted_price, 
to_char(avg(UNIT_RETAIL_AMOUNT),'fm9999999.90') as unit_regular_price
        from abc_data.xyz_DIM_VOUCHER_PROMOTIONS p
        join abc_data.xyz_fact_used_vouchers u
        on p.voucher_skey=u.voucher_skey
        join  abc_data.xyz_FACT_ORDER_ITEMS  i
        on i.sku_id=u.sku_id
        and i.order_skey=u.order_skey
        INNER JOIN abc_data.xyz_FACT_SHIPPING s
               on i.order_id=s.order_id
        inner join abc_data.xyz_DIM_DAY d
               ON s.DAY_SKEY = d.DAY_SKEY                  
        where promotion_type in (1,2,3)
        and i.store_id in ('123','456')
        and i.sku_id in 
        (select distinct sku_id
                    from (select sku_id, DEPT_ID , DEPT_NAME ,total_ordered_qty,total_subst_qty,
                            rank() over (partition by DEPT_ID order by total_subst_qty desc) as rk
                              from (
                                    select sku_id, DEPT_ID , DEPT_NAME ,
                                    sum(oi.quantity_ordered) as total_ordered_qty,
                                    sum(oi.subst_for_qty) as total_subst_qty
                                    from    abc_data.xyz_FACT_ORDER_ITEMS oi
                                    INNER JOIN abc_data.xyz_FACT_SHIPPING sh
                                    on oi.order_id=sh.order_id
                                    INNER JOIN  abc_data.xyz_DIM_PRODUCT  pr
                                    on oi.product_skey=pr.product_skey
                                    inner join abc_data.xyz_DIM_DAY dy
                                    ON sh.DAY_SKEY = dy.DAY_SKEY
                                    where oi.store_id in ('123','456')
                                    and sh.delivery_date  BETWEEN  '05-OCT-2019' and '19-OCT-2019'
                                GROUP BY sku_id, DEPT_ID , DEPT_NAME
                                        )
                                  where total_subst_qty>0
                                       )
                            where rk<=50)                       
                   
 and delivery_date  BETWEEN  '05-OCT-2019' and '19-OCT-2019'
 and PICKED_QTY>0
 group by year,week_in_year,WEEK_START_DATE,WEEK_NAME,WEEK_ID,i.store_id, i.sku_id)  )  

--geneate the final output for the top 50 items within each department 
select distinct o.year,o.week_in_year, o.WEEK_START_DATE,o.WEEK_NAME,o.WEEK_ID,o.store_id,o.sku_id,o.product_name,o.DEPT_ID ,o.DEPT_NAME,total_ordered_qty,total_subst_qty,min_unit_price,max_unit_price,
COALESCE(d.unit_discounted_price,o.avg_unit_price) as avg_item_price,COALESCE(min_price, min_unit_price) as price_min,COALESCE(max_price,max_unit_price) as price_max,
o.avg_unit_price,d.unit_discounted_price
from (select year, week_in_year, WEEK_START_DATE,WEEK_NAME,WEEK_ID,store_id,p.sku_id,p.product_name,p.DEPT_ID ,p.DEPT_NAME,total_ordered_qty,total_subst_qty,avg_unit_price,min_unit_price,max_unit_price
        from  cte_rk r  
        JOIN cte_od p
     on r.DEPT_ID=p.DEPT_ID and r.sku_id=p.sku_id) o
left join cte_dc d
on o.year=d.year and o.week_id=d.week_id and o.sku_id=d.sku_id and o.store_id=d.store_id;


--checking if quantity the same


select year, week_in_year, WEEK_START_DATE,WEEK_NAME,WEEK_ID,o.store_id,o.sku_id,p.product_name,p.DEPT_ID ,p.DEPT_NAME,
            sum(o.quantity_ordered) as total_ordered_qty,       
            sum(o.subst_for_qty) as total_subst_qty,
            to_char(avg(unit_price), 'fm9999999.90') as avg_unit_price
            from    abc_data.xyz_FACT_ORDER_ITEMS o 
            INNER JOIN abc_data.xyz_FACT_SHIPPING s
                on o.order_id=s.order_id
            INNER JOIN  abc_data.xyz_DIM_PRODUCT  p
                on o.product_skey=p.product_skey
            inner join abc_data.xyz_DIM_DAY d
                ON s.DAY_SKEY = d.DAY_SKEY                     
            where o.store_id in ('123','456')
            and s.delivery_date  BETWEEN  '05-OCT-2019' and '19-OCT-2019'
            and sku_id=910001706771
            GROUP BY year,week_in_year,WEEK_START_DATE,WEEK_NAME,WEEK_ID,o.store_id, o.sku_id,p.product_name, p.DEPT_ID,p.DEPT_NAME
910001706771




--sql to create random sample based on percentile

--first select the cutoff amount for percentiles

drop table aaa_dev.test_hf_pct_cutoff;
create table aaa_dev.test_hf_pct_cutoff as
select distinct PERCENTILE_cont(0.01) within group (order by amt) over () as cutoff, '0.01' as pct
from  (select household_id, sum(txn_amt) as amt 
      from aaa_dev.bbb_q3_2018_groc g
      join (select household_id, card from aaa_dev.exp_bbb_exposed_q3_crd 
            where household_id not in (#####1,#####6)
            group by 1,2) c
      on g.hashed_card_no=c.card
      where  local_txn_ts between '2018-04-01 00:00:00' AND '2018-06-30 11:59:59' group by 1
      ) a

union
select distinct PERCENTILE_cont(0.05) within group (order by amt) over () as cutoff, '0.05' as pct
from  (select household_id, sum(txn_amt) as amt 
      from aaa_dev.bbb_q3_2018_groc g
      join (select household_id, card from aaa_dev.exp_bbb_exposed_q3_crd 
            where household_id not in (#####1,#####6)
            group by 1,2) c
      on g.hashed_card_no=c.card
      where  local_txn_ts between '2018-04-01 00:00:00' AND '2018-06-30 11:59:59' group by 1
      ) a
....
---use the cutoff amount to select random samples within the group

create table aaa_dev.exp_bbb_comp_pool_q3_crd_pct as

(select household_id, amt,'0.01' as pct from 
       ( select household_id, sum(txn_amt) as amt 
           from aaa_dev.bbb_q3_2018_groc g
           join (select household_id, card 
                 from aaa_dev.exp_bbb_comp_pool_q3_crd 
                 group by 1,2) c
           on g.hashed_card_no=c.card
           where  local_txn_ts between '2018-04-01 00:00:00' AND '2018-06-30 11:59:59'
           group by 1) p
        where amt<=(select cutoff from aaa_dev.test_hf_pct_cutoff   where pct='0.01')
        group by 1,2
        order by RANDOM() LIMIT 37506     )
union 
  (select household_id, amt, '0.05' as pct from 
         ( select household_id, sum(txn_amt) as amt 
           from aaa_dev.bbb_q3_2018_groc g
           join (select household_id, card 
                 from aaa_dev.exp_bbb_comp_pool_q3_crd 
                 group by 1,2) c
           on g.hashed_card_no=c.card
           where  local_txn_ts between '2018-04-01 00:00:00' AND '2018-06-30 11:59:59'
           group by 1)  p
       where amt>(select cutoff from aaa_dev.test_hf_pct_cutoff   where pct='0.01') 
                 and amt<=(select cutoff from aaa_dev.test_hf_pct_cutoff   where pct='0.05') 
      group by 1,2
      order by RANDOM() LIMIT 150024        )

  .....

