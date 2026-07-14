"""
Seed script (batch 17) for MedForsa GCC's Lab Info reference library.
Adds Thyroid Peroxidase Antibody (TPOAb) and Thyroglobulin Antibody (TgAb).

Run once: python3 seed_lab_tests_batch17.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "anti-tpo", "name_en": "Thyroid Antibodies (TPOAb and TgAb)",
        "aliases": "Anti-TPO, TPO Antibody, Thyroid Peroxidase Antibody, Thyroglobulin Antibody, TgAb, Anti-Thyroid Antibodies",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Confirms an autoimmune cause of thyroid dysfunction (Hashimoto's thyroiditis or Graves' disease) when TSH/free T4 are abnormal, and helps predict future thyroid dysfunction in subclinical hypothyroidism or during pregnancy planning; thyroglobulin antibody (TgAb) is also required alongside thyroglobulin tumor marker testing to validate that result in thyroid cancer surveillance.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Usually ordered together with TSH and free T4 rather than in isolation.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) or enzyme immunoassay (EIA) on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "Thyroid peroxidase antibody (TPOAb)", "population": "Normal", "range": "<35 IU/mL", "notes": "Some labs use cutoffs up to 60 IU/mL; assay-dependent"},
            {"parameter": "Thyroglobulin antibody (TgAb)", "population": "Normal", "range": "<20 IU/mL", "notes": "Assay-dependent"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated TPOAb is the most sensitive marker for autoimmune thyroid disease and is positive in the large majority of Hashimoto's thyroiditis cases and roughly 70-80% of Graves' disease cases. TgAb is positive in a similar proportion of Hashimoto's cases and is the only positive antibody in a minority (roughly 10-15%) of cases where TPOAb is negative, which is why both are typically tested together. Both antibodies can be present in roughly 10-15% of the general population without clinical thyroid disease, so a positive result supports but does not by itself diagnose autoimmune thyroid disease -- it must be interpreted alongside TSH, free T4, and clinical findings. TgAb positivity also invalidates thyroglobulin as a reliable tumor marker in post-thyroidectomy cancer surveillance, since the antibody interferes with the assay and can mask a rising thyroglobulin that would otherwise indicate cancer recurrence.",
        "critical_values_en": None,
        "interfering_factors_en": "TgAb positivity artificially suppresses measured thyroglobulin levels in the same blood draw, so a 'low' or 'undetectable' thyroglobulin result cannot be trusted for cancer surveillance purposes when TgAb is positive -- this is a critical interaction to flag when both tests are ordered together in a post-thyroidectomy patient.",
        "questions_to_ask_en": "Given a positive result, do I currently have (or am I at risk of developing) overt thyroid dysfunction, and how often should my TSH be monitored? If I'm planning a pregnancy, does this affect my risk of pregnancy complications or postpartum thyroiditis? If I'm being monitored for thyroid cancer, does a positive TgAb mean my thyroglobulin results can't be trusted, and what alternative monitoring is being used instead?",
        "next_steps": "A positive antibody result with normal thyroid function usually leads to periodic TSH monitoring (since autoimmune thyroid antibodies predict a higher future risk of developing over dysfunction), rather than immediate treatment. If thyroid function is already abnormal, treatment follows standard management for hypothyroidism (Hashimoto's) or hyperthyroidism (Graves'). In pregnancy or preconception, a positive TPOAb may prompt closer monitoring given the association with pregnancy complications and postpartum thyroiditis.",
        "associated_conditions": [
            {"condition": "Hashimoto's thyroiditis (autoimmune hypothyroidism)", "direction": "positive TPOAb and/or TgAb"},
            {"condition": "Graves' disease (autoimmune hyperthyroidism)", "direction": "positive TPOAb, positive TRAb (a separate, stimulating antibody) is more specific"},
            {"condition": "Postpartum thyroiditis risk", "direction": "positive TPOAb predicts higher risk"},
            {"condition": "Invalidated thyroglobulin tumor marker (post-thyroidectomy)", "direction": "positive TgAb interferes with the Tg assay"}
        ],
        "sources": [{"name": "Medscape/eMedicine - Antithyroid Antibody: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2086819-overview", "accessed": "2026-07-14"}]
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
             critical_values_en, interfering_factors_en, questions_to_ask_en, next_steps_en,
             associated_conditions_json, related_tests_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             t.get("critical_values_en"), t.get("interfering_factors_en"),
             t.get("questions_to_ask_en"), t.get("next_steps"),
             json.dumps(t.get("associated_conditions", [])),
             json.dumps(["tsh", "free-t4", "free-t3"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
