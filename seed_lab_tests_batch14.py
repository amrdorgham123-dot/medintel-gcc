"""
Seed script (batch 14) for MedForsa GCC's Lab Info reference library.
Adds Hemoglobin Electrophoresis (hemoglobinopathy/thalassemia screening).

Run once: python3 seed_lab_tests_batch14.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "hemoglobin-electrophoresis", "name_en": "Hemoglobin Electrophoresis (Hemoglobinopathy Evaluation)",
        "aliases": "Hb Electrophoresis, HPLC Hemoglobin Analysis, Thalassemia Screen, Sickle Cell Screen",
        "category": "Hematology",
        "purpose_en": "Identifies and quantifies normal and abnormal hemoglobin types to diagnose hemoglobinopathies (sickle cell trait/disease, hemoglobin C/E/D and other variants) and thalassemias; used for newborn screening, premarital/carrier screening, prenatal screening, and workup of unexplained microcytic anemia not responding to iron therapy.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top); heel-stick for newborn screening",
        "collection_notes_en": "No fasting required. Recent blood transfusion can mask or dilute the patient's own hemoglobin pattern with donor hemoglobin -- testing should ideally be deferred at least 3 months after transfusion when possible, or the transfusion history noted for interpretation.",
        "methodology_en": "Cation-exchange high-performance liquid chromatography (HPLC) and/or capillary electrophoresis are the current standard methods (having largely superseded older cellulose acetate gel electrophoresis), separating hemoglobin fractions by charge/size and quantifying each as a percentage of total hemoglobin.",
        "reference_ranges": [
            {"parameter": "Hemoglobin A (HbA)", "population": "Adult", "range": "95-98%"},
            {"parameter": "Hemoglobin A2 (HbA2)", "population": "Adult", "range": "2-3%", "notes": "Some labs cite up to 3.5% as the upper limit"},
            {"parameter": "Hemoglobin F (HbF)", "population": "Adult (age >3 years)", "range": "<1-2%", "notes": "Levels above ~2% in individuals older than 3 are considered elevated"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated HbA2 (commonly >3.5%) with a microcytic blood picture supports beta-thalassemia trait; in HbS/beta-thalassemia, HbA2 can be even higher (median around 6.5% in some series). Presence of HbS with roughly 60% HbA and 40% HbS indicates sickle cell trait (usually asymptomatic carrier status); absence of HbA with predominant HbS (often 80-95%) indicates sickle cell disease (HbSS). HbSC disease shows roughly equal HbS and HbC. Elevated HbF can be seen in beta-thalassemia major, hereditary persistence of fetal hemoglobin, and in sickle cell patients on hydroxyurea therapy (where higher HbF is therapeutically beneficial, reducing sickling). Results should always be interpreted alongside the CBC (particularly MCV/MCH) and iron studies, since thalassemia trait can be confused with iron deficiency on red cell indices alone.",
        "critical_values_en": None,
        "interfering_factors_en": "Recent blood transfusion introduces donor hemoglobin that can mask or dilute the patient's true hemoglobin pattern -- testing should note transfusion history and ideally be deferred when a non-transfused sample is needed. Concurrent iron deficiency can lower HbA2 percentage in beta-thalassemia trait carriers, sometimes masking the diagnosis until iron status is corrected and the test repeated.",
        "questions_to_ask_en": "What specific hemoglobin variant or pattern was found, and what does it mean for my health? Am I a carrier (trait) or do I have the disease form of this condition? Do my partner and I need testing together if we're planning a pregnancy, given the risk to offspring? Do I need genetic counseling, and should other family members be screened? If I have sickle cell trait, are there any activity or environmental precautions I should know about?",
        "next_steps": "A carrier (trait) result in someone planning a family typically prompts partner testing, since two carriers of a compatible trait have a chance of having a child with the more severe disease form, and genetic counseling is recommended in that situation. A disease-level result (e.g., sickle cell disease, thalassemia major) leads to referral to hematology for ongoing specialized management. Trait results in an otherwise healthy person usually require no treatment, only awareness for family planning and, for sickle cell trait, certain precautions in extreme physical exertion or high-altitude/low-oxygen situations.",
        "associated_conditions": [
            {"condition": "Sickle cell trait (HbAS)", "direction": "~60% HbA, ~40% HbS"},
            {"condition": "Sickle cell disease (HbSS)", "direction": "predominant HbS, little/no HbA"},
            {"condition": "Beta-thalassemia trait (minor)", "direction": "elevated HbA2 (>3.5%), microcytosis"},
            {"condition": "Beta-thalassemia major", "direction": "predominant HbF, minimal/no HbA"},
            {"condition": "Hemoglobin C or E disease/trait", "direction": "presence of HbC or HbE variant"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Hemoglobin Electrophoresis: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2085637-overview", "accessed": "2026-07-14"},
            {"name": "Hematology.org (ASH) - Hemoglobin Electrophoresis in Sickle Cell Disease: A Primer for the Clinician", "url": "https://www.hematology.org/education/trainees/fellows/hematopoiesis/2021/hemoglobin-electrophoresis-in-sickle-cell-disease", "accessed": "2026-07-14"}
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
             json.dumps(["cbc", "ferritin", "serum-iron", "reticulocyte-count"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
