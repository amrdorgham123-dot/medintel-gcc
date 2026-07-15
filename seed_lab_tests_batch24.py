"""
Seed script (batch 24) for MedForsa GCC's Lab Info reference library.
Adds 9 tests: Serum Protein Electrophoresis, Serum Free Light Chains,
Plasma Free Metanephrines, Chromogranin A, Fasting Serum Gastrin, 5-HIAA,
ENA Antibody Panel, Cold Agglutinin Titer, Cryoglobulins.

Run once: python3 seed_lab_tests_batch24.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "spep", "name_en": "Serum Protein Electrophoresis (SPEP)",
        "aliases": "SPEP, Protein Electrophoresis, M-Spike",
        "category": "Clinical Chemistry",
        "purpose_en": "Screens for monoclonal gammopathies (multiple myeloma, MGUS, Waldenstrom macroglobulinemia, AL amyloidosis) and evaluates unexplained findings such as anemia, hypercalcemia, renal impairment, bone pain, or elevated total protein/globulin gap.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. If a monoclonal band (M-spike) is detected, reflex immunofixation electrophoresis (IFE) is typically performed to identify the specific immunoglobulin class and light chain type.",
        "methodology_en": "Gel or capillary zone electrophoresis separates serum proteins by charge into fractions (albumin, alpha-1, alpha-2, beta, gamma), producing a densitometric tracing; a discrete narrow spike (M-spike), usually in the gamma or beta region, indicates a monoclonal protein.",
        "reference_ranges": [{"parameter": "SPEP", "population": "Normal", "range": "No monoclonal (M) protein band detected; polyclonal gamma fraction pattern", "notes": "Individual fraction reference ranges (albumin, globulins) vary by lab"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A monoclonal (M-spike) band indicates clonal proliferation of a single plasma cell or lymphocyte line producing identical immunoglobulin, seen across a spectrum from monoclonal gammopathy of undetermined significance (MGUS, the most common finding, often incidental and non-progressive) to smoldering or active multiple myeloma, Waldenstrom macroglobulinemia, and AL amyloidosis. SPEP is used per International Myeloma Working Group guidelines for baseline diagnosis and disease monitoring when the M-protein is measurable (\u22651 g/dL); when not measurable, serum free light chain testing is used instead. SPEP alone cannot identify the specific immunoglobulin type -- immunofixation electrophoresis is required for that.",
        "associated_conditions": [
            {"condition": "Monoclonal gammopathy of undetermined significance (MGUS)", "direction": "small M-spike, no other myeloma-defining features"},
            {"condition": "Multiple myeloma", "direction": "M-spike, often with anemia, hypercalcemia, renal impairment, bone lesions"},
            {"condition": "Waldenstrom macroglobulinemia / AL amyloidosis", "direction": "M-spike, with disease-specific features"}
        ],
        "sources": [{"name": "Inciteful Med - Myeloma Lab Results: M-Spike & Light Chains Guide", "url": "https://incitefulmed.com/resources/guides/multiple-myeloma-patient-guide/multiple-myeloma-lab-results/", "accessed": "2026-07-15"}]
    },
    {
        "slug": "serum-free-light-chains", "name_en": "Serum Free Light Chains (Kappa/Lambda Ratio)",
        "aliases": "sFLC, Free Kappa, Free Lambda, FLC Ratio",
        "category": "Clinical Chemistry / Tumor Markers",
        "purpose_en": "Ordered alongside SPEP in the workup of suspected monoclonal gammopathy; particularly valuable for oligosecretory or non-secretory myeloma, light chain-only myeloma, and AL amyloidosis, where SPEP alone may be falsely negative.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Renal impairment can elevate both free light chains and shift the ratio, so results should be interpreted with kidney function in mind.",
        "methodology_en": "Immunonephelometric or immunoturbidimetric assay using antisera specific to free (unbound) kappa and lambda light chains, distinct from the light chains bound within intact immunoglobulins.",
        "reference_ranges": [
            {"parameter": "Free kappa light chain", "population": "Adult", "range": "~0.33-1.94 mg/dL"},
            {"parameter": "Free lambda light chain", "population": "Adult", "range": "~0.57-2.63 mg/dL"},
            {"parameter": "Kappa/lambda ratio", "population": "Adult, normal renal function", "range": "0.26-1.65", "notes": "Widened reference range (approximately 0.37-3.1) is used in patients with renal failure, since reduced clearance raises both light chains"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "An abnormal kappa/lambda ratio with one light chain elevated out of proportion to the other supports a monoclonal free light chain-producing process and, combined with SPEP/IFE, supports diagnosis of a plasma cell disorder. When both free light chains are elevated but the ratio stays normal or only mildly increased, this more often reflects polyclonal elevation from renal impairment or chronic inflammation rather than a monoclonal process. The involved light chain and the sFLC ratio are used by the International Myeloma Working Group for diagnosis, risk stratification, and response assessment (a normalized ratio is required to document a stringent complete response), and sFLC monitoring is the preferred method for light chain-only or non-secretory disease.",
        "associated_conditions": [
            {"condition": "Light chain multiple myeloma / oligosecretory or non-secretory myeloma", "direction": "abnormal kappa/lambda ratio, disproportionate elevation of one light chain"},
            {"condition": "AL amyloidosis", "direction": "abnormal ratio, often with a modestly elevated involved light chain"},
            {"condition": "Renal impairment / chronic inflammation (polyclonal elevation)", "direction": "both light chains elevated, ratio normal or only mildly increased"}
        ],
        "sources": [
            {"name": "ARUP Consult - Kappa/Lambda Quantitative Free Light Chain With Ratio, Serum", "url": "https://arupconsult.com/ati/kappalambda-quantitative-free-light-chain-ratio-serum", "accessed": "2026-07-15"},
            {"name": "myADLM - Serum Free Light Chains (Optimal Testing Guide)", "url": "https://myadlm.org/advocacy-and-outreach/optimal-testing-guide-to-lab-test-utilization/g-s/serum-free-light-chains", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "metanephrines-plasma-free", "name_en": "Metanephrines, Fractionated, Plasma Free",
        "aliases": "Plasma Free Metanephrines, Metanephrine, Normetanephrine",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "First-line screening test for pheochromocytoma and paraganglioma (catecholamine-secreting tumors), used in patients with suggestive symptoms (episodic headache, palpitations, sweating, hypertension) or an incidentally found adrenal mass.",
        "specimen_type": "Venous plasma, drawn after the patient has been supine/resting for at least 20-30 minutes",
        "collection_notes_en": "Blood should be drawn from a seated or, preferably, supine patient after a period of rest, since upright posture and stress/anxiety during the draw can cause false-positive elevations; many interfering medications (tricyclic antidepressants, some psychiatric drugs) should be discussed with the ordering clinician beforehand when possible.",
        "methodology_en": "Liquid chromatography-tandem mass spectrometry (LC-MS/MS), the preferred modern method for specificity, or immunoassay/HPLC with electrochemical detection.",
        "reference_ranges": [{"parameter": "Normetanephrine and metanephrine", "population": "Adult, supine sample", "range": "Age-adjusted upper cutoffs (normetanephrine cutoff rises from ~0.47 nmol/L in children to ~1.05 nmol/L in adults over 60)", "notes": "Reference intervals are method- and age-specific; always use the reporting lab's own cutoffs"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Normal plasma free metanephrines (in a properly collected supine sample) have very high negative predictive value, essentially ruling out a catecholamine-secreting tumor. An elevation three-fold or more above the upper cutoff is rarely a false positive and should prompt imaging to localize the tumor; borderline elevations (less than three-fold) are more often false positives from stress, posture, or medication interference, and are typically followed up with a repeat supine sample, 24-hour urinary fractionated metanephrines, or a clonidine suppression test before proceeding to imaging.",
        "associated_conditions": [
            {"condition": "Pheochromocytoma / paraganglioma", "direction": "high, especially \u22653x upper cutoff"},
            {"condition": "False-positive elevation from posture, stress, or interfering medications", "direction": "mildly high, typically <3x upper cutoff"}
        ],
        "questions_to_ask_en": "Was my sample drawn in the correct (supine/resting) position, since that affects accuracy? If borderline, do I need repeat testing or a confirmatory test before imaging? Are any of my current medications known to interfere with this test?",
        "next_steps": "A markedly elevated result (typically \u22653x the upper cutoff) prompts imaging (CT or MRI of the adrenal glands/abdomen, sometimes functional imaging) to localize the tumor. A borderline result is usually repeated under optimal (supine, rested) conditions, or confirmed with 24-hour urinary fractionated metanephrines or a clonidine suppression test, before imaging is pursued.",
        "sources": [
            {"name": "Labcorp - Metanephrines, Fractionated, Plasma Free (test description)", "url": "https://www.labcorp.com/tests/121806/metanephrines-fractionated-plasma-free", "accessed": "2026-07-15"},
            {"name": "PMC - Reference intervals for plasma free metanephrines with an age adjustment for normetanephrine", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4714582/", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "chromogranin-a", "name_en": "Chromogranin A, Plasma/Serum",
        "aliases": "CgA, Chromogranin A",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "General marker for neuroendocrine tumors, used as a complementary test to plasma metanephrines in pheochromocytoma/paraganglioma workup, and as a marker for carcinoid tumors, gastroenteropancreatic neuroendocrine tumors, and to monitor treatment response.",
        "specimen_type": "Venous plasma or serum, per assay requirements",
        "collection_notes_en": "Proton pump inhibitors (PPIs) can significantly raise chromogranin A independent of tumor activity by causing reactive hypergastrinemia -- ideally stopped for 1-2 weeks before testing when feasible, per assay-specific guidance.",
        "methodology_en": "Immunoradiometric assay (IRMA) or enzyme-linked immunoassay.",
        "reference_ranges": [{"parameter": "Chromogranin A", "population": "Normal (assay-dependent)", "range": "Commonly cited cutoff around 150 \u00b5g/L in one validated assay", "notes": "Reference ranges vary substantially between assay platforms -- always use the reporting lab's own cutoff"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated chromogranin A supports the presence of a neuroendocrine tumor (pheochromocytoma, paraganglioma, carcinoid, gastroenteropancreatic neuroendocrine tumors, some pituitary tumors), with sensitivity around 82-90% depending on tumor type in published series, and can be the only abnormal circulating marker in a minority of cases where metanephrines/catecholamines are normal. It has lower specificity than plasma metanephrines for pheochromocytoma specifically, since PPI use, atrophic gastritis, renal impairment, and other conditions with increased adrenergic activity can also raise it -- making it most useful as a complementary follow-up test rather than a first-line screen for catecholamine-secreting tumors.",
        "associated_conditions": [
            {"condition": "Neuroendocrine tumors (pheochromocytoma, paraganglioma, carcinoid, GEP-NETs)", "direction": "high"},
            {"condition": "PPI use / atrophic gastritis / renal impairment (non-tumor cause of elevation)", "direction": "high, non-specific"}
        ],
        "sources": [{"name": "PMC - Chromogranin A in the Laboratory Diagnosis of Pheochromocytoma and Paraganglioma", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6521298/", "accessed": "2026-07-15"}]
    },
    {
        "slug": "gastrin", "name_en": "Fasting Serum Gastrin",
        "aliases": "Gastrin, Fasting Gastrin",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Primary screening test for Zollinger-Ellison syndrome (gastrinoma), evaluated in patients with refractory or recurrent peptic ulcer disease, unexplained chronic diarrhea, or multiple endocrine neoplasia type 1 (MEN1).",
        "specimen_type": "Venous serum, fasting (at least 8-12 hours)",
        "collection_notes_en": "Proton pump inhibitors and H2 blockers must be stopped before testing (commonly 6 days for PPIs, 1 day for H2 blockers, per institutional protocol) since they cause reactive hypergastrinemia that can mimic or mask true gastrinoma; the sample should be drawn fasting and processed/frozen promptly.",
        "methodology_en": "Chemiluminescent or radioimmunoassay.",
        "reference_ranges": [{"parameter": "Fasting serum gastrin", "population": "Normal", "range": "Approximately 15-100 pg/mL (commonly cited upper limit up to 150 pg/mL)", "notes": "Reference range varies by lab/assay"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A fasting gastrin above 10 times the upper limit of normal (roughly >1,000 pg/mL) in a patient with gastric acid hypersecretion is considered virtually diagnostic of Zollinger-Ellison syndrome without further testing. However, two-thirds of confirmed gastrinoma patients have levels less than 10-fold the upper limit, which overlaps considerably with more common causes of hypergastrinemia -- most importantly proton pump inhibitor use, but also H. pylori infection, atrophic gastritis, pernicious anemia, renal failure, and prior gastric surgery -- so a secretin stimulation test is often needed to confirm the diagnosis when gastrin is only modestly elevated.",
        "associated_conditions": [
            {"condition": "Zollinger-Ellison syndrome (gastrinoma)", "direction": "high, especially >1,000 pg/mL with acid hypersecretion"},
            {"condition": "Proton pump inhibitor use / H. pylori infection / atrophic gastritis (non-tumor causes)", "direction": "mild-moderate high, overlapping with mild gastrinoma elevations"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Gastrinoma Workup: Laboratory Studies", "url": "https://emedicine.medscape.com/article/184332-workup", "accessed": "2026-07-15"},
            {"name": "Labcorp - Gastrin (test description)", "url": "https://www.labcorp.com/tests/004390/gastrin", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "5-hiaa", "name_en": "5-Hydroxyindoleacetic Acid (5-HIAA)",
        "aliases": "5-HIAA, Urine 5-HIAA, Serotonin Metabolite",
        "category": "Clinical Chemistry / Tumor Markers",
        "purpose_en": "Confirms carcinoid syndrome in patients with a neuroendocrine tumor and compatible symptoms (flushing, diarrhea, wheezing), and can be used to monitor disease activity and treatment response.",
        "specimen_type": "24-hour urine collection (traditional standard) or venous serum (newer alternative)",
        "collection_notes_en": "For urine testing, dietary restriction of serotonin-rich foods (bananas, tomatoes, avocados, walnuts, pineapple) and certain medications for 2-3 days before and during collection is traditionally recommended to avoid false elevation, though this requirement is being reconsidered with modern mass spectrometry methods; serum 5-HIAA avoids the need for a 24-hour collection and dietary restriction.",
        "methodology_en": "High-performance liquid chromatography (HPLC) or liquid chromatography-tandem mass spectrometry (LC-MS/MS).",
        "reference_ranges": [{"parameter": "Serum 5-HIAA", "population": "Optimal cutoff (peer-reviewed study)", "range": "139.4 nmol/L (sensitivity 96.3%, specificity 87.6% for carcinoid syndrome in SSA-naive patients)", "notes": "24-hour urine 5-HIAA reference ranges and units differ by lab; serum and urine results correlate well (r=0.892) but are not directly interchangeable"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated 5-HIAA, a breakdown product of serotonin, supports carcinoid syndrome in a patient with a known or suspected neuroendocrine tumor, and correlates with the presence of flushing, diarrhea, and carcinoid heart disease -- each 100 nmol/L rise in serum 5-HIAA is associated with modestly increased odds of these symptoms. Serial 5-HIAA is used to monitor disease activity and response to somatostatin analog therapy. False elevation can occur from dietary serotonin intake (in urine testing) or certain medications, so results should be interpreted alongside diet/medication history.",
        "associated_conditions": [
            {"condition": "Carcinoid syndrome (from a serotonin-secreting neuroendocrine tumor)", "direction": "high, correlates with flushing/diarrhea/carcinoid heart disease"}
        ],
        "sources": [{"name": "PMC - Serum 5-Hydroxyindoleacetic Acid Measurements for the Diagnosis and Follow-up of Carcinoid Syndrome", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12623023/", "accessed": "2026-07-15"}]
    },
    {
        "slug": "ena-panel", "name_en": "Extractable Nuclear Antigen (ENA) Antibody Panel",
        "aliases": "ENA Panel, Anti-Ro/SSA, Anti-La/SSB, Anti-Sm, Anti-RNP",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Reflex panel ordered after a positive ANA to identify specific autoantibodies that help diagnose and subtype connective tissue diseases -- Sjogren's syndrome (Anti-Ro/SSA, Anti-La/SSB), systemic lupus erythematosus (Anti-Sm, Anti-Ro/SSA), and mixed connective tissue disease (Anti-RNP).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Typically ordered as a reflex panel after a positive ANA screen with a compatible clinical picture, rather than as an isolated first-line test.",
        "methodology_en": "Solid-phase immunoassay (chemiluminescent or ELISA) or multiplex bead-based assay, detecting IgG antibodies against specific nuclear/cytoplasmic antigens (Ro/SSA, La/SSB, Sm, RNP, Scl-70, Jo-1, and others depending on the panel).",
        "reference_ranges": [{"parameter": "ENA panel components (Ro/SSA, La/SSB, Sm, RNP)", "population": "Result categories", "range": "Negative or Positive, commonly reported with a titer/unit value against an assay-specific cutoff (e.g., >10 U/mL positive on some platforms)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Anti-Ro/SSA and Anti-La/SSB antibodies are found in roughly 60-75% of primary Sjogren's syndrome cases and about 50% (Ro) of SLE cases, and Anti-Ro/SSA is specifically associated with photosensitivity, subacute cutaneous lupus, neonatal lupus, and congenital heart block risk in pregnancy. Anti-Sm antibodies are highly specific for SLE (found in only 5-30% of cases but rarely in other conditions), making a positive result strong supportive evidence when clinical suspicion exists, though titer does not correlate with disease activity. Anti-RNP antibodies are the defining serologic feature of mixed connective tissue disease (found in the large majority of cases) and are also seen in a minority of SLE cases. Isolated Anti-La/SSB without Anti-Ro/SSA has low positive predictive value for Sjogren's syndrome on its own.",
        "associated_conditions": [
            {"condition": "Sjogren's syndrome", "direction": "positive Anti-Ro/SSA and/or Anti-La/SSB"},
            {"condition": "Systemic lupus erythematosus", "direction": "positive Anti-Sm (highly specific) and/or Anti-Ro/SSA"},
            {"condition": "Mixed connective tissue disease", "direction": "positive Anti-RNP, often high titer"},
            {"condition": "Neonatal lupus / congenital heart block risk (maternal Anti-Ro/SSA)", "direction": "positive Anti-Ro/SSA in a pregnant patient"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Anti-Ro Antibody: Reference Range, Interpretation", "url": "https://emedicine.medscape.com/article/2086660-overview", "accessed": "2026-07-15"},
            {"name": "The Rheumatologist - Know Your Labs (ACR-referenced antibody prevalence data)", "url": "https://www.the-rheumatologist.org/article/know-your-labs/?singlepage=1", "accessed": "2026-07-15"},
            {"name": "Mayo Clinic Laboratories - SS-A and SS-B Antibodies, IgG, Serum (test catalog)", "url": "https://neurology.testcatalog.org/show/SSAB", "accessed": "2026-07-15"}
        ]
    },
    {
        "slug": "cold-agglutinin-titer", "name_en": "Cold Agglutinin Titer",
        "aliases": "Cold Agglutinins, CA Titer",
        "category": "Hematology",
        "purpose_en": "Diagnoses cold agglutinin disease and investigates cold-related hemolytic anemia; also relevant preoperatively before planned intraoperative hypothermia, since clinically significant cold agglutinins can cause dangerous red cell agglutination during cooling.",
        "specimen_type": "Venous whole blood, drawn into a pre-warmed tube and kept warm (37\u00b0C) until the serum is separated",
        "collection_notes_en": "The specimen must be kept warm from collection through serum separation, since cold agglutinins can bind to red cells and be lost from the serum (falsely lowering the titer) if the sample is allowed to cool before processing -- a critical and unique preanalytical requirement for this test.",
        "methodology_en": "Serial dilutions of patient serum are mixed with reagent red cells and tested for agglutination at 4\u00b0C (and often also at 30\u00b0C and 37\u00b0C to assess thermal amplitude); the titer is the reciprocal of the highest dilution still showing agglutination.",
        "reference_ranges": [{"parameter": "Cold agglutinin titer at 4\u00b0C", "population": "Normal/non-pathogenic", "range": "<1:64", "notes": "Low-titer, low-thermal-amplitude cold agglutinins occur in a small percentage of the healthy population without hemolysis"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A titer \u22651:64 at 4\u00b0C is considered abnormal, and cold agglutinin disease is typically associated with much higher titers (often >1:10,000) with a thermal amplitude reaching up to 30-32\u00b0C or higher, meaning the antibody remains active closer to body temperature and can cause clinically significant hemolysis and cold-induced symptoms (acrocyanosis, Raynaud-like phenomena). Thermal amplitude, not titer alone, best predicts clinical significance -- a high-titer cold agglutinin that only reacts at very low temperatures (4\u00b0C) may be less clinically relevant than a lower-titer one that reacts up to near-body temperature. Causes include primary cold agglutinin disease, Mycoplasma pneumoniae or EBV infection (typically transient, lower titer), and lymphoproliferative disorders (e.g., Waldenstrom macroglobulinemia, CLL).",
        "associated_conditions": [
            {"condition": "Primary cold agglutinin disease", "direction": "very high titer (often >1:10,000), high thermal amplitude"},
            {"condition": "Mycoplasma pneumoniae or EBV infection (secondary, usually transient)", "direction": "moderately elevated titer"},
            {"condition": "Lymphoproliferative disorders (Waldenstrom macroglobulinemia, CLL)", "direction": "elevated titer, often monoclonal IgM"}
        ],
        "sources": [{"name": "Medscape/eMedicine - Cold Agglutinin Disease Workup", "url": "https://emedicine.medscape.com/article/135327-workup", "accessed": "2026-07-15"}]
    },
    {
        "slug": "cryoglobulins", "name_en": "Cryoglobulins",
        "aliases": "Cryoglobulin Screen",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Investigates suspected cryoglobulinemia in patients with purpura, arthralgia, peripheral neuropathy, or glomerulonephritis, particularly in the context of hepatitis C infection, lymphoproliferative disorders, or autoimmune disease (e.g., Sjogren's syndrome).",
        "specimen_type": "Venous whole blood, drawn into a pre-warmed tube and kept at 37\u00b0C during transport and clotting, then refrigerated at 4\u00b0C to allow cryoprecipitation",
        "collection_notes_en": "Strict temperature control is essential and easily gets this test wrong: the sample must be kept warm (37\u00b0C) from the moment of collection through clot formation and serum separation, since cryoglobulins will precipitate prematurely at room or cold temperature and be lost from the serum before ever reaching the cold incubation step used to detect them.",
        "methodology_en": "Serum is incubated at 4\u00b0C for up to 7 days and observed for precipitate (cryoprecipitate) formation; if present, the precipitate is redissolved by warming and characterized by immunofixation to classify the cryoglobulin type (Type I monoclonal, Type II mixed monoclonal-polyclonal, Type III mixed polyclonal).",
        "reference_ranges": [{"parameter": "Cryoglobulins", "population": "Normal", "range": "Negative (no cryoprecipitate) or Not detected", "notes": "When present in low concentration, cryoglobulins exist alongside vastly larger concentrations of normal serum proteins, making the test technically demanding"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Type I cryoglobulinemia (a single monoclonal immunoglobulin) is associated with lymphoproliferative disorders such as Waldenstrom macroglobulinemia and multiple myeloma. Type II and III (mixed cryoglobulinemia, involving both monoclonal and/or polyclonal components with rheumatoid factor activity) are most strongly associated with chronic hepatitis C infection, and also occur in autoimmune diseases (Sjogren's syndrome, SLE) and some lymphoproliferative disorders. Clinical manifestations of mixed cryoglobulinemia include palpable purpura, arthralgia, peripheral neuropathy, and membranoproliferative glomerulonephritis, resulting from immune complex deposition in small vessels.",
        "associated_conditions": [
            {"condition": "Chronic hepatitis C infection (mixed cryoglobulinemia)", "direction": "positive, Type II/III"},
            {"condition": "Waldenstrom macroglobulinemia / multiple myeloma", "direction": "positive, Type I (monoclonal)"},
            {"condition": "Sjogren's syndrome / SLE (secondary mixed cryoglobulinemia)", "direction": "positive, Type II/III"}
        ],
        "sources": [{"name": "Annals of Clinical & Laboratory Science - Cryoglobulins: An Important but Neglected Clinical Test", "url": "https://www.annclinlabsci.org/content/36/4/395.full", "accessed": "2026-07-15"}]
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
