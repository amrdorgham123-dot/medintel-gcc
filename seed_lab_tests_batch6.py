"""
Seed script (batch 6) for MedForsa GCC's Lab Info reference library.
Adds advanced coagulation, hematology, and cardiovascular risk marker tests.
English-only content per platform policy.

Run once: python3 seed_lab_tests_batch6.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "fibrinogen", "name_en": "Fibrinogen, Plasma",
        "aliases": "Factor I, Clauss Fibrinogen",
        "category": "Hematology / Coagulation",
        "purpose_en": "Assesses the final common pathway of coagulation; used to investigate unexplained bleeding, monitor DIC and massive transfusion/obstetric hemorrhage, and evaluate for congenital fibrinogen disorders.",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "Tube must be filled to the correct volume for the citrate:blood ratio to be accurate.",
        "methodology_en": "Clauss (functional/clot-based) method is the most common; a fibrinogen antigen (immunologic) assay measures total protein regardless of function and is used to distinguish hypo- from dysfibrinogenemia.",
        "reference_ranges": [{"parameter": "Fibrinogen (Clauss/functional)", "population": "Adult", "range": "150-400 mg/dL", "notes": "Some labs report a slightly wider range (e.g., 150-450 mg/dL)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low fibrinogen (<100 mg/dL) is associated with bleeding risk and is seen in DIC, severe liver disease, massive transfusion/dilutional coagulopathy, and rare congenital fibrinogen disorders (afibrinogenemia, hypofibrinogenemia, dysfibrinogenemia). As an acute-phase reactant, fibrinogen rises with inflammation, infection, pregnancy, and malignancy, and elevated levels are also an independent cardiovascular risk marker. In DIC, fibrinogen is monitored serially alongside platelets, D-dimer, and PT/aPTT.",
        "associated_conditions": [
            {"condition": "Disseminated intravascular coagulation (DIC)", "direction": "low, falling trend"},
            {"condition": "Severe liver disease", "direction": "low"},
            {"condition": "Congenital afibrinogenemia/hypofibrinogenemia/dysfibrinogenemia", "direction": "low (or normal antigen with abnormal function in dysfibrinogenemia)"},
            {"condition": "Acute-phase response / inflammation / pregnancy", "direction": "high"}
        ],
        "sources": [{"name": "Medscape/eMedicine - Fibrinogen: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2085501-overview", "accessed": "2026-07-14"}]
    },
    {
        "slug": "antithrombin-iii", "name_en": "Antithrombin III (Antithrombin Activity)",
        "aliases": "AT-III, Antithrombin Activity",
        "category": "Hematology / Coagulation",
        "purpose_en": "Screens for hereditary or acquired antithrombin deficiency as part of a thrombophilia workup, typically after an unprovoked or recurrent venous thromboembolism, especially at a young age or with a positive family history.",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "Testing is ideally deferred until at least 2-6 weeks after an acute thrombotic event and while off anticoagulation (or with awareness that heparin and warfarin can affect results), since acute thrombosis and anticoagulant therapy can transiently lower levels and confound interpretation.",
        "methodology_en": "Chromogenic (functional activity) assay is standard; an antigen (immunologic) assay is used to distinguish Type I (reduced protein and activity) from Type II (normal protein, reduced activity) hereditary deficiency.",
        "reference_ranges": [{"parameter": "Antithrombin activity", "population": "Adult", "range": "80-120%", "notes": "Reference intervals vary by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Hereditary antithrombin deficiency is a rare but strong risk factor for venous thromboembolism, typically presenting with a first clot in early adulthood. Acquired reductions occur with liver disease/cirrhosis, nephrotic syndrome (urinary loss), DIC, acute thrombosis itself (consumption), L-asparaginase therapy, and pregnancy/estrogen use (mild reduction). Antithrombin is also the cofactor for heparin's anticoagulant effect, so severe deficiency can cause apparent heparin resistance.",
        "associated_conditions": [
            {"condition": "Hereditary antithrombin deficiency (venous thromboembolism risk)", "direction": "low"},
            {"condition": "Liver disease / nephrotic syndrome / DIC / acute thrombosis", "direction": "low, acquired"},
            {"condition": "Heparin resistance", "direction": "low, causing reduced heparin effect"}
        ],
        "sources": [{"name": "Medscape/eMedicine - Antithrombin III: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2084978-overview", "accessed": "2026-07-14"}]
    },
    {
        "slug": "protein-c", "name_en": "Protein C Activity",
        "aliases": "Protein C",
        "category": "Hematology / Coagulation",
        "purpose_en": "Screens for hereditary or acquired protein C deficiency as part of a thrombophilia workup; also relevant when starting warfarin, since severe deficiency carries a risk of warfarin-induced skin necrosis.",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "Should not be tested during an acute thrombotic event or while on warfarin (which lowers protein C, a vitamin K-dependent factor) unless interpreted with that context in mind; testing is ideally deferred to a stable, non-anticoagulated state when possible.",
        "methodology_en": "Chromogenic or clot-based (functional activity) assay on automated coagulation analyzers.",
        "reference_ranges": [{"parameter": "Protein C activity", "population": "Adult", "range": "70-140%", "notes": "Reference intervals vary by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Protein C is a natural anticoagulant that, together with protein S, inactivates factors Va and VIIIa. Hereditary deficiency increases venous thromboembolism risk. Acquired reductions occur with warfarin therapy, liver disease, DIC, and vitamin K deficiency. Because protein C has a short half-life, starting warfarin without concurrent heparin bridging in a patient with protein C deficiency can transiently create a hypercoagulable state, causing warfarin-induced skin necrosis -- a key reason protein C status is considered before/during warfarin initiation in high-risk patients.",
        "associated_conditions": [
            {"condition": "Hereditary protein C deficiency (venous thromboembolism risk)", "direction": "low"},
            {"condition": "Warfarin-induced skin necrosis risk", "direction": "low, especially if warfarin started without heparin bridging"},
            {"condition": "Liver disease / vitamin K deficiency / DIC", "direction": "low, acquired"}
        ],
        "sources": [{"name": "PMC - High prevalence of protein C, protein S, antithrombin deficiency, and Factor V Leiden mutation as a cause of hereditary thrombophilia", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4320724/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "protein-s", "name_en": "Protein S (Free Antigen or Activity)",
        "aliases": "Protein S",
        "category": "Hematology / Coagulation",
        "purpose_en": "Screens for hereditary or acquired protein S deficiency as part of a thrombophilia workup, usually alongside protein C and antithrombin.",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "Same timing caveats as protein C -- avoid testing during acute thrombosis, pregnancy, estrogen/oral contraceptive use, or warfarin therapy when possible, as all of these lower protein S levels.",
        "methodology_en": "Free protein S antigen (immunologic, measuring the active unbound fraction) or a functional clot-based activity assay.",
        "reference_ranges": [
            {"parameter": "Free protein S", "population": "Adult male", "range": "75-145%", "notes": "Reference intervals vary by lab/method"},
            {"parameter": "Free protein S", "population": "Adult female", "range": "55-125%", "notes": "Lower than males; further reduced by pregnancy and estrogen use"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Protein S is a cofactor for protein C's anticoagulant activity; hereditary deficiency increases venous thromboembolism risk, similar to protein C deficiency. Levels are physiologically lower in women, and further reduced by pregnancy, estrogen-containing contraceptives/hormone therapy, warfarin, liver disease, DIC, and nephrotic syndrome (urinary loss) -- all of which must be considered before diagnosing a hereditary deficiency from a single low result.",
        "associated_conditions": [
            {"condition": "Hereditary protein S deficiency (venous thromboembolism risk)", "direction": "low"},
            {"condition": "Pregnancy / estrogen therapy / oral contraceptive use", "direction": "low, physiologic/acquired"},
            {"condition": "Warfarin therapy / liver disease / nephrotic syndrome", "direction": "low, acquired"}
        ],
        "sources": [{"name": "PMC - High prevalence of protein C, protein S, antithrombin deficiency, and Factor V Leiden mutation as a cause of hereditary thrombophilia", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4320724/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "reticulocyte-count", "name_en": "Reticulocyte Count",
        "aliases": "Retic Count, Reticulocytes",
        "category": "Hematology",
        "purpose_en": "Assesses bone marrow's red blood cell production activity; used to classify anemia (production vs. destruction/loss) and to monitor marrow recovery after treatment (e.g., chemotherapy, iron/B12 replacement, bone marrow transplant).",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "No fasting required. Best interpreted alongside hemoglobin/hematocrit, since the raw percentage can be misleadingly elevated in anemia -- a corrected reticulocyte count or reticulocyte production index should be used when anemia is present.",
        "methodology_en": "Automated flow cytometry with fluorescent RNA-binding dyes (e.g., thiazole orange) on hematology analyzers, or manual microscopic counting with supravital staining (e.g., new methylene blue).",
        "reference_ranges": [
            {"parameter": "Reticulocyte percentage", "population": "Adult, non-anemic", "range": "0.5%-2.5%"},
            {"parameter": "Absolute reticulocyte count", "population": "Adult", "range": "~25,000-75,000/\u00b5L", "notes": "Some sources cite up to 100,000/\u00b5L as the upper limit"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A high (corrected) reticulocyte count in the setting of anemia indicates an appropriate marrow response to blood loss or hemolysis (e.g., hemolytic anemia, acute bleeding, or recovery phase after treatment). A low or inappropriately normal reticulocyte count in the setting of anemia suggests decreased marrow production, as seen in iron/B12/folate deficiency, chronic kidney disease (reduced erythropoietin), marrow infiltration by malignancy, or marrow failure syndromes. The reticulocyte production index (RPI), which corrects for both anemia severity and reticulocyte maturation time, is the most reliable way to interpret the result when hematocrit is reduced.",
        "associated_conditions": [
            {"condition": "Hemolytic anemia / acute blood loss / marrow recovery", "direction": "high (appropriate marrow response)"},
            {"condition": "Iron, B12, or folate deficiency anemia", "direction": "low or inappropriately normal for degree of anemia"},
            {"condition": "Chronic kidney disease / marrow failure / marrow infiltration", "direction": "low"}
        ],
        "sources": [
            {"name": "MedlinePlus (NIH/NLM) - Reticulocyte count", "url": "https://medlineplus.gov/ency/article/003637.htm", "accessed": "2026-07-14"},
            {"name": "Medscape/eMedicine - Reticulocyte Count and Reticulocyte Hemoglobin Content: Reference Range", "url": "https://emedicine.medscape.com/article/2086146-overview", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "g6pd", "name_en": "Glucose-6-Phosphate Dehydrogenase (G6PD) Screen",
        "aliases": "G6PD, G6PD Deficiency Screen",
        "category": "Hematology",
        "purpose_en": "Screens for G6PD deficiency, an X-linked enzyme deficiency that predisposes red blood cells to oxidative hemolysis; used to investigate unexplained hemolytic anemia and before prescribing certain oxidant drugs (e.g., some antimalarials, dapsone, sulfonamides) in at-risk populations.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "Testing during or shortly after an acute hemolytic episode can give a falsely normal result, because the oldest (most deficient) red cells have already been destroyed and young cells/reticulocytes have relatively higher enzyme activity -- retesting several weeks after recovery is recommended if an acute-phase result is normal but suspicion remains high.",
        "methodology_en": "Quantitative spectrophotometric enzyme activity assay (reference method) or qualitative/semi-quantitative point-of-care fluorescent spot tests used for rapid screening.",
        "reference_ranges": [{"parameter": "G6PD activity", "population": "Normal", "range": "Approximately 7-11 IU/g Hb", "notes": "Reference range and deficient/intermediate cutoffs vary by assay and are typically expressed relative to a population median; a result below 80% of the lower limit of normal is generally considered deficient"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Deficient G6PD activity predisposes to acute hemolytic episodes triggered by oxidative stressors -- classically fava beans (favism), certain infections, and oxidant medications (some antimalarials such as primaquine, sulfonamides, dapsone, nitrofurantoin). Because G6PD is X-linked, deficiency is more common and typically more severe in males; heterozygous females can have intermediate activity due to random X-inactivation (mosaicism) and may be missed by qualitative screening tests, sometimes requiring quantitative testing or genetic confirmation.",
        "associated_conditions": [
            {"condition": "Favism / drug-induced oxidative hemolysis", "direction": "low activity (deficient)"},
            {"condition": "Neonatal hyperbilirubinemia risk", "direction": "low activity (deficient), in affected newborns"}
        ],
        "sources": [{"name": "ScienceDirect - Glucose-6-phosphate dehydrogenase deficiency (clinical review)", "url": "https://www.sciencedirect.com/science/article/pii/S0006497120617190", "accessed": "2026-07-14"}]
    },
    {
        "slug": "homocysteine", "name_en": "Homocysteine, Total, Plasma",
        "aliases": "Homocysteine, tHcy",
        "category": "Clinical Chemistry / Cardiac Biomarkers",
        "purpose_en": "Evaluates for vitamin B12/folate deficiency (functional marker, elevated even when serum B12 is borderline-normal) and is used as a secondary cardiovascular risk marker.",
        "specimen_type": "Venous plasma (EDTA tube, kept on ice and processed promptly)",
        "collection_notes_en": "Ideally fasting; the sample should be centrifuged and separated promptly (or kept on ice) since homocysteine continues to be released from blood cells after collection, which can falsely raise results if processing is delayed.",
        "methodology_en": "Immunoassay or HPLC/LC-MS/MS on automated analyzers.",
        "reference_ranges": [{"parameter": "Total homocysteine", "population": "Adult", "range": "Approximately 5-15 \u00b5mol/L", "notes": "Reference ranges vary by lab/assay and rise with age and reduced kidney function"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated homocysteine (hyperhomocysteinemia) is most commonly caused by vitamin B12, folate, or B6 deficiency, reduced kidney function, hypothyroidism, or certain medications; it is also seen in the rare inherited disorder homocystinuria. It is an independent, though modest, cardiovascular risk marker and has been studied in combination with elevated Lp(a) for synergistic cardiovascular risk, though homocysteine-lowering therapy (B-vitamin supplementation) has not been shown to reduce cardiovascular events in most large trials, limiting its use as a routine risk-modifying target.",
        "associated_conditions": [
            {"condition": "Vitamin B12 or folate deficiency", "direction": "high"},
            {"condition": "Chronic kidney disease", "direction": "high"},
            {"condition": "Homocystinuria (rare inherited disorder)", "direction": "markedly high"},
            {"condition": "Cardiovascular risk (modest, independent marker)", "direction": "high"}
        ],
        "sources": [{"name": "Kang et al., Arteriosclerosis, Thrombosis, and Vascular Biology (AHA Journals) - Homocysteine and Lipoprotein(a) Interact to Increase CAD Risk", "url": "https://www.ahajournals.org/doi/10.1161/01.atv.20.2.493", "accessed": "2026-07-14"}]
    },
    {
        "slug": "lipoprotein-a", "name_en": "Lipoprotein(a) [Lp(a)]",
        "aliases": "Lp(a), Lipoprotein a",
        "category": "Clinical Chemistry / Cardiac Biomarkers",
        "purpose_en": "Independent, largely genetically-determined cardiovascular risk marker; major cardiology societies now recommend measuring it at least once in a person's lifetime to refine atherosclerotic cardiovascular disease (ASCVD) risk assessment.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Fasting is not required. Because Lp(a) is genetically determined and stays relatively stable over a lifetime, a single measurement is generally considered sufficient (repeat testing is not usually needed).",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay; results may be reported in mg/dL (mass) or nmol/L (particle concentration) -- these units are not directly interconvertible due to variation in particle size between individuals, so the reporting unit should always be noted.",
        "reference_ranges": [
            {"parameter": "Lp(a)", "population": "Lower risk", "range": "<30 mg/dL (approximately <75 nmol/L)"},
            {"parameter": "Lp(a)", "population": "Elevated / increased risk", "range": "\u226530-50 mg/dL (approximately \u226575-125 nmol/L)", "notes": "Thresholds vary slightly by society (EAS, ACC/AHA, NLA); risk is highest in the top 5-10% of the population"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated Lp(a) is an independent, causal risk factor for atherosclerotic cardiovascular disease (coronary artery disease, stroke, peripheral artery disease) and calcific aortic valve stenosis, and is not reliably lowered by standard lifestyle changes or statins. It is used to refine risk in patients with intermediate calculated ASCVD risk or a strong family history of early cardiovascular disease out of proportion to standard risk factors, prompting more aggressive management of other modifiable risk factors (e.g., LDL/ApoB targets) even though Lp(a)-specific therapies are still emerging.",
        "associated_conditions": [
            {"condition": "Premature/familial atherosclerotic cardiovascular disease", "direction": "high"},
            {"condition": "Calcific aortic valve stenosis", "direction": "high"}
        ],
        "sources": [{"name": "Medscape/eMedicine - Lipoprotein (a): Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2088118-overview", "accessed": "2026-07-14"}]
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
             associated_conditions_json, sources_json, is_published)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (t["slug"], t["name_en"], "", t.get("aliases"), t["category"],
             t.get("purpose_en"), None, t.get("specimen_type"),
             t.get("collection_notes_en"), None,
             t.get("methodology_en"), None,
             json.dumps(t.get("reference_ranges", [])), int(t.get("reference_ranges_verified", False)),
             t.get("clinical_significance_en"), None,
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
