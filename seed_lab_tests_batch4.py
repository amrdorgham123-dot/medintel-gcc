"""
Seed script (batch 4) for MedForsa GCC's Lab Info reference library.
Adds 23 more tests across cardiac biomarkers, autoimmune/inflammation, endocrinology,
extended iron studies, tumor markers, transfusion-transmitted infection screening,
pancreatic enzymes, pregnancy, and urinalysis. English-only content per platform policy.

Run once: python3 seed_lab_tests_batch4.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "free-t4", "name_en": "Free Thyroxine (Free T4)", "aliases": "FT4, Free T4",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Measures the unbound, biologically active fraction of thyroxine; used with TSH to diagnose and monitor thyroid disorders, especially when pituitary/central causes are suspected or TSH results are discordant with symptoms.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Automated immunoassay (competitive analog immunoassay); equilibrium dialysis is used as a reference method when binding-protein abnormalities are suspected to interfere with routine assays.",
        "reference_ranges": [{"parameter": "Free T4", "population": "Adult", "range": "0.8-1.8 ng/dL", "notes": "Assay-dependent; some labs report 0.8-1.7 or 0.9-1.7 ng/dL"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low free T4 with high TSH indicates primary hypothyroidism; low free T4 with low/inappropriately normal TSH suggests central (pituitary/hypothalamic) hypothyroidism. High free T4 with low TSH indicates hyperthyroidism. Certain medications (e.g., phenytoin, heparin) and non-thyroidal illness can cause artifactually abnormal free T4 on routine immunoassays -- equilibrium dialysis is more accurate in these situations.",
        "associated_conditions": [
            {"condition": "Primary hypothyroidism", "direction": "low, with high TSH"},
            {"condition": "Central (pituitary) hypothyroidism", "direction": "low, with low/normal TSH"},
            {"condition": "Hyperthyroidism", "direction": "high, with low TSH"}
        ],
        "sources": [{"name": "Mayo Clinic Laboratories - T4 (Thyroxine), Free, Dialysis, Serum (test catalog)", "url": "https://endocrinology.testcatalog.org/show/FRT4D", "accessed": "2026-07-14"}]
    },
    {
        "slug": "free-t3", "name_en": "Free Triiodothyronine (Free T3)", "aliases": "FT3, Free T3",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Measures the unbound, active fraction of triiodothyronine; used mainly to help diagnose hyperthyroidism (including T3 toxicosis, where T3 is elevated but T4 is normal) or when TSH/free T4 do not fully explain symptoms.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Automated competitive immunoassay on immunoassay analyzers.",
        "reference_ranges": [{"parameter": "Free T3", "population": "Adult", "range": "2.3-4.2 pg/mL", "notes": "Assay-dependent; some labs report 2.0-4.4 pg/mL"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated free T3 with a suppressed TSH supports hyperthyroidism, including T3 toxicosis (isolated T3 elevation with normal T4, seen especially in early Graves disease or toxic nodules). Low free T3 can occur in hypothyroidism, but is also commonly seen in non-thyroidal illness ('euthyroid sick syndrome') where TSH and free T4 may be normal -- so free T3 alone is not routinely used to diagnose hypothyroidism.",
        "associated_conditions": [
            {"condition": "Hyperthyroidism / T3 toxicosis", "direction": "high"},
            {"condition": "Non-thyroidal illness (euthyroid sick syndrome)", "direction": "low, without primary thyroid disease"}
        ],
        "sources": [{"name": "Testing.com - Thyroid Test Results Chart (reference ranges compiled from lab reports)", "url": "https://www.testing.com/thyroid-testing-example-results/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "pth", "name_en": "Parathyroid Hormone, Intact (PTH)", "aliases": "PTH, Intact PTH, Parathormone",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Assesses parathyroid gland function; used to investigate abnormal calcium levels and diagnose primary, secondary, or tertiary hyperparathyroidism, and hypoparathyroidism.",
        "specimen_type": "Venous serum or plasma (EDTA plasma preferred by some assays for stability)",
        "collection_notes_en": "Best interpreted alongside a simultaneously-drawn calcium (ideally ionized calcium) and vitamin D level; morning fasting sample often preferred due to diurnal variation.",
        "methodology_en": "Second- or third-generation immunoassay (chemiluminescent) detecting intact PTH molecule on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "Intact PTH", "population": "Adult, normal calcium and vitamin D status", "range": "15-65 pg/mL", "notes": "Assay-dependent; some labs report 10-65 pg/mL. Must be interpreted alongside simultaneous calcium level"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "PTH must always be interpreted together with the calcium level: high PTH with high calcium suggests primary hyperparathyroidism; high PTH with low/normal calcium suggests secondary hyperparathyroidism (commonly from vitamin D deficiency or chronic kidney disease); low PTH with high calcium suggests a non-parathyroid cause of hypercalcemia (e.g., malignancy); low PTH with low calcium suggests hypoparathyroidism.",
        "associated_conditions": [
            {"condition": "Primary hyperparathyroidism", "direction": "high PTH, high calcium"},
            {"condition": "Secondary hyperparathyroidism (vitamin D deficiency, CKD)", "direction": "high PTH, low/normal calcium"},
            {"condition": "Hypoparathyroidism", "direction": "low PTH, low calcium"},
            {"condition": "Malignancy-associated hypercalcemia (PTH-independent)", "direction": "low/suppressed PTH, high calcium"}
        ],
        "sources": [{"name": "Cleveland Clinic - Parathyroid Hormone: What It Is, Function & Normal Levels", "url": "https://my.clevelandclinic.org/health/articles/22355-parathyroid-hormone", "accessed": "2026-07-14"}]
    },
    {
        "slug": "cortisol", "name_en": "Cortisol, Serum (AM)", "aliases": "Cortisol, Morning Cortisol",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Assesses adrenal (HPA axis) function; used to investigate suspected adrenal insufficiency (Addison disease) or Cushing syndrome.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Cortisol has strong diurnal variation (highest in early morning, lowest at night), so timing of the draw (typically 7-9 AM) must be specified and matched against the appropriate reference range; stress, illness, and exogenous steroid use affect results.",
        "methodology_en": "Chemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "Cortisol", "population": "Adult, 8 AM specimen", "range": "5-23 \u00b5g/dL", "notes": "Reference range is specific to morning collection; afternoon/evening levels are normally lower"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A low morning cortisol raises concern for adrenal insufficiency and typically prompts an ACTH stimulation test to confirm. A high cortisol, especially if it fails to suppress with a dexamethasone suppression test, raises concern for Cushing syndrome. Random single cortisol values are of limited use without knowing the time of day and the clinical context (acute illness/stress physiologically raises cortisol).",
        "associated_conditions": [
            {"condition": "Adrenal insufficiency (Addison disease, or secondary to pituitary/steroid withdrawal)", "direction": "low"},
            {"condition": "Cushing syndrome (endogenous or exogenous steroid excess)", "direction": "high, loss of normal diurnal variation"}
        ],
        "sources": [{"name": "NBME Laboratory Reference Values (academic reference table, 0800h cortisol)", "url": "https://www.nbme.org/sites/default/files/2025-03/NBME_Laboratory_Reference_Values.pdf", "accessed": "2026-07-14"}]
    },
    {
        "slug": "serum-iron", "name_en": "Iron, Serum", "aliases": "Serum Iron, Fe",
        "category": "Clinical Chemistry / Hematology",
        "purpose_en": "Measures iron currently circulating in the blood bound to transferrin; part of a full iron panel alongside ferritin, TIBC, and transferrin saturation to evaluate iron deficiency or overload.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Morning fasting sample preferred, since serum iron has diurnal variation (higher in the morning, lower in the afternoon/evening) and is affected by recent iron intake/supplementation.",
        "methodology_en": "Colorimetric method on automated chemistry analyzers.",
        "reference_ranges": [
            {"parameter": "Serum iron", "population": "Adult male", "range": "59-158 \u00b5g/dL (10.6-28.3 \u00b5mol/L)"},
            {"parameter": "Serum iron", "population": "Adult female", "range": "37-145 \u00b5g/dL (6.6-25.9 \u00b5mol/L)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Serum iron alone is not reliable for diagnosing iron deficiency or overload because of its wide diurnal swing and sensitivity to recent intake -- it is always interpreted together with TIBC/transferrin saturation and ferritin. Low serum iron with high TIBC and low saturation suggests iron deficiency; low serum iron with low/normal TIBC suggests anemia of chronic disease/inflammation instead. High serum iron with high saturation suggests iron overload (e.g., hereditary hemochromatosis).",
        "associated_conditions": [
            {"condition": "Iron deficiency (with high TIBC, low saturation)", "direction": "low"},
            {"condition": "Anemia of chronic disease/inflammation (with low/normal TIBC)", "direction": "low"},
            {"condition": "Hereditary hemochromatosis / iron overload", "direction": "high, with high saturation"}
        ],
        "sources": [{"name": "MedlinePlus (NIH/NLM) - Serum Iron Test", "url": "https://medlineplus.gov/ency/article/003488.htm", "accessed": "2026-07-14"}]
    },
    {
        "slug": "tibc-transferrin-saturation", "name_en": "TIBC & Transferrin Saturation", "aliases": "Total Iron-Binding Capacity, TIBC, Transferrin Saturation, TSAT",
        "category": "Clinical Chemistry / Hematology",
        "purpose_en": "Measures the blood's total capacity to bind iron (TIBC, a reflection of transferrin level) and the percentage of that capacity currently occupied by iron (transferrin saturation); used together with serum iron and ferritin to distinguish iron deficiency from other causes of anemia or from iron overload.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Should be drawn alongside serum iron, ideally as a fasting morning sample, since transferrin saturation is calculated from both values.",
        "methodology_en": "TIBC measured colorimetrically after saturating the sample with excess iron; transferrin saturation is calculated as (serum iron / TIBC) x 100.",
        "reference_ranges": [
            {"parameter": "TIBC", "population": "Adult male", "range": "171-505 \u00b5g/dL (30.6-90.3 \u00b5mol/L)"},
            {"parameter": "TIBC", "population": "Adult female", "range": "149-492 \u00b5g/dL (26.7-88.0 \u00b5mol/L)"},
            {"parameter": "Transferrin saturation", "population": "Adult male", "range": "20-50%"},
            {"parameter": "Transferrin saturation", "population": "Adult female", "range": "15-45%"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "In uncomplicated iron deficiency, TIBC (transferrin) rises while transferrin saturation falls. In anemia of chronic disease, TIBC is typically low-to-normal while saturation is low-to-normal (a pattern that helps distinguish it from true iron deficiency). A transferrin saturation above roughly 45-50% raises concern for iron overload (e.g., hereditary hemochromatosis) and often prompts genetic testing (HFE gene) and ferritin correlation.",
        "associated_conditions": [
            {"condition": "Iron deficiency anemia", "direction": "high TIBC, low saturation"},
            {"condition": "Anemia of chronic disease/inflammation", "direction": "low/normal TIBC, low/normal saturation"},
            {"condition": "Hereditary hemochromatosis / iron overload", "direction": "saturation >45-50%"}
        ],
        "sources": [{"name": "MedlinePlus (NIH/NLM) - Serum Iron Test (includes TIBC and saturation)", "url": "https://medlineplus.gov/ency/article/003488.htm", "accessed": "2026-07-14"}]
    },
    {
        "slug": "esr", "name_en": "Erythrocyte Sedimentation Rate (ESR)", "aliases": "ESR, Sed Rate",
        "category": "Hematology / Inflammation Markers",
        "purpose_en": "Non-specific marker of inflammation; used to support diagnosis and monitor disease activity in inflammatory and rheumatologic conditions (e.g., polymyalgia rheumatica, giant cell arteritis, rheumatoid arthritis), and to screen for infection or malignancy in unexplained symptoms.",
        "specimen_type": "Venous whole blood, EDTA tube (lavender top)",
        "collection_notes_en": "No fasting required. Sample should be tested within a few hours of collection, as prolonged storage affects the result. Anemia, pregnancy, and age can all raise ESR independent of inflammation.",
        "methodology_en": "Westergren method (classic reference method: rate of red cell sedimentation in a vertical tube over 1 hour) or automated modified methods calibrated against it.",
        "reference_ranges": [
            {"parameter": "ESR", "population": "Men <50 years", "range": "0-15 mm/hr"},
            {"parameter": "ESR", "population": "Men \u226550 years", "range": "0-20 mm/hr"},
            {"parameter": "ESR", "population": "Women <50 years", "range": "0-20 mm/hr"},
            {"parameter": "ESR", "population": "Women \u226550 years", "range": "0-30 mm/hr"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "ESR is a non-specific marker -- it rises with essentially any inflammatory, infectious, or neoplastic process, and can also be affected by anemia, pregnancy, obesity, and aging independent of disease. It is most useful in monitoring disease activity over time in a known condition (e.g., polymyalgia rheumatica, temporal arteritis) rather than as a standalone diagnostic test. CRP is generally preferred for detecting acute changes, since it rises and falls faster than ESR.",
        "associated_conditions": [
            {"condition": "Polymyalgia rheumatica / giant cell arteritis", "direction": "high, often markedly"},
            {"condition": "Rheumatoid arthritis / other inflammatory arthritis (disease activity monitoring)", "direction": "high"},
            {"condition": "Chronic infection or malignancy (e.g., multiple myeloma)", "direction": "high"}
        ],
        "sources": [{"name": "Hospital for Special Surgery (HSS) - Understanding Rheumatoid Arthritis Blood Test Results", "url": "https://www.hss.edu/health-library/conditions-and-treatments/understanding-rheumatoid-arthritis-lab-tests-results", "accessed": "2026-07-14"}]
    },
    {
        "slug": "rheumatoid-factor", "name_en": "Rheumatoid Factor (RF)", "aliases": "RF",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "Supports the diagnosis of rheumatoid arthritis and helps evaluate other autoimmune/inflammatory conditions, usually alongside anti-CCP antibodies (which are more specific for RA).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Nephelometric or turbidimetric immunoassay on automated analyzers.",
        "reference_ranges": [{"parameter": "Rheumatoid factor", "population": "Adult", "range": "Negative, or <20-30 IU/mL by nephelometry", "notes": "Cutoff varies by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive RF supports but does not confirm rheumatoid arthritis -- it is present in roughly 70-80% of RA patients but also occurs in other autoimmune conditions (Sjogren syndrome, SLE), chronic infections (hepatitis C, endocarditis), and in a smaller percentage of healthy people (especially older adults). Anti-CCP antibodies are more specific for RA and are often tested alongside RF. A negative RF does not exclude RA ('seronegative RA').",
        "associated_conditions": [
            {"condition": "Rheumatoid arthritis", "direction": "positive (70-80% sensitivity)"},
            {"condition": "Sjogren syndrome / SLE / chronic infections", "direction": "positive, non-specific"}
        ],
        "sources": [{"name": "droracle.ai - Normal reference ranges for rheumatoid factor and ESR (clinical reference summary)", "url": "https://www.droracle.ai/articles/990908/what-are-the-normal-reference-ranges-for-rheumatoid-factor", "accessed": "2026-07-14"}]
    },
    {
        "slug": "ana", "name_en": "Antinuclear Antibody (ANA)", "aliases": "ANA, FANA",
        "category": "Immunoassay / Inflammation Markers",
        "purpose_en": "First-line screening test for systemic lupus erythematosus (SLE) and other connective tissue diseases; detects autoantibodies against components of the cell nucleus.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Indirect immunofluorescence (IIF) on Hep-2 cells is the gold-standard method, reporting both a titer (dilution) and a fluorescence pattern (e.g., homogeneous, speckled, nucleolar); solid-phase assays (ELISA, multiplex bead) are also used as screening tools, with reflex IIF titering on positive/equivocal results.",
        "reference_ranges": [{"parameter": "ANA titer", "population": "Negative", "range": "\u22641:40 dilution (varies by lab)"}, {"parameter": "ANA titer", "population": "Significantly positive", "range": "\u22651:160 dilution", "notes": "The 2019 EULAR/ACR SLE classification criteria use \u22651:80 as the entry criterion"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "ANA is highly sensitive for SLE (a negative ANA makes SLE unlikely) but not specific -- roughly 5-15% of the healthy general population is ANA-positive at low titer (1:40), increasing with age, and positivity also occurs in other autoimmune diseases, chronic infections, and malignancy. A positive ANA is never diagnostic alone; the titer, pattern, and specific reflex antibody testing (anti-dsDNA, anti-Sm, anti-SSA/Ro, anti-SSB/La, anti-Scl-70, anti-Jo-1, anti-centromere) together with clinical findings are needed to reach a diagnosis.",
        "associated_conditions": [
            {"condition": "Systemic lupus erythematosus (SLE)", "direction": "positive, high sensitivity"},
            {"condition": "Other connective tissue diseases (Sjogren syndrome, scleroderma, mixed connective tissue disease)", "direction": "positive, pattern-dependent"},
            {"condition": "Low-titer incidental positivity in healthy individuals (especially older adults)", "direction": "positive, low titer, non-pathological"}
        ],
        "sources": [
            {"name": "Medscape/eMedicine - Antinuclear Antibody: Reference Range, Interpretation", "url": "https://emedicine.medscape.com/article/2086616-overview", "accessed": "2026-07-14"},
            {"name": "PMC - The Art of Interpreting Antinuclear Antibodies (ANAs) in Everyday Practice", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12348033/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "troponin", "name_en": "Cardiac Troponin (I or T)", "aliases": "Troponin, cTnI, cTnT, hs-Troponin",
        "category": "Immunoassay / Cardiac Biomarkers",
        "purpose_en": "The preferred and most specific biomarker for diagnosing acute myocardial infarction and myocardial injury; central to acute coronary syndrome (ACS) evaluation in the emergency setting.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Serial measurements (e.g., at presentation and again at 1-3 hours or 3-6 hours depending on the assay/protocol) are standard practice, since a single value is far less informative than the rise-and-fall pattern.",
        "methodology_en": "Chemiluminescent or electrochemiluminescent immunoassay; high-sensitivity troponin (hs-cTn) assays can detect concentrations 10-100 times lower than older-generation assays and are now the standard of care in most emergency settings.",
        "reference_ranges": [{"parameter": "Cardiac troponin", "population": "Reference cutoff concept", "range": "Elevated when above the assay's 99th-percentile upper reference limit", "notes": "Exact numeric cutoffs are highly assay-specific (conventional vs high-sensitivity, troponin I vs T) -- always use the reporting laboratory's own cutoff, never a generic number"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Cardiac troponin rises within 1-3 hours of myocardial injury (earlier with high-sensitivity assays) and can remain elevated for up to 1-2 weeks, making it both sensitive for early detection and useful for confirming a recent event. Elevation above the 99th-percentile cutoff, especially with a rising/falling pattern on serial testing, supports acute myocardial infarction, but troponin can also be elevated in other conditions causing myocardial strain or injury (heart failure, myocarditis, pulmonary embolism, sepsis, renal failure, strenuous exercise) -- so results must always be interpreted alongside the clinical presentation and ECG.",
        "associated_conditions": [
            {"condition": "Acute myocardial infarction", "direction": "high, with rise-and-fall pattern"},
            {"condition": "Myocarditis / pulmonary embolism / sepsis / renal failure (non-ACS causes)", "direction": "high, without classic ACS pattern"}
        ],
        "sources": [
            {"name": "University of Rochester Medical Center - Cardiac Biomarkers (Blood)", "url": "https://www.urmc.rochester.edu/encyclopedia/content?contenttypeid=167&contentid=cardiac_biomarkers", "accessed": "2026-07-14"},
            {"name": "PMC - Cardiac Biomarkers: What Is and What Can Be", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6957084/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "bnp", "name_en": "B-Type Natriuretic Peptide (BNP / NT-proBNP)", "aliases": "BNP, NT-proBNP, Natriuretic Peptide",
        "category": "Immunoassay / Cardiac Biomarkers",
        "purpose_en": "Used to diagnose and gauge the severity of heart failure, and to help distinguish cardiac from non-cardiac causes of dyspnea (shortness of breath).",
        "specimen_type": "Venous serum or plasma (EDTA plasma commonly used for BNP)",
        "collection_notes_en": "No fasting required. Note that BNP and NT-proBNP are metabolized at different rates and have distinct reference ranges -- results must be compared against the range for the specific assay used, not interchanged.",
        "methodology_en": "Chemiluminescent or electrochemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "BNP", "population": "Normal (heart failure unlikely)", "range": "<100 pg/mL", "notes": "NT-proBNP has a separate, generally higher-numbered reference range and age-adjusted cutoffs -- do not apply the BNP cutoff to an NT-proBNP result"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated BNP/NT-proBNP supports a diagnosis of heart failure and correlates broadly with severity, and is used to help distinguish cardiac dyspnea from primarily pulmonary causes. Levels also rise with renal impairment, atrial fibrillation, pulmonary embolism, sepsis, and advancing age, so results must be interpreted in the full clinical context rather than as a standalone diagnostic cutoff, and age/renal-function-adjusted reference ranges are often used, particularly for NT-proBNP.",
        "associated_conditions": [
            {"condition": "Heart failure (diagnosis and severity assessment)", "direction": "high"},
            {"condition": "Renal impairment / atrial fibrillation / pulmonary embolism (non-heart-failure elevation)", "direction": "high, confounding factor"}
        ],
        "sources": [{"name": "SmarterBlood - Cardiac Biomarkers: Troponin, BNP, CK-MB Heart Tests (clinical summary)", "url": "https://www.smarterblood.org/markers/cardiac-biomarkers", "accessed": "2026-07-14"}]
    },
    {
        "slug": "ck-mb", "name_en": "Creatine Kinase-MB (CK-MB)", "aliases": "CK-MB, CPK-MB",
        "category": "Clinical Chemistry / Cardiac Biomarkers",
        "purpose_en": "Historically used cardiac injury marker, now largely superseded by troponin for diagnosing acute MI, but still used in specific settings such as detecting reinfarction shortly after a recent MI, or when troponin assays are unavailable/unreliable (e.g., severe renal failure).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Serial sampling over 24 hours is traditionally used, similar to troponin protocols, though CK-MB has been largely replaced by high-sensitivity troponin in most modern emergency department protocols.",
        "methodology_en": "Immunoassay (mass or activity-based) on automated chemistry/immunoassay analyzers.",
        "reference_ranges": [{"parameter": "CK-MB", "population": "General guidance", "range": "Elevated when >5% of total CK activity, or above the assay-specific upper reference limit", "notes": "Numeric cutoffs are highly assay-dependent; always use the reporting lab's own reference range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "CK-MB rises within 4-6 hours of myocardial injury and typically returns to normal within 1-2 days, making it useful for detecting a new (re-infarction) event in a patient whose troponin is already elevated from a recent MI. It is less specific than troponin, since CK-MB can also rise with skeletal muscle injury, making troponin the preferred marker per AHA/ACC guidelines for primary MI diagnosis.",
        "associated_conditions": [
            {"condition": "Acute myocardial infarction / reinfarction (especially when troponin already elevated)", "direction": "high"},
            {"condition": "Skeletal muscle injury (non-specific elevation)", "direction": "high, without cardiac cause"}
        ],
        "sources": [{"name": "PMC - The Best of Both Worlds: Eliminating CK-MB Testing in the Emergency Department", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8214836/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "psa", "name_en": "Prostate-Specific Antigen (PSA)", "aliases": "PSA, Total PSA",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Used for prostate cancer screening (where locally recommended) and for monitoring known prostate cancer or benign prostatic hyperplasia (BPH).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Should ideally be drawn before a digital rectal exam, prostate biopsy, or ejaculation, all of which can transiently raise PSA; recent urinary tract infection or catheterization can also elevate results.",
        "methodology_en": "Chemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "Total PSA", "population": "Historically used general cutoff", "range": "<4.0 ng/mL", "notes": "Age-specific reference ranges are now generally preferred over a single fixed cutoff; screening/threshold recommendations vary by guideline body and clinical context"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "PSA is prostate-specific but not cancer-specific -- it is also elevated by BPH, prostatitis, and recent prostate manipulation, and a substantial proportion of men with a 'normal' PSA below 4.0 ng/mL still have prostate cancer detected on biopsy, while many men with a modestly elevated PSA do not have cancer. The free-to-total PSA ratio and PSA velocity (rate of change over time) can help refine risk assessment. PSA screening decisions should follow current, locally-endorsed clinical guidelines given the trade-offs between early detection and overdiagnosis.",
        "associated_conditions": [
            {"condition": "Prostate cancer", "direction": "high (imperfect sensitivity and specificity)"},
            {"condition": "Benign prostatic hyperplasia (BPH) / prostatitis", "direction": "high, non-malignant cause"}
        ],
        "sources": [{"name": "ScienceDirect Topics - Elevated Alpha-Fetoprotein (includes PSA reference discussion)", "url": "https://www.sciencedirect.com/topics/medicine-and-dentistry/elevated-alpha-fetoprotein", "accessed": "2026-07-14"}]
    },
    {
        "slug": "afp", "name_en": "Alpha-Fetoprotein (AFP)", "aliases": "AFP",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Tumor marker used to help diagnose and monitor hepatocellular carcinoma and non-seminomatous germ cell tumors (testicular/ovarian); also used in maternal serum screening during pregnancy for neural tube defects and certain chromosomal conditions (a separate, pregnancy-specific application).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Results are not meaningful during pregnancy for the oncologic application (AFP is physiologically elevated) -- pregnancy-related AFP screening uses separate, gestational-age-specific reference ranges.",
        "methodology_en": "Chemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "AFP", "population": "Non-pregnant adult", "range": "<10-15 ng/mL (\u00b5g/L)", "notes": "Essentially undetectable in healthy adult men and non-pregnant women"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Markedly elevated AFP in a patient with liver disease or a liver mass strongly supports hepatocellular carcinoma, and AFP is used both diagnostically and to monitor treatment response (a falling AFP after treatment is reassuring; a persistently high or rising level suggests residual/recurrent disease). AFP is also elevated in non-seminomatous germ cell tumors (embryonal carcinoma, yolk sac tumor) but not in pure seminoma or choriocarcinoma -- helping distinguish these tumor types alongside beta-hCG and LDH.",
        "associated_conditions": [
            {"condition": "Hepatocellular carcinoma", "direction": "high"},
            {"condition": "Non-seminomatous germ cell tumors (testicular/ovarian)", "direction": "high"},
            {"condition": "Pregnancy (physiological elevation, separate reference ranges apply)", "direction": "high, non-pathological in pregnancy"}
        ],
        "sources": [{"name": "ScienceDirect Topics - Elevated Alpha-Fetoprotein", "url": "https://www.sciencedirect.com/topics/medicine-and-dentistry/elevated-alpha-fetoprotein", "accessed": "2026-07-14"}]
    },
    {
        "slug": "cea", "name_en": "Carcinoembryonic Antigen (CEA)", "aliases": "CEA",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Tumor marker primarily used to monitor treatment response and detect recurrence in colorectal cancer; also used, less specifically, in some other GI and gynecological malignancies.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Smoking can modestly raise CEA even without malignancy.",
        "methodology_en": "Chemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "CEA", "population": "Non-smoking adult", "range": "<5 ng/mL", "notes": "Smokers may have a modestly higher normal range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "CEA is not recommended as a general cancer screening test due to low sensitivity and specificity for early disease, but it is well-established for postoperative surveillance in colorectal cancer -- a rising CEA after treatment raises concern for recurrence and prompts further imaging workup. Non-malignant causes of mild elevation include smoking, inflammatory bowel disease, pancreatitis, and liver disease.",
        "associated_conditions": [
            {"condition": "Colorectal cancer recurrence (postoperative monitoring)", "direction": "rising trend after treatment"},
            {"condition": "Smoking / inflammatory bowel disease / pancreatitis (non-malignant elevation)", "direction": "mildly high, non-specific"}
        ],
        "sources": [{"name": "PMC - Serum CA19-9, CA-125 and CEA as tumor markers for mucinous ovarian tumors (cites standard CEA reference range)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7693209/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "ca-125", "name_en": "Cancer Antigen 125 (CA-125)", "aliases": "CA-125, CA125",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Tumor marker primarily used to monitor treatment response and detect recurrence in epithelial ovarian cancer; also used as part of risk-of-malignancy assessment for an adnexal mass alongside imaging.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Levels fluctuate with the menstrual cycle and are commonly elevated by benign conditions (endometriosis, fibroids, pelvic inflammatory disease, pregnancy, menstruation), limiting its use as a standalone screening test.",
        "methodology_en": "Chemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "CA-125", "population": "Adult", "range": "<35 U/mL"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Roughly 85% of women with epithelial ovarian cancer have an elevated CA-125, but it is not specific -- many benign gynecological conditions also raise it, so CA-125 is not recommended as a general population screening test for ovarian cancer. It is most useful for monitoring known ovarian cancer during and after treatment, where a rising trend suggests recurrence, and as one input (alongside imaging and menopausal status) in risk-of-malignancy algorithms for an incidentally found ovarian mass.",
        "associated_conditions": [
            {"condition": "Epithelial ovarian cancer (monitoring/recurrence)", "direction": "high, rising trend after treatment"},
            {"condition": "Endometriosis / fibroids / pelvic inflammatory disease / pregnancy (benign causes)", "direction": "mildly-moderately high, non-malignant"}
        ],
        "sources": [{"name": "PMC - Serum CA19-9, CA-125 and CEA as tumor markers for mucinous ovarian tumors", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7693209/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "ca19-9", "name_en": "Cancer Antigen 19-9 (CA 19-9)", "aliases": "CA 19-9, CA19-9",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Tumor marker primarily used to help differentiate pancreatic cancer from other conditions and to monitor treatment response/recurrence; also used in some biliary tract and colorectal cancers.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Individuals who are Lewis antigen-negative (a minority of the population) cannot produce CA 19-9 and will have a falsely low/undetectable result regardless of tumor burden.",
        "methodology_en": "Chemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "CA 19-9", "population": "Adult", "range": "<37 U/mL"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "CA 19-9 is not sensitive or specific enough for pancreatic cancer screening in the general population, but is useful for monitoring known pancreatic or biliary tract cancer, where a marked or rising elevation after treatment suggests residual/recurrent disease. Benign causes of elevation include cholestasis/biliary obstruction, pancreatitis, and other GI inflammatory conditions -- an elevated CA 19-9 with biliary obstruction should be reassessed after the obstruction resolves.",
        "associated_conditions": [
            {"condition": "Pancreatic cancer (monitoring/recurrence)", "direction": "high, rising trend"},
            {"condition": "Biliary obstruction / cholestasis / pancreatitis (benign elevation)", "direction": "high, non-malignant"}
        ],
        "sources": [{"name": "Medscape/eMedicine - CA 19-9: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2087513-overview", "accessed": "2026-07-14"}]
    },
    {
        "slug": "ca15-3", "name_en": "Cancer Antigen 15-3 (CA 15-3)", "aliases": "CA 15-3, CA15-3",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Tumor marker used mainly to monitor treatment response and detect recurrence in breast cancer; not recommended for screening or initial diagnosis.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Chemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "CA 15-3", "population": "Adult", "range": "<25 U/mL"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "CA 15-3 is often normal in early-stage breast cancer, limiting its use for screening or diagnosis; it is used mainly for monitoring metastatic or advanced breast cancer during and after treatment, where trends over serial measurements are more informative than any single value. Benign conditions such as liver disease, cirrhosis, hepatitis, and benign breast disease can also elevate it.",
        "associated_conditions": [
            {"condition": "Breast cancer (monitoring metastatic/advanced disease)", "direction": "high, rising trend suggests progression"},
            {"condition": "Liver disease / benign breast disease (non-malignant elevation)", "direction": "high, non-specific"}
        ],
        "sources": [{"name": "PMC - Diagnostic Role of Tumour Markers CEA, CA15-3, CA19-9 and CA125 in Lung Cancer", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3547445/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "blood-donor-tti-screening", "name_en": "Blood Donor Infectious Disease Screening Panel (TTI Panel)",
        "aliases": "TTI Screening, Donor Screening Panel, HIV/HBsAg/HCV/Syphilis Panel",
        "category": "Blood Bank / Immunohematology",
        "purpose_en": "Mandatory screening of every blood donation for the major transfusion-transmissible infections (TTIs), performed before any unit is released for clinical use, per WHO minimum requirements and national blood safety regulations.",
        "specimen_type": "Venous whole blood/serum, collected from the donor at the time of donation",
        "collection_notes_en": "Testing is performed on every single donation, not just at first-time donor screening; positive/reactive results trigger donor notification, deferral, and confirmatory testing protocols per institutional and national blood safety policy.",
        "methodology_en": "Chemiluminescent microparticle immunoassay (CMIA) or ELISA for HIV Ag/Ab combo, HBsAg, and anti-HCV Ab/Ag; treponemal antibody assay (or RPR/VDRL with treponemal confirmation) for syphilis. Nucleic acid testing (NAT) is used in many blood services in addition to serology to shorten the diagnostic window period.",
        "reference_ranges": [
            {"parameter": "HIV-1/2 Ag/Ab", "population": "Result categories", "range": "Non-reactive (required for release) or Reactive"},
            {"parameter": "HBsAg (Hepatitis B surface antigen)", "population": "Result categories", "range": "Non-reactive (required for release) or Reactive"},
            {"parameter": "Anti-HCV Ab/Ag", "population": "Result categories", "range": "Non-reactive (required for release) or Reactive"},
            {"parameter": "Treponemal antibody (Syphilis)", "population": "Result categories", "range": "Non-reactive (required for release) or Reactive"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Per WHO guidance, only donations that are non-reactive on all four mandatory markers should be released for clinical or manufacturing use. A reactive screening result requires the unit to be discarded, the donor to be deferred, and confirmatory/supplemental testing plus donor notification and counseling per national protocol. Even with universal serologic and NAT screening, a small residual risk remains during the 'window period' (the interval after infection before markers become detectable), which is part of the rationale for combining serology with NAT in many blood services and for maintaining strict donor risk-history screening as a complementary safeguard.",
        "associated_conditions": [
            {"condition": "HIV, Hepatitis B, Hepatitis C, or syphilis infection in the donor", "direction": "reactive result -- unit discarded, donor deferred"},
            {"condition": "Window-period infection (recently acquired, not yet detectable)", "direction": "false-negative risk despite screening -- rationale for NAT and donor history screening"}
        ],
        "sources": [
            {"name": "NCBI Bookshelf / WHO - Screening for transfusion-transmissible infections", "url": "https://www.ncbi.nlm.nih.gov/books/NBK142989/", "accessed": "2026-07-14"},
            {"name": "PMC - Blood Supply Testing for Infectious Diseases", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7157473/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "amylase", "name_en": "Amylase, Serum", "aliases": "Serum Amylase",
        "category": "Clinical Chemistry",
        "purpose_en": "Used, alongside lipase, to help diagnose and monitor acute pancreatitis and other pancreatic disorders.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Enzymatic kinetic assay on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Serum amylase", "population": "Adult", "range": "40-140 U/L"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Serum amylase rises within 6-48 hours of acute pancreatitis onset but does not correlate with disease severity, and typically normalizes within 3-5 days -- lipase is generally preferred because it stays elevated longer and is more pancreas-specific. Amylase can also be elevated in non-pancreatic conditions such as bowel perforation, peptic ulcer penetration, salivary gland disease (mumps, parotitis), and macroamylasemia.",
        "associated_conditions": [
            {"condition": "Acute pancreatitis", "direction": "high, rises within 6-48h"},
            {"condition": "Salivary gland disease (mumps, parotitis) / bowel perforation (non-pancreatic causes)", "direction": "high, non-specific"}
        ],
        "sources": [{"name": "Medscape/eMedicine - Amylase: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2054386-overview", "accessed": "2026-07-14"}]
    },
    {
        "slug": "lipase", "name_en": "Lipase, Serum", "aliases": "Serum Lipase",
        "category": "Clinical Chemistry",
        "purpose_en": "The preferred enzyme marker (alongside or instead of amylase) for diagnosing and monitoring acute pancreatitis, due to its greater pancreas-specificity and longer window of elevation.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Enzymatic kinetic assay on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Serum lipase", "population": "Adult", "range": "7-60 U/L", "notes": "Varies by lab/assay"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Lipase greater than 3x the upper limit of normal, in the appropriate clinical context (epigastric pain radiating to the back, nausea/vomiting), is one of the diagnostic criteria for acute pancreatitis. Lipase remains elevated longer than amylase (up to 8-14 days), making it useful even when a patient presents somewhat later in the course of illness. It is more specific to the pancreas than amylase, though renal failure and some non-pancreatic abdominal conditions can also raise it.",
        "associated_conditions": [
            {"condition": "Acute pancreatitis", "direction": "high, typically >3x upper limit of normal"},
            {"condition": "Renal failure (reduced clearance, non-pancreatic elevation)", "direction": "mildly high, non-specific"}
        ],
        "sources": [{"name": "Clinical trial protocol reference range compilation (multi-site laboratory reference table)", "url": "https://cdn.clinicaltrials.gov/large-docs/87/NCT05025787/Prot_002.pdf", "accessed": "2026-07-14"}]
    },
    {
        "slug": "beta-hcg", "name_en": "Human Chorionic Gonadotropin, Beta Subunit (Beta-hCG)", "aliases": "hCG, Beta-hCG, Pregnancy Test (Quantitative)",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Confirms and monitors early pregnancy; also used as a tumor marker in suspected gestational trophoblastic disease and, alongside AFP and LDH, in the workup of suspected testicular/germ cell tumors.",
        "specimen_type": "Venous serum or plasma (quantitative); urine (qualitative point-of-care testing)",
        "collection_notes_en": "No fasting required. Serial quantitative levels (drawn 48 hours apart) are used in early pregnancy to assess whether a pregnancy is progressing normally (levels should roughly double every 48-72 hours in early normal pregnancy) or raise concern for ectopic pregnancy/miscarriage.",
        "methodology_en": "Chemiluminescent immunoassay (quantitative, serum) or lateral-flow immunochromatographic assay (qualitative, urine point-of-care).",
        "reference_ranges": [
            {"parameter": "Beta-hCG", "population": "Non-pregnant", "range": "<5 mIU/mL"},
            {"parameter": "Beta-hCG", "population": "Early pregnancy detection threshold", "range": "\u226525 mIU/mL typically detectable, often positive by ~2-3 days before expected menses"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A positive/detectable hCG confirms pregnancy; quantitative serial levels that fail to roughly double over 48-72 hours in early pregnancy raise concern for an ectopic pregnancy or a failing intrauterine pregnancy and prompt further evaluation (ultrasound correlation). Markedly elevated hCG for gestational age can suggest multiple gestation or gestational trophoblastic disease (molar pregnancy). Outside of pregnancy, elevated hCG can indicate a germ cell tumor or, rarely, other malignancies.",
        "associated_conditions": [
            {"condition": "Normal early pregnancy", "direction": "positive, appropriately rising serial levels"},
            {"condition": "Ectopic pregnancy / failing pregnancy", "direction": "positive, abnormally slow rise or fall"},
            {"condition": "Gestational trophoblastic disease (molar pregnancy)", "direction": "markedly high for gestational age"},
            {"condition": "Germ cell tumors (non-pregnant)", "direction": "high"}
        ],
        "sources": [{"name": "Children's Minnesota Lab Reference - Pregnancy Test, Urine (hCG kinetics in early pregnancy)", "url": "https://www.childrensmn.org/references/lab/urinestool/pregnancy-test-urine.pdf", "accessed": "2026-07-14"}]
    },
    {
        "slug": "urinalysis", "name_en": "Urinalysis (Routine)", "aliases": "UA, Urine Analysis, Routine Urinalysis",
        "category": "Clinical Chemistry / Urinalysis",
        "purpose_en": "Broad screening test for urinary tract, kidney, and metabolic disorders, evaluating the physical, chemical, and microscopic characteristics of urine in a single panel.",
        "specimen_type": "Random, first-morning, or clean-catch midstream urine (clean-catch preferred to reduce contamination for culture correlation)",
        "collection_notes_en": "First-morning specimens are most concentrated and preferred when feasible; clean-catch technique reduces contamination that can confound interpretation (especially white cells/bacteria).",
        "methodology_en": "Physical examination (color, clarity), chemical analysis by reagent dipstick (pH, specific gravity, protein, glucose, ketones, blood, leukocyte esterase, nitrite, bilirubin, urobilinogen), and microscopic examination of urine sediment (red cells, white cells, casts, crystals, bacteria) when indicated.",
        "reference_ranges": [
            {"parameter": "Color/clarity", "population": "Normal", "range": "Pale yellow to amber, clear"},
            {"parameter": "Specific gravity", "population": "Normal", "range": "1.005-1.030"},
            {"parameter": "pH", "population": "Normal", "range": "4.5-8.0"},
            {"parameter": "Protein, glucose, ketones, blood, leukocyte esterase, nitrite, bilirubin", "population": "Normal", "range": "Negative"},
            {"parameter": "Microscopic RBC/WBC", "population": "Normal", "range": "0-2 RBC/hpf; 0-5 WBC/hpf (varies by lab)"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Protein or blood on dipstick prompts further evaluation for glomerular or urinary tract disease (and quantitative urine protein/albumin-creatinine ratio if persistent). Leukocyte esterase and nitrite positivity suggest urinary tract infection, ideally confirmed with urine culture. Glucose and ketones can indicate diabetes/diabetic ketoacidosis. Microscopic findings such as red cell casts, white cell casts, or specific crystal types point toward particular kidney diseases and require correlation with the full clinical picture -- urinalysis is a screening tool, not a standalone diagnosis.",
        "associated_conditions": [
            {"condition": "Urinary tract infection", "direction": "positive leukocyte esterase/nitrite, pyuria"},
            {"condition": "Glomerular disease / nephrotic or nephritic syndrome", "direction": "proteinuria and/or hematuria, possible casts"},
            {"condition": "Diabetes mellitus / diabetic ketoacidosis", "direction": "glucosuria and/or ketonuria"}
        ],
        "sources": [{"name": "MedlinePlus (NIH/NLM) - Basic Metabolic Panel reference table cross-referenced with standard urinalysis parameters", "url": "https://medlineplus.gov/lab-tests/basic-metabolic-panel-bmp/", "accessed": "2026-07-14"}]
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
