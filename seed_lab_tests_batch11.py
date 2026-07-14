"""
Seed script (batch 11) for MedForsa GCC's Lab Info reference library.
Adds Insulin, C-Peptide, and Serum Osmolality -- with the full section structure
including critical_values, interfering_factors, questions_to_ask, and next_steps.

Run once: python3 seed_lab_tests_batch11.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "insulin", "name_en": "Insulin, Serum",
        "aliases": "Fasting Insulin, Serum Insulin",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Investigates the cause of hypoglycemia (its primary use), evaluates insulin resistance, and helps guide treatment decisions in type 2 diabetes; also used to monitor pancreatic islet cell transplant function.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Typically drawn fasting (8-12 hours); stop biotin (vitamin B7) supplements for at least a day before testing, as biotin can interfere with many immunoassay platforms. Usually collected together with a simultaneous glucose level for meaningful interpretation.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "Fasting insulin", "population": "Adult", "range": "~2-25 \u00b5U/mL (\u00b5IU/mL)", "notes": "Reference ranges vary considerably between labs/assays; some clinicians and researchers consider levels well below the upper limit (e.g., under ~10 \u00b5U/mL) more consistent with good insulin sensitivity, though this is not a formal diagnostic cutoff"}],
        "reference_ranges_verified": True,
        "interfering_factors_en": "Biotin (vitamin B7) supplementation can cause significant interference (falsely low or falsely high results depending on the assay design) on many immunoassay platforms -- patients should stop biotin at least 24-48 hours before testing per the specific assay's recommendation. Recent food intake invalidates a 'fasting' interpretation.",
        "questions_to_ask_en": "Was my glucose measured at the same time, and how do the two results relate to each other? Could my result reflect insulin resistance, and if so, what does that mean for my future diabetes risk? Do I need additional testing (e.g., HOMA-IR calculation, C-peptide) to clarify the picture? Is there anything in my diet, medications, or recent activity that could have affected this result?",
        "next_steps": "Insulin results are always interpreted alongside a simultaneous glucose level, since the two must be considered together (e.g., high insulin with normal-to-high glucose suggests insulin resistance; high insulin with low glucose suggests inappropriate insulin excess). Depending on the pattern, your clinician may discuss lifestyle changes, calculate a HOMA-IR insulin resistance index, or investigate further with a C-peptide test or extended fasting study if hypoglycemia is a concern.",
        "clinical_significance_en": "High insulin with normal or elevated glucose suggests insulin resistance, a precursor to type 2 diabetes and a feature of metabolic syndrome and PCOS. High or inappropriately normal insulin with low glucose suggests excess insulin action -- causes include insulinoma, exogenous insulin administration (including surreptitious use), sulfonylurea use, or Cushing syndrome. Low insulin with high glucose suggests inadequate insulin production, as in type 1 diabetes or pancreatitis-related beta-cell loss.",
        "associated_conditions": [
            {"condition": "Insulin resistance / metabolic syndrome / PCOS", "direction": "high, with normal-high glucose"},
            {"condition": "Insulinoma / exogenous insulin administration", "direction": "high or inappropriately normal, with low glucose"},
            {"condition": "Type 1 diabetes / beta-cell failure", "direction": "low, with high glucose"}
        ],
        "sources": [{"name": "MedlinePlus (NIH/NLM) - Insulin in Blood, citing Mayo Clinic Laboratories Test ID: INS", "url": "https://medlineplus.gov/lab-tests/insulin-in-blood/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "c-peptide", "name_en": "C-Peptide, Serum",
        "aliases": "C-Peptide, Connecting Peptide",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Marker of the body's own (endogenous) insulin production -- used to distinguish type 1 from type 2 diabetes, investigate hypoglycemia (including suspected surreptitious insulin use, since injected insulin doesn't raise C-peptide), and monitor islet/pancreas transplant function.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Usually drawn fasting alongside a simultaneous glucose level; stop biotin supplements for at least 12 hours before testing per most assay manufacturer recommendations, as biotin can interfere with the assay.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "Fasting C-peptide", "population": "Adult", "range": "~0.3-3.3 ng/mL (or ~0.2-1.0 nmol/L)", "notes": "Reference ranges vary by lab/assay; result should always be interpreted alongside a simultaneous glucose"}],
        "reference_ranges_verified": True,
        "interfering_factors_en": "Even mild hemolysis can artifactually lower C-peptide values. Biotin supplementation can interfere with the assay. Very high C-peptide levels (rare, typically only in specific research/pathological contexts) can cause a falsely low result due to a 'hook effect' on some immunoassay platforms.",
        "questions_to_ask_en": "Was my glucose checked at the same time, and how should the two results be interpreted together? Does this result help clarify whether I have type 1 or type 2 diabetes? If I'm on insulin therapy, does this tell us anything about how much of my own insulin production remains? Do I need islet cell antibody testing alongside this to further clarify the diabetes type?",
        "next_steps": "C-peptide results are interpreted together with the simultaneous glucose level and, often, diabetes-related autoantibody testing. A low C-peptide with high glucose supports a type 1 diabetes diagnosis (little remaining endogenous insulin production); a normal-to-high C-peptide in a person with diabetes and insulin resistance supports type 2 diabetes. In suspected factitious hypoglycemia, a low C-peptide despite a high measured insulin level points to exogenous (injected) insulin as the cause.",
        "clinical_significance_en": "Low C-peptide indicates little remaining endogenous insulin production, as seen in longstanding type 1 diabetes, advanced type 2 diabetes with beta-cell exhaustion, or after pancreatectomy. Normal-to-high C-peptide with hyperglycemia is typical of insulin-resistant type 2 diabetes, where the pancreas is still producing (often excess) insulin but the body isn't responding effectively. Because C-peptide is co-secreted with the person's own insulin but is not present in most injected insulin formulations, a discordantly low C-peptide with a high insulin level in a hypoglycemic patient suggests exogenous insulin administration rather than an insulin-producing tumor.",
        "associated_conditions": [
            {"condition": "Type 1 diabetes / advanced beta-cell failure", "direction": "low"},
            {"condition": "Type 2 diabetes / insulin resistance", "direction": "normal to high, with hyperglycemia"},
            {"condition": "Exogenous (injected) insulin as cause of hypoglycemia", "direction": "low C-peptide despite high measured insulin"},
            {"condition": "Insulinoma", "direction": "inappropriately high relative to a low glucose"}
        ],
        "sources": [
            {"name": "UCSF Health - Insulin C-peptide test", "url": "https://www.ucsfhealth.org/care/medical-tests/insulin-c-peptide-test", "accessed": "2026-07-14"},
            {"name": "Medscape/eMedicine - C-Peptide: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2087824-overview", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "osmolality", "name_en": "Osmolality, Serum",
        "aliases": "Serum Osmolality, Plasma Osmolality",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses the body's fluid/water balance and screens for toxic alcohol ingestion (via the osmolal gap); used to evaluate hyponatremia/hypernatremia, suspected diabetes insipidus, and unexplained altered mental status.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required; can be drawn at any time. Often ordered alongside sodium, glucose, and BUN so a calculated osmolality (and the osmolal gap versus the measured value) can be determined.",
        "methodology_en": "Directly measured by freezing point depression osmometry (captures all osmotically active particles); calculated osmolality is derived mathematically from sodium, glucose, and BUN (Posm = 2[Na] + glucose/18 + BUN/2.8) and is not a true independent measurement.",
        "reference_ranges": [{"parameter": "Serum osmolality", "population": "Adult", "range": "275-295 mOsm/kg H2O"}],
        "reference_ranges_verified": True,
        "critical_values_en": "Serum osmolality above roughly 420 mOsm/kg can be lethal regardless of underlying cause and represents a medical emergency; in critically ill patients, values above 300 mOsm/kg are independently associated with higher risk of acute kidney injury and mortality.",
        "interfering_factors_en": "A discrepancy of more than ~10 mOsm/kg between measured and calculated osmolality (the 'osmolal gap') suggests the presence of unmeasured osmotically active substances -- classically toxic alcohols (methanol, ethylene glycol), mannitol, or ethanol -- and should prompt urgent toxicologic evaluation when clinically suspected.",
        "questions_to_ask_en": "Is my osmolality result consistent with my sodium level, or is there a gap that needs further investigation? Could dehydration, a medication, or an ingestion explain this result? Do I need urine osmolality testing as well to fully evaluate my fluid balance? What is the underlying cause, and how will it be treated?",
        "next_steps": "Depending on the result and clinical context, your clinician may compare the measured value with a calculated osmolality to check for an osmolal gap (which raises concern for toxic alcohol ingestion or other unmeasured substances), order a urine osmolality to help distinguish causes of abnormal sodium/water balance, or investigate for underlying causes such as SIADH, diabetes insipidus, or dehydration.",
        "clinical_significance_en": "Low osmolality most often reflects hyponatremia (since sodium accounts for the majority of the osmolality value) and can be caused by SIADH, heart failure, cirrhosis, or excessive water intake. High osmolality reflects free water loss or a solute gain, seen in dehydration, hyperglycemia, or diabetes insipidus (in which urine remains inappropriately dilute despite high plasma osmolality). An elevated osmolal gap (measured minus calculated osmolality) is a key screening clue for toxic alcohol ingestion even before specific levels are available.",
        "associated_conditions": [
            {"condition": "SIADH / hyponatremia", "direction": "low"},
            {"condition": "Dehydration / diabetes insipidus / hyperglycemia", "direction": "high"},
            {"condition": "Toxic alcohol ingestion (methanol, ethylene glycol)", "direction": "elevated osmolal gap"}
        ],
        "sources": [
            {"name": "StatPearls / NCBI Bookshelf - Serum Osmolality", "url": "https://www.ncbi.nlm.nih.gov/books/NBK567764/", "accessed": "2026-07-14"},
            {"name": "Medscape/eMedicine - Serum Osmolality: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2099042-overview", "accessed": "2026-07-14"}
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
             associated_conditions_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             t.get("critical_values_en"), t.get("interfering_factors_en"),
             t.get("questions_to_ask_en"), t.get("next_steps"),
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
