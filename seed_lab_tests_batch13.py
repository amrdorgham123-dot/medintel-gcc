"""
Seed script (batch 13) for MedForsa GCC's Lab Info reference library.
Adds DHEA-Sulfate (adrenal androgen marker).

Run once: python3 seed_lab_tests_batch13.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "dhea-s", "name_en": "Dehydroepiandrosterone Sulfate (DHEA-S), Serum",
        "aliases": "DHEA-S, DHEAS, DHEA Sulfate",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Evaluates adrenal androgen production; used to investigate hirsutism and virilization in women, distinguish adrenal from ovarian sources of excess androgen, evaluate suspected congenital adrenal hyperplasia, and investigate premature adrenarche in children.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Unlike testosterone, DHEA-S has minimal diurnal variation (because of its long half-life and stable sulfate conjugation), so timing of the draw during the day is less critical than for testosterone or cortisol.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) on automated immunoassay analyzers; LC-MS/MS offers greater specificity at the extremes.",
        "reference_ranges": [{"parameter": "DHEA-S", "population": "Adult male", "range": "~28-640 \u00b5g/dL", "notes": "Wide range reflects natural decline with age after young adulthood; reference intervals vary by lab/assay and age band"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "DHEA-S is produced almost exclusively by the adrenal gland (unlike testosterone, which has both ovarian/testicular and adrenal sources), making it useful for distinguishing an adrenal from a gonadal cause of excess androgen. Mild elevation is usually idiopathic or related to PCOS; a level 5-fold or more above the upper limit of normal (often cited around 600 \u00b5g/dL or higher) raises significant concern for an androgen-secreting adrenal tumor, since DHEA-S is elevated in over 90% of such tumors, particularly adrenal carcinomas. DHEA-S is also used alongside 17-hydroxyprogesterone and cortisol in the evaluation of congenital adrenal hyperplasia and premature adrenarche in children.",
        "associated_conditions": [
            {"condition": "Polycystic ovary syndrome (PCOS) / idiopathic hyperandrogenism", "direction": "mildly high"},
            {"condition": "Androgen-secreting adrenal tumor (adenoma or carcinoma)", "direction": "markedly high, often \u2265600 \u00b5g/dL or \u22655x upper limit"},
            {"condition": "Congenital adrenal hyperplasia / premature adrenarche", "direction": "high, interpreted alongside 17-OH progesterone"},
            {"condition": "Adrenal insufficiency", "direction": "low"}
        ],
        "sources": [
            {"name": "Mayo Clinic Laboratories - Dehydroepiandrosterone Sulfate (DHEA-S), Serum (test catalog)", "url": "https://pediatric.testcatalog.org/show/DHES1", "accessed": "2026-07-14"},
            {"name": "ClinicalTrials.gov - Enzalutamide + External Beam RT for Prostate (documented adult male DHEA-S reference range)", "url": "https://clinicaltrials.gov/study/NCT02028988", "accessed": "2026-07-14"}
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
             associated_conditions_json, related_tests_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             json.dumps(t.get("associated_conditions", [])),
             json.dumps(["total-testosterone", "free-testosterone", "cortisol", "lh", "fsh"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
