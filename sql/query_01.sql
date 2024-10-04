WITH TRANSACTIONS AS (
    SELECT DATE '2019-05-01' AS date,1234 AS order_id, 999 AS client_id,490756 AS prop_id,50 AS prod_price, 1 AS prod_qty UNION ALL
    SELECT DATE '2019-01-01', 1234, 999,389728, 3.56 AS prod_price, 4 AS prod_qty UNION ALL
    SELECT DATE '2019-01-01', 3456, 845, 490756, 50 AS prod_price,2 AS prod_qty UNION ALL
    SELECT DATE '2019-01-01', 3456, 845,549380,300 AS prod_price, 1 AS prod_qty UNION ALL
    SELECT DATE '2019-01-01', 3456, 845,293718, 10 AS prod_price, 6 AS prod_qty
), PRODUCT_NOMENCLATURE AS (
    SELECT 490756 AS product_id,'MEUBLE' AS product_type,'Chaise' AS product_name UNION ALL
    SELECT 389728,'DECO' AS product_type,'Boule de Noël' AS product_name UNION ALL
    SELECT 549380, 'MEUBLE' AS product_type, 'Canapé' AS product_name UNION ALL
    SELECT 293718,'DECO' AS product_type,'Mug' AS product_name
)

SELECT DISTINCT
        date,
        SUM(prod_price * prod_qty) OVER (PARTITION BY date) AS ventes
FROM TRANSACTIONS
where date BETWEEN '2019-01-01' AND '2019-12-31'
ORDER BY DATE ASC