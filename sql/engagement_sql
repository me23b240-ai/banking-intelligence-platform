
-- Engagement tiers by inactivity months
SELECT
  CASE
    WHEN e.Months_Inactive_12_mon <= 1 THEN 'High engagement (0-1 inactive months)'
    WHEN e.Months_Inactive_12_mon BETWEEN 2 AND 3 THEN 'Moderate engagement (2-3 inactive months)'
    ELSE 'Low engagement (4+ inactive months)'
  END AS engagement_tier,
  COUNT(*) AS customer_count,
  ROUND(AVG(t.Total_Trans_Ct), 1) AS avg_trans_count
FROM engagement e
JOIN transactions_agg t ON e.customer_id = t.customer_id
GROUP BY engagement_tier
ORDER BY customer_count DESC;

-- Engagement by tenure bracket
SELECT
  CASE
    WHEN a.Months_on_book < 24 THEN 'Under 2 years'
    WHEN a.Months_on_book BETWEEN 24 AND 36 THEN '2-3 years'
    WHEN a.Months_on_book BETWEEN 37 AND 48 THEN '3-4 years'
    ELSE '4+ years'
  END AS tenure_bracket,
  ROUND(AVG(e.Months_Inactive_12_mon), 2) AS avg_inactive_months,
  ROUND(AVG(e.Contacts_Count_12_mon), 2) AS avg_contacts
FROM accounts a
JOIN engagement e ON a.customer_id = e.customer_id
GROUP BY tenure_bracket
ORDER BY tenure_bracket;

-- Customer service contact frequency vs transaction activity (checking if high-contact customers are also low-activity)
SELECT e.Contacts_Count_12_mon,
       COUNT(*) AS customer_count,
       ROUND(AVG(t.Total_Trans_Ct), 1) AS avg_trans_count,
       ROUND(AVG(e.Months_Inactive_12_mon), 2) AS avg_inactive_months
FROM engagement e
JOIN transactions_agg t ON e.customer_id = t.customer_id
GROUP BY e.Contacts_Count_12_mon
ORDER BY e.Contacts_Count_12_mon;

-- Monthly-equivalent activity proxy: transaction count relative to tenure
SELECT c.customer_id,
       ROUND(CAST(t.Total_Trans_Ct AS FLOAT) / NULLIF(a.Months_on_book, 0), 3) AS trans_per_month,
       a.Months_on_book, t.Total_Trans_Ct
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions_agg t ON c.customer_id = t.customer_id
ORDER BY trans_per_month DESC
LIMIT 20;
