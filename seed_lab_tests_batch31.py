"""
Seed script (batch 31) for MedForsa GCC's Lab Info reference library.
Adds C1 Esterase Inhibitor (Quantitative and Functional).

Run once: python3 seed_lab_tests_batch31.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "c1-esterase-inhibitor", "name_en": "C1 Esterase Inhibitor (Quantitative and Functional)",
        "aliases": "C1-INH, C1 Inhibitor, HAE Panel",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Diagnoses hereditary or acquired angioedema (C1 esterase inhibitor deficiency), evaluated in patients with recurrent, non-itching episodes of swelling (skin, GI tract, or upper airway) without urticaria, especially with a family history or attacks unresponsive to antihistamines/steroids.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Sample should be processed promptly; functional C1 inhibitor activity can be falsely reduced by transit delay, so a result down to about 40% may still be considered normal if the accompanying C4 level is also normal. Testing is ideally done between attacks for baseline assessment, though it can be checked during an acute episode if diagnosis is urgent.",
        "methodology_en": "C1 esterase inhibitor antigen (protein quantity) is measured by nephelometric or turbidimetric immunoassay; C1 esterase inhibitor functional activity (how well the protein actually works) is measured by a separate chromogenic functional assay, since roughly 15% of hereditary angioedema patients have a normal or even elevated antigen level but a non-functional protein (detectable only by the functional assay).",
        "reference_ranges": [
            {"parameter": "C1 esterase inhibitor, quantitative (antigen)", "population": "Normal", "range": "Assay-specific reference range; patients with hereditary angioedema type I typically have levels at 5-30% of normal"},
            {"parameter": "C1 esterase inhibitor, functional", "population": "Normal", "range": "Assay-specific reference range; reduced in both type I and type II HAE despite a normal antigen level in type II"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low C1 esterase inhibitor antigen with low functional activity supports type I hereditary angioedema (about 85% of hereditary cases), caused by reduced protein production. Normal or elevated antigen with low functional activity supports type II hereditary angioedema (about 15% of cases), where the protein is present but doesn't work -- this is why both the antigen and functional tests are needed together, since testing only the antigen level would miss type II cases. A low C1q level helps distinguish acquired angioedema (low C1q, often associated with a lymphoproliferative disorder or autoantibody) from the hereditary form (normal C1q). C4 is typically low in both hereditary and acquired forms and is often used as an accessible screening test, with C1 inhibitor testing used to confirm the diagnosis and determine the type.",
        "associated_conditions": [
            {"condition": "Hereditary angioedema type I (low antigen and function)", "direction": "low both, ~85% of hereditary cases"},
            {"condition": "Hereditary angioedema type II (normal/high antigen, low function)", "direction": "normal/high antigen, low functional activity, ~15% of hereditary cases"},
            {"condition": "Acquired angioedema (associated with lymphoproliferative disease or autoantibody)", "direction": "low antigen/function with additionally low C1q"}
        ],
        "questions_to_ask_en": "Which type of angioedema does this confirm, and does that affect my treatment options? Do I need C1q testing too, to distinguish hereditary from acquired disease? Should my family members be tested, given this is often hereditary? What should I do if I have an acute attack, especially if it affects my airway?",
        "next_steps": "A confirmed diagnosis leads to a personalized treatment plan that typically includes on-demand therapy for acute attacks (C1 inhibitor concentrate or other targeted therapies), consideration of long-term prophylactic medication depending on attack frequency and severity, an emergency action plan (especially for airway involvement), and often genetic counseling and testing of at-risk family members.",
        "sources": [
            {"name": "Mayo Clinic Laboratories - C1 Esterase Inhibitor Antigen, Serum (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/overview/8198", "accessed": "2026-07-19"},
            {"name": "The Pathology Centre - C1 Esterase Inhibitor (Quantitation and Functional Level)", "url": "https://www.thepathologycentre.org/test/c1-esterase-inhibitor-quantitation-and-functional-level/", "accessed": "2026-07-19"},
            {"name": "PMC - Hereditary angioedema with C1 inhibitor (C1-INH) deficit: the strength of recognition (51 cases)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6247277/", "accessed": "2026-07-19"}
        ]
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
             questions_to_ask_en, next_steps_en,
             associated_conditions_json, related_tests_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             t.get("questions_to_ask_en"), t.get("next_steps"),
             json.dumps(t.get("associated_conditions", [])),
             json.dumps(["complement-c3", "complement-c4", "ch50"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
