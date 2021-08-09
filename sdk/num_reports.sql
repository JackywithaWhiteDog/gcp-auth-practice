SELECT
    EXTRACT(YEAR FROM date) year,
    EXTRACT(MONTH FROM date) month,
    SUM(confirmed) num_reports
FROM `bigquery-public-data.covid19_open_data.compatibility_view`
WHERE country_region = 'Taiwan'
GROUP BY year, month
HAVING num_reports IS NOT NULL
ORDER BY year, month ASC
