"""
Seed script (batch 20) for MedForsa GCC's Lab Info reference library.
Adds 10 tests: LDH, Haptoglobin, 17-OH Progesterone, Aldosterone/Renin Ratio,
AMH, Beta-2 Microglobulin, Alpha-1 Antitrypsin, SHBG, ACTH, Factor VIII Activity.

Run once: python3 seed_lab_tests_batch20.py
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")

TESTS = [
    {
        "slug": "ldh", "name_en": "Lactate Dehydrogenase (LDH), Serum",
        "aliases": "LDH, Lactic Dehydrogenase",
        "category": "Clinical Chemistry",
        "purpose_en": "Nonspecific marker of cell/tissue damage and turnover; used in hemolysis workup, as part of tumor marker panels (germ cell tumors, lymphoma), and to assess tissue injury (e.g., muscle, liver, myocardial).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Avoid hemolysis during collection, since red cells contain high LDH concentrations and in-vitro hemolysis will falsely raise results.",
        "methodology_en": "Enzymatic kinetic assay (lactate-to-pyruvate conversion, measuring NADH formation) on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "LDH", "population": "Adult", "range": "~140-280 U/L", "notes": "Reference ranges vary meaningfully between labs/methods (some report up to 333 U/L); always confirm against the reporting lab's range"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Elevated LDH is a nonspecific finding seen in hemolysis, myocardial infarction, hepatitis, muscle injury, pulmonary infarction, and many malignancies (notably germ cell tumors and lymphoma, where it is used as a prognostic marker). In suspected hemolytic anemia, elevated LDH together with low haptoglobin and elevated indirect bilirubin supports the diagnosis, though a meaningful minority of confirmed hemolytic anemia cases (roughly 25% in some case series) can have a normal LDH, so a normal result does not exclude hemolysis. LDH lacks organ specificity on its own; isoenzyme fractionation (historically used to help localize the source, e.g., a 'flipped' LDH1:LDH2 ratio in myocardial infarction) has been largely superseded by more specific tests like troponin.",
        "associated_conditions": [
            {"condition": "Hemolytic anemia", "direction": "high, alongside low haptoglobin and high indirect bilirubin"},
            {"condition": "Germ cell tumors / lymphoma (tumor burden marker)", "direction": "high"},
            {"condition": "Tissue injury (myocardial, hepatic, muscle, pulmonary infarction)", "direction": "high"}
        ],
        "critical_values_en": None,
        "interfering_factors_en": "In-vitro hemolysis during or after sample collection is a major cause of falsely elevated results, since red blood cells contain LDH concentrations far exceeding plasma -- a hemolyzed sample should prompt a repeat draw before an elevated LDH is acted upon in isolation.",
        "questions_to_ask_en": "Given my other results (haptoglobin, bilirubin, reticulocyte count), does this LDH level support a diagnosis of hemolysis or point to a different cause? If I have a known tumor, how is my LDH being used to guide prognosis or treatment monitoring? Do I need further testing to identify the source of an elevated LDH?",
        "next_steps": "An isolated elevated LDH is usually interpreted alongside other tests (haptoglobin, bilirubin, reticulocyte count for hemolysis; troponin for cardiac injury; liver enzymes for hepatic injury) rather than acted on by itself, since LDH alone doesn't identify the source. In oncology, LDH is often tracked serially as part of established prognostic scoring systems and treatment monitoring.",
        "sources": [
            {"name": "The Role of the LDH Test in Diagnosing Haemolytic Anaemia - Lupin Diagnostics (clinical reference range synthesis)", "url": "https://www.lupindiagnostics.com/blog/chemistry/the-role-of-the-ldh-test-in-diagnosing-hemolytic-anemia", "accessed": "2026-07-14"},
            {"name": "droracle.ai - Significance of Lactate Dehydrogenase (LDH) and Haptoglobin (clinical synthesis)", "url": "https://www.droracle.ai/articles/111831/what-is-the-significance-of-lactate-dehydrogenase-ldh-and", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "haptoglobin", "name_en": "Haptoglobin, Serum",
        "aliases": "Haptoglobin",
        "category": "Clinical Chemistry / Hematology",
        "purpose_en": "Key marker of intravascular hemolysis -- haptoglobin binds and clears free hemoglobin released from destroyed red cells, so its level falls as it is consumed during active hemolysis.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. As an acute-phase reactant, results should be interpreted with awareness of concurrent inflammation, which can raise haptoglobin independent of hemolysis.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay on automated chemistry analyzers.",
        "reference_ranges": [{"parameter": "Haptoglobin", "population": "Adult", "range": "~30-200 mg/dL", "notes": "Reference range varies by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low or undetectable haptoglobin, together with elevated LDH and indirect bilirubin, supports a diagnosis of hemolytic anemia -- haptoglobin is consumed as it binds free hemoglobin, making it one of the more specific markers of hemolysis (particularly intravascular hemolysis). As a positive acute-phase reactant, haptoglobin can also rise with inflammation, infection, or malignancy, which can mask a mild concurrent hemolytic process -- a 'normal' haptoglobin in an acutely ill patient does not fully exclude hemolysis. Absent or very low haptoglobin can also reflect a rare congenital haptoglobin deficiency (anhaptoglobinemia), more common in some populations, which is not itself pathologic.",
        "associated_conditions": [
            {"condition": "Hemolytic anemia (especially intravascular)", "direction": "low/undetectable"},
            {"condition": "Acute-phase response (inflammation, infection, malignancy) masking hemolysis", "direction": "high, potentially obscuring a concurrent low value"},
            {"condition": "Congenital haptoglobin deficiency (anhaptoglobinemia)", "direction": "very low/absent, without hemolysis"}
        ],
        "critical_values_en": None,
        "interfering_factors_en": "As an acute-phase reactant, concurrent inflammation, infection, or malignancy can elevate haptoglobin and mask a true underlying low level from mild hemolysis -- interpret alongside LDH, indirect bilirubin, and reticulocyte count rather than in isolation.",
        "questions_to_ask_en": "Does my low haptoglobin, together with my other results, confirm active hemolysis? If so, what is the underlying cause, and does it need urgent treatment? If my haptoglobin is normal despite suspected hemolysis, could inflammation be masking a low result?",
        "next_steps": "A low haptoglobin supporting hemolysis typically prompts further workup to identify the cause -- a direct antiglobulin test (Coombs test) to check for immune-mediated hemolysis, peripheral blood smear review, and consideration of hereditary causes (e.g., hemoglobinopathy, G6PD deficiency, hereditary spherocytosis) depending on the clinical picture.",
        "sources": [{"name": "droracle.ai - Significance of Lactate Dehydrogenase (LDH) and Haptoglobin (clinical synthesis)", "url": "https://www.droracle.ai/articles/111831/what-is-the-significance-of-lactate-dehydrogenase-ldh-and", "accessed": "2026-07-14"}]
    },
    {
        "slug": "17-ohp", "name_en": "17-Hydroxyprogesterone (17-OHP), Serum",
        "aliases": "17-OHP, 17-Hydroxyprogesterone",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Primary screening test for congenital adrenal hyperplasia (CAH) due to 21-hydroxylase deficiency, used alongside cortisol and androstenedione; also part of the workup for hirsutism and infertility in women with suspected non-classic CAH.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Morning sample preferred, given adrenal steroid diurnal variation. In equivocal cases, an ACTH stimulation test (with 17-OHP measured before and after synthetic ACTH) improves diagnostic accuracy for non-classic CAH.",
        "methodology_en": "Liquid chromatography-tandem mass spectrometry (LC-MS/MS), the preferred modern method for accuracy at low concentrations and to avoid cross-reactivity issues seen with older immunoassays.",
        "reference_ranges": [
            {"parameter": "17-OHP", "population": "Adult male", "range": "<220 ng/dL"},
            {"parameter": "17-OHP", "population": "Adult female, follicular phase", "range": "<80 ng/dL"},
            {"parameter": "17-OHP", "population": "Adult female, luteal phase", "range": "<285 ng/dL"},
            {"parameter": "17-OHP", "population": "Postmenopausal female", "range": "<51 ng/dL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Markedly elevated 17-OHP (classically several-fold above the upper limit) supports classic congenital adrenal hyperplasia from 21-hydroxylase deficiency, typically diagnosed in infancy via newborn screening. Moderately elevated levels, especially with a level above roughly 30 ng/mL (300 ng/dL) after ACTH stimulation, support non-classic (late-onset) CAH, which can present later in life with hirsutism, irregular menses, or infertility. All three analytes (17-OHP, androstenedione, cortisol) should be measured together, since the two rarer forms of CAH (11-hydroxylase and 17-hydroxylase deficiency) do not show the same 17-OHP elevation pattern and require a different diagnostic approach (deoxycorticosterone and progesterone, respectively).",
        "associated_conditions": [
            {"condition": "Classic congenital adrenal hyperplasia (21-hydroxylase deficiency)", "direction": "markedly high"},
            {"condition": "Non-classic (late-onset) congenital adrenal hyperplasia", "direction": "moderately high, especially post-ACTH stimulation"},
            {"condition": "17-alpha-hydroxylase deficiency (rare)", "direction": "low, with elevated mineralocorticoid precursors instead"}
        ],
        "sources": [{"name": "Mayo Clinic Laboratories - 17-Hydroxyprogesterone, Serum (test catalog)", "url": "https://pediatric.testcatalog.org/show/OHPG", "accessed": "2026-07-14"}]
    },
    {
        "slug": "aldosterone-renin-ratio", "name_en": "Aldosterone and Renin (Aldosterone-Renin Ratio)",
        "aliases": "ARR, Aldosterone-Renin Ratio, Plasma Aldosterone Concentration, Plasma Renin Activity, PAC, PRA",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Recommended first-line screening test for primary aldosteronism (Conn syndrome), the most common identifiable and curable cause of secondary hypertension; ordered in patients with resistant hypertension, hypertension with hypokalemia, or hypertension with an adrenal incidentaloma.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Testing should ideally be done seated after being upright for at least 2 hours, mid-morning; potassium should be corrected before testing (hypokalemia suppresses aldosterone and can mask the diagnosis); spironolactone/eplerenone must be stopped for 4-6 weeks before testing, and other antihypertensives that affect the renin-aldosterone axis (beta-blockers, ACE inhibitors, ARBs, diuretics) are ideally adjusted per endocrinology guidance, though the screening test can still be performed on most other medications with appropriate interpretation caveats.",
        "methodology_en": "Plasma aldosterone concentration (PAC) measured by immunoassay or LC-MS/MS; renin measured either as plasma renin activity (PRA, an enzymatic assay) or direct renin concentration (DRC, an immunoassay) -- the two renin methods are not directly interchangeable, and conversion factors vary by laboratory.",
        "reference_ranges": [{"parameter": "Aldosterone-Renin Ratio (ARR)", "population": "Positive screen threshold", "range": "\u226520-30 (ng/dL)/(ng/mL/h) with PAC \u226515 ng/dL (using PRA); ratio cutoffs differ when direct renin concentration is used instead", "notes": "Exact cutoff varies by guideline/laboratory; both PAC and the ratio must be elevated together for the screen to be considered positive"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "A high ARR (elevated aldosterone relative to suppressed renin) with PAC above the threshold is a positive screening result for primary aldosteronism and warrants confirmatory testing (e.g., saline infusion test, oral sodium loading test) before subtype classification (adrenal adenoma vs. bilateral adrenal hyperplasia) via adrenal CT and, often, adrenal venous sampling. A low ARR with elevated renin instead suggests secondary hyperaldosteronism (renal artery stenosis, heart failure, cirrhosis with ascites, diuretic use) rather than a primary adrenal cause. ACE inhibitors and ARBs can falsely elevate renin, potentially masking primary aldosteronism (a low/undetectable renin on an ACE inhibitor is actually a strong predictor of primary aldosteronism despite the medication).",
        "critical_values_en": None,
        "interfering_factors_en": "Spironolactone and eplerenone must be stopped 4-6 weeks before testing, as they invalidate results. Beta-blockers can lower renin (falsely raising the ratio); ACE inhibitors/ARBs and diuretics can raise renin (potentially masking a true positive ratio, though a suppressed renin despite an ACE inhibitor still strongly suggests primary aldosteronism). Posture (supine vs. upright), time of day, and dietary sodium intake at the time of the blood draw significantly affect both aldosterone and renin and must be standardized per the testing protocol.",
        "questions_to_ask_en": "Does my result require confirmatory testing before a diagnosis is made? Do any of my current blood pressure medications need to be adjusted or stopped before repeating this test for an accurate result? If primary aldosteronism is confirmed, what additional imaging or testing (adrenal CT, adrenal venous sampling) will be needed to determine the best treatment (surgery vs. medication)?",
        "next_steps": "A positive screen (high ARR with elevated PAC) is followed by a confirmatory test (such as saline infusion or oral sodium loading) to establish the diagnosis, since the screening ratio alone has a meaningful false-positive rate. A confirmed diagnosis leads to adrenal CT imaging and, in surgical candidates, adrenal venous sampling to determine whether the source is unilateral (favoring surgery) or bilateral (favoring mineralocorticoid receptor antagonist therapy).",
        "associated_conditions": [
            {"condition": "Primary aldosteronism (adrenal adenoma or bilateral hyperplasia)", "direction": "high aldosterone, suppressed renin -- high ratio"},
            {"condition": "Secondary hyperaldosteronism (renal artery stenosis, heart failure, cirrhosis)", "direction": "high aldosterone, high renin -- normal/low ratio"}
        ],
        "sources": [
            {"name": "Mayo Clinic Laboratories - Aldosterone, Serum and Renin Activity, Plasma (test catalog)", "url": "https://endocrinology.testcatalog.org/show/ALDS", "accessed": "2026-07-14"},
            {"name": "Cleveland Clinic Journal of Medicine - Our evolving understanding of primary aldosteronism (Endocrine Society guideline summary)", "url": "https://www.ccjm.org/content/88/4/221", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "amh", "name_en": "Anti-Mullerian Hormone (AMH), Serum",
        "aliases": "AMH, Anti-Mullerian Hormone",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Assesses ovarian reserve (the remaining egg supply) for fertility counseling and IVF stimulation planning; also used to help diagnose PCOS (where AMH is often elevated) and to predict menopause timing in some contexts.",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "Can be drawn on any day of the menstrual cycle (unlike FSH/estradiol), since AMH shows relatively little cycle-dependent variation compared to other reproductive hormones, though some intra- and inter-cycle variability has been documented with newer, more sensitive assays.",
        "methodology_en": "Chemiluminescent or enzyme immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "AMH", "population": "Reproductive-age woman, general reference", "range": "~1.0-4.0 ng/mL", "notes": "Strongly age-dependent -- peaks around age 25 and declines steadily thereafter; no single universal cutoff exists, and age-specific nomograms are increasingly used"},
            {"parameter": "AMH", "population": "Diminished ovarian reserve (commonly cited threshold)", "range": "<1.0-1.1 ng/mL"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low AMH indicates diminished ovarian reserve and is associated with a reduced number of eggs retrieved during IVF stimulation, though it does not directly predict egg quality or the ability to conceive naturally, and should not be used alone to counsel a woman against attempting pregnancy. AMH declines with age and becomes undetectable around menopause. Elevated AMH is commonly seen in polycystic ovary syndrome (PCOS), reflecting the increased number of small antral follicles characteristic of that condition, and is sometimes used as a supportive (though not diagnostic) marker in PCOS evaluation.",
        "associated_conditions": [
            {"condition": "Diminished ovarian reserve", "direction": "low"},
            {"condition": "Polycystic ovary syndrome (PCOS)", "direction": "high"},
            {"condition": "Premature ovarian insufficiency", "direction": "very low/undetectable"}
        ],
        "questions_to_ask_en": "Given my age, how should my AMH level be interpreted -- is it typical for my age group or lower/higher than expected? Does this result change my fertility treatment plan or timeline? Should this be repeated, or combined with antral follicle count, for a fuller picture of my ovarian reserve? If elevated, does this support a PCOS diagnosis alongside my other symptoms/tests?",
        "next_steps": "Low AMH in someone considering pregnancy often prompts a conversation about timelines and, if fertility treatment is being considered, about expected response to ovarian stimulation. AMH is typically interpreted alongside antral follicle count (by ultrasound) and FSH for the most complete ovarian reserve assessment, rather than as a standalone test.",
        "sources": [
            {"name": "MedPark Hospital - Anti-Mullerian Hormone (AMH) Test: Levels, Results", "url": "https://www.medparkhospital.com/en-US/disease-and-treatment/anti-mullerian-hormone-test", "accessed": "2026-07-14"},
            {"name": "PMC - Using anti-Mullerian hormone to predict premature ovarian insufficiency (Bologna Criteria threshold)", "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11611575/", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "beta-2-microglobulin", "name_en": "Beta-2 Microglobulin, Serum",
        "aliases": "B2M, Beta-2 Microglobulin",
        "category": "Immunoassay / Tumor Markers",
        "purpose_en": "Prognostic marker in multiple myeloma, chronic lymphocytic leukemia, and lymphoma (higher levels correlate with greater tumor burden and worse prognosis); also used as a marker of kidney function/tubular damage in some settings.",
        "specimen_type": "Venous serum or plasma; also measurable in urine and CSF for specific indications",
        "collection_notes_en": "No fasting required.",
        "methodology_en": "Immunoturbidimetric, immunonephelometric, or chemiluminescent immunoassay.",
        "reference_ranges": [{"parameter": "Beta-2 microglobulin", "population": "Adult", "range": "~1-3 \u00b5g/mL", "notes": "Reference range varies by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "In multiple myeloma, beta-2 microglobulin is a key component of the International Staging System (ISS), with higher levels indicating greater tumor burden and worse prognosis. It is also elevated in lymphoma and chronic lymphocytic leukemia, where it has independent prognostic value for remission duration and survival. Because beta-2 microglobulin is cleared by the kidneys, reduced kidney function (regardless of malignancy) also raises levels, so results must be interpreted alongside renal function -- an elevated level in a patient with impaired kidney function may reflect reduced clearance rather than increased tumor burden.",
        "associated_conditions": [
            {"condition": "Multiple myeloma (staging/prognosis)", "direction": "high, correlates with tumor burden"},
            {"condition": "Lymphoma / chronic lymphocytic leukemia (prognosis)", "direction": "high"},
            {"condition": "Reduced kidney function (non-malignant cause of elevation)", "direction": "high, due to reduced clearance"}
        ],
        "sources": [{"name": "Medscape/eMedicine - Beta2 Microglobulin: Reference Range, Interpretation, Collection and Panels", "url": "https://emedicine.medscape.com/article/2086864-overview", "accessed": "2026-07-14"}]
    },
    {
        "slug": "alpha-1-antitrypsin", "name_en": "Alpha-1 Antitrypsin (A1AT), Serum",
        "aliases": "A1AT, AAT, Alpha-1 Antitrypsin",
        "category": "Clinical Chemistry",
        "purpose_en": "Screens for alpha-1 antitrypsin deficiency, a genetic condition predisposing to early-onset emphysema/COPD (especially in non-smokers or with disproportionate lung disease for smoking history) and liver disease (cirrhosis, hepatocellular carcinoma).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. As a positive acute-phase reactant, a normal or elevated result during acute illness/inflammation does not fully exclude an underlying deficiency allele -- retesting when clinically stable, or direct genotyping/phenotyping, may be needed if suspicion remains.",
        "methodology_en": "Immunoturbidimetric or immunonephelometric assay for quantification; phenotyping (isoelectric focusing) or genotyping is used to identify the specific deficiency allele (e.g., PiZZ, PiSZ) when levels are low.",
        "reference_ranges": [{"parameter": "Alpha-1 antitrypsin (normal M/M phenotype)", "population": "Adult", "range": "~100-273 mg/dL", "notes": "Reference range varies modestly by lab/method"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low alpha-1 antitrypsin suggests a deficiency genotype (most significantly the ZZ genotype, causing severe deficiency), which predisposes to early-onset panacinar emphysema (accelerated by smoking) and can cause liver disease including cirrhosis and hepatocellular carcinoma, since the abnormal protein accumulates and damages hepatocytes. As a positive acute-phase reactant, levels rise with inflammation, infection, or malignancy, which can transiently mask a mild deficiency -- phenotyping or genotyping is more reliable than a single quantitative level when deficiency is strongly suspected clinically.",
        "associated_conditions": [
            {"condition": "Alpha-1 antitrypsin deficiency (e.g., PiZZ genotype)", "direction": "low"},
            {"condition": "Early-onset emphysema/COPD (especially in non-smokers)", "direction": "low, underlying cause"},
            {"condition": "Liver cirrhosis / hepatocellular carcinoma (from protein accumulation)", "direction": "low serum level despite hepatocyte accumulation of abnormal protein"}
        ],
        "sources": [{"name": "PubMed - Reference and interpretive ranges for alpha(1)-antitrypsin quantitation by phenotype in adult and pediatric populations", "url": "https://pubmed.ncbi.nlm.nih.gov/22912357/", "accessed": "2026-07-14"}]
    },
    {
        "slug": "shbg", "name_en": "Sex Hormone-Binding Globulin (SHBG), Serum",
        "aliases": "SHBG",
        "category": "Immunoassay / Reproductive Endocrinology",
        "purpose_en": "Measures the main carrier protein for testosterone and estradiol in blood; used alongside total testosterone to calculate free/bioavailable testosterone, and as a marker of insulin resistance/metabolic risk (low SHBG correlates with insulin resistance).",
        "specimen_type": "Venous serum or plasma",
        "collection_notes_en": "No fasting required. Often ordered together with total testosterone for calculation of free testosterone.",
        "methodology_en": "Chemiluminescent immunoassay on automated immunoassay analyzers.",
        "reference_ranges": [
            {"parameter": "SHBG", "population": "Adult male, 20-49 years", "range": "16.5-55.9 nmol/L"},
            {"parameter": "SHBG", "population": "Adult male, >49 years", "range": "19.3-76.4 nmol/L"},
            {"parameter": "SHBG", "population": "Adult female, 20-49 years", "range": "24.6-122.0 nmol/L"},
            {"parameter": "SHBG", "population": "Adult female, >49 years", "range": "17.3-125.0 nmol/L"}
        ],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low SHBG is associated with obesity, insulin resistance, type 2 diabetes, and non-alcoholic fatty liver disease, and can cause a normal total testosterone to actually reflect low free (bioavailable) testosterone -- or the reverse in a woman with PCOS, where low SHBG amplifies the effect of even modestly elevated total testosterone, worsening clinical hyperandrogenism. High SHBG is seen with estrogen therapy/pregnancy, hyperthyroidism, and liver disease, and can cause a normal or even low-normal total testosterone to still result in adequate free testosterone, or conversely can make total testosterone appear falsely reassuring in true androgen deficiency. SHBG is essential context whenever total testosterone results are borderline or don't match the clinical picture.",
        "associated_conditions": [
            {"condition": "Obesity / insulin resistance / type 2 diabetes / NAFLD", "direction": "low"},
            {"condition": "PCOS (low SHBG amplifying hyperandrogenism)", "direction": "low"},
            {"condition": "Estrogen therapy / pregnancy / hyperthyroidism / liver disease", "direction": "high"}
        ],
        "sources": [{"name": "Labcorp - Sex Hormone-binding Globulin (SHBG), Serum (specialty test catalog)", "url": "https://specialtytesting.labcorp.com/tests/500848/sex-hormone-binding-globulin-shbg-serum", "accessed": "2026-07-14"}]
    },
    {
        "slug": "acth", "name_en": "Adrenocorticotropic Hormone (ACTH), Plasma",
        "aliases": "ACTH, Corticotropin",
        "category": "Immunoassay / Endocrinology",
        "purpose_en": "Evaluates the hypothalamic-pituitary-adrenal axis; used together with cortisol to distinguish primary from secondary/tertiary adrenal insufficiency, and to distinguish ACTH-dependent from ACTH-independent causes of Cushing syndrome.",
        "specimen_type": "Venous plasma, EDTA tube, collected on ice and processed/frozen promptly",
        "collection_notes_en": "Requires morning collection (typically 08:00-09:00h) due to strong diurnal variation (highest early morning, lowest in the evening); the hormone is unstable with a plasma half-life of only about 22-30 minutes, so the sample must be chilled and processed rapidly to avoid falsely low results from ex-vivo degradation. Recent exogenous steroid use (even inhaled or topical) can suppress ACTH and must be noted.",
        "methodology_en": "Chemiluminescent immunoassay (CLIA) on automated immunoassay analyzers.",
        "reference_ranges": [{"parameter": "ACTH", "population": "Adult, morning sample (08:00-09:00h)", "range": "~10-60 pg/mL (2.2-13.3 pmol/L)", "notes": "Levels are physiologically lower in the evening (often <20 pg/mL); reference ranges vary by lab/assay"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "ACTH must always be interpreted alongside a simultaneous cortisol level. Low cortisol with elevated ACTH indicates primary adrenal insufficiency (Addison's disease) -- the adrenal gland cannot respond despite appropriate pituitary stimulation. Low cortisol with low or inappropriately normal ACTH indicates secondary (pituitary) or tertiary (hypothalamic) adrenal insufficiency. In suspected Cushing syndrome, a detectable/normal-to-high ACTH suggests an ACTH-dependent cause (pituitary Cushing disease or ectopic ACTH secretion), while a suppressed/undetectable ACTH suggests an ACTH-independent adrenal source (adrenal adenoma or carcinoma).",
        "critical_values_en": None,
        "interfering_factors_en": "Exogenous corticosteroid use (oral, inhaled, or topical) suppresses endogenous ACTH and invalidates interpretation unless this is specifically accounted for. Physical or emotional stress at the time of the draw can appropriately raise ACTH. Improper sample handling (delayed processing, not kept on ice) causes rapid ex-vivo degradation and falsely low results, given the hormone's very short half-life.",
        "questions_to_ask_en": "Was my cortisol measured at the same time, and how do the two results fit together? Does this pattern point to a pituitary, hypothalamic, or adrenal cause? Do I need additional dynamic testing (e.g., cosyntropin stimulation test, dexamethasone suppression test) to clarify the diagnosis? Could any medications (including inhaled or topical steroids) be affecting this result?",
        "next_steps": "Depending on the ACTH/cortisol pattern, your clinician may order a cosyntropin (synthetic ACTH) stimulation test to confirm adrenal insufficiency, pituitary imaging if a central (secondary/tertiary) cause is suspected, or a dexamethasone suppression test and/or adrenal imaging if Cushing syndrome is being investigated. Results are never used to start or stop steroid treatment without this fuller diagnostic workup.",
        "associated_conditions": [
            {"condition": "Primary adrenal insufficiency (Addison's disease)", "direction": "high, with low cortisol"},
            {"condition": "Secondary/tertiary adrenal insufficiency (pituitary/hypothalamic)", "direction": "low or inappropriately normal, with low cortisol"},
            {"condition": "Cushing disease (pituitary) / ectopic ACTH syndrome", "direction": "detectable/high, with elevated cortisol"},
            {"condition": "Adrenal Cushing syndrome (adenoma/carcinoma)", "direction": "suppressed/undetectable, with elevated cortisol"}
        ],
        "sources": [
            {"name": "University of Rochester Medical Center - ACTH blood test", "url": "https://www.urmc.rochester.edu/encyclopedia/content?contenttypeid=167&contentid=acth_blood", "accessed": "2026-07-14"},
            {"name": "UMass Memorial Health - ACTH (Blood)", "url": "https://www.ummhealth.org/health-library/acth-blood", "accessed": "2026-07-14"}
        ]
    },
    {
        "slug": "factor-viii-activity", "name_en": "Coagulation Factor VIII Activity Assay",
        "aliases": "Factor VIII, F8, FVIII Activity",
        "category": "Hematology / Coagulation",
        "purpose_en": "Diagnoses and classifies severity of hemophilia A (factor VIII deficiency), and helps distinguish von Willebrand disease from hemophilia A (since vWF stabilizes factor VIII, vWD can also cause low factor VIII levels).",
        "specimen_type": "Venous whole blood, sodium citrate tube (light blue top)",
        "collection_notes_en": "Avoid warfarin for 2 weeks and heparin for 2 days before testing when possible; do not draw from a line containing heparin. Sample should reach the lab promptly per the coagulation lab's protocol.",
        "methodology_en": "One-stage clot-based assay (most common) or chromogenic assay on automated coagulation analyzers.",
        "reference_ranges": [{"parameter": "Factor VIII activity", "population": "Adult", "range": "~50-150%", "notes": "Reference range varies by lab/method; results are reported relative to a pooled normal plasma standard"}],
        "reference_ranges_verified": True,
        "clinical_significance_en": "Low factor VIII activity (<40%) with a personal/family history of bleeding supports hemophilia A; severity is classified as severe (<1%), moderate (1-5%), or mild (5-40%), which correlates with bleeding frequency and severity. Because von Willebrand factor carries and stabilizes factor VIII in circulation, von Willebrand disease can also present with reduced factor VIII -- vWF antigen and activity testing are needed to distinguish the two conditions, since their treatment differs. Factor VIII is also an acute-phase reactant and rises with inflammation, stress, and pregnancy, which can transiently normalize a mild deficiency.",
        "associated_conditions": [
            {"condition": "Hemophilia A (factor VIII deficiency)", "direction": "low, isolated (normal vWF)"},
            {"condition": "Von Willebrand disease (factor VIII secondarily reduced)", "direction": "low, with concurrently low/abnormal vWF"}
        ],
        "sources": [{"name": "Mayo Clinic Laboratories - von Willebrand Factor Antigen, Plasma, referencing Factor VIII coagulant activity assay as a companion test", "url": "https://hematology.testcatalog.org/show/VWAG", "accessed": "2026-07-14"}]
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
