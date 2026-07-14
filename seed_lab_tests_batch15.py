"""
Seed script (batch 15) for MedForsa GCC's Lab Info reference library.
Adds Fecal Immunochemical Test (FIT/FOBT) for colorectal cancer screening.

Run once: python3 seed_lab_tests_batch15.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "fit-fobt", "name_en": "Fecal Immunochemical Test (FIT / FOBT)",
        "aliases": "FIT, FOBT, Fecal Occult Blood Test, Stool Occult Blood",
        "category": "Clinical Chemistry / Point of Care",
        "purpose_en": "Screens for colorectal cancer and precancerous polyps by detecting hidden (occult) blood in stool; the modern fecal immunochemical test (FIT) has largely replaced the older guaiac-based test (gFOBT) as the standard non-invasive stool screening option, alongside colonoscopy and multitarget stool DNA testing.",
        "specimen_type": "Stool sample, collected by the patient at home using the kit provided",
        "collection_notes_en": "FIT (immunochemical) testing requires no dietary or medication restrictions, unlike the older guaiac-based test, since it uses antibodies specific to human hemoglobin and is not affected by dietary blood, vitamin C, or red meat. Only a single stool sample is typically required for FIT-based colorectal cancer screening (versus multiple samples historically needed for guaiac testing).",
        "methodology_en": "Immunochromatographic or automated immunoturbidimetric assay using antibodies specific to human hemoglobin, distinguishing it from the older guaiac (chemical peroxidase) method that could react with non-human or upper-GI-degraded blood and dietary substances.",
        "reference_ranges": [{"parameter": "FIT result", "population": "Result categories", "range": "Negative (below the assay's positivity cutoff, commonly around 100 ng/mL hemoglobin) or Positive"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive FIT result requires follow-up colonoscopy to evaluate for colorectal cancer or advanced polyps, and should not be repeated as a way to 'confirm' the result -- any positive FIT warrants colonoscopy regardless of a subsequent negative repeat test. FIT specificity is routinely above 95%, but sensitivity for cancer detection varies by population (roughly 40-70% per average-risk screening data, higher in some study populations), meaning a negative FIT reduces but does not eliminate colorectal cancer risk, which is why average-risk guidelines recommend annual FIT testing (versus a longer interval for colonoscopy) if FIT is the chosen screening method. A positive result can also reflect other sources of GI bleeding (hemorrhoids, diverticulosis, peptic ulcer, inflammatory bowel disease) rather than cancer.",
        "associated_conditions": [
            {"condition": "Colorectal cancer / advanced adenomatous polyps", "direction": "positive"},
            {"condition": "Other GI bleeding sources (hemorrhoids, diverticulosis, peptic ulcer, IBD)", "direction": "positive, non-malignant cause"}
        ],
        "critical_values_en": None,
        "interfering_factors_en": "Unlike the older guaiac-based test, FIT is not affected by diet (red meat), vitamin C, or most medications, since it specifically detects human hemoglobin via antibodies -- this is a key advantage that eliminated the need for pre-test dietary restriction. Active menstrual bleeding or bleeding hemorrhoids contaminating the sample can cause a false-positive result unrelated to colorectal pathology.",
        "questions_to_ask_en": "Since my result is positive, when should I schedule my follow-up colonoscopy? Does a positive result mean I definitely have cancer, or could it be from something else? If negative, when should I repeat this screening test, and is that the right screening strategy for my risk level, or should I consider colonoscopy instead? Do I have any risk factors (family history, symptoms) that should change my screening plan?",
        "next_steps": "A positive result should prompt scheduling of a diagnostic colonoscopy -- this is the standard next step regardless of symptoms, and should not be delayed or substituted with a repeat FIT. A negative result in an average-risk person means continuing with annual FIT screening (or the screening interval recommended by your clinician) as part of ongoing colorectal cancer prevention, alongside attention to any new symptoms (rectal bleeding, unexplained weight loss, change in bowel habits) that would warrant earlier evaluation regardless of the FIT result.",
        "sources": [
            {"name": "Mayo Clinic Laboratories - Fecal Occult Blood, Colorectal Cancer Screen, Qualitative, Immunochemical, Feces (test catalog)", "url": "https://gi.testcatalog.org/show/FOBT", "accessed": "2026-07-14"},
            {"name": "StatPearls / NCBI Bookshelf - Fecal Occult Blood Test", "url": "https://www.ncbi.nlm.nih.gov/books/NBK537138/", "accessed": "2026-07-14"}
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
             json.dumps(["cea", "cbc", "ferritin"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
