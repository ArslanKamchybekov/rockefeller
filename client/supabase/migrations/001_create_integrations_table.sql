-- Create integrations table to store OAuth tokens and integration data
CREATE TABLE IF NOT EXISTS integrations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    integration_type VARCHAR(50) NOT NULL, -- 'shopify', 'stripe', etc.
    external_id VARCHAR(255) NOT NULL, -- shop domain, account ID, etc.
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_expires_at TIMESTAMP WITH TIME ZONE,
    scopes TEXT[], -- array of granted scopes
    metadata JSONB DEFAULT '{}', -- additional integration-specific data
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_integrations_user_id ON integrations(user_id);
CREATE INDEX IF NOT EXISTS idx_integrations_type ON integrations(integration_type);
CREATE INDEX IF NOT EXISTS idx_integrations_external_id ON integrations(external_id);
CREATE INDEX IF NOT EXISTS idx_integrations_active ON integrations(is_active);

-- Create unique constraint to prevent duplicate integrations
CREATE UNIQUE INDEX IF NOT EXISTS idx_integrations_unique 
ON integrations(user_id, integration_type, external_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_integrations_updated_at 
    BEFORE UPDATE ON integrations 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE integrations ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view their own integrations" 
    ON integrations FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own integrations" 
    ON integrations FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own integrations" 
    ON integrations FOR UPDATE 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own integrations" 
    ON integrations FOR DELETE 
    USING (auth.uid() = user_id);
