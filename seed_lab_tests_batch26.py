"""
Seed script (batch 26) for MedForsa GCC's Lab Info reference library.
Adds Digoxin Level, Lithium Level, Factor V Leiden, Prothrombin G20210A,
ADAMTS13 Activity, Vitamin K, and Stool Culture.

Run once: python3 seed_lab_tests_batch26.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "digoxin-level", "name_en": "Digoxin, Serum (Therapeutic Drug Monitoring)",
        "aliases": "Digoxin Level, Digitalis Level",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Monitors digoxin therapy in heart failure and atrial fibrillation, confirms medication adherence, and investigates suspected digoxin toxicity, given its narrow therapeutic index.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Blood should be drawn at least 6-8 hours after the last oral dose (trough level, just before the next dose) -- levels drawn earlier will be falsely elevated due to the drug's distribution pattern, since blood levels don't yet reflect tissue equilibration.",
        "methodology_en": "Chemiluminescent or fluorescence polarization immunoassay on automated analyzers.",
        "reference_ranges": [{"parameter": "Digoxin", "population": "Conventional therapeutic range", "range": "0.8-2.0 ng/mL", "notes": "Contemporary evidence and updated recommendations increasingly favor a lower target of 0.5-1.0 ng/mL for heart failure, since higher levels within the older 'therapeutic' range are associated with increased morbidity and mortality without added benefit -- many labs and references have not yet fully adopted this lower target"}],
        "reference_ranges_verified": True,
        "critical_values_en": "A level >2.4 ng/mL is generally considered toxic, though roughly 10% of patients can show toxicity symptoms even below 2.0 ng/mL, particularly in the presence of hypokalemia, hypomagnesemia, hypoxia, underlying heart disease, or hypercalcemia -- toxicity should be assessed clinically, not by level alone.",
        "interfering_factors_en": "Drawing the sample too soon after a dose (before 6-8 hours) falsely elevates the result, since digoxin has not yet fully distributed from blood into tissue. Low potassium, low magnesium, and impaired kidney function (which reduces digoxin clearance) all increase the risk of toxicity at a given level.",
        "questions_to_ask_en": "Was this sample drawn at the correct time relative to my last dose? Given contemporary evidence, should my target level be lower than the traditional range? Are my kidney function and electrolytes being checked alongside this, since they affect my risk of toxicity?",
        "next_steps": "A subtherapeutic level may prompt a dose increase (after checking for adherence and correct timing of the draw); a level above target, especially with symptoms of toxicity (nausea, visual changes, arrhythmias), prompts dose reduction or holding the medication, correction of contributing electrolyte abnormalities, and in severe toxicity, digoxin-specific antibody fragments (Fab).",
        "sources": [
            {"name": "Medscape/eMedicine - Digoxin Level: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2089975-overview", "accessed": "2026-07-15"},
            {"name": "PMC - Failure of current digoxin monitoring for toxicity: new monitoring recommendations", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10350506/", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "lithium-level", "name_en": "Lithium, Serum (Therapeutic Drug Monitoring)",
        "aliases": "Lithium Level",
        "category": "Clinical Chemistry / Therapeutic Drug Monitoring",
        "purpose_en": "Monitors lithium therapy for bipolar disorder to maintain therapeutic efficacy while avoiding toxicity, given its narrow therapeutic index; also used to investigate suspected toxicity.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Blood should be drawn approximately 12 hours after the last dose (trough level, typically a morning draw after an evening dose) for standardized, comparable results between visits.",
        "methodology_en": "Ion-selective electrode or atomic absorption spectrophotometry on automated analyzers.",
        "reference_ranges": [{"parameter": "Lithium", "population": "Maintenance therapeutic range", "range": "Approximately 0.6-1.2 mEq/L", "notes": "Target range varies by clinical indication and prescriber's treatment plan -- follow local/institutional guidance"}],
        "reference_ranges_verified": True,
        "critical_values_en": "Toxicity risk rises substantially above the therapeutic range, and levels can rise unexpectedly due to dehydration or low sodium (lithium excretion tracks with sodium/water balance) even without a dose change -- any signs of toxicity (tremor, confusion, ataxia, vomiting) warrant urgent level checking regardless of the last known result.",
        "interfering_factors_en": "Dehydration, low-sodium diets, and certain medications (thiazide diuretics, NSAIDs, ACE inhibitors) can raise lithium levels by reducing renal excretion, sometimes causing toxicity even without a dose increase. Drawing the sample too soon after a dose (before reaching steady state or before the appropriate trough timing) can give a misleading result.",
        "questions_to_ask_en": "Was this drawn at the right time (about 12 hours post-dose)? Could dehydration, a new medication, or my kidney function be affecting this level? How often should this be monitored going forward, and is my thyroid and kidney function also being checked periodically?",
        "next_steps": "A subtherapeutic level with inadequate response may prompt a dose increase; a level above the therapeutic range prompts dose reduction and review of factors that may have raised it. Since lithium can affect the kidneys and thyroid over time, periodic monitoring of both is typically done alongside lithium levels.",
        "sources": [
            {"name": "GoodNurse - Therapeutic Drug Levels: Vancomycin, Digoxin, Lithium - Monitoring, Toxicity", "url": "https://goodnurse.com/article/208/therapeutic-drug-levels-2026-vancomycin-digoxin-lithium-monitoring-toxicity-teaching", "accessed": "2026-07-15"},
            {"name": "PMC - Overview of Therapeutic Drug Monitoring", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC2687654/", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "factor-v-leiden", "name_en": "Factor V Leiden Mutation Testing",
        "aliases": "Factor V Leiden, FVL, Activated Protein C Resistance",
        "category": "Hematology / Coagulation",
        "purpose_en": "Identifies the most common inherited thrombophilia, evaluated in patients with unprovoked or recurrent venous thromboembolism, VTE at a young age, VTE with a strong family history, or recurrent pregnancy loss.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "Can be tested at any time, including during acute thrombosis or while on anticoagulation, since this is a DNA-based test and not affected by current clotting status (unlike protein C, protein S, or antithrombin levels).",
        "methodology_en": "PCR-based DNA testing detects the specific G1691A mutation in the factor V gene; a functional activated protein C (APC) resistance assay can be used as an initial screen, with genetic testing to confirm.",
        "reference_ranges": [{"parameter": "Factor V Leiden mutation", "population": "Result categories", "range": "Not detected (wild-type), Heterozygous, or Homozygous -- a genetic result, not a numeric value; prevalence varies substantially by ethnicity (e.g., ~4-7% in Northern/Southern Europeans, 7.5% in some Middle Eastern populations, rare in East Asian and African populations)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Heterozygous Factor V Leiden increases venous thromboembolism risk roughly 3-8 fold; homozygous carriers have a substantially higher risk (estimates vary, often cited around 20-fold or more). The mutation causes resistance to inactivation by activated protein C, leading to a hypercoagulable state. Risk is further amplified by additional factors such as estrogen-containing contraceptives, pregnancy, surgery, and immobility. It is also associated with certain obstetric complications (recurrent miscarriage, preeclampsia) though the strength of this association remains debated in the literature.",
        "associated_conditions": [
            {"condition": "Venous thromboembolism (DVT/PE) risk", "direction": "positive, heterozygous or homozygous"},
            {"condition": "Recurrent pregnancy loss / preeclampsia (debated association)", "direction": "positive"}
        ],
        "questions_to_ask_en": "Given this result, what precautions should I take during pregnancy, surgery, or long flights? Does this affect my choice of contraception or hormone therapy? Do family members need to be tested?",
        "next_steps": "A positive result leads to a discussion of risk-reduction strategies (avoiding estrogen-containing contraceptives, prophylactic anticoagulation around high-risk situations like surgery or pregnancy) rather than routine long-term anticoagulation in someone who hasn't had a clot, and family testing may be offered given the hereditary nature of this mutation.",
        "sources": [
            {"name": "PMC - Factor V Leiden G1691A and Prothrombin Gene G20210A Mutations on Pregnancy Outcome (prevalence data)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8439407/", "accessed": "2026-07-15"},
            {"name": "Testing.com - Factor 5 Leiden Mutation Test: Purpose and Results", "url": "https://www.testing.com/tests/factor-v-leiden-mutation-and-pt-20210-mutation/", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "prothrombin-g20210a", "name_en": "Prothrombin G20210A Mutation Testing",
        "aliases": "Prothrombin Gene Mutation, Factor II Mutation",
        "category": "Hematology / Coagulation",
        "purpose_en": "Identifies the second most common inherited thrombophilia after Factor V Leiden, evaluated as part of the same thrombophilia workup for unprovoked or recurrent venous thromboembolism, especially at a young age or with a family history.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "Can be tested at any time, including during acute thrombosis or while on anticoagulation, since this is a DNA-based test unaffected by current clotting status.",
        "methodology_en": "PCR-based DNA testing detects the specific G20210A mutation in the prothrombin (factor II) gene, which increases prothrombin production and clotting activity.",
        "reference_ranges": [{"parameter": "Prothrombin G20210A mutation", "population": "Result categories", "range": "Not detected (wild-type), Heterozygous, or Homozygous -- a genetic result; overall population prevalence is approximately 2%, higher in some European populations"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "This gain-of-function mutation increases thrombin and fibrin generation, raising venous thromboembolism risk (heterozygous carriers have an estimated 2-3 fold increased risk, similar in magnitude to Factor V Leiden). It is often tested alongside Factor V Leiden as part of a standard thrombophilia panel, and the combination of both mutations together (or with other risk factors) substantially increases risk beyond either alone.",
        "associated_conditions": [
            {"condition": "Venous thromboembolism (DVT/PE) risk", "direction": "positive, heterozygous or homozygous"},
            {"condition": "Combined thrombophilia (with Factor V Leiden or other risk factors)", "direction": "positive, compounding risk"}
        ],
        "questions_to_ask_en": "Does this change my risk during pregnancy, surgery, or with hormone-based contraception? Should I be on prophylactic blood thinners in high-risk situations even without a prior clot? Do my family members need testing?",
        "next_steps": "As with Factor V Leiden, a positive result leads to counseling on situational risk reduction (avoiding estrogen-based contraceptives, prophylactic anticoagulation around surgery/pregnancy) rather than automatic long-term anticoagulation without a prior clot, guided by hematology.",
        "sources": [
            {"name": "World Thrombosis Day - Thrombophilia Testing and MTHFR", "url": "https://www.worldthrombosisday.org/thrombophilia-testing-and-mthfr/", "accessed": "2026-07-15"},
            {"name": "PubMed - Testing for Factor V Leiden (FVL) and Prothrombin G20210A Genetic Variants", "url": "https://pubmed.ncbi.nlm.nih.gov/37204714/", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "adamts13-activity", "name_en": "ADAMTS13 Activity",
        "aliases": "ADAMTS13, vWF-Cleaving Protease Activity",
        "category": "Hematology / Coagulation",
        "purpose_en": "Confirms or excludes thrombotic thrombocytopenic purpura (TTP) in patients presenting with microangiopathic hemolytic anemia and thrombocytopenia, distinguishing TTP from other thrombotic microangiopathies (like hemolytic uremic syndrome) that require different treatment.",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top) -- EDTA tubes are not acceptable, as EDTA strongly inhibits ADAMTS13 function",
        "collection_notes_en": "Should be drawn before starting plasma exchange therapy whenever possible, since plasma exchange will alter results; specimens must not be hemolyzed, clotted, or heparin-contaminated.",
        "methodology_en": "Functional activity assay (e.g., FRET-based cleavage of a synthetic vWF substrate), often combined with antigen level and inhibitor (autoantibody) testing when activity is low.",
        "reference_ranges": [{"parameter": "ADAMTS13 activity", "population": "Normal", "range": "Approximately 60-130 IU/dL (methods vary)"}],
        "reference_ranges_verified": True,
        "critical_values_en": "Severe deficiency (<10 IU/dL, some labs use <10%) is considered diagnostic of TTP in the appropriate clinical context and is treated as a critical, actionable result requiring urgent plasma exchange therapy.",
        "interfering_factors_en": "High bilirubin (>15-30 mg/dL depending on the assay), significant hemolysis (free hemoglobin >2 g/dL), hyperlipidemia, and high endogenous von Willebrand factor can all interfere with the activity assay -- results should be interpreted with awareness of these confounders, particularly in critically ill patients with multiple abnormalities.",
        "questions_to_ask_en": "Does this confirm TTP as the cause of my low platelets and anemia, or point to a different cause (like HUS or DIC)? If severely deficient, is this from an autoantibody or a genetic cause? How quickly does treatment need to start?",
        "next_steps": "A severely deficient result in a compatible clinical picture confirms TTP and prompts urgent plasma exchange therapy, typically started even before the result is finalized if clinical suspicion is high, given how quickly untreated TTP can become life-threatening. A normal or only mildly reduced result makes TTP less likely and prompts investigation of other causes.",
        "associated_conditions": [
            {"condition": "Thrombotic thrombocytopenic purpura (TTP)", "direction": "severely low, typically <10 IU/dL"},
            {"condition": "Congenital TTP (Upshaw-Schulman syndrome)", "direction": "severely low from birth, without inhibitory antibody"}
        ],
        "sources": [
            {"name": "Practical Haemostasis - ADAMTS13 Assays", "url": "https://practical-haemostasis.com/Miscellaneous/adamts13_assays.html", "accessed": "2026-07-15"},
            {"name": "MLabs (University of Michigan) - ADAMTS-13 Activity (test catalog)", "url": "https://mlabs.umich.edu/tests/adamts-13-activity", "accessed": "2026-07-15"},
            {"name": "myADLM - The Role of ADAMTS13 Testing in the Work up of Suspected TTP", "url": "https://myadlm.org/cln/articles/2016/april/the-role-of-adamts13-testing-in-the-work-up-of-suspected-thrombotic-thrombocytopenic-purpura", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "vitamin-k", "name_en": "Vitamin K1 (Phylloquinone), Serum",
        "aliases": "Vitamin K, Phylloquinone",
        "category": "Clinical Chemistry",
        "purpose_en": "Evaluates suspected vitamin K deficiency, particularly in patients with unexplained bleeding/bruising, malabsorption (e.g., cystic fibrosis, cholestatic liver disease), or prolonged PT/INR not explained by warfarin use.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Fasting sample is generally preferred, since recent dietary intake of vitamin K-rich foods (leafy greens, certain oils) can transiently raise levels.",
        "methodology_en": "High-performance liquid chromatography (HPLC) or LC-MS/MS, given the very low circulating concentrations involved.",
        "reference_ranges": [{"parameter": "Vitamin K1 (phylloquinone)", "population": "Adult, general reference", "range": "Approximately 0.2-3.0 ng/mL", "notes": "Reference ranges vary meaningfully by population, age, and laboratory method -- functional markers (like PIVKA-II or PT) are often used alongside or instead of direct vitamin K level measurement, since direct testing is not widely standardized"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low vitamin K impairs the liver's ability to produce functional clotting factors II, VII, IX, and X, leading to a prolonged PT/INR and bleeding risk -- this is why vitamin K deficiency is a key differential when PT/INR is elevated in someone not on warfarin. Causes include malabsorption syndromes (celiac disease, cystic fibrosis, cholestatic liver disease), prolonged antibiotic use (which reduces gut bacterial vitamin K production), and inadequate dietary intake. In practice, functional testing (PT/INR response to vitamin K administration, or PIVKA-II) is often used to assess vitamin K status rather than direct serum level measurement, since direct assays are less standardized and widely available.",
        "associated_conditions": [
            {"condition": "Malabsorption syndromes (celiac disease, cystic fibrosis, cholestatic liver disease)", "direction": "low"},
            {"condition": "Prolonged broad-spectrum antibiotic use", "direction": "low, from reduced gut bacterial synthesis"},
            {"condition": "Unexplained bleeding / prolonged PT-INR (not on warfarin)", "direction": "low, contributing cause"}
        ],
        "sources": [
            {"name": "PMC - Reference Range of Vitamin K Evaluating Indicators in Chinese Childbearing Women", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10143736/", "accessed": "2026-07-15"},
            {"name": "PMC - Preliminary study on the reference intervals of vitamin K in a normal physical examination population (Beijing)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11811856/", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "stool-culture", "name_en": "Stool Culture",
        "aliases": "Stool C&S, Enteric Pathogen Culture",
        "category": "Microbiology",
        "purpose_en": "Identifies bacterial pathogens causing infectious diarrhea/gastroenteritis (e.g., Salmonella, Shigella, Campylobacter, pathogenic E. coli), used in patients with severe, bloody, or persistent diarrhea, or during suspected outbreaks.",
        "specimen_type": "Fresh stool sample, collected in a sterile container (or rectal swab in some settings)",
        "collection_notes_en": "Sample should be transported and processed promptly, or placed in appropriate transport media, since some enteric pathogens are fragile and can die off or be overgrown by normal flora if the sample is delayed.",
        "methodology_en": "Selective and differential culture media targeting specific enteric pathogens, since normal stool flora (anaerobes, gram-negative enterics, Enterococcus) is abundant and would otherwise overwhelm a non-selective culture; molecular (PCR panel) methods are increasingly used alongside or instead of culture for faster, broader pathogen detection.",
        "reference_ranges": [{"parameter": "Stool culture", "population": "Normal", "range": "No pathogenic organisms isolated (normal flora only) -- growth of a specific enteric pathogen (Salmonella, Shigella, Campylobacter, etc.) is a positive/reportable result"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Identification of a specific enteric pathogen guides targeted antibiotic therapy (when indicated -- many bacterial gastroenteritis cases are self-limited and don't require antibiotics) and, for reportable organisms like Salmonella and Shigella, triggers public health reporting to monitor for outbreaks. A negative culture in someone with persistent symptoms may prompt additional testing (stool PCR panel, ova and parasites, C. difficile toxin testing) since culture alone doesn't detect all causes of infectious diarrhea (viruses, parasites, and some bacteria are not reliably identified by standard culture).",
        "associated_conditions": [
            {"condition": "Bacterial gastroenteritis (Salmonella, Shigella, Campylobacter, pathogenic E. coli)", "direction": "positive, specific pathogen identified"},
            {"condition": "Traveler's diarrhea", "direction": "positive, commonly enterotoxigenic E. coli in many regions"}
        ],
        "questions_to_ask_en": "Does this identify what's causing my symptoms? Do I need antibiotics, or will this resolve on its own? Is this a reportable infection, and do I need to take precautions to avoid spreading it to others?",
        "next_steps": "A positive result for a specific pathogen guides whether antibiotics are needed (many cases don't require them) and any public health reporting/isolation precautions required for that organism. A negative result with ongoing symptoms often leads to additional testing (PCR panel, parasite testing, or C. difficile testing depending on your history).",
        "sources": [{"name": "Medscape/eMedicine - Stool Culture: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2107038-overview", "accessed": "2026-07-15"}]
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
             json.dumps(t.get("associated_conditions", [])), json.dumps(t.get("sources", [])),
             1)
        )
        print(f"INSERTED: {t['slug']} ({t['name_en']})")
        inserted += 1
    conn.commit()
    conn.close()
    print(f"\nDone. Inserted: {inserted}, Skipped (already existed): {skipped}")

if __name__ == "__main__":
    main()
