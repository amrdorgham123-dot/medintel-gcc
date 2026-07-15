"""
Seed script (batch 18) for MedForsa GCC's Lab Info reference library.
Adds Toxoplasma gondii IgG/IgM and Cytomegalovirus (CMV) IgG/IgM serology.

Run once: python3 seed_lab_tests_batch18.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "toxoplasma-igg-igm", "name_en": "Toxoplasma gondii IgG/IgM",
        "aliases": "Toxoplasma Serology, Toxo IgG, Toxo IgM, TORCH - Toxoplasmosis",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Screens for Toxoplasma gondii infection, most importantly during pregnancy, since primary maternal infection can cause congenital toxoplasmosis with serious fetal harm (chorioretinitis, intracranial calcifications, hydrocephalus); also used in immunocompromised patients at risk of reactivation (e.g., cerebral toxoplasmosis in advanced HIV).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. In pregnancy, testing is often done at the first prenatal visit and, if seronegative, may be repeated later in pregnancy in regions/populations with higher prevalence, to catch a new infection acquired during pregnancy.",
        "methodology_en": "Chemiluminescent or enzyme immunoassay detecting IgG and IgM separately; IgG avidity testing (a related assay) helps estimate how long ago an IgG-positive infection occurred, which is important for timing risk in pregnancy.",
        "reference_ranges": [
            {"parameter": "Toxoplasma IgG", "population": "Negative (non-immune)", "range": "<7.2 IU/mL (assay-dependent cutoff)"},
            {"parameter": "Toxoplasma IgM", "population": "Negative", "range": "<10.0 AU/mL (assay-dependent cutoff)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "IgG-positive/IgM-negative indicates past infection and immunity, generally not a concern in pregnancy since reactivation causing fetal harm is rare in immunocompetent people. IgM-positive results (with or without IgG) require careful interpretation, since IgM can remain detectable for months to over a year after infection and false-positive IgM results are common on initial (non-reference-laboratory) assays -- a positive IgM should prompt confirmatory testing at a reference toxoplasma laboratory, including IgG avidity testing, before concluding a recent infection occurred. A confirmed recent/acute infection during pregnancy requires urgent obstetric and infectious disease consultation, since treatment can reduce (though not eliminate) the risk of congenital transmission.",
        "associated_conditions": [
            {"condition": "Congenital toxoplasmosis risk (acute maternal infection during pregnancy)", "direction": "IgM positive, confirmed recent infection"},
            {"condition": "Past infection / immunity", "direction": "IgG positive, IgM negative"},
            {"condition": "Cerebral toxoplasmosis (reactivation in advanced immunosuppression, e.g., AIDS)", "direction": "IgG positive (prior infection) with new neurologic symptoms -- imaging and often empiric treatment take precedence over serology in this setting"}
        ],
        "critical_values_en": None,
        "interfering_factors_en": "Toxoplasma IgM has a well-documented tendency toward false positives on many commercial assays and can also remain positive for over a year after the true infection, so a positive IgM alone (especially from a non-reference laboratory) should not be used to diagnose acute infection or guide major clinical decisions (such as termination of pregnancy) without confirmatory reference-laboratory testing.",
        "questions_to_ask_en": "Does my result indicate a new infection or immunity from a past infection? If IgM is positive, do I need confirmatory testing at a reference laboratory before we act on this result? If I'm pregnant and non-immune (IgG negative), what precautions should I take to avoid a new infection during pregnancy? If a recent infection is confirmed, what is the plan for monitoring and possibly treating the pregnancy?",
        "next_steps": "A positive IgM result should prompt referral to (or consultation with) a reference toxoplasma serology laboratory for confirmatory testing and IgG avidity testing before concluding a recent infection has occurred, given the high false-positive rate of IgM on standard assays. If acute infection in pregnancy is confirmed, this requires close collaboration between obstetrics, infectious disease, and maternal-fetal medicine to guide treatment and fetal monitoring (which may include amniocentesis for PCR testing after 18 weeks gestation).",
        "sources": [
            {"name": "droracle.ai - Interpretation and management of a positive TORCH panel report (clinical synthesis)", "url": "https://www.droracle.ai/articles/423819/what-is-the-interpretation-and-management-of-a-positive", "accessed": "2026-07-14"},
            {"name": "Maurya Labs - TORCH Panel reference ranges", "url": "https://mauryalabs.com/patients-corner/pathology-tests/torch-panel/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "cmv-igg-igm", "name_en": "Cytomegalovirus (CMV) IgG/IgM",
        "aliases": "CMV Serology, CMV IgG, CMV IgM, TORCH - Cytomegalovirus",
        "category": "Immunoassay / Infectious Disease Serology",
        "purpose_en": "Screens for CMV infection, most importantly during pregnancy (congenital CMV is a leading infectious cause of hearing loss and developmental disability), and evaluates CMV status before transplant (donor/recipient matching) and in immunocompromised patients at risk of reactivation.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. In suspected active/congenital infection, CMV serology is often paired with CMV PCR (viral load) testing, which more directly detects active viral replication.",
        "methodology_en": "Chemiluminescent or enzyme immunoassay detecting IgG and IgM separately; IgG avidity testing helps estimate timing of infection (low avidity suggests infection within the past ~3-4 months).",
        "reference_ranges": [
            {"parameter": "CMV IgG", "population": "Negative (non-immune)", "range": "<12.0 IU/mL (assay-dependent cutoff)"},
            {"parameter": "CMV IgM", "population": "Negative", "range": "<18.0 AU/mL (assay-dependent cutoff)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "CMV seroprevalence is very high in the general population (commonly cited around 60-99% depending on the population studied), so IgG positivity alone is common and mainly indicates past infection/immunity, not current risk, in an immunocompetent person. As with toxoplasma, CMV IgM can persist for many months after primary infection and can also appear during reactivation or reinfection with a different strain, so a positive IgM (with or without positive IgG) requires IgG avidity testing to help distinguish a recent primary infection (the scenario of greatest concern in pregnancy) from an older infection or reactivation. Confirmed primary maternal infection carries the highest risk of severe congenital CMV; reactivation/reinfection in an already-immune mother carries substantially lower risk but is not zero.",
        "associated_conditions": [
            {"condition": "Congenital CMV risk (primary maternal infection during pregnancy)", "direction": "IgM positive with low IgG avidity, confirmed recent primary infection"},
            {"condition": "Past infection / immunity", "direction": "IgG positive, IgM negative, high avidity"},
            {"condition": "CMV reactivation (immunocompromised patients, transplant recipients)", "direction": "positive CMV PCR/viral load is the more direct marker; serology has limited utility for detecting reactivation in this setting"}
        ],
        "critical_values_en": None,
        "interfering_factors_en": "As with toxoplasma, CMV IgM can remain detectable for an extended period after primary infection and can be falsely positive, so it should not be used alone to date an infection or guide major clinical decisions -- IgG avidity testing and, where relevant, direct CMV PCR are needed for a confident interpretation. In immunocompromised or transplant patients, serology has limited value for detecting reactivation, since a new antibody response may not develop or may be blunted -- CMV PCR (viral load) is the preferred monitoring test in that setting.",
        "questions_to_ask_en": "Does my result mean I'm immune from a past infection, or could this be a new (primary) infection? If I'm pregnant, do I need IgG avidity testing to clarify the timing? If I'm being evaluated before a transplant, how does my CMV status affect donor selection or post-transplant monitoring? If I'm already immunosuppressed, should CMV PCR be used instead of (or alongside) serology to monitor for reactivation?",
        "next_steps": "In pregnancy, a positive IgM prompts IgG avidity testing to estimate timing of infection; a confirmed recent primary infection is discussed with maternal-fetal medicine regarding fetal monitoring and potential treatment options. In transplant candidates, CMV IgG status (positive or negative) is recorded and used alongside donor CMV status to guide post-transplant prophylaxis or monitoring strategy. In immunosuppressed patients with suspected active disease, CMV PCR (viral load) rather than serology is typically used to guide diagnosis and treatment decisions.",
        "sources": [
            {"name": "Today's Clinical Lab - Prenatal Diagnosis of TORCH Pathogens", "url": "https://www.clinicallab.com/prenatal-diagnosis-of-torch-pathogens-21819", "accessed": "2026-07-14"},
            {"name": "Maurya Labs - TORCH Panel reference ranges", "url": "https://mauryalabs.com/patients-corner/pathology-tests/torch-panel/", "accessed": "2026-07-14"}
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
             json.dumps(["rubella-igg", "hiv-ag-ab-combo"]),
             json.dumps(t["sources"]), 1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
