-- Migration for model mappings table

CREATE TABLE IF NOT EXISTS model_mappings (
                                              id SERIAL PRIMARY KEY,
                                              pattern VARCHAR(255) NOT NULL,
    mapping VARCHAR(255) NOT NULL,
    priority INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                             );

-- Create index on pattern for faster lookups
CREATE INDEX IF NOT EXISTS idx_model_mappings_pattern ON model_mappings(pattern);

-- Create unique constraint for pattern+mapping combinations
CREATE UNIQUE INDEX IF NOT EXISTS idx_model_mappings_unique ON model_mappings(pattern, mapping);

-- Function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update the updated_at timestamp
CREATE TRIGGER update_model_mappings_timestamp
    BEFORE UPDATE ON model_mappings
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- Sample data migration function for initial setup from JSON file
CREATE OR REPLACE FUNCTION import_model_mappings_from_json(json_data JSONB)
RETURNS VOID AS $$
DECLARE
pattern_key TEXT;
    mappings JSONB;
    mapping_value TEXT;
BEGIN
    -- Loop through each key-value pair in the JSON object
FOR pattern_key, mappings IN SELECT * FROM jsonb_each(json_data) LOOP
                                           -- Loop through the array of mappings for this pattern
    FOR mapping_value IN SELECT jsonb_array_elements_text(mappings) LOOP
                             -- Insert the pattern and mapping into the model_mappings table
                             INSERT INTO model_mappings (pattern, mapping)
                             VALUES (pattern_key, mapping_value)
                             ON CONFLICT (pattern, mapping) DO NOTHING;
END LOOP;
END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Usage example:
-- SELECT import_model_mappings_from_json('{
--     "WL Grand Cherokee": [
--         "Jeep|WL|Grand Cherokee",
--         "Jeep|WL|Grand Cherokee L"
--     ]
-- }'::jsonb);

COMMENT ON TABLE model_mappings IS 'Maps vehicle model patterns found in part applications to structured make/model data';
COMMENT ON COLUMN model_mappings.pattern IS 'The pattern to match in the vehicle text (e.g., "WK Grand Cherokee")';
COMMENT ON COLUMN model_mappings.mapping IS 'The mapping in format "Make|VehicleCode|Model" (e.g., "Jeep|WK|Grand Cherokee")';
COMMENT ON COLUMN model_mappings.priority IS 'Priority for pattern matching (higher numbers are processed first)';
COMMENT ON COLUMN model_mappings.active IS 'Whether this mapping is currently active';
