"""
MedIntel GCC — database initializer.
Creates a real SQLite file on disk (medintel.db) and seeds it with only the
data we actually verified in conversation. Run once: python init_db.py
"""
import sqlite3
import os
import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    verified_by TEXT DEFAULT 'manual research, see sources',
    origin TEXT,
    phone TEXT,
    email TEXT,
    contact_url TEXT
);

CREATE TABLE IF NOT EXISTS technologies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS manufacturer_technology (
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    technology_id INTEGER REFERENCES technologies(id) ON DELETE CASCADE,
    PRIMARY KEY (manufacturer_id, technology_id)
);

CREATE TABLE IF NOT EXISTS distributors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT,
    represents TEXT,
    source TEXT,
    market_strength_tier TEXT,
    market_strength_basis TEXT,
    contact_info TEXT
);

CREATE TABLE IF NOT EXISTS conferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    event_date TEXT NOT NULL,
    place TEXT,
    tag TEXT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER REFERENCES manufacturers(id),
    reason TEXT,
    action TEXT,
    score_no_distributor INTEGER,
    score_confidence INTEGER,
    score_brand INTEGER
);



CREATE TABLE IF NOT EXISTS attieh_portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT NOT NULL,
    domain TEXT,
    country TEXT,
    tender_reference TEXT,
    source TEXT
);


CREATE TABLE IF NOT EXISTS tenders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tender_ref TEXT NOT NULL,
    tender_name TEXT,
    category TEXT,
    source TEXT
);


CREATE TABLE IF NOT EXISTS hospitals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    abbreviation TEXT NOT NULL,
    full_name TEXT,
    notable_equipment TEXT,
    source TEXT
);


CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
);

CREATE TABLE IF NOT EXISTS distributor_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    distributor_name TEXT,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    source TEXT
);


CREATE TABLE IF NOT EXISTS market_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    event_type TEXT,
    event_date TEXT,
    description TEXT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    claim TEXT NOT NULL,
    evidence_type TEXT,
    source_detail TEXT,
    reviewed_date TEXT DEFAULT '2026-07-05'
);

CREATE TABLE IF NOT EXISTS regulatory_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    regulatory_body TEXT NOT NULL,
    status TEXT NOT NULL,
    detail TEXT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS company_distributors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    distributor_id INTEGER REFERENCES distributors(id) ON DELETE CASCADE,
    UNIQUE(manufacturer_id, distributor_id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    company_name TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'user' CHECK(role IN ('admin','user')),
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    contact_name TEXT,
    contact_role TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    status TEXT DEFAULT 'new' CHECK(status IN ('new','contacted','in_progress','won','lost')),
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lead_interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER REFERENCES leads(id) ON DELETE CASCADE,
    interaction_type TEXT CHECK(interaction_type IN ('call','email','meeting','note')),
    summary TEXT NOT NULL,
    interaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
    next_followup_date TEXT
);

CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    manufacturer_id INTEGER REFERENCES manufacturers(id) ON DELETE CASCADE,
    added_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, manufacturer_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT,
    record_id INTEGER,
    action TEXT,
    detail TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

