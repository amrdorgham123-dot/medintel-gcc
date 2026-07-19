"""
Seed script (batch 29) for MedForsa GCC's Lab Info reference library.
Adds the Antiphospholipid Antibody Panel (Lupus Anticoagulant, Anticardiolipin
Antibodies, Anti-Beta2-Glycoprotein I Antibodies).

Run once: python3 seed_lab_tests_batch29.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "antiphospholipid-panel", "name_en": "Antiphospholipid Antibody Panel (Lupus Anticoagulant, Anticardiolipin, Anti-\u03b22-Glycoprotein I)",
        "aliases": "APS Panel, Lupus Anticoagulant, Anticardiolipin Antibodies, Anti-B2GPI, aPL Panel",
        "category": "Hematology / Coagulation",
        "purpose_en": "Diagnoses antiphospholipid syndrome (APS), evaluated in patients with unprovoked venous or arterial thrombosis, recurrent pregnancy loss or other specific pregnancy morbidity, or an unexplained prolonged aPTT, particularly in the context of SLE or other autoimmune disease.",
        "specimen_type": "Venous whole blood, sodium citrate tube (for lupus anticoagulant) plus serum (for anticardiolipin and anti-\u03b22GPI antibodies)",
        "collection_notes_en": "Testing should ideally be done while off anticoagulation when possible, since anticoagulants can interfere with lupus anticoagulant testing; any positive result must be confirmed on a repeat sample at least 12 weeks later before a diagnosis of APS is made, since transient positivity (e.g., from acute infection) is common and not diagnostic.",
        "methodology_en": "Lupus anticoagulant is detected via phospholipid-dependent clotting assays (commonly dilute Russell viper venom time [dRVVT] and a sensitive aPTT), which show prolonged clotting that doesn't correct with a mixing study but does correct with excess phospholipid. Anticardiolipin and anti-\u03b22-glycoprotein I antibodies (IgG, IgM, and sometimes IgA) are measured by enzyme-linked immunosorbent assay (ELISA).",
        "reference_ranges": [
            {"parameter": "Lupus anticoagulant", "population": "Result categories", "range": "Negative or Positive -- based on a prolonged phospholipid-dependent clotting time (e.g., aPTT \u226546 sec or dRVVT \u226540 sec on some assay platforms) that fails to correct with mixing but corrects with excess phospholipid"},
            {"parameter": "Anticardiolipin antibody (aCL)", "population": "Negative", "range": "IgG <19.3 U/mL, IgM <15.7 U/mL, IgA <8.2 U/mL (assay-dependent cutoffs)"},
            {"parameter": "Anti-\u03b22-glycoprotein I antibody", "population": "Negative", "range": "IgG, IgM, and IgA each <20 U/mL (assay-dependent cutoffs)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Per the revised (Sapporo) classification criteria, a diagnosis of antiphospholipid syndrome requires at least one clinical criterion (vascular thrombosis or specific pregnancy morbidity) plus at least one of these three laboratory criteria (lupus anticoagulant, anticardiolipin IgG/IgM at medium-high titer, or anti-\u03b22-glycoprotein I IgG/IgM), confirmed on two occasions at least 12 weeks apart. All three tests carry equal diagnostic weight, but lupus anticoagulant has been shown in multiple studies to correlate most strongly with thrombosis risk, and \u03b22-glycoprotein I-dependent lupus anticoagulant in particular is a strong predictor. Triple positivity (all three tests positive) carries the highest risk of thrombosis and pregnancy complications. A single positive result without confirmatory repeat testing, or a low-titer result, is not sufficient for diagnosis given the risk of transient positivity from unrelated causes (infection, certain medications).",
        "associated_conditions": [
            {"condition": "Antiphospholipid syndrome (primary or secondary to SLE)", "direction": "positive on \u22651 criterion, confirmed 12+ weeks apart"},
            {"condition": "Recurrent pregnancy loss / pre-eclampsia / placental insufficiency", "direction": "positive, associated with obstetric morbidity"},
            {"condition": "Unprovoked venous or arterial thrombosis", "direction": "positive, especially with triple positivity"}
        ],
        "questions_to_ask_en": "Which of the three tests came back positive, and does that affect my risk level? Does this need to be repeated before a diagnosis is confirmed? If confirmed, do I need long-term blood thinners, and does this change how any future pregnancy would be managed?",
        "next_steps": "Any positive result requires confirmatory repeat testing at least 12 weeks later before antiphospholipid syndrome can be diagnosed. A confirmed diagnosis typically leads to hematology or rheumatology-guided long-term anticoagulation planning (for those with a prior thrombosis) and, for women of childbearing age, a specific management plan for future pregnancies given the associated risks.",
        "sources": [
            {"name": "Mayo Clinic Laboratories - Beta-2 Glycoprotein 1 Antibodies, IgG and IgM, Serum (test catalog, 2023 ACR/EULAR criteria)", "url": "https://www.mayocliniclabs.com/test-catalog/overview/62926", "accessed": "2026-07-19"},
            {"name": "PMC - IgA Anti-\u03b22-Glycoprotein I Autoantibodies Are Associated with an Increased Risk of Thromboembolic Events in SLE (assay cutoffs)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2924386/", "accessed": "2026-07-19"},
            {"name": "Blood (American Society of Hematology) - \u03b22-glycoprotein I-dependent lupus anticoagulant highly correlates with thrombosis in the antiphospholipid syndrome", "url": "https://ashpublications.org/blood/article/104/12/3598/89073/2-glycoprotein-I-dependent-lupus-anticoagulant", "accessed": "2026-07-19"}
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
             json.dumps(["pt-inr", "aptt", "ana", "anti-dsdna", "factor-v-leiden"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
