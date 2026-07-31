-- company's table
CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    city TEXT NOT NULL,
    address TEXT,
    rating REAL,
    reviews_count INTEGER DEFAULT 0,
    site TEXT,
    phone TEXT
);


-- index
CREATE INDEX IF NOT EXISTS idx_companies_category ON companies (category);
CREATE INDEX IF NOT EXISTS idx_companies_city ON companies (city);
CREATE INDEX IF NOT EXISTS idx_companies_rating ON companies (rating);
CREATE INDEX IF NOT EXISTS idx_companies_reviews_count ON companies (reviews_count);