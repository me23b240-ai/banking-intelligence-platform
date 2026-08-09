
-- Top 20 customers by transaction value
SELECT c.customer_id, c.Customer_Age, c.Income_Category,
       t.Total_Trans_Amt, t.Total_Trans_Ct
FROM customers c
JOIN transactions_agg t ON c.customer_id = t.customer_id
ORDER BY t.Total_Trans_Amt DESC
LIMIT 20;

-- Average transaction value by income category
SELECT c.Income_Category,
       ROUND(AVG(t.Total_Trans_Amt), 2) AS avg_trans_amt,
       COUNT(*) AS customer_count
FROM customers c
JOIN transactions_agg t ON c.customer_id = t.customer_id
GROUP BY c.Income_Category
ORDER BY avg_trans_amt DESC;