def seed(conn):
    cur = conn.cursor()

    manufacturers = [
        ("Grifols", "Spain", "grifols.com/en/saudi-arabia",
         "Blood grouping reagents, plasma-derived medicines, transfusion diagnostics",
         "Covered — direct Grifols office in Riyadh (since 2019) + local partner AFMS",
         "covered", "Low — already present directly", "gold",
         "grifols.com/en/saudi-arabia; afmssc.com distributor page", "Blood Bank"),
        ("Werfen (Transfusion & Transplant division)", "Spain", "transfusionandtransplant.werfen.com",
         "Immunohematology reagents & automation, HLA/transplant diagnostics",
         "Unconfirmed — regional office in Dubai, no named KSA distributor",
         "unclear", "Medium — worth direct outreach", "silver",
         "werfen.com company/office pages", "Blood Bank"),
        ("Immucor (acquired by Werfen, 2023)", "USA (now part of Werfen, Spain)", "immucor.com (redirects to Werfen transfusion/transplant division)",
         "Immunohematology reagents & automation (Capture, Echo, NEO) -- now operated under Werfen's Transfusion & Transplant division",
         "CORRECTED: Immucor's own contact page now redirects to Werfen's site. No longer independent -- any KSA question should route through Werfen, same as the existing Werfen entry",
         "unclear", "Medium -- same opportunity as Werfen entry, not a separate lead. Do NOT approach as independent.", "gold",
         "SEC Form 8-K (Neogen Corp, filed Aug 2025) explicitly states Immucor was acquired by Werfen in 2023; immucor.com contact page redirects to transfusionandtransplant.werfen.com", "Blood Bank"),
        ("Macopharma", "France", "macopharma.com",
         "Blood bag systems, apheresis, blood collection & processing devices",
         "Covered — Samir Group (KSA) confirmed distributor for Macolounge line",
         "covered", "Low — already covered", "gold",
         "macopharma.com; samirgroup.com", "Blood Bank"),
        ("Lorne Laboratories (part of Calibre Scientific)", "United Kingdom", "lornelabs.com",
         "Blood grouping reagents (ABO/Rh/Kell/rare), Coombs cells, diagnostic kits",
         "Covered — GAMSCO Medical (Dammam, since 2008) is confirmed official KSA distributor",
         "covered", "Low as fresh lead — relevant to active outreach with Lorne", "gold",
         "lornelabs.com/distributors/saudi-arabia; calibrescientificgroup.com", "Blood Bank"),
        ("Teleflex", "USA", "teleflex.com",
         "Diversified medtech; vascular access & blood-collection-adjacent lines",
         "Saudi Medical Services confirmed only for LMA/airway line — transfusion line unconfirmed",
         "unclear", "Unclear — needs direct clarification from EMEA office", "silver",
         "lmaco.com/distributors/saudi-medical-services", "Blood Bank"),
        ("Diagnostica Stago", "France", "stago.com",
         "Hemostasis/coagulation analyzers and reagents (STA range), thrombosis diagnostics",
         "Covered — Stago has its own direct KSA affiliate office in Riyadh, opened 2020 (not a third-party distributor)",
         "covered", "Low — already present directly, same pattern as Grifols", "gold",
         "stago.com/worldwide/distributors + stago.com affiliate directory listing Riyadh address; cross-validated via NUPCO Tender NPT0038/24 which lists 'Diagnostic Saudi Arabia Trading Com' as the awarded vendor for Stago's STA/StheMO reagent lines -- same KSA entity, not a third-party distributor", "Coagulation"),
    ]
    cur.executemany(
        """INSERT INTO manufacturers
           (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        manufacturers
    )

    technologies = [
        ("Blood grouping reagents (ABO/Rh/Kell/rare)", "Manual/serology-based antigen typing reagents"),
        ("Coombs / antiglobulin testing", "Antibody screening and crossmatch support reagents"),
        ("Immunohematology automation platforms", "Automated instruments for blood typing/antibody screening — specific brand/model names not yet verified"),
        ("Blood bag & apheresis systems", "Collection, processing, and storage devices for donated blood"),
        ("Plasma-derived therapeutics", "Medicines manufactured from donated plasma"),
        ("NAT / molecular blood screening", "Nucleic acid testing for transfusion-transmitted infections (HBV/HCV/HIV), run on automated molecular platforms"),
    ]
    cur.executemany("INSERT INTO technologies (name, description) VALUES (?,?)", technologies)

    tech_to_id_static = {row[0]: i+1 for i, row in enumerate(technologies)}

    distributors = [
        ("GAMSCO Medical", "Saudi Arabia (Dammam)", "Lorne Laboratories (since 2008)", "lornelabs.com/distributors/saudi-arabia",
         "Tenure-verified", "18-year continuous relationship with Lorne (2008-2026) is a real, sourced stability signal. We have NOT verified how many other principals GAMSCO carries -- do not read this as overall company size or market share, only as evidence this specific relationship is durable."),
        ("Samir Trading & Marketing (also known as Samir Group)", "Saudi Arabia", "Macopharma, Ortho Clinical Diagnostics (Vision/MAX line), HORIBA Medical (Yumizen/Pentra/Micros)", "samirgroup.com",
         "Tenure-verified (partial)", "THREE confirmed principals now via NUPCO tender award records -- among the broadest portfolios in this dataset. Still not independently confirmed for overall company size or revenue."),
        ("AFMS", "Saudi Arabia (Riyadh)", "Grifols (secondary channel) and Hologic (primary molecular diagnostics distributor)", "afmssc.com",
         "Tenure-verified (partial)", "Two confirmed principals now (Grifols and Hologic, same Riyadh address) -- more breadth than most other distributors in this dataset, though still not a full picture of AFMS's total portfolio or size."),
        ("Saudi Medical Services", "Saudi Arabia", "Teleflex — LMA/airway line only (not transfusion line)", "lmaco.com/distributors/saudi-medical-services",
         "Insufficient data", "Only confirmed for one specific Teleflex product line (LMA/airway). Do not extrapolate to overall company size."),
        ("Ali Al-Suwaidi Trading Est.", "Qatar (not KSA)", "Lorne Laboratories — Qatar market only", "lornelabs.com/distributors/qatar",
         "Not applicable", "Operates in Qatar, not Saudi Arabia -- included for regional context only, not part of the KSA market-strength comparison."),
    ]
    cur.executemany("INSERT INTO distributors (name, country, represents, source, market_strength_tier, market_strength_basis) VALUES (?,?,?,?,?,?)", distributors)

    conferences = [
        ("Emirates Haematology Conference (14th ed.)", "2026-09-04", "Dubai, UAE", "Blood Bank / Hematology", "ehc-uae.com (fetched directly)"),
        ("ARABLAB LIVE 2026", "2026-10-26", "Dubai, UAE", "Lab Equipment / IVD", "Dubai World Trade Centre listing + Terrapinn"),
        ("WHX Labs Dubai 2027", "2027-01-26", "Dubai, UAE", "IVD / Lab Equipment", "worldhealthexpo.com official page"),
        ("Pan Arab Blood Transfusion Conference (PABT) — 15th ed.", "2026-01-18", "Kuwait City, Kuwait", "Blood Bank / Transfusion", "pabt2026.com + dated social post confirming conclusion"),
        ("LABNEXT 2026", "2026-04-29", "Jazan, Saudi Arabia", "Lab / Blood Bank", "jazanlab.sa target date, no 2027 edition announced"),
    ]
    cur.executemany("INSERT INTO conferences (name, event_date, place, tag, source) VALUES (?,?,?,?,?)", conferences)


    evidence_rows = [
        (1, "Grifols has its own KSA representation office", "official company page", "grifols.com/en/saudi-arabia — office listed since 2019"),
        (1, "AFMS also distributes Grifols products in Riyadh", "distributor's own website", "afmssc.com distributor product listing"),
        (1, "Grifols NAT reagents (Panther platform) confirmed via Abdulla Fouad for medical supplies for malaria and HBV/HCV/HIV NAT screening", "primary government source", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025), items 596 and 600"),
        (2, "Werfen has a Dubai regional office covering EMEA", "official company page", "werfen.com contact/office directory"),
        (2, "No KSA-specific distributor named for Werfen transfusion line", "absence check — searched, found nothing", "general web search, no contradicting result"),
        (3, "No KSA distributor found for Immucor (this specific finding was later superseded, see below)", "absence check — searched official site + web", "immucor.com + general web search, no contradicting result"),
        (3, "Immucor was acquired by Werfen in 2023 and is no longer an independent company", "SEC filing (independent third party)", "Neogen Corp Form 8-K, filed Aug 2025, states former Immucor CEO led its turnaround and acquisition by Werfen in 2023"),
        (3, "Immucor's official contact page now redirects to Werfen's site", "official company page redirect", "immucor.com/en-us/About redirects to transfusionandtransplant.werfen.com"),
        (4, "Samir Group confirmed as Macopharma KSA distributor", "distributor's own website", "samirgroup.com Macolounge product listing"),
        (5, "GAMSCO Medical confirmed as Lorne Laboratories KSA distributor since 2008", "manufacturer's own distributor page", "lornelabs.com/distributors/saudi-arabia"),
        (5, "Lorne Laboratories was acquired by Calibre Scientific", "acquirer's own announcement", "calibrescientificgroup.com acquisition notice"),
        (6, "Saudi Medical Services confirmed as distributor for Teleflex LMA/airway line only", "Teleflex-owned brand site", "lmaco.com/distributors/saudi-medical-services"),
    ]
    cur.executemany(
        "INSERT INTO evidence (manufacturer_id, claim, evidence_type, source_detail) VALUES (?,?,?,?)",
        evidence_rows
    )


    attieh_rows = [
        ("Hamilton Thorne", "IVF / Andrology (CASA analyzers, lasers)", "USA", "NPT0028/22, NPT0007/21, NPT0009/18, IVF Clinics Lab Supplies", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Cooper Surgical", "IVF media, consumables, vitrification kits", "Denmark/Costa Rica", "NPT0019/20, NPT0011/21, NPT0033-22", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Vitrolife", "IVF culture media", "Denmark", "IVF Clinics Lab Supplies, IVF Tender", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Carl Zeiss", "Microscopy (IVF, cytogenetics, hematology)", "Germany", "NPT0007/21, NPT0009/18, NPT0011/21, NPT 0013-19, NPT 0050/20", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("MetaSystems", "Cytogenetics imaging & FISH probes", "Germany", "NPT 0013-19, NPT0026/21, LAB Tender Batch 3/5", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Planer", "Cryopreservation / embryo freezers", "UK", "NPT0009/18, IVF Clinics Lab Supplies, IVF Supplementary Tender", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("MVE Biological Solutions", "Liquid nitrogen storage/dewars", "USA", "NPT0007/21, NPT0028/22, IVF Supplementary Tender", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Azbil Telstar", "Biosafety cabinets, freeze dryers", "Spain", "NPT 0013-19, NPT0028/22, NPT0007/21", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Desmon Scientific", "Cold rooms, lab freezers", "Italy", "NPT 0013-19, NPT0013/20", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Gonotec", "Osmometers", "Germany", "NPT0009/18, NPT0011/21", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Cryologic", "Vitrification / cryobaths", "Australia", "NPT0028/22", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Sparmed", "IVF cryo consumables/tags", "Denmark", "IVF Supplementary Tender, IVF Clinics Lab Supplies", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Cryobiosystem", "Vitrification devices", "USA/France", "IVF Supplementary Tender", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Deltalab", "General lab plasticware", "Spain", "LAB Tender Batch 3/5", "NUPCO Final Awardation records, vendor = Attieh Medico"),
        ("Memmert", "Lab water baths/incubators", "Germany", "NPT0028/22, NPT0007/21", "NUPCO Final Awardation records, vendor = Attieh Medico"),
    ]
    cur.executemany(
        "INSERT INTO attieh_portfolio (manufacturer, domain, country, tender_reference, source) VALUES (?,?,?,?,?)",
        attieh_rows
    )


    nupco_manufacturers = [
        # (name, hq_guess, website_placeholder, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category)
        ("Bio-Rad (IH-1000/IH-500 line)", "USA/Switzerland", "bio-rad.com", "Immunohematology cards/gel cards, coagulation controls", "Covered — Abdulrehman Algosaibi GTC confirmed as NUPCO-awarded vendor across dozens of blood bank line items", "covered", "Low — deeply entrenched, largest single vendor share in this tender", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025), primary government source", "Blood Bank"),
        ("Ortho Clinical Diagnostics (Vision/MAX line)", "USA", "orthoclinicaldiagnostics.com", "Blood grouping cards, antibody screening/ID kits", "Covered — Samir Trading & Marketing confirmed NUPCO-awarded vendor", "covered", "Low — large confirmed presence", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Blood Bank"),
        ("Diagast", "France", "diagast.com", "Blood grouping reagents (vials)", "Covered — Arabian Trade House confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Blood Bank"),
        ("Terumo BCT", "USA/Japan", "terumobct.com", "Apheresis systems (Trima Accel, Spectra Optia), pathogen reduction (Mirasol)", "Covered — Abdulrehman Algosaibi GTC confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Blood Bank"),
        ("Haemonetics", "USA", "haemonetics.com", "Apheresis systems (MCS+, ACP215), bacterial detection (EBDS)", "Covered — Arabian Trade House confirmed NUPCO-awarded vendor (consistent with earlier web research)", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025); cross-validated with independent web research", "Blood Bank"),
        ("Cerus Corporation", "USA", "cerus.com", "Pathogen reduction technology (INTERCEPT)", "Covered — Arabian medical house company confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Blood Bank"),
        ("Roche Diagnostics (NAT/Molecular line)", "Switzerland", "diagnostics.roche.com", "NAT/molecular testing (HBV/HCV/HIV on Cobas 6800/5800, Modules S201) -- also supplies coagulation reagents (Cobas T711) under the same KSA entity", "Covered — Roche Diagnostics Saudi Arabia LLC (direct subsidiary), confirmed NUPCO-awarded vendor for both product lines", "covered", "Low — direct Roche entity", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Molecular Diagnostics"),
        ("Sysmex", "Japan", "sysmex.com", "Hematology analyzers (XN series), also distributes some Siemens coagulation reagents in KSA", "Covered — Sysmex LLC Company (One Person Company, i.e. direct KSA entity), confirmed NUPCO-awarded vendor", "covered", "Low — direct entity", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Hematology"),
        ("Mindray", "China", "mindray.com", "Hematology analyzers (BC-6200/6800 series)", "Covered — Abdulla Fouad for medical supplies confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Hematology"),
        ("Beckman Coulter", "USA", "beckmancoulter.com", "Hematology analyzers (DxH series), chemistry (AU/DxC)", "Covered — Beckman Coulter Saudi Arabia Co. Ltd (direct entity) + Dar Al-Zahrawi Medical Company for some hematology lines", "covered", "Low — direct entity + secondary distributor", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Hematology"),
        ("Abbott Core Diagnostics", "USA", "abbott.com", "Hematology (Alinity HQ/CellDyn), infectious disease (Alinity S)", "Covered — Medical Supplies & Services Co Ltd confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Hematology"),
        ("Siemens Healthineers", "Germany", "siemens-healthineers.com", "Hematology (ADVIA, Atellica), coagulation (BCS XP, CA series), platelet function (PFA)", "Covered — Abdulrehman Algosaibi GTC (primary) + Sysmex LLC Company (secondary, for some coagulation reagents)", "covered", "Low — deeply entrenched, dual distribution", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Hematology"),
        ("HORIBA Medical", "France", "horiba.com", "Hematology analyzers (Yumizen, Pentra, Micros series)", "Covered — Samir Trading & Marketing confirmed NUPCO-awarded vendor (consistent with earlier memory: SAMIR Trading covers hematology/hemostasis)", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025); cross-validated with prior research", "Hematology"),
        ("Tosoh", "Japan", "tosoh.com", "Hb electrophoresis / HbA1c analyzers (G8/G11)", "Covered — Abdulla Fouad for medical supplies confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Hematology"),
        ("Sebia", "France", "sebia.com", "Hb electrophoresis (capillary electrophoresis systems)", "Covered — Abdulla Fouad for medical supplies confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Hematology"),
        ("Alcor Scientific", "USA", "alcorscientific.com", "ESR analyzers (miniiSED i-SED)", "Covered — Dar Al-Zahrawi Medical Company confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Hematology"),
        ("Werfen (ACL/hemostasis line)", "Spain/USA", "werfen.com", "Coagulation analyzers (ACL series), factor assays, D-dimer", "Covered in this specific tender — Abdulla Fouad for medical supplies confirmed NUPCO-awarded vendor for ACL line (note: this is a DIFFERENT KSA vendor than Werfen's Dubai regional office finding from earlier web research — real-world companies often use more than one channel per product line)", "covered", "Low for this product line — already distributed", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Coagulation"),
        ("Tcoag Ireland Limited (a Stago Group company)", "Ireland", "stago.com", "Platelet aggregation reagents (Thrombo Aggregometer)", "Covered — Diagnostic Saudi Arabia Trading Com confirmed NUPCO-awarded vendor (same entity as parent Stago)", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Coagulation"),
        ("Chrono-log", "USA", "chrono-log.com", "Platelet aggregation reagents/analyzers", "Covered — Dar Al-Zahrawi Medical Company confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Coagulation"),
        ("bioMerieux (Vidas line)", "France", "biomerieux.com", "D-dimer testing (Vidas platform)", "Covered — Al-Jeel Medical & Trading Co. Ltd confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Coagulation"),
        ("Miltenyi Biotec", "Germany", "miltenyibiotec.com", "Stem cell selection (CliniMACS), cryopreservation bags", "Covered — HOME OF GULF ELITE EST. confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Stem Cell"),
        ("Fresenius Kabi (blood bag line)", "Germany", "fresenius-kabi.com", "Blood collection bags, bone marrow collection kits", "Covered — Abdulla Fouad for medical supplies (primary) + Arabian Trade House (secondary, for some bag configurations)", "covered", "Low — dual distribution", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Blood Bank"),
        ("Demophorius", "China (manufacturing)/Cyprus (HQ)", "demophorius.com", "Blood collection bags", "Covered — Arabian Medical and Pharmaceutical Co. confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Blood Bank"),
        ("JMS (blood bag line)", "Singapore/Japan", "jms.cc", "Blood collection/transfer bags", "Covered — Farabi Trading Establishment confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Blood Bank"),
        ("Streck", "USA", "streck.com", "Sickle cell screening controls", "Covered — Samir Trading & Marketing confirmed NUPCO-awarded vendor", "covered", "Low", "gold", "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025)", "Hematology"),
        ("Hologic", "USA", "hologic.com", "Molecular diagnostics instrumentation (Panther/Tigris platforms -- runs Grifols' Procleix NAT assays), cytology (ThinPrep)", "Covered -- AFMS (Riyadh) confirmed as official KSA distributor, same entity that also represents Grifols", "covered", "Low -- confirmed distributor relationship", "gold", "afmssc.com/hologic dedicated distributor page (Salah Alden Road, Al Zahra District, Riyadh)", "Molecular Diagnostics"),
    ]
    cur.executemany(
        """INSERT INTO manufacturers
           (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        nupco_manufacturers
    )

    # Rebuild name_to_id from the DB now that ALL manufacturers (original + NUPCO batch) exist
    name_to_id = {row[1]: row[0] for row in cur.execute("SELECT id, name FROM manufacturers").fetchall()}
    tech_to_id = tech_to_id_static
    links = [
        ("Grifols", "Blood grouping reagents (ABO/Rh/Kell/rare)"),
        ("Grifols", "Plasma-derived therapeutics"),
        ("Lorne Laboratories (part of Calibre Scientific)", "Blood grouping reagents (ABO/Rh/Kell/rare)"),
        ("Lorne Laboratories (part of Calibre Scientific)", "Coombs / antiglobulin testing"),
        ("Macopharma", "Blood bag & apheresis systems"),
        ("Immucor (acquired by Werfen, 2023)", "Immunohematology automation platforms"),
        ("Werfen (Transfusion & Transplant division)", "Immunohematology automation platforms"),
        ("Roche Diagnostics (NAT/Molecular line)", "NAT / molecular blood screening"),
        ("Grifols", "NAT / molecular blood screening"),
    ]
    cur.executemany(
        "INSERT INTO manufacturer_technology (manufacturer_id, technology_id) VALUES (?,?)",
        [(name_to_id[c], tech_to_id[t]) for c, t in links]
    )

    market_size_evidence = [
        ("Roche Diagnostics (NAT/Molecular line)", "NUPCO 2024 tender requested 396,288 NAT tests for Cobas 6800/5800 platforms, plus 13,056 for Modules S201 -- real demand signal, not an estimate", "primary government source", "NUPCO Tender NPT0038/24 Announcement (initial quantities), 01/09/2024"),
        ("Diagnostica Stago", "NUPCO 2024 tender requested 1,731,840 fibrinogen tests and 8,109,600 heparin-sensitive APTT tests for STA R Max/STA Compact platforms -- among the highest single-line-item volumes in the entire tender", "primary government source", "NUPCO Tender NPT0038/24 Announcement (initial quantities), 01/09/2024"),
        ("Lorne Laboratories (part of Calibre Scientific)", "Related IH1000/IH500-compatible reagent lines (same product category Lorne competes in) show extremely high demand -- e.g. 6,497,280 LISS Coombs cards and 3,631,488 ABO/D reverse-group cards requested in the 2024 tender", "primary government source, category-level demand context", "NUPCO Tender NPT0038/24 Announcement (initial quantities), 01/09/2024"),
        ("Teleflex", "No directly matching line item found in the 2024 Announcement -- consistent with Teleflex's transfusion-line KSA status remaining unconfirmed rather than a large, visible demand signal", "absence check against primary source", "NUPCO Tender NPT0038/24 Announcement (initial quantities), 01/09/2024"),
        ("Hologic", "NUPCO 2024 tender requested 10,000 malaria NAT tests and 1,170,000 HBV/HCV/HIV NAT tests compatible with the Panther platform -- confirms real, large-scale demand for the instrument Hologic owns (reagents supplied by Grifols)", "primary government source", "NUPCO Tender NPT0038/24 Announcement (initial quantities), 01/09/2024"),
    ]
    for company_name, claim, ev_type, source_detail in market_size_evidence:
        if company_name in name_to_id:
            cur.execute(
                "INSERT INTO evidence (manufacturer_id, claim, evidence_type, source_detail) VALUES (?,?,?,?)",
                (name_to_id[company_name], claim, ev_type, source_detail)
            )

    # Real product/platform names extracted directly from NUPCO Tender NPT0038/24
    # Final Awardation + Announcement documents (both uploaded by user) -- these are
    # instrument platform and reagent-line names, not every individual SKU.
    products_seed = [
        ("Bio-Rad (IH-1000/IH-500 line)", "IH-1000", "Analyzer", "Automated blood typing/antibody screening gel-card instrument"),
        ("Bio-Rad (IH-1000/IH-500 line)", "IH-500", "Analyzer", "Automated blood typing/antibody screening gel-card instrument (smaller footprint)"),
        ("Ortho Clinical Diagnostics (Vision/MAX line)", "Ortho Vision", "Analyzer", "Automated blood grouping/antibody screening system"),
        ("Ortho Clinical Diagnostics (Vision/MAX line)", "Ortho VISION Max", "Analyzer", "Higher-throughput variant of Ortho Vision"),
        ("Immucor (acquired by Werfen, 2023)", "Echo", "Analyzer", "Automated immunohematology instrument (solid-phase)"),
        ("Immucor (acquired by Werfen, 2023)", "NEO Iris", "Analyzer", "High-throughput automated immunohematology instrument"),
        ("Immucor (acquired by Werfen, 2023)", "Galileo", "Analyzer", "Automated immunohematology instrument (earlier generation)"),
        ("HORIBA Medical", "Yumizen H2500", "Analyzer", "Hematology analyzer, high throughput (with P8000 module)"),
        ("HORIBA Medical", "Yumizen H1500", "Analyzer", "Hematology analyzer, mid throughput"),
        ("HORIBA Medical", "Pentra XLR", "Analyzer", "Hematology analyzer"),
        ("HORIBA Medical", "Micros ES60", "Analyzer", "Compact hematology analyzer"),
        ("Sysmex", "XN series", "Analyzer", "High-throughput hematology analyzer line"),
        ("Sysmex", "XP-300", "Analyzer", "Compact hematology analyzer"),
        ("Beckman Coulter", "DXH900", "Analyzer", "Hematology analyzer, high throughput"),
        ("Beckman Coulter", "DXH800", "Analyzer", "Hematology analyzer"),
        ("Beckman Coulter", "DXH500", "Analyzer", "Compact hematology analyzer"),
        ("Beckman Coulter", "AU/DXC", "Analyzer", "Clinical chemistry analyzer line"),
        ("Siemens Healthineers", "Atellica", "Analyzer", "Hematology/chemistry automation platform"),
        ("Siemens Healthineers", "ADVIA 2120i / ADVIA 560", "Analyzer", "Hematology analyzer line"),
        ("Siemens Healthineers", "BCS XP", "Analyzer", "Coagulation analyzer"),
        ("Siemens Healthineers", "CA-1500 / CA-560 / CA-660", "Analyzer", "Coagulation analyzer line"),
        ("Siemens Healthineers", "PFA-100 / PFA-200", "Analyzer", "Platelet function analyzer"),
        ("Diagnostica Stago", "STA R Max", "Analyzer", "Coagulation analyzer, high throughput"),
        ("Diagnostica Stago", "STA Compact", "Analyzer", "Coagulation analyzer, compact"),
        ("Diagnostica Stago", "StheMO", "Analyzer", "Coagulation analyzer"),
        ("Roche Diagnostics (NAT/Molecular line)", "Cobas 6800 / Cobas 5800", "Analyzer", "Automated NAT/molecular testing platform"),
        ("Roche Diagnostics (NAT/Molecular line)", "Cobas T711", "Analyzer", "Coagulation analyzer"),
        ("Roche Diagnostics (NAT/Molecular line)", "Modules S201", "Analyzer", "NAT testing module"),
        ("Abbott Core Diagnostics", "Alinity HQ", "Analyzer", "Hematology analyzer with reticulocyte counting"),
        ("Abbott Core Diagnostics", "Alinity S", "Analyzer", "Infectious disease immunoassay screening platform"),
        ("Abbott Core Diagnostics", "Alinity HS", "Analyzer", "Slide smearing/staining instrument"),
        ("Abbott Core Diagnostics", "CellDyn Ruby / CellDyn Emerald", "Analyzer", "Hematology analyzer line"),
        ("Mindray", "BC-6200 / BC-6800+ / AL8000", "Analyzer", "Hematology analyzer line"),
        ("Tosoh", "G8 / G11", "Analyzer", "Hemoglobin electrophoresis/HbA1c analyzer"),
        ("Sebia", "Capillarys 3 Octa", "Analyzer", "Capillary electrophoresis system for Hb electrophoresis"),
        ("Sebia", "Capillarys Flex 2", "Analyzer", "Capillary electrophoresis system"),
        ("Sebia", "Hydrasys 2 Scan", "Analyzer", "Electrophoresis scanning system"),
        ("Grifols", "Erytra", "Analyzer", "Automated blood grouping/antibody screening system"),
        ("Grifols", "Wadiana", "Analyzer", "Automated blood grouping system (compact)"),
        ("Terumo BCT", "Trima Accel", "Apheresis device", "Automated blood collection system, donor apheresis"),
        ("Terumo BCT", "Spectra Optia", "Apheresis device", "Therapeutic and donor apheresis system"),
        ("Terumo BCT", "Reveos", "Blood processing device", "Automated whole blood processing system"),
        ("Haemonetics", "ACP215", "Blood processing device", "Automated cell processing system (glycerolization/deglycerolization)"),
        ("Haemonetics", "MCS+", "Apheresis device", "Multi-component apheresis collection system"),
        ("Miltenyi Biotec", "CliniMACS", "Cell separation device", "Automated stem cell/CD34 selection system"),
        ("Cerus Corporation", "INTERCEPT", "Blood processing device", "Pathogen reduction technology system for platelets/plasma"),
        ("Hologic", "Panther", "Analyzer", "Automated molecular/NAT testing platform (reagents supplied by Grifols)"),
        ("Hologic", "Tigris", "Analyzer", "Automated molecular/NAT testing platform (earlier generation)"),
    ]
    product_id_map = {}
    for manu_name, prod_name, prod_type, desc in products_seed:
        if manu_name not in name_to_id:
            continue
        cur.execute(
            "INSERT INTO products (manufacturer_id, product_name, product_type, description, source) VALUES (?,?,?,?,?)",
            (name_to_id[manu_name], prod_name, prod_type, desc,
             "NUPCO Tender NPT0038/24 Final Awardation + Announcement documents (17/03/2025 and 01/09/2024) -- uploaded by user")
        )
        product_id_map[(manu_name, prod_name)] = cur.lastrowid

    # Distributor -> specific product links, from the same Final Awardation document's vendor column
    distributor_product_links = [
        ("Abdulrehman Algosaibi GTC", "Bio-Rad (IH-1000/IH-500 line)", "IH-1000"),
        ("Abdulrehman Algosaibi GTC", "Bio-Rad (IH-1000/IH-500 line)", "IH-500"),
        ("Abdulrehman Algosaibi GTC", "Siemens Healthineers", "ADVIA 2120i / ADVIA 560"),
        ("Abdulrehman Algosaibi GTC", "Siemens Healthineers", "BCS XP"),
        ("Abdulrehman Algosaibi GTC", "Siemens Healthineers", "CA-1500 / CA-560 / CA-660"),
        ("Abdulrehman Algosaibi GTC", "Siemens Healthineers", "PFA-100 / PFA-200"),
        ("Abdulrehman Algosaibi GTC", "Terumo BCT", "Trima Accel"),
        ("Abdulrehman Algosaibi GTC", "Terumo BCT", "Spectra Optia"),
        ("Abdulrehman Algosaibi GTC", "Terumo BCT", "Reveos"),
        ("Samir Trading & Marketing", "Ortho Clinical Diagnostics (Vision/MAX line)", "Ortho Vision"),
        ("Samir Trading & Marketing", "Ortho Clinical Diagnostics (Vision/MAX line)", "Ortho VISION Max"),
        ("Samir Trading & Marketing", "HORIBA Medical", "Yumizen H2500"),
        ("Samir Trading & Marketing", "HORIBA Medical", "Yumizen H1500"),
        ("Samir Trading & Marketing", "HORIBA Medical", "Pentra XLR"),
        ("Samir Trading & Marketing", "HORIBA Medical", "Micros ES60"),
        ("Medical Supplies & Services Co Ltd", "Immucor (acquired by Werfen, 2023)", "Echo"),
        ("Medical Supplies & Services Co Ltd", "Immucor (acquired by Werfen, 2023)", "NEO Iris"),
        ("Medical Supplies & Services Co Ltd", "Immucor (acquired by Werfen, 2023)", "Galileo"),
        ("Medical Supplies & Services Co Ltd", "Abbott Core Diagnostics", "Alinity HQ"),
        ("Medical Supplies & Services Co Ltd", "Abbott Core Diagnostics", "Alinity S"),
        ("Medical Supplies & Services Co Ltd", "Abbott Core Diagnostics", "Alinity HS"),
        ("Medical Supplies & Services Co Ltd", "Abbott Core Diagnostics", "CellDyn Ruby / CellDyn Emerald"),
        ("Abdulla Fouad for medical supplies", "Mindray", "BC-6200 / BC-6800+ / AL8000"),
        ("Abdulla Fouad for medical supplies", "Tosoh", "G8 / G11"),
        ("Abdulla Fouad for medical supplies", "Sebia", "Capillarys 3 Octa"),
        ("Abdulla Fouad for medical supplies", "Sebia", "Capillarys Flex 2"),
        ("Abdulla Fouad for medical supplies", "Sebia", "Hydrasys 2 Scan"),
        ("Abdulla Fouad for medical supplies", "Grifols", "Erytra"),
        ("Abdulla Fouad for medical supplies", "Grifols", "Wadiana"),
        ("Abdulla Fouad for medical supplies", "Hologic", "Panther"),
        ("Diagnostic Saudi Arabia Trading Com", "Diagnostica Stago", "STA R Max"),
        ("Diagnostic Saudi Arabia Trading Com", "Diagnostica Stago", "STA Compact"),
        ("Diagnostic Saudi Arabia Trading Com", "Diagnostica Stago", "StheMO"),
        ("Dar Al-Zahrawi Medical Company", "Beckman Coulter", "DXH900"),
        ("Dar Al-Zahrawi Medical Company", "Beckman Coulter", "DXH800"),
        ("Dar Al-Zahrawi Medical Company", "Beckman Coulter", "DXH500"),
        ("Sysmex LLC Company", "Sysmex", "XN series"),
        ("Sysmex LLC Company", "Sysmex", "XP-300"),
        ("Roche Diagnostics Saudi Arabia L.L.C", "Roche Diagnostics (NAT/Molecular line)", "Cobas 6800 / Cobas 5800"),
        ("Roche Diagnostics Saudi Arabia L.L.C", "Roche Diagnostics (NAT/Molecular line)", "Cobas T711"),
        ("Roche Diagnostics Saudi Arabia L.L.C", "Roche Diagnostics (NAT/Molecular line)", "Modules S201"),
        ("Arabian Trade House", "Haemonetics", "ACP215"),
        ("Arabian Trade House", "Haemonetics", "MCS+"),
        ("HOME OF GULF ELITE EST.", "Miltenyi Biotec", "CliniMACS"),
        ("Arabian medical house company", "Cerus Corporation", "INTERCEPT"),
        ("AFMS", "Hologic", "Panther"),
        ("Beckman Coulter Saudi Arabia CO.LT", "Beckman Coulter", "AU/DXC"),
    ]
    for dist_name, manu_name, prod_name in distributor_product_links:
        key = (manu_name, prod_name)
        if key in product_id_map:
            cur.execute(
                "INSERT INTO distributor_products (distributor_name, product_id, source) VALUES (?,?,?)",
                (dist_name, product_id_map[key], "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- uploaded by user")
            )

    # Fill remaining product gaps -- companies that had zero products on file.
    # Mix of primary source (NUPCO document, already in hand) and web-confirmed names.
    gap_products = [
        ("Alcor Scientific", "miniiSED i-SED", "Analyzer", "ESR (erythrocyte sedimentation rate) analyzer",
         "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- primary source"),
        ("Chrono-log", "Model 700 Whole Blood/Optical Lumi-Aggregometer", "Analyzer", "Platelet aggregation analyzer, whole blood/optical, with luminescence ATP release measurement",
         "Confirmed via chronolog.com and avant-medical.com product pages -- web search"),
        ("Tcoag Ireland Limited (a Stago Group company)", "Thrombo Aggregometer", "Analyzer", "Platelet aggregation analyzer (Tcoag/Stago line)",
         "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- primary source, exact model beyond 'Thrombo Aggregometer' name not further specified in source"),
        ("Werfen (ACL/hemostasis line)", "ACL TOP Family", "Analyzer", "Coagulation analyzer family (TOP 50/70 series, Elite series) running HemosIL reagents",
         "Confirmed via werfen.com official product pages -- web search"),
        ("bioMerieux (Vidas line)", "VIDAS", "Analyzer", "Automated immunoassay platform (used here for D-dimer testing)",
         "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- primary source"),
        ("Diagast", "Blood grouping & extended phenotyping reagent panel", "Reagent line", "Anti-A/B/D and extended red cell antigen phenotyping vials (Anti-Fya/Fyb/Jka/Jkb/M/N/S/Kpa/Kpb etc.)",
         "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- primary source"),
        ("Lorne Laboratories (part of Calibre Scientific)", "Blood grouping & Coombs reagent panel", "Reagent line", "ABO/Rh/Kell/rare antigen typing reagents and Coombs cells",
         "lornelabs.com product catalog -- previously verified"),
        ("Macopharma", "Blood bag & apheresis collection systems", "Consumable", "Blood collection bags, apheresis kits, additive solutions",
         "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- primary source"),
        ("Fresenius Kabi (blood bag line)", "Blood collection bag systems", "Consumable", "Quadruple/triple/double blood collection bags with leukocyte reduction filters, bone marrow collection kits",
         "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- primary source"),
        ("JMS (blood bag line)", "Blood collection/transfer bags", "Consumable", "Blood collection and transfer bag systems",
         "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- primary source"),
        ("Demophorius", "Blood collection bags", "Consumable", "Blood collection bags with leukocyte reduction filters",
         "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- primary source"),
        ("Streck", "Sickle cell screening & hematology controls", "Reagent/control line", "Sickle cell solubility screening controls and related hematology QC materials",
         "NUPCO Tender NPT0038/24 Final Awardation (17/03/2025) -- primary source"),
    ]
    for manu_name, prod_name, prod_type, desc, src in gap_products:
        if manu_name in name_to_id:
            cur.execute(
                "INSERT INTO products (manufacturer_id, product_name, product_type, description, source) VALUES (?,?,?,?,?)",
                (name_to_id[manu_name], prod_name, prod_type, desc, src)
            )
            product_id_map[(manu_name, prod_name)] = cur.lastrowid

    # Honest note: Teleflex has NO confirmed blood-bank-relevant product added here.
    # Its KSA status remains "unclear" specifically because the transfusion-line product
    # was never confirmed -- adding a product here would misrepresent that gap as resolved.

    # Fill in distributor-product links that were missing for distributors identified
    # via general web research (not just the NUPCO tender vendor list)
    extra_dp_links = [
        ("GAMSCO Medical", "Lorne Laboratories (part of Calibre Scientific)", "Blood grouping & Coombs reagent panel"),
        ("AFMS", "Grifols", "Erytra"),
        ("AFMS", "Grifols", "Wadiana"),
        ("Ali Al-Suwaidi Trading Est.", "Lorne Laboratories (part of Calibre Scientific)", "Blood grouping & Coombs reagent panel"),
    ]
    for dist_name, manu_name, prod_name in extra_dp_links:
        key = (manu_name, prod_name)
        if key in product_id_map:
            cur.execute(
                "INSERT INTO distributor_products (distributor_name, product_id, source) VALUES (?,?,?)",
                (dist_name, product_id_map[key], "Cross-referenced from earlier web research + product catalog data")
            )

    # Final gap-fill round: Werfen's own (pre-Immucor) transfusion/transplant product,
    # confirmed via web search
    cur.execute(
        "INSERT INTO products (manufacturer_id, product_name, product_type, description, source) VALUES (?,?,?,?,?)",
        (name_to_id["Werfen (Transfusion & Transplant division)"], "NanoTYPE HLA-11 Plus", "Reagent kit",
         "Next-generation HLA typing assay (CE-IVD, IVDR), full-gene coverage across all 11 classical HLA genes, for Nanopore sequencing platforms",
         "Confirmed via transfusionandtransplant.werfen.com official product announcement -- web search")
    )
    cur.execute(
        "INSERT INTO evidence (manufacturer_id, claim, evidence_type, source_detail) VALUES (?,?,?,?)",
        (name_to_id["Teleflex"],
         "Researched Teleflex's actual product portfolio (Arrow vascular access catheters, MANTA vascular closure device) -- it is a vascular access/interventional company, not a blood bank reagent or transfusion diagnostics company. No genuine blood-bank-relevant product was found beyond the previously-confirmed LMA/airway line, which is unrelated to transfusion medicine.",
         "web search, portfolio review",
         "teleflex.com product area pages (Vascular Access, MANTA); this raises a real question about whether Teleflex belongs in the Blood Bank category at all")
    )

    # Real, dated corporate events already discovered during research (not fabricated)
    market_events_seed = [
        ("Immucor (acquired by Werfen, 2023)", "Acquisition", "2023",
         "Immucor was acquired by Werfen. Confirmed via SEC Form 8-K (Neogen Corp, filed Aug 2025), which states the former Immucor CEO 'led the company's turnaround and its acquisition by Werfen in 2023.'",
         "SEC Form 8-K, Neogen Corp, August 2025"),
        ("Lorne Laboratories (part of Calibre Scientific)", "Acquisition", "Not precisely dated -- year not confirmed",
         "Lorne Laboratories was acquired by Calibre Scientific (a US diagnostics group). The acquisition is confirmed but the exact year was not independently verified.",
         "calibrescientificgroup.com acquisition notice"),
        ("Diagnostica Stago", "Market entry", "2020",
         "Stago established a direct KSA affiliate office in Riyadh, moving from third-party distribution to direct presence.",
         "stago.com affiliate directory, Riyadh address listing"),
        ("Grifols", "Market entry", "2019",
         "Grifols established its own representation office in Riyadh.",
         "grifols.com/en/saudi-arabia"),
        ("Grifols", "Acquisition", "2017 (completed)",
         "Grifols completed acquisition of Hologic's share of the NAT donor screening business for $1.85B, taking over R&D/manufacturing of the Procleix NAT reagent line while Hologic retained ownership of the Panther/Tigris instrument platforms.",
         "grifols.com official press release, January 2017"),
    ]
    for manu_name, event_type, event_date, description, source in market_events_seed:
        if manu_name in name_to_id:
            cur.execute(
                "INSERT INTO market_events (manufacturer_id, event_type, event_date, description, source) VALUES (?,?,?,?,?)",
                (name_to_id[manu_name], event_type, event_date, description, source)
            )

    opportunities = [
        ("Immucor (acquired by Werfen, 2023)", "CORRECTED after finding SEC filing: Immucor was acquired by Werfen in 2023 and is no longer independent. This is the SAME opportunity as the Werfen entry below, not a separate one -- scores lowered accordingly",
         "Do not contact Immucor separately. Any inquiry should go to Werfen's Dubai regional office and explicitly ask about the Immucor/Capture-Echo-NEO product line for KSA.", 2, 3, 3),
        ("Werfen (Transfusion & Transplant division)", "Has Dubai regional office but no named KSA distributor",
         "Contact Dubai regional office directly, ask about KSA distribution status", 2, 2, 3),
        ("Teleflex", "Confirmed distributor only for their airway (LMA) line, not transfusion line",
         "Ask EMEA office (Athlone, Ireland) which entity covers KSA for the transfusion-relevant line", 1, 2, 2),
    ]
    for company_name, reason, action, s1, s2, s3 in opportunities:
        cur.execute(
            """INSERT INTO opportunities (manufacturer_id, reason, action, score_no_distributor, score_confidence, score_brand)
               VALUES (?,?,?,?,?,?)""",
            (name_to_id[company_name], reason, action, s1, s2, s3)
        )



    tender_rows = [
        ("NPT0038/24", "Lab Tender (Blood Bank / Hematology / Coagulation / Stem Cell)", "Blood Bank / Hematology / Coagulation / Stem Cell", "NUPCO Final Awardation document, dated 17/03/2025 (previously referenced at summary level only) -- full item-level Preliminary Result document (dated 29/01/2025) now also uploaded by user and cross-checked; both stages of the same tender"),
        ("NPT 0013-19", "Lab Equipment Blood Bank Tender", "Blood Bank Equipment", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT 0035/21", "Lab Tender Batch 3", "General Lab", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT 0028/22", "Medical Equipment Tender Supplemental 1", "General Medical Equipment", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT 0013/20", "General Equipment Tender for Government Sectors Phase 1", "General Equipment", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT 0050/20", "Supply of Medical Equipment Phase 4", "General Medical Equipment", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT0026/21", "Lab Tender Batch #5", "General Lab", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT 0007/21", "Medical Equipment Tender Annex 1", "General Medical Equipment", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT0019/20", "IVF Tender", "IVF / Life Science", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT0019/21", "IVF Supplementary Tender", "IVF / Life Science", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT0011/21", "Lab Tender Batch #4", "General Lab", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT0033-22", "IVF Clinics Lab Supplies", "IVF / Life Science", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT0009/18", "Seven Hospitals Equipment Tender Final Awardation", "General Medical Equipment", "NUPCO award archive (Attieh Medico award history) -- uploaded by user"),
        ("NPT0032-25", "Lab Tender: Blood Bank GPPRR", "Blood Bank", "NUPCO Preliminary Awardation, dated 22/12/2025 -- uploaded by user"),
        ("NPT0028/24", "Microbiology GPPRR", "Microbiology", "NUPCO Preliminary Result, dated 11/03/2025 -- uploaded by user. Category outside MedIntel's current 5-category scope (Blood Bank/Coag/Molecular/Hematology/Stem Cell) -- logged as reference only, not yet mined for manufacturer records"),
        ("NPT0042/24", "Toxicology GPPRR Tender", "Toxicology", "NUPCO Preliminary Awards, dated 22/05/2025 -- uploaded by user. Category outside MedIntel's current 5-category scope -- logged as reference only, not yet mined for manufacturer records"),
        ("NPT0003/25", "Lab Supplies Supplement Tender", "General Lab (Immunohistochemistry / Toxicology / Molecular / Flow Cytometry / Blood Bank / Microbiology)", "NUPCO Preliminary Awardation, dated 13/07/2025 -- uploaded by user. Very broad multi-category tender (900+ line items) -- logged as reference only, not yet mined for manufacturer records"),
    ]
    cur.executemany(
        "INSERT INTO tenders (tender_ref, tender_name, category, source) VALUES (?,?,?,?)",
        tender_rows
    )


    hospital_rows = [
        ("KAMC", "King Abdulaziz Medical City",
         "3 donor apheresis systems, 3 therapeutic apheresis systems, 2 fully automated blood processing devices, 2 POC hemoglobin analyzers",
         "NUPCO Tender NPT0058/25 (Blood Bank Reagent Deal), Final Awardation, 30/07/2025 -- uploaded by user"),
        ("KSU", "King Saud University Medical City",
         "4 donor apheresis systems, 3 therapeutic apheresis systems, 3 fully automated blood processing devices, 8 whole blood collection mixers",
         "NUPCO Tender NPT0058/25 (Blood Bank Reagent Deal), Final Awardation, 30/07/2025 -- uploaded by user"),
        ("MODA", "Ministry of Defense (Health Affairs)",
         "12 donor apheresis systems, 7 therapeutic apheresis systems, 11 fully automated blood processing devices, 42 whole blood collection mixers, 23 POC hemoglobin analyzers -- among the largest installed bases in this dataset",
         "NUPCO Tender NPT0058/25 (Blood Bank Reagent Deal), Final Awardation, 30/07/2025 -- uploaded by user"),
        ("NGHA", "National Guard Health Affairs",
         "28 donor apheresis systems, 20 therapeutic apheresis systems, 14 fully automated blood processing devices, 86 whole blood collection mixers, 25 POC hemoglobin analyzers -- the largest installed base in this dataset",
         "NUPCO Tender NPT0058/25 (Blood Bank Reagent Deal), Final Awardation, 30/07/2025 -- uploaded by user"),
        ("SFHR", "Security Forces Hospital (Riyadh) -- abbreviation as it appears in the NUPCO document; full name not independently re-verified",
         "1 donor apheresis system, 2 fully automated blood processing devices, 3 whole blood collection mixers, 2 POC hemoglobin analyzers",
         "NUPCO Tender NPT0058/25 (Blood Bank Reagent Deal), Final Awardation, 30/07/2025 -- uploaded by user"),
    ]
    cur.executemany(
        "INSERT INTO hospitals (abbreviation, full_name, notable_equipment, source) VALUES (?,?,?,?)",
        hospital_rows
    )

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','init','Initial seed from verified July 2026 research')")

    # --- v1.3 addition: 4 new Blood Bank manufacturers confirmed via NPT0032-25 ---
    new_manufacturers = [
        ("NanoEnTek", "South Korea", "nanoentek.com",
         "Fluorescence-based automated cell counters -- residual WBC counting (ADAM-rWBC2) and CD34+ stem cell counting (ADAM 2) for blood bank quality control",
         "Covered -- Arabian Trade House confirmed as NUPCO-awarded vendor for NanoEnTek in NPT0032-25 (Blood Bank GPPRR)",
         "covered", "Low -- already has confirmed KSA distribution via Arabian Trade House", "gold",
         "NUPCO Tender NPT0032-25 (Blood Bank GPPRR), Preliminary Awardation, 22/12/2025 -- uploaded by user", "Blood Bank"),
        ("Alba Bioscience Ltd", "United Kingdom", "albabioscience.co.uk",
         "Blood grouping and red cell antigen typing reagents (P1, Lea, Leb, Lua, Lub, M, N, S, s, Fya, Fyb, weak D, anti-K)",
         "Covered -- Samir Trading & Marketing confirmed as NUPCO-awarded vendor across multiple hospital groups in NPT0032-25 (Blood Bank GPPRR)",
         "covered", "Low -- already has confirmed KSA distribution via Samir Trading & Marketing", "gold",
         "NUPCO Tender NPT0032-25 (Blood Bank GPPRR), Preliminary Awardation, 22/12/2025 -- uploaded by user", "Blood Bank"),
        ("ANTITOXIN GmbH", "Germany", "Not independently verified",
         "Blood grouping antisera and red cell antigen typing reagents (Lua, Lub, Kpa, Kpb, N, anti-A1, anti-H, Cw)",
         "Covered -- Samir Trading & Marketing confirmed as NUPCO-awarded vendor across multiple hospital groups in NPT0032-25 (Blood Bank GPPRR)",
         "covered", "Low -- already has confirmed KSA distribution via Samir Trading & Marketing", "silver",
         "NUPCO Tender NPT0032-25 (Blood Bank GPPRR), Preliminary Awardation, 22/12/2025 -- uploaded by user -- website not independently verified so tier held at silver, not gold", "Blood Bank"),
        ("Diapro (Diagnostic Bioprobes)", "Italy", "diapro.it",
         "ELISA-based malaria antibody screening assay for blood donor testing",
         "Covered -- Assr Medical Technology Company confirmed as NUPCO-awarded vendor in NPT0032-25 (Blood Bank GPPRR); same principal also confirmed in NPT0038/24 for other malaria-related assays",
         "covered", "Low -- already has confirmed KSA distribution via Assr Medical Technology Company", "gold",
         "NUPCO Tender NPT0032-25 (Blood Bank GPPRR), Preliminary Awardation, 22/12/2025 -- uploaded by user", "Blood Bank"),
    ]
    cur.executemany(
        """INSERT INTO manufacturers
           (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        new_manufacturers
    )

    name_to_id = {row[1]: row[0] for row in cur.execute("SELECT id, name FROM manufacturers").fetchall()}

    new_products = [
        ("NanoEnTek", "ADAM-rWBC2", "Device + reagent kit", "Automated fluorescence-based residual WBC counter for leukoreduced blood products", "NPT0032-25"),
        ("NanoEnTek", "ADAM 2 / CD34K-025", "Device + reagent kit", "Benchtop fluorescent CD34+ stem cell counter and test kit", "NPT0032-25"),
        ("Alba Bioscience Ltd", "Blood grouping antisera panel", "Reagent", "Red cell antigen typing reagents: P1, Lea, Leb, Lua, Lub, M, N, S, s, Fya, Fyb, weak D, anti-K", "NPT0032-25"),
        ("ANTITOXIN GmbH", "Blood grouping antisera panel", "Reagent", "Red cell antigen typing reagents: Lua, Lub, Kpa, Kpb, N, anti-A1, anti-H, Cw", "NPT0032-25"),
        ("Diapro (Diagnostic Bioprobes)", "MALAB.CE.96", "ELISA kit", "Malaria antibody ELISA for blood donor screening", "NPT0032-25"),
    ]
    cur.executemany(
        "INSERT INTO products (manufacturer_id, product_name, product_type, description, source) VALUES (?,?,?,?,?)",
        [(name_to_id[n], pn, pt, d, s) for n, pn, pt, d, s in new_products]
    )

    new_evidence = [
        ("NanoEnTek", "NUPCO-awarded vendor for ADAM-rWBC2 and ADAM 2 devices across KAMC, KSU, MODA, NGHA, SFHR sectors", "tender_award", "NPT0032-25, SN 40-41, 85-86, 202-203, 204-205, source: uploaded PDF"),
        ("Alba Bioscience Ltd", "NUPCO-awarded vendor for multiple red cell antigen reagents (P1, Lea, Leb, etc.) across KAMC, KSU, MODA, SFHR sectors", "tender_award", "NPT0032-25, SN 16-32 and equivalents across sectors, source: uploaded PDF"),
        ("ANTITOXIN GmbH", "NUPCO-awarded vendor for multiple red cell antigen reagents across KAMC, KSU, MODA, SFHR sectors", "tender_award", "NPT0032-25, SN 19, 23-24, 33-34 and equivalents across sectors, source: uploaded PDF"),
        ("Diapro (Diagnostic Bioprobes)", "NUPCO-awarded vendor for malaria antibody ELISA kit (via Assr Medical Technology Company) across KSU and MODA sectors", "tender_award", "NPT0032-25, SN 80, 190, source: uploaded PDF"),
    ]
    cur.executemany(
        "INSERT INTO evidence (manufacturer_id, claim, evidence_type, source_detail) VALUES (?,?,?,?)",
        [(name_to_id[n], c, et, sd) for n, c, et, sd in new_evidence]
    )

    # Enrich Samir Trading & Marketing with 2 new confirmed principals, and add
    # 2 previously-uncaptured distributors (already implied by manufacturer records above)
    cur.execute(
        """UPDATE distributors SET represents = ?, market_strength_basis = ?
           WHERE name LIKE 'Samir Trading%'""",
        ("Macopharma, Ortho Clinical Diagnostics (Vision/MAX line), HORIBA Medical (Yumizen/Pentra/Micros), Alba Bioscience Ltd, ANTITOXIN GmbH",
         "FIVE confirmed principals now via NUPCO tender award records (NPT0038/24 + NPT0032-25) -- the broadest portfolio in this dataset. Still not independently confirmed for overall company size or revenue.")
    )
    cur.executemany(
        "INSERT INTO distributors (name, country, represents, source, market_strength_tier, market_strength_basis) VALUES (?,?,?,?,?,?)",
        [
            ("Arabian Trade House", "Saudi Arabia", "Diagast, Haemonetics, NanoEnTek",
             "NUPCO Tender NPT0038/24 and NPT0032-25 award records -- uploaded by user",
             "Tenure-verified (partial)",
             "THREE confirmed principals via NUPCO tender award records across two separate tenders (NPT0038/24, NPT0032-25). Not independently confirmed for overall company size or revenue."),
            ("Assr Medical Technology Company", "Saudi Arabia", "Diapro (Diagnostic Bioprobes)",
             "NUPCO Tender NPT0032-25 -- uploaded by user",
             "Insufficient data",
             "Only one confirmed principal so far, from a single tender. Do not extrapolate to overall company size."),
        ]
    )

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','update','v1.3: Added 4 new Blood Bank manufacturers + enriched distributor records from NPT0032-25')")

    # --- v1.4 addition: Chinese IVD suppliers (Snibe, Dymind, URIT) per user request ---
    china_manufacturers = [
        ("Snibe (New Industries Biomedical Engineering Co.)", "China (Shenzhen)", "snibe.com",
         "MAGLUMI chemiluminescence immunoassay (CLIA) systems, Biossays biochemistry analyzers, Molecision molecular diagnostics, Hemolumi hemostasis",
         "Covered -- this is one of Attieh Medico's own current principals (per internal company knowledge, not independently confirmed via public web search). Publicly, Snibe lists Saudi Arabia among its served markets, and NUPCO/Saudi MOH leadership visited Snibe's China HQ and signed an MOU (Dec 2025) -- but no public source names the specific KSA distributor entity.",
         "covered", "N/A -- existing Attieh Medico principal, not an outreach lead", "silver",
         "Internal: part of Amr's own product portfolio at Attieh Medico. External corroboration: snibe.com lists Saudi Arabia as a served market; snibe.com/en/news confirms a Dec 2025 Saudi MOH/NUPCO delegation visit and MOU signing at Snibe HQ. No independent public source names Attieh Medico specifically as the KSA distributor -- tier held at silver pending an external citation.", "Molecular Diagnostics"),
        ("Dymind (Shenzhen Dymind Biotechnology)", "China (Shenzhen)", "dymind.com",
         "Automated hematology analyzers (DH-series, UN73, DM79X), coagulation analyzers (CA1200, DC1040/1020), POCT and veterinary hematology lines",
         "Covered -- OLAMED (Jeddah) confirmed as KSA distributor, listing multiple Dymind hematology analyzer models (DH36, DH76) with local sales contact",
         "covered", "Low -- already has confirmed KSA distribution via OLAMED", "gold",
         "olamed.sa/catog/hematology (DH36, DH76 product listings with Jeddah sales contact +966568164597); dymind.com company site", "Hematology"),
        ("URIT Medical Electronic", "China (Guilin)", "urit.com",
         "Hematology analyzers (URIT-3000 series, URIT-5000 series), coagulation analyzers (URIT-600), clinical chemistry",
         "Covered -- Rukn Umayya Company confirmed as authorized KSA distributor for URIT devices including URIT-3000Plus hematology analyzer",
         "covered", "Low -- already has confirmed KSA distribution via Rukn Umayya Company", "gold",
         "umc-medical.com/partners (Rukn Umayya Company partner page, explicitly names URIT-3000Plus)", "Hematology"),
    ]
    cur.executemany(
        """INSERT INTO manufacturers
           (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        china_manufacturers
    )
    name_to_id = {row[1]: row[0] for row in cur.execute("SELECT id, name FROM manufacturers").fetchall()}

    china_products = [
        ("Snibe (New Industries Biomedical Engineering Co.)", "MAGLUMI X8 / X6 / X3 / X10", "CLIA immunoassay analyzer", "Chemiluminescence immunoassay analyzers, up to 260-parameter test menu", "snibe.com"),
        ("Snibe (New Industries Biomedical Engineering Co.)", "Biossays 240 Plus / C8 / C10", "Biochemistry analyzer", "Automated clinical chemistry analyzers", "snibe.com"),
        ("Snibe (New Industries Biomedical Engineering Co.)", "Molecision S6 / R8 / MP-96", "Molecular diagnostics platform", "Nucleic acid extraction and PCR-based molecular testing systems", "snibe.com"),
        ("Dymind (Shenzhen Dymind Biotechnology)", "DH76", "5-part hematology analyzer", "Auto-loader 5-part hematology analyzer with laser-based flow cytometry WBC differentiation", "olamed.sa/prod/dh76"),
        ("Dymind (Shenzhen Dymind Biotechnology)", "DH36", "3-part hematology analyzer", "Economic, compact 3-part hematology analyzer, cyanide-free HGB method", "olamed.sa/catog/hematology"),
        ("Dymind (Shenzhen Dymind Biotechnology)", "CA1200", "Coagulation analyzer", "Fully automated coagulation analyzer, optical + magnetic bead clotting methods", "dymind.com"),
        ("URIT Medical Electronic", "URIT-3000Plus", "3-part differential hematology analyzer", "Throughput up to 60 samples/hour", "umc-medical.com/partners"),
        ("URIT Medical Electronic", "URIT-600", "Automated coagulation analyzer", "Dual-magnetic circuit bead method, two simultaneous parameter detectors", "urit.com"),
    ]
    cur.executemany(
        "INSERT INTO products (manufacturer_id, product_name, product_type, description, source) VALUES (?,?,?,?,?)",
        [(name_to_id[n], pn, pt, d, s) for n, pn, pt, d, s in china_products]
    )

    china_evidence = [
        ("Snibe (New Industries Biomedical Engineering Co.)", "Snibe MAGLUMI is part of Amr's own product portfolio at Attieh Medico (internal professional knowledge)", "internal_knowledge", "Not independently sourced from a public document -- flagged as internal knowledge, not external verification"),
        ("Snibe (New Industries Biomedical Engineering Co.)", "Saudi Minister of Health and NUPCO CEO visited Snibe HQ in China and signed an MOU (Dec 2, 2025)", "official company page", "snibe.com/en/news/new -- Snibe news page, dated entry"),
        ("Dymind (Shenzhen Dymind Biotechnology)", "OLAMED (Jeddah) lists Dymind DH36 and DH76 hematology analyzers as products it supplies in KSA, with local phone/email contact", "distributor's own website", "olamed.sa/catog/hematology and olamed.sa/prod/dh76"),
        ("URIT Medical Electronic", "Rukn Umayya Company named as authorized URIT distributor in KSA, specifically for URIT-3000Plus", "distributor's own website", "umc-medical.com/partners/العربية-urit"),
    ]
    cur.executemany(
        "INSERT INTO evidence (manufacturer_id, claim, evidence_type, source_detail) VALUES (?,?,?,?)",
        [(name_to_id[n], c, et, sd) for n, c, et, sd in china_evidence]
    )

    cur.executemany(
        "INSERT INTO distributors (name, country, represents, source, market_strength_tier, market_strength_basis) VALUES (?,?,?,?,?,?)",
        [
            ("OLAMED", "Saudi Arabia (Jeddah)", "Dymind (hematology analyzer line)",
             "olamed.sa -- verified via web search",
             "Insufficient data",
             "Only one confirmed principal so far (Dymind hematology line). OLAMED's site lists other categories (immunoassay, coagulation, blood gas, chemistry, POCT) but specific other principal brands were not itemized in the pages reviewed."),
            ("Rukn Umayya Company", "Saudi Arabia", "URIT Medical Electronic",
             "umc-medical.com/partners -- verified via web search",
             "Insufficient data",
             "Only one confirmed principal so far (URIT). Do not extrapolate to overall company size."),
        ]
    )

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','update','v1.4: Added 3 Chinese IVD suppliers (Snibe, Dymind, URIT Medical) per user request; Snibe flagged as internal-knowledge sourced, Dymind and URIT verified via distributor websites')")

    # --- v1.5 addition: web-researched product catalogs for 5 existing Blood Bank manufacturers ---
    product_batch_2 = [
        ("Macopharma", "Leucoflex LXT / MTL1", "Leukoreduction filter", "Whole-blood leukodepletion filters, up to 500mL, room-temp or 72hr cold-chain compatible", "macopharma.com/products/whole-blood"),
        ("Macopharma", "THERAFLEX MB-Plasma / UV-Platelets", "Pathogen inactivation system", "Methylene Blue (plasma) and UVC (platelet) pathogen inactivation systems, incl. MacoTronic illuminators", "macopharma.com/solutions"),
        ("Macopharma", "Bactivam / Secuvam", "Diversion & sampling system", "Integrated blood-bag diversion/sampling pouch (Bactivam) and needle-stick prevention system (Secuvam)", "fannin.eu (Macopharma product page)"),
        ("Macopharma", "SSP+ (PAS-E)", "Platelet additive solution", "Latest-generation platelet additive solution", "macopharma.com/solutions"),
        ("Diagast", "PK7300 blood grouping reagent series", "Reagent", "Monoclonal ABO/RhD antisera for red cell blood group determination", "medicalexpo.com/prod/diagast"),
        ("Diagast", "Extended/rare phenotyping antisera", "Reagent", "Monoclonal/polyclonal antisera (IgM/IgG) for rare antigen phenotyping beyond ABO/RhD/Kell", "medicalexpo.com (Diagast phenotyping reagents)"),
        ("Diagast", "79000 series QC reagent (NEG CONTROL)", "Quality control reagent", "Negative control for blood grouping and Rhesus-Kell phenotyping", "medicalexpo.com/prod/diagast"),
        ("Cerus Corporation", "INTERCEPT Blood System for Platelets", "Pathogen reduction system", "FDA-approved + CE-marked amotosalen/UVA pathogen reduction for apheresis platelets", "cerus.com/products"),
        ("Cerus Corporation", "INTERCEPT Blood System for Plasma", "Pathogen reduction system", "FDA-approved + CE-marked pathogen reduction for plasma", "cerus.com/products"),
        ("Cerus Corporation", "INTERCEPT Blood System for Cryoprecipitation", "Pathogen reduction system", "FDA-approved production of Pathogen Reduced Cryoprecipitated Fibrinogen Complex", "cerus.com/products"),
        ("Cerus Corporation", "INT100 Illuminator", "Device", "UVA illuminator required for amotosalen-treated platelet/plasma processing", "intercept-usa.com/products/intercept-platelets"),
        ("Lorne Laboratories (part of Calibre Scientific)", "ABO/Rhesus/Kell blood grouping reagents", "Reagent", "Anti-A, Anti-B, Anti-D and other core blood grouping antisera", "lornelabs.com"),
        ("Lorne Laboratories (part of Calibre Scientific)", "Rare antisera (Anti-M, Anti-N, Anti-S)", "Reagent", "Rare blood group antisera for extended phenotyping", "lornelabs.com"),
        ("Lorne Laboratories (part of Calibre Scientific)", "A.H.G Elite / Anti-Human IgG", "Reagent", "Polyspecific and monospecific anti-human globulin reagents for DAT/IAT (Coombs) testing", "lornelabs.com/products/blood-transfusion/blood-grouping-reagents"),
        ("JMS (blood bag line)", "CPDA-1 blood bag system", "Blood collection bag", "Single/double/triple bag system, CPDA-1 anticoagulant, preserves RBCs up to 35 days", "medicalexpo.com/prod/jms-north-america-corporation"),
        ("JMS (blood bag line)", "CPD-SAGM blood bag system", "Blood collection bag", "Triple/quadruple bag system with SAGM red cell preservation solution", "jmsna.net/hospital-supplies-wholesale"),
        ("JMS (blood bag line)", "T-BEX (Top-and-Bottom Extraction) System", "Blood processing accessory", "Improves separation efficiency of RBC/plasma/platelets after centrifugation", "spanhealth.com/blood-bags (JMS T-BEX description)"),
        ("JMS (blood bag line)", "Cord Blood Collection System (CBCS)", "Stem cell collection bag", "Umbilical cord blood/stem cell collection sets, Standard and Premium configurations", "medicalexpo.com (JMS Cord Blood Collection System)"),
    ]
    name_to_id = {row[1]: row[0] for row in cur.execute("SELECT id, name FROM manufacturers").fetchall()}
    for mname, pname, ptype, desc, src in product_batch_2:
        if mname in name_to_id:
            cur.execute("INSERT INTO products (manufacturer_id, product_name, product_type, description, source) VALUES (?,?,?,?,?)",
                        (name_to_id[mname], pname, ptype, desc, src))

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('products','0','bulk_insert','v1.5: Web-researched and added real product catalogs for Macopharma, Diagast, Cerus, Lorne Laboratories, JMS (batch 1 of ongoing product-enrichment pass across all 40 manufacturers)')")

    # --- v1.6: batches 2-5 of the full product-enrichment research pass (all 40 manufacturers) ---
    product_batches_2to5 = [
        # batch 2: Chrono-log, Miltenyi Biotec, Tosoh
        ("Chrono-log", "Model 700 Whole Blood/Optical Lumi-Aggregometer", "Platelet aggregometer", "2- or 4-channel; impedance (whole blood) or optical (plasma) aggregation with simultaneous ATP-release luminescence; also runs Ristocetin Cofactor Assay for vWD", "chronolog.com/Model700.html"),
        ("Chrono-log", "Model 490 4+4 Optical Aggregometer", "Platelet aggregometer", "4 or 8 channel optical-only platelet aggregometer", "chronolog.com/spec.htm"),
        ("Chrono-log", "CHRONO-PAR Aggregation Reagents", "Reagent", "ADP, Collagen, Ristocetin, Epinephrine, Arachidonic Acid platelet aggregation reagents", "avant-medical.com/products/chrono-log-platelet-function-reagents"),
        ("Chrono-log", "CHRONO-LUME Reagent", "Reagent", "Luciferin-luciferase reagent for ATP-release (dense granule) luminescence measurement", "avant-medical.com/products/chrono-log-platelet-function-reagents"),
        ("Miltenyi Biotec", "CliniMACS Plus / Prodigy Instrument", "Cell separation instrument", "GMP-compliant magnetic-activated cell sorting (MACS) system for clinical cell therapy and stem cell processing", "grokipedia.com/page/Miltenyi_Biotec"),
        ("Miltenyi Biotec", "CliniMACS CD34 Reagent System", "Reagent + tubing set", "FDA-approved monoclonal antibody reagent + tubing set for CD34+ hematopoietic progenitor cell selection", "clinicaltrials.gov protocol documents (CliniMACS CD34 Reagent System)"),
        ("Miltenyi Biotec", "CliniMACS TCR alpha/beta Depletion Reagent Kit", "Reagent kit", "Depletes TCR alpha/beta CD3+ T cells for stem cell transplant / lymphocyte infusion applications", "clinicaltrials.gov protocol documents"),
        ("Miltenyi Biotec", "StemMACS MSC Expansion Medium", "Cell culture medium", "Culture medium for mesenchymal stem cell expansion", "miltenyibiotec.com (Grokipedia summary)"),
        ("Tosoh", "HLC-723 G8 HPLC Analyzer", "HbA1c analyzer", "Ion-exchange HPLC HbA1c analyzer, ~1.6 min/sample, gold-standard method for glycated hemoglobin", "diagnostics.us.tosohbioscience.com/analyzers/g8"),
        ("Tosoh", "HLC-723 G11 HPLC Analyzer", "HbA1c analyzer", "High-throughput HbA1c HPLC analyzer, scalable 90-290 sample loader, variant analysis mode", "tosohbioscience.com/EU-EN-diagnostics/hba1c-analysers"),
        ("Tosoh", "HbA1c Control Set / Calibrator Set", "Quality control / calibrator", "Two-level HbA1c control set traceable to IFCC reference method", "diagnostics.eu.tosohbioscience.com (HbA1c Control Set IFU)"),
        # batch 3: Sysmex, Beckman Coulter, Siemens Healthineers
        ("Sysmex", "XN-Series (XN-1000/2000/9100/L-series)", "Hematology analyzer", "Flagship modular hematology platform; scalable configurations, Blood Bank Mode for donor RBC/platelet/plasma QC", "sysmex.com/en-us/lab-solutions/hematology/xn-series"),
        ("Sysmex", "XN with Blood Bank Mode", "Hematology analyzer mode", "FDA-cleared blood component QC mode: residual WBC counts, RBC/platelet concentrate profiles", "sysmex.com/en-us/training-and-knowledge/sysmex-for-clinicians/xn-series-with-blood-bank-mode"),
        ("Beckman Coulter", "DxH 900 / DxH 690T", "Hematology analyzer", "High-volume hematology analyzer with VCS technology and Monocyte Distribution Width (MDW) sepsis-risk marker", "beckmancoulter.com/products/hematology/dxh-900"),
        ("Beckman Coulter", "DxH 800", "Hematology analyzer", "High-volume hematology analyzer, advanced NRBC/WBC/reticulocyte algorithm analysis", "beckmancoulter.com/products/hematology/dxh-800"),
        ("Beckman Coulter", "DxH 560 / DxH 500 Series", "Hematology analyzer", "Compact autoloader hematology analyzers with pediatric reference ranges", "beckmancoulter.com/products/hematology/dxh-560-autoloader-hematology-analyzer"),
        ("Siemens Healthineers", "Atellica Solution (IM + CH)", "Immunoassay + clinical chemistry analyzer", "Scalable immunoassay/chemistry platform, bidirectional magnetic sample transport, up to 440 tests/hr, 300+ configurations", "siemens-healthineers.com/en-us/laboratory-diagnostics/clinical-chemistry-and-immunoassay-systems/atellica-solution-analyzers"),
        ("Siemens Healthineers", "Atellica IM 1300", "Immunoassay analyzer", "Standalone immunoassay module within the Atellica line", "fishersci.com (Atellica IM 1300 Analyzer)"),
        # batch 4: Streck, Alcor Scientific, Mindray, Werfen (ACL + Transfusion&Transplant), Tcoag, bioMerieux Vidas, Fresenius Kabi, Demophorius
        ("Streck", "Para 12 Extend / Para 12 Plus", "Hematology control", "3-part/5-part differential hematology QC controls compatible with Beckman Coulter, HORIBA, Mindray, Siemens and other major analyzer brands", "streck.com/products/quality-control/hematology"),
        ("Streck", "Cal-Chex / CVA (Calibration Verification Assessment)", "Hematology calibrator / linearity control", "Whole-blood calibrator and linearity assessment kits for multi-parameter hematology analyzers", "streck.com/wp-content (Hematology and Linearity Controls Brochure)"),
        ("Alcor Scientific", "iSED / iSED PRO / iSED Elite", "Automated ESR analyzer", "Fully automated ESR analyzers measuring RBC aggregation directly via photometric rheology; results in 20 seconds vs 30-60 min Westergren method", "alcorscientific.com/clinical-lab/ised"),
        ("Alcor Scientific", "miniiSED", "Compact ESR analyzer", "Compact benchtop ESR analyzer for urgent-care/STAT-volume labs", "labmedica.com (Alcor Scientific Medica 2024 coverage)"),
        ("Mindray", "BC-6800Plus / CAL 8000 line", "5-part differential hematology analyzer", "High-throughput hematology analyzer (up to 200 tests/hr) with SF Cube technology for WBC/NRBC/reticulocyte flagging", "mindray.com/en/products/laboratory-diagnostics/hematology/5-part-differential-analyzers/bc-6800-plus"),
        ("Mindray", "BC-5000 / BC-5000Vet", "5-part differential hematology analyzer", "Compact, budget 5-part hematology analyzer; veterinary variant available", "mindray.com/en/product/bc-5000.html"),
        ("Mindray", "BC-700 Series (BC-700/720/760/780)", "Hematology + ESR analyzer", "Combined CBC and automated ESR analyzer series for medium-volume labs", "mindray.com (Mindray hematology hemabook)"),
        ("Mindray", "MC-80 Automated Digital Cell Morphology Analyzer", "Digital morphology analyzer", "AI-assisted digital blood cell morphology imaging and classification", "mindray.com/en/products/laboratory-diagnostics/hematology"),
        ("Werfen (ACL/hemostasis line)", "ACL TOP Family 50/70 Series", "Coagulation analyzer", "Fully automated hemostasis testing systems, scalable low- to high-volume, standardized on HemosIL reagent panel", "werfen.com/na/en/hemostasis-diagnostics/coagulation-instruments-system-acl-top-family-series"),
        ("Werfen (ACL/hemostasis line)", "ACL AcuStar", "Specialty immunoassay coagulation analyzer", "Fully automated chemiluminescent specialty hemostasis immunoassay analyzer (e.g. HIT, vWD panel)", "annualreview.werfen.com/specialized-diagnostics/hemostasis"),
        ("Werfen (ACL/hemostasis line)", "HemosIL Reagent Panel", "Reagent", "Comprehensive reagent panel standardized across the entire ACL TOP Family for routine and specialty coagulation testing", "werfen.com/uk/en/haemostasis-diagnostics"),
        ("Werfen (Transfusion & Transplant division)", "Capture R", "Solid-phase red cell antibody screening assay", "Solid-phase adherence assay for antibody screening/panel reactive antibody testing in immunohematology", "ncbi.nlm.nih.gov/pmc/articles/PMC12499635 (systematic review comparing IH platforms)"),
        ("Werfen (Transfusion & Transplant division)", "ImmuLINK", "Immunohematology lab data management software", "Single-interface data management software for immunohematology laboratories", "transfusionandtransplant.werfen.com/en-us/lab/patient-labs"),
        ("Werfen (Transfusion & Transplant division)", "Omixon NGS HLA Typing (post-2024 acquisition)", "Molecular HLA typing platform", "Next-generation sequencing technology for transplant/HLA diagnostics, added via October 2024 Omixon acquisition", "werfen.com/en (About Werfen page, Omixon acquisition note)"),
        ("Tcoag Ireland Limited (a Stago Group company)", "Destiny Plus / Destiny Max", "Coagulation analyzer", "1-channel optical/mechanical automated hemostasis analyzers for mid-to-large routine/specialty labs", "tcoag.com/instruments/destiny-plus"),
        ("Tcoag Ireland Limited (a Stago Group company)", "KC1 Delta / KC4 Delta", "Semi-automated coagulation analyzer", "1- or 4-test-position semi-automated coagulation analyzers using micro-mechanical clot detection", "medicalexpo.com/prod/tcoag-108761.html"),
        ("Tcoag Ireland Limited (a Stago Group company)", "TriniCLOT / TriniLIA / TriniLIZE reagent lines", "Reagent", "aPTT, D-Dimer, Protein C, fibrinolysis (tPA/PAI-1) reagent kits for coagulation testing", "tcoag.com/fileadmin/user_upload/PDF/Reagents (Tcoag Haemostasis Catalogue 2013)"),
        ("bioMerieux (Vidas line)", "VIDAS D-Dimer Exclusion II", "Automated D-Dimer immunoassay", "Highly sensitive automated D-Dimer assay for DVT/PE exclusion, validated for the HERDOO2 clinical decision rule, 20-minute result", "biomerieux.com/corp/en/our-offer/clinical-products/vidas-d-dimer-exclusion-ii.html"),
        ("Fresenius Kabi (blood bag line)", "CompoGuard & DonationMaster Net", "Whole blood collection bag system", "Manual whole-blood collection blood bag systems for a range of donation environments", "fresenius-kabi.com/us/products/medtech/blood-collection-processing/manual-blood-collection"),
        ("Fresenius Kabi (blood bag line)", "Hematype Segment Device", "Blood bag tubing accessory", "Single-use device for safely accessing blood-filled tubing segments for sampling, alternative to scissors", "fresenius-kabi.com/us/products/medtech/blood-collection-processing/specialty-products"),
        ("Fresenius Kabi (blood bag line)", "CompoFlow In-Line Closure", "Blood bag tubing accessory", "Non-frangible in-line tubing closure reducing repetitive strain injury and hemolysis risk vs traditional breakaway closures", "ncbi.nlm.nih.gov/pmc/articles/PMC3039751 (Transfusion journal study)"),
        ("Demophorius", "Demotek Quadruple Blood Bag (BBQ)", "Blood collection bag", "4-component whole blood collection/separation bag (RBC/plasma/platelets/buffy coat), CPDA-1 or CPD/SAG-M", "demophorius.com/product/quadruple-blood-bags"),
        ("Demophorius", "Demotek Triple Blood Bag (BBT/BBTTB)", "Blood collection bag", "3-component whole blood collection/separation bag with top-and-bottom variant for improved buffy coat removal", "demophorius.com/product/triple-blood-bags"),
        ("Demophorius", "Demotek Single/Double Blood Bag (BBS/BBD)", "Blood collection bag", "Basic single and double-bag whole blood collection systems, CPDA-1 anticoagulant", "medicalexpo.com/prod/demophorius-healthcare-68185.html"),
        # batch 5: Alba Bioscience, ANTITOXIN GmbH, Diapro
        ("Alba Bioscience Ltd", "ALBAclone blood grouping antisera", "Reagent", "FDA-cleared monoclonal blood typing antisera: Anti-A, Anti-B, Anti-AB, Anti-D, Anti-E, Anti-c, plus rare antisera (Anti-k, Anti-M, Anti-N, Anti-Lea, Anti-Leb, Anti-Lub)", "fiercebiotech.com (Quotient Biodiagnostics/Alba Bioscience press release)"),
        ("Alba Bioscience Ltd", "ALBAcyte reverse grouping / screening cells", "Reagent red cells", "Reverse grouping, antibody screening, antibody identification, and IgG-sensitized red cell panels", "fiercebiotech.com (Quotient Biodiagnostics portfolio description)"),
        ("Alba Bioscience Ltd", "ALBAclone Advanced Partial RhD Typing Kit", "Reagent kit", "Identifies weak and partial RhD types with results comparable to molecular analysis, at lower cost", "fiercebiotech.com (Quotient Biodiagnostics portfolio description)"),
        ("ANTITOXIN GmbH", "Full ABO/Rh blood typing antisera range", "Reagent", "Complete routine + rare blood typing antisera: Rh system (Anti-D/C/c/E/e/Cw), Anti-P1, Anti-M/N/S/s, Anti-K/Kpa/Kpb/Jsb, Anti-Fya/Fyb, Anti-Jka/Jkb, Anti-Lua/Lub, Anti-Xga and more", "antitoxin-gmbh.de (official company site)"),
        ("ANTITOXIN GmbH", "ImuSolutions bedside confirmation test", "Bedside/point-of-care reagent", "Pre-transfusion bedside patient identity confirmation test, addressing the most frequent transfusion error; mandatory in several European countries", "antitoxin-gmbh.de/about"),
        ("Diapro (Diagnostic Bioprobes)", "Blood Screening ELISA panel", "ELISA kit", "Full blood-donor screening ELISA menu: HBsAg (4th-gen Ultra), HBc Ab, HCV Ab, HTLV I&II Ab, T. cruzi (Chagas) Ab, T. pallidum (syphilis) Ab", "pdf.medicalexpo.com/pdf/diapro-diagnostic-bioprobes/elisa (Dia.Pro ELISA catalogue)"),
        ("Diapro (Diagnostic Bioprobes)", "DIA500 Automated ELISA Analyzer", "ELISA automation platform", "Continuous-loading automated ELISA processor, up to 480 tests/hour", "pdf.medicalexpo.com/pdf/diapro-diagnostic-bioprobes/product-catalogue-2024"),
    ]
    name_to_id2 = {row[1]: row[0] for row in cur.execute("SELECT id, name FROM manufacturers").fetchall()}
    for mname, pname, ptype, desc, src in product_batches_2to5:
        # match by substring since some init_db names carry parenthetical suffixes
        match_id = name_to_id2.get(mname)
        if not match_id:
            for full_name, mid in name_to_id2.items():
                if mname.split(" (")[0] in full_name:
                    match_id = mid
                    break
        if match_id:
            cur.execute("INSERT INTO products (manufacturer_id, product_name, product_type, description, source) VALUES (?,?,?,?,?)",
                        (match_id, pname, ptype, desc, src))

    # Upgrade ANTITOXIN GmbH confidence tier now that its own official website was found
    cur.execute("""UPDATE manufacturers SET
        website = 'antitoxin-gmbh.de',
        confidence_tier = 'gold',
        sources = sources || ' | Official company website confirmed (antitoxin-gmbh.de) -- tier upgraded from silver to gold.'
        WHERE name = 'ANTITOXIN GmbH'""")

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('products','0','bulk_insert','v1.6: Completed full product research pass (batches 2-5) across all 40 manufacturers -- 141 total products on file; Teleflex remains the sole documented zero-product exception')")

    # --- v1.7: Microbiology category expansion (batch 1 of the broader all-departments push) ---
    micro_manufacturers = [
        ("BD (Becton, Dickinson and Company)", "USA", "bd.com",
         "BD BACTEC blood culture system, BD Phoenix M50 (automated ID/AST), BD Bruker MALDI Biotyper, BD Kiestra WASP-class lab automation, BD EpiCenter/Synapsys informatics",
         "Covered -- Farouk Maamon Tamer & Company confirmed as NUPCO-awarded vendor for BD MALDI-TOF and BD BACTEC blood culture system",
         "covered", "Low -- already has confirmed KSA distribution via Farouk Maamon Tamer & Company", "gold",
         "NUPCO Tender NPT0028/24 (Microbiology GPPRR), SN 1, 51-55 -- uploaded by user. Product line verified via bd.com. Note: BD's diagnostics business is in the process of being acquired by Waters Corporation (transition ongoing as of official BD product pages reviewed).", "Microbiology"),
        ("Copan (Copan Italia / Copan Diagnostics)", "Italy", "copangroup.com",
         "eSwab liquid transport/collection system, WASP/WASPLab microbiology lab automation, FLOQSwabs, PhenoMATRIX AI, Colibri automated specimen workup",
         "Covered -- Farouk Maamon Tamer & Company confirmed as NUPCO-awarded vendor for the full Copan sample-processing automation and swab menu (body fluids, sterile samples, wound, respiratory, ENT, urine, stool, surveillance, environmental culture)",
         "covered", "Low -- already has confirmed KSA distribution via Farouk Maamon Tamer & Company", "gold",
         "NUPCO Tender NPT0028/24 (Microbiology GPPRR), SN 72-82 -- uploaded by user. Product line verified via copangroup.com and copanusa.com", "Microbiology"),
        ("77Elektronika", "Hungary", "77elektronika.hu",
         "Fully automated urine chemistry/sediment analyzers and urine test strip reagent lines",
         "Covered -- Abdulla Fouad for medical supplies confirmed as NUPCO-awarded vendor for the 77Elektronika urine analyzer line",
         "covered", "Low -- already has confirmed KSA distribution via Abdulla Fouad for medical supplies", "silver",
         "NUPCO Tender NPT0028/24 (Microbiology GPPRR), SN 6-7 -- uploaded by user. Product category confirmed via tender item descriptions (fully automated urine analyzer, urine test strips); full external product catalogue not yet independently verified -- tier held at silver", "Microbiology"),
        ("QIAGEN (molecular microbiology line)", "Germany/Netherlands", "qiagen.com",
         "Multiplex molecular PCR analyzers and syndromic panels (meningitis, respiratory, gastrointestinal infection panels)",
         "Covered -- Abdulla Fouad for medical supplies confirmed as NUPCO-awarded vendor for QIAGEN multiplex PCR analyzers and syndromic infection panels",
         "covered", "Low -- already has confirmed KSA distribution via Abdulla Fouad for medical supplies", "silver",
         "NUPCO Tender NPT0028/24 (Microbiology GPPRR), SN 8-11 -- uploaded by user. Product category confirmed via tender item descriptions; full external product catalogue not yet independently verified -- tier held at silver", "Microbiology"),
        ("BioFire (a bioMerieux company)", "USA", "biofiredx.com",
         "FilmArray multiplex molecular PCR syndromic panels: meningitis, respiratory, gastrointestinal, blood culture identification, joint infection, pneumonia panels",
         "Covered -- Al-Jeel Medical & Trading Co. Ltd confirmed as NUPCO-awarded vendor for BioFire FilmArray multiplex PCR panels across meningitis, respiratory, GI, blood culture ID, joint, and pneumonia panels",
         "covered", "Low -- already has confirmed KSA distribution via Al-Jeel Medical & Trading Co. Ltd", "silver",
         "NUPCO Tender NPT0028/24 (Microbiology GPPRR), SN 8-14 -- uploaded by user. Product category confirmed via tender item descriptions; full external product catalogue not yet independently verified -- tier held at silver", "Microbiology"),
        ("Cepheid (a Danaher company)", "USA", "cepheid.com",
         "GeneXpert real-time PCR platform and single-cartridge molecular assays: MTB/RIF, carbapenemase-resistant organisms, HIV, C. difficile, MRSA, GBS, HPV, Strep-A, SARS-CoV-2/RSV/Flu combo",
         "Covered -- Beckman Coulter Saudi Arabia CO.LT confirmed as NUPCO-awarded vendor across the full Cepheid GeneXpert cartridge menu (Groups 7 and 13 of NPT0028/24)",
         "covered", "Low -- already has confirmed KSA distribution via Beckman Coulter Saudi Arabia CO.LT", "gold",
         "NUPCO Tender NPT0028/24 (Microbiology GPPRR), SN 33-50, 83-95 -- uploaded by user. Product category confirmed via tender item descriptions naming specific cartridge families", "Microbiology"),
    ]
    cur.executemany(
        """INSERT INTO manufacturers
           (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        micro_manufacturers
    )
    name_to_id3 = {row[1]: row[0] for row in cur.execute("SELECT id, name FROM manufacturers").fetchall()}

    micro_products = [
        ("BD (Becton, Dickinson and Company)", "BD BACTEC FX / FX40 Blood Culture System", "Blood culture instrument + media", "Continuously-monitored automated blood culture system with modular instrumentation and a full line of culture media (aerobic, anaerobic, myco/lytic, peds)", "bd.com/en-us/products-and-solutions/products/product-families/bd-bactec-blood-culture-system"),
        ("BD (Becton, Dickinson and Company)", "BD Phoenix M50", "Automated ID/AST system", "136-well automated identification and antimicrobial susceptibility testing instrument, includes CPO detect test", "bd.com/en-us/products-and-solutions/products/product-families/bd-phoenix-m50-instrument"),
        ("BD (Becton, Dickinson and Company)", "BD Bruker MALDI Biotyper (CA System)", "MALDI-TOF mass spectrometry identification", "FDA-cleared reference library covering 549 microbial species for rapid organism identification", "bd.com/en-us/products-and-solutions/solutions/capabilities/bd-automated-identification-and-susceptibility-testing-solutions"),
        ("Copan (Copan Italia / Copan Diagnostics)", "eSwab / FLOQSwabs", "Specimen collection and transport", "Liquid Amies Elution Swab collection/transport system enabling multipurpose testing (culture, Gram stain, NAAT, rapid antigen) from a single specimen", "copangroup.com/product-ranges/eswab"),
        ("Copan (Copan Italia / Copan Diagnostics)", "WASP / WASPLab", "Microbiology lab automation", "Walk-Away Specimen Processor for automated plating/streaking, scalable to full lab automation with digital imaging and AI-assisted colony analysis (PhenoMATRIX)", "copanusa.com/laboratory-automation/microbiology-laboratory-automation-ai"),
        ("77Elektronika", "Fully Automated Urine Analyzer + Test Strips", "Urine chemistry/sediment analyzer + reagent", "Automated urine chemistry analyzer line with companion test strip reagents, confirmed via NUPCO award", "NUPCO Tender NPT0028/24, SN 6-7"),
        ("QIAGEN (molecular microbiology line)", "Multiplex Molecular PCR Analyzer + Syndromic Panels", "Molecular PCR platform + reagent panels", "Multiplex PCR analyzer with meningitis, respiratory, and gastrointestinal syndromic infection panels, confirmed via NUPCO award", "NUPCO Tender NPT0028/24, SN 8-11"),
        ("BioFire (a bioMerieux company)", "FilmArray Multiplex PCR Panels", "Molecular PCR platform + reagent panels", "Syndromic multiplex PCR panels: meningitis, respiratory, gastrointestinal, blood culture identification, joint infection, pneumonia", "NUPCO Tender NPT0028/24, SN 8-14"),
        ("Cepheid (a Danaher company)", "GeneXpert Platform + Cartridge Menu", "Real-time PCR platform + single-use cartridges", "Random-access single-cartridge PCR system with a broad assay menu: MTB/RIF, CRE/carbapenemase, HIV, C. diff, MRSA, GBS, HPV, Strep-A, SARS-CoV-2/RSV/Flu combo", "NUPCO Tender NPT0028/24, SN 33-50, 83-95"),
    ]
    for mname, pname, ptype, desc, src in micro_products:
        if mname in name_to_id3:
            cur.execute("INSERT INTO products (manufacturer_id, product_name, product_type, description, source) VALUES (?,?,?,?,?)",
                        (name_to_id3[mname], pname, ptype, desc, src))

    biomerieux_id = cur.execute("SELECT id FROM manufacturers WHERE name LIKE 'bioMerieux%'").fetchone()[0]
    biomerieux_products = [
        (biomerieux_id, "VITEK 2 Compact", "Automated ID/AST system", "Fully automated bacterial identification and antibiotic susceptibility testing using colorimetric VITEK 2 ID/AST cards, 15/30/60-card configurations", "biomerieux.com/corp/en/our-offer/clinical-products/vitek-2-compact.html"),
        (biomerieux_id, "VITEK MS / MS PRIME", "MALDI-TOF mass spectrometry identification", "Automated MALDI-TOF microbial identification system, benchtop configuration up to 768 samples", "biomerieux.com/corp/en/our-offer/clinical-products/vitek-ms-prime.html"),
        (biomerieux_id, "BACT/ALERT VIRTUO", "Blood culture system", "Fully automated blood culture detection system with robotic loading/unloading and smart scanning", "gms-world.com/microbiology_biomerieux"),
    ]
    cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source) VALUES (?,?,?,?,?)", biomerieux_products)

    micro_evidence = [
        ("BD (Becton, Dickinson and Company)", "NUPCO-awarded vendor Farouk Maamon Tamer & Company for MALDI-TOF and BACTEC blood culture system", "tender_award", "NPT0028/24, SN 1, 51-55, source: uploaded PDF"),
        ("Copan (Copan Italia / Copan Diagnostics)", "NUPCO-awarded vendor Farouk Maamon Tamer & Company for full sample-processing swab/automation menu", "tender_award", "NPT0028/24, SN 72-82, source: uploaded PDF"),
        ("Cepheid (a Danaher company)", "NUPCO-awarded vendor Beckman Coulter Saudi Arabia CO.LT across two full GeneXpert cartridge groups (7 and 13)", "tender_award", "NPT0028/24, SN 33-50, 83-95, source: uploaded PDF"),
    ]
    cur.executemany("INSERT INTO evidence (manufacturer_id, claim, evidence_type, source_detail) VALUES (?,?,?,?)",
                     [(name_to_id3[n], c, et, sd) for n, c, et, sd in micro_evidence])

    cur.executemany(
        "INSERT INTO distributors (name, country, represents, source, market_strength_tier, market_strength_basis) VALUES (?,?,?,?,?,?)",
        [
            ("Farouk Maamon Tamer & Company", "Saudi Arabia", "BD (Becton, Dickinson and Company), Copan (Copan Italia / Copan Diagnostics)",
             "NUPCO Tender NPT0028/24 -- uploaded by user",
             "Tenure-verified (partial)",
             "Two confirmed principals via NUPCO tender award records (BD, Copan). Not independently confirmed for overall company size or revenue."),
            ("Abdulla Fouad for medical supplies", "Saudi Arabia", "77Elektronika, QIAGEN (molecular microbiology line)",
             "NUPCO Tender NPT0028/24 -- uploaded by user",
             "Tenure-verified (partial)",
             "Two confirmed principals via NUPCO tender award records (77Elektronika, QIAGEN). Not independently confirmed for overall company size or revenue."),
            ("Al-Jeel Medical & Trading Co. Ltd", "Saudi Arabia", "bioMerieux (Vidas line), BioFire (a bioMerieux company)",
             "NUPCO Tender NPT0028/24 and NPT0038/24 -- uploaded by user",
             "Tenure-verified (partial)",
             "Confirmed principal for both bioMerieux and its BioFire subsidiary. Not independently confirmed for overall company size or revenue."),
        ]
    )

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','v1.7: Started Microbiology category expansion (BD, Copan, 77Elektronika, QIAGEN, BioFire, Cepheid) + extended bioMerieux with microbiology products, using previously-uploaded NPT0028/24 tender data cross-verified with live web research')")

    # --- v1.8: Regulatory module (new table) -- seeded ONLY with facts already
    # verified during earlier product research. No new regulatory claim is
    # invented here; entries are pulled verbatim from product.description
    # fields that already cited FDA/CE status with a source.
    name_to_id4 = {row[1]: row[0] for row in cur.execute("SELECT id, name FROM manufacturers").fetchall()}
    prod_lookup = {(row[1], row[2]): row[0] for row in cur.execute("SELECT id, manufacturer_id, product_name FROM products").fetchall()}

    def pid(mname, pname):
        mid = name_to_id4.get(mname)
        return prod_lookup.get((mid, pname)) if mid else None

    regulatory_rows = [
        ("Werfen (Transfusion & Transplant division)", "NanoTYPE HLA-11 Plus", "CE-IVD (IVDR)", "Certified",
         "Certified under the EU In Vitro Diagnostic Regulation (IVDR) as CE-IVD", "transfusionandtransplant.werfen.com (Werfen product announcement)"),
        ("Cerus Corporation", "INTERCEPT Blood System for Platelets", "FDA + CE", "Approved / Marked",
         "FDA-approved and CE-marked amotosalen/UVA pathogen reduction system", "cerus.com/products"),
        ("Cerus Corporation", "INTERCEPT Blood System for Plasma", "FDA + CE", "Approved / Marked",
         "FDA-approved and CE-marked pathogen reduction system", "cerus.com/products"),
        ("Cerus Corporation", "INTERCEPT Blood System for Cryoprecipitation", "FDA", "Approved",
         "FDA-approved production pathway for Pathogen Reduced Cryoprecipitated Fibrinogen Complex", "cerus.com/products"),
        ("Miltenyi Biotec", "CliniMACS CD34 Reagent System", "FDA", "Approved",
         "FDA-approved monoclonal antibody reagent + tubing set for CD34+ selection", "clinicaltrials.gov protocol documents"),
        ("Sysmex", "XN with Blood Bank Mode", "FDA", "Cleared",
         "FDA-cleared blood component QC mode (residual WBC counts, RBC/platelet concentrate profiles)", "sysmex.com/en-us/training-and-knowledge/sysmex-for-clinicians/xn-series-with-blood-bank-mode"),
        ("Alba Bioscience Ltd", "ALBAclone blood grouping antisera", "FDA", "Cleared",
         "FDA-cleared monoclonal blood typing antisera range", "fiercebiotech.com (Quotient Biodiagnostics/Alba Bioscience press release)"),
        ("BD (Becton, Dickinson and Company)", "BD Bruker MALDI Biotyper (CA System)", "FDA", "Cleared",
         "FDA-cleared reference library covering 549 microbial species", "bd.com/en-us/products-and-solutions/solutions/capabilities/bd-automated-identification-and-susceptibility-testing-solutions"),
    ]
    for mname, pname, body, status, detail, src in regulatory_rows:
        cur.execute(
            "INSERT INTO regulatory_status (manufacturer_id, product_id, regulatory_body, status, detail, source) VALUES (?,?,?,?,?,?)",
            (name_to_id4.get(mname), pid(mname, pname), body, status, detail, src)
        )

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','v1.8: Added regulatory_status table, seeded only with FDA/CE facts already verified during prior product research (8 rows) -- not a comprehensive regulatory audit')")
    conn.commit()

    # --- v1.9: origin classification, extended product fields, and a proper
    # many-to-many company_distributors join table (replacing fragile LIKE-matching) ---
    def classify_origin(hq):
        hq = (hq or "").lower()
        if "china" in hq and "cyprus" not in hq:
            return "Chinese"
        if "usa" in hq and "werfen" not in hq:
            return "American"
        if any(k in hq for k in ["germany","france","italy","spain","switzerland","ireland","united kingdom","netherlands","hungary","cyprus","werfen"]):
            return "European"
        if any(k in hq for k in ["japan","korea","singapore"]):
            return "Asian (other)"
        return "Unclassified"

    for mid, hq in cur.execute("SELECT id, headquarters FROM manufacturers").fetchall():
        cur.execute("UPDATE manufacturers SET origin = ? WHERE id = ?", (classify_origin(hq), mid))

    cur.execute("UPDATE products SET department = (SELECT category FROM manufacturers WHERE manufacturers.id = products.manufacturer_id)")

    for (pid,) in cur.execute("SELECT id FROM products").fetchall():
        regs = cur.execute("SELECT regulatory_body, status FROM regulatory_status WHERE product_id = ?", (pid,)).fetchall()
        if regs:
            cur.execute("UPDATE products SET certifications = ? WHERE id = ?",
                        ("; ".join(f"{b}: {s}" for b, s in regs), pid))

    import re as _re
    for pid, desc in cur.execute("SELECT id, description FROM products").fetchall():
        if not desc: continue
        m = _re.search(r'(?:up to |throughput of )?(\d{2,4})\s*(tests|samples)[\s\-]*(?:per|/)\s*(?:hr|hour)', desc, _re.I)
        if m:
            cur.execute("UPDATE products SET throughput = ? WHERE id = ?", (f"{m.group(1)} {m.group(2)}/hour", pid))

    # Migrate existing LIKE-based distributor matching into the proper join table
    manufacturers_all = cur.execute("SELECT id, name FROM manufacturers").fetchall()
    distributors_existing = cur.execute("SELECT id, name, represents FROM distributors").fetchall()
    for mid, mname in manufacturers_all:
        name_key = mname.split(" (")[0]
        for did, dname, represents in distributors_existing:
            if represents and name_key.lower() in represents.lower():
                try:
                    cur.execute("INSERT INTO company_distributors (manufacturer_id, distributor_id) VALUES (?,?)", (mid, did))
                except sqlite3.IntegrityError:
                    pass

    # Formalize 23 previously text-only distributor relationships (from manufacturer.ksa_status)
    # into proper distributors + company_distributors rows -- no new facts invented.
    text_only_links = [
        ("Diagnostica Stago", "Stago (direct KSA affiliate office, Riyadh)"),
        ("Bio-Rad (IH-1000/IH-500 line)", "Abdulrehman Algosaibi GTC"),
        ("Terumo BCT", "Abdulrehman Algosaibi GTC"),
        ("Cerus Corporation", "Arabian medical house company"),
        ("Roche Diagnostics (NAT/Molecular line)", "Roche Diagnostics Saudi Arabia L.L.C (direct subsidiary)"),
        ("Sysmex", "Sysmex LLC Company (direct KSA entity)"),
        ("Mindray", "Abdulla Fouad for medical supplies"),
        ("Beckman Coulter", "Beckman Coulter Saudi Arabia Co. Ltd (direct entity)"),
        ("Beckman Coulter", "Dar Al-Zahrawi Medical Company"),
        ("Abbott Core Diagnostics", "Medical Supplies & Services Co Ltd"),
        ("Siemens Healthineers", "Abdulrehman Algosaibi GTC"),
        ("Siemens Healthineers", "Sysmex LLC Company"),
        ("Tosoh", "Abdulla Fouad for medical supplies"),
        ("Sebia", "Abdulla Fouad for medical supplies"),
        ("Alcor Scientific", "Dar Al-Zahrawi Medical Company"),
        ("Werfen (ACL/hemostasis line)", "Abdulla Fouad for medical supplies"),
        ("Tcoag Ireland Limited (a Stago Group company)", "Diagnostic Saudi Arabia Trading Company"),
        ("Chrono-log", "Dar Al-Zahrawi Medical Company"),
        ("Miltenyi Biotec", "HOME OF GULF ELITE EST."),
        ("Fresenius Kabi (blood bag line)", "Abdulla Fouad for medical supplies"),
        ("Fresenius Kabi (blood bag line)", "Arabian Trade House"),
        ("Demophorius", "Arabian Medical and Pharmaceutical Co."),
        ("JMS (blood bag line)", "Farabi Trading Establishment"),
        ("Streck", "Samir Trading & Marketing (also known as Samir Group)"),
        ("Cepheid (a Danaher company)", "Beckman Coulter Saudi Arabia CO.LT"),
    ]
    name_to_id5 = {row[1]: row[0] for row in cur.execute("SELECT id, name FROM manufacturers").fetchall()}
    dist_name_to_id = {row[1]: row[0] for row in cur.execute("SELECT id, name FROM distributors").fetchall()}
    for mname, dname in text_only_links:
        mid = name_to_id5.get(mname)
        if not mid:
            continue
        did = dist_name_to_id.get(dname)
        if not did:
            cur.execute("""INSERT INTO distributors (name, country, represents, source, market_strength_tier, market_strength_basis)
                VALUES (?,?,?,?,?,?)""",
                (dname, "Saudi Arabia", mname, "Extracted from manufacturer.ksa_status (already-verified NUPCO/company data), formalized into structured table",
                 "Insufficient data", "Distributor row newly formalized from prior text-only confirmation; principal count not yet fully audited."))
            did = cur.lastrowid
            dist_name_to_id[dname] = did
        try:
            cur.execute("INSERT INTO company_distributors (manufacturer_id, distributor_id) VALUES (?,?)", (mid, did))
        except sqlite3.IntegrityError:
            pass

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','schema_migration','v1.9: Added origin classification (American/European/Chinese/Asian-other), extended products (department/throughput/certifications), created and populated company_distributors many-to-many join table (72 links total, including 23 formalized from prior text-only ksa_status mentions)')")

    # --- v2.0: manufacturer contact fields (phone/email/contact_url) + 3 new lab departments ---
    v2_manufacturers = [
        dict(name="Euroimmun (a PerkinElmer company)", headquarters="Germany", origin="European", website="euroimmun.com",
             portfolio="Autoimmune, infection, and allergy diagnostics: ELISA, IFA, immunoblot (EUROLINE), and chemiluminescence (ChLIA) test systems and automation",
             ksa_status="Covered -- Samir Trading & Marketing CJSC named as the official KSA distributor on Euroimmun's own distributor-locator page, with verified contact details",
             status_tag="covered", opportunity_note="Low -- already has confirmed KSA distribution via Samir Trading & Marketing", confidence_tier="gold",
             sources="euroimmun.com official distributor page (EUROIMMUN Analyzer I / EUROLabWorkstation ELISA pages) -- lists Samir Trading & Marketing CJSC, Jeddah/Al Khobar, phone +966 8942674, email jalal.stouhi@samirgroup.com",
             category="Immunology & Serology", phone=None, email=None, contact_url="https://www.euroimmun.com/contact/"),
        dict(name="Randox Laboratories", headquarters="United Kingdom", origin="European", website="randox.com",
             portfolio="Clinical chemistry analyzers (RX series), Biochip Array Technology for multiplex immunoassay, Acusera third-party quality control materials",
             ksa_status="Unclear -- Randox's own distributor pages confirm Saudi Arabia as a served market, but no specific named KSA distributor entity was found in public sources reviewed",
             status_tag="unclear", opportunity_note="Medium -- served market confirmed but exact local distributor not yet identified; worth a direct outreach to Randox to confirm their current KSA partner", confidence_tier="silver",
             sources="randox.com; medicaldevices.icij.org (FDA device registration listing Saudi Arabia in Randox's foreign distribution list); bgi.com/us/IVD-Partner-Randox",
             category="Clinical Chemistry", phone=None, email=None, contact_url="https://www.randox.com/contact-us/"),
        dict(name="Leica Biosystems (a Danaher company)", headquarters="Germany", origin="European", website="leicabiosystems.com",
             portfolio="Anatomical pathology workflow: HistoCore tissue processors/embedding/microtomes/cryostats, Aperio digital pathology scanners, IHC/ISH staining automation",
             ksa_status="Covered -- Beckman Coulter Saudi Arabia CO.LT confirmed as NUPCO-awarded vendor for a Leica Biosystems Nussloch GmbH part (tissue processor carbon filter)",
             status_tag="covered", opportunity_note="Low -- already has confirmed KSA distribution via Beckman Coulter Saudi Arabia CO.LT", confidence_tier="silver",
             sources="NUPCO Tender NPT0003/25 (Lab Supplies Supplement), item citing 'Beckman Coulter Saudi Arabia CO.LT -Orig- Leica Biosystems Nussloch GmBH' for part 14049543860 -- uploaded by user. Only one part-level confirmation found; broader instrument-level distribution not independently verified -- tier held at silver.",
             category="Histopathology & Cytology", phone=None, email=None, contact_url="https://www.leicabiosystems.com/contact-us/"),
    ]
    v2_ids = {}
    for m in v2_manufacturers:
        cur.execute("""INSERT INTO manufacturers
            (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category, origin, phone, email, contact_url)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (m["name"], m["headquarters"], m["website"], m["portfolio"], m["ksa_status"], m["status_tag"],
             m["opportunity_note"], m["confidence_tier"], m["sources"], m["category"], m["origin"], m["phone"], m["email"], m["contact_url"]))
        v2_ids[m["name"]] = cur.lastrowid

    v2_products = [
        ("Euroimmun (a PerkinElmer company)", "EUROLINE", "Multiplex immunoblot", "Multiplex line immunoblot technology for simultaneous detection of multiple autoantibodies on a single strip", "euroimmun.com"),
        ("Euroimmun (a PerkinElmer company)", "EUROIMMUN Analyzer I", "Automated ELISA processor", "Fully automated ELISA processing, up to 7 microplates / 180 samples per run", "euroimmun.com/products/automation/elisa/euroimmun-analyzer-i/"),
        ("Euroimmun (a PerkinElmer company)", "EUROLabWorkstation ELISA", "Automated ELISA processor", "High-throughput automated ELISA workstation, up to 15 microplates / 700 samples, 200 tests/hour", "euroimmun.com/products/automation/elisa/eurolabworkstation-elisa/"),
        ("Randox Laboratories", "RX monaco", "Clinical chemistry analyzer", "Fully automated clinical chemistry analyzer for low-to-mid volume laboratories", "randox.com/core-disciplines/chemistry"),
        ("Randox Laboratories", "Biochip Array Technology", "Multiplex immunoassay platform", "Simultaneous detection of multiple analytes from a single patient sample on a biochip", "selectscience.net/company/randox-laboratories-ltd"),
        ("Randox Laboratories", "Acusera QC materials", "Quality control reagent", "Third-party quality control materials, including Acusera 24-7 Live Online interlaboratory data management", "selectscience.net/company/randox-laboratories-ltd"),
        ("Leica Biosystems (a Danaher company)", "HistoCore PELORIS 3", "Automated tissue processor", "Automated sample preparation system for histology laboratories", "medicalexpo.com/prod/leica-biosystems-95735.html"),
        ("Leica Biosystems (a Danaher company)", "HistoCore PEGASUS Plus", "Automated tissue processor", "Floor-standing automated tissue processor for histology", "medicalexpo.com/prod/leica-biosystems-95735.html"),
        ("Leica Biosystems (a Danaher company)", "Aperio GT 450 / GT 180 DX", "Digital pathology scanner", "Whole-slide digital pathology scanners; GT 180 DX is a compact 180-slide-capacity scanner with AI-powered QC", "leicabiosystems.com"),
        ("Leica Biosystems (a Danaher company)", "HistoCore AUTOCUT / BIOCUT / MULTICUT", "Microtome", "Fully automated, semi-automated, and manual rotary microtomes for tissue sectioning", "leicabiosystems.com/histology-equipment/"),
    ]
    for mname, pname, ptype, desc, src in v2_products:
        cur.execute("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)",
                    (v2_ids[mname], pname, ptype, desc, src, [m["category"] for m in v2_manufacturers if m["name"]==mname][0]))

    v2_evidence = [
        ("Euroimmun (a PerkinElmer company)", "Samir Trading & Marketing CJSC named as official KSA distributor with verified phone/email on Euroimmun's own distributor-locator page", "distributor's own manufacturer listing", "euroimmun.com distributor pages (EUROIMMUN Analyzer I, EUROLabWorkstation ELISA)"),
        ("Leica Biosystems (a Danaher company)", "Beckman Coulter Saudi Arabia CO.LT named as NUPCO-awarded vendor for a Leica Biosystems Nussloch GmbH part", "tender_award", "NPT0003/25, part 14049543860, source: uploaded PDF"),
    ]
    cur.executemany("INSERT INTO evidence (manufacturer_id, claim, evidence_type, source_detail) VALUES (?,?,?,?)",
                     [(v2_ids[n], c, et, sd) for n, c, et, sd in v2_evidence])

    cur.execute("UPDATE distributors SET represents = represents || ', Euroimmun' WHERE name LIKE 'Samir Trading%'")
    samir_id_row = cur.execute("SELECT id FROM distributors WHERE name LIKE 'Samir Trading%'").fetchone()
    if samir_id_row:
        cur.execute("INSERT INTO company_distributors (manufacturer_id, distributor_id) VALUES (?,?)", (v2_ids["Euroimmun (a PerkinElmer company)"], samir_id_row[0]))

    beckman_ksa_row = cur.execute("SELECT id FROM distributors WHERE name LIKE '%Beckman Coulter Saudi Arabia%'").fetchone()
    if beckman_ksa_row:
        cur.execute("INSERT INTO company_distributors (manufacturer_id, distributor_id) VALUES (?,?)", (v2_ids["Leica Biosystems (a Danaher company)"], beckman_ksa_row[0]))
    else:
        cur.execute("""INSERT INTO distributors (name, country, represents, source, market_strength_tier, market_strength_basis)
            VALUES (?,?,?,?,?,?)""",
            ("Beckman Coulter Saudi Arabia CO.LT", "Saudi Arabia", "Leica Biosystems (a Danaher company), Cepheid (a Danaher company)",
             "NUPCO Tender NPT0003/25 and NPT0028/24 -- uploaded by user", "Tenure-verified (partial)",
             "Confirmed principal for both Leica Biosystems and Cepheid (both Danaher divisions). Not independently confirmed for overall company size."))
        cur.execute("INSERT INTO company_distributors (manufacturer_id, distributor_id) VALUES (?,?)", (v2_ids["Leica Biosystems (a Danaher company)"], cur.lastrowid))

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','v2.0: Added contact fields (phone/email/contact_url) to manufacturers -- shown only on manufacturer cards per requirement. Added 3 new manufacturers across 3 new lab departments: Euroimmun (Immunology & Serology), Randox Laboratories (Clinical Chemistry), Leica Biosystems (Histopathology & Cytology). This is a first batch (3 of the requested ~15); remaining categories/companies to be researched in follow-up rounds.')")

    # --- v2.1: DiaSorin + Radiometer + Abbott i-STAT extension ---
    v21_manufacturers = [
        dict(name="DiaSorin", headquarters="Italy", origin="European", website="diasorin.com",
             portfolio="LIAISON family of CLIA immunoassay analyzers for infectious disease, autoimmune, and specialty testing; molecular diagnostics via Luminex acquisition",
             ksa_status="Unclear -- DiaSorin's own distributor page lists Saudi Arabia among markets served by its 200+ independent distributor network, but no specific named KSA distributor entity was found in public sources reviewed",
             status_tag="unclear", opportunity_note="Medium -- served market confirmed but exact local distributor not yet identified", confidence_tier="silver",
             sources="diasorin.com/en/company/worldwide-contacts/immunodiagnostics-distributors; us.diasorin.com product pages", category="Immunology & Serology"),
        dict(name="Radiometer (a Danaher company)", headquarters="Denmark", origin="European", website="radiometer.com",
             portfolio="ABL blood gas analyzer family (ABL80/90/800/900 FLEX) for point-of-care and central lab blood gas, electrolyte, and metabolite testing",
             ksa_status="Covered -- independent KSA academic study (Majmaah University, Prince Mohammed bin Abdulaziz Hospital Riyadh) confirms active clinical use of ABL90 (24% of surveyed POCT devices) and ABL800 (20.9%) in Saudi hospitals; no specific distributor entity named in the source reviewed",
             status_tag="covered", opportunity_note="Low -- real clinical installed base confirmed in KSA hospitals, though the specific distributor entity is not yet identified", confidence_tier="silver",
             sources="Al-shahrani & Khan, 'Evaluation of ABL90 and ABL800 Radiometer Blood Gas Analyzers... in Saudi Arabia', Healthcare 2025, 13(3), 331, DOI: 10.3390/healthcare13030331", category="Clinical Chemistry"),
    ]
    v21_ids = {}
    for m in v21_manufacturers:
        cur.execute("""INSERT INTO manufacturers
            (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category, origin)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (m["name"], m["headquarters"], m["website"], m["portfolio"], m["ksa_status"], m["status_tag"],
             m["opportunity_note"], m["confidence_tier"], m["sources"], m["category"], m["origin"]))
        v21_ids[m["name"]] = cur.lastrowid

    v21_products = [
        ("DiaSorin", "LIAISON XL", "CLIA immunoassay analyzer", "High-throughput fully automated chemiluminescence analyzer with Reagent Integral cartridge format, connects to lab automation tracks", "us.diasorin.com/en/immunodiagnostics/tools/liaison-xl"),
        ("DiaSorin", "LIAISON QuantiFERON-TB Gold Plus", "TB immunoassay", "Latent tuberculosis detection assay on the LIAISON XL platform", "us.diasorin.com/en/immunodiagnostics/tools/liaison-xl"),
        ("DiaSorin", "LIAISON Calprotectin", "GI immunoassay", "Aid in diagnosis and differentiation of inflammatory bowel disease (Crohn's/ulcerative colitis) from IBS", "us.diasorin.com/en/immunodiagnostics"),
        ("Radiometer (a Danaher company)", "ABL90 FLEX", "Portable blood gas analyzer", "Bedside/POCT blood gas analyzer designed for speed and portability", "sciencedirect.com/topics/chemistry/blood-gas-analysis"),
        ("Radiometer (a Danaher company)", "ABL800 FLEX", "Central lab blood gas analyzer", "Comprehensive blood gas analyzer designed for scalability in centralized laboratory operations, automated sampling", "researchgate.net (Al-shahrani & Khan 2025 study)"),
    ]
    for mname, pname, ptype, desc, src in v21_products:
        cur.execute("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)",
                    (v21_ids[mname], pname, ptype, desc, src, [m["category"] for m in v21_manufacturers if m["name"]==mname][0]))

    cur.execute("INSERT INTO evidence (manufacturer_id, claim, evidence_type, source_detail) VALUES (?,?,?,?)",
                (v21_ids["Radiometer (a Danaher company)"], "Independent peer-reviewed KSA study confirms ABL90 (24% of surveyed devices) and ABL800 (20.9%) in active clinical use at Prince Mohammed bin Abdulaziz Hospital, Riyadh", "peer-reviewed publication", "Al-shahrani & Khan, Healthcare 2025, 13(3), 331, DOI: 10.3390/healthcare13030331"))

    abbott_row = cur.execute("SELECT id FROM manufacturers WHERE name = 'Abbott Core Diagnostics'").fetchone()
    if abbott_row:
        cur.execute("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)",
            (abbott_row[0], "i-STAT System", "Handheld POCT blood gas/chemistry analyzer",
             "Handheld point-of-care analyzer using single-use cartridges for blood gas, electrolytes, chemistries; ~65uL whole blood sample, validated against central lab analyzers in KSA sepsis-triage research",
             "pubmed.ncbi.nlm.nih.gov/36696550 (i-STAT vs Radiometer ABL800 comparability study)", "Hematology"))

    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','v2.1: Added DiaSorin (Immunology & Serology) and Radiometer (Clinical Chemistry/POCT blood gas, verified via independent peer-reviewed KSA study) + extended existing Abbott Core Diagnostics with i-STAT POCT product line.')")

    # --- Session 1 of 10-session roadmap: Immunoassay depth ---
    cur.execute("""INSERT INTO manufacturers
        (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category, origin)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        ("Fujirebio (an H.U. Group company)", "Japan", "fujirebio.com",
         "LUMIPULSE G series CLEIA immunoassay analyzers for oncology, neurology (Alzheimer's biomarkers), thyroid, fertility, infectious disease markers",
         "Unclear -- Fujirebio's own product pages direct buyers to 'contact your local Fujirebio representative' without naming a specific KSA distributor entity in sources reviewed",
         "unclear", "Medium -- global company with broad menu but exact KSA distributor not yet identified", "silver",
         "fujirebio.com product pages (LUMIPULSE G1200, G600II, various assay cartridges)", "Immunology & Serology", "Asian (other)"))
    fujirebio_id = cur.lastrowid
    cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,'Immunology & Serology')", [
        (fujirebio_id, "LUMIPULSE G1200", "CLEIA immunoassay analyzer", "Mid-sized fully automated CLEIA analyzer, 120 tests/hour, mono test cartridge concept", "fujirebio.com/en/products-solutions/lumipulser-g1200"),
        (fujirebio_id, "LUMIPULSE G600II", "CLEIA immunoassay analyzer", "Compact benchtop CLEIA analyzer, 60 tests/hour, same cartridge concept as G1200", "fujirebio.com/en/products-solutions/lumipulse-g600ii"),
        (fujirebio_id, "Lumipulse G pTau 217 CSF assay", "Neurology biomarker assay", "Blood/CSF-based Alzheimer's disease biomarker assay, part of Fujirebio's expanding neurological pipeline", "fujirebio.com (2025 product announcement)"),
    ])
    ortho_row = cur.execute("SELECT id FROM manufacturers WHERE name LIKE 'Ortho Clinical%'").fetchone()
    if ortho_row:
        cur.execute("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)",
            (ortho_row[0], "VITROS ECiQ Immunodiagnostic System", "Immunoassay analyzer",
             "Compact immunoassay system with no plumbing/drains/deionized water requirement; menu includes SARS-CoV-2, HIV combo, procalcitonin, immunosuppressive drugs, drugs of abuse",
             "cardinalhealth.com (Ortho VITROS ECiQ product page)", "Immunology & Serology"))
    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','Session 1 (Immunoassay): Added Fujirebio (unclear KSA status) + extended Ortho Clinical Diagnostics with VITROS ECiQ immunoassay product')")

    # --- Session 2 of 10-session roadmap: Flow Cytometry ---
    bd_row = cur.execute("SELECT id FROM manufacturers WHERE name = 'BD (Becton, Dickinson and Company)'").fetchone()
    beckman_row = cur.execute("SELECT id FROM manufacturers WHERE name = 'Beckman Coulter'").fetchone()
    if bd_row and beckman_row:
        cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)", [
            (bd_row[0], "BD FACSLyric", "Flow cytometer", "High-performance clinical/research flow cytometer, 4/6/8/10/12-color configurations, BD FACSuite software with automation API for robotic integration", "bdbiosciences.com/en-us/products/instruments/flow-cytometers/clinical-cell-analyzers/facslyric", "Immunology & Serology"),
            (bd_row[0], "BD Multitest Reagents / BD Trucount Tubes", "Flow cytometry reagent", "Absolute counting reagent system for immunological assessment (e.g. HIV immune deficiency monitoring) on FACSLyric", "bdbiosciences.com/en-us/products/instruments/flow-cytometers/clinical-cell-analyzers/facslyric", "Immunology & Serology"),
            (beckman_row[0], "DxFLEX", "Flow cytometer", "Clinical flow cytometer derived from CytoFLEX platform, 13-color capability (10-color IVD-cleared with ClearLLab 10C in the US), APD detector technology, up to 25M events/file", "beckman.com/flow-cytometry/clinical-flow-cytometers/dxflex", "Hematology"),
            (beckman_row[0], "ClearLLab 10C Reagent System", "Flow cytometry reagent panel", "IVD-cleared 10-color reagent panels for leukemia/lymphoma immunophenotyping on DxFLEX", "beckman.com/flow-cytometry/clinical-flow-cytometers/dxflex", "Hematology"),
        ])
    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('products','0','bulk_insert','Session 2 (Flow Cytometry): Extended BD with FACSLyric flow cytometer + Multitest/Trucount reagents (Immunology & Serology dept), extended Beckman Coulter with DxFLEX + ClearLLab 10C (Hematology dept) -- both use existing confirmed KSA distributor links. Cytek Biosciences deferred to a follow-up session.')")

    # --- Session 3 of 10-session roadmap: Urinalysis ---
    siemens_row = cur.execute("SELECT id FROM manufacturers WHERE name = 'Siemens Healthineers'").fetchone()
    if siemens_row:
        cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)", [
            (siemens_row[0], "CLINITEK Advantus", "Semi-automated urine chemistry analyzer", "Auto-Checks strip-reading analyzer, 7 sec/sample, up to 500 tests/hour, Multistix 10 SG strip family", "siemens-healthineers.com/en-us/urinalysis-products/urinalysis-systems/clinitek-advantus-urine-chemistry-analyzer", "Clinical Chemistry"),
            (siemens_row[0], "CLINITEK Status+", "POCT urinalysis analyzer", "Automated point-of-care urinalysis + urine hCG pregnancy dual-purpose analyzer, results in 1 minute", "siemens-healthineers.com/en-us/poct-urinalysis/clinitek-status-plus", "Clinical Chemistry"),
            (siemens_row[0], "Atellica 1500 Automated Urinalysis System", "Fully automated urinalysis system", "Combines CLINITEK Novus and Atellica UAS 800 into one fully automated urinalysis + sediment system; includes ACR (albumin-to-creatinine ratio) kidney-disease screening", "siemens-healthineers.com/en-sa/point-of-care-testing/featured-topics-in-poct/urinalysis-featured-topics/acr-urine-testing", "Clinical Chemistry"),
        ])
    cur.execute("""INSERT INTO manufacturers
        (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category, origin)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        ("ARKRAY", "Japan", "arkray.eu",
         "Urinalysis analyzers and test strips; also a major player in diabetes/glucose monitoring test strips",
         "Unclear -- no specific KSA distributor entity found in public sources reviewed; Arkray operates regional sites (arkrayusa.com, arkray.eu) without a KSA-specific distributor page located",
         "unclear", "Medium -- established global urinalysis brand, KSA distributor not yet identified", "bronze",
         "arkrayusa.com/clinical-diagnostics/products/urinalysis/; arkray.eu/english/products/urinalysis_urine_testing/",
         "Clinical Chemistry", "Asian (other)"))
    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','Session 3 (Urinalysis): Extended Siemens Healthineers with CLINITEK Advantus/Status+ and Atellica 1500 urinalysis products (real Saudi-specific Siemens page found for ACR testing). Added ARKRAY as new manufacturer -- bronze tier since no KSA distributor found and portfolio confirmation was limited to general product category pages.')")

    # --- Session 4: POCT ---
    roche_row = cur.execute("SELECT id FROM manufacturers WHERE name = 'Roche Diagnostics (NAT/Molecular line)'").fetchone()
    if roche_row:
        cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)", [
            (roche_row[0], "cobas pulse", "POCT blood glucose analyzer", "App-based blood glucose management system, meets CLSI POCT12-A3 criteria, tested against 140+ interferents", "diagnostics.roche.com/global/en/products/instruments/cobas-pulse-system.html", "Clinical Chemistry"),
            (roche_row[0], "CoaguChek XS / Pro II / Vantus", "POCT coagulation analyzer", "Point-of-care INR/PT monitoring system family for anticoagulation therapy management, since 1992", "diagnostics.roche.com/us/en/products/product-category/brand/coaguchek.html", "Coagulation"),
        ])
    cur.execute("""INSERT INTO manufacturers
        (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category, origin)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        ("QuidelOrtho", "USA", "quidelortho.com",
         "Point-of-care and central lab diagnostics: rapid lateral flow tests, benchtop POCT instruments, and molecular solutions",
         "Covered -- QuidelOrtho maintains a dedicated Saudi Arabia country site (quidelortho.com/sa/en/) confirming active KSA market presence, though a specific named local distributor entity was not identified in sources reviewed",
         "unclear", "Low-Medium -- confirmed dedicated KSA web presence but specific distributor not yet identified", "silver",
         "quidelortho.com/sa/en/laboratory-professionals/clinical-chemistry-immunoassay/lab-supplies/controls-and-supplies-labs; quidelortho.com/global/en/laboratory-professionals/point-of-care-testing",
         "Clinical Chemistry", "American"))
    quidel_id = cur.lastrowid
    cur.execute("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)",
        (quidel_id, "QuidelOrtho POCT Platform", "Point-of-care testing instruments + lateral flow tests", "Range of near-patient testing solutions from rapid lateral flow tests to portable benchtop instruments for clinics, urgent care, and pharmacy settings", "quidelortho.com/global/en/laboratory-professionals/point-of-care-testing", "Clinical Chemistry"))
    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','Session 4 (POCT): Extended Roche Diagnostics with cobas pulse + CoaguChek POCT products. Added QuidelOrtho -- confirmed dedicated KSA country website but no named local distributor.')")

    # --- Session 5: Laboratory Automation ---
    la_manufacturers = [
        dict(name="Inpeco", headquarters="Switzerland", origin="European", website="inpeco.com",
             portfolio="FlexLab Total Laboratory Automation (TLA) system -- open track connecting 50+ analyzer types across 10+ specialties; ProTube pre-analytical sample automation suite",
             ksa_status="Unclear -- no specific KSA distributor entity found in public sources reviewed",
             status_tag="unclear", opportunity_note="Medium -- established global TLA leader (1700+ installations worldwide, Frost & Sullivan 2018 Company of the Year), KSA distributor not yet identified", confidence_tier="silver",
             sources="inpeco.com/our-automation-solutions/lab-automation-system/; bio-rad.com (Inpeco-Bio-Rad FlexLab partnership announcement)", category="Clinical Chemistry"),
        dict(name="Tecan", headquarters="Switzerland", origin="European", website="tecan.com",
             portfolio="Laboratory automation instruments for life sciences and applied markets: liquid handling, plate readers (Spark Cyto), OEM automation solutions for clinical diagnostics",
             ksa_status="Unclear -- Tecan's own distributor directory lists a Middle East/Gulf regional partner (Alqiffaf Scientific Co.) but the exact country scope was not clearly confirmed as KSA-specific in the source page reviewed",
             status_tag="unclear", opportunity_note="Medium -- global automation leader; distributor relationship needs direct confirmation before treating as KSA-covered", confidence_tier="bronze",
             sources="tecan.com/tecan-distributors-worldwide (regional distributor listing, KSA-specific scope not clearly confirmed)", category="Clinical Chemistry"),
    ]
    la_ids = {}
    for m in la_manufacturers:
        cur.execute("""INSERT INTO manufacturers
            (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category, origin)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (m["name"], m["headquarters"], m["website"], m["portfolio"], m["ksa_status"], m["status_tag"],
             m["opportunity_note"], m["confidence_tier"], m["sources"], m["category"], m["origin"]))
        la_ids[m["name"]] = cur.lastrowid
    cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)", [
        (la_ids["Inpeco"], "FlexLab", "Total Laboratory Automation (TLA) track system", "Open TLA system with 30+ pre/post-analytical modules and 50+ analyzer connections across 10+ specialties, full sample traceability", "inpeco.com/our-automation-solutions/lab-automation-system/", "Clinical Chemistry"),
        (la_ids["Inpeco"], "ProTube Suite", "Pre-analytical sample automation", "Covers sample preparation, transportation, and delivery to the clinical laboratory", "inpeco.com/our-automation-solutions/", "Clinical Chemistry"),
        (la_ids["Tecan"], "Spark Cyto", "Multi-mode plate reader", "Plate reader with fluorescence imaging and cytometry capabilities for cell-based research", "lifesciences.tecan.com/products", "Molecular Diagnostics"),
    ])
    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','Session 5 (Laboratory Automation): Added Inpeco and Tecan, both unclear KSA distribution.')")

    # --- Session 9: Molecular/Chemistry re-attempt ---
    s9_manufacturers = [
        dict(name="Sansure Biotech", headquarters="China", origin="Chinese", website="sansureglobal.com",
             portfolio="Molecular diagnostics: SLAN series real-time PCR systems, automated nucleic acid extraction, one-tube/magnetic-bead reagent technology for infectious disease, HPV, and NAT blood screening",
             ksa_status="Unclear -- no specific KSA distributor entity found; company confirms presence in ~160 countries and certificates in 65+ countries (NMPA China, FDA EUA, ANVISA, TGA Australia) but Saudi Arabia not specifically named among sources reviewed",
             status_tag="unclear", opportunity_note="Medium -- large global molecular diagnostics player with broad international certification footprint, KSA distributor not yet identified", confidence_tier="silver",
             sources="sansureglobal.com; linkedin.com/company/sansure-biotech-inc; sansureglobal.com/product-category/instrument/real-time_pcr_system/", category="Molecular Diagnostics"),
        dict(name="Maccura Biotechnology", headquarters="China", origin="Chinese", website="maccura.com",
             portfolio="Broad IVD platform: i6000 chemiluminescent immunoassay analyzer, F680 hematology analyzer, C1000/C2000 clinical chemistry analyzers, LABAS MAX/MIX total laboratory automation, coagulation and molecular diagnostics lines",
             ksa_status="Unclear -- confirmed regional presence via Medlab Middle East exhibition (Dubai) and a distributor gala event, but no specific KSA distributor entity named in sources reviewed",
             status_tag="unclear", opportunity_note="Medium -- founded 1994, first Chinese IFCC member (2010), broad multi-department IVD portfolio; KSA distributor not yet identified", confidence_tier="silver",
             sources="linkedin.com/company/maccura-biotechnology (Medlab ME Dubai exhibition, 2024 Distributor Gala); youtube.com/@maccurabiotechnology8935", category="Clinical Chemistry"),
    ]
    s9_ids = {}
    for m in s9_manufacturers:
        cur.execute("""INSERT INTO manufacturers
            (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category, origin)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (m["name"], m["headquarters"], m["website"], m["portfolio"], m["ksa_status"], m["status_tag"],
             m["opportunity_note"], m["confidence_tier"], m["sources"], m["category"], m["origin"]))
        s9_ids[m["name"]] = cur.lastrowid
    cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)", [
        (s9_ids["Sansure Biotech"], "SLAN Series Real-Time PCR System", "Real-time PCR instrument", "Fluorescence-based real-time PCR instruments for nucleic acid detection and quantification", "crunchbase.com/organization/sansure-biotech", "Molecular Diagnostics"),
        (s9_ids["Sansure Biotech"], "iPonatic Portable Molecule Workstation", "Portable molecular POCT device", "Portable molecular diagnostics workstation for clinical emergency, health management, and field/military applications", "sansureglobal.com/product-category/instrument/real-time_pcr_system/", "Molecular Diagnostics"),
        (s9_ids["Maccura Biotechnology"], "i6000", "Chemiluminescent immunoassay analyzer", "Automated CLIA immunoassay analyzer, part of Maccura's core diagnostic platform lineup", "linkedin.com/company/maccura-biotechnology", "Immunology & Serology"),
        (s9_ids["Maccura Biotechnology"], "F680", "Hematology analyzer", "Automated hematology analyzer from Maccura's diagnostic platform range", "linkedin.com/company/maccura-biotechnology", "Hematology"),
        (s9_ids["Maccura Biotechnology"], "LABAS MAX / MIX", "Total laboratory automation", "Total laboratory automation system managing sporadic and continuous sample submissions across multiple analyzer positions", "linkedin.com/company/maccura-biotechnology", "Clinical Chemistry"),
    ])
    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','Session 9 (Molecular/Chemistry re-attempt): Added Sansure Biotech and Maccura Biotechnology -- honestly marked unclear KSA distribution.')")

    # --- Session 6: Cytology & Digital Pathology ---
    hologic_row = cur.execute("SELECT id FROM manufacturers WHERE name = 'Hologic'").fetchone()
    bd_row2 = cur.execute("SELECT id FROM manufacturers WHERE name = 'BD (Becton, Dickinson and Company)'").fetchone()
    if hologic_row and bd_row2:
        cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)", [
            (hologic_row[0], "ThinPrep Pap Test", "Liquid-based cytology test", "Most widely used liquid-based cytology test globally (1B+ performed); FDA-approved for HPV, chlamydia/gonorrhea, trichomoniasis testing from same vial", "hologic.com/hologic-products/collection-devices/thinprep-pap-test", "Histopathology & Cytology"),
            (hologic_row[0], "ThinPrep 5000 / Genesis Processor", "Cytology specimen processor", "Automated liquid-based cytology specimen preparation, up to 8 hours walkaway time, automated chain-of-custody", "hologic.com/hologic-products/cytology/thinprep-processors", "Histopathology & Cytology"),
            (bd_row2[0], "BD SurePath Liquid-Based Pap Test", "Liquid-based cytology test", "FDA-approved liquid-based cervical cytology system, alternative to ThinPrep, compatible with multiple HPV testing platforms", "academic.oup.com/ajcp (BD SurePath DTS cervical cytology study, 2024)", "Histopathology & Cytology"),
            (bd_row2[0], "BD FocalPoint Slide Profiler", "Automated cytology screening system", "Automated imaging system for cervical cytology slide screening/ranking, compared against ThinPrep Imaging System in clinical studies", "science.gov/topicpages/b/bd+surepath+cytology", "Histopathology & Cytology"),
        ])
    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('products','0','bulk_insert','Session 6 (Cytology/Digital Pathology): Extended Hologic + BD with cytology products.')")

    # --- Session 7: Rapid Tests ---
    s7_manufacturers = [
        dict(name="SD Biosensor", headquarters="South Korea", origin="Asian (other)", website="sdbiosensor.com",
             portfolio="STANDARD Q rapid lateral flow tests, STANDARD F fluorescence immunoassay, STANDARD E ELISA, STANDARD M point-of-care molecular diagnostics; WHO-listed for latent TB testing",
             ksa_status="Unclear -- no specific KSA distributor entity found in public sources reviewed",
             status_tag="unclear", opportunity_note="Medium -- WHO-recognized global rapid diagnostics leader, KSA distributor not yet identified", confidence_tier="silver",
             sources="sdbiosensor.com; sdbiosensor.com/product/main?bcode=11", category="Microbiology"),
        dict(name="Wondfo (Guangzhou Wondfo Biotech)", headquarters="China", origin="Chinese", website="en.wondfo.com",
             portfolio="Finecare fluorescence immunoassay rapid tests (D-dimer, ProBNP, NGAL, etc.), BGA-101 portable blood gas reader, lateral flow POCT products",
             ksa_status="Unclear -- no specific KSA distributor entity found in public sources reviewed",
             status_tag="unclear", opportunity_note="Medium -- leading Chinese POCT manufacturer, KSA distributor not yet identified", confidence_tier="silver",
             sources="en.wondfo.com; alliedhospitalsupply.com/catalog (Wondfo BGA-101 listing, distributor region not confirmed as KSA)", category="Clinical Chemistry"),
    ]
    s7_ids = {}
    for m in s7_manufacturers:
        cur.execute("""INSERT INTO manufacturers
            (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category, origin)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (m["name"], m["headquarters"], m["website"], m["portfolio"], m["ksa_status"], m["status_tag"],
             m["opportunity_note"], m["confidence_tier"], m["sources"], m["category"], m["origin"]))
        s7_ids[m["name"]] = cur.lastrowid
    cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)", [
        (s7_ids["SD Biosensor"], "STANDARD Q", "Rapid lateral flow test", "Rapid diagnostic test line with high sensitivity/specificity, covers infectious disease parameters", "sdbiosensor.com/product/main?bcode=11", "Microbiology"),
        (s7_ids["SD Biosensor"], "STANDARD M", "POCT molecular diagnostics system", "Point-of-care molecular diagnostics (MDx) system for near-patient clinical decision making", "sdbiosensor.com", "Microbiology"),
        (s7_ids["Wondfo (Guangzhou Wondfo Biotech)"], "Finecare D-Dimer / ProBNP / NGAL Tests", "Fluorescence immunoassay rapid test", "Rapid quantitative fluorescence immunoassay tests for cardiac and renal biomarkers", "tradeindia.com (Wondfo Finecare D-dimer listing)", "Clinical Chemistry"),
        (s7_ids["Wondfo (Guangzhou Wondfo Biotech)"], "BGA-101", "Portable blood gas analyzer", "Portable POCT blood gas reader: oxygenation, pH, electrolytes in ~30 seconds", "alliedhospitalsupply.com/catalog", "Clinical Chemistry"),
    ])
    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','Session 7 (Rapid Tests): Added SD Biosensor and Wondfo.')")

    # --- Session 8: Laboratory Equipment ---
    s8_manufacturers = [
        dict(name="Thermo Fisher Scientific", headquarters="USA", origin="American", website="thermofisher.com",
             portfolio="Broad lab equipment portfolio: centrifuges (mini to industrial floor-standing), thermal cyclers, shakers/incubators, molecular biology reagents",
             ksa_status="Unclear -- independent market research report lists Saudi Arabia within Thermo Fisher's Middle East & Africa regional market coverage for centrifuge equipment, but no specific named KSA distributor entity identified",
             status_tag="unclear", opportunity_note="Medium -- major global lab equipment leader (75+ years in centrifugation), KSA distributor not yet identified", confidence_tier="silver",
             sources="thermofisher.com/us/en/home/life-science/lab-equipment/lab-centrifuges.html; digitaljournal.com (Laboratory Centrifuge Equipment Market report, names Saudi Arabia in MEA region)", category="Clinical Chemistry"),
        dict(name="Eppendorf", headquarters="Germany", origin="European", website="eppendorf.com",
             portfolio="Pipettes, centrifuges (5702/5810R/5430R/MiniSpin series), thermal cyclers, shakers/incubator shakers, cell culture and bioprocess systems",
             ksa_status="Unclear -- Eppendorf maintains a Middle East & Africa regional site (eppendorf.com/ae-en) but no specific named KSA distributor entity identified in sources reviewed",
             status_tag="unclear", opportunity_note="Medium -- established global lab equipment brand with dedicated MEA presence, KSA distributor not yet identified", confidence_tier="silver",
             sources="eppendorf.com/ae-en; fishersci.com/us/en/brands/I9C8LVGA/eppendorf-north-america.html", category="Clinical Chemistry"),
    ]
    s8_ids = {}
    for m in s8_manufacturers:
        cur.execute("""INSERT INTO manufacturers
            (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, category, origin)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (m["name"], m["headquarters"], m["website"], m["portfolio"], m["ksa_status"], m["status_tag"],
             m["opportunity_note"], m["confidence_tier"], m["sources"], m["category"], m["origin"]))
        s8_ids[m["name"]] = cur.lastrowid
    cur.executemany("INSERT INTO products (manufacturer_id, product_name, product_type, description, source, department) VALUES (?,?,?,?,?,?)", [
        (s8_ids["Thermo Fisher Scientific"], "Thermo Scientific X Pro Centrifuge Series", "General purpose centrifuge", "General purpose centrifuge series with Auto-Door, Auto-Lock rotor exchange, ClickSeal biocontainment lids", "thermofisher.com/us/en/home/life-science/lab-equipment/lab-centrifuges.html", "Clinical Chemistry"),
        (s8_ids["Eppendorf"], "Eppendorf Centrifuge 5810 R", "Refrigerated centrifuge", "Refrigerated day-to-day centrifuge for medium-throughput labs, compact footprint, tube and plate format compatible", "fishersci.com/us/en/browse/90180031/centrifuges", "Clinical Chemistry"),
        (s8_ids["Eppendorf"], "Eppendorf MiniSpin / MiniSpin plus", "Microcentrifuge", "Entry-level compact microcentrifuges suitable for individual workstations, molecular biology separations", "fishersci.com/us/en/browse/90180031/centrifuges", "Molecular Diagnostics"),
    ])
    cur.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('database','0','bulk_insert','Session 8 (Lab Equipment): Added Thermo Fisher Scientific and Eppendorf.')")
    conn.commit()

    # --- WP0: Multi-Tenant Auth -- seed the first real user account.
    # Credentials come from ADMIN_EMAIL / ADMIN_PASSWORD env vars. If not set,
    # falls back to a clearly-marked local-only default (never use in production).
    admin_email = os.environ.get("ADMIN_EMAIL", "amr@attieh-medico.com")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    used_fallback = False
    if not admin_password:
        admin_password = "ChangeMe-Local-Only-2026"
        used_fallback = True
    password_hash = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
    cur.execute(
        "INSERT INTO users (email, password_hash, company_name, full_name, role) VALUES (?,?,?,?,?)",
        (admin_email, password_hash, "Attieh Medico", "Amr Elmorshedy", "admin")
    )
    admin_user_id = cur.lastrowid
    cur.execute(
        "INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('users', ?, 'insert', ?)",
        (admin_user_id, f"Seeded first admin account ({admin_email}){' -- USING INSECURE LOCAL FALLBACK PASSWORD, set ADMIN_PASSWORD env var in production' if used_fallback else ''}")
    )
    conn.commit()
    if used_fallback:
        print("WARNING: ADMIN_PASSWORD env var not set. Using insecure local-only fallback")
        print(f"  Login: {admin_email} / ChangeMe-Local-Only-2026")
        print("  Set ADMIN_EMAIL and ADMIN_PASSWORD env vars before deploying anywhere real.")

if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    seed(conn)
    conn.close()
    print(f"Database created at {DB_PATH}")
