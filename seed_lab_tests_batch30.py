"""
Seed script (batch 30) for MedForsa GCC's Lab Info reference library.
Adds GAD65 Antibody (glutamic acid decarboxylase autoantibody).

Run once: python3 seed_lab_tests_batch30.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "gad65-antibody", "name_en": "Glutamic Acid Decarboxylase (GAD65) Antibody",
        "aliases": "GAD65, GAD Antibody, Anti-GAD",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Most sensitive of the islet autoantibodies for confirming autoimmune (type 1) diabetes and distinguishing it from type 2 diabetes, including in adults with new-onset diabetes where the type is unclear (latent autoimmune diabetes of adulthood, LADA); also the recommended first-line test for suspected stiff-person syndrome and related autoimmune neurologic disorders.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Often ordered alongside other islet autoantibodies (insulin autoantibody, IA-2 antibody, ZnT8 antibody) for a complete assessment of beta-cell autoimmunity, since no single antibody has complete sensitivity.",
        "methodology_en": "Radioimmunoassay (RIA) or enzyme-linked immunosorbent assay (ELISA) detecting IgG antibodies against the 65-kDa isoform of glutamic acid decarboxylase.",
        "reference_ranges": [
            {"parameter": "GAD65 antibody", "population": "Normal (type 1 diabetes unlikely)", "range": "\u22640.02 nmol/L"},
            {"parameter": "GAD65 antibody", "population": "Positive, low titer (consistent with type 1 diabetes susceptibility)", "range": "0.03-19.9 nmol/L"},
            {"parameter": "GAD65 antibody", "population": "High titer (seen in stiff-person syndrome)", "range": "\u226520.0 nmol/L"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "GAD65 antibodies are present in approximately 80% of type 1 diabetes patients at clinical presentation, the highest individual sensitivity among the islet autoantibodies (compared to roughly 54-75% for IA-2 antibody and lower for insulin autoantibody), and in less than 5% of type 2 diabetes patients, making it useful for distinguishing autoimmune from non-autoimmune diabetes, particularly in adults with an ambiguous presentation (LADA). Testing multiple islet autoantibodies together substantially increases sensitivity (up to ~96%) and helps predict future progression to type 1 diabetes in at-risk relatives -- the five-year risk of developing diabetes rises from about 17% with one positive antibody to about 70% with three. GAD65 antibodies also mark susceptibility to other autoimmune endocrine conditions that cluster with type 1 diabetes (autoimmune thyroid disease, pernicious anemia, Addison disease, premature ovarian failure), and at high titer (\u226520 nmol/L) are strongly associated with stiff-person syndrome and related autoimmune neurologic disorders, a distinct clinical use for this same antibody.",
        "associated_conditions": [
            {"condition": "Type 1 diabetes mellitus / LADA", "direction": "positive, low-moderate titer"},
            {"condition": "Autoimmune polyendocrine susceptibility (thyroid disease, pernicious anemia, Addison disease)", "direction": "positive, marker of associated risk"},
            {"condition": "Stiff-person syndrome / related autoimmune neurologic disorders", "direction": "high titer, \u226520 nmol/L"}
        ],
        "questions_to_ask_en": "Does this result mean I have type 1 diabetes rather than type 2? Do I need additional islet autoantibody testing (IA-2, insulin, ZnT8) for a complete picture? If I'm a relative of someone with type 1 diabetes, what does a positive result mean for my own future risk?",
        "next_steps": "A positive result in someone with new-onset diabetes supports a type 1 (or LADA) diagnosis and typically changes management toward insulin therapy sooner rather than oral diabetes medications alone. In an at-risk relative without diabetes, a positive result (especially with multiple positive antibodies) prompts closer monitoring for progression, since risk rises substantially with each additional positive antibody.",
        "sources": [
            {"name": "Mayo Clinic Laboratories - Glutamic Acid Decarboxylase (GAD65) Antibody Assay, Serum (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/overview/81596", "accessed": "2026-07-19"},
            {"name": "ClinLab Navigator - Islet Cell Antibodies (combined sensitivity data)", "url": "https://www.clinlabnavigator.com/test-interpretations/test-interpretations-1/islet-cell-antibodies.html", "accessed": "2026-07-19"},
            {"name": "Johns Hopkins Diabetes Guide - Autoantibodies in Type 1 Diabetes", "url": "https://www.hopkinsguides.com/hopkins/view/Johns_Hopkins_Diabetes_Guide/547013/all/Autoantibodies_in_Type_1_Diabetes", "accessed": "2026-07-19"}
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
             json.dumps(["fasting-glucose", "hba1c", "c-peptide", "insulin", "anti-tpo"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
