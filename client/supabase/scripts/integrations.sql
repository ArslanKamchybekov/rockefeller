-- Helper functions and queries for managing integrations

-- Function to get integration by user and type
CREATE OR REPLACE FUNCTION get_integration(
    p_user_id UUID,
    p_integration_type VARCHAR(50),
    p_external_id VARCHAR(255)
)
RETURNS TABLE (
    id UUID,
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP WITH TIME ZONE,
    scopes TEXT[],
    metadata JSONB,
    is_active BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.id,
        i.access_token,
        i.refresh_token,
        i.token_expires_at,
        i.scopes,
        i.metadata,
        i.is_active,
        i.created_at,
        i.updated_at
    FROM integrations i
    WHERE i.user_id = p_user_id
        AND i.integration_type = p_integration_type
        AND i.external_id = p_external_id
        AND i.is_active = true;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to upsert integration (insert or update)
CREATE OR REPLACE FUNCTION upsert_integration(
    p_user_id UUID,
    p_integration_type VARCHAR(50),
    p_external_id VARCHAR(255),
    p_access_token TEXT,
    p_refresh_token TEXT DEFAULT NULL,
    p_token_expires_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    p_scopes TEXT[] DEFAULT NULL,
    p_metadata JSONB DEFAULT '{}'
)
RETURNS UUID AS $$
DECLARE
    integration_id UUID;
BEGIN
    INSERT INTO integrations (
        user_id,
        integration_type,
        external_id,
        access_token,
        refresh_token,
        token_expires_at,
        scopes,
        metadata
    ) VALUES (
        p_user_id,
        p_integration_type,
        p_external_id,
        p_access_token,
        p_refresh_token,
        p_token_expires_at,
        p_scopes,
        p_metadata
    )
    ON CONFLICT (user_id, integration_type, external_id)
    DO UPDATE SET
        access_token = EXCLUDED.access_token,
        refresh_token = EXCLUDED.refresh_token,
        token_expires_at = EXCLUDED.token_expires_at,
        scopes = EXCLUDED.scopes,
        metadata = EXCLUDED.metadata,
        is_active = true,
        updated_at = NOW()
    RETURNING id INTO integration_id;
    
    RETURN integration_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to deactivate integration
CREATE OR REPLACE FUNCTION deactivate_integration(
    p_user_id UUID,
    p_integration_type VARCHAR(50),
    p_external_id VARCHAR(255)
)
RETURNS BOOLEAN AS $$
BEGIN
    UPDATE integrations 
    SET is_active = false, updated_at = NOW()
    WHERE user_id = p_user_id
        AND integration_type = p_integration_type
        AND external_id = p_external_id;
    
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get all active integrations for a user
CREATE OR REPLACE FUNCTION get_user_integrations(p_user_id UUID)
RETURNS TABLE (
    id UUID,
    integration_type VARCHAR(50),
    external_id VARCHAR(255),
    scopes TEXT[],
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.id,
        i.integration_type,
        i.external_id,
        i.scopes,
        i.metadata,
        i.created_at,
        i.updated_at
    FROM integrations i
    WHERE i.user_id = p_user_id
        AND i.is_active = true
    ORDER BY i.created_at DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Example usage queries:

-- Get Shopify integration for a user
-- SELECT * FROM get_integration('user-uuid', 'shopify', 'my-store.myshopify.com');

-- Upsert a new Shopify integration
-- SELECT upsert_integration(
--     'user-uuid',
--     'shopify',
--     'my-store.myshopify.com',
--     'shpat_abc123...',
--     NULL,
--     NULL,
--     ARRAY['read_products', 'write_products'],
--     '{"shop_name": "My Store", "plan": "basic"}'::jsonb
-- );

-- Get all integrations for a user
-- SELECT * FROM get_user_integrations('user-uuid');

-- Deactivate an integration
-- SELECT deactivate_integration('user-uuid', 'shopify', 'my-store.myshopify.com');
