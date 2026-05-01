CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    c_id INTEGER;
BEGIN
    SELECT id INTO c_id FROM contacts WHERE name = p_contact_name;
    IF c_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    INSERT INTO phones (contact_id, phone, type) VALUES (c_id, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    g_id INTEGER;
BEGIN
    -- создаем группу, если не существует
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO g_id FROM groups WHERE name = p_group_name;
    UPDATE contacts SET group_id = g_id WHERE name = p_contact_name;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
) LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name
    ORDER BY c.name;
END;
$$;