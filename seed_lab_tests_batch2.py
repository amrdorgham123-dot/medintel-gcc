"""
Seed script (batch 2) for MedForsa GCC's Lab Info reference library.
Adds 21 more common tests -- electrolytes/extended renal panel, iron studies,
vitamins, and coagulation. English-only content per platform policy.
Sources: MedlinePlus/NIH, Mayo Clinic Labs, StatPearls/NCBI Bookshelf, Medscape/eMedicine.

Run once: python3 seed_lab_tests_batch2.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

MEDLINEPLUS_CMP = {"name": "MedlinePlus (NIH/NLM) - Comprehensive Metabolic Panel", "url": "https://medlineplus.gov/ency/article/003468.htm", "accessed": "2026-07-14"}
MEDLINEPLUS_BMP = {"name": "MedlinePlus (NIH/NLM) - Basic Metabolic Panel", "url": "https://medlineplus.gov/ency/article/003462.htm", "accessed": "2026-07-14"}
MEDSCAPE_LABVALUES = {"name": "Medscape/eMedicine - Lab Values, Normal Adult (reference table)", "url": "https://emedicine.medscape.com/article/2172316-overview", "accessed": "2026-07-14"}

TESTS = [
    {
        "slug": "sodium", "name_en": "Sodium (Na)", "aliases": "Na, Serum Sodium",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses fluid balance, kidney function, and electrolyte status; part of the basic/comprehensive metabolic panel.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Part of routine electrolyte/metabolic panels.",
        "methodology_en": "Ion-selective electrode (ISE) method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Sodium", "population": "Adult", "range": "135-145 mEq/L (135-145 mmol/L)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Hyponatremia (low sodium) may reflect fluid overload, SIADH, heart/liver/kidney failure, or diuretic use, and can cause confusion or seizures if severe/acute. Hypernatremia (high sodium) usually reflects free water loss or deficit (dehydration, diabetes insipidus) and can cause lethargy or seizures. Always interpreted alongside volume status and other electrolytes.",
        "associated_conditions": [
            {"condition": "SIADH / fluid overload / heart failure", "direction": "low"},
            {"condition": "Dehydration / diabetes insipidus", "direction": "high"}
        ],
        "sources": [MEDLINEPLUS_BMP]
    },
    {
        "slug": "potassium", "name_en": "Potassium (K)", "aliases": "K, Serum Potassium",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses electrolyte balance, kidney function, and cardiac/neuromuscular risk; critical value in emergency settings.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Avoid prolonged tourniquet time or hemolysis, which can falsely elevate results.",
        "methodology_en": "Ion-selective electrode (ISE) method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Potassium", "population": "Adult", "range": "3.7-5.2 mEq/L (3.7-5.2 mmol/L)", "notes": "Some labs report 3.5-5.0 mEq/L; always confirm against local range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Hypokalemia (low potassium) can cause muscle weakness and cardiac arrhythmias; common causes include diuretics, vomiting/diarrhea, or inadequate intake. Hyperkalemia (high potassium) is a medical emergency at high levels -- can cause life-threatening cardiac arrhythmias; common causes include renal failure, certain medications (ACE inhibitors, potassium-sparing diuretics), and tissue breakdown.",
        "associated_conditions": [
            {"condition": "Diuretic use / GI losses (vomiting, diarrhea)", "direction": "low"},
            {"condition": "Renal failure / ACE inhibitor or ARB use / tissue breakdown", "direction": "high"}
        ],
        "sources": [MEDLINEPLUS_BMP]
    },
    {
        "slug": "chloride", "name_en": "Chloride (Cl)", "aliases": "Cl, Serum Chloride",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses electrolyte and acid-base balance; usually interpreted together with sodium, bicarbonate, and anion gap.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Ion-selective electrode (ISE) method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Chloride", "population": "Adult", "range": "96-106 mEq/L (96-106 mmol/L)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low chloride can accompany metabolic alkalosis, prolonged vomiting, or SIADH. High chloride can accompany metabolic acidosis (e.g., diarrhea, renal tubular acidosis) or dehydration. Chloride is most useful interpreted alongside sodium, bicarbonate, and the calculated anion gap.",
        "associated_conditions": [
            {"condition": "Metabolic alkalosis / prolonged vomiting", "direction": "low"},
            {"condition": "Non-anion-gap metabolic acidosis / dehydration", "direction": "high"}
        ],
        "sources": [MEDLINEPLUS_BMP]
    },
    {
        "slug": "bicarbonate-co2", "name_en": "Bicarbonate (CO2, Total Carbon Dioxide)", "aliases": "CO2, HCO3, Bicarb, TCO2",
        "category": "Clinical Chemistry",
        "purpose_en": "Reflects the body's acid-base (bicarbonate buffer) status; part of the basic/comprehensive metabolic panel.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Sample should be analyzed promptly, as CO2 can be lost from an exposed sample over time.",
        "methodology_en": "Enzymatic or electrode-based method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Bicarbonate (CO2)", "population": "Adult", "range": "23-29 mEq/L (23-29 mmol/L)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low bicarbonate suggests metabolic acidosis (e.g., diabetic ketoacidosis, renal failure, lactic acidosis, diarrhea) or respiratory compensation for chronic respiratory alkalosis. High bicarbonate suggests metabolic alkalosis (e.g., prolonged vomiting, diuretic use) or renal compensation for chronic respiratory acidosis (e.g., COPD). Best interpreted alongside blood gas analysis when acid-base status is the primary concern.",
        "associated_conditions": [
            {"condition": "Diabetic ketoacidosis / renal failure / lactic acidosis", "direction": "low"},
            {"condition": "Prolonged vomiting / chronic CO2 retention (e.g., COPD)", "direction": "high"}
        ],
        "sources": [MEDLINEPLUS_BMP]
    },
    {
        "slug": "bun", "name_en": "Blood Urea Nitrogen (BUN)", "aliases": "BUN, Urea Nitrogen",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses kidney function and hydration status; used alongside creatinine to evaluate renal function (BUN:creatinine ratio).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No special fasting required; high-protein meals or GI bleeding can transiently raise results.",
        "methodology_en": "Enzymatic (urease-based) method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "BUN", "population": "Adult", "range": "6-20 mg/dL (2.14-7.14 mmol/L)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated BUN suggests reduced kidney filtration, dehydration, high protein intake, or GI bleeding (digested blood raises urea). A BUN:creatinine ratio >20:1 suggests a prerenal cause (dehydration, GI bleed) rather than intrinsic kidney disease. Low BUN may reflect liver disease, malnutrition, or overhydration.",
        "associated_conditions": [
            {"condition": "Dehydration / prerenal azotemia / GI bleeding", "direction": "high, elevated BUN:creatinine ratio"},
            {"condition": "Intrinsic kidney disease", "direction": "high, proportionate rise with creatinine"},
            {"condition": "Liver disease / malnutrition / overhydration", "direction": "low"}
        ],
        "sources": [MEDLINEPLUS_BMP]
    },
    {
        "slug": "calcium", "name_en": "Calcium, Total (Serum)", "aliases": "Ca, Serum Calcium, Total Calcium",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses bone, parathyroid, and kidney health; important in neuromuscular and cardiac function.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Total calcium should be interpreted alongside serum albumin, since roughly 40% of calcium is protein-bound (a 'corrected calcium' calculation is used when albumin is abnormal).",
        "methodology_en": "Colorimetric (e.g., o-cresolphthalein complexone) method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Total calcium", "population": "Adult", "range": "8.5-10.2 mg/dL (2.13-2.55 mmol/L)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Hypercalcemia is most commonly caused by primary hyperparathyroidism or malignancy; symptoms may include fatigue, constipation, kidney stones, and confusion at high levels. Hypocalcemia may be caused by hypoparathyroidism, vitamin D deficiency, or renal failure, and can cause neuromuscular irritability (tingling, muscle cramps, tetany). Always check ionized calcium or corrected calcium (for albumin) when the total calcium result is borderline or albumin is abnormal.",
        "associated_conditions": [
            {"condition": "Primary hyperparathyroidism / malignancy", "direction": "high"},
            {"condition": "Hypoparathyroidism / vitamin D deficiency / renal failure", "direction": "low"}
        ],
        "sources": [MEDLINEPLUS_CMP]
    },
    {
        "slug": "magnesium", "name_en": "Magnesium (Mg)", "aliases": "Mg, Serum Magnesium",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses magnesium status, relevant to neuromuscular, cardiac, and metabolic function; often checked alongside calcium and potassium in unexplained arrhythmia or refractory hypokalemia/hypocalcemia.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No special fasting required.",
        "methodology_en": "Colorimetric method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Serum magnesium", "population": "Adult", "range": "1.7-2.2 mg/dL (0.70-0.91 mmol/L)", "notes": "Serum level reflects only ~1% of total body magnesium and may not detect intracellular depletion"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Hypomagnesemia is associated with alcohol use disorder, GI losses (diarrhea, malabsorption), certain diuretics/proton pump inhibitors, and can cause or worsen refractory hypokalemia and hypocalcemia, as well as cardiac arrhythmias. Hypermagnesemia is uncommon outside renal failure or magnesium supplementation/antacid overuse, and can cause weakness, hypotension, or cardiac conduction abnormalities at high levels.",
        "associated_conditions": [
            {"condition": "Alcohol use disorder / GI losses / diuretic or PPI use", "direction": "low"},
            {"condition": "Renal failure / magnesium supplementation overuse", "direction": "high"}
        ],
        "sources": [{"name": "MedlinePlus (NIH/NLM) - Magnesium Blood Test", "url": "https://medlineplus.gov/ency/article/003487.htm", "accessed": "2026-07-14"}]
    },
    {
        "slug": "phosphorus", "name_en": "Phosphorus (Inorganic Phosphate)", "aliases": "Phosphate, PO4, Serum Phosphorus",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses bone, kidney, and parathyroid-related mineral metabolism; often checked alongside calcium and magnesium.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Morning fasting sample preferred, as phosphorus has diurnal variation and is affected by recent meals.",
        "methodology_en": "Colorimetric (ammonium molybdate) method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Serum phosphorus", "population": "Adult", "range": "2.5-4.5 mg/dL (0.81-1.45 mmol/L)", "notes": "Higher in children; varies modestly across labs"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Hypophosphatemia may occur with refeeding syndrome, hyperparathyroidism, or malnutrition, and severe cases can cause muscle weakness or respiratory failure. Hyperphosphatemia is most often seen in chronic kidney disease (reduced renal excretion) or tumor lysis syndrome, and contributes to secondary hyperparathyroidism and vascular calcification in CKD.",
        "associated_conditions": [
            {"condition": "Refeeding syndrome / hyperparathyroidism / malnutrition", "direction": "low"},
            {"condition": "Chronic kidney disease / tumor lysis syndrome", "direction": "high"}
        ],
        "sources": [{"name": "ScienceDirect - Magnesium and phosphorus (clinical review, adult reference range)", "url": "https://www.sciencedirect.com/science/article/abs/pii/S0140673697105359", "accessed": "2026-07-14"}]
    },
    {
        "slug": "albumin", "name_en": "Albumin, Serum", "aliases": "Serum Albumin",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses liver synthetic function and nutritional/inflammatory status; also affects interpretation of total calcium and drug levels.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Colorimetric (bromocresol green or bromocresol purple dye-binding) method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Serum albumin", "population": "Adult", "range": "3.4-5.4 g/dL (34-54 g/L)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low albumin can reflect chronic liver disease (reduced synthesis), malnutrition, nephrotic syndrome (urinary loss), or acute/chronic inflammation (albumin is a negative acute-phase reactant). It is not a reliable acute marker on its own, since its half-life (~20 days) makes it slow to change. High albumin is uncommon and usually reflects dehydration/hemoconcentration.",
        "associated_conditions": [
            {"condition": "Chronic liver disease", "direction": "low"},
            {"condition": "Nephrotic syndrome (urinary protein loss)", "direction": "low"},
            {"condition": "Malnutrition / chronic inflammation", "direction": "low"},
            {"condition": "Dehydration", "direction": "high (relative hemoconcentration)"}
        ],
        "sources": [MEDLINEPLUS_CMP]
    },
    {
        "slug": "total-bilirubin", "name_en": "Total Bilirubin", "aliases": "Bilirubin, T. Bili",
        "category": "Clinical Chemistry",
        "purpose_en": "Assesses liver function and red blood cell breakdown (hemolysis); part of standard liver function panels.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Fasting preferred but not strictly required; protect sample from light, as bilirubin degrades on exposure.",
        "methodology_en": "Diazo colorimetric method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Total bilirubin", "population": "Adult", "range": "0.1-1.2 mg/dL (2-21 \u00b5mol/L)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated total bilirubin causes jaundice when sufficiently high. Predominantly unconjugated (indirect) elevation suggests hemolysis, ineffective erythropoiesis, or Gilbert syndrome. Predominantly conjugated (direct) elevation suggests hepatocellular or cholestatic (bile duct obstruction) liver disease. Fractionation into direct/indirect bilirubin is needed to distinguish these causes.",
        "associated_conditions": [
            {"condition": "Hemolysis / Gilbert syndrome (unconjugated)", "direction": "high, indirect predominant"},
            {"condition": "Biliary obstruction / cholestatic or hepatocellular liver disease (conjugated)", "direction": "high, direct predominant"}
        ],
        "sources": [MEDLINEPLUS_CMP]
    },
    {
        "slug": "alkaline-phosphatase", "name_en": "Alkaline Phosphatase (ALP)", "aliases": "ALP, Alk Phos",
        "category": "Clinical Chemistry",
        "purpose_en": "Screens for bile duct/liver (cholestatic) disease and bone disorders; part of standard liver function panels.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No special fasting required.",
        "methodology_en": "Enzymatic kinetic assay (IFCC-standardized method) on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Alkaline phosphatase", "population": "Adult", "range": "20-130 U/L (0.33-2.17 \u00b5kat/L)", "notes": "Markedly higher in growing children/adolescents due to bone turnover"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated ALP suggests bile duct obstruction/cholestatic liver disease or a bone disorder with increased osteoblastic activity (e.g., Paget disease, bone metastases, fractures healing). GGT can help distinguish a liver source (GGT also elevated) from a bone source (GGT normal). Physiologically elevated during pregnancy (placental source) and childhood growth.",
        "associated_conditions": [
            {"condition": "Biliary obstruction / cholestatic liver disease", "direction": "high, with elevated GGT"},
            {"condition": "Bone disease (Paget disease, bone metastases, fractures)", "direction": "high, with normal GGT"}
        ],
        "sources": [MEDLINEPLUS_CMP]
    },
    {
        "slug": "ggt", "name_en": "Gamma-Glutamyl Transferase (GGT)", "aliases": "GGT, Gamma-GT",
        "category": "Clinical Chemistry",
        "purpose_en": "Helps determine whether an elevated alkaline phosphatase originates from the liver/biliary tract or from bone; sensitive marker of alcohol use and biliary disease.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No special fasting required.",
        "methodology_en": "Enzymatic kinetic assay on automated chemistry analyzers.",
        "reference_ranges": [
            {"parameter": "GGT", "population": "Adults \u226545 years (both sexes)", "range": "8-38 U/L"},
            {"parameter": "GGT", "population": "Women <45 years", "range": "5-27 U/L"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated GGT is a sensitive marker for biliary tract disease, alcohol-related liver injury, and can be induced by certain medications. Used mainly to confirm a hepatic/biliary source when ALP is elevated (GGT is not made by bone, so a normal GGT with high ALP points to a bone cause instead).",
        "associated_conditions": [
            {"condition": "Biliary disease / cholestasis", "direction": "high"},
            {"condition": "Alcohol-related liver injury / chronic alcohol use", "direction": "high"},
            {"condition": "Medication induction (e.g., anticonvulsants)", "direction": "high"}
        ],
        "sources": [MEDSCAPE_LABVALUES]
    },
    {
        "slug": "uric-acid", "name_en": "Uric Acid, Serum", "aliases": "Serum Urate",
        "category": "Clinical Chemistry",
        "purpose_en": "Diagnoses and monitors gout and evaluates kidney stone risk; also used to monitor tumor lysis syndrome risk during chemotherapy.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Fasting is not strictly required but is often requested alongside other metabolic tests.",
        "methodology_en": "Enzymatic (uricase-based) colorimetric method on automated chemistry analyzers.",
        "reference_ranges": [
            {"parameter": "Uric acid", "population": "Adult male", "range": "4.0-8.5 mg/dL (0.24-0.51 mmol/L)"},
            {"parameter": "Uric acid", "population": "Adult female", "range": "2.7-7.3 mg/dL (0.16-0.43 mmol/L)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated uric acid (hyperuricemia) is associated with gout, kidney stones, and tumor lysis syndrome, though many people with high uric acid never develop gout. Low uric acid is less commonly clinically significant and may be seen with some kidney tubular disorders or overtreatment with urate-lowering therapy.",
        "associated_conditions": [
            {"condition": "Gout", "direction": "high"},
            {"condition": "Uric acid kidney stones", "direction": "high"},
            {"condition": "Tumor lysis syndrome", "direction": "high"}
        ],
        "sources": [MEDSCAPE_LABVALUES]
    },
    {
        "slug": "ferritin", "name_en": "Ferritin, Serum", "aliases": "Serum Ferritin",
        "category": "Clinical Chemistry / Hematology",
        "purpose_en": "Primary marker of the body's iron stores; used to diagnose iron deficiency and iron overload, usually alongside serum iron and TIBC/transferrin saturation.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Ferritin is an acute-phase reactant, so results can be falsely elevated during acute or chronic inflammation/infection.",
        "methodology_en": "Chemiluminescent or electrochemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "Ferritin", "population": "Adult female", "range": "10-150 ng/mL (10-150 \u00b5g/L)"},
            {"parameter": "Ferritin", "population": "Adult male", "range": "12-300 ng/mL (12-300 \u00b5g/L)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low ferritin is a sensitive and specific marker of iron deficiency (in the absence of inflammation). High ferritin may indicate iron overload (hereditary hemochromatosis, transfusion-related) but is also a nonspecific acute-phase reactant that rises with inflammation, infection, liver disease, or malignancy -- so an elevated result must be interpreted alongside CRP/clinical context, not iron status alone.",
        "associated_conditions": [
            {"condition": "Iron deficiency anemia", "direction": "low"},
            {"condition": "Hereditary hemochromatosis / iron overload", "direction": "high"},
            {"condition": "Acute-phase response (infection, inflammation, malignancy)", "direction": "high, non-iron-related"}
        ],
        "sources": [MEDSCAPE_LABVALUES]
    },
    {
        "slug": "total-protein", "name_en": "Total Protein, Serum", "aliases": "Serum Total Protein",
        "category": "Clinical Chemistry",
        "purpose_en": "Screens for liver, kidney, and bone marrow/immunoglobulin disorders; measures the sum of albumin and globulins.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Biuret colorimetric method on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Total protein", "population": "Adult", "range": "6.0-8.3 g/dL (60-83 g/L)"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low total protein may reflect malnutrition, liver disease, nephrotic syndrome, or malabsorption. High total protein may suggest chronic inflammation, dehydration, or a monoclonal gammopathy/multiple myeloma (in which case serum protein electrophoresis is indicated to characterize the globulin fraction).",
        "associated_conditions": [
            {"condition": "Malnutrition / liver disease / nephrotic syndrome", "direction": "low"},
            {"condition": "Multiple myeloma / monoclonal gammopathy / chronic inflammation", "direction": "high"}
        ],
        "sources": [MEDLINEPLUS_CMP]
    },
    {
        "slug": "vitamin-d", "name_en": "Vitamin D, 25-Hydroxy [25(OH)D]", "aliases": "Vitamin D, 25-OH Vitamin D, Calcidiol",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Best indicator of overall vitamin D status (from sun exposure, diet, and supplements); used to evaluate bone health and investigate calcium/PTH abnormalities.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) or LC-MS/MS on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "25(OH)D", "population": "Deficient", "range": "<20 ng/mL (<50 nmol/L)"},
            {"parameter": "25(OH)D", "population": "Insufficient", "range": "20-29 ng/mL (50-72 nmol/L)"},
            {"parameter": "25(OH)D", "population": "Sufficient", "range": "\u226530 ng/mL (\u226575 nmol/L)", "notes": "Thresholds vary by guideline body; some societies use different cutoffs -- see clinical significance"},
            {"parameter": "25(OH)D", "population": "Potential toxicity", "range": ">100 ng/mL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Deficiency is linked to secondary hyperparathyroidism, osteomalacia/rickets, and increased fracture risk. Note that different guideline bodies use different cutoffs -- the widely-cited Endocrine Society thresholds are used here, but the Institute of Medicine/NIH generally considers levels below 20 ng/mL as deficient for the general population without recommending routine universal screening or a specific target above that. Interpret alongside calcium, phosphorus, and PTH when relevant.",
        "associated_conditions": [
            {"condition": "Osteomalacia / rickets / secondary hyperparathyroidism", "direction": "low"},
            {"condition": "Vitamin D toxicity (rare, usually from excessive supplementation)", "direction": "very high, with hypercalcemia"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Vitamin D3 25-Hydroxyvitamin D: Reference Range, Interpretation", "url": "https://emedicine.medscape.com/article/2088694-overview", "accessed": "2026-07-14"},
            {"name": "StatPearls / NCBI Bookshelf - Vitamin D (Endocrine Society guideline thresholds)", "url": "https://www.ncbi.nlm.nih.gov/books/NBK441912/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "vitamin-b12", "name_en": "Vitamin B12 (Cobalamin), Serum", "aliases": "B12, Cobalamin, Serum B12",
        "category": "Immunoassay / Hematology",
        "purpose_en": "Evaluates for B12 deficiency, a cause of megaloblastic anemia and neurologic symptoms (peripheral neuropathy, cognitive changes).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Fasting sample generally preferred; recent B12 injection or high-dose supplementation should be noted, as it can affect results.",
        "methodology_en": "Chemiluminescent or competitive-binding immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "Vitamin B12", "population": "Normal", "range": "200-900 ng/L (pg/mL)", "notes": "Varies by lab/assay"},
            {"parameter": "Vitamin B12", "population": "Deficient", "range": "<150 ng/L"},
            {"parameter": "Vitamin B12", "population": "Borderline", "range": "150-400 ng/L", "notes": "Consider methylmalonic acid (MMA) or homocysteine testing if clinically suspicious despite borderline/normal result"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low B12 causes megaloblastic (macrocytic) anemia and can cause irreversible neurologic damage if untreated (peripheral neuropathy, subacute combined degeneration of the spinal cord). Common causes include pernicious anemia (autoimmune, needs intrinsic factor antibody testing), malabsorption, strict vegan diet, and metformin use. A normal serum B12 does not fully exclude tissue-level deficiency -- methylmalonic acid (MMA) is a more sensitive functional marker when clinical suspicion is high.",
        "associated_conditions": [
            {"condition": "Pernicious anemia / B12 malabsorption / strict vegan diet / metformin use", "direction": "low"}
        ],
        "sources": [
            {"name": "Mayo Clinic Laboratories - Vitamin B12 Assay, Serum (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/Overview/9154", "accessed": "2026-07-14"},
            {"name": "University Hospitals - Vitamin B-12 and Folate patient reference range", "url": "https://www.uhhospitals.org/health-information/health-and-wellness-library/article/lab-tests-v1/vitamin-b12-and-folate", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "folate", "name_en": "Folate (Folic Acid), Serum", "aliases": "Folic Acid, Vitamin B9, Serum Folate",
        "category": "Immunoassay / Hematology",
        "purpose_en": "Evaluates for folate deficiency, a cause of megaloblastic anemia; usually tested alongside vitamin B12.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Ideally an 8-hour fast; recent dietary folate intake can transiently raise serum levels even with normal tissue stores.",
        "methodology_en": "Competitive-binding immunoassay or chemiluminescent assay on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "Serum folate", "population": "Normal", "range": "2-10 ng/mL"},
            {"parameter": "Serum folate", "population": "Suggestive of deficiency", "range": "<4 \u00b5g/L (per Mayo Clinic Laboratories cutoff)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low folate causes megaloblastic (macrocytic) anemia, similar to B12 deficiency, and is linked to neural tube defects in pregnancy when maternal folate is low. Common causes include poor dietary intake, alcohol use disorder, malabsorption, and certain medications (e.g., methotrexate). Serum folate reflects recent intake and can fluctuate; RBC folate is a more stable long-term marker in some clinical settings, though serum folate is generally preferred per Mayo Clinic Laboratories due to less assay variability.",
        "associated_conditions": [
            {"condition": "Poor dietary intake / alcohol use disorder / malabsorption / methotrexate use", "direction": "low"},
            {"condition": "Neural tube defect risk in pregnancy (maternal deficiency)", "direction": "low"}
        ],
        "sources": [
            {"name": "Mayo Clinic Laboratories - Vitamin B12 and Folate, Serum (test catalog)", "url": "https://www.mayocliniclabs.com/test-catalog/overview/9156", "accessed": "2026-07-14"},
            {"name": "University Hospitals - Vitamin B-12 and Folate patient reference range", "url": "https://www.uhhospitals.org/health-information/health-and-wellness-library/article/lab-tests-v1/vitamin-b12-and-folate", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "pt-inr", "name_en": "Prothrombin Time (PT) & INR", "aliases": "PT, INR, International Normalized Ratio",
        "category": "Hematology / Coagulation",
        "purpose_en": "Assesses the extrinsic and common coagulation pathways; used to monitor warfarin therapy, screen for bleeding disorders, and evaluate liver synthetic function/vitamin K status.",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "Tube must be filled to the correct volume for the citrate:blood ratio to be accurate; avoid drawing from a line containing heparin.",
        "methodology_en": "Clot-based (optical or mechanical clot detection) assay on automated coagulation analyzers; INR is calculated from the PT ratio adjusted for reagent sensitivity (ISI).",
        "reference_ranges": [
            {"parameter": "PT", "population": "Adult", "range": "9-13 seconds", "notes": "Lab/reagent-dependent"},
            {"parameter": "INR", "population": "Adult, not anticoagulated", "range": "0.8-1.2"},
            {"parameter": "INR", "population": "Therapeutic target, standard warfarin indication (e.g., AFib)", "range": "2.0-3.0", "notes": "Target varies by indication (e.g., mechanical heart valve targets are higher) -- follow the prescribing indication"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Prolonged PT/INR suggests warfarin effect, vitamin K deficiency, liver disease (reduced clotting factor synthesis), or specific factor deficiencies (factor VII). INR is specifically standardized for monitoring warfarin therapy. A markedly prolonged PT with a normal aPTT suggests an isolated factor VII or extrinsic pathway problem; prolongation of both PT and aPTT suggests a common pathway problem, liver disease, DIC, or vitamin K deficiency.",
        "associated_conditions": [
            {"condition": "Warfarin therapy (expected/monitored effect)", "direction": "high, by design within target range"},
            {"condition": "Liver disease / vitamin K deficiency", "direction": "high"},
            {"condition": "Disseminated intravascular coagulation (DIC)", "direction": "high, with prolonged aPTT too"}
        ],
        "sources": [{"name": "StatPearls / NCBI Bookshelf - Interpretation of Blood Clotting Studies and Values (PT, PTT, aPTT, INR, D-Dimer)", "url": "https://www.ncbi.nlm.nih.gov/books/NBK604215/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "aptt", "name_en": "Activated Partial Thromboplastin Time (aPTT)", "aliases": "PTT, aPTT, Partial Thromboplastin Time",
        "category": "Hematology / Coagulation",
        "purpose_en": "Assesses the intrinsic and common coagulation pathways; used to monitor unfractionated heparin therapy and screen for bleeding disorders/factor deficiencies.",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "Tube must be filled to the correct volume for the citrate:blood ratio to be accurate; avoid drawing from a line containing heparin unless heparin monitoring is the purpose of the test.",
        "methodology_en": "Clot-based (optical or mechanical clot detection) assay on automated coagulation analyzers.",
        "reference_ranges": [{"parameter": "aPTT", "population": "Adult", "range": "25-35 seconds", "notes": "Reagent- and lab-dependent; therapeutic heparin target is typically 1.5-2.5x the lab's control value"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Prolonged aPTT suggests unfractionated heparin effect, hemophilia A/B (factor VIII/IX deficiency), von Willebrand disease, lupus anticoagulant/antiphospholipid antibodies, or other intrinsic-pathway factor deficiencies. Isolated aPTT prolongation with a normal PT points toward the intrinsic pathway (factors VIII, IX, XI, XII) or heparin effect; prolongation of both PT and aPTT suggests a common pathway problem, liver disease, DIC, or vitamin K deficiency.",
        "associated_conditions": [
            {"condition": "Unfractionated heparin therapy (expected/monitored effect)", "direction": "high, by design within target range"},
            {"condition": "Hemophilia A or B", "direction": "high, isolated"},
            {"condition": "Lupus anticoagulant / antiphospholipid syndrome", "direction": "high, isolated, may not correlate with bleeding risk"}
        ],
        "sources": [{"name": "StatPearls / NCBI Bookshelf - Interpretation of Blood Clotting Studies and Values (PT, PTT, aPTT, INR, D-Dimer)", "url": "https://www.ncbi.nlm.nih.gov/books/NBK604215/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "d-dimer", "name_en": "D-Dimer", "aliases": "D-Dimer, Fibrin Degradation Product",
        "category": "Hematology / Coagulation",
        "purpose_en": "Primarily used to help rule out venous thromboembolism (DVT/PE) in patients with low-to-moderate clinical probability; also elevated in DIC.",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "No fasting required. Tube must be filled to the correct volume for accurate results.",
        "methodology_en": "Immunoturbidimetric or ELISA-based assay on automated coagulation analyzers.",
        "reference_ranges": [{"parameter": "D-dimer", "population": "Normal", "range": "<500 ng/mL (FEU)", "notes": "Units and cutoffs vary by assay; age-adjusted cutoffs are commonly used in patients over 50"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "D-dimer has high sensitivity but low specificity for venous thromboembolism (DVT/PE) -- a normal result in a patient with low-to-moderate pretest probability helps rule out VTE, but an elevated result does not confirm it, since D-dimer also rises with surgery, trauma, pregnancy, malignancy, infection, and normal aging. It is a key marker in DIC alongside prolonged PT/aPTT and low platelets/fibrinogen. Always interpreted together with clinical pretest probability scoring (e.g., Wells score).",
        "associated_conditions": [
            {"condition": "Deep vein thrombosis (DVT) / pulmonary embolism (PE)", "direction": "high (sensitive but non-specific)"},
            {"condition": "Disseminated intravascular coagulation (DIC)", "direction": "high, with prolonged PT/aPTT and low fibrinogen/platelets"},
            {"condition": "Recent surgery, trauma, pregnancy, malignancy, infection (non-thrombotic elevation)", "direction": "high, non-specific"}
        ],
        "sources": [{"name": "StatPearls / NCBI Bookshelf - Interpretation of Blood Clotting Studies and Values (PT, PTT, aPTT, INR, D-Dimer)", "url": "https://www.ncbi.nlm.nih.gov/books/NBK604215/", "accessed": "2026-07-14"}]
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
