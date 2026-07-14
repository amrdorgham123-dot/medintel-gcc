"""
Seed script (batch 7) for MedForsa GCC's Lab Info reference library.
Adds additional autoimmune/rheumatology serology tests.
English-only content per platform policy.

Run once: python3 seed_lab_tests_batch7.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "anti-ccp", "name_en": "Anti-Cyclic Citrullinated Peptide Antibody (Anti-CCP)",
        "aliases": "Anti-CCP, CCP Antibody, ACPA",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Highly specific serologic marker for rheumatoid arthritis (RA), used alongside rheumatoid factor (RF) to support diagnosis, particularly in early or RF-negative disease, and to help predict a more erosive disease course.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Enzyme immunoassay (EIA) or chemiluminescent immunoassay using cyclic citrullinated peptide (CCP2 or CCP3 generation) antigens.",
        "reference_ranges": [{"parameter": "Anti-CCP", "population": "Negative (normal)", "range": "Typically <20 U/mL", "notes": "Cutoff varies by assay/manufacturer, commonly reported in the 5-20 U/mL range -- always use the reporting lab's stated cutoff; results are often further classified as low-positive (up to 3x the upper limit) or high-positive (>3x the upper limit) per 2010 ACR/EULAR criteria"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Anti-CCP has approximately 95-98% specificity for rheumatoid arthritis, meaning a positive result strongly supports the diagnosis in a patient with compatible joint symptoms, and can appear years before clinical disease onset. It is more specific than rheumatoid factor (which is also positive in other conditions and healthy aging individuals) though somewhat less sensitive; testing both together improves diagnostic accuracy. Higher titers, especially high-positive results, are associated with more aggressive disease and greater risk of joint erosion.",
        "associated_conditions": [
            {"condition": "Rheumatoid arthritis (RA)", "direction": "positive"},
            {"condition": "Erosive/aggressive RA disease course", "direction": "high-positive titer"}
        ],
        "sources": [{"name": "PMC - Anti-CCP Revised Criteria for the Classification of Rheumatoid Arthritis", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC2964864/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "complement-c3", "name_en": "Complement C3",
        "aliases": "C3, Complement C3",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Assesses complement system activation; used mainly to monitor systemic lupus erythematosus (SLE) disease activity and to investigate suspected complement deficiency or immune complex-mediated disease.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Complement C3", "population": "Adult", "range": "Approximately 90-180 mg/dL", "notes": "Reference range varies by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low C3 (especially falling alongside rising anti-dsDNA titers) is the most specific laboratory combination for identifying active lupus, particularly lupus nephritis, and can precede abnormalities on urinalysis. Low C3 is also seen in other immune complex-mediated conditions (post-infectious glomerulonephritis, cryoglobulinemia) and consumptive states. Rare hereditary C3 deficiency causes recurrent serious bacterial infections (especially encapsulated organisms) and lupus-like autoimmune features. High C3 is a nonspecific acute-phase reactant finding, of limited clinical significance on its own.",
        "associated_conditions": [
            {"condition": "Active systemic lupus erythematosus / lupus nephritis", "direction": "low, especially with rising anti-dsDNA"},
            {"condition": "Post-infectious glomerulonephritis / cryoglobulinemia", "direction": "low"},
            {"condition": "Hereditary C3 deficiency", "direction": "very low/absent, recurrent bacterial infections"}
        ],
        "sources": [{"name": "Lamkin Clinic - Complement C3: Optimal Levels, Reference Ranges & Immune Interpretation", "url": "https://lamkinclinic.com/complement-c3/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "complement-c4", "name_en": "Complement C4",
        "aliases": "C4, Complement C4",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Assesses complement system activation via the classical pathway; used mainly alongside C3 to monitor SLE disease activity and to investigate hereditary angioedema or complement deficiency.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Complement C4", "population": "Adult", "range": "Approximately 10-40 mg/dL", "notes": "Reference range varies by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low C4 is seen in active SLE (often alongside low C3), immune complex diseases, and hereditary angioedema (due to C1 esterase inhibitor deficiency, which secondarily consumes C4 -- a persistently low C4 between angioedema attacks supports that diagnosis). A chronically low C4 with normal C3 can also reflect hereditary partial C4 deficiency, which is common and usually clinically insignificant on its own but can be a lupus susceptibility factor.",
        "associated_conditions": [
            {"condition": "Active systemic lupus erythematosus", "direction": "low, often with low C3"},
            {"condition": "Hereditary angioedema (C1 esterase inhibitor deficiency)", "direction": "low, even between attacks"}
        ],
        "sources": [{"name": "Bloodsight - Reading an Autoimmune Panel: ANA, RF, Anti-CCP & Complement", "url": "https://bloodsight.com/learn/reading-autoimmune-panel", "accessed": "2026-07-14"}]
    },
    {
        "slug": "anti-dsdna", "name_en": "Anti-Double-Stranded DNA Antibody (Anti-dsDNA)",
        "aliases": "Anti-dsDNA, dsDNA Antibody",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Highly specific marker for systemic lupus erythematosus (SLE); used to support diagnosis and, because titers correlate with disease activity in many patients, to help monitor lupus flares (especially lupus nephritis).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Typically ordered as a reflex/follow-up test after a positive ANA (antinuclear antibody) screen.",
        "methodology_en": "Enzyme immunoassay (EIA), Crithidia luciliae immunofluorescence assay (considered most specific), or the Farr radioimmunoassay technique.",
        "reference_ranges": [{"parameter": "Anti-dsDNA", "population": "Result categories", "range": "Negative or Positive (titer-dependent) -- reported by assay-specific units/titer, not a single universal numeric cutoff"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Anti-dsDNA is highly specific for SLE (much more specific than the broader ANA screen, though less sensitive), and rising titers -- especially alongside falling complement (C3/C4) -- are the most specific laboratory pattern for active lupus, particularly lupus nephritis, and may precede clinical/urinary findings. Titers can fluctuate with disease activity and are sometimes used to help guide treatment intensity in patients with an established SLE diagnosis, though the correlation with activity is not perfect in every patient.",
        "associated_conditions": [
            {"condition": "Systemic lupus erythematosus (SLE)", "direction": "positive, high specificity"},
            {"condition": "Active lupus nephritis / SLE flare", "direction": "rising titer, especially with falling C3/C4"}
        ],
        "sources": [{"name": "Lamkin Clinic - Complement C3, citing anti-dsDNA/C3 inverse relationship in SLE monitoring", "url": "https://lamkinclinic.com/complement-c3/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "anca", "name_en": "Anti-Neutrophil Cytoplasmic Antibody (ANCA)",
        "aliases": "ANCA, c-ANCA, p-ANCA, Anti-PR3, Anti-MPO",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Screens for ANCA-associated vasculitis (granulomatosis with polyangiitis, microscopic polyangiitis, eosinophilic granulomatosis with polyangiitis), particularly when there is unexplained glomerulonephritis, pulmonary hemorrhage, or systemic small-vessel vasculitis.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. A positive screen by immunofluorescence (IFA) is typically confirmed with specific antigen testing (anti-proteinase 3 [PR3] and anti-myeloperoxidase [MPO]).",
        "methodology_en": "Indirect immunofluorescence assay (IFA) for initial pattern screening (cytoplasmic [c-ANCA] or perinuclear [p-ANCA] pattern), confirmed by antigen-specific enzyme immunoassay for anti-PR3 and anti-MPO antibodies.",
        "reference_ranges": [{"parameter": "ANCA (IFA screen and PR3/MPO antigen-specific)", "population": "Result categories", "range": "Negative or Positive, with pattern (c-ANCA/p-ANCA) and antigen specificity (PR3/MPO) reported for positive results"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "c-ANCA with anti-PR3 specificity is classically associated with granulomatosis with polyangiitis (formerly Wegener's granulomatosis). p-ANCA with anti-MPO specificity is more associated with microscopic polyangiitis and eosinophilic granulomatosis with polyangiitis (formerly Churg-Strauss syndrome), though there is overlap. ANCA testing is used alongside clinical findings and often kidney/lung biopsy to diagnose ANCA-associated vasculitis, and antigen-specific titers can help monitor disease activity and relapse risk in some patients, though this correlation is imperfect.",
        "associated_conditions": [
            {"condition": "Granulomatosis with polyangiitis (GPA)", "direction": "c-ANCA / anti-PR3 positive"},
            {"condition": "Microscopic polyangiitis (MPA) / eosinophilic granulomatosis with polyangiitis (EGPA)", "direction": "p-ANCA / anti-MPO positive"}
        ],
        "sources": [{"name": "Labcorp - Patient Care in Rheumatology & Autoimmune Disease (ANCA/anti-MPO/anti-PR3 diagnostic panels)", "url": "https://www.labcorp.com/treatment-areas/rheumatology/clinical-testing/autoimmune-profiles", "accessed": "2026-07-14"}]
    }
]

def main():
    conn = sqlite3.connect(DB_PATH)
    inserted, skipped = 0, 0
    for t in TESTS:
        existing = conn.execute("SELECT id FROM lab_tests WHERE slug = ?", (t["slug"],)).fetchone()
        if existing:
            print(f"SKIP (already exists): {t['slug']}")
            skipped += 1
            continue
        conn.execute(
            """INSERT INTO lab_tests
            (slug, name_en, name_ar, aliases, category, purpose_en, purpose_ar, specimen_type,
             collection_notes_en, collection_notes_ar, methodology_en, methodology_ar,
             reference_ranges_json, reference_ranges_verified, clinical_significance_en, clinical_significance_ar,
             associated_conditions_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             json.dumps(t.get("associated_conditions", [])), json.dumps(t["sources"]),
             1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
