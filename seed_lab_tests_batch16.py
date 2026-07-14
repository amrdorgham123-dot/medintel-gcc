"""
Seed script (batch 16) for MedForsa GCC's Lab Info reference library.
Adds Zinc and Ceruloplasmin (trace element / copper metabolism markers).

Run once: python3 seed_lab_tests_batch16.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "zinc", "name_en": "Zinc, Serum",
        "aliases": "Serum Zinc",
        "category": "Clinical Chemistry",
        "purpose_en": "Evaluates suspected zinc deficiency, most often in the context of malabsorption, prolonged parenteral nutrition, burns, chronic liver/kidney disease, or characteristic clinical findings (poor wound healing, dermatitis, hair loss, taste/smell disturbance, impaired immunity).",
        "specimen_type": "Venous serum or plasma, collected in a zinc-free (trace-element) tube using a stainless steel needle",
        "collection_notes_en": "Requires specialized zinc-free collection tubes and avoidance of rubber stopper contact; ideally a fasting morning sample, separated from cells within about 45 minutes to prevent contamination or redistribution artifacts.",
        "methodology_en": "Atomic absorption spectrophotometry or inductively coupled plasma mass spectrometry (ICP-MS).",
        "reference_ranges": [{"parameter": "Serum zinc", "population": "Adult", "range": "~66-106 \u00b5g/dL", "notes": "Reference ranges vary meaningfully between labs/sources (some cite 60-130 \u00b5g/dL); always confirm against the reporting lab's own range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Zinc deficiency causes impaired wound healing, dermatitis (classically acrodermatitis enteropathica in severe/congenital deficiency), hair loss, diarrhea, taste and smell disturbance, growth impairment in children, and impaired immune function. Common causes include malabsorption (e.g., Crohn's disease, short bowel syndrome), inadequate zinc in parenteral nutrition, chronic liver disease, chronic kidney disease with dialysis, burns (zinc lost through wound exudate), and excess dietary copper or iron (which competes with zinc absorption). Elevated zinc is of minimal independent clinical significance and is uncommon outside of supplementation or occupational/environmental exposure.",
        "interfering_factors_en": "Hemolysis causes false elevation, since red blood cells contain much higher zinc concentrations than plasma. Contact with rubber stoppers or non-trace-element collection tubes can contaminate the sample and falsely raise results. Zinc is also a negative acute-phase reactant, so acute illness/inflammation can transiently lower levels independent of true zinc status, similar to albumin.",
        "questions_to_ask_en": "Could my low zinc level explain some of my symptoms (e.g., poor wound healing, taste changes, hair loss)? Do I need supplementation, and if so, for how long and at what dose? Is there an underlying cause (malabsorption, diet, chronic illness) that also needs to be addressed? Should copper be checked too, since zinc supplementation can affect copper status?",
        "next_steps": "Confirmed deficiency is typically managed with oral zinc supplementation, with the underlying cause (dietary, malabsorptive, or disease-related) investigated and addressed where possible. Because high-dose or prolonged zinc supplementation can cause copper deficiency, copper status is sometimes monitored alongside zinc during treatment, and a repeat zinc level may be checked after a period of supplementation to confirm improvement.",
        "associated_conditions": [
            {"condition": "Malabsorption (e.g., Crohn's disease, short bowel syndrome)", "direction": "low"},
            {"condition": "Chronic liver or kidney disease", "direction": "low"},
            {"condition": "Acrodermatitis enteropathica (congenital zinc transport defect)", "direction": "very low"},
            {"condition": "Burns (zinc loss through wound exudate)", "direction": "low"}
        ],
        "sources": [{"name": "Mayo Clinic Laboratories - Zinc, Serum (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/overview/7735", "accessed": "2026-07-14"}]
    },
    {
        "slug": "ceruloplasmin", "name_en": "Ceruloplasmin, Serum",
        "aliases": "Ceruloplasmin",
        "category": "Clinical Chemistry",
        "purpose_en": "Primary first-line screening test for Wilson disease (an inherited disorder of copper metabolism), particularly in patients with unexplained liver disease, neurological, or psychiatric symptoms at a young age.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. As an acute-phase reactant, results should ideally be interpreted outside of acute illness/inflammation when possible, or with that context noted.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Ceruloplasmin", "population": "Adult", "range": "~20-40 mg/dL", "notes": "Reference ranges vary modestly by lab/method; levels are physiologically low in newborns and rise over the first 2 years of life"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Approximately 85-90% of patients with Wilson disease have a ceruloplasmin below 20 mg/dL, and this remains the standard first-line screening test, especially when combined with slit-lamp examination for Kayser-Fleischer corneal rings and 24-hour urine copper. However, ceruloplasmin is also a positive acute-phase reactant that can rise with inflammation, pregnancy, estrogen use, or infection -- and can be falsely low in general protein deficiency/malnutrition or nephrotic syndrome (urinary loss) -- so an isolated low or borderline result should be interpreted alongside the full clinical picture, and a normal ceruloplasmin does not completely exclude Wilson disease (a minority of confirmed cases have levels within or near the normal range). Cutoff values for diagnosing Wilson disease may also vary somewhat by population/laboratory.",
        "associated_conditions": [
            {"condition": "Wilson disease (hepatolenticular degeneration)", "direction": "low, typically <20 mg/dL"},
            {"condition": "Malnutrition / protein-losing states (nephrotic syndrome, protein-losing enteropathy)", "direction": "low, non-Wilson cause"},
            {"condition": "Acute-phase response (inflammation, infection, pregnancy, estrogen use)", "direction": "high, can mask an underlying low baseline"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Wilson Disease Workup: Serum Ceruloplasmin", "url": "https://emedicine.medscape.com/article/183456-workup", "accessed": "2026-07-14"},
            {"name": "University of Rochester Medical Center - Ceruloplasmin (Blood)", "url": "https://www.urmc.rochester.edu/encyclopedia/content?contenttypeid=167&contentid=ceruloplasmin_blood", "accessed": "2026-07-14"}
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
             interfering_factors_en, questions_to_ask_en, next_steps_en,
             associated_conditions_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
             t.get("interfering_factors_en"), t.get("questions_to_ask_en"), t.get("next_steps"),
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
