"""
Seed script (batch 27) for MedForsa GCC's Lab Info reference library.
Adds Sweat Chloride Test, Fecal Elastase-1, Cystatin C, and PIVKA-II.

Run once: python3 seed_lab_tests_batch27.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "sweat-chloride", "name_en": "Sweat Chloride Test",
        "aliases": "Sweat Test, Pilocarpine Iontophoresis Sweat Test",
        "category": "Clinical Chemistry",
        "purpose_en": "Gold-standard diagnostic test for cystic fibrosis (CF), used to confirm the diagnosis in infants with a positive newborn screen or in patients with clinical features suggestive of CF (chronic respiratory infections, growth failure, malabsorption).",
        "specimen_type": "Sweat, collected via pilocarpine iontophoresis (a small electrical current stimulates local sweat production, which is then collected and analyzed)",
        "collection_notes_en": "Requires an adequate sweat volume for a valid result; testing is ideally performed at an accredited CF center given the technical precision required, and repeated if the initial sample volume is insufficient.",
        "methodology_en": "Chloride concentration in the collected sweat is measured by coulometric titration or ion-selective electrode.",
        "reference_ranges": [
            {"parameter": "Sweat chloride", "population": "Normal", "range": "<40 mEq/L (mmol/L)"},
            {"parameter": "Sweat chloride", "population": "Intermediate (requires further evaluation)", "range": "30-59 mEq/L (age-dependent cutoffs vary)"},
            {"parameter": "Sweat chloride", "population": "Consistent with CF", "range": "\u226560 mEq/L"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A sweat chloride \u226560 mEq/L on two separate occasions is considered diagnostic of cystic fibrosis in the appropriate clinical context. Intermediate results require CFTR genetic mutation analysis to clarify the diagnosis, since some patients with CFTR-related disease can have borderline sweat chloride values. A normal sweat chloride makes classic CF unlikely but does not completely exclude rare CFTR-related disorders in patients with a strongly suggestive clinical picture.",
        "associated_conditions": [
            {"condition": "Cystic fibrosis", "direction": "high, \u226560 mEq/L"},
            {"condition": "CFTR-related disorder (borderline phenotype)", "direction": "intermediate, 30-59 mEq/L"}
        ],
        "questions_to_ask_en": "If the result is intermediate, do I need CFTR genetic testing to clarify the diagnosis? What does this mean for my child's long-term care plan? Do other family members need to be tested?",
        "next_steps": "A diagnostic result leads to referral to a CF care center for comprehensive management planning (pulmonary, nutritional, and genetic counseling). An intermediate result prompts CFTR genetic mutation analysis, and the test may be repeated to confirm an adequate, valid sweat sample was obtained.",
        "sources": [
            {"name": "droracle.ai - Cystic Fibrosis Diagnosis and Management (CDC/AAP-referenced sweat chloride and fecal elastase cutoffs)", "url": "https://www.droracle.ai/guidelines/2c50bd2d-9911-426c-909b-ab6b2bd9c198?z=673774", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "fecal-elastase", "name_en": "Fecal Elastase-1",
        "aliases": "Fecal Elastase, Pancreatic Elastase",
        "category": "Clinical Chemistry",
        "purpose_en": "Non-invasive screening test for exocrine pancreatic insufficiency (EPI), used in patients with cystic fibrosis, chronic pancreatitis, or unexplained malabsorption/steatorrhea.",
        "specimen_type": "Random stool sample (formed, not liquid, for accurate results)",
        "collection_notes_en": "A formed stool sample is needed for accurate results, since liquid/watery stool can dilute the elastase concentration and cause a falsely low result unrelated to true pancreatic function. Pancreatic enzyme replacement therapy does not need to be stopped before testing, since the assay detects human elastase specifically and does not cross-react with supplemental enzymes.",
        "methodology_en": "Enzyme-linked immunosorbent assay (ELISA) using antibodies specific to human pancreatic elastase-1.",
        "reference_ranges": [
            {"parameter": "Fecal elastase-1", "population": "Normal pancreatic function", "range": ">200 \u00b5g/g (some sources cite >184-480 \u00b5g/g as the normal cutoff, varying by study/population)"},
            {"parameter": "Fecal elastase-1", "population": "Exocrine pancreatic insufficiency", "range": "<100 \u00b5g/g"},
            {"parameter": "Fecal elastase-1", "population": "Severe exocrine pancreatic insufficiency", "range": "<50 \u00b5g/g", "notes": "Per American Academy of Pediatrics guidance for cystic fibrosis"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A low result supports exocrine pancreatic insufficiency and, in patients with cystic fibrosis or chronic pancreatitis, guides the decision to start or adjust pancreatic enzyme replacement therapy (PERT). It is a sensitive and specific indirect marker, though borderline results (roughly 100-200 \u00b5g/g) may need clinical correlation or a repeat test, since dilutional effects from liquid stool can lower the result independent of true pancreatic function.",
        "associated_conditions": [
            {"condition": "Cystic fibrosis with pancreatic insufficiency", "direction": "low, often severely (<50 \u00b5g/g)"},
            {"condition": "Chronic pancreatitis", "direction": "low"},
            {"condition": "Malabsorption / steatorrhea from exocrine pancreatic insufficiency", "direction": "low"}
        ],
        "questions_to_ask_en": "Does this confirm my malabsorption symptoms are from pancreatic insufficiency? Do I need to start (or adjust) pancreatic enzyme replacement therapy? Should this be rechecked periodically to monitor my pancreatic function?",
        "next_steps": "A low result in someone with malabsorption symptoms typically leads to pancreatic enzyme replacement therapy (PERT), with fat-soluble vitamin (A, D, E, K) levels also checked given the associated malabsorption risk, and nutritional status monitored over time.",
        "sources": [
            {"name": "ScienceDirect - Fecal elastase-1 cut-off levels in the assessment of exocrine pancreatic function in cystic fibrosis", "url": "https://www.sciencedirect.com/science/article/pii/S1569199302000966", "accessed": "2026-07-15"},
            {"name": "droracle.ai - Cystic Fibrosis Diagnosis and Management (AAP fecal elastase cutoffs)", "url": "https://www.droracle.ai/guidelines/2c50bd2d-9911-426c-909b-ab6b2bd9c198?z=673774", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "cystatin-c", "name_en": "Cystatin C, Serum",
        "aliases": "Cystatin C",
        "category": "Clinical Chemistry",
        "purpose_en": "Alternative/complementary marker of kidney function to creatinine, used to estimate GFR, particularly valuable when creatinine-based estimates may be unreliable (e.g., very muscular, frail/sarcopenic, or malnourished patients) or to confirm early kidney function decline.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Unlike creatinine, cystatin C production is not significantly affected by muscle mass, diet, or sex, making it useful when these factors are expected to distort creatinine-based estimates.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Cystatin C", "population": "Adult", "range": "Approximately 0.6-1.0 mg/L", "notes": "Reference range varies modestly by lab/assay"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated cystatin C suggests reduced kidney filtration, and current KDIGO guidance recommends using the combined creatinine-cystatin C eGFR equation (CKD-EPI 2021) for improved accuracy, particularly in elderly, cancer, or hospitalized patients, and in situations where creatinine-based eGFR results (60-75 mL/min/1.73m\u00b2) need clarification -- distinguishing true kidney function decline from a muscle-mass effect on creatinine. Cystatin C has also been studied as a stronger predictor of cardiovascular events than creatinine-based eGFR in some large cohort studies, though it should be used alongside, not instead of, standard cardiovascular risk assessment. Clinical decisions should rely on validated combined eGFR equations rather than an isolated cystatin C value.",
        "associated_conditions": [
            {"condition": "Chronic kidney disease (early or masked by low muscle mass)", "direction": "high"},
            {"condition": "Reduced GFR in elderly, frail, or highly muscular patients where creatinine is unreliable", "direction": "high, clarifies true kidney function"}
        ],
        "questions_to_ask_en": "Why was this test added to my creatinine-based kidney function assessment? Does this change my calculated eGFR and kidney disease stage? Does this affect any medication dosing decisions?",
        "next_steps": "Results are used together with creatinine in a combined eGFR equation (per current KDIGO guidance) rather than interpreted alone, and a combined eGFR significantly different from the creatinine-only estimate may prompt adjustment of medication dosing or kidney disease staging.",
        "sources": [
            {"name": "Cleveland Clinic Journal of Medicine - The role of cystatin C in estimating glomerular filtration rate and guiding medication dosing", "url": "https://www.ccjm.org/content/92/9/546", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "pivka-ii", "name_en": "PIVKA-II (Des-Gamma-Carboxy Prothrombin, DCP)",
        "aliases": "PIVKA-II, DCP, Des-Gamma-Carboxy Prothrombin",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Tumor marker used alongside AFP for hepatocellular carcinoma (HCC) surveillance and diagnosis in high-risk patients (cirrhosis, chronic hepatitis B/C), particularly useful for detecting AFP-negative HCC.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Vitamin K deficiency or warfarin use can independently raise PIVKA-II (since it reflects an abnormal, undercarboxylated prothrombin produced when vitamin K-dependent carboxylation is impaired) unrelated to HCC -- this history should be reviewed when interpreting an elevated result.",
        "methodology_en": "Chemiluminescent or electrochemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "PIVKA-II", "population": "Normal", "range": "Commonly cited cutoffs for HCC detection range from ~37-58 mAU/mL depending on the study/population", "notes": "Cutoffs vary by assay and population; always use the reporting lab's own reference range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated PIVKA-II supports a diagnosis of hepatocellular carcinoma, with several studies showing it performs comparably to or better than AFP alone for HCC detection, and the combination of both markers together improves diagnostic accuracy over either alone. Higher levels are also associated with larger tumor size, vascular invasion, and worse prognosis in confirmed HCC. As with AFP, PIVKA-II is used for surveillance in high-risk patients (cirrhosis, chronic hepatitis) and to help monitor treatment response, but a mildly elevated result should be interpreted alongside vitamin K/warfarin status, since that is a well-recognized non-cancer cause of elevation.",
        "associated_conditions": [
            {"condition": "Hepatocellular carcinoma (diagnosis, surveillance, prognosis)", "direction": "high, correlates with tumor size and vascular invasion"},
            {"condition": "Vitamin K deficiency / warfarin therapy (non-cancer cause)", "direction": "high, unrelated to malignancy"}
        ],
        "questions_to_ask_en": "Does this, combined with my AFP result, suggest liver cancer? Could my warfarin use or vitamin K status be contributing to this result? Do I need imaging to look for a liver mass?",
        "next_steps": "An elevated result, especially combined with an elevated AFP, typically prompts liver imaging (ultrasound, CT, or MRI) to look for a mass; if you're on warfarin or have vitamin K deficiency, this is factored into interpretation before further workup is pursued.",
        "sources": [
            {"name": "PMC - Value of AFP and PIVKA-II in diagnosis of HBV-related hepatocellular carcinoma", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7684907/", "accessed": "2026-07-15"},
            {"name": "PMC - Utility of PIVKA-II and AFP in Differentiating Hepatocellular Carcinoma from Non-Malignant High-Risk Patients", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9416286/", "accessed": "2026-07-15"}
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
        related = ["afp"] if t["slug"]=="pivka-ii" else (["creatinine", "bun"] if t["slug"]=="cystatin-c" else [])
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
             json.dumps(related),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
