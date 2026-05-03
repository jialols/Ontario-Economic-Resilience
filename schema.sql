-- Schema for the Ontario Economic Resilience Project

-- Geography dimension: allows extension beyond Ontario if needed.
CREATE TABLE geography (
    geo_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Fact table: labour statistics and resilience score by geography, age group, year, and gender.
CREATE TABLE labor_stats (
    stat_id SERIAL PRIMARY KEY,
    geo_id INT NOT NULL REFERENCES geography(geo_id),
    age_group VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    gender VARCHAR(50) NOT NULL,
    employment_rate DECIMAL(5, 2),
    participation_rate DECIMAL(5, 2),
    unemployment_rate DECIMAL(5, 2),
    resilience_score DECIMAL(6, 2)
);

-- Optional: index to speed up common analytical queries by age group and year.
CREATE INDEX idx_labor_stats_age_year
    ON labor_stats (age_group, year);

-- Optional: index for geography-based queries.
CREATE INDEX idx_labor_stats_geo
    ON labor_stats (geo_id);

-- Example analytical query:
-- Find the most resilient years for the 15–24 age group.
SELECT
    year,
    resilience_score
FROM labor_stats
WHERE age_group = '15 to 24 years'
ORDER BY resilience_score DESC
LIMIT 5;
