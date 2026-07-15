"""
Seed script (batch 22) for MedForsa GCC's Lab Info reference library.
Adds 7 tests: Procalcitonin, Creatine Kinase (Total), Tissue Transglutaminase
IgA, Fecal Calprotectin, Myoglobin, Interleukin-6, Anti-Xa (Heparin) Assay.

Run once: python3 seed_lab_tests_batch22.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "procalcitonin", "name_en": "Procalcitonin (PCT), Serum",
        "aliases": "PCT, Procalcitonin",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Helps distinguish bacterial from non-bacterial causes of infection/inflammation and supports decisions about starting or stopping antibiotics, particularly in sepsis, lower respiratory tract infection, and febrile neutropenia.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Often ordered serially (e.g., daily) to track trend during antibiotic treatment, since the trajectory is often more clinically useful than a single value.",
        "methodology_en": "Chemiluminescent or immunofluorescent immunoassay on automated immunoassay analyzers or point-of-care platforms.",
        "reference_ranges": [{"parameter": "Procalcitonin", "population": "Adult/child \u226572 hours old", "range": "\u22640.15 ng/mL", "notes": "Neonates <72 hours have markedly different, higher physiologic reference ranges"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Procalcitonin rises specifically in response to bacterial infection (via bacterial endotoxin-driven cytokine release) more than in viral infection or non-infectious inflammation, making it useful for distinguishing bacterial sepsis from other causes of systemic inflammatory response and for guiding antibiotic initiation/discontinuation protocols. Higher levels generally correlate with greater severity and risk of progression to septic shock; a level that fails to fall (or rises) despite treatment suggests inadequate source control or ongoing/secondary infection. Levels also vary by the causative organism, tending to be higher with gram-negative than gram-positive or fungal infections in some studies, though this is not reliable enough to guide organism-specific therapy on its own.",
        "associated_conditions": [
            {"condition": "Bacterial sepsis/septic shock", "direction": "high, correlates with severity"},
            {"condition": "Viral infection / non-infectious inflammation", "direction": "typically low/normal, helping distinguish from bacterial cause"},
            {"condition": "Response to antibiotic therapy (monitoring)", "direction": "declining trend indicates response; persistent/rising suggests treatment failure"}
        ],
        "critical_values_en": None,
        "interfering_factors_en": "Non-infectious causes of marked systemic inflammation (major trauma, surgery, burns, cardiogenic shock, severe pancreatitis) can also elevate procalcitonin independent of bacterial infection, so results must be interpreted alongside the full clinical picture rather than as a standalone rule-in/rule-out test.",
        "questions_to_ask_en": "Does this level support starting or continuing antibiotics, or could it support stopping them? How does today's level compare to previous days, and what does that trend mean for my treatment plan? Could a non-infectious cause (recent surgery, trauma) be contributing to this result?",
        "next_steps": "Procalcitonin results are typically used alongside clinical assessment, cultures, and other inflammatory markers (like CRP) to guide antibiotic decisions -- many hospitals use protocol-driven algorithms where a low or declining procalcitonin supports antibiotic discontinuation, while a rising or persistently high level prompts reassessment for ongoing infection or source control failure.",
        "sources": [{"name": "Medscape/eMedicine - Procalcitonin (PCT): Reference Range, Interpretation of Procalcitonin Levels", "url": "https://emedicine.medscape.com/article/2096589-overview", "accessed": "2026-07-15"}]
    },
    {
        "slug": "creatine-kinase-total", "name_en": "Creatine Kinase (CK), Total",
        "aliases": "CK, CPK, Creatine Phosphokinase",
        "category": "Clinical Chemistry",
        "purpose_en": "Screens for and monitors muscle injury (skeletal or cardiac); used to diagnose and follow rhabdomyolysis, myositis/myopathy, and to distinguish myoglobinuria from hemoglobinuria; historically used for MI diagnosis before troponin became standard.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Avoid strenuous exercise immediately before the draw and note any recent intramuscular injections, surgery, or muscle trauma, all of which can transiently raise results.",
        "methodology_en": "Enzymatic kinetic assay on automated chemistry analyzers.",
        "reference_ranges": [
            {"parameter": "CK, total", "population": "Adult male (Caucasian/Asian)", "range": "~227-440 U/L (upper limit varies by population)", "notes": "Black individuals have significantly higher normal upper limits (~520-810 U/L); values are non-Gaussian distributed and vary by lab/method"},
            {"parameter": "CK, total", "population": "Adult female", "range": "~135-248 U/L (upper limit varies by population)", "notes": "Higher upper limits reported in Black women (~up to 354 U/L)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Markedly elevated CK (often 5-10x the upper limit or more) supports rhabdomyolysis, with the degree of elevation correlating with risk of acute kidney injury in observational data (risk of dialysis/renal failure increases progressively above roughly 1,000-5,000 U/L and higher). Milder elevations are common after strenuous exercise, intramuscular injections, surgery, or seizures, and are not necessarily pathologic. CK is also used with LD to distinguish myoglobinuria (CK markedly elevated, LD mildly elevated) from hemoglobinuria/hemolysis (CK normal, LD/LD1 elevated). Statin-associated myopathy is another common cause of mild-to-moderate elevation.",
        "critical_values_en": "CK levels \u22651,000 U/L are associated with progressively increasing risk of acute kidney injury and need for dialysis in rhabdomyolysis per observational cohort data; markedly elevated CK in a symptomatic patient (muscle pain, dark urine) warrants urgent evaluation for rhabdomyolysis and its renal complications.",
        "interfering_factors_en": "Strenuous exercise, intramuscular injections, recent surgery involving muscle incision, and seizures can all transiently raise CK independent of significant underlying pathology -- timing and history around the draw are important for interpretation.",
        "questions_to_ask_en": "Is this level of elevation consistent with a benign cause (recent exercise, injection) or does it suggest rhabdomyolysis requiring urgent evaluation? Do I need kidney function monitoring given this result? If I'm on a statin, could this be medication-related, and does my statin need adjustment?",
        "next_steps": "Markedly elevated CK, especially with symptoms (muscle pain, weakness, dark urine), typically prompts urgent evaluation of kidney function, aggressive IV fluid hydration to prevent kidney injury, and investigation of the underlying cause (exertional, traumatic, toxic/drug-induced, or inflammatory myopathy). Mild elevations without symptoms are often simply repeated or monitored.",
        "associated_conditions": [
            {"condition": "Rhabdomyolysis", "direction": "markedly high, often several-fold above upper limit"},
            {"condition": "Statin-associated myopathy", "direction": "mild-moderate high"},
            {"condition": "Inflammatory myopathy (polymyositis/dermatomyositis)", "direction": "high"},
            {"condition": "Recent exercise, IM injection, or surgery (benign cause)", "direction": "mild-moderate high"}
        ],
        "sources": [
            {"name": "PMC - What Are the Normal Serum Creatine Kinase Values for Skeletal Muscle? A Worldwide Systematic Review", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12163646/", "accessed": "2026-07-15"},
            {"name": "PMC - Creatine Kinase Elevations and Risk of Renal Failure and Dialysis in Patients With Rhabdomyolysis", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12282552/", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "ttg-iga", "name_en": "Tissue Transglutaminase IgA Antibody (tTG-IgA)",
        "aliases": "tTG-IgA, Anti-tTG, Celiac Antibody Screen",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "First-line serologic screening test for celiac disease in patients with compatible symptoms (chronic diarrhea, malabsorption, unexplained iron deficiency) or at increased risk (first-degree relatives, type 1 diabetes, autoimmune thyroid disease).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Must be tested while the patient is still consuming gluten -- starting a gluten-free diet before testing can cause a false-negative result. A total IgA level should be checked alongside, since IgA-deficient patients (about 2-3% of celiac patients) will have a falsely low/negative tTG-IgA and need tTG-IgG testing instead.",
        "methodology_en": "Enzyme immunoassay (EIA) or chemiluminescent immunoassay (CLIA) detecting IgA antibodies against tissue transglutaminase.",
        "reference_ranges": [{"parameter": "tTG-IgA", "population": "Negative", "range": "Assay-dependent cutoff, commonly <4 to <20 U/mL depending on the platform", "notes": "Different manufacturers/labs use different units and cutoffs -- always use the reporting lab's own reference range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A tTG-IgA titer \u226510 times the assay's upper limit of normal has a high positive predictive value (around 95% in adults) for celiac disease, and some pediatric guidelines allow a biopsy-free diagnosis when combined with a positive endomysial antibody on a separate sample and compatible symptoms. Lower-titer positive results are less specific and generally warrant duodenal biopsy for confirmation, since tTG-IgA can also be mildly elevated in other autoimmune or liver conditions. A negative result in a patient with normal total IgA makes celiac disease unlikely but does not completely exclude it, particularly in patients already reducing gluten intake or with very mild disease.",
        "associated_conditions": [
            {"condition": "Celiac disease", "direction": "high, especially \u226510x upper limit of normal"},
            {"condition": "IgA deficiency (false-negative tTG-IgA)", "direction": "falsely low despite possible celiac disease -- check total IgA"}
        ],
        "sources": [{"name": "Mayo Clinic Laboratories - Tissue Transglutaminase Antibodies, IgA and IgG Profile, Serum (test catalog)", "url": "https://neurology.testcatalog.org/show/TSTGP", "accessed": "2026-07-15"}]
    },
    {
        "slug": "fecal-calprotectin", "name_en": "Fecal Calprotectin",
        "aliases": "Calprotectin, Stool Calprotectin",
        "category": "Clinical Chemistry / Point of Care",
        "purpose_en": "Non-invasive marker of intestinal mucosal inflammation, used to distinguish inflammatory bowel disease (Crohn's disease, ulcerative colitis) from irritable bowel syndrome, and to monitor IBD disease activity and response to treatment without repeated colonoscopy.",
        "specimen_type": "Stool sample, collected by the patient in a specimen container",
        "collection_notes_en": "A random stool sample is generally sufficient (no special preparation required); recent NSAID/aspirin use should be noted, as it can cause a false-positive elevation unrelated to IBD.",
        "methodology_en": "Enzyme immunoassay (ELISA) or lateral-flow point-of-care immunoassay detecting the calprotectin protein, which is released by neutrophils during intestinal inflammation.",
        "reference_ranges": [
            {"parameter": "Fecal calprotectin", "population": "Not suggestive of active inflammation", "range": "<50 \u00b5g/g"},
            {"parameter": "Fecal calprotectin", "population": "Borderline/mild inflammation", "range": "50-120 \u00b5g/g", "notes": "May warrant retesting in 4-6 weeks"},
            {"parameter": "Fecal calprotectin", "population": "Suggestive of active inflammation", "range": ">120 \u00b5g/g", "notes": "Cutoffs vary somewhat between labs (commonly cited thresholds range from 50-250 \u00b5g/g depending on clinical use)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A normal fecal calprotectin (<50 \u00b5g/g) has high sensitivity and negative predictive value for excluding IBD in adults and children, meaning colonoscopy can often be safely deferred in patients with IBS-like symptoms and a normal result. Elevated levels support active mucosal inflammation but are not specific to IBD -- infectious enteritis, colorectal cancer, celiac disease, and NSAID use can also raise it, so results must be interpreted alongside the clinical picture. In established IBD, serial calprotectin is used to monitor disease activity and treatment response, often targeting levels below roughly 250 \u00b5g/g as part of tight-control treatment strategies, since it correlates with mucosal healing better than symptoms alone.",
        "interfering_factors_en": "NSAID and aspirin use can cause mucosal inflammation independent of IBD, leading to false-positive elevation. Children under 4-5 years and adults over 65 have physiologically higher baseline levels, requiring age-adjusted interpretation.",
        "questions_to_ask_en": "Given my result, is colonoscopy still needed, or can it reasonably be deferred? If I have known IBD, does this level suggest my current treatment is controlling inflammation adequately? Could a medication I'm taking (like NSAIDs) be affecting this result? Should this be repeated, and if so, when?",
        "next_steps": "A normal result in a patient with IBS-like symptoms generally supports a non-inflammatory diagnosis and colonoscopy can often be deferred with clinical monitoring. An elevated result typically prompts further workup (colonoscopy, stool studies for infection) to identify the cause. In established IBD, serial levels guide treatment adjustments as part of a tight-control monitoring strategy.",
        "associated_conditions": [
            {"condition": "Inflammatory bowel disease (Crohn's disease, ulcerative colitis)", "direction": "high, correlates with mucosal inflammation"},
            {"condition": "Irritable bowel syndrome (functional, non-inflammatory)", "direction": "normal/low in the vast majority of cases"},
            {"condition": "Infectious enteritis / NSAID-induced enteropathy", "direction": "high, non-IBD cause"}
        ],
        "sources": [
            {"name": "American Family Physician (AAFP) - Fecal Calprotectin for the Evaluation of Inflammatory Bowel Disease", "url": "https://www.aafp.org/pubs/afp/issues/2021/0900/p303.html", "accessed": "2026-07-15"},
            {"name": "Mayo Clinic Laboratories - Calprotectin, Feces (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/Overview/63016", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "myoglobin", "name_en": "Myoglobin, Serum",
        "aliases": "Myoglobin",
        "category": "Clinical Chemistry / Cardiac Biomarkers",
        "purpose_en": "Early, sensitive but non-specific marker of muscle injury, historically used as an early marker for myocardial infarction (rises faster than troponin) and now mainly used to diagnose and assess severity of rhabdomyolysis.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Often ordered serially in the early hours after suspected muscle injury given its rapid rise and fall kinetics.",
        "methodology_en": "Chemiluminescent or turbidimetric immunoassay on automated analyzers.",
        "reference_ranges": [
            {"parameter": "Myoglobin", "population": "Adult male", "range": "0-72 ng/mL"},
            {"parameter": "Myoglobin", "population": "Adult female", "range": "0-58 ng/mL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Myoglobin rises within 1-2 hours of muscle injury (faster than CK or troponin), making it useful as an early, sensitive marker, but it lacks specificity since it rises with any skeletal or cardiac muscle injury and is also elevated in renal failure due to reduced clearance. A level above roughly 150-170 ng/mL is often cited as supportive of rhabdomyolysis, with some sources using higher thresholds (around 600 ng/mL) as more specifically concerning, though CK trend and clinical context remain central to the diagnosis. Because of its low specificity, myoglobin has been largely superseded by troponin for cardiac diagnosis and is now used mainly in rhabdomyolysis assessment alongside CK.",
        "associated_conditions": [
            {"condition": "Rhabdomyolysis", "direction": "high, often markedly, with elevated CK"},
            {"condition": "Acute myocardial infarction (early marker, historical use)", "direction": "high, rises before troponin but less specific"},
            {"condition": "Renal failure (reduced clearance)", "direction": "high, independent of new muscle injury"}
        ],
        "sources": [
            {"name": "MedlinePlus (NIH/NLM) - Myoglobin blood test", "url": "https://medlineplus.gov/ency/article/003663.htm", "accessed": "2026-07-15"},
            {"name": "droracle.ai - Diagnostic serum myoglobin level for rhabdomyolysis (clinical synthesis)", "url": "https://www.droracle.ai/articles/301838/what-is-the-diagnostic-serum-myoglobin-myoglobin-level-for", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "il-6", "name_en": "Interleukin-6 (IL-6), Serum",
        "aliases": "IL-6, Interleukin-6",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Pro-inflammatory cytokine marker used to assess severity and prognosis in sepsis/critical illness (including COVID-19), evaluate suspected cytokine release syndrome, and as a research/adjunct marker in some inflammatory and autoimmune conditions.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Plasma is preferred over serum by some laboratories -- confirm the specimen type required by the specific assay.",
        "methodology_en": "Enzyme-linked immunosorbent assay (ELISA) or chemiluminescent immunoassay.",
        "reference_ranges": [{"parameter": "IL-6", "population": "Healthy adult", "range": "Approximately <12.5 to <17.4 pg/mL", "notes": "Reference values are derived from limited healthy populations and are not formal diagnostic thresholds; cutoffs vary meaningfully by assay platform"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated IL-6 is a marker of active systemic inflammation and has been studied as a prognostic marker in sepsis and critical illness, with higher and rising levels associated with greater disease severity and, in some studies (including COVID-19 cohorts), higher risk of mortality or need for escalated care. It is also used to help identify cytokine release syndrome (e.g., after CAR-T cell therapy or severe infection) and can guide use of IL-6 receptor-blocking therapies (e.g., tocilizumab) in specific clinical contexts. As a research-oriented and less standardized assay compared to CRP, results should be interpreted with awareness of assay-specific reference ranges and in the context of the broader clinical picture rather than as an isolated diagnostic threshold.",
        "associated_conditions": [
            {"condition": "Severe sepsis / septic shock (prognostic marker)", "direction": "high, correlates with severity"},
            {"condition": "Cytokine release syndrome", "direction": "markedly high"},
            {"condition": "Severe COVID-19 / other severe systemic inflammatory states", "direction": "high, associated with worse outcomes in some studies"}
        ],
        "sources": [{"name": "MLabs (University of Michigan) - Interleukin 6 (IL-6), Serum (test catalog)", "url": "https://mlabs.umich.edu/tests/interleukin-6-il-6-serum", "accessed": "2026-07-15"}]
    },
    {
        "slug": "anti-xa-assay", "name_en": "Anti-Xa (Heparin) Assay",
        "aliases": "Anti-Factor Xa, Anti-Xa, Heparin Level, UFH Anti-Xa, LMWH Anti-Xa",
        "category": "Hematology / Coagulation",
        "purpose_en": "Monitors anticoagulation with unfractionated heparin (UFH) and low-molecular-weight heparin (LMWH), particularly when aPTT is unreliable (e.g., baseline prolonged aPTT, lupus anticoagulant, heparin resistance) or when monitoring LMWH, which does not reliably affect aPTT.",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "Timing relative to the dose is critical: for LMWH, blood is typically drawn 3-4 hours after subcutaneous injection (peak level) unless a trough level is specifically needed; for continuous UFH infusion, timing follows institutional protocol (commonly every 6 hours after a rate change). Avoid drawing from a line containing heparin.",
        "methodology_en": "Chromogenic anti-Xa assay measuring the degree of inhibition of activated factor X by heparin-antithrombin complexes.",
        "reference_ranges": [
            {"parameter": "Anti-Xa, unfractionated heparin (UFH) therapeutic range", "population": "Adult, for venous thromboembolism treatment", "range": "0.3-0.7 IU/mL", "notes": "Lower-intensity ranges (e.g., 0.10-0.32 IU/mL, aligned with aPTT 50-70 sec) are used for some indications"},
            {"parameter": "Anti-Xa, LMWH therapeutic range", "population": "Adult", "range": "Assay/indication-dependent, commonly around 0.5-1.0 IU/mL for treatment dosing (peak level)", "notes": "Target ranges vary by specific LMWH product and indication"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A result below the therapeutic range suggests under-anticoagulation and increased clotting/thrombosis risk, prompting a dose increase per institutional heparin nomogram. A result above the therapeutic range (a critical value is commonly set around >1.0 IU/mL) suggests over-anticoagulation and increased bleeding risk, prompting a dose reduction or hold. In renal impairment, LMWH clearance is reduced, so anti-Xa levels can rise unexpectedly even without a dose change, making monitoring especially important in that population.",
        "critical_values_en": "A UFH anti-Xa level >1.0 IU/mL is commonly used as a critical value indicating significant over-anticoagulation and bleeding risk, warranting prompt dose reduction/hold and clinical reassessment.",
        "interfering_factors_en": "Sample contamination from a heparin-containing IV line falsely raises results. Delayed separation of plasma from cells, incorrect draw timing relative to the dose, and under-filled citrate tubes (wrong blood-to-anticoagulant ratio) can all affect accuracy.",
        "questions_to_ask_en": "Is my current heparin dose in the therapeutic range, and if not, how will it be adjusted? Given my kidney function, do I need more frequent monitoring if I'm on LMWH? If my aPTT and anti-Xa results don't agree, which one is guiding my dose adjustments and why?",
        "next_steps": "Results are used directly with an institutional heparin dosing nomogram to adjust the infusion rate or next LMWH dose; levels are typically rechecked after each dose adjustment (commonly every 6 hours for UFH) until therapeutic, then monitored periodically or with any change in renal function or bleeding/clotting symptoms.",
        "associated_conditions": [
            {"condition": "Sub-therapeutic anticoagulation (thrombosis risk)", "direction": "below target range"},
            {"condition": "Supra-therapeutic anticoagulation (bleeding risk)", "direction": "above target range, especially >1.0 IU/mL"},
            {"condition": "LMWH accumulation in renal impairment", "direction": "unexpectedly high despite stable dosing"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Anti-Xa Assay (Heparin Assay): Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2085000-overview", "accessed": "2026-07-15"},
            {"name": "MLabs (University of Michigan) - UFH Anti-Xa (test catalog)", "url": "https://mlabs.umich.edu/tests/ufh-anti-xa", "accessed": "2026-07-15"}
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
