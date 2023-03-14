Write a query which finds a salesmen, who don't have any sales for the RED company

    SELECT
         s.name
     FROM
         sales_person s
     WHERE
         s.sales_id NOT IN (SELECT
                 o.sales_id
             FROM
                 orders o
                     LEFT JOIN
                 company c USING(company_id)
             WHERE
                 c.name = 'RED');   