-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS market_data;
CREATE SCHEMA IF NOT EXISTS research;
CREATE SCHEMA IF NOT EXISTS portfolio;
CREATE SCHEMA IF NOT EXISTS audit;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA market_data TO agentplayground;
GRANT ALL PRIVILEGES ON SCHEMA research TO agentplayground;
GRANT ALL PRIVILEGES ON SCHEMA portfolio TO agentplayground;
GRANT ALL PRIVILEGES ON SCHEMA audit TO agentplayground;

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';
