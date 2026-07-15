"""
Seed script (batch 19) for MedForsa GCC's Lab Info reference library.
Adds von Willebrand Factor (Antigen + Ristocetin Cofactor Activity).

Run once: python3 seed_lab_tests_batch19.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "von-willebrand-factor", "name_en": "von Willebrand Factor (Antigen + Ristocetin Cofactor Activity)",
        "aliases": "vWF, vWF:Ag, vWF:RCo, Von Willebrand Panel",
        "category": "Hematology / Coagulation",
        "purpose_en": "Diagnoses and classifies von Willebrand disease (vWD), the most common inherited bleeding disorder, and differentiates it from hemophilia A; used to investigate mucocutaneous bleeding symptoms (easy bruising, heavy menstrual bleeding, prolonged bleeding after dental work or surgery).",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "Avoid warfarin for 2 weeks and heparin for 2 days before testing when possible, and do not draw from an arm with a heparin lock. Sample should reach the lab within about 3 hours of collection at room temperature (or be double-centrifuged and frozen promptly per the specific lab's protocol) for accurate results.",
        "methodology_en": "vWF antigen (vWF:Ag) is measured by immunoturbidimetric or ELISA methods (protein mass, regardless of function); vWF ristocetin cofactor activity (vWF:RCo) is a functional platelet agglutination assay measuring how well vWF supports platelet binding; newer collagen-binding (vWF:CB) assays are increasingly used as well. Factor VIII activity is typically measured alongside, since vWF stabilizes circulating factor VIII.",
        "reference_ranges": [
            {"parameter": "vWF Antigen (vWF:Ag)", "population": "Adult, non-O blood group", "range": "~50-150%", "notes": "Blood group O individuals normally run lower (as low as 40-50%), which must be considered before diagnosing a deficiency"},
            {"parameter": "vWF Ristocetin Cofactor Activity (vWF:RCo)", "population": "Adult", "range": "~50-150%", "notes": "A level <30% is considered diagnostic of vWD; 30-50% is a gray zone requiring correlation with bleeding history"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low vWF:Ag and vWF:RCo together (with a normal RCo:Ag ratio) suggest type 1 vWD (a partial quantitative deficiency, the most common form). A disproportionately low vWF:RCo relative to vWF:Ag (RCo:Ag ratio below about 0.7) suggests type 2 vWD (a qualitative/functional defect). Very low or undetectable levels of both suggest type 3 vWD (severe, near-complete deficiency). Because vWF is an acute-phase reactant, levels rise with pregnancy, estrogen therapy, inflammation, acute infection, surgery, and stress -- which can transiently normalize results in a person with mild congenital vWD, sometimes requiring repeat testing outside of these conditions. Blood group O individuals have physiologically lower vWF levels (roughly 25-30% lower) than other blood groups, which must be factored in before diagnosing deficiency.",
        "critical_values_en": None,
        "interfering_factors_en": "ABO blood group significantly affects baseline vWF levels (lower in group O), acute-phase reactant physiology means results rise with pregnancy, stress, inflammation, infection, surgery, and exercise (potentially masking a mild underlying deficiency), and recent warfarin or heparin use can affect related coagulation testing -- all must be considered when interpreting a result, and repeat testing away from these confounders is often needed before a definitive diagnosis.",
        "questions_to_ask_en": "Which subtype of von Willebrand disease do I have, and how does that affect my treatment options (e.g., desmopressin/DDAVP responsiveness versus need for factor concentrate)? Does my blood group affect how this result should be interpreted? Do I need repeat testing at a different time, given that results can be affected by stress, illness, or hormonal factors? What precautions should I take before surgery, dental work, or childbirth?",
        "next_steps": "A borderline or mildly low result is often repeated at a separate visit, ideally when not acutely ill, stressed, pregnant, or on estrogen therapy, since these can transiently raise levels and mask a mild deficiency. A confirmed diagnosis leads to classification of the vWD subtype (which guides whether desmopressin/DDAVP or vWF/factor VIII concentrate is the appropriate treatment for bleeding episodes or procedures) and referral to hematology for a comprehensive bleeding disorder management plan, including precautions for future surgery, dental procedures, and childbirth.",
        "associated_conditions": [
            {"condition": "Von Willebrand disease, type 1 (partial quantitative deficiency)", "direction": "low vWF:Ag and vWF:RCo, proportionate (RCo:Ag ratio >0.7)"},
            {"condition": "Von Willebrand disease, type 2 (qualitative/functional defect)", "direction": "disproportionately low vWF:RCo relative to vWF:Ag (ratio <0.7)"},
            {"condition": "Von Willebrand disease, type 3 (severe deficiency)", "direction": "very low/undetectable vWF:Ag and vWF:RCo"},
            {"condition": "Acquired von Willebrand syndrome (e.g., lymphoproliferative disease, aortic stenosis)", "direction": "low, in a patient without a prior personal/family bleeding history"}
        ],
        "sources": [
            {"name": "Mayo Clinic Laboratories - von Willebrand Factor Antigen, Plasma (test catalog)", "url": "https://hematology.testcatalog.org/show/VWAG", "accessed": "2026-07-14"},
            {"name": "Medscape/eMedicine - Ristocetin Cofactor (Functional von Willebrand Factor): Reference Range, Interpretation", "url": "https://emedicine.medscape.com/article/2086190-overview", "accessed": "2026-07-14"},
            {"name": "Labcorp - von Willebrand Factor (vWF) Antigen test description", "url": "https://www.labcorp.com/tests/086280/von-willebrand-factor-vwf-antigen", "accessed": "2026-07-14"}
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
             json.dumps(["pt-inr", "aptt", "fibrinogen", "abo-rh-typing"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
