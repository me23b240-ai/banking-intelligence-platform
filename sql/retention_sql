
-- Overall churn rate (baseline, should match 16.06% from earlier)
SELECT Attrition_Flag, COUNT(*) AS customer_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM churn_outcome), 2) AS pct
FROM churn_outcome
GROUP BY Attrition_Flag;

-- Churn rate by age bracket
SELECT
  CASE
    WHEN c.Customer_Age < 30 THEN 'Under 30'
    WHEN c.Customer_Age BETWEEN 30 AND 39 THEN '30-39'
    WHEN c.Customer_Age BETWEEN 40 AND 49 THEN '40-49'
    WHEN c.Customer_Age BETWEEN 50 AND 59 THEN '50-59'
    ELSE '60+'
  END AS age_bracket,
  COUNT(*) AS total_customers,
  SUM(CASE WHEN ch.Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) AS churned,
  ROUND(100.0 * SUM(CASE WHEN ch.Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN churn_outcome ch ON c.customer_id = ch.customer_id
GROUP BY age_bracket
ORDER BY churn_rate_pct DESC;

-- Churn rate by product count (Total_Relationship_Count)
SELECT a.Total_Relationship_Count,
       COUNT(*) AS total_customers,
       SUM(CASE WHEN ch.Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) AS churned,
       ROUND(100.0 * SUM(CASE WHEN ch.Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM accounts a
JOIN churn_outcome ch ON a.customer_id = ch.customer_id
GROUP BY a.Total_Relationship_Count
ORDER BY a.Total_Relationship_Count;

-- Churn rate by tenure bracket
SELECT
  CASE
    WHEN a.Months_on_book < 24 THEN 'Under 2 years'
    WHEN a.Months_on_book BETWEEN 24 AND 36 THEN '2-3 years'
    WHEN a.Months_on_book BETWEEN 37 AND 48 THEN '3-4 years'
    ELSE '4+ years'
  END AS tenure_bracket,
  COUNT(*) AS total_customers,
  ROUND(100.0 * SUM(CASE WHEN ch.Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM accounts a
JOIN churn_outcome ch ON a.customer_id = ch.customer_id
GROUP BY tenure_bracket
ORDER BY tenure_bracket;

-- Churn rate by inactivity (testing the industry research finding directly on our data)
SELECT e.Months_Inactive_12_mon,
       COUNT(*) AS total_customers,
       ROUND(100.0 * SUM(CASE WHEN ch.Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM engagement e
JOIN churn_outcome ch ON e.customer_id = ch.customer_id
GROUP BY e.Months_Inactive_12_mon
ORDER BY e.Months_Inactive_12_mon;

-- Churn rate by customer service contact count
SELECT e.Contacts_Count_12_mon,
       COUNT(*) AS total_customers,
       ROUND(100.0 * SUM(CASE WHEN ch.Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM engagement e
JOIN churn_outcome ch ON e.customer_id = ch.customer_id
GROUP BY e.Contacts_Count_12_mon
ORDER BY e.Contacts_Count_12_mon;

-- Churn rate by card category
SELECT a.Card_Category,
       COUNT(*) AS total_customers,
       ROUND(100.0 * SUM(CASE WHEN ch.Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM accounts a
JOIN churn_outcome ch ON a.customer_id = ch.customer_id
GROUP BY a.Card_Category
ORDER BY churn_rate_pct DESC;

-- Compound risk: age 50+ AND high inactivity (testing the research finding about compounding effect)
SELECT
  CASE WHEN c.Customer_Age >= 50 THEN '50+' ELSE 'Under 50' END AS age_group,
  CASE WHEN e.Months_Inactive_12_mon >= 3 THEN 'High inactivity (3+)' ELSE 'Low inactivity (<3)' END AS inactivity_group,
  COUNT(*) AS total_customers,
  ROUND(100.0 * SUM(CASE WHEN ch.Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers c
JOIN engagement e ON c.customer_id = e.customer_id
JOIN churn_outcome ch ON c.customer_id = ch.customer_id
GROUP BY age_group, inactivity_group
ORDER BY churn_rate_pct DESC;
