"""
Seed script (batch 12) for MedForsa GCC's Lab Info reference library.
Adds Free PSA (%), Prealbumin, and Transferrin.

Run once: python3 seed_lab_tests_batch12.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "free-psa", "name_en": "Free PSA (% Free PSA)",
        "aliases": "Free PSA, %fPSA, Free-to-Total PSA Ratio",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Refines prostate cancer risk when total PSA falls in the diagnostically ambiguous 'gray zone' (roughly 4-10 ng/mL), helping decide whether a biopsy is warranted and reducing unnecessary biopsies for benign prostatic hyperplasia (BPH).",
        "specimen_type": "Venous serum, ideally processed promptly (free PSA is less stable than total PSA and can degrade with storage/delay)",
        "collection_notes_en": "Should be drawn before a digital rectal exam, prostate biopsy, or catheterization when possible, as manipulation of the prostate can transiently raise both total and free PSA. Recent ejaculation can also transiently affect results.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) measuring free (unbound) PSA, reported as a percentage of the simultaneously measured total PSA (% free PSA = free PSA / total PSA x 100).",
        "reference_ranges": [
            {"parameter": "% Free PSA", "population": "Lower risk (benign disease more likely)", "range": ">25%"},
            {"parameter": "% Free PSA", "population": "Intermediate risk", "range": "10-25%"},
            {"parameter": "% Free PSA", "population": "Higher risk", "range": "<10%", "notes": "Most clinically useful when total PSA is 4-10 ng/mL; cutoffs vary somewhat by lab, age, and guideline source"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Men with prostate cancer tend to have a lower percentage of free (unbound) PSA relative to total PSA than men with benign prostatic hyperplasia, even at the same total PSA level. In the 4-10 ng/mL total PSA gray zone, a % free PSA below roughly 10% is associated with a substantially higher probability of a positive biopsy (historically cited around 50%) compared to a % free PSA above 25% (historically cited around 10-16%). This test does not replace biopsy for diagnosis but helps stratify who is more or less likely to benefit from one, reducing unnecessary biopsies in men with a high % free PSA.",
        "critical_values_en": None,
        "interfering_factors_en": "Recent digital rectal exam, prostate biopsy, catheterization, or ejaculation can transiently raise PSA (both total and free) and should be avoided before the draw when possible. Free PSA is less stable than total PSA in a stored/delayed sample, so prompt processing improves accuracy.",
        "questions_to_ask_en": "Given my total PSA and % free PSA together, what is my estimated risk of prostate cancer? Do I need a biopsy now, or is continued PSA monitoring reasonable? Are there other tools (e.g., PSA density, MRI, newer biomarker tests) that could help refine this decision further? How often should PSA and % free PSA be rechecked if we decide to monitor rather than biopsy?",
        "next_steps": "Your urologist will weigh your % free PSA together with your total PSA, age, family history, and DRE findings to decide whether biopsy, active PSA/free PSA surveillance, or additional imaging (such as prostate MRI) is the most appropriate next step -- a low % free PSA increases suspicion but does not alone confirm cancer, just as a reassuring % free PSA does not completely exclude it.",
        "associated_conditions": [
            {"condition": "Prostate cancer (higher probability)", "direction": "low % free PSA (<10%), especially with total PSA 4-10 ng/mL"},
            {"condition": "Benign prostatic hyperplasia (more likely)", "direction": "high % free PSA (>25%)"}
        ],
        "sources": [
            {"name": "Mayo Clinic Proceedings - Percent Free Prostate-Specific Antigen: Entering a New Era in the Detection of Prostate Cancer", "url": "https://www.mayoclinicproceedings.org/article/S0025-6196(11)63334-X/fulltext", "accessed": "2026-07-14"},
            {"name": "PMC - Using the Free-to-total Prostate-specific Antigen Ratio to Detect Prostate Cancer in Men with Nonspecific Elevations of PSA Levels", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC1495603/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "prealbumin", "name_en": "Prealbumin (Transthyretin), Serum",
        "aliases": "Prealbumin, Transthyretin, TTR",
        "category": "Clinical Chemistry",
        "purpose_en": "Sensitive short-term marker of nutritional status and protein-calorie malnutrition; used to assess and monitor nutritional status in hospitalized, critically ill, or chronically ill patients, since it responds faster to changes in nutrition than albumin.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Because prealbumin is also a negative acute-phase reactant, it should ideally be interpreted alongside CRP to distinguish true malnutrition from an acute inflammatory drop.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay on automated chemistry analyzers.",
        "reference_ranges": [
            {"parameter": "Prealbumin", "population": "Adult", "range": "15-30 mg/dL (150-300 mg/L)", "notes": "Some labs cite up to 35-40 mg/dL as the upper limit"},
            {"parameter": "Prealbumin", "population": "Moderate malnutrition risk", "range": "10-17 mg/dL"},
            {"parameter": "Prealbumin", "population": "Severe malnutrition risk", "range": "<10 mg/dL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Because prealbumin has a short half-life (about 2-3 days, compared to roughly 20 days for albumin), it reflects recent changes in nutritional status more quickly and is useful for monitoring response to nutritional support over days to weeks rather than months. As a negative acute-phase reactant, prealbumin also falls during acute illness, inflammation, infection, surgery, or trauma independent of true nutritional intake, so a low level should be interpreted alongside CRP or clinical context before attributing it purely to malnutrition. It can also be falsely elevated in dehydration and in some cases of acute alcohol-related liver injury.",
        "associated_conditions": [
            {"condition": "Protein-calorie malnutrition", "direction": "low"},
            {"condition": "Acute-phase response (infection, inflammation, surgery, trauma)", "direction": "low, independent of nutrition"},
            {"condition": "Chronic liver disease (reduced synthesis)", "direction": "low"}
        ],
        "sources": [{"name": "American Family Physician (AAFP) - Prealbumin: A Marker for Nutritional Evaluation", "url": "https://www.aafp.org/pubs/afp/issues/2002/0415/p1575.html", "accessed": "2026-07-14"}]
    },
    {
        "slug": "transferrin", "name_en": "Transferrin, Serum",
        "aliases": "Transferrin",
        "category": "Clinical Chemistry / Hematology",
        "purpose_en": "Iron transport protein used both as an iron-status marker (with iron and TIBC) and, historically, as a longer-term nutritional status marker; low transferrin is one of several markers used to assess protein malnutrition.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Morning fasting sample preferred when assessed together with serum iron, due to diurnal variation in iron studies.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay on automated chemistry analyzers; TIBC (total iron-binding capacity) is closely related and can be calculated from transferrin, or measured directly.",
        "reference_ranges": [{"parameter": "Transferrin", "population": "Adult", "range": "~200-360 mg/dL", "notes": "Reference range varies modestly by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low transferrin is seen in protein-calorie malnutrition, chronic liver disease (reduced synthesis), nephrotic syndrome (urinary loss), and chronic inflammation (transferrin is a negative acute-phase reactant, similar to albumin). High transferrin is the classic finding in iron-deficiency anemia, where the body upregulates transferrin production in an attempt to maximize iron transport despite low iron stores -- this is why transferrin/TIBC rises while ferritin and serum iron fall in iron deficiency, a pattern that helps distinguish it from anemia of chronic disease (where transferrin is typically low-normal or low despite also having low iron).",
        "associated_conditions": [
            {"condition": "Iron-deficiency anemia", "direction": "high (elevated TIBC)"},
            {"condition": "Protein-calorie malnutrition / chronic liver disease / nephrotic syndrome", "direction": "low"},
            {"condition": "Anemia of chronic disease/inflammation", "direction": "low-normal, despite also having low iron"}
        ],
        "sources": [
            {"name": "Medscape - Nutritional Support and the Surgical Patient (transferrin as nutritional marker)", "url": "https://www.medscape.com/viewarticle/474066_6", "accessed": "2026-07-14"}
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
