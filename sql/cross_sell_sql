
-- Product penetration: distribution of relationship count
SELECT Total_Relationship_Count, COUNT(*) AS customer_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM accounts), 2) AS pct_of_base
FROM accounts
GROUP BY Total_Relationship_Count
ORDER BY Total_Relationship_Count;

-- Single-product customers who resemble multi-product customers (candidates for cross-sell)
-- Using transaction activity and utilization as similarity signals, proxy since no propensity score exists yet
SELECT c.customer_id, c.Customer_Age, c.Income_Category,
       a.Total_Relationship_Count, t.Total_Trans_Amt, t.Total_Trans_Ct, a.Avg_Utilization_Ratio
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions_agg t ON c.customer_id = t.customer_id
WHERE a.Total_Relationship_Count = 1
  AND t.Total_Trans_Amt > (SELECT AVG(Total_Trans_Amt) FROM transactions_agg)
ORDER BY t.Total_Trans_Amt DESC
LIMIT 30;

-- Average transaction behavior by product count (does more products correlate with more activity)
SELECT a.Total_Relationship_Count,
       ROUND(AVG(t.Total_Trans_Amt), 2) AS avg_trans_amt,
       ROUND(AVG(t.Total_Trans_Ct), 1) AS avg_trans_ct,
       ROUND(AVG(a.Avg_Utilization_Ratio), 3) AS avg_utilization
FROM accounts a
JOIN transactions_agg t ON a.customer_id = t.customer_id
GROUP BY a.Total_Relationship_Count
ORDER BY a.Total_Relationship_Count;

-- Income category vs product count (are higher earners holding more products)
SELECT c.Income_Category,
       ROUND(AVG(a.Total_Relationship_Count), 2) AS avg_product_count
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.Income_Category
ORDER BY avg_product_count DESC;
