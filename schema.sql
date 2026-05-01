-- Create the schema for the Economic Resilience Project
CREATE TABLE geography (
    geo_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE labor_stats (
    stat_id SERIAL PRIMARY KEY,
    geo_id INT REFERENCES geography(geo_id),
    age_group VARCHAR(50),
    year INT,
    gender VARCHAR(50),
    employment_rate DECIMAL(5, 2),
    participation_rate DECIMAL(5, 2),
    unemployment_rate DECIMAL(5, 2),
    resilience_score DECIMAL(5, 2)
);

-- Example Query: Find the most resilient years for the 15-24 age group
SELECT year, resilience_score 
FROM labor_stats 
WHERE age_group = '15 to 24 years' 
ORDER BY resilience_score DESC 
LIMIT 5;
