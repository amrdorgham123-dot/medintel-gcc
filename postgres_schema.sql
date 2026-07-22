CREATE TABLE manufacturers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    headquarters TEXT,
    website TEXT,
    portfolio TEXT,
    ksa_status TEXT,
    status_tag TEXT CHECK(status_tag IN ('covered','unclear','open')),
    opportunity_note TEXT,
    confidence_tier TEXT CHECK(confidence_tier IN ('gold','silver','bronze')),
    sources TEXT,
    category TEXT DEFAULT 'Blood Bank',
    is_published INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    verified_by TEXT DEFAULT 'manual research, see sources',
    origin TEXT,
    phone TEXT,
    email TEXT,
    contact_url TEXT
, slug TEXT);

CREATE TABLE technologies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE manufacturer_technology (
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    technology_id INTEGER REFERENCES technologies(id) ON DELETE CASCADE,
    PRIMARY KEY (manufacturer_id, technology_id)
);

CREATE TABLE distributors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT,
    represents TEXT,
    source TEXT,
    market_strength_tier TEXT,
    market_strength_basis TEXT,
    contact_info TEXT
);

CREATE TABLE conferences (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    event_date TEXT NOT NULL,
    place TEXT,
    tag TEXT,
    source TEXT
, created_at TEXT);

CREATE TABLE opportunities (
    id SERIAL PRIMARY KEY,
    manufacturer_id INTEGER REFERENCES manufacturers(id),
    reason TEXT,
    action TEXT,
    score_no_distributor INTEGER,
    score_confidence INTEGER,
    score_brand INTEGER
, created_at TEXT);

CREATE TABLE attieh_portfolio (
    id SERIAL PRIMARY KEY,
    manufacturer TEXT NOT NULL,
    domain TEXT,
    country TEXT,
    tender_reference TEXT,
    source TEXT
);

CREATE TABLE tenders (
    id SERIAL PRIMARY KEY,
    tender_ref TEXT NOT NULL,
    tender_name TEXT,
    category TEXT,
    source TEXT
);

CREATE TABLE hospitals (
    id SERIAL PRIMARY KEY,
    abbreviation TEXT NOT NULL,
    full_name TEXT,
    notable_equipment TEXT,
    source TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    product_name TEXT NOT NULL,
    product_type TEXT,
    description TEXT,
    source TEXT,
    department TEXT,
    throughput TEXT,
    sample_types TEXT,
    certifications TEXT,
    brochure_url TEXT
, image_url TEXT, specs_json TEXT);

CREATE TABLE distributor_products (
    id SERIAL PRIMARY KEY,
    distributor_name TEXT,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    source TEXT
);

CREATE TABLE market_events (
    id SERIAL PRIMARY KEY,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    event_type TEXT,
    event_date TEXT,
    description TEXT,
    source TEXT
);

CREATE TABLE evidence (
    id SERIAL PRIMARY KEY,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    claim TEXT NOT NULL,
    evidence_type TEXT,
    source_detail TEXT,
    reviewed_date TEXT DEFAULT '2026-07-05'
);

CREATE TABLE regulatory_status (
    id SERIAL PRIMARY KEY,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    regulatory_body TEXT NOT NULL,
    status TEXT NOT NULL,
    detail TEXT,
    source TEXT
);

CREATE TABLE company_distributors (
    id SERIAL PRIMARY KEY,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    distributor_id INTEGER REFERENCES distributors(id) ON DELETE CASCADE, created_at TEXT,
    UNIQUE(manufacturer_id, distributor_id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    company_name TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'user' CHECK(role IN ('admin','user')),
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text
);

CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    contact_name TEXT,
    contact_role TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    status TEXT DEFAULT 'new' CHECK(status IN ('new','contacted','in_progress','won','lost')),
    notes TEXT,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text
);

CREATE TABLE lead_interactions (
    id SERIAL PRIMARY KEY,
    lead_id INTEGER REFERENCES leads(id) ON DELETE CASCADE,
    interaction_type TEXT CHECK(interaction_type IN ('call','email','meeting','note')),
    summary TEXT NOT NULL,
    interaction_date TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    next_followup_date TEXT
);

CREATE TABLE watchlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    added_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    UNIQUE(user_id, manufacturer_id)
);

CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name TEXT,
    record_id INTEGER,
    action TEXT,
    detail TEXT,
    timestamp TEXT DEFAULT (CURRENT_TIMESTAMP)::text
);

CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    patient_code TEXT UNIQUE,
    full_name TEXT NOT NULL,
    gender TEXT,
    age INTEGER,
    department TEXT,
    visit_type TEXT DEFAULT 'Outpatient',
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    created_by TEXT
);

CREATE TABLE patient_visits (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    visit_time TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    visit_type TEXT,
    notes TEXT
);

CREATE TABLE patient_reports (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    file_name TEXT,
    uploaded_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text
);

CREATE TABLE patient_chat_messages (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text
);

CREATE TABLE lab_tests (
    id SERIAL PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    name_en TEXT NOT NULL,
    name_ar TEXT NOT NULL,
    aliases TEXT,
    category TEXT NOT NULL,
    purpose_en TEXT,
    purpose_ar TEXT,
    specimen_type TEXT,
    collection_notes_en TEXT,
    collection_notes_ar TEXT,
    methodology_en TEXT,
    methodology_ar TEXT,
    reference_ranges_json TEXT,
    reference_ranges_verified INTEGER DEFAULT 0,
    clinical_significance_en TEXT,
    clinical_significance_ar TEXT,
    associated_conditions_json TEXT,
    sources_json TEXT NOT NULL,
    is_published INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    updated_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text
, related_tests_json TEXT DEFAULT '[]', critical_values_en TEXT, interfering_factors_en TEXT, questions_to_ask_en TEXT, next_steps_en TEXT);

CREATE TABLE order_sets (
    id SERIAL PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    name_en TEXT NOT NULL,
    description_en TEXT,
    category TEXT,
    test_slugs_json TEXT NOT NULL,
    is_published INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text
);

CREATE TABLE whatsapp_messages (
    id SERIAL PRIMARY KEY,
    phone_number TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user','assistant')),
    content TEXT NOT NULL,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text
);

CREATE TABLE company_settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    plan TEXT NOT NULL DEFAULT 'trial',
    status TEXT NOT NULL DEFAULT 'trialing',
    started_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    current_period_end TEXT,
    granted_by TEXT,
    grant_note TEXT,
    stripe_customer_id TEXT,
    stripe_subscription_id TEXT,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    updated_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE notification_reads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    notification_key TEXT NOT NULL,
    read_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    UNIQUE(user_id, notification_key),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    key_hash TEXT NOT NULL UNIQUE,
    key_prefix TEXT NOT NULL,
    label TEXT,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    last_used_at TEXT,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE demo_requests (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    company_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    message TEXT,
    plan_interest TEXT,
    status TEXT DEFAULT 'new',
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text
);

CREATE TABLE password_resets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    used INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (CURRENT_TIMESTAMP)::text,
    FOREIGN KEY(user_id) REFERENCES users(id)
);